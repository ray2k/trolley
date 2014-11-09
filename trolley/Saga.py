import uuid
import inspect
import trolley.Util
from trolley.Util import get_handled_types

class SagaError(BaseException):
	pass

def _validate_handled_type(saga_handler, message_types):
	for h in set(message_types):
		if h == None:
			raise SagaError("Unexpected 'None' in handled message list")
		try:
			h()
		except Exception as e:
			raise SagaError("Unable to create instance of handled message " + str(h), e)

def validate(saga_handler):

	if hasattr(saga_handler, "handle") == False:
		raise SagaError("Saga handler does not have a 'handle' method")
	else: 
		signature = inspect.signature(saga_handler.handle)
		if len(signature.parameters) != 1:
			raise SagaError("Saga handler 'handle' method does not have exactly 1 parameter")

	if hasattr(saga_handler, "handles") == False:
		raise SagaError("Saga handler does not have a 'handles' attribute")
	
	handles = getattr(saga_handler, "handles", None)
	if handles == None:
		raise SagaError("Saga handler does not declare any handled message types")

	if isinstance(handles, list):
		if len(handles) == 0:
			raise SagaError("Saga handler does not declare any handled message types")
		else:
			_validate_handled_type(saga_handler, handles)
	elif isinstance(handles, type):
		_validate_handled_type(saga_handler, [handles])
	else:
		raise SagaError("'handles' attribute must be single type or list of types")

	#initiated_by must exist, be creatable
	if hasattr(saga_handler, "initiated_by") == False:
		raise SagaError("Saga handler does not have a 'initiated_by' attribute")

	initiatedby = getattr(saga_handler, "initiated_by", None)
	if initiatedby == None:
		raise SagaError("Saga handler does not declare an initiator message type")
	if isinstance(initiatedby, type) == False:
		raise SagaError("'initiated_by' attribute must be a single type")
	else:
		try:
			initiatedby()
		except BaseException as e:
			raise SagaError("Unable to create instance of initiator message " + str(h), e)
		
	#saga_data_type must be creatable
	sagaDataType = getattr(saga_handler, "saga_data_type", None)
	if sagaDataType == None:
		raise SagaError("Saga hander does not have a 'saga_data_type' attribute")
	if isinstance(sagaDataType, type) == False:
		raise SagaError("'saga_data_type' attribute must be a single type")
	else:
		try:
			sagaDataType()
		except BaseException as e:
			raise SagaError("Unable to create instance of saga data type " + str(sagaDataType), e)

class SagaData(object):
	def __init__(self):
		self.id = uuid.UUID()

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, value):
		self._id = value

class SagaStorage(object):
	def fetch(self, id):
		pass

	def store(self, saga_data):
		#: :type saga_data: SagaData	
		pass

class InMemorySagaStorage(SagaStorage):
	data = {}

	def get_saga_data(self, id):
		if id in self.data:
			return self.data[id]
		else: 
			return None

	def set_saga_data(self, saga_data):
		#: :type saga_data: SagaData	
		self.data[saga_data.id] = saga_data
		
class Saga:
	initiated_by = None	
	handles = []
	saga_data_type = None

	def __init__(self):
		self._data = None
		self._is_new = False
		self._mappings = {}
		self.configure_mappings()

	def map(self, message_type, handler_func):
		self._mappings[message_type] = handler_func
	
	def can_handle(self, message_type):
		return message_type in self._mappings

	def handle(self, message):
		if type(message) in self._mappings:
			self._mappings[type(message)](message)
		else:
			raise SagaError("No internal handler for type " + str(type(message)))	
	
	def configure_mappings(self):
		pass

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, value):
		self._data = value

	@property
	def is_new(self):
		return self._is_new

	@is_new.setter
	def is_new(self, value):
		self._is_new = value
		
class AutoMappedSagaMixin:	
	def configure_mappings(self):	
		allMethodTuples = inspect.getmembers(self, lambda f: inspect.ismethod(f) or inspect.isfunction(f))
		handleMethodsByname = dict( (x, y) for x, y in allMethodTuples if x.startswith("handle_"))
		
		handledTypes = get_handled_types(self)
		for msgType in handledTypes:
			methodName = "handle_" + msgType.__name__
			if methodName in handleMethodsByname:
				self.map(msgType, handleMethodsByname[methodName])
		
import trolley.Bus
import trolley.Address
import trolley.PickleSerializer
import inspect

def append_module_handlers(sourceMappings, module):
	classes = inspect.getmembers(module, lambda c: inspect.isclass(c));
	for name, cls in classes:
		handledTypes = getattr(cls, "handles", None) #Handles = [FooMessage,BarMessage]
		if isinstance(handledTypes, list):
			map(append_static_handler, [((sourceMappings, msgType) for msgType in handledTypes)])
			#for msgType in handledTypes:
				#append_static_handler(sourceMappings, msgType, cls)
		elif isinstance(handledTypes, type): # Handles = SomeMessage
			append_static_handler(sourceMappings, handledTypes, cls)
			
def append_static_handler(sourceMappings, messageType, handlerType):	
	if messageType not in sourceMappings:
		sourceMappings[messageType] = []
	sourceMappings[messageType].append(handlerType)

def print_handler_mappings(mappings):
	for messageType in mappings:
		for subscriberType in mappings[messageType]:			
			print("Message Type", messageType.__name__, "is handled by", subscriberType.__name__)

class BusConfigurationException(Exception):
	pass		

class BusConfiguration(object):

	def __init__(self):
		self._handlerMappings = {}
		self._ad = None
		self._incoming_transport = None
		self._outgoing_transport = None
		self._default_serializer = None

	def set_incoming_transport(self, incomingTransport):
		self._incoming_transport = incomingTransport
		return self

	def set_outgoing_transport(self, outgoingTransport):
		self._outgoing_transport = outgoingTransport
		return self

	def set_transport(self, duplexTransport):
		self._incoming_transport = duplexTransport
		self._outgoing_transport = duplexTransport
		return self

	def set_address(self, *args, **kwargs):
		self._address = trolley.Address(*args, **kwargs)
		return self

	def auto_subscribe(self, handlerModule):
		append_module_handlers(self._handlerMappings, handlerModule)
		return self

	def subscribe(self, messageType, handlerType):
		append_static_handler(self._handlerMappings, messageType, handlerType)
		return self

	def use_serializer(self, serializerType):
		self._default_serializer = serializerType
		return self

	def create_bus(self):
		if self._address == None:
			raise BusConfigurationException("Address configuration missing")
		if self._incoming_transport == None:
			raise BusConfigurationException("Incoming transport configuration missing")
		if self._outgoing_transport == None:
			raise BusConfigurationException("Outgoing transport configuration missing")
		if len(self._handlerMappings) == 0:
			raise BusConfigurationException("Message handler mapping configuration missing")
		if (self._default_serializer == None):
			self._default_serializer = trolley.PickleSerializer()

		incoming = self._incoming_transport(self._address)
		outgoing = self._outgoing_transport(self._address)

		#def __init__(self, address, incomingTransport, outgoingTransport, handlerMappings, defaultSerializer=None):
		return trolley.Bus(self._address, incoming, outgoing, self._handlerMappings)
		
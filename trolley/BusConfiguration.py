from .Bus import Bus
from .Address import Address
from .PickleSerializer import PickleSerializer
import trolley.Util

class BusConfigurationException(Exception):
	pass		

class BusConfiguration(object):

	def __init__(self):
		self._handlerMappings = {}
		self._ad = None
		self._incoming_transport = None
		self._outgoing_transport = None
		self._default_serializer = None
		self._saga_storage = None

	def set_incoming_transport(self, incomingTransport):
		#: :type incomingTransport: IncomingTransport
		self._incoming_transport = incomingTransport
		return self

	def set_outgoing_transport(self, outgoingTransport):
		#: :type outgoingTransport: OutgoingTransport
		self._outgoing_transport = outgoingTransport
		return self

	def set_transport(self, duplexTransport):
		#: :type duplexTransport: DuplexTransport
		self._incoming_transport = duplexTransport
		self._outgoing_transport = duplexTransport
		return self

	def set_address(self, *args, **kwargs):
		self._address = Address(*args, **kwargs)
		return self

	def auto_subscribe(self, handlerModule):
		trolley.Util.append_module_handlers(self._handlerMappings, handlerModule)
		return self

	def subscribe(self, messageType, handlerType):		
		trolley.Util.append_static_handler(self._handlerMappings, messageType, handlerType)
		return self

	def use_serializer(self, serializerType):
		self._default_serializer = serializerType
		return self

	def use_saga_storage(self, saga_storage_type):
		self._saga_storage = saga_storage_type

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
			self._default_serializer = PickleSerializer()

		incoming = self._incoming_transport(self._address)
		outgoing = self._outgoing_transport(self._address)
		
		sagaStorage = None
		if self._saga_storage != None:
			sagaStorage = self._saga_storage()

		return Bus(self._address, incoming, outgoing, self._handlerMappings, sagaStorage, self._default_serializer)
		
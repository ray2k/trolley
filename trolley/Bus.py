from .Endpoint import Endpoint
from .PickleSerializer import PickleSerializer
from .Dispatcher import Dispatcher
from .SyncWorkerPool import SyncWorkerPool
import threading

class Bus(object):
	def __init__(self, address, incomingTransport, outgoingTransport, handlerMappings, sagaStorage, defaultSerializer=None):
		#: :type address: Address	
		#: :type incomingTransport: IncomingTransport
		#: :type outgoingTransport: OutgoingTransport
		#: :type handlerMappings: dict	
		#: :type sagaStorage: SagaStorage
		#: :type defaultSerializer: Serializer
		
		if defaultSerializer == None:
			defaultSerializer = PickleSerializer()

		self._endpoint = Endpoint(address, incomingTransport, outgoingTransport, defaultSerializer)
		self._is_started = False		
		self._handlerMappings = handlerMappings		
		self._poller = None
		self._saga_storage = sagaStorage
		self._poll_lock = threading.Lock()
		self._stopping = False		
		self._dispatcher = Dispatcher(SyncWorkerPool(), sagaStorage)

	def start(self):
		# sign up for recieve self._endpoint.receive(
		self._endpoint.open()        
		self._is_started = True
		self._poller = threading.Thread(target=self.__poll_endpoint)
		self._poller.start()

	def stop(self):
		# tear down receiving
		self._endpoint.close()
		self._is_started = False

		self._poll_lock.acquire()
		self._stopping = True
		self._poll_lock.release()

		if self._poller != None:
			self._poller.join()

	def publish(self, message):
		self._endpoint.send(message)
		return

	def reply(self, message):
		raise NotImplementedError()
		return

	@property
	def endpoint(self):
		return self._endpoint

	@property
	def is_started(self):
		return self._is_started

	def __poll_endpoint(self):
		while(True):						
			self._poll_lock.acquire()
			if self._stopping == True:
				self._poll_lock.release()
				break
			else:
				self._poll_lock.release()
			
			message = self._endpoint.receive()
			if message != None:
				if type(message) in self._handlerMappings:
					for h in self._handlerMappings[type(message)]:
						self._dispatch_message(message, h())				
	
	def _dispatch_message(self, messageObject, messageHandler):
		self._dispatcher.dispatch(messageObject, messageHandler, self)

	# retrieval strategies: greedy, linear throttle, exponential throttle
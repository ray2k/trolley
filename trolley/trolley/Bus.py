

class Bus(object):
	def __init__(self, address, incomingTransport, outgoingTransport):
		self._endpoint = Endpoint(address, incomingTransport, outgoingTransport)
		self._is_started = False
		return

	def start(self):
		# sign up for recieve self._endpoint.receive(
		self._endpoint.open()        
		self._is_started = True
		return

	def stop(self):
		# tear down receiving
		self._endpoint.close()
		self._is_started = False
		return

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

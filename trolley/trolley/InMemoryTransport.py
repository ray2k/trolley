from trolley.Transport import DuplexTransport
import queue

class InMemoryTransport(DuplexTransport):

	_queue = queue.Queue()

	def __init__(self, address):
		DuplexTransport.__init__(self, address)

	def receive(self):
		if self._queue.empty():
			return None
		else:
			return self._queue.get()

	def send(self, message):
		self._queue.put(message)		
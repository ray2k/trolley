from .Transport import DuplexTransport
import queue

class InMemoryTransport(DuplexTransport):

	_queue = queue.Queue()

	def __init__(self, address):
		DuplexTransport.__init__(self, address)

	def receive(self):
		if InMemoryTransport._queue.empty():
			return None
		else:
			return InMemoryTransport._queue.get()

	def send(self, message):
		InMemoryTransport._queue.put(message)		
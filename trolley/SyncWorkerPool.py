import time

class SyncWorker:
	def __init__(self, message, handler, on_completed):
		self._message = message
		self._handler = handler		
		self._on_completed = on_completed

	def run(self):
		self._handler.handle(self._message)
		self._on_completed(self)


class SyncWorkerPool:

	def __init__(self):
		self._workers = []

	def spawn(self, message, handler):
		worker = SyncWorker(message, handler, self._on_worker_completed)
		self._workers.append(worker)
		worker.run()

	def wait_all(self):
		while len(self._workers) > 0:
			time.sleep(.25)
				
	def _on_worker_completed(self, worker):
		self._workers.remove(worker)
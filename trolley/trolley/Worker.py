
class Foo:
	pass


class SyncWorker:
	def __init__(self, message, handler, on_completed):
		pass
		#self._message = message
		#self._handler = handler		
		#self._on_completed = on_completed

	def run(self):
		pass
		#self._handler.handle(self._message)
		#self._on_completed(self)


class SyncWorkerPool:

	def __init__(self):
		#self._workers = []
		pass

	def spawn(self, message, handler):
		#worker = SyncWorker(message, handler, self._on_worker_completed)
		#self._workers.append(result)
		#worker.run()
		pass

	def wait_all(self):
		pass
		#while len(self._workers) > 0:
			#time.sleep(.25)
				
	def _on_worker_completed(self, worker):
		#self._workers.remove(worker)
		pass
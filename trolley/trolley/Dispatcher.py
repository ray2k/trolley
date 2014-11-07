import inspect
import time

class DispatchError(BaseException):
	pass

class Dispatcher:
	def __init__(self, worker_factory, saga_storage):
		self._worker_factory = worker_factory
		self._saga_storage = saga_storage

	def dispatch(self, message, handler, bus):
		result = []

		correlated = False
		initiator = False		
		correlationId = getattr(message, "correlation_id", None)
		sagaType = getattr(handler, "saga_data_type", None)

		if correlationId != None:
			correlated = True
			initiated = getattr(handler, "initiated_by", None)
			if initiated == type(message).__name__:
				initiator = True

		sagaData = None

		if correlated == True:
			if initiator == True and sagaType != None:
				sagaData = sagaType()
				handler.is_new = True
			else:
				sagaData = self._saga_storage.fetch(correlationId)
				handler.is_new = False
			handler.bus = bus
			handler.data = sagaData

			result.append(self._worker_factory.create(message, handler))
		else:
			result.append(self._worker_factory.create(message, handler))

		# should scan saga handlers at bus startup to store what they handle/are initiated by/saga data types

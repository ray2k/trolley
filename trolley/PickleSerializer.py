from .Serializer import Serializer
from .ContentTypes import ContentTypes
import pickle
import io

class PickleSerializer(Serializer):
	def __init__(self):
		Serializer.__init__(self, ContentTypes.CONTENT_TYPE_BINARY_PICKLE)

	def serialize(self, messageBody):
		theBytes = io.BytesIO()
		pickle.dump(messageBody, theBytes)	
		theBytes.seek(0)
		return theBytes	

	def deserialize(self, input):
		return pickle.load(input)
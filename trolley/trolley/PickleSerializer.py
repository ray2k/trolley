from .Serializer import Serializer
from trolley.ContentTypes import ContentTypes
import pickle
import io

class PickleSerializer(Serializer):
	def __init__(self):
		Serializer.__init__(self, ContentTypes.CONTENT_TYPE_BINARY_PICKLE)

	def serialize(self, messageBody):
		bytes = io.BytesIO()
		pickle.dump(messageBody, bytes)	
		bytes.seek(0)
		return bytes	

	def deserialize(self, input):
		return pickle.load(input)
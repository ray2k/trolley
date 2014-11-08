from .Serializer import Serializer
from .ContentTypes import ContentTypes
import jsonpickle

class JsonPickleSerializer(Serializer):
	def __init__(self):
		Serializer.__init__(self, ContentTypes.CONTENT_TYPE_JSON_PICKLE)

	def serialize(self, messageBody):
		encoded = jsonpickle.encode(messageBody)
		return bytearray(encoded, "utf-8")

	def deserialize(self, input):
		temp = input.decode("utf-8")
		decoded = jsonpickle.decode(temp)	
		return decoded
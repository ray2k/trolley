import abc

class Serializer(object):
    __metaclass__ = abc.ABCMeta
    _serializers = {}

    def __init__(self, contentType):
        if contentType is None:
            raise Exception("contentType is required for all serializers")
        self._content_type = contentType

    @staticmethod
    def register(contentType, serializer_func):
        Serializer._serializers[contentType] = serializer_func

    @staticmethod
    def get_serializer(contentType):
        return Serializer._serializers.get(contentType, None)

    @property
    def content_type(self):
        return self._content_type;

    @abc.abstractmethod
    def serialize(self, messageBody):
        """Implementors should return a byte array representing the serialized content of the messageBody parameter"""
        return

    @abc.abstractmethod
    def deserialize(self, bytes):
        """Implementors should return a new {type_name} initialized by the payload in {bytes}"""
        return  





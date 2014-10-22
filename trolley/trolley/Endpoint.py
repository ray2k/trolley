from trolley import TransportMessage

class Endpoint(object):
    def __init__(self, address, incomingTransport, outgoingTransport, defaultSerializer):
        self._address = address
        self._incomingTransport = incomingTransport
        self._outgoingTransport = outgoingTransport
        self._defaultSerializer = defaultSerializer;
    
    def open(self):
        self._incomingTransport
        return

    def close(self):
        return

    @property 
    def default_serializer(self):
        return self._defaultSerializer;

    @property
    def address(self):
        return self._address;

    def send(self, message):
        transportMessage = TransportMessage()
        transportMessage.body = self.default_serializer.serialize(message);
        transportMessage.content_type = self.default_serializer.content_type;
        transportMessage.message_type = type(message)
        self._outgoingTransport.send(transportMessage)

    def receive(self):
        return
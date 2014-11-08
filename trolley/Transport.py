
class TransportBase():
    def __init__(self, address):
        #: :type address: Address    
        self._address = address

    @property
    def address(self):
        return self._address

class OutgoingTransport(TransportBase):
    def __init__(self, address):
        #: :type address: Address    
        TransportBase.__init__(self, address);

    def send(self, message):
        """Implementors should send the provided TransportMessage over the their chosen medium"""
        return

class IncomingTransport(TransportBase):
    def __init__(self, address):
        #: :type address: Address    
        TransportBase.__init__(self, address);

    def receive(self):
        """Implementors should send the provided TransportMessage over the their chosen medium"""

class DuplexTransport(OutgoingTransport, IncomingTransport):
    def __init__(self, address):
        #: :type address: Address    
        TransportBase.__init__(self, address);
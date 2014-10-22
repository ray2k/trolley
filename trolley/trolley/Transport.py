import abc

class TransportBase(object):
    def __init__(self, address):
        self._address = address

    @property
    def address(self):
        return self._address

class OutgoingTransport(TransportBase):
    __metaclass__ = abc.ABCMeta

    def __init__(self, address):
        TransportBase.__init__(self, address);

    @abc.abstractmethod
    def send(self, message):
        """Implementors should send the provided TransportMessage over the their chosen medium"""
        return

class IncomingTransport(TransportBase):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, address):
        TransportBase.__init__(self, address);

    @abc.abstractmethod
    def receive(self):
        """Implementors should send the provided TransportMessage over the their chosen medium"""

class DuplexTransport(OutgoingTransport, IncomingTransport):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, address):
        TransportBase.__init__(self, address);
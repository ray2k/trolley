from .Headers import Headers
import io

class TransportMessage:
    def __init__(self):
        self._headers = {}
        self._body = io.BytesIO()

    @property
    def headers(self):
        return self._headers;

    @property
    def id(self):
        return self.headers.get(Headers.HEADER_MESSAGE_ID, None)

    @id.setter
    def id(self, value):
        self.headers[Headers.HEADER_MESSAGE_ID] = value

    @property
    def correlation_id(self):
        return self.headers.get(Headers.HEADER_CORRELATION_ID, None)

    @correlation_id.setter
    def correlation_id(self, value):
        self.headers[Headers.HEADER_CORRELATION_ID] = value

    @property
    def content_type(self):
        return self.headers.get(Headers.HEADER_CONTENT_TYPE, None)

    @content_type.setter
    def content_type(self, value):
        self.headers[Headers.HEADER_CONTENT_TYPE] = value

    @property
    def message_type(self):
        return self.headers.get(Headers.HEADER_MESSAGE_TYPE, None)
    
    @message_type.setter
    def message_type(self, value):
        self.headers[Headers.HEADER_MESSAGE_TYPE] = value

    @property
    def body(self):
        return self._body;

    @body.setter
    def body(self, value):
        self._body = value
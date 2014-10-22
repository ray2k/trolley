import unittest
from multipledispatch import dispatch
import trolley

class BarMessage:
    pass

class BazMessage:
    pass

class BarMessageHandler:
    @dispatch(BarMessage)
    def handle(self, message):
        print("handling barmessage")

    @dispatch(BazMessage)
    def handle(self, message):
        print("handling bazmessage")    

class Test_TransportMessageTests(unittest.TestCase):
    def test_TransportMessage_properties_should_wrap_headers(self):      
        msg = trolley.TransportMessage()

        msgType = type(msg)
        print(msgType)

        test = msgType()
        test.id = "foo"
        print(type(test))
        
        msg.id = "the id"
        self.assertEqual(msg.id, "the id")        
        headerVal = msg.headers.get(trolley.Headers.HEADER_MESSAGE_ID, None)
        self.assertIsNotNone(headerVal)
        self.assertEqual(headerVal, msg.id)

        msg.correlation_id = "correlation id"
        self.assertEqual(msg.correlation_id, "correlation id")        
        headerVal = msg.headers.get(trolley.Headers.HEADER_CORRELATION_ID, None)
        self.assertIsNotNone(headerVal)
        self.assertEqual(headerVal, msg.correlation_id)

        msg.content_type = "content type"
        self.assertEqual(msg.content_type, "content type")
        headerVal = msg.headers.get(trolley.Headers.HEADER_CONTENT_TYPE, None)
        self.assertIsNotNone(headerVal)
        self.assertEqual(headerVal, msg.content_type)

if __name__ == '__main__':
    unittest.main()

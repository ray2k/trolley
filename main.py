import trolley
import sys
import eventlet
import select
import inspect

class PingMessage:
    pass

class PongMessage:
    pass

class PingMessageHandler:
    handles = [PingMessage]

    def handle(self, message):
        print("received a PingMessage (PingMessageHandler)")
        print("publishing a PongMessage (PingMessageHandler)")
        self.bus.publish(PongMessage())

class PongMessageHandler:
    handles = PongMessage

    def handle(self, message):
        print("received a PongMessage (PongMessageHandler)")
        
class OtherPongMessageHandler:
    handles = PongMessage
    
    def handle(self, message):
        print("received a PongMessage (OtherPongMessageHandler)")
        
class PingPongSagaData(trolley.SagaData):    
    def __init__(self):
        print("PingPongSagaData.__init__")
        self.received_ping = False
        self.received_pong = False        
        
class InitiationMessage:
    pass
    
class PingPongSaga(trolley.AutoMappedSagaMixin, trolley.Saga):
    handles = [PingMessage,PongMessage]
    initiated_by = InitiationMessage    
    saga_data_type = PingPongSagaData
    
    def __init__(self):
        trolley.Saga.__init__(self)        
            
    def handle_PingMessage(self, message):
        self.data.received_ping = True
        print("received a PingMessage (PingPongSaga)")
        
    def handle_PongMessage(self, message):
        self.data.received_pong = True
        print("received a PongMessage (PingPongSaga)")              
        
def main():
    cfg = trolley.BusConfiguration()
    cfg.auto_subscribe(sys.modules[__name__])
    #cfg.subscribe(PingMessage, PingMessageHandler)
    #cfg.subscribe(PongMessage, PongMessageHandler)
    #cfg.subscribe(PongMessage, OtherPongMessageHandler)
    cfg.set_address(queueName="thequeue")
    cfg.set_transport(trolley.InMemoryTransport)
    bus = cfg.create_bus()    
    
    print("starting bus")
    bus.start()
    print("bus started")
    while(True):
        line = async_input()
        print("--enter something--")
        if line == "quit":
            print("quitting")
            break
        else:
            print("publishing PingMessage")
            bus.publish(PingMessage())
            print("PingMessage published")
    print("stopping bus")
    bus.stop()
    print("bus stopped")

def async_input():
    select.select([sys.stdin], [], [])
    return sys.stdin.readline().lstrip().rstrip()

if __name__ == '__main__':
    eventlet.monkey_patch(os=True, select=True, socket=None, thread=True, time=True, psycopg=None)
    main()
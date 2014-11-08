import trolley
import sys
import eventlet
import select

class PingMessage:
    pass

class PongMessage:
    pass

class PingMessageHandler:
    Handles = [PingMessage]

    def handle(self, message):
        print("RECEIVED PING")
        print("PUBLISHING PONG #1")
        self.bus.publish(PongMessage())
        print("PUBLISHING PONG #2")
        self.bus.publish(PongMessage())

class PongMessageHandler:
    Handles = PongMessage

    def handle(self, message):
        print("RECEIVED PONG")
        
def main():
    cfg = trolley.BusConfiguration()
    #cfg.auto_subscribe(sys.modules[__name__])
    cfg.subscribe(PingMessage, PingMessageHandler)
    cfg.subscribe(PongMessage, PongMessageHandler)
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
import trolley
import pickle
import jsonpickle
import io
import sys
from trolley import InMemoryTransport
import eventlet
import select

class Product:
	def __init__(self):
		self.product_id = 99
		self.product_name = "shoes"        

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

	sw = trolley.SyncWorker(None, None, None)

	cfg = trolley.BusConfiguration()
	#cfg.auto_subscribe(sys.modules[__name__])
	cfg.subscribe(PingMessage, PingMessageHandler)
	cfg.subscribe(PongMessage, PongMessageHandler)
	cfg.set_address(queueName="thequeue")
	cfg.set_transport(trolley.InMemoryTransport)
	bus = cfg.create_bus()	
	
	bus.start()
	while(True):
		line = async_input()
		
		if line == "quit":
			break
		else:
			bus.publish(PingMessage())

	bus.stop()

def async_input():
	select.select([sys.stdin], [], [])
	return sys.stdin.readline().lstrip().rstrip()

if __name__ == '__main__':
	eventlet.monkey_patch(os=True, select=True, socket=None, thread=True, time=True, psycopg=None)
	main()




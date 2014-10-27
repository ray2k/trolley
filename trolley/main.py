import trolley
import pickle
import jsonpickle
import io
import sys
from trolley import InMemoryTransport
import eventlet

class Product:
	def __init__(self):
		self.product_id = 99
		self.product_name = "shoes"        

class PingMessage:
	pass

class PongMessage:
	pass

class PingMessageHandler:
	Handles = [PingMessage,PongMessage]

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
	
	bus.start()
	while(True):
		line = input()
		if line == "quit":
			break
		else:
			bus.publish(PingMessage())	
	
	bus.stop()

if __name__ == '__main__':
	main()


import trolley
import pickle
import jsonpickle
import io


class Product:
	def __init__(self):
		self.product_id = 99
		self.product_name = "shoes"        

def main():

	p = Product()

	ser = trolley.JsonPickleSerializer()
	#ser = trolley.PickleSerializer()
	buffer = ser.serialize(p)
	deserialized = ser.deserialize(buffer)



	print(p.product_id, p.product_name)

	#print(deserialized.product_name)
	#print(deserialized.product_id)

	#print(ser.content_type)

	#deserialized = ser.deserialize(bytes)
	#print(deserialized.product_id)
	#print(deserialized.product_name)


if __name__ == '__main__':
	main()


class Address:
	def __init__(self, *args, **kwargs):
		self._settings = {}
		for key, value in kwargs.items():
			self._settings[key] = value
		self._location = Address.build_location(self._settings)
		
	@staticmethod
	def build_location(settings):
		settingString = ""
		for setting in settings:
			settingString += setting
			settingString += "="
			settingString += str(settings[setting])
			settingString += ";"
		return settingString        
		
	@property
	def location(self):
		return self._location
	
	@location.setter
	def location(self, value):
		self._location = value
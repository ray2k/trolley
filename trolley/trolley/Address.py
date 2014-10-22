class Address:
    def __init__(self, settings):
        self._location = self.build_location(settings)
        self._settings = settings

    def build_location(self, settings):
        settingString = ""
        for key, value in settings.items():
            settingString += key
            settingString += "="
            settingString += value
            settingString += ";"
        return settingString        
        
    @property
    def location(self):
     return self._location
    
    @location.setter
    def location(self, value):
        self._location = value
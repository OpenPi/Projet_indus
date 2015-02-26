# to Add a new preference :
# Add in __init__ method your data with default value (like self.ph = 7.4)
# Add your data in copy method (self.yourData = ObjectToCopy.yourData)
# Erase the preferences file
# setup your preferences

import pickle


class Preferences:

	def __init__(self, path):



		try:
			with open(path, 'rb') as fichier:               
				prefFromFile = self.read_preferences(path)
				self.copy(prefFromFile)

		except IOError:# If the file doesn't exist 

			# Default values
			self.filepath = path
			self.ph = 7.4
			self.write_preferences(self) # Create a new file and write default values 
            

	def copy(self, ObjectToCopy):
		self.ph = ObjectToCopy.ph
		self.filepath = ObjectToCopy.filepath

	def read_preferences(self, path):
		with open(path, 'rb+') as fichier:
			Unpickler = pickle.Unpickler(fichier)
			return Unpickler.load()

	def write_preferences(self, preferences):
		with open(self.filepath, 'wb') as fichier:
			PreferencePickler = pickle.Pickler(fichier)
			PreferencePickler.dump(preferences)
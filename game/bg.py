import math, random
from . import gameobject, resources

class Background(gameobject.GameObject):
	def __init__(self, *args, **kwargs):
		day = random.choice(['bg_day', 'bg_night'])
		super(Background, self).__init__(img = resources.spriteDictionary[day],
									*args, **kwargs)
		self.solid = False
		self.name = "BG"
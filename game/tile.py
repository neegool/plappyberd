import math, gameobject, resources

class Tile(gameobject.GameObject):
	velocity_x = resources.GAME_SPEED

	def __init__(self, *args, **kwargs):
		super(Tile, self).__init__(img = resources.spriteDictionary['tile'],
									*args, **kwargs)
		self.name = "Tile"

		Tile.velocity_x = resources.GAME_SPEED

	# wrap tiles around
	def check_bounds(self):
		min_x = resources.screen_width * 0.5 - self.image.width * 1.5
		if self.x <= min_x:
			self.x += resources.TILE_AMOUNT * self.image.width

	@staticmethod
	def stop_tiles():
		Tile.velocity_x = 0

	def update(self, dt):
		super(Tile, self).update(dt)
		self.x -= Tile.velocity_x * dt
		self.check_bounds()
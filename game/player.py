from pyglet.window import key, mouse
import math, util, bg, gameobject, tile, pipe, resources, random

class Player(gameobject.GameObject):
	player_list = []
	current_player = 0

	def __init__(self, *args, **kwargs):
		self.color_choice = random.choice(['player_red', 'player_blue', 'player_yellow'])
		super(Player, self).__init__(img = resources.spriteDictionary[self.color_choice][0],
										*args, **kwargs)
		self.acceleration = 320
		self.keyHandler = key.KeyStateHandler()
		self.velocity_y = 0
		self.gravity = 19.0
		self.base_y = 256

		self.grounded = False
		self.dead = False
		self.jump_pressed = False
		self.mouse_pressed = False
		self.name = "Player"

		self.spriteIndex = 0
		self.timer = 0
		self.limit = 0.05
		self.counter = 0
		self.score = 0
		self.ready = False
		self.tile_hit_first = False
		self.jump_point_y = 0

		Player.player_list.append(self)
		Player.current_player = 0
		# print self.name, ":", self.collider

	def update(self, dt):
		super(Player, self).update(dt)

		self.timer += dt
		self.counter += dt

		rotate_direction = 1

		if self.ready == False:
			self.limit = 0.12
			rotate_direction = 0
		else:
			self.limit = 0.05

		if self.dead == False and self.timer >= self.limit:
			self.image = resources.spriteDictionary[self.color_choice][self.spriteIndex]
			if self.ready == False or self.rotation <= 0:
				self.spriteIndex = (self.spriteIndex + 1) % len(resources.spriteDictionary[self.color_choice])
			else:
				self.spriteIndex = 1
			self.timer = 0

		if self.dead == False:
			if self.keyHandler[key.SPACE] or self.mouse_pressed == True:
				if self.ready == False:
					self.ready = True
					Player.current_player = (Player.current_player + 1) % len(Player.player_list)
				if self.jump_pressed == False and self.y < resources.screen_height:
					resources.soundDictionary['wing'].play()
					self.jump_point_y = self.y
					self.velocity_y = self.acceleration
					self.jump_pressed = True
			else:
				if self.jump_pressed == True:
					self.jump_pressed = False

		# apply gravity
		if self.grounded == False and self.ready == True:
			self.velocity_y = max(self.velocity_y - self.gravity, -2 * self.acceleration)

		if self.ready == False:
			self.y = self.base_y + math.sin((8 * self.counter) % (2 * math.pi)) * 4

		if self.dead == True and self.counter > 0.3:
			if self.tile_hit_first == False:
				resources.soundDictionary['die'].play()
				self.counter = -999

		# check for ball collisions
		for obj in gameobject.GameObject.get_game_objects(True):
			if obj != self and obj.solid == True:
				if self.collides_with(obj):
					if obj.name == 'PipeManager':
						if obj.cleared == False:
							resources.soundDictionary['point'].play()
							self.score += 1
							obj.cleared = True
					elif self.dead == False:
						resources.soundDictionary['hit'].play()
						self.tile_hit_first = (obj.name == 'Tile')
						self.velocity_y = 0
						self.dead = True
						self.counter = 0
						tile.Tile.stop_tiles()
						pipe.PipeManager.stop_pipes()

					if (obj.name == 'Tile'):
						self.velocity_y = 0
						self.y = obj.y + (obj.image.height + self.image.height) * 0.5
						self.grounded = True

		rotate_factor = 2 * dt
		if self.velocity_y <= 0 and self.y <= self.jump_point_y + self.image.height:
			rotate_direction = -1
			rotate_factor = dt

		self.rotation = util.clamp(self.rotation - rotate_direction * 300 * rotate_factor, -20, 90)

		# move player with respect to velocity
		self.y += self.velocity_y * dt


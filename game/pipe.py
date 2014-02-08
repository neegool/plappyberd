import math, gameobject, resources, player, random, util

class PipeManager(gameobject.GameObject):
	velocity_x = resources.GAME_SPEED

	# classify pipe gap locations into three tiers
	# pick a random threshold (pipe_limit)
	hole_tier = {
		'high': resources.screen_height * 0.75,
		'mid' : resources.screen_height * 0.6,
		'low' : resources.screen_height * 0.45
	}

	current_tier = hole_tier['mid']
	pipe_counter = 0
	pipe_limit = random.randint(2, 5)
	player = None

	def __init__(self, *args, **kwargs):
		super(PipeManager, self).__init__(img = resources.spriteDictionary['checkpoint']
											,*args, **kwargs)
		self.visible = False
		self.cleared = False
		self.name = "PipeManager"

		self.current_tier = PipeManager.current_tier
		self.pipe_up = Pipe(type = 'Up', x = self.x)
		self.pipe_down = Pipe(type = 'Down', x = self.x)

		PipeManager.player = None
		PipeManager.pipe_counter = 0
		PipeManager.velocity_x = resources.GAME_SPEED

	# wrap the pipe around and change the offset of the gaps
	# if pipe_limit is reached, pick a random tier
	def check_bounds(self):
		min_x = resources.screen_width * 0.5 - resources.PIPE_DISTANCE * 2.5
		if self.x <= min_x:
			self.x += resources.PIPE_AMOUNT * resources.PIPE_DISTANCE
			self.cleared = False

			if self.current_tier != PipeManager.current_tier:
				self.y = PipeManager.current_tier
				self.current_tier = PipeManager.current_tier

			PipeManager.pipe_counter += 1
			self.y = util.clamp(self.y + random.choice([-40, -20, 20, 40]), 200, resources.screen_height - 88)
			
			if PipeManager.pipe_counter >= PipeManager.pipe_limit:
				PipeManager.pipe_limit = random.randint(2, 5)
				choice = random.choice(['high', 'mid', 'low'])
				PipeManager.current_tier = PipeManager.hole_tier[choice]
				PipeManager.pipe_counter = 0

	@staticmethod
	def stop_pipes():
		PipeManager.velocity_x = 0

	def update(self, dt):
		super(PipeManager, self).update(dt)

		if PipeManager.player == None:
			PipeManager.player = gameobject.GameObject.find_game_object("Player")

		if PipeManager.player.ready == True:
			self.x -= PipeManager.velocity_x * dt
			self.pipe_up.x = self.x
			self.pipe_down.x = self.x

			self.check_bounds()

			self.pipe_up.y = self.y - (self.pipe_up.image.height + resources.PIPE_GAP) * 0.5
			self.pipe_down.y = self.y + (self.pipe_down.image.height + resources.PIPE_GAP) * 0.5

class Pipe(gameobject.GameObject):
	def __init__(self, type, *args, **kwargs):
		if type == 'Up':
			image = resources.spriteDictionary['pipe_up']
		elif type == 'Down':
			image = resources.spriteDictionary['pipe_down']
		super(Pipe, self).__init__(img = image,
									*args, **kwargs)
		self.name = "Pipe"

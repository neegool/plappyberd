import pyglet, util

class GameObject(pyglet.sprite.Sprite):
	pool = []

	def __init__(self, *args, **kwargs):
		super(GameObject, self).__init__(*args, **kwargs)
		self.name = "GameObject"
		self.active = True
		self.solid = True
		self.size = min(self.image.width, self.image.height) * 0.5
		self.parent = None

		self.collider = {
			'left': 	0,
			'right': 	0,
			'top':		0,
			'bottom':	0
		}

		self.get_collider()

		#add game object to pool
		GameObject.pool.append(self)

	# def collides_with(self, other):
	# 	c1 = self.collider
	# 	c2 = other.collider

	# 	return not (other.x + c2['left'] > self.x + c1['right'] or
	# 				other.x + c2['right'] <  self.x + c1['left'] or 
	# 			    other.y + c2['top'] <  self.y + c1['bottom'] or
	# 			    other.y + c2['bottom'] >  self.y + c1['top'])

	def collides_with(self, other):
		o = other.collider

		closest_x = util.clamp(self.x, other.x + o['left'], other.x + o['right'])
		closest_y = util.clamp(self.y, other.y + o['bottom'], other.y + o['top'])

		dist_x = self.x - closest_x
		dist_y = self.y - closest_y

		dist = util.distance_squared(self.position, (closest_x, closest_y))

		return dist < (self.size ** 2)

	def get_collider(self):
		self.collider['left'] 	= (self.image.anchor_x - self.image.width)
		self.collider['right'] 	= (self.image.width - self.image.anchor_x)
		self.collider['top'] 	= (self.image.height - self.image.anchor_y)
		self.collider['bottom'] = (self.image.anchor_y - self.image.height)

	@staticmethod
	def find_game_objects(name):
		found_objects = []
		for obj in GameObjectpool:
			if obj.name == name:
				found_objects.append(obj)

		return found_objects[0]

	@staticmethod
	def find_game_object(name):
		for obj in GameObject.pool:
			if obj.name == name:
				return obj

		return None
 
	@staticmethod
	def get_game_objects(active = True):
		new_pool = []
		for obj in GameObject.pool:
			if active == True and obj.active == True:
				new_pool.append(obj)
			elif active == False and obj.active == False:
				new_pool.append(obj)
		return new_pool

	def update(self, dt):
		yield None
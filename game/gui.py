import math, gameobject, resources, util, random

class GUIManager(gameobject.GameObject):
	# GUI Elements

	def __init__(self, *args, **kwargs):
		super(GUIManager, self).__init__(img = resources.no_sprite,
									*args, **kwargs)
		self.name = "GUIManager"
		self.visible = False
		self.solid = False

		self.score_length = 6

		self.getready = GUIObject(img = resources.spriteDictionary['get_ready'],
							x = resources.screen_width * 0.5,
							y = 284)
		self.getready.name = "Get Ready"
		self.getready.set_opacity(0)
		self.getready.parent = self

		self.gameover = GUIObject(img = resources.spriteDictionary['game_over'],
							x = resources.screen_width * 0.5,
							y = 360)
		self.gameover.name = "Game Over"
		self.gameover.set_opacity(0)
		self.gameover.parent = self

		self.resultpanel = GUIObject(img = resources.spriteDictionary['result_panel'],
							x = resources.screen_width * 0.5,
							y = -57)
		self.resultpanel.name = "Result Panel"
		#self.resultpanel.set_opacity(0)
		self.resultpanel.parent = self

		self.play = GUIObject(img = resources.spriteDictionary['play'],
							x = resources.screen_width * 0.5,
							y = 137)
		self.play.name = "Play"
		self.play.parent = self

		self.score = []
		self.highscore = []
		self.resultscore = []

		self.medal = GUIObject(img = resources.spriteDictionary['medal_bronze'],
							x = self.resultpanel.x - 65,
							y = self.resultpanel.y)
		self.medal.name = "Medal"
		self.medal.parent = self

		self.newrecord = GUIObject(img = resources.spriteDictionary['new'],
							x = self.resultpanel.x + 39,
							y = self.resultpanel.y)
		self.newrecord.name = "New"
		self.newrecord.parent = self

		self.star = GUIObject(img = resources.spriteDictionary['star_1'],
							x = self.resultpanel.x + 39,
							y = self.resultpanel.y)
		self.star.name = "Star"
		self.star.parent = self
		self.star_index = 0

		for i in range(0, self.score_length):
			self.score.append(GUIObject(img = resources.spriteDictionary['bigscore_0'],
								x = resources.screen_width * 0.5,
								y = 412))
			self.score[i].name = "Score"
			self.score[i].parent = self

			self.highscore.append(GUIObject(img = resources.spriteDictionary['smallscore_0'],
								x = resources.screen_width * 0.5 + 84,
								y = -86))
			self.highscore[i].name = "HighScore"
			self.highscore[i].parent = self

			self.resultscore.append(GUIObject(img = resources.spriteDictionary['smallscore_0'],
								x = resources.screen_width * 0.5 + 84,
								y = -86))
			self.resultscore[i].name = "ResultScore"
			self.resultscore[i].parent = self

		self.flash = GUIObject(img = resources.spriteDictionary['flash'],
								x = resources.screen_width * 0.5,
								y = resources.screen_height * 0.5)
		self.flash.name = "Flash"
		self.flash.set_opacity(0)
		self.flash.parent = self

		self.fader = GUIObject(img = resources.spriteDictionary['fader'],
								x = resources.screen_width * 0.5,
								y = resources.screen_height * 0.5)
		self.fader.name = "Fader"
		self.fader.parent = self

		self.flashed = False
		self.ready = False
		self.over = False
		self.result = False
		self.done = False

		self.player = None

		self.counter = 0
		self.movement = 1
		self.result_current_score = 0

		self.set_gui_active(False)
		self.set_gui_list_active(self.score, True)
		self.getready.active = True
		self.fader.active = True

	def set_gui_active(self, active):
		for obj in gameobject.GameObject.get_game_objects(not active):
			if obj.parent == self:
				obj.active = active

	def set_gui_list_active(self, guilist, active):
		for obj in guilist:
			obj.active = active

	# maps the score digits to their respective textures
	def int_to_sprite(self, num, sprites, type, spacing = 0):
		int_list = str(num)

		offset_x = (resources.screen_width * 0.5)
		for i in range(0, self.score_length):
			sprites[i].x = offset_x + (sprites[i].image.width * 0.5)
			sprites[i].visible = False
			if i < len(int_list):
				sprites[i].image = resources.spriteDictionary[type + 'score_' + int_list[i]] 
				offset_x += resources.spriteDictionary[type + 'score_' + int_list[i]].width + spacing

		return len(int_list), offset_x

	def offset_sprite_list(self, sprites, offset):
		#diff = offset - (resources.screen_width * 0.5)

		for i in range(0, len(sprites)):
			sprites[i].x += offset
			sprites[i].visible = True

	def update(self, dt):
		super(GUIManager, self).update(dt)

		if self.player == None:
			self.player = gameobject.GameObject.find_game_object("Player")
			self.fader.fade_out(1024)

		# show the "Get Ready" image
		if self.player.ready == False:
			self.getready.fade_in(1024)
		elif self.ready == False:
			self.getready.fade_out(1024)
			self.ready = True

		# flash the screen when the player hits something
		if self.player.dead == True and self.flashed == False:
			self.flash.active = True
			self.flash.set_opacity(255)
			self.flash.fade_out(2048)
			self.flashed = True

		# show the "Game Over" image
		if self.flashed == True:
			self.counter += dt
		 	if self.over == False:
				if self.counter > 0.5:
					for obj in self.score:
						obj.set_opacity(0)
						obj.active = False

					resources.soundDictionary['swooshing'].play()

					self.gameover.active = True
					self.gameover.fade_in(1024)
					#self.resultpanel.fade_in(1024)
					self.over = True

		if self.over == True and self.result == False:
			self.gameover.y += 100 * self.movement * dt
			if self.gameover.y > 367 and self.movement == 1:
				self.movement = -1
			if self.gameover.y <= 359:
				self.gameover.y = 359
				self.movement = 0
			if self.counter > 1.5:
				resources.soundDictionary['swooshing'].play()
				self.result = True
				self.movement = 0
				self.counter = 0

		if self.result == True and self.done == False:
			self.resultpanel.active = True
			delta = util.clamp(math.sin(5 * self.counter) * 260, -1000, 260)
			
			if self.resultpanel.y <= 259:
				self.resultpanel.y = delta
			else:
				self.resultpanel.y = 259
				self.done = True
				self.counter = -0.25
				#self.result = False

		if self.done == True:
			if self.counter > 0.05:
				if self.result_current_score < self.player.score:
					self.result_current_score += 1
					self.counter = 0

			if self.result_current_score == self.player.score:
				medal_img = resources.no_sprite
				if self.player.score >= 40:
					medal_img = resources.spriteDictionary['medal_platinum']
				elif self.player.score >= 30:
					medal_img = resources.spriteDictionary['medal_gold']
				elif self.player.score >= 20:
					medal_img = resources.spriteDictionary['medal_silver']
				elif self.player.score >= 10:
					medal_img = resources.spriteDictionary['medal_bronze']

				self.medal.active = True
				self.medal.y = self.resultpanel.y - 7
				self.medal.image = medal_img

				self.play.active = True
				resources.GameManager.game_state = 'GAMEOVER_STATE'


				if self.player.score >= 10:
					self.star.active = True

					if self.counter > 0.1:
						self.star_index = (self.star_index + 1) % len(resources.spriteDictionary['star'])
						self.counter = 0

						if self.star_index == 0:
							self.star.x = self.medal.x + random.randint(self.medal.collider['left'],
															self.medal.collider['right']) * 0.8
							self.star.y = self.medal.y + random.randint(self.medal.collider['bottom'],
															self.medal.collider['top']) * 0.8

						self.star.image = resources.spriteDictionary['star'][self.star_index]

				if self.player.score > resources.data['highscore']:
					resources.write_data('highscore', self.player.score)
					self.newrecord.active = True
					self.newrecord.y = self.resultpanel.y - 8


		num_digits, offset = self.int_to_sprite(self.player.score, self.score, 'big', -4)
		diff = ((resources.screen_width * 0.5) - offset) * 0.5
		self.offset_sprite_list(self.score[0:num_digits], diff)

		if self.over == True:

			self.set_gui_list_active(self.highscore, True)
			self.set_gui_list_active(self.resultscore, True)

			num_digits_highscore, offset_highscore = self.int_to_sprite(resources.data['highscore'], self.highscore, 'small', 1)
			diff = (resources.screen_width * 0.5) - offset_highscore + 91
			self.offset_sprite_list(self.highscore[0:num_digits_highscore], diff)

			num_digits_result, offset_result = self.int_to_sprite(self.result_current_score, self.resultscore, 'small', 1)
			diff = (resources.screen_width * 0.5) - offset_result + 91
			self.offset_sprite_list(self.resultscore[0:num_digits_result], diff)

			for digit in self.highscore:
				digit.y = self.resultpanel.y - 29

			for digit in self.resultscore:
				digit.y = self.resultpanel.y + 13

class GUIObject(gameobject.GameObject):
	def __init__(self, *args, **kwargs):
		super(GUIObject, self).__init__(*args, **kwargs)
		self.solid = False
		self.name = "GUIObject"
		self.fade_direction = 1
		self.fade_rate = 0

	def fade_in(self, rate = 255):
		self.fade_rate = rate
		self.fade_direction = 1


	def fade_out(self, rate = 255):
		self.fade_rate = rate
		self.fade_direction = -1

	def set_opacity(self, opacity):
		self.opacity = opacity

	def update(self, dt):
		super(GUIObject, self).update(dt)
		
		self.opacity = util.clamp(self.opacity + self.fade_direction * self.fade_rate * dt, 0, 255)

		if self.opacity <= 0 or self.opacity >= 255:
			self.fade_direction = 0

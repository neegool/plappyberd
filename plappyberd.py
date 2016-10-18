import pyglet, random
from pyglet.window import key, mouse
from game import bg, pipe, player, tile, resources, gameobject, gui, util

# initialize the game window
# it is currently set to 800x600, but you may change this as needed.
game_window = pyglet.window.Window(resources.screen_width, resources.screen_height)
game_window.set_caption("PlappyBerd")

# initialize objects
newplayer = None

# resources for title screen
def init_title():
	newbg = bg.Background(x = resources.screen_width * 0.5,
							y = resources.screen_height * 0.5)
	newplayer = player.Player(x = resources.screen_width * 0.5, y = 280)
	newplayer.base_y = 280

	newtitle = gui.GUIObject(img = resources.spriteDictionary['plappyberd'],
								x = resources.screen_width * 0.5,
								y = 342)

	newplay = gui.GUIObject(img = resources.spriteDictionary['play'],
								x = resources.screen_width * 0.5,
								y = 211)

	tile_x = resources.screen_width * 0.5 - 336
	for i in range(0, resources.TILE_AMOUNT):
		newtile = tile.Tile(x = tile_x, y = 56)
		tile_x += newtile.image.width

	resources.GameManager.game_state = 'TITLE_STATE'

# resources for gameplay level
def init_level():
	newbg = bg.Background(x = resources.screen_width * 0.5,
							y = resources.screen_height * 0.5)

	#pipe_x = resources.screen_width * 2 - resources.PIPE_DISTANCE
	pipe_x = 140 * resources.START_TIME
	pipe_y = resources.screen_height * 0.6
	for i in range(0, resources.PIPE_AMOUNT):
		pipe_y = util.clamp(pipe_y + random.choice([-40, -20, 20, 40]), 200, resources.screen_height - 88)
		newpipe = pipe.PipeManager(x = pipe_x, y = pipe_y)
		pipe_x += resources.PIPE_DISTANCE

	newplayer = player.Player(x = 89, y = 300)
	game_window.push_handlers(newplayer.keyHandler)
	#newplayer = player.Player(x = 49, y = 300)
	#game_window.push_handlers(newplayer.keyHandler)
	
	tile_x = resources.screen_width * 0.5 - 336
	for i in range(0, resources.TILE_AMOUNT):
		newtile = tile.Tile(x = tile_x, y = 56)
		tile_x += newtile.image.width

	newguimanager = gui.GUIManager(x = 0, y = 0)

	resources.GameManager.game_state = 'GAMEPLAY_STATE'

# cleanup resources
def delete():
	for obj in gameobject.GameObject.pool:
		if obj.name != "Fader":
			obj.delete()
	to_delete = gameobject.GameObject.pool
	gameobject.GameObject.pool = []
	del to_delete

# print [obj.name for obj in gameobject.GameObject.get_game_objects(True)]

@game_window.event
def on_draw():
	game_window.clear()
	for obj in gameobject.GameObject.get_game_objects():
		obj.draw()

@game_window.event
def on_mouse_press(x, y, button, modifiers):
    player.mouse_pressed = (button == mouse.LEFT)

@game_window.event
def on_key_press(symbol, modifiers):
	if symbol == key.SPACE:
		if resources.GameManager.game_state == 'TITLE_STATE':
			resources.soundDictionary['swooshing'].play()
			delete()
			init_level()
		elif resources.GameManager.game_state == 'GAMEOVER_STATE':
			resources.soundDictionary['swooshing'].play()
			delete()
			init_level()

	if symbol == key.R:
		delete()
		init_title()

@game_window.event
def on_mouse_release(x, y, button, modifiers):
     player.mouse_pressed = not (button == mouse.LEFT)

def update(dt):
	#print dt
	for obj in gameobject.GameObject.get_game_objects():
		obj.update(dt)	

if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1/120.0)
	init_title()
	pyglet.app.run()
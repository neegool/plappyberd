import os, pyglet

pyglet.lib.load_library('avbin64')
pyglet.have_avbin = True

screen_width = 288
screen_height = 512

TILE_AMOUNT = 3
PIPE_AMOUNT = 5
PIPE_DISTANCE = 157
PIPE_GAP = 96
GAME_SPEED = 120
START_TIME = 4

class GameManager:
	timer = 0
	game_state = "TITLE_STATE"

def center_image(image):
	image.anchor_x = image.width * 0.5
	image.anchor_y = image.height * 0.5


# load user preferences
media_path = './data/media'

pyglet.resource.path = ['./data/resources.zip']
pyglet.resource.reindex()

dir = pyglet.resource.get_settings_path('PlappyBerd')
if not os.path.exists(dir):
    os.makedirs(dir)

save_data = None
data_path = os.path.join(dir, 'data.sav')

try:
	save_data = open(data_path, 'rt')
except IOError:
	print('no save data found')
	save_data = open(data_path, 'wt')
	save_data.write("highscore:0\n")
	save_data.close()
	save_data = open(data_path, 'rt')

data = {}

data['highscore'] = 0

for line in save_data:
	key, value = line.split(':')
	data[key] = int(value)
save_data.close()


no_sprite = pyglet.resource.image("blank.png")

# create a dictionary for sprites and sounds for easier access later
spriteDictionary = {}

spriteDictionary['plappyberd'] 		= pyglet.resource.image("plappyberd.png")
spriteDictionary['play'] 			= pyglet.resource.image("play.png")

spriteDictionary['tile'] 			= pyglet.resource.image("tilelegit.png")
spriteDictionary['pipe_up'] 		= pyglet.resource.image("pipe_up.png")
spriteDictionary['pipe_down'] 		= pyglet.resource.image("pipe_down.png")
spriteDictionary['bg_day'] 			= pyglet.resource.image("bg_day.png")
spriteDictionary['bg_night'] 		= pyglet.resource.image("bg_night.png")
spriteDictionary['flash'] 			= pyglet.resource.image("flash.png")
spriteDictionary['checkpoint'] 		= pyglet.resource.image("checkpoint.png")
spriteDictionary['get_ready'] 		= pyglet.resource.image("get_ready.png")
spriteDictionary['game_over'] 		= pyglet.resource.image("game_over.png")
spriteDictionary['result_panel']	= pyglet.resource.image("result_panel.png")
spriteDictionary['medal_platinum']	= pyglet.resource.image("medal_platinum.png")
spriteDictionary['medal_gold']		= pyglet.resource.image("medal_gold.png")
spriteDictionary['medal_silver']	= pyglet.resource.image("medal_silver.png")
spriteDictionary['medal_bronze']	= pyglet.resource.image("medal_bronze.png")
spriteDictionary['new']				= pyglet.resource.image("new.png")
spriteDictionary['fader']			= pyglet.resource.image("fader.png")

for i in ['red', 'blue', 'yellow']:
	spriteDictionary['player_' + i + '_1'] = pyglet.resource.image('bird_' + i + '_1.png')
	spriteDictionary['player_' + i + '_2'] = pyglet.resource.image('bird_' + i + '_2.png')
	spriteDictionary['player_' + i + '_3'] = pyglet.resource.image('bird_' + i + '_3.png')

	spriteDictionary['player_' + i] = [spriteDictionary['player_' + i + '_1'],
										spriteDictionary['player_' + i + '_2'],
										spriteDictionary['player_' + i + '_3'],	
										spriteDictionary['player_' + i + '_2']]
for i in range(1, 4):
	spriteDictionary["star_" + str(i)] = pyglet.resource.image("star_" + str(i) + ".png")

spriteDictionary['star'] = [no_sprite,
							spriteDictionary['star_1'],
							spriteDictionary['star_2'],
							spriteDictionary['star_3'],	
							spriteDictionary['star_2'],
							spriteDictionary['star_1']]

for i in range(0, 10):
	spriteDictionary['bigscore_' + str(i)] = pyglet.resource.image(str(i) + ".png")
	spriteDictionary['smallscore_' + str(i)] = pyglet.resource.image(str(i) + "_small.png")


soundDictionary = {}

soundDictionary['wing'] 		= pyglet.media.load(os.path.join(media_path, "sfx_wing.ogg"), streaming = False)
soundDictionary['hit'] 			= pyglet.media.load(os.path.join(media_path, "sfx_hit.ogg"), streaming = False)
soundDictionary['point'] 		= pyglet.media.load(os.path.join(media_path, "sfx_point.ogg"), streaming = False)
soundDictionary['die'] 			= pyglet.media.load(os.path.join(media_path, "sfx_die.ogg"), streaming = False)
soundDictionary['swooshing'] 	= pyglet.media.load(os.path.join(media_path, "sfx_swooshing.ogg"), streaming = False)

# center the anchor point of each sprite in the dictionary
for key in spriteDictionary:
	if not type(spriteDictionary[key]) is list:
		center_image(spriteDictionary[key])
		#tex_border(spriteDictionary[key])

#level_label = pyglet.text.Label(text="Game Test", x=400, y=575, anchor_x='center')

def write_data(key, value):
	data[key] = value
	save_data = open(data_path, 'wt')
	for k in data:
		save_data.write(k + ":" + str(data[k]) + '\n')
	save_data.close()


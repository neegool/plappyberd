import math, pyglet

# get distance between two points
def distance(a = (0,0), b = (0,0)):
	return math.sqrt(distance_squared(a, b))

def distance_squared(a = (0,0), b = (0,0)):
	return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def clamp(value, minval, maxval):
	return max(min(value, maxval), minval)

def lerp(start, end, ratio):
	return start + (end - start) * ratio

def sign(value):
	if value > 0:
		return 1
	elif value < 0:
		return -1
	else:
		return 0

def get_approx_size(width, height):
	return math.sqrt(width * height / math.pi)

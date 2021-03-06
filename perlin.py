from PIL import Image, ImageDraw
import random, math

GRADIENT = []

def regenerate():
	global GRADIENT
	GRADIENT = []
	for i in range(200):
		#print "Row ", i
		row = []
		for k in range(200):
			r = (random.random() + 1.0) * math.pi
			row.append([math.sin(r), math.cos(r)])
		GRADIENT.append(row)

def lerp(a0, a1, w):
	return (1.0 - w)*a0 + w*a1

def dotGridGradient(ix, iy, x, y):
	#print iy, " +++ ", ix
	dx = x - float(ix)
	dy = y - float(iy)
	
	return (dx*GRADIENT[iy][ix][0] + dy*GRADIENT[iy][ix][1])

def perlin(x, y):
	#print x, " - ", y
	x0 = int(x) if x > 0.0 else int(x) - 1
	x1 = x0 + 1
	y0 = int(y) if y > 0.0 else int(y) - 1
	y1 = y0 + 1
	
	sx = x - x0
	sy = y - y0
	
	n0 = dotGridGradient(x0, y0, x, y)
	n1 = dotGridGradient(x1, y0, x, y)
	ix0 = lerp(n0, n1, sx)
	n0 = dotGridGradient(x0, y1, x, y)
	n1 = dotGridGradient(x1, y1, x, y)
	ix1 = lerp(n0, n1, sx)
	return lerp(ix0, ix1, sy)

def perlinDeep(x, y, d, acc=0):
	if d == 0:
		return acc
	return perlinDeep(x, y, d - 1, acc + perlin(x / 2.0, y / 2.0))

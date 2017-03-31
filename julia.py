from PIL import Image, ImageDraw, ImageFilter
import numpy, math, random, itertools, perlin
import time

def noise(n):  # Prototype noise adding function to change texture
	return n + 10 * random.random()

def pickViewWindow():
	ct = time.localtime()
	theta = ct.tm_hour * 15.0 + ct.tm_min * 15.0 / 60.0
	theta = theta / 180.0 * math.pi
	R = 1.0
	x = math.sin(theta) * R
	y = math.cos(theta) * R
	SIZE = 2.0
	return (x - SIZE, x + SIZE, y - SIZE, y + SIZE)

def pickOffset():
	x_min, x_max, y_min, y_max = pickViewWindow()
	centerpoint = (x_max - x_min)/2.0 + (y_max - y_min)/2.0 * 1j
	r = abs(centerpoint)
	offset = centerpoint/r
	return offset

def mandlebrotDistance(c): # Finds distance from a point to the Mandlebrot Set (source: Wiki)
	n = 0
	zprime = 0
	while abs(c) < 5 and n < 20:
		zprime = 2 * c * zprime + 1
		c = c ** 2 + c
	return (abs(c) * math.log(abs(c))) / abs(zprime)

def inJulia(f_c, z, exp=2): # Prototype Julia Function Iterator
	n = 50
	while abs(z) < 10 and n > 0:
		z = z ** exp + f_c
		n -= 1
	return n == 0 

def pickRandomInterest(): # Picks a probably interesting point near the border of the mandlebrot set
	t = random.random() * math.pi
	x = (2.0 * math.cos(t) - math.cos(2.0 * t)) / 4.0
	y = (2.0 * math.sin(t) - math.sin(2.0 * t)) / 4.0
	x = x + (0.5 - random.random()) / 2.0
	y = y + (0.5 - random.random()) / 2.0
	return complex(x, y)

def pickTimeInterest(offset=0.0): # Same as pickRandomInterest, but based on time
	ct = time.time() + offset
	t = (ct % (60 * 60 * 24)) / (60 * 60 * 24) * math.pi
	x = (2.0 * math.cos(t) - math.cos(2.0 * t)) / 3.5 # 4.0 is exact border
	y = (2.0 * math.sin(t) - math.sin(2.0 * t)) / 4.0
	x = x + math.sin(ct / 60.0)
	y = y + math.cos(ct / 60.0)
	#x = x + (0.5 - random.random()) / 2.0
	#y = y + (0.5 - random.random()) / 2.0
	return complex(x, y)

def pickNearnessInterest(c=complex(0, 0), r=2, step=0): # Prototype to pick point near mandlebrot set
	if step < 5:
		x = [pickNearnessInterest(c+complex(r - random.random() * 2 * r, r - random.random() * 2 * r), r = r / 2.0, step = step+1) for i in range(5)]
		tr = c
		record = 100
		for item in x:
			if mandlebrotDistance(item) < record:
				tr = item
				record = mandlebrotDistance(item)
		return tr
	else:
		return c

def gentleClamp(v, up, low):
	if v > up:
		v = up
	elif v < low:
		v = low
	return v

def toRGB(n): # H in [0, 360), S in [0, 1], V in [0, 1]
	H, S, V = n
	C = V * S
	Hprime = H / 60.0
	X = C * (1 - abs(Hprime % 2 - 1))
	pickList = []
	for item in itertools.permutations([C, X, 0.0]):
		a, b, c = item
		pickList.append((c, b, a))
	result = pickList[gentleClamp(int(Hprime), len(pickList), 0)]
	result = list(result)
	result = map(lambda n: int(n * 255.0), result)
	return result

def colorBlend(a, b):
	def blender(n, x, real=0.0, imag=0.0):
		percemp = (255 - ((n ** 2) / 255.0)) / 100.0
		percemp += x
		tr = map(lambda n, m: n + m, map(lambda n: n * percemp, a), map(lambda n: n * (1.0 - percemp), b))
		tr = map(int, tr)
		return tuple(tr)
	return blender

def blueCentricHSV(n):
	theta = n / 255.0 * 70
	HSV = (180+int(theta), 188, 230)
	return toRGB(HSV)

def adjacent(c):
	H, S, V = c
	color1 = (H + 30 % 360, 1.0, V + 0.5)
	color2 = (H - 30 % 360, 1.0, V - 0.25)
	color1 = toRGB(color1)
	color2 = toRGB(color2)
	return color1, color2

def timeColor(real, imag):
	ct = time.localtime()
	return ((ct.tm_hour % 24 + ct.tm_min / 60.0 + 0.0) * 5.0 % 360,  0.5 + abs(real / 10.0), 0.5 + abs(imag / 10.0)) # 0.0 -> real * imag * 2.0

def roughTimeColor(real, imag):
	ct = time.localtime()
	return ((ct.tm_hour % 24 + ct.tm_min / 60.0 + 0.0) * 5.0 % 360, abs(real / 5.0), abs(imag / 5.0))

def timeBased(n, x, real, imag):
	color1, color2 = adjacent(timeColor(real, imag))
	color1 = list(color1)
	color2 = list(color2)
	return colorBlend(color1, color2)(n, x)

similar = colorBlend([62, 185, 237], [30, 115, 57])

silverAndGold = colorBlend([222, 213, 227], [181, 139, 2])

redAndGold = colorBlend([240, 38, 42], [181, 139, 2])

greenAndRed = colorBlend([29, 237, 21], [237, 36, 21])

meganMix = colorBlend([254, 248, 139], [51, 26, 0])

def julia(c, exponent, width=500, height=500, real_min=-2.0, real_max=2.0, imag_min=-2.0, imag_max=2.0, pickColor=timeBased, allPerlin = False):
	#print "Julia Called: ", c, " + ", exponent
	perlin.regenerate()
	
	# Generate evenly spaced values over real and imaginary ranges
	real_range = numpy.arange(real_min, real_max, float(real_max - real_min) / width)
	imag_range = numpy.arange(imag_max, imag_min, float(imag_min - imag_max) / height)
	
	# Obtain image to work with
	image = Image.new('RGB', (width, height), (0, 0, 0))
	drawer = ImageDraw.Draw(image)
	
	# Generate pixel values
	for imag, ipix in itertools.izip(imag_range, range(height)):
		for real, rpix in itertools.izip(real_range, range(width)):
			z = complex(real, imag)
			n = 255
			while abs(z) < 10 and n >= 5:
				z = z ** exponent + c
				n -= 5
			x = 0.0
			if n <= 10 or allPerlin:
				x = perlin.perlin((imag - imag_min + 1) * 25.0, (real - real_min + 1) * 25.0) * 100
				x = abs(x)
			drawer.point((ipix, rpix), fill=pickColor(n, x, real, imag)) # n varies between 255 and 5
	
	#time.increase()
	
	# And return results
	return image

def saveImage(path, c, n, colorBalance):
	julia(c, n, colorBalance).save(path)


if __name__ == "__main__":
	import sys
	julia(complex(sys.argv[1]), 3, pickColor=meganMix, width=1920, height=1920).save(sys.argv[2])

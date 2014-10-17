import julia, numpy, random
from PIL import Image, ImageDraw

def judge(image):
	l = image.getcolors()
	for i in l:
		count, color = i
		if color == (255, 255, 255):
			return int((count / (250.0 ** 2)) * 255)
	return 0
	

def mapper(width=75, height=75, real_min=-2.0, real_max=2.0, imag_min=-2.0, imag_max=2.0):
	
	# Generate evenly spaced values over real and imaginary ranges
	real_range = numpy.arange(real_min, real_max, (real_max - real_min) / width)
	imag_range = numpy.arange(imag_max, imag_min, (imag_min - imag_max) / height)
	
	# Obtain image to work with
	image = Image.new('RGB', (width, height), (0, 0, 0))
	drawer = ImageDraw.Draw(image)
	
	# Generate pixel values
	x = zip(imag_range, range(height))
	for imag, ipix in x:
		print "Reached: ", ipix
		y = zip(real_range, range(width))
		for real, rpix in y:
			z = complex(real, imag)
			x = judge(julia.julia(z, 2, pickColor=julia.cutoff, height=250, width=250))
			drawer.point((ipix, rpix), fill=(x, x, x)) # n varies between 255 and 5
	
	# Make a 'truer' representation of the julia set
	#image = image.filter(ImageFilter.FIND_EDGES)
	image.show()
	# And return results
	return image

mapper()

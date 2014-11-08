import julia, numpy, itertools
from PIL import Image, ImageDraw

def combined(c1, exp1, offset1, c2, exp2, offset2, width=500, height=500, real_min=-2.0, real_max=2.0, imag_min=-2.0, imag_max=2.0, pickColor=julia.timeBased, allPerlin = False):
	
	# Generate evenly spaced values over real and imaginary ranges
	real_range = numpy.arange(real_min, real_max, (real_max - real_min) / width)
	imag_range = numpy.arange(imag_max, imag_min, (imag_min - imag_max) / height)
	
	# Obtain image to work with
	image = Image.new('RGB', (width, height), (0, 0, 0))
	drawer = ImageDraw.Draw(image)
	
	# Generate pixel values
	for imag, ipix in itertools.izip(imag_range, range(height)):
		for real, rpix in itertools.izip(real_range, range(width)):
			z = complex(real, imag) + offset1
			n = 255
			while abs(z) < 10 and n >= 5:
				z = z ** exp1 + c1
				n -= 5
			m = 255
			z = (complex(real, imag) + offset2) * 2
			while abs(z) < 10 and n >= 5:
				z = z ** exp2 + c2
				n -= 5
			n = n - (m * 5)
			n = n % 255
			drawer.point((ipix, rpix), fill=pickColor(n, 0, real, imag)) # n varies between 255 and 5
	
	#time.increase()
	
	# And return results
	return image

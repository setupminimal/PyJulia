from PIL import Image
import julia

BASE = "anim"

for i in range(600):
	print i
	real_min, real_max, imag_min, imag_max = julia.pickViewWindow()
	x = julia.julia(julia.pickTimeInterest(), 3, 700, 700, real_min=real_min, real_max=real_max, imag_min=imag_min, imag_max=imag_max)
	x.save(BASE + str(i) + ".png")

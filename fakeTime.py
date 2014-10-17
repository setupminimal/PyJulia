import time

counter = 1413499835.0

class Fish():
	def __init__(self, counter):
		self.tm_hour = counter % (60 * 60 * 24)
		self.tm_min = counter % (60 * 60)
		self.tm_sec = counter % 60

def localtime():
	global counter
	counter += 0.5
	return Fish(counter)

def time():
	return counter

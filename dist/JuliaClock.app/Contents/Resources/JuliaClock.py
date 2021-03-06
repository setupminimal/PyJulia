import Tkinter as tk
from PIL import ImageTk
import julia, time, math, combinedJulia

WIDTH = 250
HEIGHT = 250

class JuliaWindow(tk.Frame):
	def __init__(self, parent):
		self.parent = parent
		tk.Frame.__init__(self)
		self.init_window()
	
	def update_image(self):
		ct = time.localtime()
		real_min, real_max, imag_min, imag_max = julia.pickViewWindow()
		#image1 = julia.julia(julia.pickTimeInterest(), ct.tm_hour % 6 + 2, WIDTH, HEIGHT, real_min = real_min, real_max = real_max, imag_min = imag_min, imag_max = imag_max)
		image1 = combinedJulia.combined(julia.pickTimeInterest(), ct.tm_hour % 6 + 2, 0, julia.pickTimeInterest(600.0), ct.tm_min % 15 + 2, julia.pickOffset(), WIDTH, HEIGHT, real_min = real_min, real_max = real_max, imag_min = imag_min, imag_max = imag_max)
		self.img = ImageTk.PhotoImage(image1)
		
		# set the label image
		self.julia_lbl.configure(image=self.img)
		self.julia_lbl.pack()
		
		self.parent.after(1000 * 10, self.update_image)
	
	def init_window(self):
		image1 = julia.julia(0.65 + 0.3j, 3, WIDTH, HEIGHT)
		self.img = ImageTk.PhotoImage(image1)
		
		self.julia_lbl = tk.Label(self, image=self.img)
		self.julia_lbl.pack(anchor=tk.N, side=tk.TOP, fill=tk.BOTH, expand=1)
		
		#self.update_btn = tk.Button(self, text="Update", command=lambda:self.update_image())
		#self.update_btn.pack(anchor=tk.S, side=tk.RIGHT)
		self.update_image()

if __name__ == "__main__":
	root = tk.Tk()
	jw = JuliaWindow(root)
	jw.pack()
	root.mainloop()

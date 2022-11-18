import time
import sys
import os
from PIL import Image, ImageOps

# import spotify
import nasa
import clock
from matrix import Matrix
import gradients
from gpiozero import Button
from signal import pause
import multiprocessing as mp
import pathlib
import snow
from typing import List, Callable, Any

class Controller:
	def __init__(self, mode_funcs: List[Callable[[Matrix], Any]], brightness: int=100) -> None:
		self.brightness = brightness
		self.m = Matrix(brightness=safe_brightness(brightness))
		self.mode_funcs = mode_funcs
		self.mode = 0
		self.mode_thread = mp.Process(target=mode_funcs[self.mode], args=(self.m,))
		self.start_mode()
	
	def next_mode(self):
		if self.mode_thread.is_alive():
			self.stop_mode()

		# Increment mode
		self.mode = (self.mode+1) % len(self.mode_funcs)
		self.start_mode()
	
	def start_mode(self):
		print(f"Starting mode {self.mode_funcs[self.mode].__name__}")
		self.mode_thread = mp.Process(target=self.mode_funcs[self.mode], args=(self.m,))
		self.mode_thread.start()

	def stop_mode(self):
		# Kill previous mode function
		self.mode_thread.kill()
		time.sleep(.5)
	
	def change_brightness(self, brighntess: int):
		if self.mode_thread.is_alive():
			self.stop_mode()
		self.brightness = safe_brightness(brighntess)
		
		self.m = Matrix(brightness=self.brightness)

		self.start_mode()

cwd = pathlib.Path(__file__).parent.resolve()

def safe_brightness(brightness):
	return max(min(brightness, 100), 1)

def digital_clock(m):
	# m = Matrix(brightness=safe_brightness(brightness))
	clock.square_clock(m)

def snow_animation(m):
	# m = Matrix(brightness=safe_brightness(brightness))
	snow.snow(m)

def nasa_apods(m):
	# m = Matrix(brightness=safe_brightness(brightness))
	im = Image.open(os.path.join(cwd, '../images/nasa.png'))
	m.show(im)
	m.set_image_processing([m.fill, ImageOps.autocontrast])
	nasa.random_apods(m, count=30)

def gradient(m):
	# m = Matrix(brightness=safe_brightness(brightness))
	gradients.infinite_random_gradient(m)

def off(m):
	pause()

controller = Controller([digital_clock, snow_animation, nasa_apods, gradient, off])

mode_btn = Button(pin=19)
mode_btn.when_pressed = controller.next_mode

brightness = 60

def change_brightness(btn: Button):
	global controller, brightness

	if btn == bright_up_btn:
		brightness = min(brightness + 5, 100)
	elif btn == bright_down_btn:
		brightness = max(brightness - 5, 0)
	
	# Restart mode with new brightness
	controller.stop_mode()

	print(f"Setting brightness to {brightness}%")
	controller.change_brightness(brightness)

bright_up_btn = Button(pin=14)
bright_up_btn.when_pressed = change_brightness

bright_down_btn = Button(pin=15)
bright_down_btn.when_pressed = change_brightness

pause()

# try:
# 	print("Press CTRL-C to stop.")
# 	while True:
# 		time.sleep(100)
# except KeyboardInterrupt:
# 	matrix_thread.kill()
# 	sys.exit(0)

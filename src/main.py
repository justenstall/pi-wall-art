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

cwd = pathlib.Path(__file__).parent.resolve()

def safe_brightness(brightness):
	return max(min(brightness, 100), 1)

def digital_clock(brightness):
	m = Matrix(brightness=safe_brightness(brightness))
	clock.square_clock(m)

def nasa_apods(brightness):
	m = Matrix(brightness=safe_brightness(brightness))
	im = Image.open(os.path.join(cwd, '../images/nasa.png'))
	m.show(im)
	m.set_image_processing([m.fill, ImageOps.autocontrast])
	nasa.random_apods(m, count=30)

def gradient(brightness):
	m = Matrix(brightness=safe_brightness(brightness))
	gradients.infinite_random_gradient(m)

def off(brightness):
	pause()

MODE_FUNCS = [digital_clock, nasa_apods, gradient, off]

mode = 0
brightness = 60

# Start initial mode
print(f"Starting mode {MODE_FUNCS[mode].__name__}")
matrix_thread = mp.Process(target=MODE_FUNCS[mode], args=(brightness,))
matrix_thread.start()

def iter_mode():
	global mode, brightness, matrix_thread

	# Increment mode
	mode = (mode+1) % len(MODE_FUNCS)

	# Kill previous mode function
	matrix_thread.kill()
	time.sleep(.5)
	
	# Start new mode function
	print(f"Starting mode {MODE_FUNCS[mode].__name__}")
	matrix_thread = mp.Process(target=MODE_FUNCS[mode], args=(brightness,))
	matrix_thread.start()

mode_btn = Button(pin=19)
mode_btn.when_pressed = iter_mode

def change_brightness(btn: Button):
	global mode, brightness, matrix_thread

	if btn == bright_up_btn:
		brightness = min(brightness + 5, 100)
	elif btn == bright_down_btn:
		brightness = max(brightness - 5, 0)
	
	# Restart mode with new brightness
	matrix_thread.kill()
	time.sleep(.5)

	print(f"Setting brightness to {brightness}%")
	matrix_thread = mp.Process(target=MODE_FUNCS[mode], args=(brightness,))
	matrix_thread.start()

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

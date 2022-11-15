import time
import sys
import itertools

# import spotify
import nasa
# import clock
from matrix import Matrix
import gradients
from gpiozero import Button
from signal import pause
import multiprocessing as mp

MODE_FUNCS = [gradients.run, nasa.run]

MODE_GRADIENT = 0
MODE_APOD = 1
MODE_SPOTIFY = 2
MODE_CLOCK = 3

mode = 0

print(f"Starting mode {MODE_FUNCS[mode].__name__}")
matrix_thread = mp.Process(target=MODE_FUNCS[mode], args=())
matrix_thread.start()
# https://stackoverflow.com/questions/32922909/how-to-stop-an-infinite-loop-safely-in-python
def iter_mode():
	global mode, matrix_thread
	mode = (mode+1) % len(MODE_FUNCS)
	print(f"Button pressed, starting mode {MODE_FUNCS[mode].__name__}")
	matrix_thread.kill()
	matrix_thread = mp.Process(target=MODE_FUNCS[mode], args=())
	matrix_thread.start()

mode_btn = Button(pin=19)
mode_btn.when_pressed = iter_mode

try:
	print("Press CTRL-C to stop.")
	while True:
		time.sleep(100)
except KeyboardInterrupt:
	matrix_thread.kill()
	sys.exit(0)
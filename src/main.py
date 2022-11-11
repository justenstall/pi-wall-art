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
from PIL import Image

m = Matrix()
loading = Image.open('../images/loading.gif')
m.show(loading)

MODE_FUNCS = [gradients.infinite_random_gradient, nasa.random_apods]

MODE_GRADIENT = 0
MODE_APOD = 1
MODE_SPOTIFY = 2
MODE_CLOCK = 3

mode = 0

print(f"Starting mode {MODE_FUNCS[mode].__name__}")
matrix_thread = mp.Process(target=MODE_FUNCS[mode], args=(), daemon=True)
matrix_thread.start()

def iter_mode():
	global m, mode, matrix_thread
	mode = (mode+1) % len(MODE_FUNCS)
	print(f"Button pressed, starting mode {MODE_FUNCS[mode].__name__}")
	matrix_thread.kill()
	matrix_thread = mp.Process(target=MODE_FUNCS[mode], args=(), daemon=True)
	matrix_thread.start()

mode_btn = Button(3)
mode_btn.when_pressed = iter_mode

pause()
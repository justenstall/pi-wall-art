from rgbmatrix import graphics
from PIL import Image
import numpy as np
import time

from matrix import Matrix

def snow(m: Matrix):
	'''
	Process:
	Generate binary array of same length as matrix row
	Set pixels to white or background color based on ones in array
	Iterate that array down the screen
	'''
	width = m.matrix.width
	height = m.matrix.height

	background_color = (1, 8, 27)
	snow_color = (255,255,255)

	snow = np.full([64, 64, 3], fill_value=background_color, dtype=np.uint8)

	while True:
		# snow = np.roll(snow, shift=1, axis=0)
		snow = np.delete(snow, len(snow))
		new_snow = np.random.choice([0, 1], size=width, p=[.95, .05])
		# snow[0] = [snow_color if pixel == 1 else background_color for pixel in new_snow]
		snow = np.insert(arr=snow, values=new_snow, obj=0)

		snow_im = Image.fromarray(snow, mode='RGB')
		m.show(snow_im)

		time.sleep(.2)

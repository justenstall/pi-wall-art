import math
from PIL import Image, ImageDraw, ImageFont
import os
import time
from datetime import datetime
import pathlib

from matrix import Matrix

cwd = pathlib.Path(__file__).parent.resolve()

def font_path(filename: str):
	return os.path.join(cwd.parent, "fonts", filename)

def digital_clock(m: Matrix):
	# Create default image without time
	clock_background = Image.new(mode='RGB', size=(64, 64))
	draw_background = ImageDraw.Draw(clock_background, mode='RGB')
	
	fnt = ImageFont.load(font_path("texgyre-27.pil"))
	# fnt = ImageFont.truetype(font_path("back-to-1982.regular.ttf", size=30)
	# fnt = ImageFont.truetype(font_path("square-pixel7.regular.ttf", size=30)
	# fnt = ImageFont.truetype(font_path("digitalix.ttf", size=16)
	# fnt = ImageFont.load(font_path("tom-thumb.pil")
	# fnt = ImageFont.load(font_path("helvR12.pil")
	
	while True:
		current_datetime = datetime.now()
		hour = current_datetime.hour % 12
		if hour == 0:
			hour = 12
		minute = current_datetime.minute

		time_text = f"{hour}:{minute:02d}"

		clock = clock_background.copy()
		draw = ImageDraw.Draw(clock, mode='RGB')
		draw.fontmode = "1"

		size = fnt.getbbox(time_text)

		x = ((63-size[2]) / 2) - 1
		y = (63-size[3]) / 2

		draw.text(xy=(x,y), text=time_text, font=fnt, fill=(255, 255, 255))
		
		m.show(clock)
		
		time.sleep(5)

def analog_clock(m: Matrix):
	hour_hand_length = 10
	minute_hand_length = 20
	center_point = (32, 32)

	# Create default clock without hands
	clock_background = Image.new(mode='RGB', size=(64, 64))
	draw_background = ImageDraw.Draw(clock_background, mode='RGB')
	draw_background.ellipse([(0, 0), (63, 63)], outline='white', fill='black', width=1)

	while True:
		clock = clock_background.copy()
		draw = ImageDraw.Draw(clock, mode='RGB')

		current_datetime = datetime.now()
		hour = current_datetime.hour % 12
		minute = current_datetime.minute

		hour_angle = (hour / 12) * 360
		minute_angle = (minute / 60) * 360

		hx = hour_hand_length * math.cos(hour_angle)
		hy = hour_hand_length * math.sin(hour_angle)
		mx = minute_hand_length * math.cos(minute_angle)
		my = minute_hand_length * math.sin(minute_angle)
		

		draw.line([center_point, (hx, hy)], fill='white', width=1)
		draw.line([center_point, (mx, my)], fill='white', width=1)

		m.show(clock)

		print(f"{hour}:{minute}")
		time.sleep(5)

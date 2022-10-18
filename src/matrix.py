import requests, time, itertools, os

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageOps, ImageFont, ImageDraw
from io import BytesIO
from typing import Callable, Union
from urllib.parse import urlparse
import imagehash

class Matrix:
    def __init__(self, brightness: int=100, limit_refresh_rate_hz: int=-1, show_refresh_rate: bool=False, font: str='/home/pi/pi-wall-art/fonts/4x6.bdf') -> None:
        # Initialize RGB Matrix object
        self.options = RGBMatrixOptions()
        self.options.rows = 64
        self.options.cols = 64
        self.options.brightness = brightness
        self.options.pwm_dither_bits = 1
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = "adafruit-hat-pwm"
        self.options.drop_privileges = False
        
        self.options.show_refresh_rate = show_refresh_rate
        if limit_refresh_rate_hz > 0:
            self.options.limit_refresh_rate_hz = limit_refresh_rate_hz

        self.matrix = RGBMatrix(options=self.options)

        # Caching features initialization
        self.image_cache_dir = 'image_cache'
        self.image_cache = {}

        self.processing_funcs: list[Callable[[Image.Image], Image.Image]] = [self.fill]

        self.resampling = Image.Resampling.LANCZOS

        self.image = Image.new('RGB', (64, 64))

        # self.font = ImageFont.load(font)
    
    # Set the image processing functions that will run on each image displayed to the matrix
    def set_image_processing(self, processing_funcs: list[Callable[[Image.Image], Image.Image]]):
        self.processing_funcs = processing_funcs
    
    def add_image_processing(self, processing_func: Callable[[Image.Image], Image.Image]):
        self.processing_funcs.append(processing_func)

    def loop_images(self, image_urls: list[str], image_descriptions: list[str]=[]):
        # processed_image_cache = 'processed_images'
        for i, image_url in itertools.cycle(enumerate(image_urls)):
            im = Image.new('RGB', size=(self.matrix.width, self.matrix.height))
            if image_url in self.image_cache:
                im = self.image_cache[image_url]
            else:
                im = self.get_image_from_url(image_url)
                self.image_cache[image_url] = im

            if len(image_descriptions) >= i:
                self.show(im, description=image_descriptions[i])
                time.sleep(5)
                self.show(im)
                time.sleep(7)
            else:
                self.show(im)
                time.sleep(10)

    def process_image(self, im: Image.Image) -> Image.Image:
        for func in self.processing_funcs: im = func(im)
        return im.convert('RGB')
    
    def size_to_matrix(self, im: Image.Image):
        im.thumbnail((self.matrix.width, self.matrix.height), self.resampling)
        return im
    
    def get_image_from_url(self, image_url: str):
        img_data = BytesIO(requests.get(image_url).content)
        im = Image.open(img_data)
        return im

    def show(self, im: Image.Image, description: Union[str,None]=None):
        image_hash = imagehash.average_hash(im)
        description_hash = f"{image_hash}-{description}"
        if image_hash in self.image_cache:
            # print('using image from cache')
            im = self.image_cache[image_hash]
            if description_hash in self.image_cache:
                im = self.image_cache[description_hash]
        else:
            im = self.process_image(im)
            self.image_cache[image_hash] = im
            if description:
                description_image = im.copy()
                print(description)
                draw = ImageDraw.Draw(description_image)
                left_offset = (self.matrix.width-draw.textlength(description))/2
                top_offest = self.matrix.height-left_offset-9
                draw.text((left_offset, top_offest), description, fill=(255, 255, 255, 128))
                im = description_image
                self.image_cache[description_hash] = im

        self.matrix.SetImage(im)
        self.image = im
    
    def display_image_from_url(self, image_url: str):
        print(f"Displaying image {image_url}")

        im = self.get_image_from_url(image_url)

        im = self.size_to_matrix(im)

        for func in self.processing_funcs: im = func(im)

        self.show(im)
    
    def fit(self, im: Image.Image, fill_color=(0, 0, 0, 0)):
        x, y = im.size
        largest_size = max(self.matrix.width, self.matrix.height, x, y)
        fit_size = (largest_size, largest_size)
        new_im = Image.new('RGB', fit_size, fill_color)
        new_im.paste(im, (int((fit_size[0] - x) / 2), int((fit_size[1] - y) / 2)))
        return new_im.convert('RGB')

    def fill(self, im: Image.Image, ):
        return ImageOps.fit(im, (self.matrix.width, self.matrix.height), self.resampling).convert('RGB')


    # Based on: https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/bindings/python/samples/runtext.py
    def overlay_text(self, text: str):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width

        while True:
            offscreen_canvas.Clear()
            offscreen_canvas.SetImage(self.image)
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# TODO: cache images with the processing, so the processing only happens the first time the image is displayed, then delete the temp folder of images after execution

import requests, time, itertools, os

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageOps, ImageFont, ImageDraw
from io import BytesIO
from typing import Callable, Union
from urllib.parse import urlparse
import imagehash
from xdg import xdg_cache_home

class Matrix:
    def __init__(self, brightness: int=100, limit_refresh_rate_hz: int=-1, show_refresh_rate: bool=False) -> None:
        # Initialize RGB Matrix object
        self.options = RGBMatrixOptions()
        self.options.rows = 64
        self.options.cols = 64
        self.options.brightness = brightness
        self.options.hardware_mapping = "adafruit-hat-pwm"
        self.options.drop_privileges = False

        # Runtime options for better performance on Raspberry Pi 4
        self.options.pwm_dither_bits = 1
        self.options.gpio_slowdown = 4
        
        self.options.show_refresh_rate = show_refresh_rate
        if limit_refresh_rate_hz > 0:
            self.options.limit_refresh_rate_hz = limit_refresh_rate_hz

        self.matrix = RGBMatrix(options=self.options)

        # Caching features initialization
        # self.image_cache = FileCache()
        self.image_cache = MemoryCache()

        self.processing_funcs: list[Callable[[Image.Image], Image.Image]] = [self.fill]

        # self.resampling = Image.Resampling.LANCZOS
        self.resampling = Image.Resampling.HAMMING

        self.image = Image.new('RGB', (64, 64))
    
    # Set the image processing functions that will run on each image displayed to the matrix
    def set_image_processing(self, processing_funcs: list[Callable[[Image.Image], Image.Image]]):
        self.processing_funcs = processing_funcs
    
    def add_image_processing(self, processing_func: Callable[[Image.Image], Image.Image]):
        self.processing_funcs.append(processing_func)

    def loop_image_urls(self, image_urls: list[str], delay: int=10):
        # processed_image_cache = 'processed_images'
        for i, image_url in itertools.cycle(enumerate(image_urls)):
            self.show_url(image_url)
            time.sleep(delay)

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

    def show(self, im: Image.Image):
        image_hash = imagehash.average_hash(im)
        if self.image_cache.exists(image_hash):
            im = self.image_cache.retrieve(image_hash)
        else:
            im = self.process_image(im)
            self.image_cache.store(image_hash, im)

        self.matrix.Clear()
        self.matrix.SetImage(im)
        self.image = im
    
    def show_url(self, image_url: str):
        key = key_from_url(image_url)
        if self.image_cache.exists(key):
            im = self.image_cache.retrieve(key)
        else:
            im = self.get_image_from_url(image_url)
            im = self.process_image(im)
            self.image_cache.store(key, im)

        self.matrix.Clear()
        self.matrix.SetImage(im)
        self.image = im
    
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
        font.LoadFont("../fonts/5x7.bdf")
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

def key_from_url(url):
    filename = os.path.basename(urlparse(url).path)
    return os.path.splitext(filename)[0]

# TODO: cache images with the processing, so the processing only happens the first time the image is displayed, then delete the temp folder of images after execution

class FileCache:
    def __init__(self, path: str=os.path.join(xdg_cache_home(), 'pi-wall-art', 'images'), prefix: str = "") -> None:
        self.path = path
        self.prefix = prefix
        os.makedirs(path, exist_ok=True)

    def _key_to_fp(self, key):
        return os.path.join(self.path, f"{self.prefix}{key}.jpg")
    
    def store(self, key, image: Image.Image):
        filename = self._key_to_fp(key)
        open(filename, 'w')
        image.save(filename)
    
    def retrieve(self, key):
        return Image.open(self._key_to_fp(key))
    
    def exists(self, key):
        return os.path.exists(self._key_to_fp(key))

class MemoryCache:
    def __init__(self) -> None:
        self.cache = {}

    def store(self, key, im: Image.Image):
        self.cache[key] = im
    
    def retrieve(self, key):
        return self.cache[key]
    
    def exists(self, key):
        return key in self.cache
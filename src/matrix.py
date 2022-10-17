import requests, time, itertools, os

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageOps
from io import BytesIO
from typing import Callable, Union
from urllib.parse import urlparse

class Matrix:
    def __init__(self, brightness: int=100, limit_refresh_rate_hz: int=-1, show_refresh_rate: bool=False) -> None:
        # Initialize RGB Matrix object
        self.options = RGBMatrixOptions()
        self.options.rows = 64
        self.options.cols = 64
        self.options.brightness = brightness
        self.options.pwm_dither_bits = 1
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = "adafruit-hat-pwm"
        
        self.options.show_refresh_rate = show_refresh_rate
        if limit_refresh_rate_hz > 0:
            self.options.limit_refresh_rate_hz = limit_refresh_rate_hz

        self.matrix = RGBMatrix(options=self.options)

        # Caching features initialization
        self.image_cache = 'image_cache'

        self.processing_funcs: list[Callable[[Image.Image], Image.Image]] = [self.fill]

        self.resampling = Image.Resampling.LANCZOS
    
    # Set the image processing functions that will run on each image displayed to the matrix
    def set_image_processing(self, processing_funcs: list[Callable[[Image.Image], Image.Image]]):
        self.processing_funcs = processing_funcs
    
    def add_image_processing(self, processing_func: Callable[[Image.Image], Image.Image]):
        self.processing_funcs.append(processing_func)
    
    def loopImageURLs(self, image_urls: list[str]):
        # processed_image_cache = 'processed_images'
        for _, image_url in itertools.cycle(enumerate(image_urls)):
            im = self.get_image_from_url(image_url)
            self.show(im)
            time.sleep(5)

    def loopImages(self, images: list[Image.Image]):
        for i, im in itertools.cycle(enumerate(images)):
            self.show(im)
            time.sleep(10)

    def process_image(self, im: Image.Image) -> Image.Image:
        for func in self.processing_funcs: im = func(im)
        return im.convert('RGB')
    
    def size_to_matrix(self, im: Image.Image):
        im.thumbnail((self.matrix.width, self.matrix.height), self.resampling)
        return im
    
    def get_image_from_url(self, image_url: str):
        # Check cached images
        # image_name = os.path.basename(urlparse(image_url).path)
        # cached_image_path = os.path.join(cache_folder, image_name)
        # if os.path.exists(cached_image_path):
        #     print("Reading image from cache")
        #     return Image.open(cached_image_path)

        img_data = BytesIO(requests.get(image_url).content)

        im = Image.open(img_data)

        # try:
        #     os.makedirs(cache_folder, exist_ok = True)
        #     # print("Directory '%s' created successfully" % cache_folder)
        #     im.save(cached_image_path, "JPEG")
        # except OSError as error:
        #     print("Directory '%s' cannot be created" % cache_folder)    

        return im

    def show(self, im: Image.Image):
        im = self.process_image(im)
        self.matrix.SetImage(im)
    
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

# TODO: cache images with the processing, so the processing only happens the first time the image is displayed, then delete the temp folder of images after execution

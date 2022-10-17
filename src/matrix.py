import requests, time, itertools, os

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageOps
from io import BytesIO
from typing import Callable, Union
from urllib.parse import urlparse

def init_matrix():
	# Initialize RGB Matrix object
	matrix_options = RGBMatrixOptions()
	matrix_options.rows = 64
	matrix_options.cols = 64
	# matrix_options.show_refresh_rate = True
	matrix_options.brightness = 100
	matrix_options.pwm_dither_bits = 1
	matrix_options.chain_length = 1
	matrix_options.parallel = 1
	matrix_options.hardware_mapping = "adafruit-hat-pwm"
	# matrix_options.limit_refresh_rate_hz = 80 

	matrix = RGBMatrix(options=matrix_options)

	return matrix

def default_processing(im: Image.Image):
    im = fill(im, size=64)
    im = size_to_matrix(im)
    return im

# TODO: cache images with the processing, so the processing only happens the first time the image is displayed, then delete the temp folder of images after execution
image_cache = 'image_cache'

def display_image_from_url(m: RGBMatrix, image_url: str, processing_funcs: list[Callable[[Image.Image], Image.Image]]=[]):
    print(f"Displaying image {image_url}")

    im = get_image_from_url(image_url)

    im = size_to_matrix(im)

    for func in processing_funcs: im = func(im)

    m.SetImage(im)

def size_to_matrix(im: Image.Image):
    im.thumbnail((64, 64), Image.Resampling.NEAREST)
    return im

def fit(im: Image.Image, size=(64, 64), fill_color=(0, 0, 0, 0)):
    x, y = im.size
    largest_size = max(size[0], size[1], x, y)
    fit_size = (largest_size, largest_size)
    new_im = Image.new('RGB', fit_size, fill_color)
    new_im.paste(im, (int((fit_size[0] - x) / 2), int((fit_size[1] - y) / 2)))
    return new_im.convert('RGB')

def fill(im: Image.Image, size=64):
    return ImageOps.fit(im, (size, size), Image.Resampling.LANCZOS).convert('RGB')

class Fade:
    def __init__(self, m: RGBMatrix, image1: Image.Image, image2: Image.Image) -> None:
        self.alpha = 0
        self.matrix = m
        self.image1 = image1
        self.image2 = image2
    
    def fade(self):
        # stop fading once alpha == 1(a.k.a.second image)
        if self.alpha > 1.0:
            return "done!"

        # create the interpolated image using the current alpha value
        new_img = Image.blend(self.image1, self.image2, self.alpha)
        self.alpha += 0.1

        # update the image displayed continuously to create the "fade" effect
        self.matrix.SetImage(new_img)
        time.sleep(1)
        return self.fade

def loopImages(m: RGBMatrix, images: list[Image.Image]):
    for i, im in itertools.cycle(enumerate(images)):
        m.SetImage(im)
        time.sleep(10)

def loopImageURLs(m: RGBMatrix, image_urls: list[str], processing_funcs: list[Callable[[Image.Image], Image.Image]]=[]):
    # processed_image_cache = 'processed_images'
    for _, image_url in itertools.cycle(enumerate(image_urls)):
        im = get_image_from_url(image_url, processing_funcs=processing_funcs)

        m.SetImage(im)
        time.sleep(5)

def get_image_from_url(image_url: str, cache_folder: str='image_cache', processing_funcs: list[Callable[[Image.Image], Image.Image]]=[]):
    # Check cached images
    image_name = os.path.basename(urlparse(image_url).path)
    cached_image_path = os.path.join(cache_folder, image_name)
    if os.path.exists(cached_image_path):
        print("Reading image from cache")
        return Image.open(cached_image_path)

    img_data = BytesIO(requests.get(image_url).content)

    im = Image.open(img_data)

    im = size_to_matrix(im)

    for func in processing_funcs: im = func(im)

    try:
        os.makedirs(cache_folder, exist_ok = True)
        # print("Directory '%s' created successfully" % cache_folder)
        im.save(cached_image_path, "JPEG")
    except OSError as error:
        print("Directory '%s' cannot be created" % cache_folder)    

    return im
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import requests
import string
from PIL import Image, ImageOps
from io import BytesIO
import time
import itertools

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
    im = ImageOps.autocontrast(im)
    return im

def get_image_from_url(image_url):
    response = requests.get(image_url)

    img_data = BytesIO(response.content)

    image = Image.open(img_data)

    return image

def display_image_from_url(m: RGBMatrix, image_url):
    print(f"Displaying image {image_url}")

    im = get_image_from_url(image_url)

    # Make image fit our screen.
    im.thumbnail((m.width, m.height),
                    Image.Resampling.LANCZOS)

    m.SetImage(im)

def fit(im: Image.Image, size=(64, 64), fill_color=(0, 0, 0, 0)):
    im.thumbnail(size, Image.Resampling.LANCZOS)
    x, y = im.size
    largest_size = max(size[0], size[1], x, y)
    fit_size = (largest_size, largest_size)
    new_im = Image.new('RGB', fit_size, fill_color)
    new_im.paste(im, (int((fit_size[0] - x) / 2), int((fit_size[1] - y) / 2)))
    return new_im.convert('RGB')

def fill(im: Image.Image, size=64):
    im.thumbnail((size, size), Image.Resampling.LANCZOS)
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

def loopImageURLs(m: RGBMatrix, image_urls: list[str]):
    for i, url in itertools.cycle(enumerate(image_urls)):
        m.SetImage(default_processing(get_image_from_url(url)))
        time.sleep(5)

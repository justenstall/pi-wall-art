import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from io import BytesIO
import datetime

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
	matrix_options.limit_refresh_rate_hz = 120

	matrix = RGBMatrix(options=matrix_options)

	return matrix

def display_image_from_url(m: RGBMatrix, image_url):
    print(f"Displaying image {image_url}")

    response = requests.get(image_url)

    img_data = BytesIO(response.content)

    image = Image.open(img_data)

    # Make image fit our screen.
    image.thumbnail((m.width, m.height),
                    Image.Resampling.LANCZOS)

    m.SetImage(fit(image).convert('RGB'))

def fit(im, min_size=64, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

def fill(im, max_size=64, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = min(max_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


pp = PrettyPrinter()

apiKey = 'IdK13tM9IR9PhWbCLfgi9esC7Gig5R2ItfDbOH2C'

def fetchAPOD(date='2020-01-22'):
  URL_APOD = "https://api.nasa.gov/planetary/apod"

  params = {
      'api_key': apiKey,
      'date': date,
      'hd': 'True'
  }
  response = requests.get(URL_APOD,params=params).json()
  pp.pprint(response)

  return response

# Main code
m = init_matrix()

start_date = datetime.date(2022, 1, 1)
today = datetime.date.today()
daydelta = datetime.timedelta(days=1)

while start_date <= today:
  response = fetchAPOD(start_date.isoformat())
  if response['media_type'] == 'image' and 'url' in response:
    display_image_from_url(m, response['url'])
    time.sleep(1)
  start_date += daydelta

try:
  print("Press CTRL-C to stop.")
  while True:
    time.sleep(100)
except KeyboardInterrupt:
  sys.exit(0)
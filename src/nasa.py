import requests
import datetime
from pprint import PrettyPrinter
from matrix import Matrix
from PIL import ImageOps

apiKey = 'IdK13tM9IR9PhWbCLfgi9esC7Gig5R2ItfDbOH2C'

pp = PrettyPrinter()

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

def fetch_random_apod(count=1):
  URL_APOD = "https://api.nasa.gov/planetary/apod"

  params = {
      'api_key': apiKey,
      'count': count,
      'hd': 'True'
  }

  response = requests.get(URL_APOD,params=params).json()
  pp.pprint(response)

  return response

def loop_apods(m: Matrix):
  start_date = datetime.date(2022, 1, 1)
  today = datetime.date.today()
  daydelta = datetime.timedelta(days=1)

  image_urls = []

  # currentImage = Image.new('RGB', (64, 64), (0, 0, 0, 0))

  while start_date < today:
    response = fetchAPOD(start_date.isoformat())
    if response['media_type'] == 'image' and 'url' in response:
      image_urls.append(response['url'])
    start_date += daydelta
  
  m.loop_images(image_urls)

def random_apods(m: Matrix, count: int=30):
  responses = fetch_random_apod(count=count)

  image_urls = []
  image_descriptions = []

  for r in responses:
    if r['media_type'] == 'image':
      image_urls.append(r['url'])
      image_descriptions.append(f"{r['date']}: {r['title']}")

  m.loop_images(image_urls, image_descriptions=image_descriptions)

m = Matrix()
m.set_image_processing([m.fill, ImageOps.autocontrast])

random_apods(m)
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

def fetchRandomAPOD(count=1):
  URL_APOD = "https://api.nasa.gov/planetary/apod"

  params = {
      'api_key': apiKey,
      'count': count,
      'hd': 'True'
  }

  response = requests.get(URL_APOD,params=params).json()
  pp.pprint(response)

  return response

def loopAPODs(m: Matrix):
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
  
  m.loopImageURLs(image_urls)

def randomAPODs(m: Matrix):
  responses = fetchRandomAPOD(count=30)

  image_urls = [r['url'] for r in responses if r['media_type'] == 'image']

  pp.pprint(image_urls)

  m.loopImageURLs(image_urls)

m = Matrix()
m.set_image_processing([m.fill, ImageOps.autocontrast])
randomAPODs(m)
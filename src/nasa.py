import requests
import datetime
from pprint import PrettyPrinter
from rgbmatrix import RGBMatrix
import matrix

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

def loopAPODs(m: RGBMatrix):
  start_date = datetime.date(2022, 1, 1)
  today = datetime.date.today()
  daydelta = datetime.timedelta(days=1)

  apodImages = []

  # currentImage = Image.new('RGB', (64, 64), (0, 0, 0, 0))

  while start_date < today:
    response = fetchAPOD(start_date.isoformat())
    if response['media_type'] == 'image' and 'url' in response:
      im = matrix.get_image_from_url(response['url'])
      im = matrix.fill(im, size=64)
      apodImages.append(im)
    start_date += daydelta
  
  matrix.loopImages(m, apodImages)

def randomAPODs(m: RGBMatrix):
  responses = fetchRandomAPOD(count=30)

  image_urls = [r['url'] for r in responses if r['media_type'] == 'image']

  # for response in responses:
  #   if response['media_type'] == 'image' and 'url' in response:
  #     image_urls.append(response['url'])

  matrix.loopImageURLs(m, image_urls)

randomAPODs(matrix.init_matrix())

# TODO: cache images with the processing, so the processing only happens the first time the image is displayed, then delete the temp folder of images after execution
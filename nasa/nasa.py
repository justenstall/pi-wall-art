import requests
from urllib.request import urlretrieve
from pprint import PrettyPrinter

from matrix.matrix import display_image_from_url, init_matrix

pp = PrettyPrinter()

apiKey = 'IdK13tM9IR9PhWbCLfgi9esC7Gig5R2ItfDbOH2C'

def fetchAPOD():
  URL_APOD = "https://api.nasa.gov/planetary/apod"
  date = '2020-01-22'
  params = {
      'api_key': apiKey,
      'date': date,
      'hd': 'True'
  }
  response = requests.get(URL_APOD,params=params).json()
  pp.pprint(response)

  return response

response = fetchAPOD()

m = init_matrix()

display_image_from_url(m, response['url'])

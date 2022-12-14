import requests
import datetime
from matrix import Matrix
from PIL import Image, ImageOps
from mysecrets import nasa as secrets

from pprint import PrettyPrinter
pp = PrettyPrinter()

'''
APOD API
'''

def fetch_apod(date='2020-01-22'):
    URL_APOD = "https://api.nasa.gov/planetary/apod"

    params = {
        'api_key': secrets['api_key'],
        'date': date,
        'hd': 'True'
    }

    response = requests.get(URL_APOD, params=params).json()
    pp.pprint(response)

    return response

def fetch_random_apod(count=1):
    URL_APOD = "https://api.nasa.gov/planetary/apod"

    params = {
        'api_key': secrets['api_key'],
        'count': count,
        'hd': 'True'
    }

    response = requests.get(URL_APOD, params=params).json()
    # pp.pprint(response)

    return response


def loop_apods(m: Matrix):
    start_date = datetime.date(2022, 1, 1)
    today = datetime.date.today()
    daydelta = datetime.timedelta(days=1)

    image_urls = []

    # currentImage = Image.new('RGB', (64, 64), (0, 0, 0, 0))

    while start_date < today:
        response = fetch_apod(start_date.isoformat())
        if response['media_type'] == 'image' and 'url' in response:
            image_urls.append(response['url'])
        start_date += daydelta

    m.loop_image_urls(image_urls)

def random_apods(m: Matrix, count: int = 30, delay: int=10):
    responses = fetch_random_apod(count=count)

    image_urls = []
    image_descriptions = []

    for r in responses:
        if r['media_type'] == 'image':
            image_urls.append(r['url'])
            image_descriptions.append(r['date'])

    m.loop_image_urls(image_urls, delay=delay)

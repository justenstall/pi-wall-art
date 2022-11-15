import requests
import datetime
from pprint import PrettyPrinter
from matrix import Matrix
from PIL import Image, ImageOps

nasa_api_key = 'IdK13tM9IR9PhWbCLfgi9esC7Gig5R2ItfDbOH2C'

pp = PrettyPrinter()

'''
APOD API
'''

def fetch_apod(date='2020-01-22'):
    URL_APOD = "https://api.nasa.gov/planetary/apod"

    params = {
        'api_key': nasa_api_key,
        'date': date,
        'hd': 'True'
    }

    response = requests.get(URL_APOD, params=params).json()
    pp.pprint(response)

    return response

def fetch_random_apod(count=1):
    URL_APOD = "https://api.nasa.gov/planetary/apod"

    params = {
        'api_key': nasa_api_key,
        'count': count,
        'hd': 'True'
    }

    response = requests.get(URL_APOD, params=params).json()
    pp.pprint(response)

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

    m.loop_images(image_urls)

def random_apods(m: Matrix, count: int = 30):
    responses = fetch_random_apod(count=count)

    image_urls = []
    image_descriptions = []

    for r in responses:
        if r['media_type'] == 'image':
            image_urls.append(r['url'])
            # image_descriptions.append(f"{r['date']}: {r['title']}")
            image_descriptions.append(r['date'])

    m.loop_images(image_urls, image_descriptions=image_descriptions)

# KEY_JWST = ''


# def get_jwst_images():
#     URL_JWST_JPG = 'https://api.jwstapi.com/all/type/jpg'
#     response = requests.get(URL_JWST_JPG, headers={'X-API-KEY': KEY_JWST})
#     return response

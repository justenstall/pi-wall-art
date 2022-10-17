
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pprint import PrettyPrinter

# ---------- FREE API KEY examples ---------------------

pp = PrettyPrinter()

# Enter your API key here
api_key = "ee04be0e2d8e86b94d82ba182b5319cd"

owm = OWM(api_key)
mgr = owm.weather_manager()

# Search for current weather in London (Great Britain) and get details
observation = mgr.weather_at_place('London,GB')
if observation is None:
	print('Could not observe weather at place')
	exit(1)

w = observation.weather

w.detailed_status         # 'clouds'
w.wind()                  # {'speed': 4.6, 'deg': 330}
w.humidity                # 87
w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
w.rain                    # {}
w.heat_index              # None
w.clouds                  # 75

# Will it be clear tomorrow at this time in Milan (Italy) ?
forecast = mgr.forecast_at_place('Milan,IT', 'daily')
if forecast is None:
	print('Could not get forecast')
	exit(1)

answer = forecast.will_be_clear_at(timestamps.tomorrow())

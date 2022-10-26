import os
import requests
import datetime
from pprint import PrettyPrinter
from dateutil import parser

pp = PrettyPrinter()

URL_NFL = "https://api.sportsdata.io/v3/nfl/scores/json/"
TOKEN_NFL = os.environ['NFL_KEY']
print(TOKEN_NFL)

def get_browns_schedule(season: str=str(datetime.date.today().year)):
	headers = {
		'Ocp-Apim-Subscription-Key': TOKEN_NFL,
	}

	request_url = f'{URL_NFL}/Schedules/{season}'
	print(request_url)
	schedule = requests.get(request_url, headers=headers).json()
	# pp.pprint(response)

	browns_schedule = []

	for i, game in enumerate(schedule):
		if game['HomeTeam'] == 'CLE' or game['AwayTeam'] == 'CLE':
			browns_schedule.append(game)

	return browns_schedule

schedule = get_browns_schedule()

for game in schedule:
	gameday = parser.parse(game['DateTime'])
	print(f'{gameday.month}/{gameday.day}: {game["AwayTeam"]}@{game["HomeTeam"]}')
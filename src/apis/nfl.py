import requests

URL = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

def get_all_games():
	try:
		res = requests.get(URL)
		res = res.json()
		games = []
		for g in res['events']:
			info = g['competitions'][0]
			game = {'name': g['shortName'], 'date': g['date'],
						'hometeam': info['competitors'][0]['team']['abbreviation'], 'homeid': info['competitors'][0]['id'], 'homescore': int(info['competitors'][0]['score']),
						'awayteam': info['competitors'][1]['team']['abbreviation'], 'awayid': info['competitors'][1]['id'], 'awayscore': int(info['competitors'][1]['score']),
						'down': info.get('situation', {}).get('shortDownDistanceText'), 'spot': info.get('situation', {}).get('possessionText'),
						'time': info['status']['displayClock'], 'quarter': info['status']['period'], 'over': info['status']['type']['completed'],
						'redzone': info.get('situation', {}).get('isRedZone'), 'possession': info.get('situation', {}).get('possession'), 'state': info['status']['type']['state']}
			games.append(game)
		return games
	except requests.exceptions.RequestException as e:
		print("Error encountered getting game info, can't hit ESPN api, retrying")
	except Exception as e:
		print("something bad?", e)

# from pprint import PrettyPrinter
# pp = PrettyPrinter()

# games = get_all_games()
# pp.pprint(games)

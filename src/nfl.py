import time
from apis import nfl
from pprint import PrettyPrinter
pp = PrettyPrinter()

def live_scores():
	while True:
		games = nfl.get_all_games()
		if games is None:
			print("Could not get games")
			continue
		for game in games:
			if is_team(game, "CLE"):
				pp.pprint(game)
			# print(game['name'])

		# time.sleep(60*3)
		time.sleep(30)

def is_team(game, team_name: str):
	return game['hometeam'] == team_name or game['awayteam'] == team_name

def scoreboard(game):
	

live_scores()

'''
{'awayid': '6',
  'awayscore': 40,
  'awayteam': 'DAL',
  'date': '2022-11-20T21:25Z',
  'down': None,
  'homeid': '16',
  'homescore': 3,
  'hometeam': 'MIN',
  'name': 'DAL @ MIN',
  'over': True,
  'possession': None,
  'quarter': 4,
  'redzone': None,
  'spot': None,
  'state': 'post',
  'time': '0:00'},
'''

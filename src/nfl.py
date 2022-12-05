import time
import os
from apis import nfl
from pprint import PrettyPrinter
pp = PrettyPrinter()
import pathlib

import nfl_data_py as nfldata
from PIL import Image, ImageDraw, ImageFont
from matrix import Matrix


from nflteamdata import teams

cwd = pathlib.Path(__file__).parent.resolve()

def live_scores(m: Matrix):
   while True:
      games = nfl.get_all_games()
      if games is None:
         print("Could not get games")
         continue
      pp.pprint(games)
      for game in games:
         pp.pprint(game)
         sb = scoreboard(game)
         m.matrix.Clear()
         m.matrix.SetImage(sb)
         time.sleep(10)
      time.sleep(10)

def team_score(m: Matrix, team: str):
   while True:
      games = nfl.get_all_games()
      if games is None:
         print("Could not get games")
         continue
      for game in games:
         if is_team(game, team):
            sb = scoreboard(game)
            m.matrix.Clear()
            m.matrix.SetImage(sb)
      time.sleep(20)

def is_team(game, team_name: str):
   return game['hometeam'] == team_name or game['awayteam'] == team_name

def get_team_logo(team_code):
   im_path = os.path.join(cwd, teams[team_code]['logo'])
   im = Image.open(fp=im_path)
   im.thumbnail((24, 24), Image.Resampling.HAMMING)
   return im

def scoreboard(game):
   sb = Image.new(mode='RGB', size=(64,64))

   # Draw team logos
   away_logo = get_team_logo(game['awayteam'])
   home_logo = get_team_logo(game['hometeam'])
   sb.paste(away_logo, box=(4,8))
   sb.paste(home_logo, box=(36,8))

   # Initialize drawing interface
   draw_sb = ImageDraw.Draw(sb, mode='RGB')

   small_font = ImageFont.load(font_path("tom-thumb.pil"))
   score_font = ImageFont.truetype(font_path("KdamThmorPro-Regular.ttf"), size=22)
   draw_sb.fontmode = "1"

   # Draw scores
   draw_sb.text(xy=(4,28), text=str(game['awayscore']), font=score_font)
   draw_sb.text(xy=(36,28), text=str(game['homescore']), font=score_font)

   # Draw @ symbol
   draw_sb.text(xy=(30, 20), text='@', font=small_font)
   
   # Draw possession dot
   if game['possession'] == 'away':
      draw_sb.ellipse(xy=[(12, 46), (14, 48)], width=2)
   elif game['possession'] == 'home':
      draw_sb.ellipse(xy=[(44, 46), (46, 48)], width=2)

   # Draw time/quarter or 'FINAL'
   if game['over']:
      # draw_sb.fontmode = "1"
      draw_sb.text(xy=(24, 2), text='FINAL', font=small_font)
   else:
      draw_sb.text(xy=(20, 2), text=f"{game['time']} Q{game['quarter']}", font=small_font)

   return sb

def font_path(filename: str):
	return os.path.join(cwd.parent, "fonts", filename)

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

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
         if is_team(game, "CLE"):
            pp.pprint(game)
            sb = scoreboard(game)
            m.matrix.Clear()
            m.matrix.SetImage(sb)
      time.sleep(30)

def is_team(game, team_name: str):
   return game['hometeam'] == team_name or game['awayteam'] == team_name

def get_team_logo(team_code):
   im_path = os.path.join(cwd, teams[team_code]['logo'])
   print(im_path)
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

   draw_sb = ImageDraw.Draw(sb, mode='RGB')
   # score_font = ImageFont.load(font_path("9x18.pil"))
   # score_font = ImageFont.truetype(font_path("digitalix.ttf"), size=10)
   # score_font = ImageFont.truetype(font_path("UpheavalPro.ttf"), size=18)
   score_font = ImageFont.truetype(font_path("square-pixel7.regular.ttf"), size=24)
   # score_font = ImageFont.truetype(font_path("bm_receipt.ttf"), size=16)
   # draw_sb.fontmode = "1"
   # Draw scores
   draw_sb.text(xy=(4,32), text=str(game['awayscore']), font=score_font)
   draw_sb.text(xy=(36,32), text=str(game['homescore']), font=score_font)

   return sb

def font_path(filename: str):
	return os.path.join(cwd.parent, "fonts", filename)

# live_scores()
# teams = nfldata.import_team_desc()
# teams.to_csv("nfldata.csv")

m = Matrix(brightness=70)
live_scores(m)

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

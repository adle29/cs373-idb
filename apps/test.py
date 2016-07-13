from unittest import main, TestCase
import os
import sys
import subprocess
import io
from flask import Flask, request, url_for
from flask import render_template, send_file
from flask_sqlalchemy import SQLAlchemy
import requests
import ast
import json
from models import *


class DBTestCases(TestCase):

    # Tests that every player is readable

    def test_players_readable_1(self):
        test_player = db.session.query(Player).get(1)

        self.assertEqual(test_player.player_id, 16)
        self.assertEqual(test_player.name, "Bastian Schweinsteiger")
        self.assertEqual(test_player.nation, "Germany")
        self.assertEqual(test_player.birth, "1984-08-01")
        self.assertEqual(test_player.pos, "Central Midfield")
        self.assertEqual(test_player.jersey_num, 31)

    def test_players_readable_2(self):
        test_player = db.session.query(Player).get(2)

        self.assertEqual(test_player.player_id, 418)
        self.assertEqual(test_player.name, "Luke Shaw")
        self.assertEqual(test_player.nation, "England")
        self.assertEqual(test_player.birth, "1995-07-12")
        self.assertEqual(test_player.pos, "Left-Back")
        self.assertEqual(test_player.jersey_num, 23)

    def test_players_readable_3(self):
        test_player = db.session.query(Player).get(3)

        self.assertEqual(test_player.player_id, 409)
        self.assertEqual(test_player.name, "David de Gea")
        self.assertEqual(test_player.nation, "Spain")
        self.assertEqual(test_player.birth, "1990-11-07")
        self.assertEqual(test_player.pos, "Keeper")
        self.assertEqual(test_player.jersey_num, 1)

    # Tests that every team is readable

    def test_teams_readable_1(self):
        test_team = db.session.query(Team).get(1)

        self.assertEqual(test_team.team_id, 66)
        self.assertEqual(test_team.team_name, "Manchester United FC")
        self.assertEqual(test_team.nickname, "ManU")
        self.assertEqual(test_team.market_val, "377,250,000 €")
        self.assertEqual(test_team.logo_url, "http://upload.wikimedia.org/wikipedia/de/d/da/Manchester_United_FC.svg")

    def test_teams_readable_2(self):
        test_team = db.session.query(Team).get(2)

        self.assertEqual(test_team.team_id, 75)
        self.assertEqual(test_team.team_name, "Wigan Athletic FC")
        self.assertEqual(test_team.nickname, "Wigan")
        self.assertEqual(test_team.market_val, None)
        self.assertEqual(test_team.logo_url, "https://upload.wikimedia.org/wikipedia/en/4/43/Wigan_Athletic.svg")

    def test_teams_readable_3(self):
        test_team = db.session.query(Team).get(3)

        self.assertEqual(test_team.team_id, 101)
        self.assertEqual(test_team.team_name, "AC Siena")
        self.assertEqual(test_team.nickname, "Siena")
        self.assertEqual(test_team.market_val, None)
        self.assertEqual(test_team.logo_url, "http://upload.wikimedia.org/wikipedia/de/4/44/AC_Siena.svg")
 

    # Tests that every game is readable

    def test_games_readable_1(self):
        test_game = db.session.query(Game).get(1)

        self.assertEqual(test_game.game_id, 145800)
        self.assertEqual(test_game.date, "2016-02-05T17:30:00Z")
        self.assertEqual(test_game.homeTeam, "VfL Bochum") #id = 36
        self.assertEqual(test_game.awayTeam, "SC Freiburg") #id = 17
        self.assertEqual(test_game.homeTeamScore, 2)
        self.assertEqual(test_game.awayTeamScore, 0)
        self.assertEqual(test_game.matchDay, 20)

    def test_games_readable_2(self):
        test_game = db.session.query(Game).get(2)

        self.assertEqual(test_game.game_id, 145805)
        self.assertEqual(test_game.date, "2016-02-07T12:30:00Z")
        self.assertEqual(test_game.homeTeam, "Red Bull Leipzig") #id = 721
        self.assertEqual(test_game.awayTeam, "Eintracht Braunschweig") #id = 33
        self.assertEqual(test_game.homeTeamScore, 2)
        self.assertEqual(test_game.awayTeamScore, 0)
        self.assertEqual(test_game.matchDay, 20)

    def test_games_readable_3(self):
        test_game = db.session.query(Game).get(3)

        self.assertEqual(test_game.game_id, 145840)
        self.assertEqual(test_game.date, "2015-11-28T12:00:00Z")
        self.assertEqual(test_game.homeTeam, "SC Paderborn 07") #id = 29
        self.assertEqual(test_game.awayTeam, "TSV 1860 München") #id = 26
        self.assertEqual(test_game.homeTeamScore, 4)
        self.assertEqual(test_game.awayTeamScore, 4)
        self.assertEqual(test_game.matchDay, 16)

    # Tests that every season is readable

    def test_season_readable_1(self):
        test_season = db.session.query(Season).get(1)

        self.assertEqual(test_season.season_id, 394)
        self.assertEqual(test_season.season_name, "1. Bundesliga 2015/16")
        self.assertEqual(test_season.league, "BL1")
        self.assertEqual(test_season.year, 2015)
        self.assertEqual(test_season.num_teams, 18)
        self.assertEqual(test_season.num_games, 306)
        self.assertEqual(test_season.num_match_days, 34)
        self.assertEqual(test_season.cur_match_day, 34)

    def test_season_readable_2(self):
        test_season = db.session.query(Season).get(2)

        self.assertEqual(test_season.season_id, 399) #399
        self.assertEqual(test_season.season_name, "Primera Division 2015/16")
        self.assertEqual(test_season.league, "PD")
        self.assertEqual(test_season.year, 2015)
        self.assertEqual(test_season.num_teams, 20)
        self.assertEqual(test_season.num_games, 380)
        self.assertEqual(test_season.num_match_days, 38)
        self.assertEqual(test_season.cur_match_day, 38)

    def test_season_readable_3(self):
        test_season = db.session.query(Season).get(3)

        self.assertEqual(test_season.season_id, 404)
        self.assertEqual(test_season.season_name, "Eredivisie 2015/16")
        self.assertEqual(test_season.league, "DED")
        self.assertEqual(test_season.year, 2015)
        self.assertEqual(test_season.num_teams, 34)
        self.assertEqual(test_season.num_games, 34)
        self.assertEqual(test_season.num_match_days, 18)
        self.assertEqual(test_season.cur_match_day, 306)

    # Tests that every standing is readable

    def test_standings_readable_1(self):
        test_standing = db.session.query(Standing).get(1)

        self.assertEqual(test_standing.standing_id, 1)
        self.assertEqual(test_standing.matchday, 38)
        self.assertEqual(test_standing.rank, 1)
        self.assertEqual(test_standing.group, None)
        self.assertEqual(test_standing.matchesPlayed, 38)
        self.assertEqual(test_standing.points, 81)
        self.assertEqual(test_standing.goalsFor, 68)
        self.assertEqual(test_standing.goalsAgainst, 36)
        self.assertEqual(test_standing.season_id, 398)
        self.assertEqual(test_standing.team_id, 338)

    def test_standings_readable_2(self):
        test_standing = db.session.query(Standing).get(2)

        self.assertEqual(test_standing.standing_id, 2)
        self.assertEqual(test_standing.matchday, 6)
        self.assertEqual(test_standing.rank, 1)
        self.assertEqual(test_standing.group, "A")
        self.assertEqual(test_standing.matchesPlayed, 6)
        self.assertEqual(test_standing.points, 16)
        self.assertEqual(test_standing.goalsFor, 19)
        self.assertEqual(test_standing.goalsAgainst, 3)
        self.assertEqual(test_standing.season_id, 405)
        self.assertEqual(test_standing.team_id, 86)


    def test_standings_readable_3(self):
        test_standing = db.session.query(Standing).get(3)

        self.assertEqual(test_standing.standing_id, 3)
        self.assertEqual(test_standing.matchday, 6)
        self.assertEqual(test_standing.rank, 2)
        self.assertEqual(test_standing.group, "B")
        self.assertEqual(test_standing.matchesPlayed, 6)
        self.assertEqual(test_standing.points, 10)
        self.assertEqual(test_standing.goalsFor, 8)
        self.assertEqual(test_standing.goalsAgainst, 7)
        self.assertEqual(test_standing.season_id, 405)
        self.assertEqual(test_standing.team_id, 674)


if __name__ == "__main__":
    try:
        app = Flask(__name__)
        app.config.from_object(os.environ['APP_SETTINGS'])
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        Base = db.Model
        main()


        
    except:
        pass

#db.db.add(self.standings)
#db.db.commit()
#rmStand = Standings.query.get(2)

"""
pylint3 results for test.py
---------------------------------------------------
Report
======
162 statements analysed.

Statistics by type
------------------

+---------+-------+-----------+-----------+------------+---------+
|type     |number |old number |difference |%documented |%badname |
+=========+=======+===========+===========+============+=========+
|module   |1      |NC         |NC         |0.00        |0.00     |
+---------+-------+-----------+-----------+------------+---------+
|class    |1      |NC         |NC         |0.00        |0.00     |
+---------+-------+-----------+-----------+------------+---------+
|method   |15     |NC         |NC         |0.00        |0.00     |
+---------+-------+-----------+-----------+------------+---------+
|function |0      |NC         |NC         |0           |0        |
+---------+-------+-----------+-----------+------------+---------+

Raw metrics
-----------

+----------+-------+------+---------+-----------+
|type      |number |%     |previous |difference |
+==========+=======+======+=========+===========+
|code      |170    |74.56 |NC       |NC         |
+----------+-------+------+---------+-----------+
|docstring |0      |0.00  |NC       |NC         |
+----------+-------+------+---------+-----------+
|comment   |5      |2.19  |NC       |NC         |
+----------+-------+------+---------+-----------+
|empty     |53     |23.25 |NC       |NC         |
+----------+-------+------+---------+-----------+

Duplication
-----------

+-------------------------+------+---------+-----------+
|                         |now   |previous |difference |
+=========================+======+=========+===========+
|nb duplicated lines      |0     |NC       |NC         |
+-------------------------+------+---------+-----------+
|percent duplicated lines |0.000 |NC       |NC         |
+-------------------------+------+---------+-----------+


Messages by category
--------------------

+-----------+-------+---------+-----------+
|type       |number |previous |difference |
+===========+=======+=========+===========+
|convention |29     |NC       |NC         |
+-----------+-------+---------+-----------+
|refactor   |0      |NC       |NC         |
+-----------+-------+---------+-----------+
|warning    |7      |NC       |NC         |
+-----------+-------+---------+-----------+
|error      |78     |NC       |NC         |
+-----------+-------+---------+-----------+

Messages
--------

+---------------------------+------------+
|message id                 |occurrences |
+===========================+============+
|undefined-variable         |53          |
+---------------------------+------------+
|missing-docstring          |17          |
+---------------------------+------------+
|no-member                  |15          |
+---------------------------+------------+
|invalid-name               |11          |
+---------------------------+------------+
|not-callable               |6           |
+---------------------------+------------+
|unused-import              |5           |
+---------------------------+------------+
|import-error               |4           |
+---------------------------+------------+
|unused-variable            |1           |
+---------------------------+------------+
|trailing-whitespace        |1           |
+---------------------------+------------+
|pointless-string-statement |1           |
+---------------------------+------------+

Global evaluation
-----------------
Your code has been rated at -16.30/10

---------------------------------------------------
"""

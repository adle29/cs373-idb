from unittest import main, TestCase
import unittest
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
import config


class DBTestCases(TestCase):

        # Tests that every player is readable

    def test_players_readable_1(self):
        test_player = db.session.query(Player).get(3238)

        self.assertEqual(test_player.player_id, 3238)
        self.assertEqual(test_player.name, "Fabian Johnson")
        self.assertEqual(test_player.nation, "United States")
        self.assertEqual(test_player.birth, "1987-12-11")
        self.assertEqual(test_player.position, "Left Wing")
        self.assertEqual(test_player.jersey_num, 19)

    def test_players_readable_2(self):
        test_player = db.session.query(Player).get(2605)

        self.assertEqual(test_player.player_id, 2605)
        self.assertEqual(test_player.name, "Kenan Karaman")
        self.assertEqual(test_player.nation, "Turkey")
        self.assertEqual(test_player.birth, "1994-03-05")
        self.assertEqual(test_player.position, "Left Wing")
        self.assertEqual(test_player.jersey_num, 26)

    def test_players_readable_3(self):
        test_player = db.session.query(Player).get(3300)

        self.assertEqual(test_player.player_id, 3300)
        self.assertEqual(test_player.name, "Claudio Pizarro")
        self.assertEqual(test_player.nation, "Peru")
        self.assertEqual(test_player.birth, "1978-10-03")
        self.assertEqual(test_player.position, "Centre Forward")
        self.assertEqual(test_player.jersey_num, 14)

    # Tests that every team is readable

    def test_teams_readable_1(self):
        test_team = db.session.query(Team).get(184)

        self.assertEqual(test_team.team_id, 184)
        self.assertEqual(test_team.team_name, "Werder Bremen")
        self.assertEqual(test_team.nickname, "Bremen")
        self.assertEqual(test_team.market_val, "55,550,000 €")
        self.assertEqual(test_team.logo_url, "http://upload.wikimedia.org/wikipedia/commons/b/be/SV-Werder-Bremen-Logo.svg")

    def test_teams_readable_2(self):
        test_team = db.session.query(Team).get(190)

        self.assertEqual(test_team.team_id, 190)
        self.assertEqual(test_team.team_name, "Hertha BSC")
        self.assertEqual(test_team.nickname, "Hertha")
        self.assertEqual(test_team.market_val, "62,050,000 €")
        self.assertEqual(test_team.logo_url, "http://upload.wikimedia.org/wikipedia/de/8/81/Hertha_BSC_Logo_2012.svg")

    def test_teams_readable_3(self):
        test_team = db.session.query(Team).get(179)

        self.assertEqual(test_team.team_id, 179)
        self.assertEqual(test_team.team_name, "Bayer Leverkusen")
        self.assertEqual(test_team.nickname, "Leverkusen")
        self.assertEqual(test_team.market_val, "202,500,000 €")
        self.assertEqual(test_team.logo_url, "http://upload.wikimedia.org/wikipedia/de/9/95/Bayer_04_Leverkusen_Logo.svg")
 

    # Tests that every game is readable

    def test_games_readable_1(self):
        test_game = db.session.query(Game).get(13233)

        self.assertEqual(test_game.game_id, 13233)
        self.assertEqual(test_game.date, "2014-06-11T22:00:00Z")
        self.assertEqual(test_game.home_team_id, 348) 
        self.assertEqual(test_game.away_team_id, 349) 
        self.assertEqual(test_game.home_team_score, 3)
        self.assertEqual(test_game.away_team_score, 1)
        self.assertEqual(test_game.match_day, 1)
        self.assertEqual(test_game.season_id, 38)

    def test_games_readable_2(self):
        test_game = db.session.query(Game).get(2330)

        self.assertEqual(test_game.game_id, 2330)
        self.assertEqual(test_game.date, "2014-09-13T13:00:00Z")
        self.assertEqual(test_game.home_team_id, 64) 
        self.assertEqual(test_game.away_team_id, 79) 
        self.assertEqual(test_game.home_team_score, 1)
        self.assertEqual(test_game.away_team_score, 1)
        self.assertEqual(test_game.match_day, 3)
        self.assertEqual(test_game.season_id, 15)

    def test_games_readable_3(self):
        test_game = db.session.query(Game).get(4098)

        self.assertEqual(test_game.game_id, 4098)
        self.assertEqual(test_game.date, "2014-10-04T22:00:00Z")
        self.assertEqual(test_game.home_team_id, 98) 
        self.assertEqual(test_game.away_team_id, 109) 
        self.assertEqual(test_game.home_team_score, 4)
        self.assertEqual(test_game.away_team_score, 0)
        self.assertEqual(test_game.match_day, 7)
        self.assertEqual(test_game.season_id, 16)

    # Tests that every season is readable

    def test_season_readable_1(self):
        test_season = db.session.query(Season).get(18)

        self.assertEqual(test_season.season_id, 18)
        self.assertEqual(test_season.season_name, "1. Bundesliga 2015/16")
        self.assertEqual(test_season.league, "BL1")
        self.assertEqual(test_season.year, 2015)
        self.assertEqual(test_season.num_teams, 18)
        self.assertEqual(test_season.num_games, 306)
        self.assertEqual(test_season.num_match_days, 34)
        self.assertEqual(test_season.cur_match_day, 34)

    def test_season_readable_2(self):
        test_season = db.session.query(Season).get(30)

        self.assertEqual(test_season.season_id, 30) 
        self.assertEqual(test_season.season_name, "Primera Division 2015/16")
        self.assertEqual(test_season.league, "PD")
        self.assertEqual(test_season.year, 2015)
        self.assertEqual(test_season.num_teams, 20)
        self.assertEqual(test_season.num_games, 380)
        self.assertEqual(test_season.num_match_days, 38)
        self.assertEqual(test_season.cur_match_day, 38)

    def test_season_readable_3(self):
        test_season = db.session.query(Season).get(27)

        self.assertEqual(test_season.season_id, 27)
        self.assertEqual(test_season.season_name, "Eredivisie 2015/16")
        self.assertEqual(test_season.league, "DED")
        self.assertEqual(test_season.year, 2015)
        self.assertEqual(test_season.num_teams, 18)
        self.assertEqual(test_season.num_games, 306)
        self.assertEqual(test_season.num_match_days, 34)
        self.assertEqual(test_season.cur_match_day, 34)

    # Tests that every standing is readable

    def test_standings_readable_1(self):
        test_standing = db.session.query(Standing).get(1)

        self.assertEqual(test_standing.standing_id, 1)
        self.assertEqual(test_standing.rank, 1)
        self.assertEqual(test_standing.group, "A")
        self.assertEqual(test_standing.match_day, 1)
        self.assertEqual(test_standing.matches_played, 0)
        self.assertEqual(test_standing.points, 0)
        self.assertEqual(test_standing.goals_for, 0)
        self.assertEqual(test_standing.goals_against, 0)
        self.assertEqual(test_standing.team_id, 28)
        self.assertEqual(test_standing.season_id, 12)

    def test_standings_readable_2(self):
        test_standing = db.session.query(Standing).get(538)

        self.assertEqual(test_standing.standing_id, 538)
        self.assertEqual(test_standing.rank, 14)
        self.assertEqual(test_standing.group, "A")
        self.assertEqual(test_standing.match_day, 38)
        self.assertEqual(test_standing.matches_played, 38)
        self.assertEqual(test_standing.points, 41)
        self.assertEqual(test_standing.goals_for, 46)
        self.assertEqual(test_standing.goals_against, 55)
        self.assertEqual(test_standing.team_id, 286)
        self.assertEqual(test_standing.season_id, 3)


    def test_standings_readable_3(self):
        test_standing = db.session.query(Standing).get(530)

        self.assertEqual(test_standing.standing_id, 530)
        self.assertEqual(test_standing.rank, 6)
        self.assertEqual(test_standing.group, "A")
        self.assertEqual(test_standing.match_day, 38)
        self.assertEqual(test_standing.matches_played, 38)
        self.assertEqual(test_standing.points, 62)
        self.assertEqual(test_standing.goals_for, 52)
        self.assertEqual(test_standing.goals_against, 48)
        self.assertEqual(test_standing.team_id, 2)
        self.assertEqual(test_standing.season_id, 3)


if __name__ == "__main__":
    try:
        app = Flask(__name__)
        app.config.from_object(app.config.from_object(config.DevelopmentConfig))
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        Base = db.Model
        log_file = 'test.log'
        f = open(log_file, "w")
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
        f.close()
    except Exception as e:
        print(e)
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

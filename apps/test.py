import os
import sqlalchemy
import unittest
import flask
import models
import datetime
import app

class DBTestCases(unittest.TestCase):

# Tests that every player is readable
def test_players_readable_1(self):
    db.session.add(self.player)
    db.session.commit()

    crisRonaldo = Players.query.get(1)

    self.assertEqual(crisRonaldo.player_id, "7")
    self.assertEqual(crisRonaldo.team_id, "Real Madrid")
    self.assertEqual(crisRonaldo.name, "Cristiano Ronaldo")
    self.assertEqual(crisRonaldo.pos, "Left Wing")
    self.assertEqual(crisRonaldo.nationality, "Portugal")

def test_players_readable_2(self):
    db.session.add(self.player)
    db.session.commit()

    gBale = Players.query.get(2)

    self.assertEqual(gBale.player_id, "11")
    self.assertEqual(gBale.team_id, "Real Madrid")
    self.assertEqual(gBale.name, "Gareth Bale")
    self.assertEqual(gBale.pos, "Right Wing")
    self.assertEqual(gBale.nationality, "Wales"

def test_players_readable_3(self):
    db.session.add(self.player)
    db.session.commit()

    davidDeGea = Players.query.get(3)

    self.assertEqual(davidDeGea.player_id, "1")
    self.assertEqual(davidDeGea.team_id, "Manchester United")
    self.assertEqual(davidDeGea.name, "David de Gea")
    self.assertEqual(davidDeGea.pos, "Keeper")
    self.assertEqual(davidDeGea.nationality, "Spain")

# Tests that every team is readable
def test_teams_readable_1(self):
    db.session.add(self.team)
    db.session.commit()

    psg = Teams.query.get(1)

    self.assertEqual(psg.team_id, "Paris Saint Germain")

def test_teams_readable_2(self):
    db.session.add(self.team)
    db.session.commit()

    manUnited = Teams.query.get(2)

    self.assertEqual(manUnited.team_id, "Manchester United")

def test_teams_readable_3(self):
    db.session.add(self.team)
    db.session.commit()

    bMunich = Teams.query.get(3)

    self.assertEqual(bMunich.team_id, "Bayern Munich")

# Tests that every game is readable
def test_games_readable_1(self):
    db.session.add(self.player)
    db.session.commit()

    euroSemi1 = Games.query.get(1)

    self.assertEqual(euroSemi1.date, datetime(2016, 7, 6, 14, 0))
    self.assertEqual(euroSemi1.result, "0 - 0"
    self.assertEqual(euroSemi1.homeTeam, "Portugal")
    self.assertEqual(euroSemi1.awayTeam, "Wales")

def test_games_readable_2(self):
    db.session.add(self.player)
    db.session.commit()

    euroSemi2 = Games.query.get(2)

    self.assertEqual(euroSemi2.date, datetime(2016, 7, 7, 14, 0))
    self.assertEqual(euroSemi2.result, "0 - 0"
    self.assertEqual(euroSemi2.homeTeam, "France")
    self.assertEqual(euroSemi2.awayTeam, "Italy")

def test_games_readable_3(self):
    db.session.add(self.player)
    db.session.commit()

    psgOpener = Games.query.get(3)

    self.assertEqual(psgOpener.date, datetime(2016, 8, 12, 0, 0))
    self.assertEqual(euroSemi2.result, "0 - 0"
    self.assertEqual(euroSemi2.homeTeam, "Paris Saint-Germain")
    self.assertEqual(euroSemi2.awayTeam, "SC Bastia")
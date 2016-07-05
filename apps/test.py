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

    self.assertEqual(crisRonaldo.id, "1")
    self.assertEqual(crisRonaldo.name, "Cristiano Ronaldo")
    self.assertEqual(crisRonaldo.nation, "Portugal")
    self.assertEqual(crisRonaldo.birth, datetime(1985, 2, 5, 0, 0))
    self.assertEqual(crisRonaldo.pos, "Left Wing")
    self.assertEqual(crisRonaldo.JerneyNum, "7")

def test_players_readable_2(self):
    db.session.add(self.player)
    db.session.commit()

    gBale = Players.query.get(2)

    self.assertEqual(gBale.id, "2")
    self.assertEqual(gBale.name, "Gareth Bale")
    self.assertEqual(gBale.nation, "Wales")
    self.assertEqual(gBale.birth, datetime(1989, 7, 16, 0, 0))
    self.assertEqual(gBale.pos, "Right Wing")
    self.assertEqual(gBale.JerneyNum, "11")

def test_players_readable_3(self):
    db.session.add(self.player)
    db.session.commit()

    davidDeGea = Players.query.get(3)

    self.assertEqual(davidDeGea.id, "3")
    self.assertEqual(davidDeGea.name, "David de Gea")
    self.assertEqual(davidDeGea.nation, "Spain")
    self.assertEqual(davidDeGea.birth, datetime(1990, 11, 7, 0, 0))
    self.assertEqual(davidDeGea.pos, "Keeper")
    self.assertEqual(davidDeGea.JerneyNum, "1")

# Tests that every team is readable
def test_teams_readable_1(self):
    db.session.add(self.team)
    db.session.commit()

    psg = Teams.query.get(1)

    self.assertEqual(psg.id, "1")
    self.assertEqual(psg.teamName, "Paris Saint-Germain")
    self.assertEqual(psg.nickname, "PSG")
    self.assertEqual(psg.marketVal, "$64,000,000")

def test_teams_readable_2(self):
    db.session.add(self.team)
    db.session.commit()

    barcelona = Teams.query.get(2)

    self.assertEqual(barcelona.id, "2")
    self.assertEqual(barcelona.teamName, "Barcelona")
    self.assertEqual(barcelona.nickname, "Barca")
    self.assertEqual(barcelona.marketVal, "$69,000,000")

def test_teams_readable_3(self):
    db.session.add(self.team)
    db.session.commit()

    bMunich = Teams.query.get(3)

    self.assertEqual(bMunich.id, "3")
    self.assertEqual(bMunich.teamName, "Bayern Munich")
    self.assertEqual(bMunich.nickname, "Bayern")
    self.assertEqual(bMunich.marketVal, "$57,000,000")

# Tests that every game is readable
def test_games_readable_1(self):
    db.session.add(self.game)
    db.session.commit()

    euroSemi1 = Games.query.get(1)

    self.assertEqual(euroSemi1.date, datetime(2016, 7, 6, 14, 0))
    self.assertEqual(euroSemi1.homeTeam, "Portugal")
    self.assertEqual(euroSemi1.awayTeam, "Wales")
    self.assertEqual(euroSemi1.homeTeamScore, "0")
    self.assertEqual(euroSemi1.awayTeamScore, "0")
    self.assertEqual(euroSemi1.matchDay, "1")

def test_games_readable_2(self):
    db.session.add(self.game)
    db.session.commit()

    euroSemi2 = Games.query.get(2)

    self.assertEqual(euroSemi2.date, datetime(2016, 7, 7, 14, 0))
    self.assertEqual(euroSemi2.homeTeam, "France")
    self.assertEqual(euroSemi2.awayTeam, "Italy")
    self.assertEqual(euroSemi2.homeTeamScore, "0")
    self.assertEqual(euroSemi2.awayTeamScore, "0")
    self.assertEqual(euroSemi2.matchDay, "2")

def test_games_readable_3(self):
    db.session.add(self.game)
    db.session.commit()

    psgOpener = Games.query.get(3)

    self.assertEqual(psgOpener.date, datetime(2016, 8, 12, 0, 0))
    self.assertEqual(psgOpener.result, "0 - 0"
    self.assertEqual(psgOpener.homeTeam, "Paris Saint-Germain")
    self.assertEqual(psgOpener.awayTeam, "SC Bastia")
    self.assertEqual(psgOpener.homeTeamScore, "0")
    self.assertEqual(psgOpener.awayTeamScore, "0")
    self.assertEqual(psgOpener.matchDay, "3")
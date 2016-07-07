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

        self.assertEqual(crisRonaldo.id, 1)
        self.assertEqual(crisRonaldo.name, "Cristiano Ronaldo")
        self.assertEqual(crisRonaldo.nation, "Portugal")
        self.assertEqual(crisRonaldo.birth, datetime(1985, 2, 5, 0, 0))
        self.assertEqual(crisRonaldo.pos, "Left Wing")
        self.assertEqual(crisRonaldo.JerneyNum, 7)

    def test_players_readable_2(self):
        db.session.add(self.player)
        db.session.commit()

        gBale = Players.query.get(2)

        self.assertEqual(gBale.id, 2)
        self.assertEqual(gBale.name, "Gareth Bale")
        self.assertEqual(gBale.nation, "Wales")
        self.assertEqual(gBale.birth, datetime(1989, 7, 16, 0, 0))
        self.assertEqual(gBale.pos, "Right Wing")
        self.assertEqual(gBale.JerneyNum, 11)

    def test_players_readable_3(self):
        db.session.add(self.player)
        db.session.commit()

        davidDeGea = Players.query.get(3)

        self.assertEqual(davidDeGea.id, 3)
        self.assertEqual(davidDeGea.name, "David de Gea")
        self.assertEqual(davidDeGea.nation, "Spain")
        self.assertEqual(davidDeGea.birth, datetime(1990, 11, 7, 0, 0))
        self.assertEqual(davidDeGea.pos, "Keeper")
        self.assertEqual(davidDeGea.JerneyNum, 1)

    # Tests that every team is readable

    def test_teams_readable_1(self):
        db.session.add(self.team)
        db.session.commit()

        psg = Teams.query.get(1)

        self.assertEqual(psg.id, 1)
        self.assertEqual(psg.teamName, "Paris Saint-Germain")
        self.assertEqual(psg.nickname, "PSG")
        self.assertEqual(psg.marketVal, "$64,000,000")

    def test_teams_readable_2(self):
        db.session.add(self.team)
        db.session.commit()

        barcelona = Teams.query.get(2)

        self.assertEqual(barcelona.id, 2)
        self.assertEqual(barcelona.teamName, "Barcelona")
        self.assertEqual(barcelona.nickname, "Barca")
        self.assertEqual(barcelona.marketVal, "$69,000,000")

    def test_teams_readable_3(self):
        db.session.add(self.team)
        db.session.commit()

        bMunich = Teams.query.get(3)

        self.assertEqual(bMunich.id, 3)
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
        self.assertEqual(euroSemi1.homeTeamScore, 0)
        self.assertEqual(euroSemi1.awayTeamScore, 0)
        self.assertEqual(euroSemi1.matchDay, 1)

    def test_games_readable_2(self):
        db.session.add(self.game)
        db.session.commit()

        euroSemi2 = Games.query.get(2)

        self.assertEqual(euroSemi2.date, datetime(2016, 7, 7, 14, 0))
        self.assertEqual(euroSemi2.homeTeam, "France")
        self.assertEqual(euroSemi2.awayTeam, "Italy")
        self.assertEqual(euroSemi2.homeTeamScore, 0)
        self.assertEqual(euroSemi2.awayTeamScore, 0)
        self.assertEqual(euroSemi2.matchDay, 2)

    def test_games_readable_3(self):
        db.session.add(self.game)
        db.session.commit()

        psgOpener = Games.query.get(3)

        self.assertEqual(psgOpener.date, datetime(2016, 8, 12, 0, 0))
        self.assertEqual(psgOpener.homeTeam, "Paris Saint-Germain")
        self.assertEqual(psgOpener.awayTeam, "SC Bastia")
        self.assertEqual(psgOpener.homeTeamScore, 0)
        self.assertEqual(psgOpener.awayTeamScore, 0)
        self.assertEqual(psgOpener.matchDay, 3)

    # Tests that every season is readable

    def test_season_readable_1(self):
        db.session.add(self.season)
        db.session.commit()

        euro16 = Seasons.query.get(1)

        self.assertEqual(euro16.id, 1)
        self.assertEqual(euro16.seasonName, "European Championships France 2016")
        self.assertEqual(euro16.league, "EC")
        self.assertEqual(euro16.year, 2016)
        self.assertEqual(euro16.numTeams, 24)
        self.assertEqual(euro16.numGames, 48)
        self.assertEqual(euro16.numMatchDays, 30)
        self.assertEqual(euro16.curMatchDay, 46)

    def test_season_readable_2(self):
        db.session.add(self.season)
        db.session.commit()

        preLeague = Seasons.query.get(2)

        self.assertEqual(preleague.id, 2)
        self.assertEqual(preleague.seasonName, "Premiere League 2016/17")
        self.assertEqual(preleague.league, "PL")
        self.assertEqual(preleague.year, 2016)
        self.assertEqual(preleague.numTeams, 20)
        self.assertEqual(preleague.numGames, 760)
        self.assertEqual(preleague.numMatchDays, 38)
        self.assertEqual(preleague.curMatchDay, 1)

    def test_season_readable_3(self):
        db.session.add(self.season)
        db.session.commit()

        ligue1 = Seasons.query.get(3)

        self.assertEqual(ligue1.id, 3)
        self.assertEqual(ligue1.seasonName, "Ligue 1 2016/17")
        self.assertEqual(ligue1.league, "FL1")
        self.assertEqual(ligue1.year, 2016)
        self.assertEqual(ligue1.numTeams, 20)
        self.assertEqual(ligue1.numGames, 760)
        self.assertEqual(ligue1.numMatchDays, 38)
        self.assertEqual(ligue1.curMatchDay, 1

    # Tests that every standing is readable
    
    def test_standings_readable_1(self):
        db.session.add(self.standings)
        db.session.commit()

        psgStand = Standings.query.get(0)

        self.assertEqual(psgStand.id, 0)
        self.assertEqual(psgStand.matchday, 1)
        self.assertEqual(psgStand.rank, 1)
        self.assertEqual(psgStand.matchesPlayed, 0)
        self.assertEqual(psgStand.points, 0)
        self.assertEqual(psgStand.goalsFor, 0)
        self.assertEqual(psgStand.goalsAgainst, 0)

    def test_standings_readable_2(self):
        db.session.add(self.standings)
        db.session.commit()

        manuStand = Standings.query.get(1)

        self.assertEqual(manuStand.id, 1)
        self.assertEqual(manuStand.matchday, 1)
        self.assertEqual(manuStand.rank, 1)
        self.assertEqual(manuStand.matchesPlayed, 0)
        self.assertEqual(manuStand.points, 0)
        self.assertEqual(manuStand.goalsFor, 0)
        self.assertEqual(manuStand.goalsAgainst, 0)

    def test_standings_readable_3(self):
        db.session.add(self.standings)
        db.session.commit()

        rmStand = Standings.query.get(2)

        self.assertEqual(rmStand.id, 2)
        self.assertEqual(rmStand.matchday, 1)
        self.assertEqual(rmStand.rank, 1)
        self.assertEqual(rmStand.matchesPlayed, 0)
        self.assertEqual(rmStand.points, 0)
        self.assertEqual(rmStand.goalsFor, 0)
        self.assertEqual(rmStand.goalsAgainst, 0)

"""
pylintrc results for test.py
---------------------------------------------------
No config file found, using default configuration
************* Module apps.test
E: 12, 0: expected an indented block (syntax-error)
---------------------------------------------------
"""
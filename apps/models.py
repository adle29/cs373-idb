#!/usr/bin/env python3

# ---------------------------
# cs373-idb/app/models.py
#
# JASON DIMITRIOU
# CLARK CLAYTONst
# KALEB ALANIS
# HASSAN SHEIKH
# Abraham Adberstein
# ---------------------------

import os
import sys
from collections import OrderedDict
from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from flask_sqlalchemy import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from __init__ import db

Base = db.Model #declarative_base()
#Base2 = declarative_base()

# for yUML model
# http://yuml.me/edit/a541cdb0
# http://yuml.me/ba69937b

# many to many relationships
# seasons to teams  #Base.metadata,
season_team = db.Table('season_team',
    db.Column('season_id', db.Integer, db.ForeignKey('season.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)
# games to teams
team_game = db.Table('team_game',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)


# --------------
# Season
# --------------
class Season(Base):
    """
    Season has everything related to a season in soccer with the name, number of games,
    number of teams, year and has relationships to teams, standings, and games
    """
    __tablename__ = 'season'
    __table_args__ = {'extend_existing': True}
    # Here we define columns for the table Season
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(Integer, primary_key=True)
    seasonName = db.Column(String(250), nullable=False)
    league = db.Column(String(250))
    year = db.Column(Integer)
    numTeams = db.Column(Integer)
    numGames = db.Column(Integer)
    numMatchdays = db.Column(Integer)
    curMatchday = db.Column(Integer)
    # relationships
    Sgame = db.relationship("Game", back_populates="Gseason")  # 1 to many
    Sstanding = db.relationship("Standing", back_populates="Rseason")  # 1 to many
    Steam = db.relationship(
        "Team", secondary=season_team, back_populates="Tseason")  # many to many

    def __init__(self, id, seasonName, league, year, numTeams, numGames, numMatchdays, curMatchday):
        """
        itializes everything in the Season class
        :param self:
        :param id: Integer
        :param league: String
        :param numTeams: Integer
        :param numGames: Integer
        :param numMatchdays: Integer
        :param curMatchday: Integer
        """
        self.id = id
        self.seasonName = seasonName
        self.league = league
        self.year = year
        self.numTeams = numTeams
        self.numGames = numGames
        self.numMatchdays = numMatchdays
        self.curMatchday = curMatchday

    def __repr__(self): #display(self):
        """
        :param self:
        :return: displayDict
        :rtype: OrderedDict
        """
        displayDict = OrderedDict()
        displayDict['id'] = self.id
        displayDict['seasonName'] = self.seasonName.title()
        displayDict['league'] = self.league
        displayDict['year'] = self.year
        displayDict['numTeams'] = self.numTeams
        displayDict['numGames'] = self.numGames
        displayDict['numMatchdays'] = self.numMatchdays
        displayDict['curMatchday'] = self.curMatchday
        displayDict['standings'] = [standing_id for standing in self.Sstanding]

        return displayDict


# # --------------
# # Standing
# # --------------
#
# class Standing(Base):
#
#     """
#     Standing has everything related to a standing in soccer with the rank, matchesPlayed,
#     points, goalsFor, and goalsAgainst
#     """
#     __tablename__ = 'standing'
#     # Here we define columns for the table Standing
#     # Notice that each column is also a normal Python instance attribute.
#     id = db.Column(Integer, primary_key=True)
#     matchday = db.Column(Integer, nullable=False)
#     group = db.Column(String(250))
#     rank = db.Column(Integer)
#     matchesPlayed = db.Column(Integer)
#     points = db.Column(Integer)
#     goalsFor = db.Column(Integer)
#     goalsAgainst = db.Column(Integer)
#     # relationships
#     season_id = db.Column(Integer, ForeignKey('season.id'))
#     Rseason = db.relationship("Season")  # many to 1
#     team_id = db.Column(Integer, ForeignKey('team.id'))
#     Rteam = db.relationship("Team")  # many to 1
#
#     def __init__(self, id, matchday, group, rank, matchesPlayed, points, goalsFor, goalsAgainst):
#         """
#         itializes everything in the Standing class
#         :param self:
#         :param id: Integer
#         :param matchday: Integer
#         :param group: String
#         :param rank: Integer
#         :param matchesPlayed: Integer
#         :param points: Integer
#         :param goalsFor: Integer
#         :param goalsAgainst: Integer
#         """
#         self.id = id
#         self.matchday = matchday
#         self.group = group
#         self.rank = rank
#         self.matchesPlayed = matchesPlayed
#         self.points = points
#         self.goalsFor = goalsFor
#         self.goalsAgainst = goalsAgainst
#
#     def __repr__(self):
#         """
#         :param self:
#         :return: displayDict
#         :rtype: OrderedDict
#         """
#         displayDict = OrderedDict()
#         displayDict['id'] = self.id
#         displayDict['matchday'] = self.matchday
#         displayDict['group'] = self.group
#         displayDict['rank'] = self.rank
#         displayDict['matchesPlayed'] = self.matchesPlayed
#         displayDict['points'] = self.points
#         displayDict['goalsFor'] = goalsFor
#         displayDict['goalsAgainst'] = goalsAgainst
#         displayDict['team'] = team_id
#         return displayDict
#
#
# --------------
# Team
# --------------

class Team(Base):
    """
    Team has everything related to a team in soccer with the name, nickname, logo, and marketVal
    """
    __tablename__ = 'team'
    __table_args__ = {'extend_existing': True}
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(250), nullable=False)
    logoURL = db.Column(db.String(250))
    nickname = db.Column(db.String(250))
    marketVal = db.Column(db.String(250))
    # relationships
    Tseason = db.relationship(
        "Season", secondary=season_team, back_populates="Steam")  # many to many
    Tstanding = db.relationship("Standing", back_populates="Rteam")  # 1 to many
    Tplayer = db.relationship("Player", back_populates="Pteam")  # 1 to many
    Tgame = db.relationship(
        "Game", secondary=team_game, back_populates="Gteam")  # many to many

    def __init__(self, id, teamName, logoURL, nickname, marketVal):
        """
        initializes everything in the Team class
        :param self:
        :param id: Integer
        :param teamName: String
        :param logoURL: String
        :param nickname: String
        :param marketVal: String
        """
        self.id = id
        self.teamName = teamName
        self.logoURL = logoURL
        self.nickname = nickname
        self.marketVal = marketVal

    def __repr__(self):
        """
        :param self:
        :return: displayDict
        :rtype: OrderedDict
        """
        displayDict = OrderedDict()
        displayDict['id'] = self.id
        displayDict['teamName'] = self.teamName.title()
        displayDict['logoURL'] = self.logoURL
        displayDict['nickname'] = self.nickname
        displayDict['marketVal'] = self.marketVal
        displayDict['players'] = [player_id for player in self.Tplayer]
        displayDict['games'] = [game_id for game in self.Tgame]
        return displayDict

# # --------------
# # Game
# # --------------
#
#
# class Game(Base):
#     """
#     Game has everything related to a game in soccer with the date, time, homeTeam, awayTeam, and result
#     """
#     __tablename__ = 'game'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     date = Column(String(250))
#     time = Column(String(250))
#     awayTeam = Column(String(250))
#     homeTeam = Column(String(250))
#     awayTeamScore = Column(Integer)
#     homeTeamScore = Column(Integer)
#     matchDay = Column(Integer)
#     # relationships
#     season_id = Column(Integer, ForeignKey('season.id'))
#     Gseason = relationship("Season", back_populates="Sgame")  # many to 1
#     Gteam = relationship(
#         "Team", secondary=team_game, back_populates="Tgame")  # many to many
#
#     def __init__(self, id, date, time, awayTeam, homeTeam, awayTeamScore, homeTeamScore, matchday):
#         """
#         itializes everything in the Game class
#         :param self:
#         :param id: Integer
#         :param date: String
#         :param time: String
#         :param awayTeam: String
#         :param homeTeam: String
#         :param awayTeamScore: Integer
#         :param hometeamScore Integer
#         """
#         self.id = id
#         self.date = date
#         self.time = time
#         self.awayTeam = awayTeam
#         self.homeTeam = homeTeam
#         self.awayTeamScore = awayTeamScore
#         self.homeTeamScore = homeTeamScore
#         self.matchday = matchday
#
#     def __repr__(self):
#         """
#         :param self:
#         :return: displayDict
#         :rtype: OrderedDict
#         """
#         displayDict = OrderedDict()
#         displayDict['id'] = self.id
#         displayDict['season_name'] = self.season_name.title()
#         displayDict['league'] = self.league
#         displayDict['year'] = self.year
#         displayDict['numTeams'] = self.numTeams
#         displayDict['numGames'] = self.numGames
#         displayDict['matchday'] = self.matchday
#         return displayDict
#
# # --------------
# # Player
# # --------------
#
#
# class Player(Base):
#
#     """
#     Player has everything related to a player in soccer with the name, nation, date of birth, position, and jersey number
#     """
#     __tablename__ = 'player'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     nation = Column(String(250))
#     birth = Column(String(250))
#     pos = Column(String(250))
#     jerseyNum = Column(Integer)
#     # relationships
#     team_id = Column(Integer, ForeignKey('team.id'))
#     Pteam = relationship("Team")  # many to 1
#
#     def __init__(self, id, name, nation, birth, pos, jerseyNum):
#         """
#         itializes everything in the player class
#         :param self:
#         :param id: Integer
#         :param name: String
#         :param nation: String
#         :param birth: String
#         :param pos: String
#         :param jerseyNum: Integer
#         """
#         self.id = id
#         self.name = name
#         self.nation = nation
#         self.birth = birth
#         self.pos = pos
#         self.jerseyNum = jerseyNum
#
#     def __repr__(self):
#         """
#         :param self:
#         :return: displayDict
#         :rtype: OrderedDict
#         """
#         displayDict = OrderedDict()
#         displayDict['id'] = self.id
#         displayDict['name'] = self.name.title()
#         displayDict['nation'] = self.nation
#         displayDict['birth'] = self.birth
#         displayDict['pos'] = self.pos
#         displayDict['jerseyNum'] = self.jerseyNum
#         return displayDict



# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# engine = create_engine('sqlite:///sqlalchemy_example.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)

#!/usr/bin/env python3


import os
import sys
from collections import OrderedDict
from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

#for yUML model
#http://yuml.me/edit/a541cdb0
#http://yuml.me/ba69937b

#many to many relationships
#seasons to teams
season_team = Table('season_team', Base.metadata,
    Column('season_id', Integer, ForeignKey('season.id')),
    Column('team_id', Integer, ForeignKey('team.id'))
)
#games to teams
team_game = Table('team_game', Base.metadata,
    Column('team_id', Integer, ForeignKey('team.id')),
    Column('game_id', Integer, ForeignKey('game.id'))
)




class Season(Base):
    """
    Season has everything related to a season in soccer with the name, number of games, 
    number of teams, year and has relationships to teams, standings, and games
    """
    __tablename__ = 'season'
    # Here we define columns for the table Season
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    seasonName = Column(String(250), nullable=False)
    league = Column(String(250))
    year = Column(Integer)
    numTeams = Column(Integer)
    numGames = Column(Integer)
    numMatchdays = Column(Integer)
    curMatchday = Column(Integer)
    #relationships
    Sgame = relationship("Game", back_populates="Gseason") #1 to many
    Sstanding = relationship("Standing", back_populates="Rseason") #1 to many
    Steam = relationship("Team", secondary=season_team, back_populates="Tseason") #many to many


    def __init__(self, id, seasonName, league, year, numTeams, numGames, numMatchdays, curMatchday):
        """
        itializes everything in the Seasons class
        :param self:
        :param id:
        :param league:
        :param numTeams:
        :param numGames:
        :param numMatchdays:
        :param curMatchday:
        """

        self.id = id
        self.seasonName = seasonName
        self.league = league
        self.year = year
        self.numTeams = numTeams
        self.numGames = numGames
        self.numMatchdays = numMatchdays
        self.curMatchday = curMatchday

    def display(self):
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



class Standing(Base):
    """
    Standing has everything related to a standing in soccer with the rank, matchesPlayed, 
    points, goalsFor, and goalsAgainst
    """
    __tablename__ = 'standing'
    # Here we define columns for the table Standing
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    matchday = Column(Integer, nullable=False)
    group = Column(String(250))
    rank = Column(Integer)
    matchesPlayed = Column(Integer)
    points = Column(Integer)
    goalsFor = Column(Integer)
    goalsAgainst = Column(Integer)
    #relationships
    season_id = Column(Integer, ForeignKey('season_id'))
    Rseason = relationship("Season", back_populates=Sstanding) #many to 1 
    team_id = Column(Integer, ForeignKey('team_id'))
    Rteam = relationship("Team", back_populates=Tstanding) #many to 1


    def __init__(self, id, matchday, group, rank, matchesPlayed, points, goalsFor, goalsAgainst):
        self.id = id
        self.matchday = matchday
        self.group = group
        self.rank = rank
        self.matchesPlayed = matchesPlayed
        self.points = points
        self.goalsFor = goalsFor
        self.goalsAgainst =goalsAgainst

    def display(self):
        """
        :param self:
        :return: displayDict
        :rtype: OrderedDict
        """
        displayDict = OrderedDict()
        displayDict['id'] = self.id
        displayDict['matchday'] = self.matchday
        displayDict['group'] = self.group
        displayDict['rank'] = self.rank
        displayDict['matchesPlayed'] = self.matchesPlayed
        displayDict['points'] = self.points
        displayDict['goalsFor'] = goalsFor
        displayDict['goalsAgainst'] = goalsAgainst
        displayDict['team'] = team_id
        return displayDict



class Team(Base):
    """
    Team has everything related to a team in soccer with the name, nickname, logo, and marketVal
    """
    __tablename__ = 'team'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    teamName = Column(String(250), nullable=False)
    logoURL = Column(String(250))
    nickname = Column(String(250))
    marketVal = Column(String(250))
    #relationships
    Tseason = relationship("Season", secondary=season_team, back_populates="Steam") #many to many
    Tstanding = relationship("Standing", back_populates="Rteam") #1 to many
    Tplayer = relationship("Player", back_populates="Pteam") #1 to many
    Tgame = relationship("Game", secondary=team_game, back_populates="Gteam") #many to many


    def __init__(self, id, teamName, logoURL, nickname, marketVal):
        self.id = id
        self.teamName = teamName
        self.logoURL = logoURL
        self.nickname = nickname
        self.marketVal = marketVal

    def display(self):
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



class Game(Base):
    """
    Game has everything related to a game in soccer with the date, time, homeTeam, awayTeam, and result
    """
    __tablename__ = 'game'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    date = Column(String(250))
    time = Column(String(250))
    awayTeam = Column(String(250))
    homeTeam = Column(String(250))
    awayTeamScore = Column(Integer)
    homeTeamScore = Column(Integer)
    matchDay = Column(Integer)
    #relationships
    season_id = Column(Integer, ForeignKey('season_id'))
    Gseason = relationship("Season", back_populates="Sgame") #many to 1
    Gteam = relationship("Team", secondary=team_game, back_populates="Tgame") #many to many

    def __init__(self, id, date, time, awayTeam, homeTeam, awayTeamScore, homeTeamScore, matchday):
        self.id = id
        self.date = date
        self.time = time
        self.awayTeam = awayTeam
        self.homeTeam = homeTeam
        self.awayTeamScore = awayTeamScore
        self.homeTeamScore = homteeamScore
        self.matchday = matchday

    def display(self):
        """
        :param self:
        :return: displayDict
        :rtype: OrderedDict
        """
        displayDict = OrderedDict()
        displayDict['id'] = self.id
        displayDict['season_name'] = self.season_name.title()
        displayDict['league'] = self.league
        displayDict['year'] = self.year
        displayDict['numTeams'] = self.numTeams
        displayDict['numGames'] = self.numGames
        displayDict['matchday'] = self.matchday
        return displayDict



class Player(Base):
    """
    Player has everything related to a player in soccer with the name, nation, date of birth, position, and jersey number
    """
    __tablename__ = 'player'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    nation = Column(String(250))
    birth = Column(String(250))
    pos = Column(String(250))
    jerseyNum = Column(Integer)
    #relationships
    team_id = Column(Integer, ForeignKey('team_id'))
    Pteam = relationship("Team", back_populates=Tplayer) #many to 1


    def __init__(self, id, name, nation, birth, pos, jerseyNum):
        self.id = id
        self.name = name
        self.nation = nation
        self.birth = birth
        self.pos = pos
        self.jerseyNum = jerseyNum

    def display(self):
        """
        :param self:
        :return: displayDict
        :rtype: OrderedDict
        """
        displayDict = OrderedDict()
        displayDict['id'] = self.id
        displayDict['name'] = self.name.title()
        displayDict['nation'] = self.nation
        displayDict['birth'] = self.birth
        displayDict['pos'] = self.pos
        displayDict['jerseyNum'] = self.jerseyNum
        return displayDict


 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
#engine = create_engine('sqlite:///sqlalchemy_example.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
#Base.metadata.create_all(engine)









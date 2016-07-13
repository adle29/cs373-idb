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
season_team = db.Table('season_team', db.metadata,
    db.Column('season_id', db.Integer, db.ForeignKey('season.season_id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.team_id')),
    extend_existing=True
)
# games to teams
# team_game = db.Table('team_game', db.metadata,
#     db.Column('team_id', db.Integer, db.ForeignKey('team.team_id')),
#     db.Column('game_id', db.Integer, db.ForeignKey('game.game_id')),
#     extend_existing=True
# )


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
    season_id = db.Column(Integer, primary_key=True)
    api_season_id = db.Column(Integer, unique=True)
    season_name = db.Column(String(250), nullable=False)
    league = db.Column(String(250))
    year = db.Column(Integer)
    num_teams = db.Column(Integer)
    num_games = db.Column(Integer)
    num_match_days = db.Column(Integer)
    cur_match_day = db.Column(Integer)
    # relationships
    s_game = db.relationship("Game", back_populates="g_season")  # 1 to many
    s_standing = db.relationship("Standing", back_populates="r_season")  # 1 to many
    s_team = db.relationship(
        "Team", secondary=season_team, back_populates="t_season")  # many to many

    def __init__(self, api_season_id, season_name, league, year, num_teams, num_games, num_match_days, cur_match_day):
        """
        itializes everything in the Season class
        :param self:
        :param season_id: Integer
        :param league: String
        :param num_teams: Integer
        :param num_games: Integer
        :param num_match_days: Integer
        :param cur_match_day: Integer
        """
        #self.season_id = db.Column(Integer, primary_key=True)
        self.api_season_id = api_season_id
        self.season_name = season_name
        self.league = league
        self.year = year
        self.num_teams = num_teams
        self.num_games = num_games
        self.num_match_days = num_match_days
        self.cur_match_day = cur_match_day

    def display(self): #display(self):
        """
        :param self:
        :return: display
        :rtype: OrderedDict
        """
        display = OrderedDict()
        display['season_id'] = self.season_id
        display['season_name'] = self.season_name.title()
        display['league'] = self.league
        display['year'] = self.year
        display['num_teams'] = self.num_teams
        display['num_games'] = self.num_games
        display['num_match_days'] = self.num_match_days
        display['cur_match_day'] = self.cur_match_day
        return display


# --------------
# Standing
# --------------

class Standing(Base):

    """
    Standing has everything related to a standing in soccer with the rank, matches_played,
    points, goals_for, and goals_against
    """
    __tablename__ = 'standing'
    __table_args__ = {'extend_existing': True}
    # Here we define columns for the table Standing
    # Notice that each column is also a normal Python instance attribute.
    standing_id = db.Column(Integer, primary_key=True)
    match_day = db.Column(Integer, nullable=False)
    group = db.Column(String(250))
    rank = db.Column(Integer)
    matches_played = db.Column(Integer)
    points = db.Column(Integer)
    goals_for = db.Column(Integer)
    goals_against = db.Column(Integer)
    api_team_id = db.Column(Integer)
    # relationships
    season_id = db.Column(db.Integer, db.ForeignKey('season.season_id'))
    r_season = db.relationship("Season", back_populates="s_standing")  # many to 1
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    r_team = db.relationship("Team")  # many to 1

    def __init__(self, match_day, group, rank, matches_played, points, goals_for, goals_against, api_team_id):
        """
        itializes everything in the Standing class
        :param self:
        :param match_day: Integer
        :param group: String
        :param rank: Integer
        :param matches_played: Integer
        :param points: Integer
        :param goals_for: Integer
        :param goals_against: Integer
        :param api_team_id: Integer
        :param season_id: Integer
        """
        self.match_day = match_day
        self.group = group
        self.rank = rank
        self.matches_played = matches_played
        self.points = points
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.api_team_id = api_team_id

    def display(self):
        """
        :param self:
        :return: display
        :rtype: OrderedDict
        """
        display = OrderedDict()
        display['match_day'] = self.match_day
        display['group'] = self.group
        display['rank'] = self.rank
        display['matches_played'] = self.matches_played
        display['points'] = self.points
        display['goals_for'] = self.goals_for
        display['goals_against'] = self.goals_against
        display['team_id'] = self.team_id
        return display


# --------------
# Team
# --------------

class Team(Base):
    """
    Team has everything related to a team in soccer with the name, nickname, logo, and market_val
    """
    __tablename__ = 'team'
    __table_args__ = {'extend_existing': True}
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    team_id = db.Column(db.Integer, primary_key=True)
    api_team_id = db.Column(Integer, unique=True)
    team_name = db.Column(db.String(250), nullable=False)
    logo_url = db.Column(db.String(250))
    nickname = db.Column(db.String(250))
    market_val = db.Column(db.String(250))
    # relationships
    t_season = db.relationship(
        "Season", secondary=season_team, back_populates="s_team")  # many to many
    t_standing = db.relationship("Standing", back_populates="r_team")  # 1 to many
    t_player = db.relationship("Player", back_populates="p_team")  # 1 to many
    #t_game = db.relationship("Game", secondary=team_game, back_populates="g_team")  # many to many
    #t_game_home = db.relationship("Game", back_populates="g_team_home") # 1 to many
    #t_game_away = db.relationship("Game", back_populates="g_team_away") # 1 to many

    def __init__(self, api_team_id, team_name, logo_url, nickname, market_val):
        """
        initializes everything in the Team class
        :param self:
        :param api_team_id: Integer
        :param team_name: String
        :param logo_url: String
        :param nickname: String
        :param market_val: String
        """
        self.api_team_id = api_team_id
        self.team_name = team_name
        self.logo_url = logo_url
        self.nickname = nickname
        self.market_val = market_val

    def display(self):
        """
        :param self:
        :return: display
        :rtype: OrderedDict
        """
        display = OrderedDict()
        display['team_id'] = self.team_id
        display['team_name'] = self.team_name.title()
        display['logo_url'] = self.logo_url
        display['nickname'] = self.nickname
        display['market_val'] = self.market_val
        display['players'] = [player.player_id for player in self.t_player]
        #display['games'] = [game.game_id for game in self.t_game]
        return display

# --------------
# Game
# --------------


class Game(Base):
    """
    Game has everything related to a game in soccer with the date, time, home_team, away_team, and result
    """
    __tablename__ = 'game'
    __table_args__ = {'extend_existing': True}
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    game_id = db.Column(db.Integer, primary_key=True)
    api_game_id = db.Column(Integer, unique=True)
    date = db.Column(db.String(250))
    time = db.Column(db.String(250))
    api_away_team_id = db.Column(Integer)
    api_home_team_id = db.Column(Integer)
    away_team_score = db.Column(db.Integer)
    home_team_score = db.Column(db.Integer)
    match_day = db.Column(Integer)
    # relationships
    season_id = db.Column(db.Integer, db.ForeignKey('season.season_id'))
    g_season = db.relationship("Season")  # many to 1
    #g_team = db.relationship("Team", secondary=team_game, back_populates="t_game")  # many to many
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    g_team_home = db.relationship("Team", backref='t_game_home', foreign_keys=[home_team_id])
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    g_team_away = db.relationship("Team", backref='t_game_away', foreign_keys=[away_team_id])



    def __init__(self, api_game_id, date, time, api_away_team_id, api_home_team_id, away_team_score, home_team_score, match_day):
        """
        itializes everything in the Game class
        :param self:
        :param api_game_id: Integer
        :param date: String
        :param time: String
        :param api_away_team_id: String
        :param api_home_team_id: String
        :param away_team_score: Integer
        :param home_team_score Integer
        """
        self.api_game_id = api_game_id
        self.date = date
        self.time = time
        self.api_away_team_id = api_away_team_id
        self.api_home_team_id = api_home_team_id
        self.away_team_score = away_team_score
        self.home_team_score = home_team_score
        self.match_day = match_day

    def display(self):
        """
        :param self:
        :return: display
        :rtype: OrderedDict
        """
        display = OrderedDict()
        display['game_id'] = self.game_id
        display['date'] = self.date
        display['away_team_score'] = self.away_team_score
        display['home_team_score'] = self.home_team_score
        display['home_team_id'] = self.home_team_id
        display['away_team_id'] = self.away_team_id
        display['match_day'] = self.match_day
        return display

# --------------
# Player
# --------------


class Player(Base):

    """
    Player has everything related to a player in soccer with the name, nation, date of birth, position, and jersey number
    """
    __tablename__ = 'player'
    __table_args__ = {'extend_existing': True}
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    player_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    nation = db.Column(db.String(250))
    birth = db.Column(db.String(250))
    position = db.Column(db.String(250))
    jersey_num = db.Column(db.Integer)
    # relationships
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    p_team = db.relationship("Team")  # many to 1

    def __init__(self, name, nation, birth, position, jersey_num):
        """
        itializes everything in the player class
        :param self:
        :param name: String
        :param nation: String
        :param birth: String
        :param position: String
        :param jersey_num: Integer
        """

        self.name = name
        self.nation = nation
        self.birth = birth
        self.position = position
        self.jersey_num = jersey_num

    def display(self):
        """
        :param self:
        :return: display
        :rtype: OrderedDict
        """
        display = OrderedDict()
        display['player_id'] = self.player_id
        display['name'] = self.name.title()
        display['nation'] = self.nation
        display['birth'] = self.birth
        display['position'] = self.position
        display['jersey_num'] = self.jersey_num
        return display



# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# engine = create_engine('sqlite:///sqlalchemy_example.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)

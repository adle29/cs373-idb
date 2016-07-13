#!flask/bin/python
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

# Server and DB data
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

from sqlalchemy.ext.declarative import DeclarativeMeta

# Requests headers
headers = { 'X-Auth-Token': '1a83f9cdfa664421bc7c1997f1409218', 'X-Response-Control': 'minified' }

# Routes
@app.route('/')
def index():
    return send_file("templates/index.html")

@app.route('/seasons')
@app.route('/seasons/<offset>')
def seasons(offset=0):
    count = len(Season.query.order_by(Season.year).all())
    query = Season.query.order_by(Season.year).limit(10).offset(offset).all()
    seasons = [season.display() for season in query]
    data = {"totalNumberOfSeasons":count, "seasons":seasons}
    return json.dumps(data)

@app.route('/season/<season_id>')
def season(season_id):
    query =  Season.query.filter(Season.season_id == season_id).first()
    data = query.display()
    return json.dumps(data)

@app.route('/season/<season_id>/teams')
def season_teams(season_id):
    query =  Season.query.filter(Season.s_team).all()
    c = query
    return json.dumps(c, cls=AlchemyEncoder)

@app.route('/season/<season_id>/standings')
def season_standings(season_id):
    query =  Standing.query.filter(Standing.season_id == season_id).all()
    standings = [standing.display() for standing in query]

    for standing in standings:
        team_id = standing["team_id"]
        teams = Team.query.filter(Team.team_id == team_id).first()
        standing["logo_url"] = teams.logo_url
        standing["team_name"] = teams.team_name

    query2 = Season.query.filter(Season.season_id == season_id).first()
    data = { "season": query2.display(), "standings": standings}
    #team data
    return json.dumps(data)

@app.route('/players')
@app.route('/players/<offset>')
def player(offset=0):
    count = len(Player.query.all())
    query = Player.query.order_by(Player.name).limit(10).offset(offset).all()
    players = [player.display() for player in query]
    data = {"totalNumberOfPlayers":count, "players":players}
    return json.dumps(data)

@app.route('/players/<team_id>')
def players(team_id):
    query =  Player.query.filter(Player.team_id == team_id).first()
    data = query.display()
    return json.dumps(data)

@app.route('/teams')
@app.route('/teams/<offset>')
def teams(offset=0):
    count = len(Team.query.all())
    query = Team.query.order_by(Team.team_name).limit(10).offset(offset).all()
    teams = [team.display() for team in query]
    data = {"totalNumberOfTeams":count, "teams":teams}
    return json.dumps(data)

@app.route('/team/<team_id>')
def team(team_id):
    query =  Team.query.filter(Team.team_id == team_id).first()
    data = query.display()
    return json.dumps(data)

@app.route('/team/<team_id>/players')
def team_players(team_id):
    query = Player.query.filter(Player.team_id == team_id).all()
    players = [player.display() for player in query]
    return json.dumps(players)

@app.route('/team/<team_id>/games')
def team_games(team_id):
    query = Game.query.filter(team_id == Game.home_team_id or team_id == Game.away_team_id).all()
    games = [game.display() for game in query]

    for game in games:
        home_team_id = game["home_team_id"]
        away_team_id = game["away_team_id"]
        homeTeam = Team.query.filter(Team.team_id == home_team_id).first()
        awayTeam = Team.query.filter(Team.team_id == away_team_id).first()
        print(homeTeam.display())
        game["home_team_name"] = homeTeam.display()["team_name"]
        game["away_team_name"] = awayTeam.display()["team_name"]

    return json.dumps(games)

@app.route('/games')
@app.route('/games/<offset>')
def games(offset=0):
    count = len(Game.query.order_by(Game.date).all())
    query = Game.query.order_by(Game.date).limit(10).offset(offset).all()
    games = [game.display() for game in query]

    for game in games:
        print(game)
        home_team_id = game["home_team_id"]
        away_team_id = game["away_team_id"]
        homeTeam = Team.query.filter(Team.team_id == home_team_id).first()
        awayTeam = Team.query.filter(Team.team_id == away_team_id).first()
        game["home_team_name"] = homeTeam.display()["team_name"]
        game["away_team_name"] = awayTeam.display()["team_name"]

    data = {"totalNumberOfGames":count, "games":games}
    return json.dumps(data)

# @app.route('/season/players/<season_id>')
# def season_players(season_id):
#     query =  Player.query.filter(Player.season_id == season_id).first()
#     data = query.display()
#     return json.dumps(data)

# @app.route('/data/<filename>')
# def data(filename):
#     print("[+]Returning JSON file.")
#     print( send_file("static/js/data/"+filename) )
#     return send_file("static/js/data/"+filename)
#
# @app.route('/team/<team_id>/players')
# def team_players(team_id):
#     r = requests.get('http://api.football-data.org/v1/teams/'+team_id+'/players', headers=headers)
#     return r.text
#
# @app.route('/team/<team_id>/fixtures')
# def team_fixtures(team_id):
#     r = requests.get('http://api.football-data.org/v1/teams/'+team_id+'/fixtures', headers=headers)
#     return r.text

@app.route('/runtests')
def run_tests():

    test_out = []
    line = "-------------------------"

    tout = io.StringIO()

    cmd = 'python apps/tests.py'
    try:
        output = subprocess.check_output("{}".format(cmd), shell = True)
        # test_out.append("{0}\n{1}\n{2}\n{3}\n".format(line,cmd,line,output))
        tout.write("{0}\n{1}\n{2}\n{3}\n".format(line,cmd,line,output))
    except Exception as e:
        tout.write("Exception when running {0}\n{1}\n{2}\n{3}\n".format(cmd, type(e), e.args, e))

    cmd = 'pylint apps/tests.py'

    try:
        output = subprocess.check_output("{}".format(cmd), shell = True)
        # test_out.append("{0}\n{1}\n{2}\n{3}\n".format(line,cmd,line,output))
        tout.write("{0}\n{1}\n{2}\n{3}\n".format(line,cmd,line,output))
    except Exception as e:
        tout.write("Exception when running {0}\n{1}\n{2}\n{3}\n".format(cmd, type(e), e.args, e))

    cmd = 'coverage apps/tests.py'
    try:
        output = subprocess.check_output("{}".format(cmd), shell = True)
        # test_out.append("{0}\n{1}\n{2}\n{3}\n".format(line,cmd,line,output))
        tout.write("{0}\n{1}\n{2}\n{3}\n".format(line,cmd,line,output))
    except Exception as e:
        tout.write("Exception when running {0}\n{1}\n{2}\n{3}\n".format(cmd, type(e), e.args, e))

    return tout.getvalue()


## utils ##
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    app.run(debug=True)

#!flask/bin/python
import os
import sys
import subprocess
import io
from flask import Flask, request, url_for
from flask import render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
import requests
import ast
import json
import config
import itertools

# Server and DB data
app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig) #os.environ['APP_SETTINGS'])
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
    count = len(db.session.query(Season).all())
    query = db.session.query(Season).order_by(Season.year.desc()).limit(10).offset(offset).all()
    seasons = [season.display() for season in query]
    data = {"totalNumberOfSeasons":count, "seasons":seasons}
    db.session.close()
    return json.dumps(data)

@app.route('/season/<season_id>')
def season(season_id):
    query =  db.session.query(Season).filter(Season.season_id == season_id).first()
    data = query.display()
    db.session.close()
    return json.dumps(data)

@app.route('/season/<season_id>/teams')
def season_teams(season_id):
    query =  db.session.query(Season).filter(Season.s_team).all()
    c = query
    db.session.close()
    return json.dumps(c, cls=AlchemyEncoder)

@app.route('/season/<season_id>/standings')
def season_standings(season_id):
    query =  db.session.query(Standing).filter(Standing.season_id == season_id).all()
    standings = [standing.display() for standing in query]

    for standing in standings:
        team_id = standing["team_id"]
        teams = Team.query.filter(Team.team_id == team_id).first()
        standing["logo_url"] = teams.logo_url
        standing["team_name"] = teams.team_name

    query2 = db.session.query(Season).filter(Season.season_id == season_id).first()
    data = { "season": query2.display(), "standings": standings}
    db.session.close()
    #team data
    return json.dumps(data)

@app.route('/players')
@app.route('/players/<offset>')
def player(offset=0):
    count = len(db.session.query(Player).all())
    query = db.session.query(Player).order_by(Player.name.asc()).limit(10).offset(offset).all()
    players = [player.display() for player in query]

    for player in players: 
        team_id = player["team_id"]
        team = db.session.query(Team).filter(Team.team_id == team_id).first()
        player["team"] = team.display()

    data = {"totalNumberOfPlayers":count, "players":players}
    db.session.close()
    return json.dumps(data)

@app.route('/players/<team_id>')
def players(team_id):
    query =  db.session.query(Player).filter(Player.team_id == team_id).first()
    data = query.display()
    db.session.close()
    return json.dumps(data)

@app.route('/teams')
@app.route('/teams/<offset>')
def teams(offset=0):
    count = len(db.session.query(Team).all())
    query = db.session.query(Team).order_by(Team.team_name).limit(10).offset(offset).all()
    teams = [team.display() for team in query]
    data = {"totalNumberOfTeams":count, "teams":teams}
    db.session.close()
    return json.dumps(data)

@app.route('/team/<team_id>')
def team(team_id):
    query = db.session.query(Team).filter(Team.team_id == team_id).first()
    data = query.display()
    db.session.close()
    return json.dumps(data)

@app.route('/team/<team_id>/players')
def team_players(team_id):
    query = db.session.query(Player).filter(Player.team_id == team_id).all()
    players = [player.display() for player in query]
    db.session.close()
    return json.dumps(players)

@app.route('/team/<team_id>/games')
def team_games(team_id):
    query = db.session.query(Game).filter(team_id == Game.home_team_id or team_id == Game.away_team_id).all()
    games = [game.display() for game in query]

    for game in games:
        home_team_id = game["home_team_id"]
        away_team_id = game["away_team_id"]
        season_id = game["season_id"]
        homeTeam = db.session.query(Team).filter(Team.team_id == home_team_id).first()
        awayTeam = db.session.query(Team).filter(Team.team_id == away_team_id).first()
        print(homeTeam.display())
        game["home_team_name"] = homeTeam.display()["team_name"]
        game["away_team_name"] = awayTeam.display()["team_name"]
        season = db.session.query(Season).filter(Season.season_id == season_id).first()
        game["season"] = season.display()

    db.session.close()

    return json.dumps(games)

@app.route('/games')
@app.route('/games/<offset>')
def games(offset=0):
    count = len(db.session.query(Game).all())
    query = db.session.query(Game).order_by(Game.date.desc()).limit(10).offset(offset).all()
    games = [game.display() for game in query]

    for game in games:
        print(game)
        home_team_id = game["home_team_id"]
        away_team_id = game["away_team_id"]
        season_id = game["season_id"]
        homeTeam = db.session.query(Team).filter(Team.team_id == home_team_id).first()
        awayTeam = db.session.query(Team).filter(Team.team_id == away_team_id).first()
        game["home_team_name"] = homeTeam.display()["team_name"]
        game["away_team_name"] = awayTeam.display()["team_name"]
        season = db.session.query(Season).filter(Season.season_id == season_id).first()
        game["season"] = season.display()

    data = {"totalNumberOfGames":count, "games":games}
    db.session.close()
    return json.dumps(data)

#function for all searches
@app.route('/search')
def search_site():
    arguments = str(request.args.get('q', '')).split(' ')
    parameters = [x for x in arguments if x != '']
    string = ' '.join(parameters)

    #loop though the attributes of the model 
    sstring  = '%' + str('%'.join(c for c in string)) + '%'

    for i in range(0, len(parameters)): 
        param = parameters[i]
        parameters[i] = '%' + str('%'.join(c for c in param)) + '%'

    def make_search(model, attributes, string, parameters, key):
        merged = {}
        merged_list = []
        query_all = None
        query = None

        for attribute in attributes:
            model_attribute = getattr(model, attribute)

            query_all = db.session.query(model).filter(
                model_attribute.like(string)).all()

            query = sum([db.session.query(model).filter(
                model_attribute.like(q)).all() for q in
                parameters], [])


            #Filter results
            l1 = [dict(item.display()) for item in query_all]
            l2 = [dict(item.display()) for item in query]

            for item in l1+l2+merged_list:
                if item[key] not in merged:
                    merged[item[key]] = item
                    merged_list.append(item)

        return merged_list

    # SEARCH SEASONS
    attributes = ["league", "season_name"]
    seasons = make_search(Season, attributes, sstring, parameters, "season_id")

    # SEARCH TEAM
    attributes = ["team_name", "nickname"]
    teams = make_search(Team, attributes, sstring, parameters, "team_id")

    # SEARCH PLAYERS
    attributes = ["nation", "name", "position"]
    players = make_search(Player, attributes, sstring, parameters, "player_id")

    # SEARCH GAMES

    query = db.session.query(Game).all()
    games = [game.display() for game in query]
    sgames = []

    # for game in games:
    #     home_team_id = game["home_team_id"]
    #     away_team_id = game["away_team_id"]
    #     homeTeam = db.session.query(Team).filter(Team.team_id == home_team_id).first()
    #     awayTeam = db.session.query(Team).filter(Team.team_id == away_team_id).first()
    #     game["home_team_name"] = homeTeam.display()["team_name"]
    #     game["away_team_name"] = awayTeam.display()["team_name"]

    #     if string in game["home_team_name"] or string in game["away_team_name"]:
    #         sgames.append(game)

    data = {
       'seasons' : seasons,
       'players' : players,
       'teams'   : teams,
       'games'   : []#sgames
    }

    db.session.close()
    return json.dumps(data)

# @app.errorhandler(404)
# def page_does_not_exist(error):
#     print(error)
#     return render_template('templates/404.html'), 404

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

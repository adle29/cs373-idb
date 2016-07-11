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

# Server and DB data
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

# Requests headers
headers = { 'X-Auth-Token': '1a83f9cdfa664421bc7c1997f1409218', 'X-Response-Control': 'minified' }

# Routes
@app.route('/')
def index():
    return send_file("templates/index.html")

@app.route('/seasons')
def seasons():
    r = requests.get('http://api.football-data.org/v1/competitions/?season=2015', headers=headers)
    return r.text

@app.route('/season/<season_id>')
def season(season_id):
    r = requests.get('http://api.football-data.org/v1/competitions/'+season_id+'/leagueTable', headers=headers)
    return r.text

@app.route('/season/<season_id>/teams')
def season_teams(season_id):
    r = requests.get('http://api.football-data.org/v1/competitions/'+season_id+'/teams', headers=headers)
    return r.text

@app.route('/season/players/<season_id>')
def season_players(season_id):
    r = requests.get('http://api.football-data.org/v1/competitions/'+season_id+'/leagueTable', headers=headers)
    return r.text

@app.route('/data/<filename>')
def data(filename):
    print("[+]Returning JSON file.")
    print( send_file("static/js/data/"+filename) )
    return send_file("static/js/data/"+filename)

@app.route('/team/<team_id>')
def team(team_id):
    r = requests.get('http://api.football-data.org/v1/teams/'+team_id, headers=headers)
    return r.text

@app.route('/team/<team_id>/players')
def team_players(team_id):
    r = requests.get('http://api.football-data.org/v1/teams/'+team_id+'/players', headers=headers)
    return r.text

@app.route('/team/<team_id>/fixtures')
def team_fixtures(team_id):
    r = requests.get('http://api.football-data.org/v1/teams/'+team_id+'/fixtures', headers=headers)
    return r.text

@app.route('/players/<team_id>')
def players(team_id):
    r = requests.get('http://api.football-data.org/v1/teams/'+team_id+'/players', headers=headers)
    return r.text

@app.route('/games')
def games():
    r = requests.get('http://api.football-data.org/v1/fixtures/', headers=headers)
    return r.text


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

if __name__ == '__main__':
    app.run(debug=True)

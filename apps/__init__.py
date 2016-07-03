#!flask/bin/python
from flask import Flask
from flask import render_template, send_file
import requests
import ast

app = Flask(__name__)

headers = { 'X-Auth-Token': '1a83f9cdfa664421bc7c1997f1409218', 'X-Response-Control': 'minified' }

@app.route('/')
def index():
    return send_file("templates/index.html")

@app.route('/seasons')
def seasons():
    r = requests.get('http://api.football-data.org/v1/competitions/?season=2016', headers=headers)
    return r.text

@app.route('/season/<season_id>')
def season(season_id):
    r = requests.get('http://api.football-data.org/v1/competitions/'+season_id+'/leagueTable', headers=headers)
    return r.text

@app.route('/team/<team_id>')
def team(team_id):
    r = requests.get('http://api.football-data.org/v1/teams/'+team_id, headers=headers)
    return r.text

@app.route('/players/<team_id>')
def players(team_id):
    r = requests.get('http://api.football-data.org/v1/teams/'+team_id+'/players', headers=headers)
    return r.text

@app.route('/games')
def games():
    r = requests.get('http://api.football-data.org/v1/fixtures/', headers=headers)
    return r.text
#
# @app.route('/seasons')
# def seasons(name=None):
#     return render_template('seasons.html', name=name)
#
# @app.route('/about')
# def about(name=None):
#     return render_template('about.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

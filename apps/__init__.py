#!flask/bin/python
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/players')
def players(name=None):
    return render_template('players.html', name=name)

@app.route('/teams')
def teams(name=None):
    return render_template('teams.html', name=name)

@app.route('/seasons')
def seasons(name=None):
    return render_template('seasons.html', name=name)

@app.route('/about')
def about(name=None):
    return render_template('about.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

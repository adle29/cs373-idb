#!flask/bin/python
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

@app.route('/players')
def players():
    return 'player'

@app.route('/teams')
def teams():
    return 'team'

@app.route('/seasons')
def seasons():
    return 'seasons'

@app.route('/about')
def about(name=None):
    return render_template('static/about.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

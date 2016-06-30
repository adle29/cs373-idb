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

@app.route('/leagues')
def leagues():
    return 'leagues'

if __name__ == '__main__':
    app.run(debug=True)

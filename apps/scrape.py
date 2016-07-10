from models import *
from __init__ import db
import requests
import json

headers = { 'X-Auth-Token': '1a83f9cdfa664421bc7c1997f1409218', 'X-Response-Control': 'minified' }


def makeRequest(url):
    r = requests.get(url, headers=headers)
    return r.text

def populateSeasons():
    url = 'http://api.football-data.org/v1/competitions/?season=2015'
    response = makeRequest(url)
    res = json.loads(response)
    print (res)
    for season in res:
        # try:

        result = Season(
        	api_season_id = season["id"],
        	season_name = season["caption"],
        	league = season["league"],
        	year = season["year"],
        	num_teams = season["numberOfTeams"],
        	num_games = season["numberOfGames"],
        	num_match_days = season["numberOfMatchdays"],
        	cur_match_day = season["currentMatchday"]
        )
        db.session.add(result)
        db.session.commit()
        # except:
        #     print("error getting data")


def populateTeamsForSeason(season):
    # url = 'http://api.football-data.org/v1/competitions/?season=2015'
    url = 'http://api.football-data.org/v1/competitions/' + str(season) +'/teams'
    response = makeRequest(url)
    res = json.loads(response)
    print (res)
    print (url)
    teams = res["teams"]
    for instance in teams:
        # try:

        result = Team(
        	api_team_id = instance["id"],
        	team_name = instance["name"],
        	logo_url = instance["crestUrl"],
        	nickname = instance["shortName"],
        	market_val = instance["squadMarketValue"]
        )



        db.session.add(result)
        db.session.commit()
        # except:
        #     print("error getting data")

def populateGamesForSeason(season):
    # url = 'http://api.football-data.org/v1/competitions/?season=2015'
    url = 'http://api.football-data.org/v1/competitions/' + str(season) +'/fixtures'
    response = makeRequest(url)
    res = json.loads(response)
    print (res)
    print (url)
    teams = res["fixtures"]
    for instance in teams:
        # try:

        result = Games(
        	api_game_id = instance["id"],
        	date = instance["date"],
        	match_day = instance["matchday"],
        	market_val = instance["squadMarketValue"],
        	away_team_score = instance["result"]["goalsAwayTeam"],
        	home_team_score = instance["result"]["goalsHomeTeam"]
        )

  		

        db.session.add(result)
        db.session.commit()
        # except:
        #     print("error getting data")

def main():
    # populateSeasons()
    populateTeamsForSeason(398)

if __name__ == "__main__":
    main()

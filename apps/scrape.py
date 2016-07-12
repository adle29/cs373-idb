from models import *
from __init__ import db
import requests
import json

headers = { 'X-Auth-Token': '1a83f9cdfa664421bc7c1997f1409218', 'X-Response-Control': 'minified' }


def make_request(url):
    r = requests.get(url, headers=headers)
    return r.text

def populate_seasons():
    url = 'http://api.football-data.org/v1/competitions/?season=2015'
    response = make_request(url)
    res = json.loads(response)
    for season in res:
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

def populate_teams_for_season(season_id):
    # url = 'http://api.football-data.org/v1/competitions/?season=2015'
    url = 'http://api.football-data.org/v1/competitions/' + str(season_id) +'/teams'
    response = make_request(url)
    res = json.loads(response)
    try:
        for instance in teams:
            result = Team(
            	api_team_id = instance["id"],
            	team_name = instance["name"],
            	logo_url = instance["crestUrl"],
            	nickname = instance["shortName"],
            	market_val = instance["squadMarketValue"]
            )

            db.session.add(result)

    except:
        print("error getting data for teams for season "+ str(season_id) )

def populate_games_for_season(season_id):
    # url = 'http://api.football-data.org/v1/competitions/?season=2015'
    url = 'http://api.football-data.org/v1/competitions/' + str(season_id) +'/fixtures'
    response = make_request(url)
    res = json.loads(response)
    try:
        games = res["fixtures"]
        for instance in games:
            result = Game(
            	api_game_id = instance["id"],
            	date = instance["date"],
                time = instance["date"],
                away_team = instance["awayTeamName"],
                home_team = instance["homeTeamName"],
            	match_day = instance["matchday"],
            	away_team_score = instance["result"]["goalsAwayTeam"],
            	home_team_score = instance["result"]["goalsHomeTeam"]
            )

            db.session.add(result)

    except:
        print("error getting data for games from season " + str(season_id))

def populate_standings_for_season(season_id):
    # url = 'http://api.football-data.org/v1/competitions/?season=2015'
    url = 'http://api.football-data.org/v1/competitions/' + str(season_id) +'/leagueTable'
    response = make_request(url)
    standings = list()

    try:
        res = json.loads(response)
        match_day = res["matchday"]

        if "standing" in res.keys():
            standings = res["standing"]

            for instance in standings:
                result = Standing(
                	api_standing_id = "",
                	match_day = match_day,
                	group = "", #CLARK KNOWS BETTER ABOUT THE GROUP SITUATION
                	rank = instance["rank"],
                	points = instance["points"],
                	matches_played = instance["playedGames"],
                	goals_for = instance["goals"],
                	goals_against = instance["goalsAgainst"]
                )

                db.session.add(result)

        elif "standings" in res.keys():
            standings = res["standings"]

            for key in standings:
                instance = standings[key]
                result = Standing(
                	api_standing_id = "",
                	match_day = match_day,
                	group = key, #CLARK KNOWS BETTER ABOUT THE GROUP SITUATION
                	rank = instance["rank"],
                	points = instance["points"],
                	matches_played = instance["playedGames"],
                	goals_for = instance["goals"],
                	goals_against = instance["goalsAgainst"]
                )

                db.session.add(result)

    except Exception as e:
        print("error getting standings for season " +  str(season_id))

def populate_players_for_team(team_id):
    url = 'http://api.football-data.org/v1/teams/'+str(team_id)+'/players'
    response = make_request(url)
    try:
        res = json.loads(response)
        players = res["players"]
        count = 0
        for instance in players:
            result = Player(
                api_player_id = 1,
                name = instance["name"],
                pos = instance["position"],
                jersey_num = instance["jerseyNumber"],
                birth = instance["dateOfBirth"],
                nation = instance["nationality"])

            db.session.add(result)

    except Exception as e:
        print("error getting players for team " +  str(team_id))
        print(e)

def season_api_ids():
	ids = list()
	for instance in db.session.query(Season):#.order_by(season_id):
		ids += [instance.season_id]
	return ids

def team_api_ids():
	ids = list()
	for instance in db.session.query(Team):#.order_by(team.team_id):
		ids += [instance.team_id]
	return ids


def main():

    populate_seasons()
    season_ids = season_api_ids()

    for season_id in season_ids:
        populate_teams_for_season(season_id)
        populate_games_for_season(season_id)
        populate_standings_for_season(season_id)

    team_ids = team_api_ids()

    for team_id in team_ids:
        populate_players_for_team(team_id)

    db.session.commit()


if __name__ == "__main__":
    main()

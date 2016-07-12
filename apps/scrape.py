from models import *
from __init__ import db
import requests
import json

headers = { 'X-Auth-Token': '1a83f9cdfa664421bc7c1997f1409218', 'X-Response-Control': 'minified' }

teams_cache = dict()
seasons_cache = list()
standings_cache = list()
games_cache = list()

def make_request(url):
    r = requests.get(url, headers=headers)
    return r.text

def populate_seasons_for_year(year):
    url = 'http://api.football-data.org/v1/competitions/?season=' + str(year)
    response = make_request(url)
    res = json.loads(response)
    try:
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

            seasons_cache.append(result)

            db.session.add(result)
            db.session.commit()
    except:
        print("error getting data")


def populate_teams_for_season(season):
    url = 'http://api.football-data.org/v1/competitions/' + str(season.api_season_id) +'/teams'
    response = make_request(url)
    res = json.loads(response)
    try:
        teams_response = res["teams"]
        for instance in teams_response:
            result = Team(
            	api_team_id = instance["id"],
            	team_name = instance["name"],
            	logo_url = instance["crestUrl"],
            	nickname = instance["shortName"],
            	market_val = instance["squadMarketValue"]
            )

            teams_cache[result.api_team_id] = result
            
            season.s_team.append(result)
            db.session.add(result)
            db.session.commit()
            
    except:
        print("error getting data for teams for season "+ str(season.api_season_id) + " response " + str(res))

def populate_games_for_season(season):
    url = 'http://api.football-data.org/v1/competitions/' + str(season.api_season_id) +'/fixtures'
    response = make_request(url)
    res = json.loads(response)
    try:
        games_response = res["fixtures"]
        for instance in games_response:
            result = Game(
            	api_game_id = instance["id"],
            	date = instance["date"],
                time = instance["date"],
                api_away_team_id = instance["awayTeamId"],
                api_home_team_id = instance["homeTeamId"],
            	match_day = instance["matchday"],
            	away_team_score = instance["result"]["goalsAwayTeam"],
            	home_team_score = instance["result"]["goalsHomeTeam"]
            )

            games_cache.append(result)
            season.s_game.append(result)

    except:
        print("error getting data for games from season " + str(season.api_season_id) + " response " + str(res))

def populate_standings_for_season(season):
    # url = 'http://api.football-data.org/v1/competitions/?season=2015'
    url = 'http://api.football-data.org/v1/competitions/' + str(season.api_season_id) +'/leagueTable'
    response = make_request(url)
    try:
        res = json.loads(response)
        match_day = res["matchday"]
        standings_response = res["standing"]

        for instance in standings_response:
            result = Standing(
            	match_day = match_day,
            	group = "CLARK", #CLARK KNOWS BETTER ABOUT THE GROUP SITUATION
            	rank = instance["rank"],
            	points = instance["points"],
            	matches_played = instance["playedGames"],
            	goals_for = instance["goals"],
            	goals_against = instance["goalsAgainst"],
                api_team_id = instance["teamId"]
            )
            
            standings_cache.append(result)
            season.s_standing.append(result)

    except Exception as e:
        print("error getting standings for season " +  str(season.api_season_id))

def populate_players_for_team(team):
    url = 'http://api.football-data.org/v1/teams/' + str(team.api_team_id) +'/players'
    response = make_request(url)
    res = json.loads(response)
    players_response = res["players"]
    for instance in players_response:
        # try:

           # THERES NO API ID COMING FROM THE API
        result = Player(
            name = instance["name"],
            position = instance["position"],
            jersey_num = instance["jerseyNumber"],
            birth = instance["dateOfBirth"],
            nation = instance["nationality"])

        team.t_player.append(result)
        db.session.add(result)
        db.session.commit()

def connect_standings_to_teams():
    for rank in standings_cache:
        team = teams_cache[rank.api_team_id]
        rank.r_team = team
        db.session.add(rank)
        db.session.commit()

def connect_games_to_teams():
    for game in games_cache:
        home = teams_cache[game.api_home_team_id]
        away = teams_cache[game.api_away_team_id]
        game.g_team_home = home
        game.g_team_away = away
        db.session.add(game)
        db.session.commit()

def main():

    # db.execute("DROP TABLE IF EXISTS season")
    # db.execute("DROP TABLE IF EXISTS standing")
    # db.execute("DROP TABLE IF EXISTS game")
    # db.execute("DROP TABLE IF EXISTS team")
    # db.execute("DROP TABLE IF EXISTS player")
    # db.execute("DROP TABLE IF EXISTS season_team")
    
    # populate_seasons_for_year(2015)

    # season = seasons_cache[0]

    # populate_teams_for_season(season)
    # populate_games_for_season(season)
    # populate_standings_for_season(season)

    # for team in teams_cache.values():
    #     populate_players_for_team(team)

    # connect_standings_to_teams()
    # connect_games_to_teams()



    for year in range(1970, 2017):
        populate_seasons_for_year(year)

    for season in seasons_cache:
        populate_teams_for_season(season)
        populate_games_for_season(season)
        populate_standings_for_season(season)

    for team in teams_cache.values():
        populate_players_for_team(team)

    connect_standings_to_teams()
    connect_games_to_teams()

    db.session.commit()

if __name__ == "__main__":
    main()

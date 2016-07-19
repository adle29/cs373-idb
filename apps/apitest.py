#!/usr/bin/env python3

import json
import unittest
import requests
import time

class APITestCases(unittest.TestCase):
    
    def test_seasons_request(self):
        r = requests.get('http://goalazostats.me/seasons')
        j = r.json() 
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('seasons' in j)
        self.assertTrue('totalNumberOfSeasons' in j)
        time.sleep(1)

    def test_seasons_offset_request(self):
        r = requests.get('http://goalazostats.me/seasons/5')
        j = r.json()
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('seasons' in j)
        self.assertTrue('totalNumberOfSeasons' in j)
        time.sleep(1)      

    def test_season_request(self):
        r = requests.get('http://goalazostats.me/season/1')
        j = r.json()
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('cur_match_day' in j)
        self.assertTrue('season_name' in j)
        self.assertTrue('league' in j)
        self.assertTrue('season_id' in j)
        self.assertTrue('num_match_days' in j)
        self.assertTrue('num_teams' in j)
        self.assertTrue('year' in j)
        self.assertTrue('num_games' in j)
        time.sleep(1)


    # test_season_teams_request
 
    def test_seasons_standing_request(self):
        r = requests.get('http://goalazostats.me/season/1/standings')
        j = r.json()
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('season' in j)
        self.assertTrue('standings' in j)
        time.sleep(1)



    def test_players_request(self):
        r = requests.get('http://goalazostats.me/players')
        j = r.json()
        #print(j) 
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('players' in j)
        self.assertTrue('totalNumberOfPlayers' in j)
        time.sleep(1)





    def test_players_offset_request(self):
        r = requests.get('http://goalazostats.me/players/5')
        j = r.json()
        #print(j) 
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('players' in j)
        self.assertTrue('totalNumberOfPlayers' in j)
        time.sleep(1)



    def test_teams_request(self):
        r = requests.get('http://goalazostats.me/teams')
        j = r.json()
        #print(j) 
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('teams' in j)
        self.assertTrue('totalNumberOfTeams' in j)
        time.sleep(1)



    def test_teams_offset_request(self):
        r = requests.get('http://goalazostats.me/teams/2')
        j = r.json()
        #print(j) 
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('teams' in j)
        self.assertTrue('totalNumberOfTeams' in j)
        time.sleep(1)



    def test_team_request(self):
        r = requests.get('http://goalazostats.me/team/1')
        j = r.json()
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('api_team_id' in j)
        self.assertTrue('team_id' in j)
        self.assertTrue('team_name' in j)
        self.assertTrue('logo_url' in j)
        self.assertTrue('nickname' in j)
        self.assertTrue('market_val' in j)
        self.assertTrue('players' in j)
        time.sleep(1)

  
    def test_team_players_request(self):
        r = requests.get('http://goalazostats.me/team/1/players')
        j = r.json()
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        time.sleep(1)


    def test_team_games_request(self):
        r = requests.get('http://goalazostats.me/team/1/games')
        j = r.json()
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        time.sleep(1)


    def test_games_request(self):
        r = requests.get('http://goalazostats.me/games')
        j = r.json()
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('games' in j)
        self.assertTrue('totalNumberOfGames' in j)
        time.sleep(1)



    def test_games_offset_request(self):
        r = requests.get('http://goalazostats.me/games/5')
        j = r.json()
        #print(j)
#        for k,v in j.items():
#            print("{0} : {1}".format(k, v))
        self.assertTrue('games' in j)
        self.assertTrue('totalNumberOfGames' in j)
        time.sleep(1)





if __name__  == '__main__':
    unittest.main()

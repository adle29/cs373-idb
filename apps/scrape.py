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
    for season in res:
        try:
            result = Season(
                id = season["id"],
                seasonName = season["caption"],
                league = season["league"],
                year = season["year"],
                numTeams = season["numberOfTeams"],
                numGames = season["numberOfGames"],
                numMatchdays = season["numberOfMatchdays"],
                curMatchday = season["currentMatchday"]
            )
            db.session.add(result)
            db.session.commit()
            return result.id
        except:
            print("error getting data")


def main():
    populateSeasons()

if __name__ == "__main__":
    main()

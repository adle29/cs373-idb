 import sqlalchemy

# Seasons
    # Season_id #connected to games
    # List of teams #connected to teams
    # Name of the Season
    # Name of the league
    # Year
    # Standings
    #

# Games
    # Season_id #connected to seasons
    # Date
    # result
    # homeTeamId #connected to teams
    # awayTeamId  #connected to teams
    # Result
#
# Teams
    # Team_id
    # Name
    # Logo_url
    # List of player ids #connected to player
    # List of games ids #contect to Games

# Player
    # Player_id
    # Team_id  #connected to team
    #  name
    # Position
    # Nationality

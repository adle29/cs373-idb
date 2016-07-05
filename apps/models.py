from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
#
# class Season(Base):
#     __tablename__ = "seasons"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#
# class Standing(Base):
#     id = Column(Integer, primary_key=True)
#     team_name =
#     team_id =
#     group_letter =
#     seasons_id = Column(Integer, primary_key=True)
#     playedGames: team.playedGames,
#     goalsAgainst: team.goalsAgainst,
#     rank =
#     goals: team.goals,
#     pts: team.points
#
# class Teams(Base):
#     __tablename__ = "seasons"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     logo = Column(String)
#
# class Games(Base):
#     __tablename__ = "seasons"
#     id = Column(Integer, primary_key=True)
#     date =
#     awayTeamName =
#     homeTeamName =
#
# class Player(Base):
#     __tablename__ = "seasons"
#     id = Column(Integer, primary_key=True)
#     team_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     position = Column(String)
#     nationality = Column(String)

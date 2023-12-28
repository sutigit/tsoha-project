from db import db
from flask import session
from sqlalchemy import text

# GET ALL GAMES
def get_games():
    sql = text("SELECT id, name, description, image FROM games")
    result = db.session.execute(sql)
    return result.fetchall()

# GET LEADER GAMES TOP 3 by vote
def get_leader_games():
    sql = text("SELECT games.id, games.name, games.description, games.image, COUNT(votes.game_id) AS vote_count FROM games LEFT JOIN votes ON games.id = votes.game_id GROUP BY games.id ORDER BY vote_count DESC LIMIT 3")
    result = db.session.execute(sql)
    return result.fetchall()


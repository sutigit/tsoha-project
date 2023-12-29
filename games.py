from db import db
from flask import session
from sqlalchemy import text

# GET ALL GAMES
def get_games():
    sql = text("SELECT id, name, description, image FROM games")
    result = db.session.execute(sql)
    return result.fetchall()

# GET GAME BY ID
def get_game(id):
    sql = text("SELECT id, name, description, image FROM games WHERE id = :id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

# GET LEADER GAMES TOP 3 by vote
def get_leader_games():
    sql = text("SELECT id, name, image FROM games ORDER BY votes DESC LIMIT 3")
    result = db.session.execute(sql)
    return result.fetchall()

# VOTE A GAME
def vote(id):
    sql = text("UPDATE games SET votes = votes + 1 WHERE id = :id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

    

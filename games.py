from db import db
from flask import session
from sqlalchemy import text

# GET ALL GAMES
def get_games():
    user_id = session.get("user_id")

    sql = text("""
            SELECT games.id, games.name, games.description, games.image, gamevotes.user_id = :user_id AS voted
            FROM games LEFT JOIN gamevotes ON games.id = gamevotes.game_id
            ORDER BY name;
        """)
    
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

# GET GAME BY ID
def get_game(id):
    sql = text("""
            SELECT id, name, description, image 
            FROM games 
            WHERE id = :id
        """)
    
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

# GET LEADER GAMES TOP 3 by vote
def get_leader_games():
    # count all votes by game id
    sql = text("""
                SELECT games.name, games.image, COUNT(gamevotes.game_id) AS votes
                FROM games LEFT JOIN gamevotes ON games.id = gamevotes.game_id
                GROUP BY games.id, games.name, games.image
                ORDER BY COUNT(gamevotes.game_id) 
                DESC
                LIMIT 3;
            """)
    
    result = db.session.execute(sql)    
    return result.fetchall()

# VOTE A GAME
def vote(game_id, user_id):
    sql = text("""
            INSERT INTO gamevotes (game_id, user_id) 
            VALUES (:game_id, :user_id)
        """)
    
    db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    db.session.commit()

# UNVOTE A GAME
def unvote(game_id, user_id):
    sql = text("""
            DELETE 
            FROM gamevotes 
            WHERE game_id = :game_id AND user_id = :user_id
        """)
    
    db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    db.session.commit()

    
# GET ALL VOTES BY USER
def get_gamevotes_by_user(user_id):
    sql = text("""
            SELECT DISTINCT game_id 
            FROM gamevotes 
            WHERE user_id = :user_id
        """)
    
    result = db.session.execute(sql, {"user_id":user_id})
    return [row[0] for row in result.fetchall()]
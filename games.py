from db import db
from sqlalchemy import text

# GET ALL GAMES
def get_games(user_id):
    sql = text("""
            SELECT games.id, games.name, games.description, games.image, gamevotes.user_id = :user_id AS voted
            FROM games LEFT JOIN gamevotes ON games.id = gamevotes.game_id AND gamevotes.user_id = :user_id
            ORDER BY name;
        """)
        
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


# GET GAME BY ID
def get_game(game_id, user_id):
    sql = text("""
            SELECT games.id, games.name, games.description, games.image, gamevotes.user_id = :user_id AS voted
            FROM games LEFT JOIN gamevotes ON games.id = gamevotes.game_id AND gamevotes.user_id = :user_id
            WHERE games.id = :game_id;
        """)
    
    result = db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    return result.fetchone()


# GET TOP 3 GAMES BY VOTES
def get_top3_games():
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

# CHECK IF USER HAS ALREADY VOTED
def has_been_voted(game_id, user_id):
    sql = text("""
            SELECT id
            FROM gamevotes
            WHERE game_id = :game_id AND user_id = :user_id
        """)
    
    result = db.session.execute(sql, {"game_id":game_id, "user_id":user_id})

    if result.fetchone():
        return True
    else:
        return False

# UNVOTE A GAME
def unvote(game_id, user_id):
    sql = text("""
            DELETE 
            FROM gamevotes 
            WHERE game_id = :game_id AND user_id = :user_id
        """)
    
    db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    db.session.commit()

    
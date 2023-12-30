from db import db
from sqlalchemy import text

def post_comment(game_id, user_id, message):
    sql = text("""
            INSERT INTO messages (game_id, user_id, message) 
            VALUES (:game_id, :user_id, :message)
        """)
    
    db.session.execute(sql, {"game_id":game_id, "user_id":user_id, "message":message})
    db.session.commit()

def get_messages(game_id):
    sql = text("""
            SELECT users.username, messages.message 
            FROM messages LEFT JOIN users ON users.id = messages.user_id
            WHERE messages.game_id = :game_id
            ORDER BY messages.created_at DESC
        """)
    
    result = db.session.execute(sql, {"game_id":game_id})
    return result.fetchall()
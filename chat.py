from db import db
from sqlalchemy import text

def post_comment(game_id, user_id, message):
    sql = text("""
            INSERT INTO messages (game_id, user_id, message) 
            VALUES (:game_id, :user_id, :message)
        """)
    
    db.session.execute(sql, {"game_id":game_id, "user_id":user_id, "message":message})
    db.session.commit()
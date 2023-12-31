from db import db
from sqlalchemy import text

# POST A MESSAGE
def post_message(game_id, user_id, message):
    sql = text("""
            INSERT INTO messages (game_id, user_id, message) 
            VALUES (:game_id, :user_id, :message)
        """)
    
    db.session.execute(sql, {"game_id":game_id, "user_id":user_id, "message":message})
    db.session.commit()


# GET ALL MESSAGES
def get_messages(game_id, user_id):
    sql = text("""
            SELECT messages.id, users.username, messages.message,
            (SELECT COUNT(messagelikes.message_id) FROM messagelikes WHERE messagelikes.message_id = messages.id) AS likes,
            messagelikes.user_id = :user_id AS liked
            FROM messages
            LEFT JOIN users ON messages.user_id = users.id
            LEFT JOIN messagelikes ON messages.id = messagelikes.message_id AND messagelikes.user_id = :user_id
            WHERE messages.game_id = :game_id
            ORDER BY messages.created_at DESC
        """)
    
    result = db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    return result.fetchall()


# LIKE A MESSAGE
def like_message(message_id, user_id):
    sql = text("""
            INSERT INTO messagelikes (message_id, user_id) 
            VALUES (:message_id, :user_id)
        """)
    
    db.session.execute(sql, {"message_id":message_id, "user_id":user_id})
    db.session.commit()


# UNLIKE A MESSAGE
def unlike_message(message_id, user_id):
    sql = text("""
            DELETE FROM messagelikes
            WHERE message_id = :message_id AND user_id = :user_id
        """)
    
    db.session.execute(sql, {"message_id":message_id, "user_id":user_id})
    db.session.commit()
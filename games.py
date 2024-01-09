"""This module contains functions for games."""

from sqlalchemy import text
from db import db

def get_games(user_id):
    """Get all games."""

    sql = text("""
            SELECT games.id, games.name, games.description, games.image, gamevotes.user_id = :user_id AS voted
            FROM games LEFT JOIN gamevotes ON games.id = gamevotes.game_id AND gamevotes.user_id = :user_id
            ORDER BY name;
        """)

    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


def get_game(game_id, user_id):
    """Get a game by id."""

    sql = text("""
            SELECT games.id, games.name, games.description, games.image, gamevotes.user_id = :user_id AS voted
            FROM games LEFT JOIN gamevotes ON games.id = gamevotes.game_id AND gamevotes.user_id = :user_id
            WHERE games.id = :game_id;
        """)

    result = db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    return result.fetchone()


def get_top3_games():
    """Get the top 3 games."""

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


def vote(game_id, user_id):
    """Vote for a game."""

    sql = text("""
            INSERT INTO gamevotes (game_id, user_id) 
            VALUES (:game_id, :user_id)
        """)

    db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    db.session.commit()

def has_been_voted(game_id, user_id):
    """Check if the user has already voted for the game."""

    sql = text("""
            SELECT game_id
            FROM gamevotes
            WHERE game_id = :game_id AND user_id = :user_id
        """)

    result = db.session.execute(sql, {"game_id":game_id, "user_id":user_id})

    if result.fetchone():
        return True

    return False


def unvote(game_id, user_id):
    """Unvote a game."""

    sql = text("""
            DELETE 
            FROM gamevotes 
            WHERE game_id = :game_id AND user_id = :user_id
        """)

    db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    db.session.commit()

"""This module contains functions for user management."""

import secrets

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

from db import db


def login(username, password):
    """Check if the username and password are correct and log the user in if they are."""

    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return False

    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return True

    return False


def logout():
    """Log the user out."""
    
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]


def signup(username, password):
    """Create a new user and log them in."""

    hash_value = generate_password_hash(password)

    try:
        sql = text("INSERT INTO users (username,password) VALUES (:username,:password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except SystemError:
        return False

    return login(username, password)


def username_available(username):
    """Check if the username is available."""

    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user: 
        return False

    return True


def user_in_db(user_id):
    """Check if the user_id exists in the database."""

    sql = text("SELECT id FROM users WHERE id=:user_id")    
    result = db.session.execute(sql, {"user_id":user_id})
    user = result.fetchone()

    if user: 
        return True

    return False


def user_is_logged_in(user_id):
    """Check if the user is logged in."""

    if user_id and user_in_db(user_id):
        return True

    return False

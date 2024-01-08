from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
import secrets


# LOGIN
def login(username, password): 
        # Create a SQL query to check if the username exists
        sql = text("SELECT id, password FROM users WHERE username=:username")

        # Execute the query
        result = db.session.execute(sql, {"username":username})
        
        # Save the query result in a variable
        user = result.fetchone()    

        # Check if the username exists
        if not user:
            return False
        else:
            # Check if the password is correct
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["username"] = username
                session["csrf_token"] = secrets.token_hex(16)
                return True
            else:
                return False
        

# LOGOUT
def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]


# SIGNUP / CREATE NEW USER
def signup(username, password):
    # Hash the password
    hash_value = generate_password_hash(password)
    
    try:
        # Create a SQL query to insert the new user
        sql = text("INSERT INTO users (username,password) VALUES (:username,:password)")
        
        # Execute the query
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    
    # Log the user in
    return login(username, password)


# CHECK IF USERNAME IS AVAILABLE
def username_available(username):

    # Create a SQL query to check if the username exists
    sql = text("SELECT id FROM users WHERE username=:username")
    
    # Execute the query
    result = db.session.execute(sql, {"username":username})
    
    # Save the query result in a variable
    user = result.fetchone()

    if user:
        return False
    else:
        return True
    

# CHECKS THAT USER IS IN DATABASE
def user_in_db(user_id):
    # Create a SQL query to check if the user_id exists
    sql = text("SELECT id FROM users WHERE id=:user_id")
    
    # Execute the query
    result = db.session.execute(sql, {"user_id":user_id})

    # Save the query result in a variable
    user = result.fetchone()

    if user:
        return True
    else:
        return False
    

# CHECKS THAT USER IS LOGGED IN    
def user_is_logged_in(user_id):
    if user_id and user_in_db(user_id): 
        return True
    else:
        return False
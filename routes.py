"""This file contains all the routes for the application."""

from flask import render_template, request, redirect, session
from app import app
import users
import games
import chats


# ------- PAGE ROUTES -------
@app.route("/")
def index():
    """Render the home page."""
    user_id = session.get("user_id")

    all_games = games.get_games(user_id)
    top3_games = games.get_top3_games()

    return render_template("index.html", games=all_games, top3_games=top3_games)

@app.route("/gamepage/<int:game_id>")
def gamepage(game_id):
    """Render the game page."""
    user_id = session.get("user_id")
    game = games.get_game(game_id, user_id)
    messages = chats.get_messages(game_id, user_id)

    return render_template("gamepage.html", game=game, messages=messages)




# ------- USER SIGNUP/LOGIN/LOGOUT ROUTES -------
@app.route("/login", methods=["GET", "POST"])
def login():
    """Render the login page."""

    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check form is not empty
        if username == "" or password == "":
            return render_template("login.html", error="Please fill in all fields")

        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error="Wrong username or password")


@app.route("/logout")
def logout():
    """Log the user out."""

    users.logout()
    return redirect(request.referrer)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Render the signup page."""

    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_again = request.form["password_again"]

        # Check that username and password are at least 3 characters long
        if len(username) < 3 or len(password) < 3:
            return render_template("signup.html", error="Username and password must be at least 3 characters long")

        # Check that username and password dont exceed 15 and 30 characters respectively
        if len(username) > 15 or len(password) > 30:
            return render_template("signup.html", error="Username must not exceed 15 characters and password must not exceed 30 characters")

        # Check that username is available
        if not users.username_available(username):
            return render_template("signup.html", error="Username already taken")

        # Check that password and password_again match
        if password != password_again:
            return render_template("signup.html", error="Passwords do not match")

        if users.signup(username, password):
            return redirect("/")

        return render_template("error.html", error="Something went wrong :(")




# ------- GAME VOTING ROUTES -------
@app.route("/vote/<int:game_id>", methods=["POST"])
def vote(game_id):
    """Vote for a game."""

    user_id = session.get("user_id")

    # check if user has already voted
    if games.has_been_voted(game_id, user_id):
        return redirect(request.referrer)

    if users.user_is_logged_in(user_id):

        # check for CSRF attack
        if request.form["csrf_token"] != session.get("csrf_token"):
            return render_template("error.html", error="Something went wrong :(")

        games.vote(game_id, user_id)
        return redirect(request.referrer)
    
    return redirect("/login")


@app.route("/unvote/<int:game_id>", methods=["POST"])
def unvote(game_id):
    """Unvote a game."""

    user_id = session.get("user_id")

    if users.user_is_logged_in(user_id):

        # check for CSRF attack
        if request.form["csrf_token"] != session.get("csrf_token"):
            return render_template("error.html", error="Something went wrong :(")

        games.unvote(game_id, user_id)
        return redirect(request.referrer)

    return redirect("/login")




# ------- MESSAGE ROUTES -------
@app.route("/postmessage/<int:game_id>", methods=["POST"])
def postmessage(game_id):
    """Post a message."""

    user_id = session.get("user_id")
    message = request.form["message"]

    if len(message) > 2000:
        return redirect(request.referrer)

    if users.user_is_logged_in(user_id):

        # check for CSRF attack
        if request.form["csrf_token"] != session.get("csrf_token"):
            return render_template("error.html", error="Something went wrong :(")

        chats.post_message(game_id, user_id, message)

        return redirect(request.referrer)

    return redirect("/login")


@app.route("/like/<int:message_id>", methods=["POST"])
def like(message_id):
    """Like a message."""

    user_id = session.get("user_id")

    # check if user has already liked
    if chats.message_has_been_liked(message_id, user_id):
        return redirect(request.referrer)

    if users.user_is_logged_in(user_id):

        # check for CSRF attack
        if request.form["csrf_token"] != session.get("csrf_token"):
            return render_template("error.html", error="Something went wrong :(")

        chats.like_message(message_id, user_id)
        return redirect(request.referrer)

    return redirect("/login")


@app.route("/unlike/<int:message_id>", methods=["POST"])
def unlike(message_id):
    """Unlike a message."""

    user_id = session.get("user_id")

    if users.user_is_logged_in(user_id):

        # check for CSRF attack
        if request.form["csrf_token"] != session.get("csrf_token"):
            return render_template("error.html", error="Something went wrong :(")

        chats.unlike_message(message_id, user_id)
        return redirect(request.referrer)

    return redirect("/login")



# ------- ERROR ROUTES -------
@app.route("/error")
def error():
    """Render the error page."""
    
    return render_template("error.html", error="Something went wrong :(")

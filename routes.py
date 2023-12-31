from app import app
from flask import render_template, request, redirect, session
import users
import games
import chats


# ------- PAGE ROUTES -------
# HOME PAGE
@app.route("/")
def index():
    user_id = session.get("user_id")

    all_games = games.get_games(user_id)
    top3_games = games.get_top3_games()

    return render_template("index.html", games=all_games, top3_games=top3_games)

# GAME PAGE
@app.route("/gamepage/<int:game_id>")
def gamepage(game_id):
    user_id = session.get("user_id")
    game = games.get_game(game_id, user_id)
    messages = chats.get_messages(game_id)

    return render_template("gamepage.html", game=game, messages=messages)




# ------- USER SIGNUP/LOGIN/LOGOUT ROUTES -------
# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
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


# LOGOUT
@app.route("/logout")
def logout():
    users.logout()
    return redirect(request.referrer)


# SIGNUP PAGE
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_again = request.form["password_again"]

        # Check that username and password are at least 3 characters long
        if len(username) < 3 or len(password) < 3:
            return render_template("signup.html", error="Username and password must be at least 3 characters long")

        # Check that username is available
        if not users.username_available(username):
            return render_template("signup.html", error="Username already taken")

        # Check that password and password_again match
        if password != password_again:
            return render_template("signup.html", error="Passwords do not match")

        if users.signup(username, password):
            return redirect("/")
        else:
            return render_template("error.html", error="Something went wrong :(")




# ------- GAME VOTING ROUTES -------
# VOTE A GAME
@app.route("/vote/<int:game_id>", methods=["POST"])
def vote(game_id):
    user_id = session.get("user_id")

    # check if user is logged in
    if not user_id:
        return redirect("/login")
    
    # check if user is in db
    if not users.user_in_db(user_id):
        return redirect("/login")
    
    # check if user has already voted
    if games.has_been_voted(game_id, user_id):
        return redirect(request.referrer)
    
    games.vote(game_id, user_id)
    return redirect(request.referrer)


# UNVOTE A GAME
@app.route("/unvote/<int:game_id>", methods=["POST"])
def unvote(game_id):
    user_id = session.get("user_id")

    # check if user is logged in
    if not user_id:
        return redirect("/login")
    
    # check if user is in db
    if not users.user_in_db(user_id):
        return redirect("/login")
    
    games.unvote(game_id, user_id)
    return redirect(request.referrer)



# ------- GAME COMMENTING ROUTES -------
# COMMENT A GAME
@app.route("/postmessage/<int:game_id>", methods=["POST"])
def postmessage(game_id):
    user_id = session.get("user_id")

    # check if user is logged in
    if not user_id:
        return redirect("/login")
    
    # check if user is in db
    if not users.user_in_db(user_id):
        return redirect("/login")
    
    message = request.form["message"]
    chats.post_message(game_id, user_id, message)
    return redirect(request.referrer)
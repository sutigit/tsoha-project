from app import app
from flask import render_template, request, redirect
import users
import games

# HOME PAGE
@app.route("/")
def index():
    all_games = games.get_games()
    leader_games = games.get_games()
    # leader_games = games.get_leader_games()

    return render_template("index.html", games=all_games, leader_games=leader_games)

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
    return redirect("/")



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



# GAME PAGE
@app.route("/gamepage")
def gamepage():
    return render_template("gamepage.html")
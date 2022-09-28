from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Create Flask App object
app = Flask(__name__)

# This allows templates to auto reload when their content are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session
app.config["SESSION_PERMANENT"] = False
# Use the server's filesystem to track the user's session (rather than signed cookies)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Connect to local sqlite database using cs50 library
db = SQL("sqlite:///birthdaytracker.db")

# Create db tables 
db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);")

db.execute("CREATE TABLE IF NOT EXISTS birthdays (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, month INTEGER NOT NULL, day INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(user_id));")

db.execute("CREATE INDEX IF NOT EXISTS birthdays_by_user_id_index ON birthdays (user_id);")                               


# Define route for login page
@app.route("/login", methods=["GET","POST"])
def login():
    # Ensure that session is not remembering some previous user
    session.clear()
    # If user reached this route via POST (via submitting a form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        users_rows = db.execute("SELECT * FROM users WHERE username = ?",
                                 request.form.get("username"))

        # Ensure username exists and password is correct
        if len(users_rows) != 1 or not check_password_hash(users_rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = users_rows[0]["user_id"]
        session["username"] = users_rows[0]["username"]

        # If everything checks out, user has successfully logged in, so redirect the user to the main page
        return redirect("/")
    """ If user reached this route via GET (via typing in the URL, clicking a link,
        or via some redirect (such as by clicking the logout button),
        render the login page """
    if request.method == "GET":
        return render_template("login.html")


# Define route for logging out
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login route
    return redirect("/login")


# Define route for registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    """" If user requests the registration page via get (via the button on the 
         login page) display the registration form; this is simply if they are
         requesting to load the page """
    if request.method == "GET":
        return render_template("register.html")
    # If user requests via POST, meaning they've submitted the form
    if request.method == "POST":
        """ Request the data that was submitted into the form from html and store
            it in python variables; the parameter on this get method corresponds 
            to the name attribute on the input element """
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Error checks on the form
        # I'm gonna make up some error codes for fun
        if username == "" or password == "" or confirmation == "":
            return apology("Dude you left one or more of the fields blank. Go do it again.", 999)
        if password != confirmation:
            return apology("The passwords you entered didn't match dude. Do it again.", 998)
        if len(db.execute("SELECT username FROM users WHERE username = ?", username)) > 0:
            return apology("The username that you entered has already been taken! Try a different username please!", 997)
        # Assuming we made it past the error checks, enter information for user's newly created account into our database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
        # Query database for username
        users_rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Get user info from database into session dictionary
        session["user_id"] = users_rows[0]["user_id"]
        session["username"] = username
        # Redirect user to main page
        return redirect("/")


# Define main app page (index.html)
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    current_user_id = session.get("user_id")
    current_username = session.get("username")

    # User is accessing page via GET, meaning they are logged in and are simply viewing their entries
    if request.method == "GET":
        # Query for all birthdays
        birthdays_rows = db.execute("SELECT name, month, day, id FROM birthdays WHERE user_id = ?", current_user_id)
        # Render birthdays page
        return render_template("index.html", birthdays=birthdays_rows)

    # This handles adding a new entry
    if request.method == "POST":
        # Request form data from user into flask backend 
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        # Insert the user's entry into the database
        db.execute("INSERT INTO birthdays (user_id, name, month, day) VALUES(?, ?, ?, ?)", current_user_id, name, month, day)
        # Reloads the page with new entry
        return redirect("/")


# Define route for deleting entry
@app.route("/deleteEntry", methods=["POST"])
@login_required
def deleteEntry():
    entry_id = request.form.get("entry_id")
    if entry_id:
        db.execute("DELETE FROM birthdays WHERE id = ?", entry_id)
    return redirect("/")










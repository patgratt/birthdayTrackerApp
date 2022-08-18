from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# Create Flask App
app = Flask(__name__)

""" This allows templates to auto reload when their content are changed """
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session
app.config["SESSION_PERMANENT"] = False
""" Use the server's filesystem to track the user's session """
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to local sqlite database using cs50 library
db = SQL("sqlite:///birthdays.db")

# Define route for login page
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
          session["username"] = request.form.get("username")
          return redirect("/")
    return render_template("login.html")


# Define default route - main page (index.html)
@app.route("/", methods=["GET", "POST"])
def index():
    """ If we can't find a username, the user has not logged in, so redirect to the 
        sign in page """
    if not session.get("username"):
        return redirect("/login")

    if request.method == "POST":
        # Request form data from user into flask backend
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Insert the user's entry into the database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        # Go back to homepage
        return redirect("/")

    else:

        # Query for all birthdays
        birthdays = db.execute("SELECT * FROM birthdays")

        # Render birthdays page
        return render_template("index.html", birthdays=birthdays)


# Define route for deleting entry
@app.route("/deleteEntry", methods=["POST"])
def deleteEntry():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")


# Define route for logging out
@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")

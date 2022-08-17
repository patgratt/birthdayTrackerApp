from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Create Flask App
app = Flask(__name__)

# This allows templates to auto reload when their content are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Connects local sqlite database using cs50 library
db = SQL("sqlite:///birthdays.db")

# Login page
"""
@app.route("/login")
def login():
    if request.method == "POST":
"""

# Define primary route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Request form data from user into flask backend
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Insert the user's entry into the database
        db.execute("INSERT INTO birthdays name, month, day) VALUES(?, ?, ?)", name, month, day)

        # Go back to homepage
        return redirect("/")

    else:

        # Query for all birthdays
        birthdays = db.execute("SELECT * FROM birthdays")

        # Render birthdays page
        return render_template("index.html", birthdays=birthdays)

@app.route("/deleteEntry", methods=["POST"])
def deleteEntry():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")


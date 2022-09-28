from flask import session, redirect, render_template
from functools import wraps


# Render message as an apology to user.
def apology(message, code=400):
    return render_template("apology.html", top=code, bottom=message)


# Decorate routes to require login - https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

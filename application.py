from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from oauth2client import client, crypt
from tempfile import gettempdir
from datetime import datetime

import seed

from helpers import *

CLIENT_ID = "1024412823571-9489vhkoanksm77ntqsste037572j8o2.apps.googleusercontent.com"

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd


# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():

    return render_template(
        'index.html', savings = seed.make_savings(),
                      mutual_fund = seed.make_mutual_fund(),
                      money_market = seed.make_money_market(),
                      bond = seed.make_bond())


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        id_token = request.form.get("idtoken")

        # (Receive token by HTTPS POST)

        try:
            idinfo = client.verify_id_token(id_token, CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

        except crypt.AppIdentityError:
            # Invalid token

            return "error"

        # remember which user has logged in
        session["user_id"] = idinfo["sub"]
        session["email"] = idinfo["email"]
        session["name"] = idinfo["name"]
        session["picture"] = idinfo["picture"]

        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

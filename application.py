from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from oauth2client import client, crypt
from tempfile import gettempdir
from datetime import datetime

import seed
import interface

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
                      bond = seed.make_bond(),
                      compound_deposit = seed.make_compound_deposit(),
                      horse_racing = seed.make_horse_racing(),
                      cash = interface.get_cash(session["user_id"]))

@app.route("/transactions")
@login_required
def transactions():

    return render_template(
        'transactions.html',
        transactions = interface.get_transactions(session["user_id"])
    )

@app.route("/savings", methods=["POST"])
@login_required
def savings():

    name = request.args.get("name")
    rate = float(request.args.get("rate"))
    amount = float(request.form.get("amount"))

    result = interface.create_savings(session["user_id"], name, rate, amount)

    try:

        message = result["message"]

        return render_template("error.html", message = message)

    except KeyError:

        return redirect(url_for("index"))

@app.route("/mutual_fund", methods=["POST"])
@login_required
def mutual_fund():

    name = request.args.get("name")
    price = float(request.args.get("price"))
    shares = int(request.form.get("shares"))

    result = interface.create_mutual_fund(session["user_id"], name, price, shares)

    try:

        message = result["message"]

        return render_template("error.html", message=message)

    except KeyError:

        return redirect(url_for("index"))

@app.route("/bond", methods=["POST"])
@login_required
def bond():

    name = request.args.get("name")
    rate = float(request.args.get("rate"))
    risk = float(request.args.get("risk"))
    amount = int(request.args.get("amount"))
    duration = int(request.args.get("duration"))

    result = interface.create_bond(session["user_id"], name, rate, risk, amount, duration)

    try:

        message = result["message"]

        return render_template("error.html", message=message)

    except KeyError:

        return redirect(url_for("index"))


@app.route("/money_market", methods=["POST"])
@login_required
def money_market():

    name = request.args.get("name")
    rate = float(request.args.get("rate"))
    risk = float(request.args.get("risk"))
    amount = float(request.form.get("amount"))

    if amount < 2000:

        return render_template("error.html", message="Minimum investment is $2000.")

    result = interface.create_money_market(session["user_id"], name, rate, amount, risk)

    try:

        message = result["message"]

        return render_template("error.html", message = message)

    except KeyError:

        return redirect(url_for("index"))

@app.route("/manage", methods=["GET", "POST"])
@login_required
def manage():

    if request.method == "GET":

        return render_template("manage.html",
                            accounts=interface.get_accounts(session["user_id"]))

    else:

        account_id = request.args.get("account_id")
        maturation_value = float(request.args.get("maturation_value"))
        mature = request.args.get("mature")
        risk = float(request.args.get("risk"))

        if risk > 0.5:

            interface.delete_account(session["user_id"], account_id)

            return render_template("crash.html", message="Money market account crashed.")

        if bool(mature):

            interface.add_cash(session["user_id"], maturation_value)

            interface.delete_account(session["user_id"], account_id)

            return redirect(url_for("index"))


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

        interface.initialize_user(session["user_id"])

        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

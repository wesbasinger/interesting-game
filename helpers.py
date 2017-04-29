from flask import redirect, render_template, request, session, url_for
from functools import wraps

from yahoo_finance import Share

import datetime

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    """Formats value as USD."""
    return "${:,.2f}".format(value)

def percent(value):
    """Formats value as percent."""
    return "{:,.3f}%".format(value)

def get_stock_index():

    yahoo = Share("^GSPC")

    return float(yahoo.get_price())

def calculate_compound_interest(principal, rate, time):

    return principal * (1 + rate / 100.00) ** time

def elapsed_hours(previous_timestamp):

    previous = datetime.datetime.strptime(previous_timestamp, '%Y-%m-%d %H:%M:%S')

    now = datetime.datetime.now()

    td = now - previous

    return td.total_seconds() / 3600

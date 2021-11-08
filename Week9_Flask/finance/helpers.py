import os
import requests
import urllib.parse

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def get_available_shares(user_id, symbol):
    # Calculate the buy total shares.
    buy_row = db.execute(
        "SELECT SUM(shares) AS buy_shares, name FROM history WHERE user_id = ? AND symbol = ? AND transaction_type = 'buy'", user_id, symbol)[0]
    buy_shares = buy_row["buy_shares"]
    buy_shares = 0 if not buy_shares else buy_shares
    name = buy_row["name"]

    # Calculate the buy sell shares.
    sell_row = db.execute(
        "SELECT SUM(shares) AS sell_shares FROM history WHERE user_id = ? AND symbol = ? AND transaction_type = 'sell'", user_id, symbol)[0]
    sell_shares = sell_row["sell_shares"]
    sell_shares = 0 if not sell_shares else sell_shares

    # Calculate the total shares.
    available_shares = buy_shares + sell_shares if buy_shares > 0 else null

    return {
        "symbol": symbol,
        "name": name,
        "available_shares": available_shares
    }


def get_symbols(user_id):
    return db.execute("SELECT DISTINCT symbol FROM history WHERE user_id = ?", user_id)
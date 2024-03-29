import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Store the user_id.
    user_id = session["user_id"]

    # Get the existing symbols.
    symbol_rows = get_symbols(user_id)

    rows = []
    total_portfolio_value = 0

    if len(symbol_rows) > 0:

        # Calculate the shares and price for each symbol.
        for symbol_row in symbol_rows:
            symbol = symbol_row["symbol"]
            shares_and_price = get_available_shares(user_id, symbol)
            # Lookup the stock symbol by calling the lookup function.
            result = lookup(symbol)
            # Calculate the total price.
            available_shares = shares_and_price["available_shares"]
            price = result["price"]
            total_amount = price * available_shares
            total_portfolio_value = total_portfolio_value + total_amount

            if available_shares > 0:
                rows.append({
                    "symbol": symbol,
                    "name": shares_and_price["name"],
                    "shares": shares_and_price["available_shares"],
                    "price": usd(price),
                    "total": usd(total_amount)
                })

    # Get the current cash value.
    cash = get_cash(user_id)
    # Add current cash row.
    rows.append({
        "symbol": "CASH",
        "name": "",
        "shares": "",
        "price": "",
        "total": usd(cash)
    })

    # Calculate the total portfolio value.
    total_portfolio_value = usd(total_portfolio_value + cash)

    # # Get the most recent transaction.
    recent_transaction_row = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY transacted DESC LIMIT 1", user_id)

    # Construct message.
    if len(recent_transaction_row) > 0:
        recent_transaction = recent_transaction_row[0]
        verb = "Bought" if recent_transaction["transaction_type"] == "buy" else "Sold"
        message = "%s %d %s stock share(s) for %s" % (
            verb, recent_transaction["shares"], recent_transaction["symbol"], usd(recent_transaction["price"]))
    else:
        message = ""

    # Render the home template.
    return render_template("home.html", rows=rows, total_portfolio_value=total_portfolio_value, message=message)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Store the user_id.
        user_id = session["user_id"]

        # Ensure symbol was submitted.
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        # Ensure shares count was submitted.
        if not request.form.get("shares"):
            return apology("must provide shares")

        # Ensure that the correct input is passed in shares.
        shares = request.form.get("shares")
        if not shares.isnumeric() or int(shares) <= 0:
            return apology("shares input is not a positive integer")

        num_shares = int(shares)

        # Lookup the stock symbol by calling the lookup function.
        result = lookup(symbol)
        symbol = symbol.upper()

        # Ensure that the stock data is valid.
        if not result:
            error_msg = "no results found for the symbol, '%s'" % symbol
            return apology(error_msg)

        # Query the database for the cash.
        cash = get_cash(user_id)

        # Calculate the total cost of the stocks.
        price = result["price"]
        total_cost = price * num_shares

        # Ensure that the user has enough money to buy the stock.
        if total_cost > cash:
            error_msg = "not enough money ($%d) to buy %d shares of the %s stock" % (cash, num_shares, symbol)
            return apology(error_msg)

        leftover_cash = cash - total_cost
        name = result["name"]

        # Purchase the stock and update the tables in the database.
        db.execute("INSERT INTO history (user_id, symbol, name, transaction_type, shares, price) VALUES(?, ?, ?, ?, ?, ?)",
                   user_id, symbol, name, "buy", num_shares, total_cost)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", leftover_cash, user_id)

        # Redirect the user back to the index page.
        return redirect("/")

    else:
        # When requested via GET, should display form to request a stock buy.
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Store the user_id.
    user_id = session["user_id"]

    # Query database to get the history
    rows = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY transacted DESC", user_id)

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        if len(rows) > 0:
            session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        # When form is submitted via POST, , and display the results.

        # Ensure quote was submitted.
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide quote")

        # Lookup the stock symbol by calling the lookup function.
        result = lookup(symbol)

        if not result:
            error_msg = "no results found for the symbol, '%s'" % symbol
            return apology(error_msg)

        result["price"] = usd(result["price"])

        return render_template("quoted.html", result=result)

    else:
        # When requested via GET, should display form to request a stock quote.
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted.
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted.
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure confirm password was submitted.
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Query database for username.
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure that a user with the same username does not exist in the database.
        if len(rows) > 0:
            error_msg = "user with the username, '%s' already exists" % username
            return apology(error_msg)

        # Validate the password to have at least 2 letters, no spaces, at least 1 number, and at least 1 symbol.
        pwd = request.form.get("password")
        check_number = False
        check_symbol = False
        space_check = False
        num_letters = 0
        for c in pwd:
            if c.isalpha():
                num_letters = num_letters + 1
            if c.isdigit() and not check_number:
                check_number = True
            if c.isspace() and not space_check:
                space_check = True
            if not c.isalnum() and not c.isspace():
                check_symbol = True
        if not check_number:
            return apology("password must contain a number")
        if num_letters < 2:
            return apology("password must contain at least 2 letters")
        if not check_symbol:
            return apology("password must contain at least 1 symbol / special character")
        if space_check:
            return apology("password must not have any spaces")

        # Insert the user into the database.
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(pwd))

        # Query for the user in the DB to get the id.
        new_user_rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(new_user_rows) > 0:
            session["user_id"] = new_user_rows[0]["id"]

        # # Redirect user to the login page.
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Store the user_id.
    user_id = session["user_id"]

    if request.method == "POST":

        # Ensure symbol was submitted.
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")

        # Calculate available shares.
        available_shares = get_available_shares(user_id, symbol)["available_shares"]

        # Check if shares are available to sell.
        if not available_shares or available_shares == 0:
            error_msg = "no shares found for the stock symbol, '%s' to sell" % symbol
            return apology(error_msg)

        # Ensure that the correct input is passed in shares.
        shares = request.form.get("shares")
        if not shares.isnumeric() or int(shares) <= 0:
            return apology("shares input is not a positive integer")

        num_shares = int(shares)

        # Check if user tries to sell more shares than what is available.
        if num_shares > available_shares:
            error_msg = "user does not own %d shares of the %s stock to sell" % (num_shares, symbol)
            return apology(error_msg)

        # Lookup the stock symbol by calling the lookup function.
        result = lookup(symbol)

        # Calculate the new total of the stock share based on current data.
        price = result["price"]
        total_amount = price * num_shares

        # Query the database for the cash.
        cash = get_cash(user_id)
        new_total_cash = cash + total_amount

        # Sell the stock and update the tables in the database.
        db.execute("INSERT INTO history (user_id, symbol, name, transaction_type, shares, price) VALUES(?, ?, ?, ?, ?, ?)",
                   user_id, symbol.upper(), result["name"], "sell", -abs(num_shares), total_amount)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_total_cash, user_id)

        # Redirect the user back to the index page.
        return redirect("/")

    else:
        # Get the existing symbols.
        symbols = get_symbols(user_id)

        if len(symbols) == 0:
            return apology("No stock shares to sell")

        # When requested via GET, should display form to sell existing stock shares.
        return render_template("sell.html", symbols=symbols)


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


def get_cash(user_id):
    return db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]


def get_symbols(user_id):
    return db.execute("SELECT DISTINCT symbol FROM history WHERE user_id = ?", user_id)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

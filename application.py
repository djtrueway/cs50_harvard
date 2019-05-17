import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    if request.method == "GET":
        user_id = session['user_id']
        cash = db.execute("SELECT cash FROM users where id = :id", id=user_id)

        histories = db.execute(
            "SELECT symbol, SUM(shares) as total_p FROM histories WHERE id = :id GROUP BY symbol HAVING total_p > 0", id=user_id)
        if histories == None:
            return render_template("index.html", cash=cash)
        else:
            stock = {}
            for history in histories:
                symbol = str(history['symbol'])
                shares = int(history['total_p'])
                quote = lookup(symbol)
                name = ""
                price = ""
                quantity = ""
                total = ""
                history['quantity'] = shares
                history["name"] = quote["name"]
                history["prix"] = usd(quote["price"])
                history["total"] = usd(quote["price"] * shares)

            return render_template("index.html", cash=cash, histories=histories)
    else:

        return apology("POST")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        if not request.form['symbol']:
            return apology("give a symbol!")

        quote = request.form['symbol']

        symbol = lookup(quote)

        if not symbol:
            return apology("bad symbol")

        try:
            share = int(request.form['shares'])
        except:
            return apology('bad digit')

        if share <= 0:
            return apology("give a number positive")

        conn = sqlite3.connect("finance.db")
        db = conn.cursor()

        id = int(session['user_id'])
        money = db.execute("SELECT cash FROM users WHERE id = ?", (id, ))
        money = money.fetchone()

        # if the user don't have enough cash
        if not money or int(money[0]) < symbol["price"] * share:
            return apology("Not enough money")

        sym = symbol["symbol"]
        share = request.form['shares']
        price = round(float(symbol["price"]), 2)
        user_id = session['user_id']
        t = symbol["price"] * int(share)
        # add stuff in the table history

        db.execute("INSERT INTO histories (symbol, shares, price, id) VALUES(?,?,?,?)",
                   (sym, share, price, user_id))
        conn.commit()

        db.execute("UPDATE users SET cash = cash - ?  WHERE id=? ", (t, user_id,))
        conn.commit()

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session['user_id']

    histories = db.execute("SELECT * FROM histories where id= :id", id=user_id)

    if histories == None:
        return render_template("index.html")
    else:
        return render_template("histories.html", histories=histories)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
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
    if request.method == "GET":
        return render_template('quote.html')
    else:
        q = request.form.get('symbol')
        quote = lookup(q)
        if not quote:
            return apology('bad symbol')
        return render_template("quoted.html", quote=quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    else:

        if request.form.get('username') and request.form.get('password') and request.form.get('confirmation'):

            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            if password == confirmation:
                hash = generate_password_hash(password)

                result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                    username=request.form.get("username"), hash=hash)
                if result:
                    rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

                    session["user_id"] = rows[0]["id"]

                    flash('Successfully registered!')

                    return redirect("/")
                else:
                    return apology("problem or username already exist")
            else:
                return apology("password dont macht")

        else:
            return apology("please submit the form")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        list = []
        user_id = session['user_id']

        sell = db.execute(
            "SELECT symbol, SUM(shares) as total_p FROM histories WHERE id = :id GROUP BY symbol HAVING total_p > 0", id=user_id)
        return render_template("sell.html", sell=sell)
    else:
        user_id = session['user_id']
        sell = request.form.get('symbol')
        shares1 = int(request.form.get('shares'))
        if shares1 <= 0:
            return apology('share cant < 0')

        negative = -(shares1)
        lookup_items = lookup(sell)

        portfolio = db.execute("SELECT shares, SUM(shares) FROM histories WHERE id = :id AND symbol = :sym", id=user_id, sym=sell)

        if not portfolio:
            return apology("you don't own any of this stock")
        if shares1 > portfolio[0]['SUM(shares)']:
            share = portfolio[0]['SUM(shares)']
            return apology(f"you don't have enought shares: {share}")

        price = round(float(lookup_items["price"]), 2)
        total = round(float(shares1 * price), 2)

        sym = lookup_items["symbol"]

        if sym and shares1:

            db.execute("INSERT INTO histories (symbol, shares, price, id) VALUES(:symbol,:shares,:price,:id)",
                       symbol=sell, shares=negative, price=price, id=user_id)

            db.execute("UPDATE users SET cash = cash + :price  WHERE id=:id ", price=total, id=user_id)

            flash('Sold!')
            return redirect('/')
        else:
            return apology('missin something')


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit cash into account."""

    # if user reached route via GET, return deposit page
    if request.method == "GET":
        return render_template("deposit.html")

    # if user reached via POST i.e. submitting form, check that the form is valid
    elif request.method == "POST":
        if not request.form.get("amount"):
            return apology("must provide amount")
        if not request.form.get("amount").isdigit():
            return apology("must provide positive integer")

        # update user's cash amount
        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :id",
                   amount=request.form.get("amount"), id=session["user_id"])
        flash("Successfully deposited cash!")

        return redirect('/')


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

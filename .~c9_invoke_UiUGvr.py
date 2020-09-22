import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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
    rows = db.execute("SELECT * FROM buy WHERE id_buy = :iduser", iduser= session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :iduser", iduser= session["user_id"])[0]["cash"]
    total = 0
    for row in rows:
        total = total + (row["shares"] * row["price"])

    return render_template("index.html", rows=rows, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # If the user send a request
    if request.method == "POST":
        if not lookup(request.form.get("symbol")):
            return apology("invalid symbol")
        elif not request.form.get("shares") or int(request.form.get("shares")) < 0:
            return apology("put a positive number")
        elif db.execute("SELECT cash FROM users WHERE id = :iduser", iduser=session["user_id"])[0]["cash"] < lookup(request.form.get("symbol"))["price"] * int(request.form.get("shares")):
            return apology("can't affrod")
        else:
            sym = db.execute("SELECT shares FROM buy WHERE id =:userid AND symbol =:symbol", iduser=session["user_id"], symbol=lookup(request.form.get("symbol")))
            if len(sym) != 1:
                db.execute("INSERT INTO buy VALUES (:id_buy, :symbol, :name, :shares, :price, datetime('now'))", id_buy=session["user_id"], symbol=lookup(request.form.get("symbol"))["symbol"], name= lookup(request.form.get("symbol"))["name"], shares=int(request.form.get("shares")), price=lookup(request.form.get("symbol"))["price"])
            else:
                db.execute("UPDATE buy SET shares=:add WHERE id= :iduser;", add=, iduser=session["user_id"])
                shares = sym[0][]
            cash = db.execute("SELECT cash FROM users WHERE id = :iduser", iduser=session["user_id"])[0]["cash"]
            rest = cash - (lookup(request.form.get("symbol"))["price"] * int(request.form.get("shares")))
            db.execute("UPDATE users SET cash=:rest WHERE id= :iduser;", rest=rest, iduser=session["user_id"])
            #TODO bought
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
    if request.method == "POST":
        if not lookup(request.form.get("symbol")):
            return apology("invalid symbol", 400)
        else:
            return render_template("quoted.html", name=lookup(request.form.get("symbol"))["name"], price=lookup(request.form.get("symbol"))["price"], symbol=lookup(request.form.get("symbol"))["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        #Ensure username was submitted
        if not request.form.get ("username"):
            return apology("must provide username", 403)

        #Ensure password was submitted
        elif not request.form.get ("password"):
            return apology("must provide password", 403)

        #Ensure confirm password was submitted
        elif not request.form.get ("confirmpassword"):
            return apology("must confirm password", 403)

        #Ensure password and confirm password are same
        elif request.form.get ("confirmpassword") != request.form.get ("password"):
            return apology("passwords don't match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        #Ensure that username not exist on database
        if len(rows) == 1:
            return apology("username is taken", 400)

        #Save the username and the hash password into user table
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=request.form.get ("username"), password=generate_password_hash(request.form.get ("confirmpassword")))
        return redirect("/")
    else:
        return render_template ("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("missing a symbol")
        elif not request.form.get ("shares"):
            return apology("messing a shares")
        elif int(request.form.get ("shares")):
            return apology("put a positive number")
        else:
            
    else:
        return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

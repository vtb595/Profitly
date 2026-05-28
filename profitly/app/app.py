from flask import Flask, render_template, request, redirect
import psycopg2
import yfinance as yf
import re

app = Flask(__name__)

# DATABASE CONNECTION
conn = psycopg2.connect(
    host="db",
    database="profitly",
    user="postgres",
    password="password"
)

# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # REGEX VALIDATION
        username_pattern = r"^[a-zA-Z0-9_]+$"

        if not re.match(username_pattern, username):
            return "Invalid username"

        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()

        if user:
            return redirect(f"/dashboard/{user[0]}")

    return render_template("login.html")


# DASHBOARD PAGE
@app.route("/dashboard/<user_id>")
def dashboard(user_id):

    cur = conn.cursor()

    cur.execute(
        "SELECT ticker, shares FROM portfolio WHERE user_id=%s",
        (user_id,)
    )

    portfolio = cur.fetchall()

    stocks = []

    total_value = 0

    for stock in portfolio:

        ticker = stock[0]
        shares = stock[1]

        yf_stock = yf.Ticker(ticker)

        try:
            price = yf_stock.info.get("currentPrice", 0)
        except:
            price = 0

        position_value = shares * price

        total_value += position_value

        stocks.append({
            "ticker": ticker,
            "shares": shares,
            "price": round(price, 2),
            "value": round(position_value, 2)
        })

    # DYNAMIC CHART DATA
    chart_data = [
        round(total_value * 0.45, 2),
        round(total_value * 0.52, 2),
        round(total_value * 0.49, 2),
        round(total_value * 0.58, 2),
        round(total_value * 0.55, 2),
        round(total_value * 0.63, 2),
        round(total_value * 0.72, 2),
        round(total_value * 0.70, 2),
        round(total_value * 0.78, 2),
        round(total_value * 0.85, 2),
        round(total_value * 0.94, 2),
        round(total_value, 2)
    ]

    return render_template(
        "dashboard.html",
        stocks=stocks,
        total_value=round(total_value, 2),
        chart_data=chart_data
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


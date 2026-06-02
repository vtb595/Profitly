from flask import Flask, render_template, request, redirect
import psycopg2
import yfinance as yf
import re
from datetime import datetime

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="db",
        database="profitly",
        user="postgres",
        password="password"
    )

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        username_pattern = r"^[a-zA-Z0-9_]+$"

        if not re.match(username_pattern, username):
            return "Invalid username"

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return redirect(f"/dashboard/{user[0]}")

    return render_template("login.html")


@app.route("/dashboard/<user_id>")
def dashboard(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT ticker, shares FROM portfolio WHERE user_id=%s",
        (user_id,)
    )

    portfolio = cur.fetchall()

    stocks = []

    total_value = 0
    portfolio_today = 0
    portfolio_yesterday = 0

    for stock in portfolio:

        ticker = stock[0]
        shares = stock[1]

        try:

            yf_stock = yf.Ticker(ticker)

            info = yf_stock.fast_info

            current_price = info["lastPrice"]
            previous_close = info["previousClose"]

        except:

            current_price = 0
            previous_close = 0

        position_value = shares * current_price

        total_value += position_value

        portfolio_today += shares * current_price
        portfolio_yesterday += shares * previous_close

        stocks.append({
            "ticker": ticker,
            "shares": shares,
            "price": round(current_price, 2),
            "value": round(position_value, 2)
        })

    if portfolio_yesterday > 0:

        daily_change = round(
            (
                (portfolio_today - portfolio_yesterday)
                / portfolio_yesterday
            ) * 100,
            2
        )

    else:
        daily_change = 0

    hour = datetime.utcnow().hour

    if 13 <= hour <= 20:
        market_status = "Open"
    else:
        market_status = "Closed"

    try:

        sp500 = yf.Ticker("^GSPC")
        sp_info = sp500.fast_info

        sp500_change = round(
            (
                (sp_info["lastPrice"]
                 - sp_info["previousClose"])
                / sp_info["previousClose"]
            ) * 100,
            2
        )

    except:
        sp500_change = 0

    try:

        nasdaq = yf.Ticker("^IXIC")
        nd_info = nasdaq.fast_info

        nasdaq_change = round(
            (
                (nd_info["lastPrice"]
                 - nd_info["previousClose"])
                / nd_info["previousClose"]
            ) * 100,
            2
        )

    except:
        nasdaq_change = 0

    watchlist_tickers = [
        "AAPL",
        "NVDA",
        "TSLA",
        "META"
    ]

    watchlist = []

    for ticker in watchlist_tickers:

        try:

            ticker_obj = yf.Ticker(ticker)

            info = ticker_obj.fast_info

            change = round(
                (
                    (info["lastPrice"]
                     - info["previousClose"])
                    / info["previousClose"]
                ) * 100,
                2
            )

        except:

            change = 0

        watchlist.append({
            "ticker": ticker,
            "change": change
        })

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

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        stocks=stocks,
        total_value=round(total_value, 2),
        chart_data=chart_data,
        daily_change=daily_change,
        market_status=market_status,
        sp500_change=sp500_change,
        nasdaq_change=nasdaq_change,
        watchlist=watchlist
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


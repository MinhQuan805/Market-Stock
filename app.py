import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, session, flash
from flask_session import Session
from datetime import datetime
from helpers import apology
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def validate(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    df = yf.Ticker("AAPL")
    time = "6mo"
    start_input = None
    end_input = None
    error = None
    information = df.info
    if request.method == "POST":
        time = request.form.get("time")
        start_input = request.form.get("start_input")
        end_input = request.form.get("end_input")
        if start_input and not validate(start_input):
            return apology("Invalid Start Date", 400)
        elif end_input and not validate(end_input):
            return apology("Invalid End Date", 400)
    if start_input and end_input:
        hist = df.history(start=start_input, end=end_input, interval="1d")
        start_date = start_input
        end_date = end_input
    else:
        hist = df.history(period=time, interval="1d")
        start_date = hist.index.min().strftime('%Y-%m-%d')
        end_date = hist.index.max().strftime('%Y-%m-%d')

    hist = hist.round(2)

    if isinstance(hist.index, pd.DatetimeIndex):
        hist.index = hist.index.strftime('%Y-%m-%d')

    data = hist.reset_index().to_dict("records")[::-1]
    return render_template("index.html", value=data, infor=information, start=start_date, end=end_date, error=error)


if __name__ == "__main__":
    app.run(debug=True)

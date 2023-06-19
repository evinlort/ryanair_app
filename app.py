from datetime import date, datetime, timedelta

from flask import Flask, render_template, request

from rair import RAir

app = Flask(__name__)


@app.route("/")
def start_page():
    params = {
        "today_date": date.today(),
    }
    return render_template('start.html', params=params)


@app.route("/", methods=["POST"])
def receive_data_from_page():
    ra = RAir(**request.form)
    all_trips = ra.get_flights()

    return render_template('response.html', trips=all_trips)


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)


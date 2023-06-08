from datetime import date

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
    from_preferred_departure_time = int(request.form["from_preferred_departure_time"]) if request.form["from_preferred_departure_time"] else 0
    from_preferred_departure_time_2 = int(request.form["from_preferred_departure_time_2"]) if request.form["from_preferred_departure_time_2"] else 0
    to_preferred_departure_time = int(request.form["to_preferred_departure_time"]) if request.form["to_preferred_departure_time"] else 0
    to_preferred_departure_time_2 = int(request.form["to_preferred_departure_time_2"]) if request.form["to_preferred_departure_time_2"] else 0
    max_sum = float(request.form["max_sum"]) if request.form["max_sum"] else 0
    # days_length = int(request.form["days_length"]) if request.form["days_length"] else 0
    trip_min_days = int(request.form["trip_min_days"]) if request.form["trip_min_days"] else 0
    trip_max_days = int(request.form["trip_max_days"]) if request.form["trip_max_days"] else 0
    trips = []
    all_trips = ra.get_flights()
    for trip in all_trips:
        if from_preferred_departure_time and trip.outbound.departureTime.hour <= from_preferred_departure_time:
            continue
        if from_preferred_departure_time_2 and trip.outbound.departureTime.hour > from_preferred_departure_time_2:
            continue
        if to_preferred_departure_time and trip.inbound.departureTime.hour < to_preferred_departure_time:
            continue
        if to_preferred_departure_time_2 and trip.inbound.departureTime.hour >= to_preferred_departure_time_2:
            continue
        # if days_length != 0 and (trip.inbound.departureTime - trip.outbound.departureTime).days >= days_length:
        #     continue
        if trip_min_days and (trip.inbound.departureTime - trip.outbound.departureTime).days < trip_min_days:
            continue
        if trip_max_days and (trip.inbound.departureTime - trip.outbound.departureTime).days > trip_max_days:
            continue
        if max_sum and trip.totalPrice > max_sum:
            continue
        trips.append(trip)
    return render_template('response.html', trips=trips)


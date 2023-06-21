import time

from ryanair import Ryanair
from datetime import datetime, timedelta

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
date_from = datetime.strptime("2023-09-01", "%Y-%m-%d")
loop_date_from = date_from
date_to = datetime.strptime("2023-10-25", "%Y-%m-%d")
loop_date_to = date_to

custom_params = {
    "IncludeConnectingFlights": False
}
start = time.time()
trips_aggregator = []
rounds = 0
max_sum = 99
min_days = 5
max_days = 8
d_f = 10
d_t = 15
b_f = 13
b_t = 19

depart_from = f"{d_f}:00"
back_from = f"{b_f}:00"
depart_to = f"{d_t}:00"
back_to = f"{b_t}:00"

sort_by = "price"

dates = set()

while loop_date_from <= loop_date_to:
    min = min_days
    while min <= max_days:
        if loop_date_from + timedelta(days=min) < loop_date_to:
            dates.add((loop_date_from, loop_date_from + timedelta(days=min)))
        min += 1
    loop_date_from += timedelta(days=1)

print(len(dates))

for date in dates:
    rounds += 1
    trips = api.get_cheapest_return_flights("TLV", date[0], date[0], date[1], date[1],
                                            custom_params=custom_params, max_price=max_sum,
                                            outbound_departure_time_from=depart_from,
                                            outbound_departure_time_to=depart_to,
                                            inbound_departure_time_from=back_from,
                                            inbound_departure_time_to=back_to,
                                            )
    for trip in trips:
        if trip.outbound.departureTime.hour < 10 or trip.outbound.departureTime.hour > 16:
            continue
        if trip.inbound.departureTime.hour > 15 or trip.inbound.departureTime.hour < 10:
            continue
        #if "Paphos" in trip.outbound.destinationFull:
        #    continue
        trips_aggregator.append(
            {
                "price": trip.summary['price']['value'],
                "currency": trip.summary['price']['currencyCode'],
                "to": trip.outbound.destinationFull,
                "to_airport": trip.outbound.destination,
                "date_from_departure": trip.outbound.departureTime,
                "date_from_arrival": trip.outbound.arrivalTime,
                "date_back_departure": trip.inbound.departureTime,
                "date_back_arrival": trip.inbound.arrivalTime,
                "days": trip.summary['tripDurationDays'],
            }
        )

if sort_by == "price":
    sorted_trips = sorted(trips_aggregator, key=lambda x: x["price"])
elif sort_by == "date":
    sorted_trips = sorted(trips_aggregator, key=lambda x: x["date_from_departure"])
else:
    sorted_trips = trips_aggregator

for index, t in enumerate(sorted_trips, start=1):
    print(f"{index}. Price: {t['price']} {t['currency']}, to: {t['to']}, "
          f"date out: {t['date_from_departure']} --- {t['date_from_arrival']}, date back {t['date_back_departure']} --- "
          f"{t['date_back_arrival']}, days: {t['days']}")

print(f"Results: {len(trips_aggregator)}")
print(f"Time: {time.time() - start}")

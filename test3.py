import time

from ryanair import Ryanair
from datetime import datetime, timedelta

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
date_from = datetime.strptime("2023-10-01", "%Y-%m-%d")
loop_date_from = date_from
date_to = datetime.strptime("2023-11-30", "%Y-%m-%d")
loop_date_to = date_to

custom_params = {
    "IncludeConnectingFlights": False
}
start = time.time()
trips_aggregator = []
rounds = 0
max_sum = 100
min_days = 3
max_days = 5

dates = []

while loop_date_from <= loop_date_to:
    min = min_days
    while min <= max_days:
        if loop_date_from + timedelta(days=min) < loop_date_to:
            dates.append((loop_date_from, loop_date_from + timedelta(days=min)))
        min += 1
    loop_date_from += timedelta(days=1)

print(len(dates))

for date in dates:
    rounds += 1
    trips = api.get_cheapest_return_flights("TLV", date[0], date[0], date[1], date[1],
                                            custom_params=custom_params, max_price=max_sum)
    for trip in trips:
        # if trip.outbound.departureTime.hour < 10 or trip.outbound.departureTime.hour > 16:
        #     continue
        # if trip.inbound.departureTime.hour > 15 or trip.inbound.departureTime.hour < 10:
        #     continue
        if "Paphos" in trip.outbound.destinationFull:
            continue
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

for index, t in enumerate(sorted(trips_aggregator, key=lambda x: x["price"]), start=1):
    print(f"{index}. Price: {t['price']} {t['currency']}, to: {t['to']}, "
          f"date out: {t['date_from']}, date back {t['date_back']}, "
          f"days: {t['days']}")

print(f"Results: {len(trips_aggregator)}")
print(f"Time: {time.time() - start}")

import time

from ryanair import Ryanair
from datetime import datetime, timedelta

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
date_from = datetime.strptime("2023-09-01", "%Y-%m-%d")
loop_date_from = date_from
date_to = datetime.strptime("2023-09-30", "%Y-%m-%d")
loop_date_to = date_to

custom_params = {
    "IncludeConnectingFlights": False
}
start = time.time()
trips_aggregator = []
rounds = 0
max_sum = 100
while loop_date_to >= loop_date_from:
    while loop_date_from <= loop_date_to:
        if (loop_date_to - loop_date_from).days > 10 or (loop_date_to - loop_date_from).days < 5:
            loop_date_from += timedelta(days=1)
            continue
        rounds += 1
        trips = api.get_cheapest_return_flights("TLV", loop_date_from, loop_date_from, loop_date_to, loop_date_to,
                                                custom_params=custom_params, max_price=max_sum)
        for trip in trips:
            # if max_sum and trip.summary['price']['value'] > max_sum:
            #     continue
            # if trip.summary['tripDurationDays'] > 10 or trip.summary['tripDurationDays'] < 5:
            #     continue
            # if trip.summary['tripDurationDays'] > 10:
            #     print(5 > trip.summary['tripDurationDays'] > 10)
            #     sys.exit(1)
            # if "Paphos" in trip.outbound.destinationFull:
            #     continue
            if trip.outbound.departureTime.hour < 10 or trip.outbound.departureTime.hour > 16:
                 continue
            if trip.inbound.departureTime.hour > 15 or trip.inbound.departureTime.hour < 10:
                continue
            trips_aggregator.append(
                {
                    "price": trip.summary['price']['value'],
                    "to": trip.outbound.destinationFull,
                    "date_from": trip.outbound.departureTime,
                    "date_back": trip.inbound.departureTime,
                    "days": trip.summary['tripDurationDays'],
                }
            )
            # print(f"Price: {trip.summary['price']['value']}, to: {trip.outbound.destinationFull}, "
            #       f"date out: {trip.outbound.departureTime}, date back {trip.inbound.departureTime}, "
            #       f"days: {trip.summary['tripDurationDays']}")
        loop_date_from += timedelta(days=1)
    loop_date_from = date_from
    loop_date_to -= timedelta(days=1)

for t in sorted(trips_aggregator, key=lambda x: x["price"]):
    print(f"Price: {t['price']}, to: {t['to']}, "
          f"date out: {t['date_from']}, date back {t['date_back']}, "
          f"days: {t['days']}")

print(f"Results: {len(trips_aggregator)}")
print(rounds)
print(f"Time: {time.time() - start}")

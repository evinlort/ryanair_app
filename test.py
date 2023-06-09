from ryanair import Ryanair

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
date_from_1 = "2023-09-01"
date_from_2 = "2023-09-03"
date_to_1 = "2023-11-07"
date_to_2 = "2023-11-15"

custom_params = {
    "IncludeConnectingFlights": False
}

trips = api.get_cheapest_return_flights("TLV", date_from_1, date_from_2, date_to_1, date_to_2, custom_params=custom_params)
# trips = api.get_all_flights("TLV", "2023-09-01", "BUD")
for trip in trips:
    # if trip.outbound.departureTime.hour <= 10:
    #     continue
    # print((trip.inbound.departureTime - trip.outbound.departureTime).days)
    # if (trip.inbound.departureTime - trip.outbound.departureTime).days >= 10:
    #     continue
    print(f"Price: {trip.summary['price']['value']}, to: {trip.outbound.destinationFull}, "
          f"date out: {trip.outbound.departureTime}, date back {trip.inbound.departureTime}, "
          f"days: {(trip.inbound.departureTime - trip.outbound.departureTime).days}")

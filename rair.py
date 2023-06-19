import datetime
from datetime import timedelta
from time import sleep

from ryanair.ryanair import Ryanair


registered_values = ["from_", "to", "except_airport", "date_from", "date_to", "trip_min_days",
                     "trip_max_days", "from_preferred_departure_time", "from_preferred_departure_time_2",
                     "to_preferred_departure_time", "to_preferred_departure_time_2", "max_sum"]


class RAir:
    def __init__(self, *args, **kwargs):
        for key, val in kwargs.items():
            if key in registered_values:
                if "date" in key:
                    setattr(self, key, datetime.datetime.strptime(val, "%Y-%m-%d"))
                else:
                    setattr(self, key, val)

        for key in registered_values:
            if hasattr(self, key):
                continue
            setattr(self, key, "")

        if not self.trip_min_days:
            self.trip_min_days = 0
        if not self.trip_max_days:
            self.trip_max_days = (self.date_to - self.date_from).days
        self.api = Ryanair(currency="EUR")

    def get_flights(self):
        dates = []
        while self.date_from <= self.date_to:
            min = int(self.trip_min_days)
            while min <= int(self.trip_max_days):
                if (self.date_from + timedelta(days=min)) < self.date_to:
                    dates.append((self.date_from, self.date_from + timedelta(days=min)))
                min += 1
            self.date_from += timedelta(days=1)

        trips_aggregator = []

        for n, date in enumerate(dates):
            if not n % 50:
                sleep(1)
            trips = self.api.get_cheapest_return_flights(source_airport=self.from_, destination_airport=self.to,
                                                     date_from=date[0], date_to=date[0],
                                                     return_date_from=date[1], return_date_to=date[1],
                                                     outbound_departure_time_from=f"{self.from_preferred_departure_time}",
                                                     outbound_departure_time_to=f"{self.from_preferred_departure_time_2}",
                                                     inbound_departure_time_from=f"{self.to_preferred_departure_time}",
                                                     inbound_departure_time_to=f"{self.to_preferred_departure_time_2}",
                                                     max_price=self.max_sum,
                                                     custom_params={"IncludeConnectingFlights": False})
            for trip in trips:
                if trip.outbound.destination in self.except_airport.upper().split():
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

        return sorted(trips_aggregator, key=lambda x: x["price"])

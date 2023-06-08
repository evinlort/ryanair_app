from ryanair.ryanair import Ryanair


registered_values = ["from_", "to", "date_from_1", "date_from_2", "date_to_1", "date_to_2", "trip_min_days",
                     "trip_max_days", "from_preferred_departure_time", "from_preferred_arrival_time",
                     "to_preferred_departure_time", "to_preferred_arrival_time", "max_sum"]


class RAir:
    def __init__(self, *args, **kwargs):
        for key, val in kwargs.items():
            if key in registered_values:
                setattr(self, key, val)
        for key in registered_values:
            if hasattr(self, key):
                continue
            setattr(self, key, "")
        print(self.to)
        self.api = Ryanair(currency="EUR")

    def get_flights(self):
        trips = self.api.get_cheapest_return_flights(source_airport=self.from_, destination_airport=self.to,
                                                     date_from=self.date_from_1, date_to=self.date_from_2,
                                                     return_date_from=self.date_to_1, return_date_to=self.date_to_2,
                                                     # outbound_departure_time_from=f"{self.from_preferred_departure_time}",
                                                     # inbound_departure_time_to=f"{self.to_preferred_departure_time}",
                                                     custom_params={"IncludeConnectingFlights": False})

        return trips

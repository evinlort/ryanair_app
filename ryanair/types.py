from collections import namedtuple

Flight = namedtuple("Flight", ("departureTime", "arrivalTime", "flightNumber", "price", "currency", "origin", "originFull",
                               "destination", "destinationFull"))
Trip = namedtuple("Trip", ("summary", "outbound", "inbound"))

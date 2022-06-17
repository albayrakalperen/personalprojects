 #This class is responsible for structuring the flight data.
class FlightData:
  
    def __init__(self, price, from_airport, to_airport, arrival_date,
                 arrival_time, departure_date, departure_time):
        self.price = price
        self.from_airport = from_airport
        self.to_airport = to_airport
        self.arrival_date = arrival_date
        self.arrival_time = arrival_time
        self.departure_date = departure_date
        self.departure_time = departure_time

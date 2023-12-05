import random
import time


class PassengerInSensor:
    def __init__(self):
        self.passenger_count = 0

    def passenger_counter(self):
        # Simulate logical behavior, allowing for small changes
        change = random.randint(-5, 5)
        self.passenger_count = max(0, min(70, self.passenger_count + change))
        print(f"Number of entered Passengers: {self.passenger_count}")
        return self.passenger_count

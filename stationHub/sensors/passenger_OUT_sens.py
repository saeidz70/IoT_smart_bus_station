import random


class PassengerOutSensor:
    def __init__(self):
        self.passenger_count = 0

    def passenger_counter(self):
        # Simulate logical behavior, allowing for small changes
        change = random.randint(-5, 5)
        self.passenger_count = max(0, min(70, self.passenger_count + change))
        return self.passenger_count, print(f"Number of exited Passengers: {self.passenger_count}")

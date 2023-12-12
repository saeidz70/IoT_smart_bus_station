import random
import time
from datetime import datetime

import requests


class PassengerInSensor:
    def __init__(self):
        self.passenger_count = 0

    def passenger_counter(self):
        # Simulate logical behavior, allowing for small changes
        change = random.randint(-5, 5)
        self.passenger_count = max(0, min(70, self.passenger_count + change))

        message = {"address":
                       ["stations", "station_1", "sensors", "passenger_IN"],

                   "data": {
                       "sensor_pass_in_1": {
                           "sensor_name": "passenger_IN_sensor_s1_1",
                           "sensor_id": "pass_IN_sen_id_s1_1",
                           "unit": "int",
                           "sensor_topic": "smartStation/station_1/passenger_IN/pass_IN_1",
                           "value": self.passenger_count,
                           "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       }
                   }
                   }

        uri = "http://127.0.0.1:8080/"
        requests.post(uri, json=message)

        print(f"Number of entered Passengers: {self.passenger_count}")
        return self.passenger_count

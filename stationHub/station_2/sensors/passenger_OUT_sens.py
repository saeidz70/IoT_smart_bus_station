import random
from datetime import datetime

import requests


class PassengerOutSensor:
    def __init__(self):
        self.passenger_count = 0

    def passenger_counter(self):
        # Simulate logical behavior, allowing for small changes
        change = random.randint(-5, 5)
        self.passenger_count = max(0, min(70, self.passenger_count + change))

        message = {"address":
                       ["stations", "station_2", "sensors", "passenger_OUT"],

                   "data": {
                       "sensor_pass_out_1": {
                           "sensor_name": "passenger_OUT_sensor_s2_1",
                           "sensor_id": "pass_OUT_sen_id_s2_1",
                           "unit": "int",
                           "sensor_topic": "smartStation/station_2/passenger_OUT/pass_OUT_1",
                           "value": self.passenger_count,
                           "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       }
                   }
                   }

        uri = "http://127.0.0.1:8080/"
        requests.post(uri, json=message)

        print(f"Number of exited Passengers: {self.passenger_count}")
        return self.passenger_count

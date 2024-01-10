import random
from datetime import datetime

import requests


class MotionSensor:
    def __init__(self):
        pass

    def passenger_motion(self):
        # Simulate logical behavior, allowing for small changes
        motion = random.randint(0, 1)

        message = {"address":
                       ["stations", "station_2", "sensors", "motion"],

                   "data": {
                       "sensor_motion_1": {
                        "sensor_name": "motion_sensor_s2_1",
                        "sensor_id": "motion_sen_id_s2_1",
                        "unit": "bol",
                        "sensor_topic": "smartStation/station_2/motion/motion_1",
                        "value": motion,
                        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       }
                   }
                   }

        uri = "http://127.0.0.1:8080/"
        requests.post(uri, json=message)

        print(f"Motion status is: {motion}")
        return motion

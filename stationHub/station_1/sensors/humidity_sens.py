from datetime import datetime
import requests
from scipy.stats import truncnorm


class HumiditySensor:
    def __init__(self):
        self.humidity_deviation = 5  # Adjust deviation as needed

    def set_seasonal_limits(self, month):
        seasons = {
            1: (30, 60),  # Winter
            2: (30, 60),  # Winter
            3: (40, 70),  # Spring
            4: (40, 70),  # Spring
            5: (40, 70),  # Spring
            6: (60, 90),  # Summer
            7: (60, 90),  # Summer
            8: (60, 90),  # Summer
            9: (40, 70),  # Fall
            10: (40, 70),  # Fall
            11: (40, 70),  # Fall
            12: (30, 60)  # Winter
        }
        return seasons[month]

    def humiditySens(self):
        current_time = datetime.now()
        month = current_time.month

        lower_limit, upper_limit = self.set_seasonal_limits(month)

        # Calculate the parameters for the truncated normal distribution
        mean = (lower_limit + upper_limit) / 2
        a = (lower_limit - mean) / self.humidity_deviation
        b = (upper_limit - mean) / self.humidity_deviation

        distribution = truncnorm(a, b, loc=mean, scale=self.humidity_deviation)

        # Generate humidity based on the truncated normal distribution
        humidity = int(distribution.rvs())

        message = {"address":
                       ["stations", "station_1", "sensors", "humidity"],

                   "data": {
                       "sensor_humid_1": {
                           "sensor_name": "humidity_sensor_s1_1",
                           "sensor_id": "humid_sen_id_s1_1",
                           "unit": "%",
                           "sensor_topic": "smartStation/station_1/humidity/humid_1",
                           "value": humidity,
                           "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       }
                   }
                   }

        uri = "http://127.0.0.1:8080/"
        requests.post(uri, json=message)
        print(f"Humidity: {humidity}%")
        return humidity

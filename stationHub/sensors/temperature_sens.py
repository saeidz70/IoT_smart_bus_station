from datetime import datetime
import random
from scipy.stats import truncnorm


class TemperatureSensor:
    def __init__(self):
        self.temperature_deviation = 1  # Adjust deviation as needed

    def set_seasonal_limits(self, month):
        seasons = {
            1: (-10, 15),  # Winter
            2: (-10, 15),  # Winter
            3: (3, 25),  # Spring
            4: (3, 25),  # Spring
            5: (3, 25),  # Spring
            6: (15, 45),  # Summer
            7: (15, 45),  # Summer
            8: (15, 45),  # Summer
            9: (0, 15),  # Fall
            10: (0, 15),  # Fall
            11: (0, 15),  # Fall
            12: (-10, 15)  # Winter
        }
        return seasons[month]

    def temperatureSens(self):
        current_time = datetime.now()
        month = current_time.month

        lower_limit, upper_limit = self.set_seasonal_limits(month)

        # Calculate the parameters for the truncated normal distribution
        mean = (lower_limit + upper_limit) / 2
        a = (lower_limit - mean) / self.temperature_deviation
        b = (upper_limit - mean) / self.temperature_deviation

        # Adjust temperature based on time of day
        hour = current_time.hour
        if 6 <= hour < 18:  # Daytime hours (6:00 to 17:59)
            mean += 5  # Increase mean for higher daytime temperature

        distribution = truncnorm(a, b, loc=mean, scale=self.temperature_deviation)

        # Generate temperature based on the truncated normal distribution
        temperature = int(distribution.rvs())
        print(f"Temperature: {temperature}^C")
        return temperature

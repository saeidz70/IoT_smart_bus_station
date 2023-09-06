import random


class HumiditySensor:
    def __init__(self, mean=40, deviation=3):
        self.mean = mean
        self.deviation = deviation
        self.previous_humidity = None

    def humiditySens(self):
        if self.previous_humidity is None:
            humidity_sens = random.gauss(self.mean, self.deviation)
        else:
            humidity_sens = random.gauss(
                (self.previous_humidity + self.mean) / 2,
                self.deviation / 2
            )

        humidity_sens = max(0, min(100, humidity_sens))  # Ensure humidity_sens stays within 0 to 100
        humidity_sens = round(humidity_sens * 2) / 2  # Round to nearest 0.5
        self.previous_humidity = humidity_sens
        return humidity_sens, print(f"Humidity: {humidity_sens:.1f}%")

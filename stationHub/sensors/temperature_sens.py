import random


class TemperatureSensor:
    def __init__(self, mean=20, deviation=3):
        self.mean = mean
        self.deviation = deviation
        self.previous_temperature = None

    def temperatureSens(self):
        if self.previous_temperature is None:
            temperature_sens = random.gauss(self.mean, self.deviation)
        else:
            temperature_sens = random.gauss(
                (self.previous_temperature + self.mean) / 2,
                self.deviation / 2
            )

        temperature_sens = max(-30, min(60, temperature_sens))  # Ensure temperature_sens stays within -30 to 60
        temperature_sens = round(temperature_sens * 2) / 2  # Round to nearest 0.5
        self.previous_temperature = temperature_sens
        return temperature_sens, print(f"Temperature: {temperature_sens:.1f}^C")

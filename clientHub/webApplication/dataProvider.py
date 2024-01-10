import requests


class DataProvider(object):
    def __init__(self):
        self.status = {}

    def get_data(self, station="station_1"):
        url = 'http://127.0.0.1:8080/stations/' + str(station)
        self.status["station"] = station

        response = requests.get(url).status_code
        self.status["response"] = response
        print(response)

        if response == 200:
            temperature_url = url + "/sensors/temperature/sensor_temp_1/value"
            print(temperature_url)
            temperature = requests.get(temperature_url).json()
            self.status["temperature"] = temperature

            humidity_url = url + "/sensors/humidity/sensor_humid_1/value"
            humidity = requests.get(humidity_url).json()
            self.status["humidity"] = humidity

            cooler_url = url + "/device_status/cooler"
            cooler = requests.get(cooler_url).json()
            self.status["cooler"] = cooler

            heater_url = url + "/device_status/heater"
            heater = requests.get(heater_url).json()
            self.status["heater"] = heater

            dehumidifier_url = url + "/device_status/dehumidifier"
            dehumidifier = requests.get(dehumidifier_url).json()
            self.status["dehumidifier"] = dehumidifier

            light_url = url + "/device_status/light"
            light = requests.get(light_url).json()
            self.status["light"] = light


        print(self.status)
        return self.status


if __name__ == "__main__":
    print('\n*** Get Current Station Conditions ***\n')

    station = input("\nPlease enter a station: ")

    if not bool(station.strip()):
        station = "station_1"
    data = DataProvider().get_data(station)

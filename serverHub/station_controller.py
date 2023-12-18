import json
import random
import time
import requests
from serverHub.serverside_subscriber import SensorsSubscriber


class StationController:
    def __init__(self):
        self.get_thresholds()
        self.get_data()
        self.command = {}

        # Initialize counters and intervals
        self.catalog_counter = 0
        self.data_counter = 0
        self.command_counter = 0

    def get_data(self):

        conf = requests.get("http://127.0.0.1:8080/settings/services/MQTT/subscribers").json()
        clientID = conf["client_id"]
        broker = conf["broker"]
        port = conf["port"]

        topic = requests.get("http://127.0.0.1:8080/stations/station_1/station_topic").json()
        sensorsSubscriber = SensorsSubscriber(clientID, topic, broker, port)
        sensorsSubscriber.run()
        time.sleep(10)
        print(sensorsSubscriber.name, sensorsSubscriber.value)
        # if sensorsSubscriber.name == "temperature":
        #     self.sensor_temperature = sensorsSubscriber.value
        #     print(self.sensor_temperature)
        # elif sensorsSubscriber.name == "humidity":
        #     self.sensor_humidity = sensorsSubscriber.value
        #     print(self.sensor_humidity)
        # elif sensorsSubscriber.name == "crowd":
        #     self.sensor_motion == sensorsSubscriber.value
        #     print(self.sensor_motion)
        # elif sensorsSubscriber.name ==  "passenger_in":
        #     self.passenger_IN = sensorsSubscriber.value
        #     print(self.passenger_IN)
        # elif sensorsSubscriber.name == "passenger_out":
        #     self.passenger_OUT = sensorsSubscriber.value
        #     print(self.passenger_OUT)
        # if sensorsSubscriber.name == self.catalog["stations"]["station_1"]["sensors"]["temperature"]:
        # for key in self.catalog["stations"]["station_1"]["sensors"]:
        #     self.sensor

    def get_thresholds(self):
        try:
            response = requests.get("http://127.0.0.1:8080/stations/station_1/threshold")
            if response.status_code == 200:
                threshold = response.json()
                self.temperature_cold_threshold = int(threshold["temperature_cold"])
                self.temperature_hot_threshold = int(threshold["temperature_hot"])
                self.humidity_threshold = int(threshold["humidity"])
                print("get_thresholds: ", self.temperature_hot_threshold, self.temperature_cold_threshold,
                      self.humidity_threshold)

                return threshold
        except Exception as e:
            print(f"Error fetching threshold information:", str(e))
        return None

    # TODO: update data from serverside_subscriber

    def update_data(self):
        self.sensor_temperature = random.randint(0, 40)
        self.sensor_humidity = random.randint(5, 95)
        self.sensor_motion = random.randint(0, 1)
        self.passenger_IN = random.randint(0, 50)
        self.passenger_OUT = random.randint(0, 50)

    def temp_control(self):
        if self.sensor_temperature > self.temperature_hot_threshold:
            self.command["cooler"] = "on"
            self.command["heater"] = "off"
        elif self.sensor_temperature < self.temperature_cold_threshold:
            self.command["cooler"] = "off"
            self.command["heater"] = "on"
        else:
            self.command["cooler"] = "off"
            self.command["heater"] = "off"
        return self.command

    def humidity_control(self):
        if self.sensor_humidity > self.humidity_threshold:
            self.command["dehumidifier"] = "on"
        else:
            self.command["dehumidifier"] = "off"
        return self.command

    def light_control(self):
        if self.sensor_motion == 1 or self.passenger_IN != 0:
            self.command["light"] = "on"
        else:
            self.command["light"] = "off"
        return self.command

    def put(self, uri, body):
        body = json.dumps(body)
        response = requests.put(uri, data=body)
        return f'''
        Response code: {response.status_code}\n
        Response content: {response.text}\n
        '''


# TODO:
#  count passenger


if __name__ == "__main__":


    uri = (requests.get("http://127.0.0.1:8080/settings/services/REST")).json()["uri"]
    print(uri)

    while True:
        controller = StationController()
        # Update get_catalog every 15 seconds
        if controller.catalog_counter % 15 == 0:
            controller.get_thresholds()
            print("temperature_hot_threshold: ", controller.temperature_hot_threshold, "temperature_cold_threshold: ",
                  controller.temperature_cold_threshold, "humidity_threshold: ", controller.humidity_threshold)

        # Update update_data every 10 seconds
        if controller.data_counter % 10 == 0:
            controller.update_data()
            print("sensor_temperature: ", controller.sensor_temperature, "sensor_humidity: ",
                  controller.sensor_humidity, "sensor_motion: ", controller.sensor_motion, "passenger_IN: ",
                  controller.passenger_IN)

        # Update command every 5 seconds
        if controller.command_counter % 5 == 0:
            body = controller.temp_control()
            body.update(controller.humidity_control())
            body.update(controller.light_control())
            print("body: ", body)

            response = controller.put(uri, body)
            print("response: ", response)

        time.sleep(1)  # Sleep for 1 second
        controller.catalog_counter += 1
        controller.data_counter += 1
        controller.command_counter += 1

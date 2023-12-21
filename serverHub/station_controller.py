import time
import requests
from mqtt.MyMQTT import *
import json


class StationController:
    def __init__(self, clientID, broker, port):
        self.client = MyMQTT(clientID, broker, port, self)
        self.client.start()
        self.command = {}
        self.catalog_counter = 0
        self.data_counter = 0
        self.command_counter = 0
        self.sensor_motion = 0
        self.passenger_IN = 0
        self.uri_actuator = None

    def subscribe(self, topic):
        self.client.mySubscribe(topic)
        self.topic_subscribe = topic.split("/")[1]

    def get_thresholds(self, uri):
        try:
            response = requests.get(uri)
            if response.status_code == 200:
                threshold = response.json()
                self.temperature_cold_threshold = int(threshold["temperature_cold"])
                self.temperature_hot_threshold = int(threshold["temperature_hot"])
                self.humidity_threshold = int(threshold["humidity"])
                self.station_threshold = {
                    self.topic_subscribe: {"temperature_cold_threshold": self.temperature_cold_threshold,
                                           "temperature_hot_threshold": self.temperature_hot_threshold,
                                           "humidity_threshold": self.humidity_threshold}}

                return self.station_threshold
        except Exception as e:
            print(f"Error fetching threshold information:", str(e))
        return None

    # TODO: update data from serverside_subscriber

    def notify(self, topic, message):
        topic_notify = topic.split("/")[1]
        data = json.loads(json.loads(message))
        print("Notification", data)
        print(topic)
        name = data["e"][0]["n"]
        value = data["e"][0]["value"]
        notify_value = [topic_notify, name, value]
        print("notify_value", notify_value)
        self.update_data(notify_value)

    def update_data(self, notify_value):
        if notify_value[1] == "temperature":
            self.sensor_temperature = notify_value[2]
            print("Temperature sensor", self.sensor_temperature)
            print("notify_value from update_data", notify_value)
            self.temp_control(notify_value)

        elif notify_value[1] == "humidity":
            self.sensor_humidity = notify_value[2]
            print("humidity sensor", self.sensor_humidity)
            self.humidity_control(notify_value)

        elif notify_value[1] == "crowd":
            self.sensor_motion = notify_value[2]
            print("Motion sensor", self.sensor_motion)
            self.light_control(notify_value)

        elif notify_value[1] == "passenger_in":
            self.passenger_IN = notify_value[2]
            print("Passenger in sensor", self.passenger_IN)
            self.light_control(notify_value)

        elif notify_value[1] == "passenger_out":
            self.passenger_OUT = notify_value[2]
            print("Passenger out sensor", self.passenger_OUT)
            self.light_control(notify_value)

    def temp_control(self, notify_value):
        print("This is temp_control")
        if notify_value[0] == list(self.station_threshold.keys())[0]:
            print("This is temp_control in the if condition, value :", self.sensor_temperature, "threshold_H:",
                  self.temperature_hot_threshold)

            if self.sensor_temperature > self.temperature_hot_threshold:
                # print("This is temp_control in the if condition, value :", self.sensor_temperature, "threshold_H:",self.sensor_temperature)
                self.command["cooler"] = "on"
                self.command["heater"] = "off"
                print("temp_control 1 if", self.command, notify_value[0])
            elif self.sensor_temperature < self.temperature_cold_threshold:
                # print("This is temp_control in the if condition, value :", self.sensor_temperature, "threshold_C:",self.sensor_temperature)

                self.command["cooler"] = "off"
                self.command["heater"] = "on"
                print("temp_control 2 if", self.command, notify_value[0])


            else:
                self.command["cooler"] = "off"
                self.command["heater"] = "off"
                print("temp_control 3 if", self.command, notify_value[0])

            self.data_format(self.command, notify_value[0])
            return self.command, notify_value

    def humidity_control(self, notify_value):
        print("This is humidity control")
        if notify_value[0] == list(self.station_threshold.keys())[0]:

            if self.sensor_humidity > self.humidity_threshold:
                self.command["dehumidifier"] = "on"
            else:
                self.command["dehumidifier"] = "off"
            self.data_format(self.command, notify_value[0])
            return self.command

    def light_control(self, notify_value):
        print("this is light control")
        if notify_value[0] == list(self.station_threshold.keys())[0]:

            if self.sensor_motion == 1:
                self.command["light"] = "on"
            elif self.passenger_IN != 0:
                self.command["light"] = "on"
            else:
                self.command["light"] = "off"
            self.data_format(self.command, notify_value[0])
            return self.command

    def data_format(self, data, station):
        print("data format line 1", data, station)
        if len(data) == 4:
            address = ["stations", station, "device_status"]
            print("data format", address, data)
            message = {"address": address, "data": data}
            station_uri = self.uri_actuator.split("/")[-1]
            print("station uri", station_uri)
            if station_uri == station:
                self.put(self.uri_actuator, message)

    def put(self, uri_actuator, message):
        body = json.dumps(message)
        print("put message", body)
        headers = {'Content-Type': 'application/json'}
        response = requests.put(uri_actuator, data=body, headers=headers)
        return f'''
        Response code: {response.status_code}\n
        Response content: {response.text}\n
        '''


if __name__ == "__main__":

    conf = requests.get("http://127.0.0.1:8080/settings/services/MQTT/subscribers").json()
    clientID = conf["client_id"]
    broker = conf["broker"]
    port = conf["port"]

    # Station 1
    topic = requests.get("http://127.0.0.1:8080/stations/station_1/station_topic").json()
    station_threshold = "http://127.0.0.1:8080/stations/station_1/threshold"
    uri = (requests.get("http://127.0.0.1:8080/stations/station_1/REST/uri")).json()

    controller_station_1 = StationController(clientID, broker, port)
    controller_station_1.subscribe(topic)
    controller_station_1.get_thresholds(station_threshold)
    controller_station_1.uri_actuator = uri
    print(uri)
    # Station 2

    while True:
        time.sleep(30)
        controller_station_1.get_thresholds(station_threshold)

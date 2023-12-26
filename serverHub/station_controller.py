import time
from datetime import datetime

import requests
from mqtt.MyMQTT import *
import json


class StationController:
    def __init__(self, clientID, broker, port):
        self.client = MyMQTT(clientID, broker, port, self)
        self.client.start()
        self.command = {}
        self.sensor_temperature = 0
        self.sensor_humidity = 0
        self.passenger_OUT = 0
        self.passenger_IN = 0
        self.sensor_motion = 0
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
        self.save_data(notify_value)

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

    def save_data(self, notify_value):
        myTime = datetime.timestamp(datetime.now())
        data = {"timestamp": myTime, "sensor_name": notify_value[1], "sensor_value": notify_value[2]}
        if notify_value[0] == "station_1":
            filename = 'database/database_station_1.json'
            with open(filename, 'r+') as file:
                file_data = json.load(file)
                file_data["station_1"].append(data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            print(file_data)
        elif notify_value[0] == "station_2":
            filename = 'database/database_station_2.json'
            with open(filename, 'r+') as file:
                file_data = json.load(file)
                file_data["station_2"].append(data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            print(file_data)
        print("save data", notify_value)


if __name__ == "__main__":

    # Station 1
    conf_s_1 = requests.get("http://127.0.0.1:8080/stations/station_1/services/MQTT/subscriber").json()
    topic_s_1 = requests.get("http://127.0.0.1:8080/stations/station_1/station_topic").json()
    station_threshold_s_1 = "http://127.0.0.1:8080/stations/station_1/threshold"
    uri_s_1 = (requests.get("http://127.0.0.1:8080/stations/station_1/services/REST/uri")).json()

    clientID_s_1 = conf_s_1["client_id"]
    broker_s_1 = conf_s_1["broker"]
    port_s_1 = conf_s_1["port"]

    controller_station_1 = StationController(clientID_s_1, broker_s_1, port_s_1)
    controller_station_1.subscribe(topic_s_1)
    controller_station_1.get_thresholds(station_threshold_s_1)
    controller_station_1.uri_actuator = uri_s_1
    print(uri_s_1)

    # Station 2
    conf_s_2 = requests.get("http://127.0.0.1:8080/stations/station_2/services/MQTT/subscriber").json()
    topic_s_2 = requests.get("http://127.0.0.1:8080/stations/station_2/station_topic").json()
    station_threshold_s_2 = "http://127.0.0.1:8080/stations/station_2/threshold"
    uri_s_2 = (requests.get("http://127.0.0.1:8080/stations/station_2/services/REST/uri")).json()

    clientID_s_2 = conf_s_2["client_id"]
    broker_s_2 = conf_s_2["broker"]
    port_s_2 = conf_s_2["port"]

    controller_station_2 = StationController(clientID_s_2, broker_s_2, port_s_2)
    controller_station_2.subscribe(topic_s_2)
    controller_station_2.get_thresholds(station_threshold_s_2)
    controller_station_2.uri_actuator = uri_s_2
    print(uri_s_2)

    while True:
        time.sleep(30)
        controller_station_1.get_thresholds(station_threshold_s_1)
        controller_station_2.get_thresholds(station_threshold_s_2)

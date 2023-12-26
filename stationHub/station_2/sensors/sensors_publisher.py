import requests
from mqtt.MyMQTT import *
import time
import json
from datetime import datetime
from stationHub.station_2.sensors.passenger_IN_sens import PassengerInSensor
from stationHub.station_2.sensors.passenger_OUT_sens import PassengerOutSensor
from stationHub.station_2.sensors.humidity_sens import HumiditySensor
from stationHub.station_2.sensors.temperature_sens import TemperatureSensor
from stationHub.station_2.sensors.motion_sens import MotionSensor


class SensorPublisher:
    def __init__(self, clientID, broker, port):
        self.client = MyMQTT(clientID, broker, port, self)
        self.get_topic()

    def start(self):
        self.client.start()
        self.publish()

    def stop(self):
        self.client.stop()

    def get_topic(self):
        self.temperature_topic = requests.get(
            "http://127.0.0.1:8080/stations/station_2/sensors/temperature/sensor_temp_1/sensor_topic").json()
        self.humidity_topic = requests.get(
            "http://127.0.0.1:8080/stations/station_2/sensors/humidity/sensor_humid_1/sensor_topic").json()
        self.passenger_IN_topic = requests.get(
            "http://127.0.0.1:8080/stations/station_2/sensors/passenger_IN/sensor_pass_in_1/sensor_topic").json()
        self.passenger_OUT_topic = requests.get(
            "http://127.0.0.1:8080/stations/station_2/sensors/passenger_OUT/sensor_pass_out_1/sensor_topic").json()
        self.motion_topic = requests.get(
            "http://127.0.0.1:8080/stations/station_2/sensors/motion/sensor_motion_1/sensor_topic").json()

    def publish(self):
        while True:
            temperature = (TemperatureSensor().temperatureSens())
            humidity = (HumiditySensor().humiditySens())
            passenger_in = (PassengerInSensor().passenger_counter())
            passenger_out = (PassengerOutSensor().passenger_counter())
            motion = (MotionSensor().passenger_motion())

            temperature_payload = self.create_sensor_payload("temperature", "Cel", temperature)
            humidity_payload = self.create_sensor_payload("humidity", "d", humidity)
            passenger_in_payload = self.create_sensor_payload("passenger_in", "d", passenger_in)
            passenger_out_payload = self.create_sensor_payload("passenger_out", "d", passenger_out)
            motion_payload = self.create_sensor_payload("crowd", "d", motion)

            self.client.myPublish(self.temperature_topic, temperature_payload)
            print(self.temperature_topic, temperature_payload)
            time.sleep(5)
            self.client.myPublish(self.humidity_topic, humidity_payload)
            print(self.humidity_topic, humidity_payload)
            time.sleep(5)
            self.client.myPublish(self.passenger_IN_topic, passenger_in_payload)
            print(self.passenger_IN_topic, passenger_in_payload)
            time.sleep(5)
            self.client.myPublish(self.passenger_OUT_topic, passenger_out_payload)
            print(self.passenger_OUT_topic, passenger_out_payload)
            time.sleep(5)
            self.client.myPublish(self.motion_topic, motion_payload)
            print(self.motion_topic, motion_payload)
            time.sleep(5)

            print("Published sensor data at", datetime.now())

    def create_sensor_payload(self, sensor_name, unit, value):
        payload = {
            "bn": self.client.clientID,
            "e": [
                {
                    "n": sensor_name,
                    "unit": unit,
                    "timestamp": int(time.time()),
                    "value": value
                }
            ]
        }
        return json.dumps(payload)


if __name__ == "__main__":
    conf = requests.get("http://127.0.0.1:8080/stations/station_2/services/MQTT/publisher").json()
    print(conf)
    clientID = conf["client_id"]
    broker = conf["broker"]
    port = conf["port"]
    SensorPublisher = SensorPublisher(clientID, broker, port)
    SensorPublisher.start()
    time.sleep(5)

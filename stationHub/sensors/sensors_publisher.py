import random
from mqtt.MyMQTT import *
import time
import json
from datetime import datetime
from stationHub.sensors.passenger_IN_sens import PassengerInSensor
from stationHub.sensors.passenger_OUT_sens import PassengerOutSensor
from stationHub.sensors.humidity_sens import HumiditySensor
from stationHub.sensors.temperature_sens import TemperatureSensor


class SensorPublisher:
    def __init__(self, clientID, topic, broker, port):
        self.client = MyMQTT(clientID, broker, port, self)
        self.base_topic = topic
        self.temperature_topic = self.base_topic + "sensor/temperature"
        self.humidity_topic = self.base_topic + "sensor/humidity"
        self.passenger_IN_topic = self.base_topic + "sensor/passengerIn"
        self.passenger_OUT_topic = self.base_topic + "sensor/passengerOut"
        self.motion_topic = self.base_topic + "sensor/motion"

    def start(self):
        self.client.start()
        self.publish()

    def stop(self):
        self.client.stop()

    def publish(self):
        while True:
            temperature = (TemperatureSensor().temperatureSens())[0]
            humidity = (HumiditySensor().humiditySens())[0]
            passenger_in = (PassengerInSensor().passenger_counter())[0]
            passenger_out = (PassengerOutSensor().passenger_counter())[0]
            motion = random.randint(0, 1)

            temperature_payload = self.create_sensor_payload("temperature", "Cel", temperature)
            humidity_payload = self.create_sensor_payload("humidity", "d", humidity)
            passenger_in_payload = self.create_sensor_payload("passenger_in", "d", passenger_in)
            passenger_out_payload = self.create_sensor_payload("passenger_out", "d", passenger_out)
            motion_payload = self.create_sensor_payload("crowd", "d", motion)


            self.client.myPublish(self.temperature_topic, temperature_payload)
            print(self.temperature_topic, temperature_payload)
            time.sleep(5)  # Publish temperature every 30 seconds
            self.client.myPublish(self.humidity_topic, humidity_payload)
            print(self.humidity_topic, humidity_payload)
            time.sleep(5)  # Publish humidity every 60 seconds
            self.client.myPublish(self.passenger_IN_topic, passenger_in_payload)
            print(self.passenger_IN_topic, passenger_in_payload)
            time.sleep(5)  # Publish humidity every 60 seconds
            self.client.myPublish(self.passenger_OUT_topic, passenger_out_payload)
            print(self.passenger_OUT_topic, passenger_out_payload)
            time.sleep(5)  # Publish humidity every 60 seconds
            self.client.myPublish(self.motion_topic, motion_payload)
            print(self.motion_topic, motion_payload)
            time.sleep(5)  # Publish temperature every 30 seconds

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
    catalog = json.load(open("../../catalog/catalog.json"))
    conf = catalog["services"]["MQTT"][0]
    print(conf)
    clientID = conf["client_id"]
    broker = conf["broker"]
    port = conf["port"]
    topic = conf["topic"]
    SensorPublisher = SensorPublisher(clientID, topic, broker, port)
    SensorPublisher.start()
    time.sleep(5)

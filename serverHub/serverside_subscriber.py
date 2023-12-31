from mqtt.MyMQTT import *
import time
import json
from datetime import datetime


class SensorsSubscriber:
    def __init__(self, clientID, topic, broker, port):
        self.passenger_OUT = None
        self.passenger_IN = None
        self.motion = None
        self.humidity = None
        self.temperature = None
        self.client = None
        self.client_ID = clientID
        self.base_topic = topic
        self.temperature_topic = self.base_topic + "sensor/temperature"
        self.humidity_topic = self.base_topic + "sensor/humidity"
        self.passenger_IN_topic = self.base_topic + "sensor/passengerIn"
        self.passenger_OUT_topic = self.base_topic + "sensor/passengerOut"
        self.motion_topic = self.base_topic + "sensor/motion"
        self.broker = broker
        self.port = port
        self.status = None

    def run(self):
        self.client = MyMQTT(self.client_ID, self.broker, self.port, self)
        self.client.start()
        self.client.mySubscribe(self.temperature_topic)
        self.client.mySubscribe(self.humidity_topic)
        self.client.mySubscribe(self.passenger_IN_topic)
        self.client.mySubscribe(self.passenger_OUT_topic)
        self.client.mySubscribe(self.motion_topic)

    def notify(self, topic, message):
        data = json.loads(json.loads(message))
        if topic == self.temperature_topic:
            self.temperature = data["e"][0]["value"]
            print("Received temperature:", self.temperature)
        elif topic == self.humidity_topic:
            self.humidity = data["e"][0]["value"]
            print("Received humidity:", self.humidity)
        elif topic == self.passenger_IN_topic:
            self.motion = data["e"][0]["value"]
            print("Received motion:", self.motion)
        elif topic == self.passenger_IN_topic:
            self.passenger_IN = data["e"][0]["value"]
            print("Received LED status:", self.passenger_IN)
        elif topic == self.passenger_IN_topic:
            self.passenger_OUT = data["e"][0]["value"]
            print("Received LED status:", self.passenger_OUT)


if __name__ == "__main__":
    catalog = json.load(open("../catalog/catalog.json"))
    conf = catalog["services"]["MQTT"][1]
    print(conf)
    clientID = conf["client_id"]
    broker = conf["broker"]
    port = conf["port"]
    topic = conf["topic"]

    SensorsSubscriber = SensorsSubscriber(clientID, topic, broker, port)
    SensorsSubscriber.run()

    while True:
        time.sleep(1)

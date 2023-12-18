import requests
from mqtt.MyMQTT import *
import time
import json


class SensorsSubscriber:
    def __init__(self, clientID, topic, broker, port):
        self.value = None
        self.name = None
        self.client_ID = clientID
        self.topic = topic
        self.broker = broker
        self.port = port
        self.status = None

    def run(self):
        self.client = MyMQTT(self.client_ID, self.broker, self.port, self)
        self.client.start()
        self.client.mySubscribe(self.topic)

    def notify(self, topic, message):
        data = json.loads(json.loads(message))
        # if topic == self.topic:
        self.name = data["e"][0]["n"]
        self.value = data["e"][0]["value"]
        print("Received data:", self.name, self.value)
        return self.name, self.value


if __name__ == "__main__":

    conf = requests.get("http://127.0.0.1:8080/settings/services/MQTT/subscribers").json()
    clientID = conf["client_id"]
    broker = conf["broker"]
    port = conf["port"]

    topic = requests.get("http://127.0.0.1:8080/stations/station_1/station_topic").json()
    print(topic)
    sensorsSubscriber = SensorsSubscriber(clientID, topic, broker, port)
    sensorsSubscriber.run()

    # print(sensorsSubscriber.name, sensorsSubscriber.value)

    while True:
        print(sensorsSubscriber.name, sensorsSubscriber.value)
        time.sleep(1)



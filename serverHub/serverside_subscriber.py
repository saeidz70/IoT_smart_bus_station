import requests
from mqtt.MyMQTT import MyMQTT
import time
import json

global_sensor_data = {}


class SensorsSubscriber:
    def __init__(self, clientID, topic, broker, port):
        self.client_ID = clientID  # Use underscores for variable names (PEP8 naming convention)
        self.base_topic = topic
        self.temperature_topic = self.base_topic + "sensor/temperature"
        self.humidity_topic = self.base_topic + "sensor/humidity"
        self.passenger_IN_topic = self.base_topic + "sensor/passengerIn"
        self.passenger_OUT_topic = self.base_topic + "sensor/passengerOut"
        self.motion_topic = self.base_topic + "sensor/motion"
        self.broker = broker
        self.port = port

        # Initialize sensor values to None
        self.temperature = None
        self.humidity = None
        self.passenger_IN = None
        self.passenger_OUT = None
        self.motion = None

        # Initialize the MQTT client
        self.client = MyMQTT(self.client_ID, self.broker, self.port, self)

    def run(self):
        self.client.start()
        self.client.mySubscribe(self.temperature_topic)
        self.client.mySubscribe(self.humidity_topic)
        self.client.mySubscribe(self.passenger_IN_topic)
        self.client.mySubscribe(self.passenger_OUT_topic)
        self.client.mySubscribe(self.motion_topic)

    def notify(self, topic, message):
        data = json.loads(json.loads(message))

        # Use elif for all conditions
        global global_sensor_data
        if topic == self.temperature_topic:
            self.temperature = data["e"][0]["value"]
            global_sensor_data["temperature"] = self.temperature
            print("Received temperature:", self.temperature)
        elif topic == self.humidity_topic:
            self.humidity = data["e"][0]["value"]
            global_sensor_data["humidity"] = self.humidity
            print("Received humidity:", self.humidity)
        elif topic == self.passenger_IN_topic:
            self.passenger_IN = data["e"][0]["value"]
            global_sensor_data["passenger_IN"] = self.passenger_IN
            print("Received passenger IN:", self.passenger_IN)
        elif topic == self.passenger_OUT_topic:
            self.passenger_OUT = data["e"][0]["value"]
            global_sensor_data["passenger_OUT"] = self.passenger_OUT
            print("Received passenger OUT:", self.passenger_OUT)
        elif topic == self.motion_topic:
            self.motion = data["e"][0]["value"]
            global_sensor_data["motion"] = self.motion
            print("Received motion:", self.motion)

            return global_sensor_data


    def put(self, uri, body):
        body = json.dumps(body)
        response = requests.put(uri, data=body)
        return f'''
        Response code: {response.status_code}\n
        Response content: {response.text}\n
        '''


if __name__ == "__main__":
    catalog = json.load(open("/Users/saeidzolfaghari/PycharmProjects/smartStation/catalog/catalog.json"))
    conf = catalog["services"]["MQTT"][1]
    clientID = conf["client_id"]
    broker = conf["broker"]
    port = conf["port"]
    topic = conf["topic"]

    sensors_subscriber = SensorsSubscriber(clientID, topic, broker, port)
    sensors_subscriber.run()


    while True:
        print(global_sensor_data)
        time.sleep(1)

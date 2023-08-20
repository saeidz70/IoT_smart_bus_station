import time
from sensors.passenger_IN_sens import PassengerInSensor
from sensors.passenger_OUT_sens import PassengerOutSensor
from sensors.humidity_sens import HumiditySensor


if __name__ == '__main__':

    while True:
        # Create an instance of the Sensors class

        passenger_in = PassengerInSensor().passenger_counter()
        # publish passenger_in TODO

        passenger_out = PassengerOutSensor().passenger_counter()
        # publish passenger_out TODO

        humidity = HumiditySensor().humiditySens()
        # publish humidity TODO

        # Wait for 1 second before generating the next sensor data
        time.sleep(5)

# Smart Bus Station

### Introduction: Transforming Bus Stations with IoT Technology
The proposed IoT platform aims to transform traditional bus stations into intelligent and efficient hubs, benefiting both passengers and authorities in a sustainable manner. Passengers will experience a secure and comfortable environment facilitated by autonomous sensors and devices. Simultaneously, public mobility authorities gain the ability to monitor passenger traffic at each station, as well as remotely control air conditioning and lighting.

![_fa4238f1-651a-469f-ac79-23dccfa2b01f (1)](https://github.com/saeidz70/IoT_smart_bus_station/assets/63140944/5dc94c2d-8065-4b19-ab12-c01df04a340f)

### Features of the Bus Station
The bus station is designed with three distinct doors – entrance, exit, and bus-side. Turnstiles at the entrance and exit accurately count the number of people passing through. On the roof, an air conditioner and dehumidifier are installed to regulate the station's internal conditions.

![Group 9](https://github.com/saeidz70/IoT_smart_bus_station/assets/63140944/ebd3815d-868f-406b-b0ea-8d281ce1520e)

### Station Infrastructure: Design and Components
Equipped with temperature, humidity, motion, and two counter sensors, the station collects valuable data. Temperature and humidity sensors provide insights into the station's climate, while motion sensors detect the presence of individuals. Counter sensors keep track of passenger entries and exits. A Raspberry Pi serves as the data publisher, transmitting information to the server. Additionally, an Arduino functions as the actuator for station devices such as the cooler, heater, dehumidifier, and lights. The actuator receives commands from the server's controller to power on or off the respective devices.

### Unified Interfaces for Seamless Operation
The platform facilitates the operation of the smart bus station through unified interfaces, employing REST and MQTT protocols. These interfaces ensure seamless communication and provide real-time information about the bus station's status.

## Diagram of connections between each part: 

![iot](https://github.com/saeidz70/IoT_smart_bus_station/assets/63140944/ff60ac3f-9f65-45a0-bba4-b34fee879dff)

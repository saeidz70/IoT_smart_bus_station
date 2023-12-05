# stations = []
#
# for key, values in dictionary["stations"].values():
#     stations.append(key)
#
# return stations
#
# station = input("Select a station: ")
# humidity = input("Select a station: ")
#
# for key, values in dictionary["stations"].items():
#     if key == station:
#         for key, values in key.items()
#             for key, values in key.items()
#                 if values == "humidity":
#
#
#     else:
#         pass


import requests

uri = "http://127.0.0.1:8080/"
body = {
    "address": ["lastUpdate3"]
}
response = requests.delete(uri, json=body)

# request = requests.post(uri, json=body)

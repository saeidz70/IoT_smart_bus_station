import cherrypy
import json


class CatalogAPI:
    exposed = True

    def __init__(self):
        self.file_name = "catalog.json"
        self.load_catalog()

    def load_catalog(self):
        try:
            with open(self.file_name, "r") as f:
                self.catalog = json.load(f)
        except FileNotFoundError:
            self.catalog = {}
            self.save_catalog()

    def save_catalog(self):
        with open(self.file_name, "w") as f:
            json.dump(self.catalog, f, indent=4)

    @cherrypy.tools.json_out()
    def GET(self, *uri):
        if not uri:
            return self.catalog

        elif len(uri) == 1 and uri[0] == "projectOwner":
            return self.catalog.get("projectOwner", "")
        elif len(uri) == 1 and uri[0] == "projectName":
            return self.catalog.get("projectName", "")
        elif len(uri) == 1 and uri[0] == "lastUpdate":
            return self.catalog.get("lastUpdate", "")

        elif len(uri) == 1 and uri[0] == "settings":
            return self.catalog.get("settings", {})
        elif len(uri) == 3 and uri[0] == "settings" and uri[1] == "services":
            service_type = uri[2]
            return self.catalog.get("settings", {}).get("services", {}).get(service_type, {})
        elif len(uri) == 2 and uri[0] == "settings":
            setting_item = uri[1]
            return self.catalog.get("settings", {}).get(setting_item, {})

        # "http://127.0.0.1:8080/stations/station_1/sensors/temperature/sensor_topic"
        elif len(uri) == 1 and uri[0] == "stations":
            return self.station_list()

        elif len(uri) == 2 and uri[0] == "stations":
            station_name = uri[1]
            return {
                "sensors": self.sensors(station_name),
                "device_status": self.device_status(station_name),
                "threshold": self.threshold(station_name)
            }
        elif len(uri) == 3 and uri[0] == "stations":
            if uri[2] == "sensors":
                station_name = uri[1]
                return self.sensors(station_name)
            elif uri[2] == "device_status":
                station_name = uri[1]
                return self.device_status(station_name)
            elif uri[2] == "threshold":
                station_name = uri[1]
                return self.threshold(station_name)

        elif len(uri) == 4 and uri[0] == "stations":
            if uri[2] == "sensors" and uri[3] == "temperature":
                station_name = uri[1]
                return self.sensors(station_name)["temperature"]

            elif uri[2] == "sensors" and uri[3] == "humidity":
                station_name = uri[1]
                return self.sensors(station_name)["humidity"]

            elif uri[2] == "sensors" and uri[3] == "motion":
                station_name = uri[1]
                return self.sensors(station_name)["motion"]

            elif uri[2] == "sensors" and uri[3] == "passenger_IN":
                station_name = uri[1]
                return self.sensors(station_name)["passenger_IN"]

            elif uri[2] == "sensors" and uri[3] == "passenger_OUT":
                station_name = uri[1]
                return self.sensors(station_name)["passenger_OUT"]


        elif len(uri) == 5 and uri[0] == "stations":

            if uri[2] == "sensors" and uri[3] == "temperature":
                if uri[4] == "sensor_name":
                    station_name = uri[1]
                    return self.sensors(station_name)["temperature"][0]["sensor_name"]

                elif uri[4] == "sensor_id":
                    station_name = uri[1]
                    return self.sensors(station_name)["temperature"][0]["sensor_id"]

                elif uri[4] == "unit":
                    station_name = uri[1]
                    return self.sensors(station_name)["temperature"][0]["unit"]

                elif uri[4] == "sensor_topic":
                    station_name = uri[1]
                    return self.sensors(station_name)["temperature"][0]["sensor_topic"]

        else:
            raise cherrypy.HTTPError(400, "Wrong URI")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        body = cherrypy.request.body.read()
        json_body = json.loads(body)

        if "settings" in json_body and "services" in json_body["settings"]:
            service_type = list(json_body["settings"]["services"].keys())[0]
            service_info = json_body["settings"]["services"][service_type]
            if service_type not in self.catalog.get("settings", {}).get("services", {}):
                self.catalog["settings"]["services"][service_type] = {}
            self.catalog["settings"]["services"][service_type] = service_info
            self.save_catalog()
            return {"message": "Service added successfully"}
        else:
            raise cherrypy.HTTPError(400, "Bad Request")

    # @cherrypy.tools.json_in()
    # @cherrypy.tools.json_out()
    # def PUT(self, *uri):
    #     if len(uri) == 2 and uri[0] == "update_service":
    #         service_type = uri[1]
    #         data = cherrypy.request.body.read()
    #         data = json.loads(data)
    #         services = self.catalog.get("settings", {}).get("services", {}).get(service_type)
    #         if services is not None:
    #             services.update(data)
    #             self.save_catalog()
    #             return {"message": "Service updated successfully"}
    #         raise cherrypy.HTTPError(404, "Service not found")
    #     else:
    #         raise cherrypy.HTTPError(400, "Wrong URI")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, *uri):
        if len(uri) == 2 and uri[0] == "update_threshold":
            station_name = uri[1]
            data = cherrypy.request.body.read()
            data = json.loads(data)

            for station in self.catalog.get("stations", []):
                if station_name in station:
                    if "threshold" in station[station_name]:
                        station[station_name]["threshold"]["humidity"] = data.get("humidity", 25)
                        self.save_catalog()
                        return {"message": f"Threshold for humidity updated successfully for {station_name}"}
                    else:
                        raise cherrypy.HTTPError(400, "Threshold not found for the specified station")

            raise cherrypy.HTTPError(404, f"Station {station_name} not found")

        else:
            raise cherrypy.HTTPError(400, "Wrong URI")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def DELETE(self, *uri):
        if len(uri) == 2 and uri[0] == "delete_service":
            service_type = uri[1]
            services = self.catalog.get("settings", {}).get("services", {}).get(service_type)
            if services is not None:
                del self.catalog["settings"]["services"][service_type]
                self.save_catalog()
                return {"message": "Service deleted successfully"}
            raise cherrypy.HTTPError(404, "Service not found")

    @cherrypy.tools.json_out()
    def sensors(self, station_name):
        for station in self.catalog.get("stations", []):
            if station_name in station:
                return station[station_name]["sensors"]
        raise cherrypy.HTTPError(404, "Station not found")

    @cherrypy.tools.json_out()
    def device_status(self, station_name):
        for station in self.catalog.get("stations", []):
            if station_name in station:
                return station[station_name]["device_status"]
        raise cherrypy.HTTPError(404, "Station not found")

    @cherrypy.tools.json_out()
    def threshold(self, station_name):
        for station in self.catalog.get("stations", []):
            if station_name in station:
                return station[station_name]["threshold"]
        raise cherrypy.HTTPError(404, "Station not found")

    @cherrypy.tools.json_out()
    def station_list(self):
        return [station for station in self.catalog.get("stations", [])]

    @cherrypy.tools.json_out()
    def project_info(self):
        return {
            "projectOwner": self.catalog.get("projectOwner", ""),
            "projectName": self.catalog.get("projectName", ""),
            "lastUpdate": self.catalog.get("lastUpdate", "")
        }


if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(CatalogAPI(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

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
        if len(uri) == 0:
            return self.catalog
        elif len(uri) == 1:
            field = uri[0]
            if field in self.catalog:
                return self.catalog[field]
        elif len(uri) == 2:
            field = uri[0]
            key = uri[1]
            if field in self.catalog:
                subfield = self.catalog[field]
                if key in subfield:
                    return subfield[key]
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

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, *uri):
        if len(uri) == 2 and uri[0] == "update_service":
            service_type = uri[1]
            data = cherrypy.request.body.read()
            data = json.loads(data)
            services = self.catalog.get("settings", {}).get("services", {}).get(service_type)
            if services is not None:
                services.update(data)
                self.save_catalog()
                return {"message": "Service updated successfully"}
            raise cherrypy.HTTPError(404, "Service not found")
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

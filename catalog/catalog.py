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
        service_type = json_body.get("service_type")
        service_info = json_body.get("service_info")

        if service_type and service_info:
            if service_type not in self.catalog.get("services", {}):
                self.catalog["services"][service_type] = []
            self.catalog["services"][service_type].append(service_info)
            self.save_catalog()
            return {"message": "Service added successfully"}
        else:
            raise cherrypy.HTTPError(400, "Bad Request")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self, *uri):
        if len(uri) == 2 and uri[0] == "update_service":
            service_type = uri[1]
            service_id = cherrypy.request.params.get("service_id")
            data = cherrypy.request.body.read()
            data = json.loads(data)
            services = self.catalog.get("services", {}).get(service_type)
            if services is not None:
                for service in services:
                    if service.get("service_id") == service_id:
                        service.update(data)
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
            service_id = cherrypy.request.params.get("service_id")
            services = self.catalog.get("services", {}).get(service_type)
            if services is not None:
                services[:] = [service for service in services if service.get("service_id") != service_id]
                self.save_catalog()
                return {"message": "Service deleted successfully"}
            raise cherrypy.HTTPError(404, "Service not found")

    @cherrypy.tools.json_out()
    def sensors(self, sensor_type):
        if sensor_type in self.catalog.get("sensors", {}):
            return self.catalog["sensors"][sensor_type]
        raise cherrypy.HTTPError(404, "Sensor not found")

    @cherrypy.tools.json_out()
    def services(self, service_type):
        if service_type in self.catalog.get("services", {}):
            return self.catalog["services"][service_type]
        raise cherrypy.HTTPError(404, "Service not found")

    @cherrypy.tools.json_out()
    def threshold(self):
        return self.catalog.get("threshold", {})

    @cherrypy.tools.json_out()
    def telegram_token(self):
        return {"telegram_token": self.catalog.get("telegram_token", "")}

# TODO: update device status
# TODO: show each device status separately



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

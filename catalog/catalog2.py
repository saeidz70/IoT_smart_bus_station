import json
import cherrypy


class Configuration:
    def __init__(self, input_file="catalog.json"):
        self.valid_IDs = []
        self.valid_types = []
        self.load_configuration(input_file)

    def load_configuration(self, input_file):
        with open(input_file, "r") as json_file:
            self.content = json.load(json_file)
            self.services = self.content.get("services", {})
            self.sensors = self.content.get("sensors", {})
            self.threshold = self.content.get("threshold", {})
            self.telegram_token = self.content.get("telegram_token")

        self.service_reader()

    def service_reader(self):
        for service_type, service_data in self.services.items():
            self.valid_types.append(service_type)
            for item in service_data:
                self.valid_IDs.append(item.get("service_id", ""))
        return self.valid_IDs, self.valid_types

    def service_validator(self, *services):
        error_id = "Invalid service ID"
        error_service = "Invalid service type"
        error_request = "Bad request"

        self.service_reader()
        services = list(services[0])
        service_len = len(services)

        if service_len in range(1, 3):
            if services[0] in self.valid_types:
                valid_st = self.services.get(services[0], [])
                if service_len == 1:
                    return valid_st
                elif service_len == 2:
                    if services[1] in self.valid_IDs:
                        for item in valid_st:
                            if item.get("service_id") == services[1]:
                                return item
                        return error_id
            return error_service
        return error_request

    def get_services(self, service_type=None, service_id=None):
        self.service_reader()
        if service_type is None and service_id is None:
            return self.services
        result = self.service_validator(service_type, service_id)
        return result

    def get_sensors(self):
        return self.sensors

    def get_sensor(self, sensor_name):
        return self.sensors.get(sensor_name)

    def set_sensor_status(self, sensor_name, new_status):
        if sensor_name in self.sensors:
            self.sensors[sensor_name]["status"] = new_status
            return True
        return False

    def get_thresholds(self):
        return self.threshold

    def set_threshold(self, sensor_name, new_threshold):
        if sensor_name in self.threshold:
            self.threshold[sensor_name] = new_threshold
            return True
        return False

    def get_telegram_token(self):
        return self.telegram_token


@cherrypy.expose
class WebServices:
    def __init__(self):
        self.config = Configuration()

    @cherrypy.tools.json_out()
    def GET(self, *uri):
        if not uri:
            return {"message": "Welcome to the Web Service! Use /services to retrieve data."}

        if uri and uri[0] == "services":
            if len(uri) == 1:
                return self.config.get_services()
            elif len(uri) >= 2:
                service_info = self.config.service_validator(uri[1:])
                if isinstance(service_info, dict):
                    return service_info
                else:
                    return {"error": "Invalid service ID."}
            return {"error": "Invalid URL. Use /services to retrieve data."}

        elif uri and uri[0] == "sensors":
            if len(uri) == 1:
                return self.config.get_sensors()
            elif len(uri) == 2:
                sensor_name = uri[1]
                sensor_info = self.config.get_sensor(sensor_name)
                if sensor_info:
                    return sensor_info
                else:
                    return {"error": "Sensor not found."}
            return {"error": "Invalid URL for sensors."}

        elif uri and uri[0] == "threshold":
            if len(uri) == 1:
                return self.config.get_thresholds()
            elif len(uri) == 2 and uri[1] in self.config.get_thresholds():
                sensor_name = uri[1]
                return {sensor_name: self.config.get_thresholds()[sensor_name]}
            return {"error": "Invalid URL for threshold."}

        return {"error": "Invalid URL. Use /services, /sensors, or /threshold to retrieve data."}

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        data = cherrypy.request.json
        if "sensor_name" in data and "new_status" in data:
            sensor_name = data["sensor_name"]
            new_status = data["new_status"]
            if self.config.set_sensor_status(sensor_name, new_status):
                return {"message": "Sensor status updated.", "success": True}
            else:
                return {"error": "Sensor not found.", "success": False}
        elif "sensor_name" in data and "new_threshold" in data:
            sensor_name = data["sensor_name"]
            new_threshold = data["new_threshold"]
            if self.config.set_threshold(sensor_name, new_threshold):
                return {"message": "Threshold updated.", "success": True}
            else:
                return {"error": "Sensor not found.", "success": False}
        else:
            return {"error": "Invalid request.", "success": False}


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    }
    cherrypy.tree.mount(WebServices(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

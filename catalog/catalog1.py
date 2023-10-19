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

        self.service_reader()

    def service_reader(self):
        for service_type, service_data in self.services.items():
            self.valid_types.append(service_type)
            print("Service:", service_type)
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

    def get_services(self, service_type, service_id):
        self.service_reader()
        result = self.service_validator(service_type, service_id)
        return result


@cherrypy.expose
class WebServices:
    def __init__(self):
        self.config = Configuration()

    def GET(self, *uri):
        if not uri:
            return "Welcome to the Web Service! Use /services to retrieve data."

        if uri and uri[0] == "services":
            if len(uri) == 1:
                return json.dumps(self.config.services)
            elif len(uri) >= 2:
                return json.dumps(self.config.service_validator(uri[1:]))

        return "Invalid URL. Use /services to retrieve data."

    def POST(self):
        return True

    @staticmethod
    def response_json(result, success):
        temp_json = {"result": result, "success": success}
        return json.dumps(temp_json)


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(WebServices(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()

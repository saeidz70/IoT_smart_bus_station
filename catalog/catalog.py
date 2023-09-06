import json
import cherrypy


class Configuration(object):
    def __init__(self, input_file="catalog.json"):
        self.services = None
        self.rest = None
        with open(input_file, "r") as json_file:
            self.content = json.load(json_file)
            self.services = self.content["services"]
            self.valid_IDs = []
            self.valid_types = []

    def service_reader(self):
        for service in self.services:
            self.valid_types.append(service)
            print("this is the service", service)
            for ID in self.services[service]:
                self.valid_IDs.append(ID["service_id"])
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
                valid_st = self.services[services[0]]
                if service_len == 1:
                    return valid_st
                elif service_len == 2:
                    if services[1] in self.valid_IDs:
                        for i in range(len(valid_st)):
                            if valid_st[i]["service_id"] == services[1]:
                                return valid_st[i]
                    else:
                        return error_id
            else:
                return error_service
        else:
            return error_request

    def get_services(self, service_type, service_id):
        self.service_reader()
        result = self.service_validator(service_type, service_id)
        return result


@cherrypy.expose
class WebServices(object):
    def __init__(self):
        self.config = Configuration()

        pass

    def GET(self, *uri):
        error = "Bad Request"
        if uri[0] == "services":
            if len(uri) == 1:
                return json.dumps(self.config.services)
            elif len(uri) >= 2:
                return json.dumps(self.config.service_validator(uri[1:]))
        else:
            return error

    def POST(self):
        return True

    def response_json(self, result, success):
        tempJson = {"result": result, "success": success}
        return json.dumps(tempJson)


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

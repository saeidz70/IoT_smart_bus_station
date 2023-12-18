import cherrypy
import json
import requests


class ActuatorServer:
    exposed = True

    @cherrypy.tools.json_out()
    def PUT(self):
        body = cherrypy.request.body.read()
        json_body = json.loads(body)
        print("json_body: ", json_body)

        # Prepare data for the request
        # data = json.dumps(json_body)
        uri = "http://127.0.0.1:8080/"
        message = {"address": ["stations", "station_1", "device_status"], "data": json_body}
        print("message: ", message)

        # Send the request
        response = requests.put(uri, json=message)

        # Extract relevant information from the response
        response_data = {
            "status_code": response.status_code,
            "content": response.text
        }

        return response_data


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(ActuatorServer(), '/', conf)
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.engine.start()
    cherrypy.engine.block()

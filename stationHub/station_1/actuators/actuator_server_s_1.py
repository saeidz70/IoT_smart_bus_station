import cherrypy
import json
import requests


class ActuatorServer:
    exposed = True

    def GET(self, *uri):
        return

    @cherrypy.tools.json_out()
    def PUT(self):
        body = cherrypy.request.body.read()
        json_body = json.loads(body)
        # Actuator activate or deactivate a device in the station
        uri = "http://127.0.0.1:8080/"
        response = requests.put(uri, json=json_body)
        response_data = {
            "status_code": response.status_code,
            "content": response.text
        }
        print(f'''In the {json_body["address"][1]}: 
              cooler is {json_body["data"]["cooler"]}
              heater is {json_body["data"]["heater"]}
              dehumidifier is {json_body["data"]["dehumidifier"]}
              lights are {json_body["data"]["light"]}''')
        return response_data


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(ActuatorServer(), '/station_1', conf)
    cherrypy.config.update({'server.socket_port': 9010})
    cherrypy.engine.start()
    cherrypy.engine.block()

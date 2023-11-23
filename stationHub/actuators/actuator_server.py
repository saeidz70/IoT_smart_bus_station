import cherrypy
import json


class ActuatorServer:
    exposed = True

    @cherrypy.tools.json_out()
    def PUT(self):
        body = cherrypy.request.body.read()
        json_body = json.loads(body)
        print(json_body)
        return json_body

# TODO: send device_status to catalog


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
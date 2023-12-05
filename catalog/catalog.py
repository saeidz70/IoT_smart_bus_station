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
        for key, value in self.catalog.items():
            if len(uri) == 0:
                welcome_message = ("This is a web service for Smart Bus Station. For more information please visit "
                                   "our Github: https://github.com/saeidz70/IoT_smart_bus_station")
                return welcome_message

            elif len(uri) == 1 and key == uri[0]:
                if isinstance(value, dict):
                    return list(value.keys())
                else:
                    return value

            elif len(uri) == 2 and key == uri[0]:
                for a, b in value.items():
                    if a == uri[1]:
                        if isinstance(b, dict):
                            return list(b.keys())
                        else:
                            return b

            elif len(uri) == 3 and key == uri[0]:
                for c, d in value.items():
                    if c == uri[1]:
                        for e, f in d.items():
                            if e == uri[2]:
                                if isinstance(f, dict):
                                    return list(f.keys())
                                else:
                                    return f

            elif len(uri) == 4 and key == uri[0]:
                for g, h in value.items():
                    if g == uri[1]:
                        for i, j in h.items():
                            if i == uri[2]:
                                for k, l in j.items():
                                    if k == uri[3]:
                                        if isinstance(l, dict):
                                            return list(l.keys())
                                        else:
                                            return l

            elif len(uri) == 5 and key == uri[0]:
                for m, n in value.items():
                    if m == uri[1]:
                        for o, p in n.items():
                            if o == uri[2]:
                                for q, r in p.items():
                                    if q == uri[3]:
                                        for s, t in r.items():
                                            if s == uri[4]:
                                                if isinstance(t, dict):
                                                    return list(t.keys())
                                                else:
                                                    return t

            elif len(uri) == 6 and key == uri[0]:
                for u, v in value.items():
                    if u == uri[1]:
                        for w, x in v.items():
                            if w == uri[2]:
                                for y, z in x.items():
                                    if y == uri[3]:
                                        for alpha, beta in z.items():
                                            if alpha == uri[4]:
                                                for gamma, epsylun in beta.items():
                                                    if gamma == uri[5]:
                                                        return epsylun
        else:
            raise cherrypy.HTTPError(400, "Wrong URI")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        body = cherrypy.request.json
        address = body["address"]
        value = body["value"]

        if len(address) == 1:
            self.catalog[address[0]] = value
            self.save_catalog()
            return self.catalog[address[0]]

        elif len(address) == 2:
            for i, j in self.catalog.items():
                if address[0] == i:
                    if isinstance(j, dict):
                        j[address[1]] = value
                        self.save_catalog()
                        return j[address[1]]

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
    @cherrypy.expose
    def DELETE(self, *uri):
        for key, value in self.catalog.items():
            if len(uri) == 1 and key == uri[0]:
                del self.catalog[uri[0]]
                self.save_catalog()
                return
            elif len(uri) == 2 and key == uri[0]:
                for a, b in value.items():
                    if a == uri[1]:
                        if isinstance(b, dict):
                            return '''take care of what you are doing!!!'''
                        else:
                            del self.catalog[uri[0]][uri[1]]
                            self.save_catalog()
                            return b

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

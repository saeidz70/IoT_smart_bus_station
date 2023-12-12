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
                return value

            elif len(uri) == 2 and key == uri[0]:
                for a, b in value.items():
                    if a == uri[1]:
                        return b

            elif len(uri) == 3 and key == uri[0]:
                for c, d in value.items():
                    if c == uri[1]:
                        for e, f in d.items():
                            if e == uri[2]:
                                return f

            elif len(uri) == 4 and key == uri[0]:
                for g, h in value.items():
                    if g == uri[1]:
                        for i, j in h.items():
                            if i == uri[2]:
                                for k, l in j.items():
                                    if k == uri[3]:
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
                                                for gamma, epsilon in beta.items():
                                                    if gamma == uri[5]:
                                                        return epsilon
        else:
            raise cherrypy.HTTPError(400, "Wrong URI")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        body = cherrypy.request.json
        address = body["address"]
        data = body["data"]

        for key, value in self.catalog.items():
            if len(address) == 1:
                self.catalog[address[0]] = data
                self.save_catalog()
                return f"Your item is successfully added to catalog: {self.catalog[address[0]]}"

            elif len(address) == 2 and address[0] == key:
                value[address[1]] = data
                self.save_catalog()
                return f"Your item is successfully added to catalog: {value[address[1]]}"

            elif len(address) == 3 and address[0] == key:
                for a, b in value.items():
                    if address[1] == a:
                        b[address[2]] = data
                        self.save_catalog()
                        return f"Your item is successfully added to catalog: {b[address[2]]}"

            elif len(address) == 4 and address[0] == key:
                for c, d in value.items():
                    if address[1] == c:
                        for e, f in d.items():
                            if address[2] == e:
                                f[address[3]] = data
                                self.save_catalog()
                                return f"Your item is successfully added to catalog: {f[address[3]]}"

            elif len(address) == 5 and address[0] == key:
                for g, h in value.items():
                    if address[1] == g:
                        for i, j in h.items():
                            if address[2] == i:
                                for k, l in j.items():
                                    if address[3] == k:
                                        l[address[4]] = data
                                        self.save_catalog()
                                        return f"Your item is successfully added to catalog: {l[address[4]]}"

            elif len(address) == 6 and address[0] == key:
                for m, n in value.items():
                    if address[1] == m:
                        for o, p in n.items():
                            if address[2] == o:
                                for q, r in p.items():
                                    if address[3] == q:
                                        for s, t in r.items():
                                            if address[4] == s:
                                                t[address[5]] = data
                                                self.save_catalog()
                                                return f"Your item is successfully added to catalog: {t[address[5]]}"
        else:
            raise cherrypy.HTTPError(400, "Wrong Request")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def PUT(self):
        body = cherrypy.request.json
        address = body["address"]
        data = body["data"]

        for key, value in self.catalog.items():
            if len(address) == 1:
                self.catalog[address[0]] = data
                self.save_catalog()
                return f"Your item is successfully added to catalog: {self.catalog[address[0]]}"

            elif len(address) == 2 and address[0] == key:
                value[address[1]] = data
                self.save_catalog()
                return f"Your item is successfully added to catalog: {value[address[1]]}"

            elif len(address) == 3 and address[0] == key:
                for a, b in value.items():
                    if address[1] == a:
                        b[address[2]] = data
                        self.save_catalog()
                        return f"Your item is successfully added to catalog: {b[address[2]]}"

            elif len(address) == 4 and address[0] == key:
                for c, d in value.items():
                    if address[1] == c:
                        for e, f in d.items():
                            if address[2] == e:
                                f[address[3]] = data
                                self.save_catalog()
                                return f"Your item is successfully added to catalog: {f[address[3]]}"

            elif len(address) == 5 and address[0] == key:
                for g, h in value.items():
                    if address[1] == g:
                        for i, j in h.items():
                            if address[2] == i:
                                for k, l in j.items():
                                    if address[3] == k:
                                        l[address[4]] = data
                                        self.save_catalog()
                                        return f"Your item is successfully added to catalog: {l[address[4]]}"

            elif len(address) == 6 and address[0] == key:
                for m, n in value.items():
                    if address[1] == m:
                        for o, p in n.items():
                            if address[2] == o:
                                for q, r in p.items():
                                    if address[3] == q:
                                        for s, t in r.items():
                                            if address[4] == s:
                                                t[address[5]] = data
                                                self.save_catalog()
                                                return f"Your item is successfully added to catalog: {t[address[5]]}"
        else:
            raise cherrypy.HTTPError(400, "Wrong Request")

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def DELETE(self, *uri):
        for a, b in self.catalog.items():
            if a == uri[0]:
                if len(uri) == 1:
                    if isinstance(b, dict) and len(b) != 0:
                        return '''take care of what you are doing!!!'''
                    else:
                        del self.catalog[uri[0]]
                        self.save_catalog()
                        return b
                else:
                    for c, d in b.items():
                        if c == uri[1]:
                            if len(uri) == 2:
                                if isinstance(d, dict) and len(d) != 0:
                                    return '''take care of what you are doing!!!'''
                                else:
                                    del self.catalog[uri[0]][uri[1]]
                                    self.save_catalog()
                                    return d
                            else:
                                for e, f in d.items():
                                    if e == uri[2]:
                                        if len(uri) == 3:
                                            if isinstance(f, dict) and len(f) != 0:
                                                return '''take care of what you are doing!!!'''
                                            else:
                                                del self.catalog[uri[0]][uri[1]][uri[2]]
                                                self.save_catalog()
                                                return f
                                        else:
                                            for g, h in f.items():
                                                if g == uri[3]:
                                                    if len(uri) == 4:
                                                        if isinstance(h, dict) and len(h) != 0:
                                                            return '''take care of what you are doing!!!'''
                                                        else:
                                                            del self.catalog[uri[0]][uri[1]][uri[2]][uri[3]]
                                                            self.save_catalog()
                                                            return h
                                                    else:
                                                        for i, j in h.items():
                                                            if i == uri[4]:
                                                                if len(uri) == 5:
                                                                    if isinstance(j, dict) and len(j) != 0:
                                                                        return '''take care of what you are doing!!!'''
                                                                    else:
                                                                        del \
                                                                            self.catalog[uri[0]][uri[1]][uri[2]][
                                                                                uri[3]][
                                                                                uri[4]]
                                                                        self.save_catalog()
                                                                        return j
                                                                else:
                                                                    for k, l in j.items():
                                                                        if k == uri[5]:
                                                                            if len(uri) == 6:
                                                                                if isinstance(l, dict) and len(l) != 0:
                                                                                    return '''take care of what you 
                                                                                    are doing!!!'''
                                                                                else:
                                                                                    del self.catalog[uri[0]][uri[1]][
                                                                                        uri[2]][uri[3]][uri[4]][
                                                                                        uri[5]]
                                                                                    self.save_catalog()
                                                                                    return l
                                                                            else:
                                                                                raise cherrypy.HTTPError("URI is not "
                                                                                                         "Valid")
        else:
            raise cherrypy.HTTPError(400, "Wrong Request")


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

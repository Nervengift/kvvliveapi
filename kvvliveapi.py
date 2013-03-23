#!/usr/bin/env python

import urllib.request
import json

API_KEY = "377d840e54b59adbe53608ba1aad70e8&_=1364044820820"
API_BASE = "http://live.kvv.de/webapp/"

class Stop:
    def __init__(self, name, id, lat, lon):
        self.name = name
        self.id = id
        self.lat = lat
        self.lon = lon

    def from_json(json):
        return Stop(json["name"], json["id"], json["lat"], json["lon"])


def query(path):
    url = API_BASE + path + "?key=" + API_KEY
    req = urllib.request.Request(url)

    try:
        handle = urllib.request.urlopen(req)
    except IOError as e:
        print("error!")
        if hasattr(e, "code"):
            if e.code != 403:
                print("We got another error")
                print(e.code)
            else:
                print(e.headers)
                print(e.headers["www-authenticate"])
        return None; #TODO: Schoenere Fehlerbehandlung

    return json.loads(handle.read().decode())

def search_by_name(name):
    json = query("stops/byname/" + name) #TODO: url encode
    stops = []
    if json:
        for stop in json["stops"]:
            stops.append(Stop.from_json(stop))
    return stops


if __name__ == "__main__":
    for stop in search_by_name("Marktplatz"):
        print(stop.name)

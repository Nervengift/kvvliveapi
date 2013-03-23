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

class Departure:
    def __init__(self, route, destination, direction, time, vehicle_type, lowfloor, realtime, traction, stop_position):
        self.route = route
        self.destination = destination
        self.direction = direction
        self.time = time #TODO: to timestamp?
        self.vehicle_type = vehicle_type
        self.lowfloor = lowfloor
        self.realtime = realtime
        self.traction = traction
        self.stop_position = stop_position

    def from_json(json):
        return Departure(json["route"], json["destionation"], json["direction"], json["time"], json["vehicleType"], json["lowfloor"], json["realtime"], json["traction"], json["stopPosition"])


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

def search_by_latlon(lat, lon):
    json = query("stops/bylatlon/" + lat + "/" + lon)
    stops = []
    if json:
        for stop in json["stops"]:
            stops.append(Stop.from_json(stop))
    return stops

def get_departures(id, max_info=10):
    json = query("departures/bystop/" + id + "?maxInfo=" + max_info)
    departures = []
    if json:
        for dep in json["departures"]:
            departures.append(dep)
    return departures


if __name__ == "__main__":
    for stop in search_by_name("Marktplatz"):
        print(stop.name)

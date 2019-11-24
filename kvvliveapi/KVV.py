#!/usr/bin/env python
# author: Clemens "Nervengift"

try:
    import urllib.request as _urllib
    from urllib.parse import quote_plus,urlencode
except ImportError:
    import urllib2 as _urllib
    from urllib import quote_plus,urlencode
from datetime import datetime,timedelta
import re
import json
import re
import sys

API_KEY = "377d840e54b59adbe53608ba1aad70e8"
API_BASE = "https://live.kvv.de/webapp/"

class Stop:
    def __init__(self, name, stop_id, lat, lon):
        self.name = name
        self.stop_id = stop_id
        self.lat = lat
        self.lon = lon

    @staticmethod
    def from_json(json):
        return Stop(json["name"], json["id"], json["lat"], json["lon"])

    def __repr__(self):
        return "Stop(name={}, stop_id={}, lat={}, lon={})".format(
            self.name, self.stop_id, self.lat, self.lon
        )


class Departure:
    def __init__(self, route, destination, direction, time, lowfloor, realtime, traction, stopPosition):
        self.route = route
        self.destination = destination
        self.direction = direction
        self.timestr = time #TODO: to timestamp?
        self.lowfloor = lowfloor
        self.realtime = realtime
        self.traction = traction
        self.time = self._str_to_time(time)
        self.stopPosition = stopPosition

    def _str_to_time(self, timestr):
        """ _str_to_time converts a time string as given in the API response to da datetime.datetime """
        time = datetime.now()

        # "0" ("sofort")
        if timestr == "sofort":
            return time

        # "5 min"
        re_min = re.compile("^([1-9]) min$")
        match = re_min.match(timestr)
        if match:
            time += timedelta(minutes=int(match.group(1)))
            return time

        # 14:23
        re_time = re.compile("^([0-2]?[0-9]):([0-5][0-9])$")
        match = re_time.match(timestr)
        if match:
            hours = int(match.group(1))
            mins = int(match.group(2))
            time_new = time.replace(hour=hours, minute=mins)
            if time_new < time:
                time_new += timedelta(days=1)
            time = time_new
            return time

    @staticmethod
    def from_json(json):
        time = json["time"]
        if time == "0":
            time = "sofort"

        # stopPosition either has been banned from json or is not defined for all stops
        if "stopPosition" in json:
            stopPosition = json["stopPosition"]
        else:
            stopPosition = None

        return Departure(json["route"], json["destination"], json["direction"], time, json["lowfloor"], json["realtime"], json["traction"], stopPosition)

    def pretty_format(self, alwaysrelative=False):
        if alwaysrelative and self.timestr != "sofort":
            mins = int((self.time - datetime.now()).total_seconds() / 60)
            timestr = "{:>3} min".format(mins)
        else:
            timestr = self.timestr
        return timestr + ("  " if self.realtime else "* ") + (" " if timestr != "sofort" else "") + self.route + " " + self.destination

    def __repr__(self):
        return "Departure(route={}, destination={}, direction={}, time={})"\
            .format(self.route, self.destination, self.direction, self.time)


def _query(path, params = {}):
    params["key"] = API_KEY
    url = API_BASE + path + "?" + urlencode(params)
    req = _urllib.Request(url)

    #try:
    handle = _urllib.urlopen(req)
    #except IOError as e:
    #    if hasattr(e, "code"):
    #        if e.code != 403:
    #            print("We got another error")
    #            print(e.code)
    #        else:
    #            print(e.headers)
    #            print(e.headers["www-authenticate"])
    #    return None; #TODO: Schoenere Fehlerbehandlung

    return json.loads(handle.read().decode("utf8"))

def _search(query):
    json = _query(query)
    stops = []
    if json:
        for stop in json["stops"]:
            stops.append(Stop.from_json(stop))
    return stops

def search_by_name(name):
    """ Search for stops by name
        returns a list of Stop objects
    """
    return _search("stops/byname/" + quote_plus(name))

def search_by_latlon(lat, lon):
    """ Search for stops by latitude and longitude
        returns a list of Stop objectss
    """
    return _search("stops/bylatlon/" + lat + "/" + lon)

def search_by_stop_id(stop_id):
    """ Search for a stop by its stop_id
        returns a list that should contain only one stop
    """
    return [Stop.from_json(_query("stops/bystop/" + stop_id))]

def _get_departures(query, max_info=10):
    json = _query(query, {"maxInfos" : str(max_info)})
    departures = []
    if json:
        for dep in json["departures"]:
            departures.append(Departure.from_json(dep))
    return departures


def get_departures(stop_id, max_info=10):
    """ Return a list of Departure objects for a given stop stop_id
        optionally set the maximum number of entries
    """
    return _get_departures("departures/bystop/" + stop_id, max_info)

def get_departures_by_route(stop_id, route, max_info=10):
    """ Return a list of Departure objects for a given stop stop_id and route
        optionally set the maximum number of entries
    """
    return _get_departures("departures/byroute/" + route + "/" + stop_id, max_info)

def errorstring(e):
    if hasattr(e, "code"):
        return {400: "invalid stop id or route",
                404: "not found"}.get(e.code, "http error " + str(e.code))
    else:
        return "unknown error"

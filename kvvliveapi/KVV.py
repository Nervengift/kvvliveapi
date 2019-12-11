#!/usr/bin/env python
# author: Clemens "Nervengift"

import requests
from datetime import datetime, timedelta

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
        return "Stop(name={0.name}, stop_id={0.stop_id}, lat={0.lat}, lon={0.lon})".format(self)


class Departure:
    def __init__(self, route, destination, direction, time, lowfloor, realtime, traction, stopPosition):
        self.route = route
        self.destination = destination
        self.direction = direction
        self.timestr = time  # TODO: to timestamp?
        self.lowfloor = lowfloor
        self.realtime = realtime
        self.traction = traction
        self.time = self._str_to_time(time)
        self.stopPosition = stopPosition

    def _str_to_time(self, timestr):
        """ _str_to_time converts a time string as given in the API response to da datetime.datetime """
        now = datetime.now()

        try:
            now += datetime.strptime(timestr, '%M min') - datetime(1900, 1, 1)
        except ValueError:  # timestr is not formatted as "xx min"
            pass

        try:
            time = datetime.strptime(timestr, '%H:%M') - datetime(1900, 1, 1)
        except ValueError:  # timestr is not formatted as "hour:min"
            pass
        else:  # Get the elapsed time since midnight and add up to 24h.
            since_midnight = now - now.replace(hour=0, minute=0, second=0, microsecond=0)
            now += (time-since_midnight-timedelta(days=1)) % timedelta(days=1)

        return now

    @staticmethod
    def from_json(json):
        time = "sofort" if json["time"] == "0" else json["time"]

        # stopPosition either has been banned from json or is not defined for all stops
        stopPosition = json.get("stopPosition", None)

        return Departure(json["route"],
                         json["destination"],
                         json["direction"],
                         time,
                         json["lowfloor"],
                         json["realtime"],
                         json["traction"],
                         stopPosition)

    def pretty_format(self, alwaysrelative=False):
        if alwaysrelative and self.timestr != "sofort":
            mins = int((self.time - datetime.now()).total_seconds() / 60)
            timestr = "{:>3} min".format(mins)
        else:
            timestr = self.timestr

        output = timestr + "  " if self.realtime else "* "
        output += " " if timestr != "sofort" else ""

        return "{0}{1.route} {1.destination}".format(output, self)

    def __repr__(self):
        return "Departure(route={}, destination={}, direction={}, time={})"\
            .format(self.route, self.destination, self.direction, self.time)


def _query(path, params={}):
    params["key"] = API_KEY
    response = requests.get("{}{}".format(API_BASE, path), params=params)
    return response.json()


def _search(query):
    json = _query(query) or []
    return [Stop.from_json(stop) for stop in json["stops"]]


def search_by_name(name):
    """ Search for stops by name
        returns a list of Stop objects
    """
    return _search("stops/byname/" + requests.utils.requote_uri(name))


def search_by_latlon(lat, lon):
    """ Search for stops by latitude and longitude
        returns a list of Stop objectss
    """
    return _search("stops/bylatlon/{}/{}".format(lat, lon))


def search_by_stop_id(stop_id):
    """ Search for a stop by its stop_id
        returns a list that should contain only one stop
    """
    return [Stop.from_json(_query("stops/bystop/{}".format(stop_id)))]


def _get_departures(query, max_info=10):
    json = _query(query, {"maxInfos": str(max_info)}) or []
    return [Departure.from_json(dep) for dep in json["departures"]]


def get_departures(stop_id, max_info=10):
    """ Return a list of Departure objects for a given stop stop_id
        optionally set the maximum number of entries
    """
    return _get_departures("departures/bystop/" + stop_id, max_info)

def get_departures_by_route(stop_id, route, max_info=10):

    """ Return a list of Departure objects for a given stop stop_id and route
        optionally set the maximum number of entries
    """
    return _get_departures("departures/byroute/{}/{}".format(route, stop_id), max_info)


def errorstring(e):
    if hasattr(e, "code"):
        return {400: "invalid stop id or route",
                404: "not found"}.get(e.code, "http error " + str(e.code))
    else:
        return "unknown error"
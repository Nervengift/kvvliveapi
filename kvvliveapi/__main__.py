from kvvliveapi.KVV import *

if __name__ == "__main__":
    try:
        if len(sys.argv) == 3 and sys.argv[1] == "search":
            if sys.argv[2].startswith("de:"):
                for stop in search_by_stop_id(sys.argv[2]):
                    print(stop.name + " (" + stop.stop_id + ")")
            else:
                for stop in search_by_name(sys.argv[2]):
                    print(stop.name + " (" + stop.stop_id + ")")
        elif len(sys.argv) == 4 and sys.argv[1] == "search":
            for stop in search_by_latlon(sys.argv[2], sys.argv[3]):
                print(stop.name + " (" + stop.stop_id + ")")
        elif len(sys.argv) == 3 and sys.argv[1] == "departures":
            for dep in get_departures(sys.argv[2]):
                print(dep.pretty_format())
        elif len(sys.argv) == 4 and sys.argv[1] == "departures":
            for dep in get_departures_by_route(sys.argv[2], sys.argv[3]):
                print(dep.pretty_format())
        else:
            print("No such command. Try \"search <name>/<stop_id>/<lat> <lon>\" or \"departures <stop stop_id> [<route>]\"")
    except IOError as e:
       sys.stderr.write("{}\n".format(errorstring(e)));

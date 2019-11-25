"""KVV Live API python bindings

Usage:
    kvvliveapi search <station>
    kvvliveapi search <lat> <lon>
    kvvliveapi departures <station>
    kvvliveapi departures <station> <line>
    kvvliveapi (-v | --version | -h | --help)

Options:
  -h --help         Show this screen.
  -v --version      Show version.

"""

VERSION = '0.1.4'

from docopt import docopt
from kvvliveapi.KVV import *

if __name__ == "__main__":
    arguments = docopt(__doc__, version=VERSION)
    if arguments['search'] and arguments['<station>']:
        if arguments['<station>'].startswith('de:'):
            for stop in search_by_stop_id(arguments['<station>']):
                print(stop.name + " (" + stop.stop_id + ")")
        else:
            for stop in search_by_name(arguments['<station>']):
                print(stop.name + " (" + stop.stop_id + ")")
    elif arguments['search'] and arguments['<lat>'] and arguments['<lon>']:
        for stop in search_by_latlon(arguments['<lat>'], arguments['<lon>']):
            print(stop.name + " (" + stop.stop_id + ")")
    elif arguments['departures'] and arguments['<station>']:
        if arguments['<line>']:
            for dep in get_departures_by_route(arguments['<station>'], arguments['<line>']):
                print(dep.pretty_format())
        else:
            for dep in get_departures(arguments['<station>']):
                print(dep.pretty_format())

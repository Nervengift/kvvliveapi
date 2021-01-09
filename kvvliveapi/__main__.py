"""KVV Live API python bindings

Usage:
    kvvliveapi search <station>
    kvvliveapi search <lat> <lon>
    kvvliveapi departures <station> [options]
    kvvliveapi departures <station> <line> [options]
    kvvliveapi (-v | --version | -h | --help)

Options:
  --always-relative         Always display realtive time. [default: False]
  --limit-results <lim>     Limits the number of results to show [default: 10]

  -h --help                 Show this screen.
  -v --version              Show version.

"""

VERSION = '0.2.1'

from docopt import docopt
from kvvliveapi.KVV import *

if __name__ == "__main__":
    arguments = docopt(__doc__, version=VERSION)
    if arguments['search'] and arguments['<station>']:
        for stop in search_by_name(arguments['<station>']):
            print('{} ({})'.format(stop.name, stop.stop_id))
    elif arguments['search'] and arguments['<lat>'] and arguments['<lon>']:
        for stop in search_by_latlon(arguments['<lat>'], arguments['<lon>']):
            print('{} ({})'.format(stop.name, stop.stop_id))
    elif arguments['departures'] and arguments['<station>']:
        for dep in get_departures(arguments['<station>'],
                                  arguments['<line>'],
                                  arguments['--limit-results']):
            print(dep.pretty_format(arguments['--always-relative']))

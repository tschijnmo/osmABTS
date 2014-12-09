"""
The main driver for the code
============================

The current package can be used both as a library and as a standalone program.
When used stand alone, it is able to simulation the mean time spent on
travelling by the travellers. And it can also optionally perform a sensitivity
analysis towards the graph or runs optional script.

"""

from __future__ import print_function

import argparse
import code

from .model import Model
from .network import print_network, draw_network
from .places import print_places
from .travellers import print_travellers
from .simultime import simul_travel_time, test_sentivity_edges


def main():

    """The main driver function"""

    parser = argparse.ArgumentParser(
        description='Perform agent based traffic simulation on OSM map'
        )
    parser.add_argument(
        'map', metavar='OSM XML map', nargs=1,
        help='The map on which to perform simulation'
        )
    parser.add_argument(
        '--verbose', '-v', action='store_true', default=False,
        help='Print information verbosely'
        )
    parser.add_argument(
        '--draw', '-d', action='store', type=str,
        metavar='FILE',
        help='Plots the graph to file'
        )
    parser.add_argument(
        '--travellers', '-t', type=int, action='store', default=100,
        help='The number of travellers to simulate'
        )
    parser.add_argument(
        '--time', '-T', type=float, action='store', default=5.0,
        help='The number of weeks of time to simulation'
        )
    parser.add_argument(
        '--sensitivity', '-s', action='store_true', default=False,
        help='Perform sensitivity analysis (slow!)'
        )
    parser.add_argument(
        '--script', '-S', action='store',
        help='Run script after the simulation'
        )

    args = parser.parse_args()

    print('*' * 80)
    print('Activity-based traffic simulation on OSM map'.center(80))
    print('*' * 80)
    print('\n\n\n')

    model = Model(args.map)
    print('Map file %s successfully parsed...' % args.map)

    model.form_network()
    print('Network successfully formed...')
    model.form_places()
    print('Places of interest recognized...')
    model.form_travellers(args.travellers)
    print(' %d travellers successfully generated ...' % args.travellers)
    model.gen_trips(args.time)
    print(' Trips for %f weeks of time successfully generated' % args.time)

    if args.verbose:
        print_network(model.network)
        print_places(model.network, model.places)
        print_travellers(model.networ, model.travellers)

    if args.draw is not None:
        draw_network(model.net, args.draw)

    mean_time = simul_travel_time(model)
    print('Mean travel time per traveller per week %f hours' % mean_time)

    if args.sensitivity:
        test_sentivity_edges(model, mean_time)

    if args.script is not None:
        print('Running custom python script %s' % args.script)
        try:
            source = open(args.script, 'r').read()
        except IOError:
            print('Unable to open script')
            raise
        interpreter = code.InteractiveInterpreter(locas={'model': model})
        interpreter.runcode(source, filename=args.script)

    return 0









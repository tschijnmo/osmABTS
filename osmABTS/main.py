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

import networkx as nx

from .model import Model
from .network import print_network, draw_network
from .places import print_places
from .travellers import print_travellers
from .simultime import simul_travel_time, test_sensitivity_edges


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

    print('\n\n\n')
    print('*' * 80)
    print('Activity-based traffic simulation on OSM map'.center(80))
    print('*' * 80)
    print('\n\n\n')

    model = Model(args.map[0])
    print('Map file %s successfully parsed...' % args.map[0])

    model.form_network()
    print('Network successfully formed...')
    print(' %d nodes and %d edges' % (
        model.network.number_of_nodes(), model.network.number_of_edges()
        ))

    model.form_places()
    print('Places of interest recognized...')
    for cat_name, places_list in model.places.iteritems():
        print('     %s: %d' % (cat_name, len(places_list)))

    model.form_travellers(args.travellers)
    print(' %d travellers successfully generated ...' % args.travellers)

    model.gen_trips(args.time)
    print('Trips for %f weeks of time successfully generated' % args.time)
    print('  total number %d' % len(model.trips))

    if args.verbose:
        print_network(model.network)
        print_places(model.network, model.places)
        print_travellers(model.network, model.travellers)

    if args.draw is not None:
        draw_network(model.network, args.draw)
        print('Network drawn to file %s' % args.draw)

    mean_time = simul_travel_time(model)
    print('Mean travel time per traveller per week %f hours' % mean_time)

    if args.sensitivity:
        test_sensitivity_edges(model, mean_time)

    if args.script is not None:
        print('Running custom python script %s' % args.script)
        execfile(
            args.script, {},
            {'model': model, 'nx': nx}
            )

    return 0









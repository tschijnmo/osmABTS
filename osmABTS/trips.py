"""
Trip generation
===============

This module can be roughtly devided into two parts, the trip description and
trip generation. The trip description part contains mostly class definitions
that can be used to describe kinds of trips, while the trip generation contains
the main driver function to generate a large list of trips based on the
travellers and places. This module is kind of at the centre of the simulation.

.. autofunction:: gen_trips

"""

import random
import collections

from .util import select_place


#
# Trip description
# ----------------
#
# The trips can be roughtly described by two data structures, Location and
# Trip. A location is a location in the ways of a trip, and a trip is a series
# of locations with a mean frequency and variation.
#
# The location can be an attribute of the traveller or a random selection in a
# category of places. It is stored in the ``source`` attribute as one of the
# two constant symbols in this module. And a trip has a frequency stored in the
# ``freq`` attribute in unit of times per week, and ``var`` stores the
# corresponding variation. The list of locations are given in the ``locations``
# attribute, while the actual route is given in the route attribute as a list
# of zero-based indices in the locations list.
#

# constants for the two kinds of locations
TRAVELLER_ATTR = 1
RANDOM_FROM_CAT = 2
# Location class definition
Location = collections.namedtuple(
    'Location',
    ['source', 'value']
    )


Trip = collections.namedtuple(
    'Trip',
    ['freq', 'var', 'locations', 'route']
    )


# The default trip

DEFAULT_TRIPS = [
    # Commuting to work
    Trip(
        freq=5.0, var=1.0,
        locations=[
            Location(source=TRAVELLER_ATTR, value='home'),
            Location(source=TRAVELLER_ATTR, value='work'),
            ],
        route=[0, 1, 0]
        ),
    # Go to a leisure place
    Trip(
        freq=2.0, var=0.5,
        locations=[
            Location(source=TRAVELLER_ATTR, value='home'),
            Location(source=RANDOM_FROM_CAT, value='leisure'),
            ],
        route=[0, 1, 0]
        ),
    # Go to a restaurant
    Trip(
        freq=4.0, var=1.0,
        locations=[
            Location(source=TRAVELLER_ATTR, value='home'),
            Location(source=RANDOM_FROM_CAT, value='restaurant'),
            ],
        route=[0, 1, 0]
        ),
    # Go to a church
    Trip(
        freq=1.0, var=0.5,
        locations=[
            Location(source=TRAVELLER_ATTR, value='home'),
            Location(source=TRAVELLER_ATTR, value='church'),
            ],
        route=[0, 1, 0]
        ),
]


#
# Trip generation
# ---------------
#

def _get_places(places, traveller, locations):

    """Gets the actual places described by a list of Locations

    :param places: The places of interest dictionary
    :param traveller: The traveller
    :param locations: The list of locations
    :returns: The corresponding list of :py:class:`places.Place` instances

    """

    result = []

    for loc in locations:

        if loc.source == TRAVELLER_ATTR:
            result.append(
                traveller.attrs[loc.value]
                )
        elif loc.source == RANDOM_FROM_CAT:
            result.append(
                select_place(places[loc.value])
                )
        else:
            assert False

    return result


def gen_trips(time_span, places, trips, traveller):

    """Generates a list of trips for a given traveller

    :param time_span: The time span of the simulation, in weeks
    :param trips: A list of :py:class:`Trip` instances describing the different
        kins of trips that the traveller is capable of
    :param traveller: A :py:class:`travellers.Traveller` instance for the
        traveller
    :returns: A list of lists of places as the trips to be travelled by the
        traveller

    """

    result = []

    for trip in trips:

        freq = random.gauss(trip.freq, trip.var)
        number = int(freq * time_span)
        if number < 1:
            continue

        for i in xrange(0, number):
            trip_places = _get_places(places, traveller, trip.locations)
            result.append(
                [trip_places[i] for i in trip.route]
                )
            continue

    return result

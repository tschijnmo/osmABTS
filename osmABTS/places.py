"""
Places of interest generation
=============================

This module defines a class for places of interest and the functions for
generating the data structure for all of them from the OSM raw data.

Each place of interest will basically just carry the information about its
location in the **network** as the identity of the network node which is
nearest to its actual location. And additionally, a name can be given for it,
as well as a weight that can be used for the random allocation for the
travellers.

The places of interest will be bundled in a dictionary, with the name of the
category as the key and a list of the actual places as the value.

"""

import collections

import numpy as np
from numpy import linalg


class Place(object):

    """The places of interest for the travellers

    Since the category is going to be stored one level upper as the dictionary
    key, here just a few attributes are needed

    .. py:attribute:: node

        The node identity for the place of interest in the network

    .. py::attribute:: name

        The name of the place of interest

    .. py::attribute:: weight

        The weight for it during the place allocation. The probability of being
        selected.

    """

    # pylint: disable=too-few-public-methods

    __slots__ = [
        'node',
        'name',
        'weight',
        ]

    def __init__(self, node, name, weight):

        """Initializes the place instance"""

        self.node = node
        self.name = name
        self.weight = weight


#
# Home generation
# ---------------
#
# The home generation is different from all the other places, since it is going
# to be based on the existance of residential road, rather than specific
# locations on the map.
#
# The generation code will iterate over all the nodes of the graph, find out
# the total length of residential road edges on it, and use that length as the
# weight. For nodes with no residential road, no people will live there.
#

def gen_homes(net):

    """Generates a list of homes for a given network

    :param net: The NetworkX graph for the simulation
    :returns: A list of :py:class:`Place` instances for the homes

    """

    homes = []

    for node in net.nodes_iter():

        weight = 0.0
        for road in net[node].itervalues():
            if road['highway'] == 'residential':
                weight += road['length']

        # 0.01 is an arbitrary delta to skip nodes with few residents
        if weight > 0.01:
            homes.append(
                Place(node, 'home', weight)
                )

    return homes


#
# Place category specification
# ----------------------------
#
# In order to facilitate common treatment for all kinds of places of interest,
# here the information that is needed for the generation of places list is
# bundled in a class (named tuple) for unifying the interface.
#
# Basically all the fields are call back functions with the
# :py:class:`readosm.Node` objects (for fields starting with ``node``) and
# :py:class:`readosm.Way` instances (for fields starting with ``way``) as
# argument. The ``test`` function should return boolean value indicating of
# a node or way is a member of that category, and the ``weight`` functions
# should return a float for the weight for nodes or ways that has been
# tested to be of the category by the testing call back.
#

PlaceCat = collections.namedtuple(
    'PlaceCat',
    [
        'node_test',
        'node_weight',
        'way_test',
        'way_weight',
        ]
    )


#
# Places generation based on the category
# ---------------------------------------
#

def _find_nearest_node_4_coord(net, coord):

    """Finds the node nearest to a coordinate in a network

    Since we just need a rough nearest point on the network, just the longitude
    and latitude coordinate is used as a linear coordinate for the metric
    approximately.

    :param net: The network
    :param coord: The longitude, latitude coordinate as numpy array
    :returns: A node id for the nearest node

    """

    nearest_node = None
    nearest_metric = None

    for node in net.nodes_iter():
        new_metric = linalg.norm(coord - node.coord)
        if nearest_metric is None or new_metric < nearest_metric:
            nearest_metric = new_metric
            nearest_node = node
        else:
            continue

    return nearest_node


def _find_nearest_node_4_node(net, node):

    """Finds the node nearest to a raw node in a network"""

    return _find_nearest_node_4_coord(net, node.coord)


def _find_nearest_node_4_way(net, raw_osm, way):

    """Finds the node nearest to a closed way in a network"""

    node_coords = np.array(
        [raw_osm.nodes[i].coord for i in way.nodes],
        dtype=np.float64
        )
    centre = np.mean(node_coords, axis=0)
    return _find_nearest_node_4_coord(net, centre)


def gen_places(raw_osm, net, place_cat):

    """Generates a list of places for a given category

    :param raw_osm: The raw OSM GIS data, :py:class:`readosm.RawOSM` instance
    :param net: The network formed from the raw data
    :param place_cat: The place category, needs to be :py:class:`PlaceCat`
        instance
    :returns: A list of :py:class:`Place` instances for the places in the map
        for the given category

    """

    places = []

    for node in raw_osm.nodes:

        if place_cat.node_test(node):
            node_id = _find_nearest_node_4_node(net, node)
            name = node.tags['name']
            weight = place_cat.node_weight(node)
            places.append(
                Place(node_id, name, weight)
                )
        else:
            continue

    for way in raw_osm.ways:

        if place_cat.way_test(way):
            node_id = _find_nearest_node_4_way(net, raw_osm, way)
            name = way.tags['name']
            weight = place_cat.way_weight(way)
            places.append(
                Place(node_id, name, weight)
                )
        else:
            continue

    return places


#
# Actual place categories
# -----------------------
#

def _leisure_test(norw):
    """Tests if a node or way is a leisure place"""
    return 'leisure' in norw.tags


# Tags that will exclude a place to be a work place
_WORK_EXCLUDE = [
    'leisure',
    'cuisine',
    'tourism',
    'religion',
    ]


def _test_contain_work_exclude(tags):
    """Tests if a tags contains any keys able to exclude the place as work"""
    return any(
        i in tags for i in _WORK_EXCLUDE
        )


def _work_node_test(node):
    """Tests if a node or way is a work place"""
    tags = node.tags
    return 'name' in tags and (not _test_contain_work_exclude(tags))


def _work_way_test(way):
    """Tests if a way is a work place"""
    tags = way.tags
    return 'building' in tags and (not _test_contain_work_exclude(tags))


def _restaurant_test(norw):
    """Tests if a node or way is a restaurant"""
    return 'cuisine' in norw.tags


def _church_test(norw):
    """Tests if a node or way is a church"""
    return 'religion' in norw.tags


# The default categories
DEFAULT_PLACE_CATS = {
    'work': PlaceCat(node_test=_work_node_test, node_weight=lambda _: 1.0,
                     way_test=_work_way_test, way_weight=lambda _: 10.0),
    'leisure': PlaceCat(node_test=_leisure_test, node_weight=lambda _: 1.0,
                        way_test=_leisure_test, way_weight=lambda _: 1.0),
    'restaurant': PlaceCat(node_test=_restaurant_test,
                           node_weight=lambda _: 1.0,
                           way_test=_restaurant_test,
                           way_weight=lambda _: 1.0),
    'church': PlaceCat(node_test=_church_test, node_weight=lambda _: 1.0,
                       way_test=_church_test, way_weight=lambda _: 1.0),

    }


#
# Driver function
# ---------------
#

def form_places_from_osm(raw_osm, net, place_cats):

    """Forms a dictionary of places

    The homes are formed by the default method, and other places are form by
    the specification in the argument.

    """

    places_dict = {
        'home': gen_homes(net),
        }

    for cat_name, cat in place_cats.iteritems():
        places_dict[cat_name] = gen_places(raw_osm, net, cat)
        continue

    return places_dict

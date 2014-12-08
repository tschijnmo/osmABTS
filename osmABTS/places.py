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

def _gen_homes(net):

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
# Some constance for place generation
# -----------------------------------
#


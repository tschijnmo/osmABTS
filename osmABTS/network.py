"""
Road network formation
======================

The primary purpose of this model is to abstract a road connectivity network
from the complicated OSM raw GIS data. The network is going to be stored as a
NetworkX graph.

The nodes are going to be just the traffic junctions and the dead ends of the
road traffic system. And each node has the original id in the raw OSM data as
their identity, and the coordinate stored in the attribute ``coord``.

Each edge is going to be an undirected edge connecting the nodes. They all have
got the attribute of ``name`` for the name of the road, and the attribute of
``travel_time`` for the time needed to traverse the edge by a common traveller.
Also there is an attribute ``length`` for the length of the actual road and
attribute ``highway`` for the type of the road.

The driver function is in

.. autofunction:: form_network_from_osm

And we have IO functions

.. autofunction:: node2str

.. autofunction:: edge2str

.. autofunction:: print_network

.. autofunction:: draw_network

"""

from __future__ import print_function

import sys
import functools

import networkx as nx
from geopy.distance import vincenty
import matplotlib.pyplot as plt

from .util import print_title


#
# Constants controlling the bahaviour of the code
# -----------------------------------------------
#

# The speed to travel on each kind of highways
# In miles per hour
_HIGHWAY_SPEEDS = {
    'residential': 20.0,
    'primary': 40.0,
    'primary_link': 40.0,
    'secondary': 35.0,
    'secondary_link': 35.0,
    'tertiary': 30.0,
    'motorway': 70.0,
    'motorway_link': 70.0,
}


#
# Utility functions
# -----------------
#

def _calc_distance(coord1, coord2):

    """Calculates the distance between two points

    A shallow wrapper of the geopy Vicinty distance calculator, returns the
    distance in miles.

    """

    return vincenty(coord1, coord2).miles


def _test_if_road(way):

    """Tests if a raw way is a road to consider"""

    tags = way.tags
    return 'highway' in tags and tags['highway'] not in [
        'footway',
        'service',
        ]


#
# The driver function
# -------------------
#

def form_network_from_osm(raw_osm, trim=True):

    """Forms a road network from the raw OSM data

    :param raw_osm: A :py:class:`osmABTS.readosm.RawOSM` instance for the raw
        data
    :param trim: Boolean value indicating if pure connection nodes are going to
        be trimmed out.
    :returns: A networkX graph for the road connectivity

    """

    net = nx.Graph()

    # nodes formation
    nodes = raw_osm.nodes
    for node_id, node in nodes.iteritems():
        net.add_node(node_id)
        net.node[node_id]['coord'] = node.coord

    # edge formation
    for way in raw_osm.ways.itervalues():

        # test if it is actually a road
        if not _test_if_road(way):
            continue
        else:
            tags = way.tags
            highway = tags['highway']

        # connect the nodes in the network

        prev_node_id = None  # The previous node in the network
        # The coordinate of the previous raw node in the OSM data
        prev_coord = nodes[way.nodes[0]].coord
        distance = 0.0

        for node_id in way.nodes:
            node = nodes[node_id]

            # Update the distance
            curr_coord = node.coord
            distance = _calc_distance(curr_coord, prev_coord)
            prev_coord = curr_coord

            # add edge if there is a previous node
            if prev_node_id is not None:
                # Add the new edge
                try:
                    travel_time = distance / _HIGHWAY_SPEEDS[highway]
                except IndexError:
                    raise IndexError(
                        'Unknown highway type %s' % highway
                        )
                net.add_edge(
                    node_id, prev_node_id,
                    travel_time=travel_time, length=distance,
                    highway=highway, name=tags.get('name', '')
                    )

            prev_node_id = node_id

    # Remove unconnected nodes
    # They are generally utility nodes for purposes other than defining roads
    net.remove_nodes_from(
        [i for i in net.nodes_iter() if len(net[i]) == 0]
        )

    # Iterate through the ways once again to remove nodes that serve only to
    # connect two points.
    if trim:
        for way in raw_osm.ways.itervalues():

            if not _test_if_road(way):
                continue

            for node_id in way.nodes:
                try:
                    neighb = net[node_id]
                except KeyError:
                    continue  # skip nodes already deleted

                if len(neighb) != 2:
                    continue
                else:
                    n1, n2 = neighb.keys()
                    if n2 not in net[n1]:
                        net.add_edge(
                            n1, n2,
                            length=neighb[n1]['length'] + neighb[n2]['length'],
                            travel_time=(
                                neighb[n1]['travel_time'] +
                                neighb[n2]['travel_time']
                                ),
                            highway=neighb[n1]['highway'],
                            name=neighb[n1]['name']
                            )
                    net.remove_node(node_id)

    return net


#
# IO functions
# ------------
#

def node2str(net, node):

    """Converts a node into a string

    The result will be written as the junction of the roads that the node is
    connected to.

    :param net: The network
    :param node: The node id

    """

    edge_names = set(
        attrs['name'] for _, attrs in net[node].iteritems()
        )

    if len(edge_names) == 1:
        prefix = 'end point of '
    else:
        prefix = 'junction of '

    return prefix + ', '.join(edge_names)


def edge2str(net, edge):

    """Converts an edge into a string

    All the basic information are put.

    :param net: The network
    :param edge: The node pair of an edge as in the ``edges`` method of the
        network

    """

    beg, end = edge
    data = net[beg][end]

    return ' %s road %s, length %s mile, travel time %s hour' % (
        data['highway'], data['name'], data['length'], data['travel_time']
        )


def draw_network(net, out_name):

    """Draws the network to a graphics file

    The actual drawing is performed by matplotlib interface of the networkX
    library.

    """

    pos = {
        key: data['coord']
        for key, data in net.nodes_iter(data=True)
        }

    nx.draw_networkx(net, pos=pos, with_labels=False, node_size=2)
    plt.axis('off')
    plt.savefig(out_name)

    return None


def print_network(net, outf=sys.stdout):

    """Prints information about the network on a file

    The file is the standard output by default.

    """

    prt = functools.partial(print, file=outf)
    title = 'Network Information'
    print_title(title, outf)

    prt(
        "Number of nodes: %d, number of edges: %d\n" % (
            net.number_of_nodes(), net.number_of_edges()
            )
        )

    for node_id, node_data in net.nodes_iter(data=True):
        prt(
            " Node %d, %s, location: (%f, %f)" % (
                node_id, node2str(net, node_id),
                node_data['coord'][0], node_data['coord'][1]
                )
            )

    prt("\n")

    for n1, n2 in net.edges_iter():
        prt(edge2str(net, (n1, n2)))

    prt("\n")

    return None

"""
Shortest path computation
=========================

This module contains functions converting the trips generated by the
:py:mod:`trips` module into concrete paths on the network. The trips are
generated by shortest-path algorithm with the travelling time as the
weight, and the results are going to be stored as :py:class:`ShortestPath`
instances, which has got the essential path information carried and some
convenience functions for getting information about the paths.

.. autoclass:: ShortestPath
    :members:
    :special-members:

"""

import networkx as nx

from .util import pairwise


class ShortestPath(object):

    """Shortest paths from trips

    Basically it just contains the list of nodes in the network that is visited
    and the travel time that is needed to traverse the edges.

    .. py:attribute:: nodes

        A list of node identity in the network, giving the shortest path for
        the trip

    .. py:attribute:: travel_times

        A list of travel times for traversing the edges connecting the nodes

    """

    # pylint: disable=too-few-public-methods

    def __init__(self, net, trip):

        """Initializes a shortest path by giving the trip

        :param net: The network on which to find the paths
        :param trip: A list of places that needs to be visited by a trip

        """

        self.nodes = []

        # find the shortest path
        for beg, end in pairwise(trip):

            beg_node = beg.node
            end_node = end.node

            self.nodes.extend(
                nx.shortest_path(
                    net, source=beg_node, target=end_node,
                    weight='travel_time'
                    )
                )

        # get the travel time
        self.travel_times = []
        for beg, end in pairwise(self.nodes):
            self.travel_times.append(
                net[beg][end]['travel_time']
                )

    def travel_time(self):

        """Returns the total travel time of the shortest path"""

        return sum(self.travel_times)

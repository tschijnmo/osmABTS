"""
Simulate average travel time
============================

This module contains functions to simulate the average travel time of the
travellers with or without some edge removed. Primarily it contains functions

.. autosummary::
    :toctree: generated

    simul_travel_time
    test_sensitivity_edges

"""

from __future__ import print_function

import sys

from .util import print_title
from .network import node2str


def simul_travel_time(model):

    """Simulates the average travel time of a model

    It is assumed that the model already has got everything except the actual
    paths already formed.

    """

    model.compute_paths()
    mean_time = model.compute_mean_time()

    return mean_time


def test_sensitivity_edges(model, mean_time):

    """Tests the sensitivity of the mean travel time for each edge

    Each edge is going to be temporarily removed to test the sensitity of the
    mean travel time for it.

    :param model: The model, with everying already setted up
    :param mean_time: The mean_time before any edge is removed

    """

    print_title('Edge sensitivity analysis', sys.stdout)

    # A shallow copy of the edges
    edges = model.network.edges()

    print("Now we remove streets between nodes, and find the new travel time")
    print(" Street name / node 1 / node 2 / new time / percentage ")
    for n1, n2 in edges:

        data = model.network[n1][n2]

        street_name = data['name']
        end1 = node2str(model.network, n1)
        end2 = node2str(model.network, n2)

        model.network.remove_edge(n1, n2)

        new_time = simul_travel_time(model)
        percentage = (new_time - mean_time) / mean_time
        print(
            ' / '.join([
                street_name, end1, end2,
                str(new_time), str(percentage)
                ])
            )

        model.network.add_edge(n1, n2, **data)

    return None


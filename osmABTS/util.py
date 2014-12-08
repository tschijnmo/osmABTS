"""
Some utility functions
======================

"""

import random
import bisect


def select_place(places):

    """Randomly selects a place from a list of places based on the weight

    :param places: A list of :py:class:`places.Place` instances. One of them is
        going to be selected based on the ``weight`` attribute
    :returns: The place selected

    """

    weights = []

    for place in places:
        weights.append(sum(weights) + place.weight)
        continue

    rand_n = random.uniform(0.0, weights[-1])
    return places[bisect.bisect(weights, rand_n) - 1]

"""
Some utility functions
======================

.. autosummary::
    :toctree: generated

    select_place
    pairwise

"""

import random
import bisect
import itertools


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


def pairwise(iterable):

    """s -> (s0,s1), (s1,s2), (s2, s3), ...

    From the official itertools recipes.

    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

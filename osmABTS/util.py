"""
Some utility functions
======================

.. autosummary::
    :toctree: generated

    select_place
    pairwise
    print_title

"""

from __future__ import print_function

import random
import bisect
import itertools


def select_place(places):

    """Randomly selects a place from a list of places based on the weight

    :param places: A list of :py:class:`places.Place` instances. One of them is
        going to be selected based on the ``weight`` attribute
    :returns: The place selected

    """

    weights = [i.weight for i in places]
    weights_acc = []

    for i in xrange(0, len(places)):
        weights_acc.append(sum(weights[0:(i + 1)]))
        continue

    rand_n = random.uniform(0.0, weights_acc[-1])
    return places[bisect.bisect(weights_acc, rand_n) - 1]


def pairwise(iterable):

    """s -> (s0,s1), (s1,s2), (s2, s3), ...

    From the official itertools recipes.

    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def print_title(title, outf):

    """Prints a title to a file

    The title will be marked up by an underline of equal signs as in the Setext
    style of headers.

    """

    print("\n\n%s" % title, file=outf)
    print("=" * len(title), file=outf)
    print("")

    return None

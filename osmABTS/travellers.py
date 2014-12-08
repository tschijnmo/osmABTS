"""
Individual traveller generation
===============================

A traveller is a person with a multiple of attributes, each attributes is a
place that is specific to the traveller. The attributes are randomly selected
based on the weights of the kinds of places of interest.

.. autoclass:: Traveller
    :members:
    :special-members:

"""

from __future__ import print_function

import sys

from .util import select_place, print_title
from .network import node2str


#
# The traveller class
# -------------------
#

class Traveller(object):

    """Travellers holding a set of places as attributes

    .. py:attribute:: attrs

        A dictionary, with attribute name of the key and the actual place as
        the value.

    """

    # pylint: disable=too-few-public-methods

    __slots__ = [
        'attrs',
        ]

    def __init__(self, places, attrs):

        """Initializes a traveller instance

        A traveller with the request attributes will be generated randomly.

        :param places: The places dictionary, with category name as key and
            actual places list as entry
        :param attrs: The attributes of the traveller, as a dictionary with the
            attribute names as keys, and the category name for the places to
            select from as values

        """

        self.attrs = {
            attr_name: select_place(places[cat_name])
            for attr_name, cat_name in attrs.iteritems()
            }


#
# Default Attributes
# ------------------
#

DEFAULT_ATTRS = {
    'home': 'home',
    'work': 'work',
    'church': 'church',
    }


#
# IO functions
# ------------
#

def print_travellers(net, travellers, outf=sys.stdout):

    """Prints the information about the travellers to a file

    :param travellers: A list of travellers

    """

    print_title('Travellers', outf)

    for i, trav in enumerate(travellers):
        print(
            "Traveller %d, home at %s, work at %s" % (
                i, node2str(net, trav.attrs['home'].node),
                trav.attrs['work'].name
                ),
            file=outf
            )
        continue

    return None

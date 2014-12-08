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

from .util import select_place


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

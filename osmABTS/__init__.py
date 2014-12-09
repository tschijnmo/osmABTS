"""
osmABTS package
===============

Activity-based traffic simulation based on OpenStreetMap

Most of the time, users only need to interact with the instances of the
:py:class:`model.Model` class, defined in the module,

.. autosummary::
    :toctree: generated
    :template: moduletempl.rstt

    model

Under the wrapper, most of the jobs are done by the core functions in the
modules,

.. autosummary::
    :toctree: generated
    :template: moduletempl.rstt

    readosm
    network
    places
    travellers
    trips
    paths
    simultime
    util

These modules contains functions and classes that is useful for doing non-
straightforward works with this package.


"""

from .model import Model
from .main import main

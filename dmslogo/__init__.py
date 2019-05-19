"""
============
dmslogo
============

Draw sequence logos for deep mutational scanning data.

Importing this package imports the following main functions
into the package namespace:

 - :py:mod:`dmslogo.logo.draw_logo`
 - :py:mod:`dmslogo.line.draw_line`
 - :py:mod:`dmslogo.facet.facet_plot`
"""

__author__ = 'Jesse Bloom'
__email__ = 'jbloom@fredhutch.org'
__version__ = '0.2.3'
__url__ = 'https://github.com/jbloomlab/dmslogo'

from dmslogo.facet import facet_plot  # noqa: F401
from dmslogo.line import draw_line  # noqa: F401
from dmslogo.logo import draw_logo  # noqa: F401

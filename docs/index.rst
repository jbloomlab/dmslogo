Documentation for ``dmslogo``
======================================

`dmslogo` is a Python package written by the `Bloom lab <https://research.fhcrc.org/bloom/en.html>`_ for making sequence logo plots of deep mutational scanning data.

It allows you to make figures like this with just a single plotting command:

.. figure:: _static/facet_plot_example.png
   :align: left
   :alt: facet plot

   Plot showing antibody selection across the entirety of HIV Env, and zooming in on mutations at strongly selected sites.
   Created using the :py:mod:`dmslogo.facet.facet_plot` command as shown in the :ref:`examples`.

It also allows you to heavily customize your logo plots, such as by coloring specific letters at specific sites or `using Comic Sans font <http://comicsanscriminal.com/>`_:

.. figure:: _static/dmslogo_comic_sans.png
   :align: left
   :alt: comic sans plot
   :width: 35%

   Logo plot with custom letter coloring and Comic Sans font.
   Created using the :py:mod:`dmslogo.logo.draw_logo` command as shown in the :ref:`examples`.

Contents
----------
.. toctree::
   :maxdepth: 1

   installation
   examples
   dmslogo
   package_index
   acknowledgments

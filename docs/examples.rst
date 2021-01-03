.. _examples:

========
Examples
========

The ``dmslogo`` package is designed to aid in the visualization of deep mutational scanning via line and logo plots of site- and mutation-wise measurements of mutationsl effects.
It provides several Python functions that you can use in scripts or Jupyter notebooks.
Major functionality includes:

 - The :py:mod:`dmslogo.logo.draw_logo` function for creating highly customizable logo plots.

 - The :py:mod:`dmslogo.line.draw_line` function for creating line plots.

 - The :py:mod:`dmslogo.facet.facet_plot` function for faceting together combinations of line and logo plots.

Below are examples that illustrate usage of this functionality and other aspects of the ``dmslogo`` package.

.. toctree::
   :maxdepth: 1

   basic_example
   overlays
   negative_values
   set_ylims

The above examples can be run as interactive Jupyter notebooks on `mybinder <https://mybinder.readthedocs.io>`_ by going to the `following link <https://mybinder.org/v2/gh/jbloomlab/dmslogo/master?filepath=notebooks>`_ (it may take a minute to load) and then opening the notebook you want to run.

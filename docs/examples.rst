.. _examples:

Examples
========

.. contents::
   :local:

.. code-links:: full
    :timeout: 200

Import packages / modules
-------------------------

Import `dmslogo` along with the other Python packages used in
these examples:

.. nbplot::

    >>> import string
    >>> import random
    >>> import tempfile
    >>> import urllib.request
    >>>
    >>> import numpy
    >>> import pandas as pd
    >>> import matplotlib.pyplot as plt
    >>>
    >>> import dmslogo
    >>> from dmslogo.colorschemes import CBPALETTE

Simple example on toy data
--------------------------

Draw a basic logo
~~~~~~~~~~~~~~~~~

Simple plotting can be done using the :py:mod:`dmslogo.logo.draw_logo`
function.

This function takes in as input a pandas DataFrame that has columns
with: - site in sequential integer numbering - letter (i.e., amino acid
or nucleotide) - height of letter (can be any positive number)

Here make a simple data frame that fits these specs:

.. nbplot::

    >>> data = pd.DataFrame.from_records(
    ...         data=   [(    1,      'A',        1),
    ...                  (    1,      'C',      0.7),
    ...                  (    2,      'C',      0.1),
    ...                  (    2,      'D',      1.2),
    ...                  (    5,      'A',      0.4),
    ...                  (    5,      'K',      0.4)],
    ...         columns=['site', 'letter', 'height'])
    ...
    >>> print('Here are the contents of `data`:')
    >>> data

    Here are the contents of `data`:


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>site</th>
          <th>letter</th>
          <th>height</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>A</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>C</td>
          <td>0.7</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>C</td>
          <td>0.1</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2</td>
          <td>D</td>
          <td>1.2</td>
        </tr>
        <tr>
          <th>4</th>
          <td>5</td>
          <td>A</td>
          <td>0.4</td>
        </tr>
        <tr>
          <th>5</th>
          <td>5</td>
          <td>K</td>
          <td>0.4</td>
        </tr>
      </tbody>
    </table>
    </div>


Use :py:mod:`dmslogo.logo.draw_logo` to draw the logo plot, passing
the names of the columns with each piece of required data:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data=data,
    ...                             x_col='site',
    ...                             letter_col='letter',
    ...                             letter_height_col='height')




Add a title:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data=data,
    ...                             x_col='site',
    ...                             letter_col='letter',
    ...                             letter_height_col='height',
    ...                             title='basic example')




Note that the call to :py:mod:`dmslogo.logo.draw_logo` returns
matplotlib Figure and Axis instances, which we have called ``fig`` and
``ax``. We can save the figure to a file using the
`savefig <https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html>`__
command of ``fig``. Below we show an example of how to do this saving to
a temporary file:

.. nbplot::

    >>> with tempfile.NamedTemporaryFile(mode='wb', suffix='.png') as f:
    ...     fig.savefig(f, dpi=450, bbox_inches='tight')

Drawing without breaks
~~~~~~~~~~~~~~~~~~~~~~

Note how the above plot has a “break” (gap and dashed line) to indicate
a break in the sequential numbering in ``x_col`` between 2 and 5. This
is useful as it indicates when we are breaking the sequence when drawing
just snippets of a protein. If you do **not** want to indicate breaks in
this way, turn off the ``addbreaks`` option. Now the logo just goes
directly from 2 to 5 without indicating a break:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data=data,
    ...                             x_col='site',
    ...                             letter_col='letter',
    ...                             letter_height_col='height',
    ...                             addbreaks=False)




Setting letter colors
~~~~~~~~~~~~~~~~~~~~~

The above plot colored letters using a default amino-acid coloring
scheme. You can set a different coloring scheme using ``colorscheme``
and ``missing_color``, or you can set letter colors at a site-specific
level by adding a column to ``data`` that specifies the colors. Here we
color letters at site-specific level:

.. nbplot::

    >>> data['color'] = ['red', 'gray', 'gray', 'gray', 'red', 'gray']
    >>>
    >>> print('Here is `data` with the added color column:')
    >>> data

    Here is `data` with the added color column:


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>site</th>
          <th>letter</th>
          <th>height</th>
          <th>color</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>A</td>
          <td>1.0</td>
          <td>red</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>C</td>
          <td>0.7</td>
          <td>gray</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>C</td>
          <td>0.1</td>
          <td>gray</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2</td>
          <td>D</td>
          <td>1.2</td>
          <td>gray</td>
        </tr>
        <tr>
          <th>4</th>
          <td>5</td>
          <td>A</td>
          <td>0.4</td>
          <td>red</td>
        </tr>
        <tr>
          <th>5</th>
          <td>5</td>
          <td>K</td>
          <td>0.4</td>
          <td>gray</td>
        </tr>
      </tbody>
    </table>
    </div>


Now plot using ``color_col`` to set the colors:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data=data,
    ...                             x_col='site',
    ...                             letter_col='letter',
    ...                             letter_height_col='height',
    ...                             color_col='color')




Labeling x-axis ticks
~~~~~~~~~~~~~~~~~~~~~

Sometimes we want to label sites with something other than the
sequential integer numbers. We can do this by adding a column for the
xtick labels to ``data``:

.. nbplot::

    >>> data['site_label'] = ['D1', 'D1', 'A2', 'A2', 'F5', 'F5']
    >>>
    >>> print('Here is `data` with the added site label column:')
    >>> data

    Here is `data` with the added site label column:


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>site</th>
          <th>letter</th>
          <th>height</th>
          <th>color</th>
          <th>site_label</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>A</td>
          <td>1.0</td>
          <td>red</td>
          <td>D1</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>C</td>
          <td>0.7</td>
          <td>gray</td>
          <td>D1</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2</td>
          <td>C</td>
          <td>0.1</td>
          <td>gray</td>
          <td>A2</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2</td>
          <td>D</td>
          <td>1.2</td>
          <td>gray</td>
          <td>A2</td>
        </tr>
        <tr>
          <th>4</th>
          <td>5</td>
          <td>A</td>
          <td>0.4</td>
          <td>red</td>
          <td>F5</td>
        </tr>
        <tr>
          <th>5</th>
          <td>5</td>
          <td>K</td>
          <td>0.4</td>
          <td>gray</td>
          <td>F5</td>
        </tr>
      </tbody>
    </table>
    </div>


Now use ``xtick_col`` to set the xticks:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data=data,
    ...                             x_col='site',
    ...                             letter_col='letter',
    ...                             letter_height_col='height',
    ...                             color_col='color',
    ...                             xtick_col='site_label')




Adjusting size, axis labels, axes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can do additional formatting by scaling the width (``widthscale``),
the height (``heightscale``), the axis font (``axisfontscale``), the
x-axis (``xlabel``) and y-axis (``ylabel``) labels, and removing the
axes altogether (``hide_axis``).

First, we make a plot where we adjust the size, change the y-axis label,
and get rid of the x-axis label:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data=data,
    ...                             x_col='site',
    ...                             letter_col='letter',
    ...                             letter_height_col='height',
    ...                             color_col='color',
    ...                             xtick_col='site_label',
    ...                             xlabel='',
    ...                             ylabel='immune selection',
    ...                             heightscale=2,
    ...                             axisfontscale=1.5
    ...                             )




Now we make a plot where we hide the axes and their labels altogether:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data=data,
    ...                             x_col='site',
    ...                             letter_col='letter',
    ...                             letter_height_col='height',
    ...                             color_col='color',
    ...                             xtick_col='site_label',
    ...                             hide_axis=True
    ...                             )




Multiple logos in one figure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So far we have made individual plots on newly generate figures created
by :py:mod:`dmslogo.draw_logo`.

But we can also create a multi-axis figure, and then draw several logos
onto that. The easiest way to do this is with the
:py:mod:`dmslogo.facet.facet_plot` command described below. But we can
also do it using matplotlib subplots as here:

.. nbplot::

    >>> # make figure with two subplots: two rows, one column
    >>> fig, axes = plt.subplots(2, 1)
    >>> fig.subplots_adjust(hspace=0.3) # add more vertical space for axis titles
    >>> fig.set_size_inches(4, 5)
    >>>
    >>> # draw top plot, no x-axis ticks or label, default coloring
    >>> _ = dmslogo.draw_logo(data.assign(no_ticks=''),
    ...                       x_col='site',
    ...                       letter_col='letter',
    ...                       letter_height_col='height',
    ...                       ax=axes[0],
    ...                       xlabel='',
    ...                       ylabel='',
    ...                       xtick_col='no_ticks',
    ...                       title='colored by amino acid')
    ...
    >>> # draw bottom plot, color as specified in `data`
    >>> _ = dmslogo.draw_logo(data,
    ...                       x_col='site',
    ...                       letter_col='letter',
    ...                       letter_height_col='height',
    ...                       color_col='color',
    ...                       ax=axes[1],
    ...                       ylabel='',
    ...                       title='user-specified colors')




Real HIV data from Dingens et al
--------------------------------

In `An Antigenic Atlas of HIV-1 Escape from Broadly Neutralizing
Antibodies Distinguishes Functional and Structural
Epitopes <https://doi.org/10.1016/j.immuni.2018.12.017>`__ (Dingens et
al, 2019), there are plots of immune selection on HIV envelope (Env)
from anti-HIV antibodies at just a subset of “strongly selected” sites
for each antibody.

Here we use ``dmslogo`` to re-create one of those plots (the one in
Figure 3D,E) showing antibodies *PG9* and *PGT145*.

Download data to plot
~~~~~~~~~~~~~~~~~~~~~

Download the data from the paper’s `GitHub
repo <https://github.com/jbloomlab/EnvsAntigenicAtlas/>`__ giving the
immune selection (as `fraction surviving above
average <https://jbloomlab.github.io/dms_tools2/fracsurvive.html>`__)
for these two antibodies, and read the data into a DataFrame:

.. nbplot::

    >>> antibodies = ['PG9', 'PGT145']
    >>>
    >>> data_hiv = []
    >>> for antibody in antibodies:
    ...     datafile = ('https://raw.githubusercontent.com/jbloomlab/EnvsAntigenicAtlas/master/results/'
    ...                 f"fracsurviveaboveavg/concavg_wtDNA_ctrl/summary_{antibody}-medianmutfracsurvive.csv")
    ...     with urllib.request.urlopen(datafile) as f:
    ...         data_hiv.append(pd.read_csv(f).assign(antibody=antibody))
    ...
    >>> data_hiv = pd.concat(data_hiv)

Here are the first few lines of the data frame. For each mutation it
gives the immune selection (*mutfracsurvive*):

.. nbplot::

    >>> data_hiv.head(n=5)



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>site</th>
          <th>wildtype</th>
          <th>mutation</th>
          <th>mutfracsurvive</th>
          <th>antibody</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>160</td>
          <td>N</td>
          <td>I</td>
          <td>0.256342</td>
          <td>PG9</td>
        </tr>
        <tr>
          <th>1</th>
          <td>160</td>
          <td>N</td>
          <td>L</td>
          <td>0.207440</td>
          <td>PG9</td>
        </tr>
        <tr>
          <th>2</th>
          <td>160</td>
          <td>N</td>
          <td>R</td>
          <td>0.184067</td>
          <td>PG9</td>
        </tr>
        <tr>
          <th>3</th>
          <td>171</td>
          <td>K</td>
          <td>E</td>
          <td>0.176118</td>
          <td>PG9</td>
        </tr>
        <tr>
          <th>4</th>
          <td>428</td>
          <td>Q</td>
          <td>Y</td>
          <td>0.150981</td>
          <td>PG9</td>
        </tr>
      </tbody>
    </table>
    </div>


The sites in this data frame are in the `HXB2 numbering
scheme <https://www.hiv.lanl.gov/content/sequence/HIV/REVIEWS/HXB2.html>`__,
which is **not** the same as sequential integer numbering of the actual
BG505 Env for which the immune selection was measured. So for our
plotting, we also need to create a column (which we will call ``isite``)
that numbers the sites a sequential numbering. A file that converts
between HXB2 and and BG505 numbering is part of the paper’s `GitHub
repo <https://github.com/jbloomlab/EnvsAntigenicAtlas/>`__. We download
the data in that file and add it to our data frame:

.. nbplot::

    >>> numberfile = ('https://raw.githubusercontent.com/jbloomlab/EnvsAntigenicAtlas/'
    ...               'master/results/HXB2_numbering/BG505_to_HXB2.csv')
    >>> with urllib.request.urlopen(numberfile) as f:
    ...     data_hiv = (pd.read_csv(f)
    ...                 .rename(columns={'original':'isite', 'new':'site'})
    ...                 [['site', 'isite']]
    ...                 .merge(data_hiv, on='site', validate='one_to_many')
    ...                 )

Now see how this data frame also has the ``isite`` column which has
sequential integer numbering of the sequence:

.. nbplot::

    >>> data_hiv.head(n=5)



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>site</th>
          <th>isite</th>
          <th>wildtype</th>
          <th>mutation</th>
          <th>mutfracsurvive</th>
          <th>antibody</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>Y</td>
          <td>0.030824</td>
          <td>PG9</td>
        </tr>
        <tr>
          <th>1</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>K</td>
          <td>0.006860</td>
          <td>PG9</td>
        </tr>
        <tr>
          <th>2</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>D</td>
          <td>0.006774</td>
          <td>PG9</td>
        </tr>
        <tr>
          <th>3</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>S</td>
          <td>0.004407</td>
          <td>PG9</td>
        </tr>
        <tr>
          <th>4</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>R</td>
          <td>0.003501</td>
          <td>PG9</td>
        </tr>
      </tbody>
    </table>
    </div>


We add a column (``site_label``) that gives the site labeled with the
wildtype identity that we can use for axis ticks. We also indicate which
sites to show (column ``show_site``) in our logoplot snippet (these are
just the same ones in Figure 3 of the `Dingens et al
(2019) <https://doi.org/10.1016/j.immuni.2018.12.017>`__ paper):

.. nbplot::

    >>> # same sites in Figure 3D,E of Dingens et al (2019)
    >>> sites_to_show = map(str, list(range(119, 125)) + 
    ...                          [127] +
    ...                          list(range(156, 174)) +
    ...                          list(range(199, 205)) +
    ...                          list(range(312, 316))
    ...                          )
    ...
    >>> data_hiv = (
    ...     data_hiv
    ...     .assign(site_label=lambda x: x['wildtype'] + x['site'],
    ...             show_site=lambda x: x['site'].isin(sites_to_show),
    ...             )
    ...     )

See how the data frame now has the ``site_label`` and ``show_site``
columns:

.. nbplot::

    >>> data_hiv.head(n=5)



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>site</th>
          <th>isite</th>
          <th>wildtype</th>
          <th>mutation</th>
          <th>mutfracsurvive</th>
          <th>antibody</th>
          <th>site_label</th>
          <th>show_site</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>Y</td>
          <td>0.030824</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
        </tr>
        <tr>
          <th>1</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>K</td>
          <td>0.006860</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
        </tr>
        <tr>
          <th>2</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>D</td>
          <td>0.006774</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
        </tr>
        <tr>
          <th>3</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>S</td>
          <td>0.004407</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
        </tr>
        <tr>
          <th>4</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>R</td>
          <td>0.003501</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
        </tr>
      </tbody>
    </table>
    </div>


Draw a logo plot
~~~~~~~~~~~~~~~~

Now we make logo plots of the sites that we have selected to show, here
just for the *PG9* antibody:

We want two plots stacked on each other. So as in the toy example above
we first make a figure with two axes. We then plot onto each axis,
showing xticks and and xlabel only for the last (bottom) plot. Note how
for both logo plots we query ``data_hiv`` for only the sites of interest
(``show_site`` is ``True``), and for each plot we query ``data_hiv`` for
just the antibody of interest:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data_hiv.query('antibody == "PG9"').query('show_site'),
    ...                             x_col='isite',
    ...                             letter_col='mutation',
    ...                             letter_height_col='mutfracsurvive',
    ...                             xtick_col='site_label',
    ...                             title='PG9')




Draw site-level line plots
~~~~~~~~~~~~~~~~~~~~~~~~~~

The logo plot above shows selection at a subset of sites. But we might
also want to summarize the selection across all sites (as is done in
Figure 2 of `Dingens et al
(2019) <https://doi.org/10.1016/j.immuni.2018.12.017>`__).

An easy way to do this is to create a summary statistic at each site.
Here we compute the average
`fracsurvive <https://jbloomlab.github.io/dms_tools2/dms_tools2.fracsurvive.html>`__
at each site across all mutations, and add that to our data frame:

.. nbplot::

    >>> data_hiv = (
    ...     data_hiv
    ...     .query('mutation != wildtype') # only care about mutations; get rid of wildtype values
    ...     .assign(avgfracsurvive=lambda x: x.groupby(['antibody', 'site'])
    ...                                         ['mutfracsurvive']
    ...                                         .transform('mean')
    ...             )
    ...     )

Now the data frame has a column (``avgfracsurvive``) giving the average
fraction surviving at each site:

.. nbplot::

    >>> data_hiv.head(n=5)



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>site</th>
          <th>isite</th>
          <th>wildtype</th>
          <th>mutation</th>
          <th>mutfracsurvive</th>
          <th>antibody</th>
          <th>site_label</th>
          <th>show_site</th>
          <th>avgfracsurvive</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>Y</td>
          <td>0.030824</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
          <td>0.00329</td>
        </tr>
        <tr>
          <th>1</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>K</td>
          <td>0.006860</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
          <td>0.00329</td>
        </tr>
        <tr>
          <th>2</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>D</td>
          <td>0.006774</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
          <td>0.00329</td>
        </tr>
        <tr>
          <th>3</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>S</td>
          <td>0.004407</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
          <td>0.00329</td>
        </tr>
        <tr>
          <th>4</th>
          <td>31</td>
          <td>30</td>
          <td>A</td>
          <td>R</td>
          <td>0.003501</td>
          <td>PG9</td>
          <td>A31</td>
          <td>False</td>
          <td>0.00329</td>
        </tr>
      </tbody>
    </table>
    </div>


Now we use the :py:mod:`dmslogo.draw_line` function to draw the line plot for
antibody *PG9*. Note how we provide our new ``avgfracsurvive`` column as
``height_col``. We also provide our previously defined ``show_site``
column (which indicates which sites were shown in the logo plot) as the
``show_col``, so that the line plot has the sites shown in the above
logo plot underlined in orange:

.. nbplot::

    >>> fig, ax = dmslogo.draw_line(data_hiv.query('antibody == "PG9"'), 
    ...                             x_col='isite',
    ...                             height_col='avgfracsurvive',
    ...                             xtick_col='site',
    ...                             show_col='show_site',
    ...                             title='PG9',
    ...                             widthscale=2)




Combining site-level line and mutation-level logo plots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Of course, a line plot isn’t that hard to make, but the advantage of
doing this using the approach above is that we can combine
:py:mod:`dmslogo.draw_line` and :py:mod:`dmslogo.draw_logo` to create a single
figure that shows the site-selection in a line plot and the selected
sites as logo plots.

The easiest way to do this using the
:py:mod:`dmslogo.facet.facet_plot` command described below. But first
here we do it using matplotlib subplots. Note how the resulting
Bcombines the line and logo plots, with the line plot using the orange
underline to indicate which sites are zoomed in the logo plot:

.. nbplot::

    >>> fig, axes = plt.subplots(1, 2,
    ...                          gridspec_kw={'width_ratios':[1, 1.5]})
    >>> fig.subplots_adjust(wspace=0.12)
    >>> fig.set_size_inches(24, 3)
    >>>
    >>> _ = dmslogo.draw_line(data_hiv.query('antibody == "PG9"'),
    ...                       x_col='isite',
    ...                       height_col='avgfracsurvive',
    ...                       xtick_col='site',
    ...                       show_col='show_site',
    ...                       ax=axes[0])
    ...
    >>> _ = dmslogo.draw_logo(data_hiv.query('antibody == "PG9"').query('show_site'),
    ...                       x_col='isite',
    ...                       letter_col='mutation',
    ...                       letter_height_col='mutfracsurvive',
    ...                       ax=axes[1],
    ...                       xtick_col='site_label')




Faceting line and logo plots together
-------------------------------------

The easiest way to facet line and logo plots together is using
:py:mod:`dmslogo.facet.facet_plot`.

The cell below shows how this is done. You pass the data to this
function, as well any columns and rows we would like to facet, the
``x_col`` and ``show_col`` arguments shared between the line and logo
plots, and additional keyword arguments for
:py:mod:`dmslogo.logo.draw_logo` and
:py:mod:`dmslogo.line.draw_line`:

.. nbplot::

    >>> fig, axes = dmslogo.facet_plot(
    ...                     data_hiv,
    ...                     gridrow_col='antibody',
    ...                     x_col='isite',
    ...                     show_col='show_site',
    ...                     draw_line_kwargs=dict(height_col='avgfracsurvive',
    ...                                           xtick_col='site',
    ...                                           widthscale=0.8),
    ...                     draw_logo_kwargs=dict(letter_col='mutation',
    ...                                           letter_height_col='mutfracsurvive',
    ...                                           xtick_col='site_label',
    ...                                           xlabel='site',
    ...                                           widthscale=0.6),
    ...                     line_titlesuffix='site-level selection',
    ...                     logo_titlesuffix='mutation-level selection'
    ...                     )




Write *DMSLOGO* in Comic Sans font
----------------------------------

Generate data to plot by creating the pandas DataFrame ``word_data``. In
this data frame, we choose large heights and bright colors for the
letters in our word (*DMSLOGO*), and smaller letters and gray for other
letters.

.. nbplot::

    >>> word = 'DMSLOGO'
    >>> lettercolors = [CBPALETTE[1]] * len('dms') + [CBPALETTE[2]] * len('logo')
    >>>
    >>> # make data frame with data to plot
    >>> random.seed(0)
    >>> word_data = {'x':[], 'letter':[], 'height':[], 'color':[]}
    >>> for x, (letter, color) in enumerate(zip(word, lettercolors)):
    ...     word_data['x'].append(x)
    ...     word_data['letter'].append(letter)
    ...     word_data['color'].append(color)
    ...     word_data['height'].append(random.uniform(1, 1.5))
    ...     for otherletter in random.sample(set('ACTG') - {letter}, 3):
    ...         word_data['x'].append(x)
    ...         word_data['letter'].append(otherletter)
    ...         word_data['color'].append(CBPALETTE[0])
    ...         word_data['height'].append(random.uniform(0.1, 0.5))
    >>> word_data = pd.DataFrame(word_data)
    >>>
    >>> print('Here are the first few rows of `word_data`:')
    >>> word_data.head(n=6)

    Here are the first few rows of `word_data`:


.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>x</th>
          <th>letter</th>
          <th>height</th>
          <th>color</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>0</td>
          <td>D</td>
          <td>1.422211</td>
          <td>#E69F00</td>
        </tr>
        <tr>
          <th>1</th>
          <td>0</td>
          <td>A</td>
          <td>0.486186</td>
          <td>#999999</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0</td>
          <td>T</td>
          <td>0.294371</td>
          <td>#999999</td>
        </tr>
        <tr>
          <th>3</th>
          <td>0</td>
          <td>G</td>
          <td>0.467294</td>
          <td>#999999</td>
        </tr>
        <tr>
          <th>4</th>
          <td>1</td>
          <td>M</td>
          <td>1.414926</td>
          <td>#E69F00</td>
        </tr>
        <tr>
          <th>5</th>
          <td>1</td>
          <td>A</td>
          <td>0.301875</td>
          <td>#999999</td>
        </tr>
      </tbody>
    </table>
    </div>


Now draw the logo. We use the ``fontfamily`` argument to set a Comic
Sans font This also requires us to increase ``fontaspect`` since this
font is wider, and increase ``letterpad`` as the font height sometimes
sticks out beyond its baseline:

.. nbplot::

    >>> fig, ax = dmslogo.draw_logo(data=word_data,
    ...                             letter_height_col='height',
    ...                             x_col='x',
    ...                             letter_col='letter',
    ...                             color_col='color',
    ...                             fontfamily='Comic Sans MS',
    ...                             hide_axis=True,
    ...                             fontaspect=0.85,
    ...                             letterpad=0.05
    ...                             )





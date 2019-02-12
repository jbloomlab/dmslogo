"""The core logo-drawing functions of `dmslogo`.

Some of this code is borrowed from
`pyseqlogo <https://github.com/saketkc/pyseqlogo>`_.
"""


import numpy
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.patheffects import RendererBase
from matplotlib import transforms
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D

from dmslogo.seaborn_utils import despine
from dmslogo.colorschemes import *


class Scale(RendererBase):
    """Scale letters using affine transformation.
    
    From here: https://www.python-forum.de/viewtopic.php?t=30856
    """

    def __init__(self, sx, sy=None):
        self._sx = sx
        self._sy = sy

    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        affine = affine.identity().scale(self._sx, self._sy) + affine
        renderer.draw_path(gc, tpath, affine, rgbFace)


def _setup_font(fontfamily, fontsize):
    """Setup font properties"""

    font = FontProperties()
    font.set_size(fontsize)
    font.set_weight('bold')
    font.set_family(fontfamily)
    return font


def _draw_text_data_coord(height_matrix, ax, fontfamily, fontaspect):
    """Draws logo letters.

    Args:
        `height_matrix` (list of lists)
            Gives letter heights. In the main list, there is a list
            for each site, with the entries being 3-tuples giving
            the letter, its height, and its color.
        `ax` (matplotlib Axes)
            Axis on which we draw logo letters.
        `fontfamily` (str)
            Name of font to use.
        `fontaspect` (float)
            Value to use for font aspect ratio (height to width).
    """
    fig = ax.get_figure()
    bbox = ax.get_window_extent().transformed(
            fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi

    max_stack_height = max([sum([tup[1] for tup in row]) for
                           row in height_matrix])

    fontsize = (height / max_stack_height) * 72.0 / fig.dpi
    font = _setup_font(fontsize=fontsize, fontfamily=fontfamily)
    trans_offset = transforms.offset_copy(
            ax.transData, fig=fig, units='dots')

    fontwidthscale = width * max_stack_height / (height * fontaspect *
                                                 len(height_matrix))

    for xindex, xcol in enumerate(height_matrix):

        for letter, letterheight, lettercolor in xcol:
            txt = ax.text(
                xindex,
                0,
                letter,
                transform=trans_offset,
                fontsize=fontsize,
                color=lettercolor,
                ha='left',
                va='baseline',
                family='monospace',
                fontproperties=font)
            txt.set_path_effects([Scale(fontwidthscale, letterheight)])
            fig.canvas.draw()
            window_ext = txt.get_window_extent(
                txt._renderer)  
            yshift = window_ext.height * letterheight  
            trans_offset = transforms.offset_copy(
                txt.get_transform(), fig=fig, y=yshift, units='dots')

        trans_offset = transforms.offset_copy(
            ax.transData, fig=fig, units='dots')


def draw_logo(data,
              letter_height_col,
              *,
              letter_col='mutation',
              x_col='site',
              xtick_col=None,
              color_col=None,
              xlabel=None,
              ylabel=None,
              colorscheme=AA_FUNCTIONAL_GROUP,
              missing_color='gray',
              addbreaks=True,
              widthscale=1,
              heightscale=1,
              show_axis=True,
              fontfamily='DejaVu Sans Mono',
              fontaspect=0.55,
              ax=None):
    """Draw sequence logo from specified letter heights.

    Args:
        `data` (pandas DataFrame)
            Holds data to plot.
        `letter_height_col` (str)
            Column in `data` with letter heights.
        `letter_col` (str)
            Column in `data` with letter identities.
        `x_col` (str)
            Column in `data` with integer site numbers.
        `xtick_col` (`None` or str)
            Column in `data` used to label sites if not using `x_col`.
        `color_col` (`None` or str)
            Column in data with colors for each letter; set to `None`
            to define colors via `colorscheme` and `missing_color`.
        `xlabel` (`None` or str)
            Label for x-axis if not using `xtick_col` or `x_col`.
        `ylabel` (`None` or str)
            Label for y-axis if not using `letter_height_col`.
        `colorscheme` (dict)
            Color for each letter. Ignored if `color_col` is not `None`.
        `missing_color` (`None` or str)
            Color for letters not assigned in `colorscheme`,
            or `None` to raise an error for unassigned letters.
        `addbreaks` (bool)
            Anywhere there is a gap in sequential numbering of
            `x_col`, add break consisting of space and dashed line.
        `widthscale` (float)
            Scale width by this much.
        `heightscale` (float)
            Scale height by this much.
        `show_axis` (bool)
            Do we show the axes with ticks and labels?
        `fontfamily` (str)
            Font to use.
        `fontaspect` (float)
            Aspect ratio of font (height to width). If letters are
            too crowded, increase this.
        `ax` (`None` or matplotlib axes.Axes object)
            Use to plot on an existing axis.

    Returns:
        The 2-tuple `(fig, ax)` giving the figure and axis.
    """
    # set default values of arguments that can be None
    if xtick_col is None:
        xtick_col = x_col
    if xlabel is None:
        xlabel = xtick_col
    if ylabel is None:
        ylabel = letter_height_col

    # checks on input data
    for col in [letter_height_col, letter_col, x_col, xtick_col]:
        if col not in data.columns:
            raise ValueError(f"`data` lacks column {col}")
    if (color_col is not None) and (color_col not in data.columns):
        raise ValueError(f"`data` lacks column {color_col}")
    if any(data[letter_height_col] < 0):
        raise ValueError('`letter_height_col` has negative heights')
    if data[x_col].dtype != int:
        raise ValueError('`x_col` does not have integer values')
    if not df_cols_one_to_one(data, x_col, xtick_col):
        raise ValueError('not 1:1 mapping of `x_col` to `xtick_col`')

    # construct height_matrix: list of lists of (letter, hegith, color)
    height_matrix = []
    xticks = []
    lastx = None
    for x, xdata in (data
                     .sort_values([x_col, letter_height_col])
                     .groupby(x_col)
                     ):

        if addbreaks and (lastx is not None) and (x != lastx + 1):
            height_matrix.append([])
            xticks.append('')
        lastx = x

        if len(xdata[letter_col]) != len(xdata[letter_col].unique()):
            raise ValueError(f"duplicate letters for `x_col` {x}")

        row = []
        for tup in xdata.itertuples(index=False):
            letter = getattr(tup, letter_col)
            if not (isinstance(letter, str) and len(letter) == 1):
                raise ValueError(f"invalid letter of {letter}")
            letter_height = getattr(tup, letter_height_col)
            if color_col is not None:
                color = getattr(tup, color_col)
            else:
                try:
                    color = colorscheme[letter]
                except KeyError:
                    if missing_color:
                        color = missing_color
                    else:
                        raise ValueError(f"no color for {letter}")
            row.append((letter, letter_height, color))
        height_matrix.append(row)

        assert len(xdata[xtick_col].unique()) == 1
        xticks.append(str(xdata[xtick_col].values[0]))

    nstacks = len(height_matrix)
    assert len(xticks) == nstacks

    # setup axis for plotting
    if ax:
        raise ValueError('not yet implemented for passing `ax`')
    else:
        fig, ax = plt.subplots()
        fig.set_size_inches((widthscale * 0.5 * (nstacks + int(show_axis)),
                             heightscale))

    ax.set_xlim(0, nstacks)
    ax.set_xticks(numpy.arange(nstacks) + 0.5)
    ax.set_xticklabels(xticks, rotation=90)
    despine(ax=ax,
            trim=False,
            top=True,
            right=True)

    # draw the letters
    _draw_text_data_coord(height_matrix, ax, fontfamily, fontaspect)

    if not show_axis:
        ax.axis('off')

    return fig, ax


def df_cols_one_to_one(df, col1, col2):
    """Is mapping between two data frame columns one-to-one?

    Args:
        `df` (pandas DataFrame)
            Data frame.
        `col1` (str)
            First column in data frame.
        `col2` (str)
            Second column in data frame (can be same as `col1`).

    Returns:
        If each entry in `col1` uniquely maps to an entry in `col2`,
        returns `True`. Otherwise returns `False`.

    Returns `True` if one-to-one mapping:

    >>> one_to_one = pd.DataFrame({'col1':[1, 2, 2], 'col2':[4, 5, 5]})
    >>> df_cols_one_to_one(one_to_one, 'col1', 'col2')
    True

    Returns `False` if one-to-many or many-to-one mapping:

    >>> one_to_many = pd.DataFrame({'col1':[1, 2, 3], 'col2':[4, 5, 5]})
    >>> df_cols_one_to_one(one_to_many, 'col1', 'col2')
    False
    >>> df_cols_one_to_one(one_to_many, 'col2', 'col1')
    False

    Returns `True` if `col1` and `col2` are the same:

    >>> df_cols_one_to_one(one_to_many, 'col1', 'col1')
    True
    """
    for c in [col1, col2]:
        if c not in df.columns:
            raise ValueError(f"`df` lacks column {c}")

    if col1 == col2:
        return True

    if any(len(g[col2].unique()) != 1 for _, g in df.groupby(col1)):
        return False
    elif any(len(g[col1].unique()) != 1 for _, g in df.groupby(col2)):
        return False
    else:
        return True


if __name__ == '__main__':
    import doctest
    doctest.testmod()

"""The core logo-drawing functions of `dmslogo`.

Some of this code is borrowed and modified from
`pyseqlogo <https://github.com/saketkc/pyseqlogo>`_.
"""


import numpy
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patheffects
import matplotlib.font_manager
import matplotlib.ticker

import dmslogo.utils
import dmslogo.colorschemes


class Scale(matplotlib.patheffects.RendererBase):
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
    """Get `FontProperties` for `fontfamily` and `fontsize`."""

    font = matplotlib.font_manager.FontProperties()
    font.set_size(fontsize)
    font.set_weight('bold')
    font.set_family(fontfamily)
    return font


def _frac_above_baseline(font):
    """Returns fraction of font height that is above baseline.

    Args:
        `font` (FontProperties)
            Font for which we are computing fraction.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    txt_baseline = ax.text(0, 0, 'A', fontproperties=font,
                           va='baseline', bbox=dict(pad=0))
    txt_bottom = ax.text(0, 0, 'A', fontproperties=font,
                         va='bottom', bbox=dict(pad=0))

    fig.canvas.draw()
    bbox_baseline = txt_baseline.get_window_extent()
    bbox_bottom = txt_bottom.get_window_extent()

    height_baseline = bbox_baseline.y1 - bbox_baseline.y0
    height_bottom = bbox_bottom.y1 - bbox_bottom.y0
    assert numpy.allclose(height_baseline, height_bottom)
    frac = (bbox_baseline.y1 - bbox_bottom.y0) / height_bottom

    plt.close(fig)

    return frac


def _draw_text_data_coord(height_matrix, ax, fontfamily, fontaspect,
                          letterpad, letterheightscale, xpad):
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
        `letterpad` (float)
            Add this much vertical padding between letters.
        `letterheightscale` (float)
            Scale height of letters by this much.
        `xpad` (float)
            x-axis is padded by this many data units on each side.
    """
    fig = ax.get_figure()
    bbox = ax.get_window_extent().transformed(
            fig.dpi_scale_trans.inverted())
    width = bbox.width * fig.dpi * len(height_matrix) / (
            2 * xpad + len(height_matrix))
    height = bbox.height * fig.dpi

    max_stack_height = max(sum([tup[1] for tup in row]) for
                           row in height_matrix)

    letterpadheight = max_stack_height * letterpad

    fontsize = (height / max_stack_height) * 72.0 / fig.dpi
    font = _setup_font(fontsize=fontsize, fontfamily=fontfamily)
    frac_above_baseline = _frac_above_baseline(font)

    fontwidthscale = width * max_stack_height / (height * fontaspect *
                                                 len(height_matrix))

    for xindex, xcol in enumerate(height_matrix):

        ypos = 0
        for letter, letterheight, lettercolor in xcol:
            txt = ax.text(
                xindex,
                ypos,
                letter,
                fontsize=fontsize,
                color=lettercolor,
                ha='left',
                va='baseline',
                fontproperties=font,
                bbox=dict(pad=0, edgecolor='none', facecolor='none')
                )

            txt.set_path_effects([Scale(fontwidthscale,
                    max(0, letterheightscale * letterheight /
                           frac_above_baseline - letterpadheight))])

            ypos += letterheight

    fig.canvas.draw()


def draw_logo(data,
              *,
              x_col,
              letter_col,
              letter_height_col,
              xtick_col=None,
              color_col=None,
              xlabel=None,
              ylabel=None,
              title=None,
              colorscheme=dmslogo.colorschemes.AA_FUNCTIONAL_GROUP,
              missing_color='gray',
              addbreaks=True,
              widthscale=1,
              heightscale=1,
              axisfontscale=1,
              hide_axis=False,
              fontfamily='DejaVu Sans Mono',
              fontaspect=0.58,
              letterpad=0.01,
              letterheightscale=0.98,
              ax=None,
              fixed_ymin=None,
              fixed_ymax=None):
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
        `title` (`None` or str)
            Title to place above plot.
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
        `axisfontscale` (float)
            Scale size of font for axis ticks and labels by this much.
        `hide_axis` (bool)
            Do we hide the axis and tick labels?
        `fontfamily` (str)
            Font to use.
        `fontaspect` (float)
            Aspect ratio of font (height to width). If letters are
            too crowded, increase this.
        `letterpad` (float)
            Add this much fixed vertical padding between letters
            as fraction of total stack height.
        `letterheightscale` (float)
            Scale height of all letters by this much.
        `ax` (`None` or matplotlib axes.Axes object)
            Use to plot on an existing axis.
        `fixed_ymin` (`None` or float)
            If not `None`, then fixed y-axis minimum.
        `fixed_ymax` (`None` or float)
            If not `None`, then fixed y-axis maximum.

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

    # check letters are all upper case
    letters = str(data[letter_col].unique())
    if letters.upper() != letters:
        raise ValueErrors('letters in `letter_col` must be uppercase')

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
    if any(len(set(g[xtick_col])) != 1 for _, g in data.groupby(x_col)):
        raise ValueError('not unique mapping of `x_col` to `xtick_col`')

    # construct height_matrix: list of lists of (letter, hegith, color)
    height_matrix = []
    xticks = []
    lastx = None
    breaks = []
    for x, xdata in (data
                     .sort_values([x_col, letter_height_col])
                     .groupby(x_col)
                     ):

        if addbreaks and (lastx is not None) and (x != lastx + 1):
            breaks.append(len(height_matrix))
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
    max_stack_height = max(sum([tup[1] for tup in row]) for
                           row in height_matrix)

    # setup axis for plotting
    if not ax:
        fig, ax = plt.subplots()
        fig.set_size_inches(
                (widthscale * 0.45 * (nstacks + int(not hide_axis)),
                 heightscale * (2 +  0.5 * int(not hide_axis))))
    else:
        fig = ax.get_figure()

    if title:
        ax.set_title(title, fontsize=20 * axisfontscale)

    xpad = 0.2
    ax.set_xlim(-xpad, nstacks + xpad)
    ylimpad = 0.05 * max_stack_height
    ax.set_ylim(-ylimpad if fixed_ymin is None else fixed_ymin,
                max_stack_height + ylimpad if fixed_ymax is None
                                           else fixed_ymax)

    if not hide_axis:
        ax.set_xticks(numpy.arange(nstacks) + 0.5)
        ax.set_xticklabels(xticks, rotation=90, ha='center', va='top')
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
        ax.tick_params('both', labelsize=12 * axisfontscale)
        ax.set_xlabel(xlabel, fontsize=17 * axisfontscale)
        ax.set_ylabel(ylabel, fontsize=17 * axisfontscale)
        dmslogo.utils.despine(
                ax=ax,
                trim=False,
                top=True,
                right=True)
    else:
        ax.axis('off')

    # draw the letters
    fig.canvas.draw()
    _draw_text_data_coord(height_matrix, ax, fontfamily, fontaspect,
                          letterpad, letterheightscale, xpad)

    # draw the breaks
    for x in breaks:
        # loosely dotted line:
        # https://matplotlib.org/gallery/lines_bars_and_markers/linestyles.html
        ax.axvline(x=x + 0.5, ls=(0, (2, 5)), color='black', lw=1)

    return fig, ax



if __name__ == '__main__':
    import doctest
    doctest.testmod()
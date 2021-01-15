"""
=======
logo
=======

Core logo-drawing functions of `dmslogo`.

Some of this code is borrowed and modified from
`pyseqlogo <https://github.com/saketkc/pyseqlogo>`_.
"""


import glob
import os

import matplotlib.font_manager
import matplotlib.patheffects
import matplotlib.pyplot as plt
import matplotlib.ticker

import numpy

import pandas as pd

import pkg_resources

import dmslogo.colorschemes
import dmslogo.utils


# default font
_DEFAULT_FONT = 'DejaVuSansMonoBold_SeqLogo'

# add fonts to font manager
_FONT_PATH = pkg_resources.resource_filename('dmslogo', 'ttf_fonts/')
if not os.path.isdir(_FONT_PATH):
    raise RuntimeError(f"Cannot find font directory {_FONT_PATH}")

for _fontfile in matplotlib.font_manager.findSystemFonts(_FONT_PATH):
    matplotlib.font_manager.fontManager.addfont(_fontfile)
for _fontfile in matplotlib.font_manager.findSystemFonts(None):
    try:
        matplotlib.font_manager.fontManager.addfont(_fontfile)
    except RuntimeError:
        # problem with loading emoji fonts; solution here is just to
        # skip any fonts that cause problems
        pass
del _fontfile

_fontlist = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
if _DEFAULT_FONT not in _fontlist:
    raise RuntimeError(f"Could not find default font {_DEFAULT_FONT}")
for _fontfile in glob.glob(f"{_FONT_PATH}/*.ttf"):
    _font = os.path.splitext(os.path.basename(_fontfile))[0]
    if _font not in _fontlist:
        raise RuntimeError(f"Could not find font {_font} in file {_fontfile}")


class Scale(matplotlib.patheffects.RendererBase):
    """Scale letters using affine transformation.

    From here: https://www.python-forum.de/viewtopic.php?t=30856
    """

    def __init__(self, sx, sy=None):
        """See main class docstring."""
        self._sx = sx
        self._sy = sy

    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        """Draw the letters."""
        affine = affine.identity().scale(self._sx, self._sy) + affine
        renderer.draw_path(gc, tpath, affine, rgbFace)


class Memoize:
    """Memoize function from https://stackoverflow.com/a/1988826"""

    def __init__(self, f):
        """See main class docstring."""
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        """Call class."""
        if args not in self.memo:
            self.memo[args] = self.f(*args)
        # Warning: You may wish to do a deepcopy here if returning objects
        return self.memo[args]


@Memoize
def _setup_font(fontfamily, fontsize):
    """Get `FontProperties` for `fontfamily` and `fontsize`."""
    font = matplotlib.font_manager.FontProperties(family=fontfamily,
                                                  size=fontsize,
                                                  weight='bold')
    return font


@Memoize
def _frac_above_baseline(font):
    """Fraction of font height that is above baseline.

    Args:
        `font` (FontProperties)
            Font for which we are computing fraction.

    """
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    txt_baseline = ax.text(0, 0, 'A', fontproperties=font,
                           va='baseline', bbox={'pad': 0})
    txt_bottom = ax.text(0, 0, 'A', fontproperties=font,
                         va='bottom', bbox={'pad': 0})

    fig.canvas.draw()
    bbox_baseline = txt_baseline.get_window_extent()
    bbox_bottom = txt_bottom.get_window_extent()

    height_baseline = bbox_baseline.y1 - bbox_baseline.y0
    height_bottom = bbox_bottom.y1 - bbox_bottom.y0
    assert numpy.allclose(height_baseline, height_bottom)
    frac = (bbox_baseline.y1 - bbox_bottom.y0) / height_bottom

    plt.close(fig)

    return frac


def _draw_text_data_coord(height_matrix, ystarts, ax, fontfamily, fontaspect,
                          letterpad, letterheightscale, xpad):
    """Draws logo letters.

    Args:
        `height_matrix` (list of lists)
            Gives letter heights. In the main list, there is a list
            for each site, with the entries being 3-tuples giving
            the letter, its height, its color, and 'pad_below' or
            'pad_above' indicating where vertical padding is added.
        `ystarts` (list)
            Gives y position of bottom of first letter for each site.
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
    # get bbox in **inches**
    bbox = ax.get_window_extent().transformed(
            fig.dpi_scale_trans.inverted())
    width = bbox.width * len(height_matrix) / (
            2 * xpad + len(height_matrix))
    height = bbox.height

    max_stack_height = max(sum(abs(tup[1]) for tup in row) for
                           row in height_matrix)

    if len(ystarts) != len(height_matrix):
        raise ValueError('`ystarts` and `height_matrix` different lengths\n'
                         f"ystarts={ystarts}\nheight_matrix={height_matrix}")

    ymin, ymax = ax.get_ylim()
    yextent = ymax - ymin
    if max_stack_height > yextent:
        raise ValueError('`max_stack_height` exceeds `yextent`')
    if ymin > 0:
        raise ValueError('`ymin` > 0')
    if min(ystarts) < ymin:
        raise ValueError('`ymin` exceeds smallest `ystarts`')

    letterpadheight = yextent * letterpad
    fontsize = 72
    font = _setup_font(fontfamily, fontsize)
    frac_above_baseline = _frac_above_baseline(font)

    fontwidthscale = width / (fontaspect * len(height_matrix))

    for xindex, (xcol, ystart) in enumerate(zip(height_matrix, ystarts)):

        ypos = ystart
        for letter, letterheight, lettercolor, pad_loc in xcol:

            adj_letterheight = letterheightscale * letterheight
            padding = min(letterheight / 2, letterpadheight)
            if pad_loc == 'pad_below':
                ypad = padding + letterheight - adj_letterheight
            elif pad_loc == 'pad_above':
                ypad = 0
            else:
                raise ValueError(f"invalid `pad_loc` {pad_loc}")

            txt = ax.text(
                xindex,
                ypos + ypad,
                letter,
                fontsize=fontsize,
                color=lettercolor,
                ha='left',
                va='baseline',
                fontproperties=font,
                bbox={'pad': 0, 'edgecolor': 'none', 'facecolor': 'none'}
                )

            scaled_height = adj_letterheight / frac_above_baseline
            scaled_padding = padding / frac_above_baseline
            txt.set_path_effects([Scale(fontwidthscale,
                                        ((scaled_height - scaled_padding) *
                                         height / yextent))
                                  ])

            ypos += letterheight


def draw_logo(data,
              *,
              x_col,
              letter_col,
              letter_height_col,
              xtick_col=None,
              color_col=None,
              shade_color_col=None,
              shade_alpha_col=None,
              heatmap_overlays=None,
              xlabel=None,
              ylabel=None,
              title=None,
              colorscheme=dmslogo.colorschemes.AA_FUNCTIONAL_GROUP,
              missing_color='gray',
              addbreaks=True,
              widthscale=1,
              heightscale=1,
              heatmap_overlay_height=0.15,
              axisfontscale=1,
              hide_axis=False,
              fontfamily=_DEFAULT_FONT,
              fontaspect=0.58,
              letterpad=0.0105,
              letterheightscale=0.96,
              ax=None,
              ylim_setter=None,
              fixed_ymin=None,
              fixed_ymax=None,
              clip_negative_heights=False,
              drop_na_letter_heights=True,
              draw_line_at_zero='if_negative',
              ):
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
        `shade_color_col` (`None` or str)
            Column in `data` indicating color to shade each site.
            Must be same color for all letters at site. If a site
            should not be shaded, set to something that evaluates
            to `False` or `NaN`.
        `shade_alpha_col` (`None` or str)
            Column in `data` giving transparency of shading at each site.
        `heatmap_overlays` (`None` or list)
            List of columns in `data` giving colors for each overlay.
        `xlabel` (`None` or str)
            Label for x-axis if not using `xtick_col` or `x_col`.
        `ylabel` (`None` or str)
            Label for y-axis if not using `letter_height_col`.
        `title` (`None` or str)
            Title to place above plot.
        `colorscheme` (dict)
            Color for each letter. Ignored if `color_col` is not `None`.
            See :py:mod:`dmslogo.colorschemes` for some color schemes.
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
        `heatmap_overlay_height` (float)
            Height of heatmap overlays relative to logo.
        `axisfontscale` (float)
            Scale size of font for axis ticks and labels by this much.
        `hide_axis` (bool)
            Do we hide the axis and tick labels?
        `fontfamily` (str)
            Font to use (for logo letters).
        `fontaspect` (float)
            Aspect ratio of logo letter font (height to width). If letters are
            too crowded, increase this.
        `letterpad` (float)
            Add this much fixed vertical padding between letters
            as fraction of total stack height.
        `letterheightscale` (float)
            Scale height of all letters by this much.
        `ax` (`None` or matplotlib axes.Axes object or list of Axes)
            Use to plot on an existing axis. If using `heatmap_overlays`
            then must be list of axes of correct length.
        `ylim_setter` (`None` or :class:`dmslogo.utils.AxLimSetter`)
            Object used to set y-limits. If `None`, a
            :class:`dmslogo.utils.AxLimSetter` is created using
            default parameters). If `fixed_ymin` and/or `fixed_ymax`
            are set, they override the limits from this setter.
        `fixed_ymin` (`None` or float)
            If not `None`, then fixed y-axis minimum.
        `fixed_ymax` (`None` or float)
            If not `None`, then fixed y-axis maximum.
        `clip_negative_heights` (bool)
            Set to 0 any value in `letter_height_col` that is < 0.
        `drop_na_letter_heights` (bool)
            Drop any rows in `data` where `letter_height_col` is NaN.
        `draw_line_at_zero` (str)
            Draw a horizontal line at the value of zero? Can have following
            values: 'if_negative' to only draw line if there are negative
            letter heights, 'always' to always draw line, and 'never' to
            never draw line.

    Returns:
        The 2-tuple `(fig, ax)` giving the figure and axis with the logo plots.
        If using `heatmap_overlays`, then `ax` will be an array of all axes
        (overlays and logo axes).

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
        raise ValueError('letters in `letter_col` must be uppercase')

    # checks on input data
    for col in [letter_height_col, letter_col, x_col, xtick_col]:
        if col not in data.columns:
            raise ValueError(f"`data` lacks column {col}")
    if (color_col is not None) and (color_col not in data.columns):
        raise ValueError(f"`data` lacks column {color_col}")
    if drop_na_letter_heights:
        data = data[-data[letter_height_col].isna()]
        if len(data) == 0:
            raise ValueError('no data after dropping nan heights')
    if clip_negative_heights:
        data = data.assign(**{letter_height_col: lambda x: numpy.clip(
                           x[letter_height_col], 0, None)})
    if any(data[x_col] != data[x_col].astype(int)):
        raise ValueError('`x_col` does not have integer values')
    if any(len(set(g[xtick_col])) != 1 for _, g in data.groupby(x_col)):
        raise ValueError('not unique mapping of `x_col` to `xtick_col`')

    # construct height_matrix: list of lists of (letter, height, color)
    height_matrix = []
    min_by_site = []
    max_by_site = []
    min_by_site_nonempty = []
    max_by_site_nonempty = []
    xticklabels = []
    xticks = []
    lastx = None
    breaks = []
    x_to_xtick = {}
    xtick = 0.5
    for x, xdata in (data
                     .sort_values([x_col, letter_height_col])
                     .groupby(x_col)
                     ):

        if addbreaks and (lastx is not None) and (x != lastx + 1):
            breaks.append(len(height_matrix))
            height_matrix.append([])
            min_by_site.append(0)
            max_by_site.append(0)
            xtick += 1
        lastx = x

        if len(xdata[letter_col]) != xdata[letter_col].nunique():
            raise ValueError(f"duplicate letters for `x_col` {x}")

        min_by_site.append(xdata[letter_height_col].clip(None, 0).sum())
        max_by_site.append(xdata[letter_height_col].clip(0, None).sum())
        min_by_site_nonempty.append(min_by_site[-1])
        max_by_site_nonempty.append(max_by_site[-1])
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
            row.append((letter,
                        abs(letter_height),
                        color,
                        'pad_below' if letter_height >= 0 else 'pad_above'))
        height_matrix.append(row)

        assert len(xdata[xtick_col].unique()) == 1
        xticklabels.append(str(xdata[xtick_col].values[0]))

        xticks.append(xtick)
        x_to_xtick[x] = xtick
        xtick += 1

    assert len(xticklabels) == len(xticks)

    if draw_line_at_zero == 'always':
        line_at_zero = True
    elif draw_line_at_zero == 'never':
        line_at_zero = False
    elif draw_line_at_zero == 'if_negative':
        if min(min_by_site) < 0:
            line_at_zero = True
        else:
            line_at_zero = False
    else:
        raise ValueError(f"invalid `draw_line_at_zero` {draw_line_at_zero}")

    # do we have overlays?
    if heatmap_overlays:
        noverlays = len(heatmap_overlays)
        for overlay in heatmap_overlays:
            if overlay not in data.columns:
                raise ValueError(f"`data` lacks `heatmap_overlay` {overlay}")
            else:
                overlay_data = (data
                                [[x_col] + list(heatmap_overlays)]
                                .drop_duplicates()
                                )
                if not all(overlay_data.values == (overlay_data
                                                   .groupby(x_col,
                                                            as_index=False)
                                                   .first()
                                                   )
                           ):
                    raise ValueError('Overlay not unique per site:\n' +
                                     overlay_data)
    else:
        heatmap_overlays = []
        noverlays = 0

    # setup axis for plotting
    if not ax:
        fig, axes = plt.subplots(
                nrows=1 + noverlays,
                ncols=1,
                sharex=True,
                sharey=False,
                squeeze=False,
                gridspec_kw={'height_ratios':
                             [heatmap_overlay_height] * noverlays + [1],
                             }
                )
        axes = axes.ravel()
        assert len(axes) == 1 + noverlays, axes
        fig.set_size_inches(
                (widthscale * 0.35 * (len(height_matrix) +
                                      int(not hide_axis)),
                 heightscale * (2 + 0.5 * int(not hide_axis) +
                                2 * noverlays * heatmap_overlay_height +
                                0.5 * int(bool(title))
                                )
                 ))
        ax = axes[-1]
    else:
        if noverlays:
            if len(ax) != noverlays + 1:
                raise ValueError(f"`ax` not axes for {noverlays} overlays")
                axes = ax
                ax = axes[0]
        else:
            if not isinstance(ax, plt.Axes):
                raise TypeError(f"`ax` is not an Axis: {ax}")
            axes = [ax]
        fig = ax.get_figure()

    # draw overlays
    for overlay, overlay_ax in zip(heatmap_overlays, axes):
        overlay_ax.set_yticks([0.5])
        overlay_ax.set_yticklabels([overlay])
        overlay_ax.tick_params('y', labelsize=14 * axisfontscale, length=0)
        dmslogo.utils.despine(
                ax=overlay_ax,
                top=True,
                right=True,
                left=True,
                bottom=True,
                )
        overlay_ax.get_xaxis().set_visible(False)
        for x, color in overlay_data.set_index(x_col)[overlay].items():
            xtick = x_to_xtick[x]
            overlay_ax.add_patch(
                    plt.Rectangle(xy=(xtick - 0.5, 0),
                                  width=1,
                                  height=1,
                                  facecolor=color,
                                  edgecolor='black',
                                  linewidth=1,
                                  clip_on=False,
                                  )
                    )

    if title:
        axes[0].set_title(title, fontsize=17 * axisfontscale)

    xpad = 0.2
    ax.set_xlim(-xpad, len(height_matrix) + xpad)

    # set y-limits
    if ylim_setter is None:
        ylim_setter = dmslogo.utils.AxLimSetter()
    ymin1, ymax1 = ylim_setter.get_lims(min_by_site_nonempty)
    ymin2, ymax2 = ylim_setter.get_lims(max_by_site_nonempty)
    ymin = min(ymin1, ymin2)
    ymax = max(ymax1, ymax2)
    if fixed_ymin is not None:
        ymin = fixed_ymin
    if fixed_ymax is not None:
        ymax = fixed_ymax
    ax.set_ylim(ymin, ymax)

    if not hide_axis:
        ax.set_xticks(xticks)
        ax.tick_params(length=5, width=1)
        ax.set_xticklabels(xticklabels, rotation=90, ha='center', va='top')
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
    _draw_text_data_coord(height_matrix, min_by_site, ax, fontfamily,
                          fontaspect, letterpad, letterheightscale, xpad)

    # draw the breaks
    for x in breaks:
        # loosely dotted line:
        # https://matplotlib.org/gallery/lines_bars_and_markers/linestyles.html
        ax.axvline(x=x + 0.5, ls=(0, (2, 5)), color='black', lw=1)

    # draw line at zero
    if line_at_zero:
        ax.axhline(y=0, ls='-', color='black', lw=1, zorder=4)

    # draw the shading
    if shade_color_col is not None:
        if shade_alpha_col is None:
            raise ValueError('`shade_color_col` without `shade_alpha_col`')
        if shade_color_col not in data.columns:
            raise ValueError(f"data lacks `shade_color_col` {shade_color_col}")
        if shade_alpha_col not in data.columns:
            raise ValueError(f"data lacks `shade_alpha_col` {shade_alpha_col}")
        for x, xdata in data.groupby(x_col):
            shade_color = xdata[shade_color_col].unique()
            if len(shade_color) != 1:
                raise ValueError(f"not exactly one shade color for {x}")
            else:
                shade_color = shade_color[0]
            shade_alpha = xdata[shade_alpha_col].unique()
            if len(shade_alpha) != 1:
                raise ValueError(f"not exactly one shade alpha for {x}")
            else:
                shade_alpha = shade_alpha[0]
            if pd.isnull(shade_color) or not shade_color:
                continue
            elif not (0 <= shade_alpha <= 1):
                raise ValueError(f"shade alpha not between 0 and 1 for {x}")
            xtick = x_to_xtick[x]
            ax.axvspan(xmin=xtick - 0.5, xmax=xtick + 0.5,
                       edgecolor=None, facecolor=shade_color,
                       alpha=shade_alpha)
    elif shade_alpha_col is not None:
        raise ValueError('`shade_alpha_col` without `shade_color_col`')

    if len(axes) == 1:
        return fig, ax
    else:
        return fig, axes


if __name__ == '__main__':
    import doctest
    doctest.testmod()

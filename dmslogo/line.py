"""
======
line
======

Draw line plots of site-level properties.
"""


import matplotlib.pyplot as plt
import matplotlib.ticker

import numpy

import dmslogo.colorschemes
import dmslogo.utils


def data_units_from_linewidth(linewidth, ax, reference):
    """Convert linewidth in points to data units.

    Args:
        `linewidth` (float)
            Linewidth in points.
        `ax` (matplotlib axis)
            The axis used to extract the relevant transformation
            (data limits and size must not change afterwards).
        `reference` (str)
            The axis that is taken as a reference for the data width.
            Possible values: 'x' and 'y'.

    Returns
        Linewidth in data units.

    Function is the inverse of the one defined here:
    https://stackoverflow.com/a/35501485

    """
    fig = ax.get_figure()
    if reference == 'x':
        length = fig.bbox_inches.width * ax.get_position().width
        value_range = numpy.diff(ax.get_xlim())
    elif reference == 'y':
        length = fig.bbox_inches.height * ax.get_position().height
        value_range = numpy.diff(ax.get_ylim())
    else:
        raise ValueError(f"invalid `ax` of {ax}")
    # Convert length to points
    length *= 72
    # Scale linewidth to value range
    return linewidth / (length / value_range)


def draw_line(data,
              *,
              x_col,
              height_col,
              xtick_col=None,
              show_col=None,
              xlabel=None,
              ylabel=None,
              title=None,
              color='black',
              show_color=dmslogo.colorschemes.CBPALETTE[1],
              linewidth=1,
              widthscale=1,
              heightscale=1,
              axisfontscale=1,
              hide_axis=False,
              ax=None,
              fixed_ymin=None,
              fixed_ymax=None):
    """Draw line plot.

    Args:
        `data` (pandas DataFrame)
            Holds data to plot. If there are duplicate rows for
            the columns of interest, removes duplicates.
        `height_col` (str)
            Column in `data` with line height.
        `x_col` (str)
            Column in `data` with integer site numbers. Must be full
            set of sequential numbers, gaps in numbering not allowed.
        `xtick_col` (`None` or str)
            Column in `data` used to label sites if not using `x_col`.
        `show_col` (`None` or str)
            Underline sites where this column is True. Useful for
            marking selected sites that are zoomed in logo plots.
        `xlabel` (`None` or str)
            Label for x-axis if not using `xtick_col` or `x_col`.
        `ylabel` (`None` or str)
            Label for y-axis if not using `height_col`.
        `title` (`None` or str)
            Title to place above plot.
        `color` (str)
            Color of line.
        `show_color` (str)
            Color of underlines specified by `show_col`.
        `linewidth` (float)
            Width of line.
        `widthscale` (float)
            Scale width by this much.
        `heightscale` (float)
            Scale height by this much.
        `axisfontscale` (float)
            Scale size of font for axis ticks and labels by this much.
        `hide_axis` (bool)
            Do we hide the axis and tick labels?
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
        ylabel = height_col

    cols = list({x_col, xtick_col, height_col})
    if show_col:
        cols.append(show_col)
        if not data[show_col].dtype == bool:
            raise ValueError('`show_col` is not bool')
    for col in cols:
        if col not in data.columns:
            raise ValueError(f"`data` lacks column {col}")

    data = data[cols].drop_duplicates().sort_values(x_col)

    if any(data[x_col] != data[x_col].astype(int)):
        raise ValueError('`x_col` does not have integer values')

    xmin = data[x_col].min()
    xmax = data[x_col].max()
    xlen = xmax - xmin + 1
    if any(list(range(xmin, xmax + 1)) != data[x_col].unique()):
        raise ValueError('`x_col` not sequential unbroken integers')

    if len(data[x_col]) != len(data[x_col].unique()):
        raise ValueError(f"not unique mapping of `x_col` to other cols {cols}")

    assert len(data) == xlen

    ylimpad = 0.05 * (data[height_col].max() - data[height_col].min())
    if fixed_ymax is None:
        ymax = data[height_col].max() + ylimpad
    else:
        if fixed_ymax < data[height_col].max():
            raise ValueError('`fixed_ymax` less then max of data')
        ymax = fixed_ymax
    if data[height_col].min() < 0:
        raise ValueError('cannot handle negatives in `height_col`')
    if fixed_ymin is None:
        ymin = -ylimpad
    else:
        if fixed_ymin > 0:
            raise ValueError('`fixed_ymin` greater than 0')
        ymin = fixed_ymin

    # setup axis for plotting
    if not ax:
        fig, ax = plt.subplots()
        # width per site ranges from 0.02 for xlen <= 100 to
        # 0.07 for xlen > 700
        xwidth = 0.02 - 0.013 * (min(700, max(100, xlen)) - 100
                                 ) / (700 - 100)
        fig.set_size_inches(
                (widthscale * xwidth * xlen + 0.5 * int(not hide_axis),
                 heightscale * (2 + 0.5 * int(not hide_axis) +
                                0.5 * int(bool(title))))
                            )
    else:
        fig = ax.get_figure()

    if title:
        ax.set_title(title, fontsize=17 * axisfontscale)

    ax.set_xlim(xmin - 0.5 - 0.02 * xlen,
                xmax + 0.5 + 0.02 * xlen)
    ax.set_ylim(ymin, ymax)

    if not hide_axis:
        xbreaks, xlabels = dmslogo.utils.breaksAndLabels(
                            data[x_col].tolist(),
                            data[xtick_col].tolist(),
                            max(4, xlen // 50))
        ax.set_xticks(xbreaks)
        ax.tick_params(length=5, width=1)
        ax.set_xticklabels(xlabels, rotation=90, ha='center', va='top')
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

    xdata = data[x_col].tolist()
    ydata = data[height_col].tolist()
    # plot with 0.5 before / after last points so steps full length
    ax.step([xmin - 0.5] + xdata + [xmax + 0.5],
            [ydata[0]] + ydata + [ydata[-1]],
            color=color,
            where='mid',
            linewidth=linewidth)

    if show_col:
        lw_to_xdata = data_units_from_linewidth(linewidth, ax, 'x')
        lw_to_ydata = data_units_from_linewidth(linewidth, ax, 'y')
        for x in data.query(f"{show_col}")[x_col].tolist():
            ax.add_patch(plt.Rectangle(
                            xy=(x - 0.5 - lw_to_xdata, ymin),
                            width=2 + 1 * lw_to_xdata,
                            height=-ymin - lw_to_ydata,
                            edgecolor='none',
                            facecolor=show_color,
                            ))

    return fig, ax


if __name__ == '__main__':
    import doctest
    doctest.testmod()

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
        value_range = numpy.diff(ax.get_xlim())[0]
    elif reference == 'y':
        length = fig.bbox_inches.height * ax.get_position().height
        value_range = numpy.diff(ax.get_ylim())[0]
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
              height_col2=None,
              xtick_col=None,
              show_col=None,
              xlabel=None,
              ylabel=None,
              title=None,
              color='black',
              color2='gray',
              show_color=dmslogo.colorschemes.CBPALETTE[1],
              linewidth=1,
              widthscale=1,
              heightscale=1,
              axisfontscale=1,
              hide_axis=False,
              ax=None,
              ylim_setter=None,
              fixed_ymin=None,
              fixed_ymax=None):
    """Draw line plot.

    Args:
        `data` (pandas DataFrame)
            Holds data to plot. If there are duplicate rows for
            the columns of interest, removes duplicates.
        `height_col` (str)
            Column in `data` with line height.
        `height_col2` (str or `None`)
            Optional second column in `data` giving second line height. This is
            typically useful when `height_col` has positive values and you also
            want to plot negative values: those can be in `height_col2`.
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
            Color of line plotting data in `height_col`.
        `color2` (str)
            Color of line plotting any data in `height_col2`.
        `show_color` (str or `None`)
            Color of underlines specified by `show_col`, or `None` if
            you don't want to show underlines.
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
        `ylim_setter` (`None` or :class:`dmslogo.utils.AxLimSetter`)
            Object used to set y-limits. If `None`, a
            :class:`dmslogo.utils.AxLimSetter` is created using
            default parameters). If `fixed_ymin` and/or `fixed_ymax`
            are set, they override the limits from this setter.
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
    if height_col2 is not None:
        cols.append(height_col2)
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
    if (xlen != data[x_col].nunique()) or any(list(range(xmin, xmax + 1)) !=
                                              data[x_col].unique()):
        raise ValueError('`x_col` not sequential unbroken integers')

    if len(data[x_col]) != len(data[x_col].unique()):
        raise ValueError(f"not unique mapping of `x_col` to other cols {cols}")

    assert len(data) == xlen

    # set y-limits
    if ylim_setter is None:
        ylim_setter = dmslogo.utils.AxLimSetter()
    ymin, ymax = ylim_setter.get_lims(data[height_col])
    ydata_min = data[height_col].min()
    ydata_max = data[height_col].max()
    if ylim_setter.include_zero:
        ydata_min = min(0, ydata_min)
        ydata_max = max(0, ydata_max)
    if height_col2 is not None:
        ymin2, ymax2 = ylim_setter.get_lims(data[height_col2])
        ymin = min(ymin, ymin2)
        ymax = max(ymax, ymax2)
        ydata_min = min(ydata_min, data[height_col2].min())
        ydata_max = max(ydata_max, data[height_col2].max())
    if fixed_ymax is not None:
        if fixed_ymax < ydata_max:
            raise ValueError('`fixed_ymax` less then max of data')
        ymax = fixed_ymax
    if fixed_ymin is not None:
        if fixed_ymin > ydata_min:
            raise ValueError('`fixed_ymin` greater then min of data')
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

    if height_col2 is not None:
        ydata2 = data[height_col2].tolist()
        ax.step([xmin - 0.5] + xdata + [xmax + 0.5],
                [ydata2[0]] + ydata2 + [ydata2[-1]],
                color=color2,
                where='mid',
                linewidth=linewidth)

    if show_col and show_color is not None:
        lw_to_xdata = data_units_from_linewidth(linewidth, ax, 'x')
        lw_to_ydata = data_units_from_linewidth(linewidth, ax, 'y')
        for x in data.query(f"{show_col}")[x_col].tolist():
            ax.add_patch(plt.Rectangle(
                            xy=(x - 0.5 - lw_to_xdata, ymin),
                            width=2 + 1 * lw_to_xdata,
                            height=(ydata_min - ymin) - lw_to_ydata,
                            edgecolor='none',
                            facecolor=show_color,
                            ))

    return fig, ax


if __name__ == '__main__':
    import doctest
    doctest.testmod()

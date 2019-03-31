"""
========
utils
========

Utility functions for plotting.
"""


import matplotlib.pyplot as plt
import matplotlib.ticker

import numpy as np


def breaksAndLabels(xi, x, n):
    """Get breaks and labels for an axis.

    Useful when you would like to re-label a numeric x-axis
    with string labels.

    Uses `matplotlib.ticker.MaxNLocator` to choose pretty breaks.

    Args:
        `xi` (list or array)
            Integer values actually assigned to axis points.
        `x` (list)
            Strings corresponding to each numeric value in `xi`.
        `n` (int)
            Approximate number of ticks to use.

    Returns:
        The tuple `(breaks, labels)` where `breaks` gives the
        locations of breaks taken from `xi`, and `labels` is
        the label for each break.

    >>> xi = list(range(213))
    >>> x = [str(i + 1) for i in xi]
    >>> (breaks, labels) = breaksAndLabels(xi, x, 5)
    >>> breaks
    [0, 50, 100, 150, 200]
    >>> labels
    ['1', '51', '101', '151', '201']

    """
    if len(xi) != len(x):
        raise ValueError('`xi` and `x` differ in length.')
    if not all(isinstance(i, (int, np.integer)) for i in xi):
        raise ValueError('xi not integer values')
    xi = list(xi)
    if sorted(set(xi)) != xi:
        raise ValueError('`xi` not unique and ordered')
    breaks = matplotlib.ticker.MaxNLocator(n).tick_values(xi[0], xi[-1])
    breaks = [int(i) for i in breaks if xi[0] <= i <= xi[-1]]
    labels = [x[xi.index(i)] for i in breaks]
    return (breaks, labels)


def _set_spine_position(spine, position):
    """
    Set the spine's position without resetting an associated axis.
    As of matplotlib v. 1.0.0, if a spine has an associated axis, then
    spine.set_position() calls axis.cla(), which resets locators, formatters,
    etc.  We temporarily replace that call with axis.reset_ticks(), which is
    sufficient for our purposes.

    This is borrowed from here:
    https://github.com/mwaskom/seaborn/blob/0beede57152ce80ce1d4ef5d0c0f1cb61d118375/seaborn/utils.py#L265
    """
    axis = spine.axis
    if axis is not None:
        cla = axis.cla
        axis.cla = axis.reset_ticks
    spine.set_position(position)
    if axis is not None:
        axis.cla = cla


def despine(fig=None,
            ax=None,
            top=True,
            right=True,
            left=False,
            bottom=False,
            offset=None,
            trim=False):
    """Remove the top and right spines from plot(s).

    Args:
        `fig` (matplotlib figure)
            Figure to despine all axes of, default uses current figure.
        `ax` (matplotlib axes)
            Specific axes object to despine.
        `top`, `right`, `left`, `bottom` (bool)
            If True, remove that spine.
        `offset` (int or dict)
            Absolute distance, in points, spines should be moved away
            from the axes (negative values move spines inward).
            A single value applies to all spines; a dict can be used
            to set offset values per side.
        `trim` (bool)
            If True, limit spines to the smallest and largest major tick
            on each non-despined axis.
    """
    # Get references to the axes we want
    if fig is None and ax is None:
        axes = plt.gcf().axes
    elif fig is not None:
        axes = fig.axes
    elif ax is not None:
        axes = [ax]

    for ax_i in axes:
        for side in ["top", "right", "left", "bottom"]:
            # Toggle the spine objects
            is_visible = not locals()[side]
            ax_i.spines[side].set_visible(is_visible)
            if offset is not None and is_visible:
                try:
                    val = offset.get(side, 0)
                except AttributeError:
                    val = offset
                _set_spine_position(ax_i.spines[side], ('outward', val))

        # Set the ticks appropriately
        if bottom:
            ax_i.xaxis.tick_top()
        if top:
            ax_i.xaxis.tick_bottom()
        if left:
            ax_i.yaxis.tick_right()
        if right:
            ax_i.yaxis.tick_left()

        if trim:
            # clip off the parts of the spines that extend past major ticks
            xticks = ax_i.get_xticks()
            if xticks.size:
                firsttick = np.compress(xticks >= min(ax_i.get_xlim()),
                                        xticks)[0]
                lasttick = np.compress(xticks <= max(ax_i.get_xlim()),
                                       xticks)[-1]
                ax_i.spines['bottom'].set_bounds(firsttick, lasttick)
                ax_i.spines['top'].set_bounds(firsttick, lasttick)
                newticks = xticks.compress(xticks <= lasttick)
                newticks = newticks.compress(newticks >= firsttick)
                ax_i.set_xticks(newticks)

            yticks = ax_i.get_yticks()
            if yticks.size:
                firsttick = np.compress(yticks >= min(ax_i.get_ylim()),
                                        yticks)[0]
                lasttick = np.compress(yticks <= max(ax_i.get_ylim()),
                                       yticks)[-1]
                ax_i.spines['left'].set_bounds(firsttick, lasttick)
                ax_i.spines['right'].set_bounds(firsttick, lasttick)
                newticks = yticks.compress(yticks <= lasttick)
                newticks = newticks.compress(newticks >= firsttick)
                ax_i.set_yticks(newticks)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

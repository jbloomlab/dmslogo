"""
========
utils
========

Utility functions for plotting.
"""


import matplotlib.pyplot as plt
import matplotlib.ticker

import numpy


class AxLimSetter:
    """Object to determine axis limits from data.

    Args:
        datalim_pad (float >= 0)
            Padding of data limits.
        include_zero (bool)
            Extend upper and lower data limits to ensure they include zero?
        max_from_quantile (`None` or 2-tuple `(quantile, frac)`)
            Used to set limits based on quantiles of data as described below.
        min_from_quantile (`None` or 2-tuple `(quantile, frac)`)
            Used to set limits based on quantiles of data as described below.
        all_equal_data ('raise' or 2-tuple `(minus_min, plus_max)`)
            If all the data are equal, it will not be possible to set
            limits using algorithm below. In this case, raise an error
            or add the indicated amounts to the data limits.

    The axis limits may just be simple padding of the data limits, but
    the `max_from_quantile` and `min_from_quantile` arguments allow the
    option to set limits in a meaningful way so data that are just "noise"
    of very similar values are plotted far inside the axis limits.
    Specifically, axis limits are determined by :meth:`AxLimSetter.get_lims`
    as follows:

      1. The user passes the data, and the upper and lower data limits are
         determined as the simple min and max of the data.

      2. If `include_zero`, these data limits are adjusted to ensure the lower
         data limit is <= 0 and the upper data limit is >= 0.

      3. If `max_from_quantile` is not `None`, the upper axis limit is
         set so that the indicated quantile of the data is `frac` of the
         way from the lower data limit to the upper axis limit. However,
         if the data max exceeds the upper axis limit this way, then
         the upper axis limit is set to the data max.

      4. If `min_from_quantile` is not `None`, similar setting of the
         lower axis limit is done.

      5. The limits from above are padded by `datalim_pad` to the total
         extent of the axis on both sides.

    Example that just adds simple padding to data:

    >>> data = [0.5, 0.6, 0.4, 0.4, 0.3, 0.5]
    >>> setter_default = AxLimSetter()
    >>> setter_default.get_lims(data)
    (-0.03, 0.63)

    Now use the `max_from_quantile` option to set an upper limit
    that substantially exceeds the "noise" of the all-similar values:

    >>> setter_max_quantile = AxLimSetter(max_from_quantile=(0.5, 0.05))
    >>> setter_max_quantile.get_lims(data)
    (-0.45, 9.45)

    """

    def __init__(self,
                 *,
                 datalim_pad=0.05,
                 include_zero=True,
                 max_from_quantile=None,
                 min_from_quantile=None,
                 all_equal_data=(-0.001, 0.001),
                 ):
        """See main class docstring."""
        if not isinstance(include_zero, bool):
            raise ValueError(f"`include_zero` not bool: {include_zero}")
        self.include_zero = include_zero

        if datalim_pad < 0:
            raise ValueError(f"`datalim_pad` must be > 0: {datalim_pad}")
        self._datalim_pad = datalim_pad

        self._quantile_lims = {}
        for arg, lim in [(max_from_quantile, 'max'),
                         (min_from_quantile, 'min')]:
            if arg is None:
                self._quantile_lims[f"{lim}_from_quantile"] = False
            elif isinstance(arg, (tuple, list)) and len(arg) == 2:
                self._quantile_lims[f"{lim}_from_quantile"] = True
                quantile, frac = arg
                if not (0 < quantile < 1):
                    raise ValueError(f"quantile for `{lim}_from_quantile` "
                                     'must be > 0 and < 1')
                if not (0 < frac < 1):
                    raise ValueError(f"frac for `{lim}_from_quantile` "
                                     'must be > 0 and < 1')
                self._quantile_lims[f"{lim}_quantile"] = quantile
                self._quantile_lims[f"{lim}_frac"] = frac
            else:
                raise ValueError(f"invalid `{lim}_from_quantile` of {arg}")

        if all_equal_data == 'raise':
            self._all_equal_data = all_equal_data
        elif (isinstance(all_equal_data, (list, tuple)) and
              len(all_equal_data) == 2):
            if all_equal_data[0] > 0:
                raise ValueError('first element of `all_equal_data` > 0')
            if all_equal_data[1] < 0:
                raise ValueError('second element of `all_equal_data` < 0')
            if all_equal_data[0] == all_equal_data[1]:
                raise ValueError('`all_equal_data` cannot be all 0')
            self._all_equal_data = tuple(all_equal_data)
        else:
            raise ValueError(f"invalid `all_equal_data`: {all_equal_data}")

    def get_lims(self, data):
        """Get 2-tuple `(ax_min, ax_max)` given list or array of data."""
        datamin = min(data)
        datamax = max(data)

        if self.include_zero:
            datamax = max(0, datamax)
            datamin = min(0, datamin)

        qlims = {'max': datamax, 'min': datamin}
        for lim, other in [('max', datamin), ('min', datamax)]:
            if self._quantile_lims[f"{lim}_from_quantile"]:
                quantile = self._quantile_lims[f"{lim}_quantile"]
                quantile_val = numpy.quantile(data, quantile)
                frac = self._quantile_lims[f"{lim}_frac"]
                qlims[lim] = other + (quantile_val - other) / frac
        datamax = max(datamax, qlims['max'])
        datamin = min(datamin, qlims['min'])

        assert datamax >= datamin
        if datamax == datamin:
            if self._all_equal_data == 'raise':
                raise ValueError('data min & max equal, see `all_equal_data`')
            else:
                datamin += self._all_equal_data[0]
                datamax += self._all_equal_data[1]

        extent = datamax - datamin
        assert extent > 0
        datamin -= self._datalim_pad * extent
        datamax += self._datalim_pad * extent

        return (datamin, datamax)


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
    if not all(isinstance(i, (int, numpy.integer)) for i in xi):
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
                firsttick = numpy.compress(xticks >= min(ax_i.get_xlim()),
                                           xticks)[0]
                lasttick = numpy.compress(xticks <= max(ax_i.get_xlim()),
                                          xticks)[-1]
                ax_i.spines['bottom'].set_bounds(firsttick, lasttick)
                ax_i.spines['top'].set_bounds(firsttick, lasttick)
                newticks = xticks.compress(xticks <= lasttick)
                newticks = newticks.compress(newticks >= firsttick)
                ax_i.set_xticks(newticks)

            yticks = ax_i.get_yticks()
            if yticks.size:
                firsttick = numpy.compress(yticks >= min(ax_i.get_ylim()),
                                           yticks)[0]
                lasttick = numpy.compress(yticks <= max(ax_i.get_ylim()),
                                          yticks)[-1]
                ax_i.spines['left'].set_bounds(firsttick, lasttick)
                ax_i.spines['right'].set_bounds(firsttick, lasttick)
                newticks = yticks.compress(yticks <= lasttick)
                newticks = newticks.compress(newticks >= firsttick)
                ax_i.set_yticks(newticks)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

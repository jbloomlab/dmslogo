"""
======
facet
======

Facet multiple plots on the same figure."""


import collections

import matplotlib.pyplot as plt

import dmslogo


def facet_plot(
            data,
            *,
            x_col,
            show_col,
            height_per_ax=2.5,
            gridrow_col=None,
            gridcol_col=None,
            draw_line_kwargs=None,
            draw_logo_kwargs=None,
            line_titlesuffix='',
            logo_titlesuffix='',
            hspace=0.8,
            wspace=1.1,
            share_xlabel=False,
            share_ylabel=False,
            ):
    """Facet together plots of different types on same figure.

    Useful for combining multiple instances of the plots you
    could create with :py:mod:`dmslogo.logo.draw_logo` and
    :py:mod:`dmslogo.line.draw_line`.

    Args:
        `data` (pandas DataFrame)
            The data to plot.
        `x_col` (str)
            Column in `data` with x-axis values, as for
            :py:mod:`dmslogo.logo.draw_logo` and
            :py:mod:`dmslogo.line.draw_line`.
        `show_col` (str or `None`)
            Column in `data` with x-axis values to highlight in line
            plots and to show in logo plots.
        `height_per_ax` (float)
            Height of each axis in the faceted plot.
        `gridrow_col` (str or `None`)
            Column in `data` to facet over for rows of plot.
        `gridcol_col` (str or `None`)
            Column in data to facet over for columns of plot.
        `draw_line_kwargs` (dict)
            All arguments to be passed to
            :py:mod:`dmslogo.line.draw_line`
            **except** `x_col`, `show_col`, and `title`. These
            are passed separately, or (in case of title) come
            from faceting variables.
        `draw_logo_kwargs`
            Like `draw_line_kwargs` but for
            :py:mod:`dmslogo.logo.draw_logo`.
        `line_titlesuffix` (str or `None`)
            String suffixed to titles for line plots.
        `logo_titlesuffix`
            String suffixed to titles for logo plots.
        `hspace` (float)
            Vertical space between axes.
        `wspace` (float)
            Horizontal space between axes.
        `share_xlabel` (bool)
            Share the x-labels across the line and logo plots.
        `share_ylabel` (bool)
            Share the y-labels across the line and logo plots.

    Returns:
        The 2-tuple `fig, axes` where `fig` is the matplotlib
        Figure and `axes` is a numpy ndarray of the figure axes.

    `x_col` and `show_col` must have the same unique entries in `data`
    for all groups in being faceted over.
    """
    if gridrow_col is None:
        gridrow_col = '_gridrow_col_'
        if gridrow_col in data.columns:
            raise ValueError(f"`data` already has column {gridrow_col}")
        data = data.assign(**{gridrow_col: ''})
    if gridcol_col is None:
        gridcol_col = '_gridcol_col_'
        if gridcol_col in data.columns:
            raise ValueError(f"`data` already has column {gridcol_col}")
        data = data.assign(**{gridcol_col: ''})
    cols = [gridrow_col, gridcol_col, x_col]
    if show_col is not None:
        cols.append(show_col)
    for col in cols:
        if col not in data.columns:
            raise ValueError(f"no {col} column in `data`")

    # make sure all groups have same x_col and show_col
    groups = (data
              [cols]
              .drop_duplicates()
              .sort_values(x_col)
              .groupby([gridrow_col, gridcol_col])
              )
    firstgroupname, firstgroup = list(groups)[0]
    firstgroup = firstgroup.reset_index(drop=True)
    for groupname, group in groups:
        assert len(group), f"empty group {groupname}"
        group = group.reset_index(drop=True)
        for col in cols[2:]:
            if any(firstgroup[col] != group[col]):
                raise ValueError(
                      f"different entries for {col} "
                      f"in `data`, differs between {firstgroupname} "
                      f"and {groupname}:\n"
                      f"{firstgroup[col]}\n{group[col]}")

    # determine which draw_funcs are being used
    draw_funcs = collections.OrderedDict()
    possible_funcs = [('draw_line', draw_line_kwargs, line_titlesuffix),
                      ('draw_logo', draw_logo_kwargs, logo_titlesuffix)]
    for name, kwargs, titlesuffix in possible_funcs:
        if kwargs is not None:
            for col in ['ax', 'title']:
                if col in kwargs:
                    raise ValueError(f"{name}_kwargs can't have {col}")
            if 'heightscale' in kwargs:
                raise ValueError(f"do not set `heightscale` in "
                                 f"{name}_kwargs; use `height_per_ax`")
            draw_funcs[name] = dict(kwargs=kwargs,
                                    func=getattr(dmslogo, name),
                                    data=data,
                                    titlesuffix=titlesuffix
                                    )
            if name == 'draw_logo' and show_col is not None:
                draw_funcs[name]['data'] = data.query(show_col)
            if not len(draw_funcs[name]['data']):
                raise ValueError(
                        f"no data for {name}. You passed empty `data` "
                        f"or `show_col` ({show_col}) is all False.")
    if len(draw_funcs) < 1:
        raise ValueError('set at least one of: ' + ', '.join(tup[0] +
                         '_kwargs' for tup in possible_funcs))

    # harmonize top-function arg columns with plotting kwargs
    for name, name_d in draw_funcs.items():
        for colname, col in [('x_col', x_col), ('show_col', show_col)]:
            if (colname in name_d['kwargs']) and (
                    name_d['kwargs'][colname] != col):
                raise ValueError(f"{colname} is in {name}_kwargs; "
                                 'should only be specified via the top '
                                 f"function-level argument {colname}")
            if (colname != 'show_col') or (name == "draw_line"):
                name_d['kwargs'][colname] = col

    nrows = len(data[gridrow_col].unique())
    nfuncs = len(draw_funcs)
    ncols_per_func = len(data[gridcol_col].unique())

    # get sizes of fig, axis limits of plots for each func
    for name, name_d in draw_funcs.items():

        for i, idata in name_d['data'].groupby(([gridrow_col,
                                                 gridcol_col])):
            fig, ax = name_d['func'](idata, **name_d['kwargs'])
            fig.tight_layout()
            width = fig.get_size_inches()[0]
            xticks = list(ax.get_xticks())
            xticklabels = [t.get_text() for t in ax.get_xticklabels()]
            ymin, ymax = ax.get_ylim()
            plt.close(fig)
            for key, val in [('width', width),
                             ('xticks', xticks),
                             ('xticklabels', xticklabels)]:
                if key not in name_d:
                    name_d[key] = val
                elif name_d[key] != val:
                    raise ValueError(f"inconsistent {key} for {name}: "
                                     f"{val} {name_d[key]}")
            if 'ymin' not in name_d:
                name_d['ymin'] = ymin
            name_d['ymin'] = min(name_d['ymin'], ymin)
            if 'ymax' not in name_d:
                name_d['ymax'] = ymax
            name_d['ymax'] = max(name_d['ymax'], ymax)

        # add the fixed y limits
        name_d['kwargs']['fixed_ymin'] = name_d['ymin']
        name_d['kwargs']['fixed_ymax'] = name_d['ymax']

    # make figure
    fig, axes = plt.subplots(
                    nrows,
                    nfuncs * ncols_per_func,
                    squeeze=False,
                    gridspec_kw={'width_ratios': [d['width']
                                 for d in draw_funcs.values()
                                 for _ in range(ncols_per_func)]}
                    )
    width = ncols_per_func * sum(d['width'] for d in
                                 draw_funcs.values())
    height = nrows * height_per_ax
    fig.set_size_inches(width, height)
    fig.subplots_adjust(wspace=wspace * nfuncs * ncols_per_func / width,
                        hspace=hspace / height_per_ax)

    # Add plots, adjust to tight layout
    _draw_facet_plots(axes, draw_funcs, ncols_per_func,
                      gridrow_col, gridcol_col, nrows)
    fig.canvas.draw()

    # only show one label for aligned axes
    assert axes.shape == (nrows, nfuncs * ncols_per_func)

    if share_xlabel:
        _axes_to_centered_fig_label(
                fig,
                [axes[nrows - 1, ifunc * ncols_per_func + icol]
                 for icol in range(ncols_per_func)
                 for ifunc in range(nfuncs)],
                'x')
    else:
        for ifunc in range(nfuncs):
            _axes_to_centered_fig_label(
                    fig,
                    [axes[nrows - 1, ifunc * ncols_per_func + icol]
                     for icol in range(ncols_per_func)],
                    'x')

    if share_ylabel:
        _axes_to_centered_fig_label(
                fig,
                [axes[irow, ifunc * ncols_per_func]
                 for irow in range(nrows)
                 for ifunc in range(nfuncs)],
                'y')
    else:
        for ifunc in range(nfuncs):
            _axes_to_centered_fig_label(
                    fig,
                    [axes[irow, ifunc * ncols_per_func]
                     for irow in range(nrows)],
                    'y')

    return fig, axes


def _axes_to_centered_fig_label(fig, axlist, axistype):
    """Replace axes labels with one figure label.

    Args:
        `fig` (matplotlib Figure)
            The figure.
        `axlist` (list)
            List of the Axes with the labels to replace.
        `axistype` (str)
            Either 'x' or 'y'.
    """
    if axistype not in ['x', 'y']:
        raise ValueError(f"invalid `axistype` of {axistype}")
    if not len(axlist):
        raise ValueError('empty `axlist`')

    loclists = collections.defaultdict(list)
    label_props = collections.defaultdict(set)
    for ax in axlist:
        axis = getattr(ax, axistype + 'axis')
        label = axis.get_label()
        bbox = label.get_window_extent().transformed(
                transform=fig.transFigure.inverted())
        for loc in ['x0', 'x1', 'y0', 'y1']:
            loclists[loc].append(getattr(bbox, loc))
        label_props['fontproperties'].add(label.get_fontproperties())
        label_props['rotation'].add(label.get_rotation())
        label_props['text'].add(label.get_text())
        label.set_visible(False)

    for propname, propset in list(label_props.items()):
        if len(propset) != 1:
            raise ValueError(f"multiple {propname} among axes: "
                             f"{propset}")
        label_props[propname] = list(propset)[0]

    if axistype == 'x':
        x = (min(loclists['x0']) + max(loclists['x1'])) / 2
        y = (min(loclists['y0']) + min(loclists['y1'])) / 2
    elif axistype == 'y':
        x = (min(loclists['x0']) + min(loclists['x1'])) / 2
        y = (min(loclists['y0']) + max(loclists['y1'])) / 2
    fig.text(x, y, label_props['text'],
             ha='center', va='center',
             rotation=label_props['rotation'],
             fontproperties=label_props['fontproperties'])


def _draw_facet_plots(axes, draw_funcs, ncols_per_func,
                      gridrow_col, gridcol_col, nrows):
    """Helper function draws plots on axes for :func:`facet_plots`."""
    for ifunc, func_d in enumerate(draw_funcs.values()):

        groups = [(row_name, row_data) for row_name, row_data in
                  func_d['data'].groupby(gridrow_col) if len(row_data)]
        assert len(groups) == nrows

        for irow, (row_name, row_data) in enumerate(groups):

            assert (0 <= irow < nrows), (
                    f"irow out of bound\nirow: {irow}\nnrows: {nrows}\n"
                    f"row_name: {row_name}\nngroups: {len(groups)}")

            row_groups = [(col_name, col_data) for col_name, col_data in
                          row_data.groupby(gridcol_col) if len(col_data)]
            assert len(row_groups) == ncols_per_func

            for icol, (col_name, col_data) in enumerate(row_groups):

                ax = axes[irow, ifunc * ncols_per_func + icol]
                title = (row_name +
                         (' ' if row_name and col_name else '') +
                         col_name +
                         (' ' if func_d['titlesuffix'] else '') +
                         func_d['titlesuffix']
                         )
                func_d['func'](
                        col_data,
                        ax=ax,
                        title=title,
                        **func_d['kwargs'])
                if irow != nrows - 1:
                    ax.set_xlabel('')
                    ax.set_xticklabels([])
                if icol != 0:
                    ax.set_ylabel('')
                    ax.set_yticklabels([])


if __name__ == '__main__':
    import doctest
    doctest.testmod()

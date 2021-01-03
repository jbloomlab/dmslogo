"""
============
colorschemes
============

Color schemes.
"""


import matplotlib.colors
import matplotlib.pyplot as plt

import numpy


#: color-blind safe palette with gray, from
#: http://bconnelly.net/2013/10/creating-colorblind-friendly-figures
CBPALETTE = ['#999999', '#E69F00', '#56B4E9', '#009E73',
             '#F0E442', '#0072B2', '#D55E00', '#CC79A7']

#:  color-blind safe palette with black, from
#: http://bconnelly.net/2013/10/creating-colorblind-friendly-figures
CBBPALETTE = ['#000000', '#E69F00', '#56B4E9', '#009E73',
              '#F0E442', '#0072B2', '#D55E00', '#CC79A7']

#: color amino acids by functional group
AA_FUNCTIONAL_GROUP = {'G': '#f76ab4',
                       'A': '#f76ab4',
                       'S': '#ff7f00',
                       'T': '#ff7f00',
                       'C': '#ff7f00',
                       'V': '#12ab0d',
                       'L': '#12ab0d',
                       'I': '#12ab0d',
                       'M': '#12ab0d',
                       'P': '#12ab0d',
                       'F': '#84380b',
                       'Y': '#84380b',
                       'W': '#84380b',
                       'D': '#e41a1c',
                       'E': '#e41a1c',
                       'H': '#3c58e5',
                       'K': '#3c58e5',
                       'R': '#3c58e5',
                       'N': '#972aa8',
                       'Q': '#972aa8'
                       }

#: color amino acids by charge
AA_CHARGE = {'A': '#000000',
             'R': '#FF0000',
             'N': '#000000',
             'D': '#0000FF',
             'C': '#000000',
             'Q': '#000000',
             'E': '#0000FF',
             'G': '#000000',
             'H': '#FF0000',
             'I': '#000000',
             'L': '#000000',
             'K': '#FF0000',
             'M': '#000000',
             'F': '#000000',
             'P': '#000000',
             'S': '#000000',
             'T': '#000000',
             'W': '#000000',
             'Y': '#000000',
             'V': '#000000'
             }


class ValueToColorMap:
    """Map numerical values to color gradient.

    Args:
        `minvalue` (float)
            Color map starts at this value.
        `maxvalue` (float)
            Color map ends at this value.
        `cmap` (str or matplotlib.colors.Colormap)
            Name of `matplotlib colormap`_, or an actual `Colormap` object. You
            can also use the wider set of color maps from palettable_, such as
            by providing `palettable.cmocean.sequential.Dense_20.mpl_colormap`.

    Attributes:
        `cmap` (matplotlib.colors.Colormap)
            Color map.
        `minvalue` (float)
            Color map starts at this value.
        `maxvalue` (float)
            Color map ends at this value.

    Make a data frame with some values, and two color maps (one with default
    'viridis' and another with 'cividis') covering value range in data frame:

    .. plot::
       :context:

        >>> import pandas as pd
        >>> from dmslogo.colorschemes import ValueToColorMap
        >>>
        >>> df = pd.DataFrame({'value': [0, 1, 2, 1, 3, 0]})
        >>> map1 = ValueToColorMap(df['value'].min(),
        ...                        df['value'].max())
        >>> map2 = ValueToColorMap(df['value'].min(),
        ...                        df['value'].max(),
        ...                        cmap='cividis')

    Map values to colors using :meth:`ValueToColorMap.val_to_color`:

    .. plot::
       :context:

        >>> df = (df
        ...       .assign(color=lambda x: x['value'].map(map1.val_to_color),
        ...               color2=lambda x: x['value'].map(map2.val_to_color),
        ...               )
        ...       )
        >>> df
           value    color   color2
        0      0  #440154  #00224d
        1      1  #30678d  #575d6d
        2      2  #35b778  #a59b73
        3      1  #30678d  #575d6d
        4      3  #fde724  #fde737
        5      0  #440154  #00224d

    Draw scale bars:

    .. plot::
       :context: close-figs

       >>> fig1, ax1 = map1.scale_bar(orientation='horizontal',
       ...                          label='viridis scale')

    .. plot::
       :context: close-figs

       >>> fig2, ax2 = map2.scale_bar(orientation='vertical',
       ...                          label='cividis scale')

    .. plot::
       :context: close-figs

       >>> fig2, ax2 = map2.scale_bar(orientation='vertical',
       ...                          label='cividis scale (alpha 0.3)',
       ...                          alpha=0.3)

    .. _matplotlib colormap:
        https://matplotlib.org/tutorials/colors/colormaps.html
    .. _palettable: https://jiffyclub.github.io/palettable/

    """

    def __init__(self,
                 minvalue,
                 maxvalue,
                 cmap='viridis',
                 ):
        """See main class docstring."""
        if isinstance(cmap, matplotlib.colors.Colormap):
            self.cmap = cmap
        elif cmap in plt.colormaps():
            self.cmap = plt.get_cmap(cmap)
        else:
            raise ValueError(f"`cmap` not `Colormap` or name of one: {cmap}")

        self.minvalue = float(minvalue)
        self.maxvalue = float(maxvalue)
        if self.maxvalue <= self.minvalue:
            raise ValueError('`maxvalue` must exceed `minvalue`')

    def val_to_color(self,
                     values,
                     *,
                     return_color_as='rgb_hex_code',
                     ):
        """Map numerical values between `minvalue` and `maxvalue` to colors.

        Args:
            `values` (number or array-like of numbers)
                Values to map to colors
            `return_color_as` ({'rgb_hex_code', 'rgb_triple'})
                Return color as RGB hex code (e.g., `'#FF0000'`) or triple of
                numbers (e.g., `[255, 0, 0]`).

        Returns:
            Either str or length-3 arrays depending on `return_color_as`.
            If `values` is single value, return single value; otherwise array.

        """
        if isinstance(values, (int, float)):
            single_value = True
            values = numpy.array([values], dtype='float')
        else:
            single_value = False
            values = numpy.array(values, dtype='float')

        if any(values < self.minvalue) or any(values > self.maxvalue):
            raise ValueError('`values` not between `minvalue` and `maxvalue`')
        values = (values - self.minvalue) / (self.maxvalue - self.minvalue)
        assert all(values >= 0) and all(values <= 1)

        colors = self.cmap(values, bytes=True)
        if colors.shape != (len(values), 4):
            raise ValueError('unexpected shape for `colors`, '
                             'is `values` multi-dimensional?')

        if return_color_as == 'rgb_triple':
            colors = colors[:, : 3]
            assert colors.shape == (len(values), 3)
        elif return_color_as == 'rgb_hex_code':
            color_list = []
            for r, g, b, _a in colors:
                assert all(0 <= x < 256 for x in [r, g, b])
                color_list.append(f"#{r:02x}{g:02x}{b:02x}")
            colors = numpy.array(color_list)
        else:
            raise ValueError(f"invalid `return_color_as` {return_color_as}")

        if single_value:
            return colors[0]
        else:
            return colors

    def scale_bar(self,
                  *,
                  orientation='vertical',
                  ax=None,
                  label=None,
                  axisfontscale=1,
                  low_high_ticks_only=False,
                  alpha=1,
                  ):
        """Draw a scale bar for the value-to-color map.

        Args:
            `orientation` ({'horizontal', 'vertical'})
                Direction that scale bar drawn is drawn.
            `ax` (None or matplotlib.axes.Axes)
                If specified, draw scale bar on this axis. Otherwise create
                new axes.
            `label` (None or str)
                Label for scale bar.
            `axisfontscale` (float)
                Scale font size by this much.
            `low_high_ticks_only` (bool)
                Rather than showing numerical ticks, indicate low and high.
            `alpha` (float)
                Transparency of scale bar colors.

        Returns:
            `(matplotlib.figure.Figure, matplotlib.axes.Axes)`,
            figure and axis on which the color bar is drawn.

        """
        colors = self.val_to_color(
                    numpy.linspace(self.minvalue, self.maxvalue, 256),
                    return_color_as='rgb_triple')
        if orientation == 'vertical':
            colors = numpy.expand_dims(colors, 1)
            extent = [0, 1, self.minvalue, self.maxvalue]
            figsize = (0.4, 3.5)
        elif orientation == 'horizontal':
            colors = numpy.expand_dims(colors, 0)
            extent = [self.minvalue, self.maxvalue, 0, 1]
            figsize = (3.5, 0.4)
        else:
            raise ValueError(f"invalid `orientation` of {orientation}")

        if ax is None:
            _, ax = plt.subplots(figsize=figsize)

        ax.imshow(colors,
                  aspect='auto',
                  extent=extent,
                  origin='lower',
                  alpha=alpha,
                  )

        if label:
            if orientation == 'vertical':
                ax.set_ylabel(label, fontsize=17 * axisfontscale)
            elif orientation == 'horizontal':
                ax.set_xlabel(label, fontsize=17 * axisfontscale)

        if low_high_ticks_only:
            ax.tick_params('both',
                           top=False,
                           bottom=False,
                           left=False,
                           right=False,
                           labelbottom=(orientation == 'horizontal'),
                           labelleft=(orientation == 'vertical'),
                           )
            axtype = {'vertical': 'y', 'horizontal': 'x'}[orientation]
            axis = getattr(ax, axtype + 'axis')
            dtick = (self.maxvalue - self.minvalue) * 0.1
            axis.set_ticks([self.minvalue + dtick, self.maxvalue - dtick])
            axis.set_ticklabels(
                    ['low', 'high'],
                    rotation=orientation,
                    verticalalignment={'vertical': 'center',
                                       'horizontal': 'top'}[orientation],
                    )
            ax.tick_params(axis=axtype, labelsize=12 * axisfontscale)
        else:
            ax.tick_params(axis='both', labelsize=12 * axisfontscale)
            ax.tick_params(axis={'vertical': 'x',
                                 'horizontal': 'y'}[orientation],
                           left=False,
                           right=False,
                           bottom=False,
                           top=False,
                           labelbottom=False,
                           labelleft=False,
                           )

        return ax.get_figure(), ax


if __name__ == '__main__':
    import doctest
    doctest.testmod()

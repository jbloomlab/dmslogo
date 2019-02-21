"""
============
colorschemes
============

Color schemes.
"""

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


if __name__ == '__main__':
    import doctest
    doctest.testmod()

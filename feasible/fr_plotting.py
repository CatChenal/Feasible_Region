"""
Module `fr_plotting` contains functions used to \
obtain a plot of the feasible region of a linear \
programming problem given the constraints.

Version: beta
Needs further testing as of 2020, September
"""

__all__ = ['despine', 'plot_feasible_region_2D']

import numpy as np
import matplotlib.pyplot as plt

from functools import reduce


def despine(which=['top','right']):
    '''
    which ([str])): 'left','top','right','bottom'.
    '''
    ax = plt.gca()
    for side in which:
        ax.spines[side].set_visible(False)
    return ax


def get_fill_hi_lo_yseries(constraints, y_ser_k):
    """
    Return the bounding y_series for use in ax.fillbetween().
    Uses id str of the 'higer' and 'lower' y-series as
    a tuple:  (['i','j' [, ]], ['k','l'[, ]]), where the first
    item is a list of the 'higher' lines ids and the second is 
    that of the lower ones.
    
    Need testing: may not work in certain cases.
    """
    n_ks = len(y_ser_k)
    n_mid = int(np.floor(n_ks/2))

    max0 = [(k, constraints[k][0].max()) for k in y_ser_k]
    maxima = sorted(max0, 
                    key=lambda max0: max0[1],reverse=True)

    ids_hi = [i for (i,_) in maxima[:n_mid]]
    ids_lo = [i for (i,_) in maxima[n_mid:]]

    y_top = reduce(np.minimum,
                   [constraints[F'{k}'][0] for k in ids_hi])
    y_bot = reduce(np.maximum,
                   [constraints[F'{k}'][0] for k in ids_lo])
    return y_top, y_bot


def plot_feasible_region_2D(ax, x, constraints, 
                            ax_props=None,
                            color_cycle='tab10'):
    """
    Plot the 2D feasible region given the a constraints of
    a linear optimization problem.

    :Note 1: The constraints are assumed to be sufficient, 
             e.g. not co-linear. Using this function prior to 
             using a solver can visualize redundant constraints.
    :Parameters:
    ax: pyplot axis
    x: iterable, domain (x axis)
    constraints: dict of constraints in canonical form.
    ax_props: dict of axis properties, e.g.: xlim, title, etc.
    color_cycle: name of color map.
    
    :Note: `constraints` must abide by the following notation
           convention: 
      1. values = (<series>, <series label>)
      2. keys: can be 'x_i' or 'y_i', where i is an integer
      3. i can be 0: when user wants to show the '0 lines'.
      4. 'x_0' or 'y_0' are excluded during the determination
         of the feasible region.
      
    :Example for constraints dict:
    constraints = dict(x_0=(x*0, r'$x0: x>0$'),
                       y_1=(x*0+2, r'$y1: y\geq2$'),
                       y_2=((25-x)/2.0, r'$y2: 2y\leq25-x$'),
                       y_3=((2*x-8)/4.0,r'$y3: 4y\geq 2x - 8$')
                       #y_4=(x*0+4, r'$y4: y\geq4$') # colinear case
                       )
                   
    Needs further testing.
    """
    if color_cycle is not None:
        ax.set_prop_cycle('color', 
                          plt.cm.get_cmap(color_cycle).colors)
    
    if ax_props is not None:
        xlim = ax_props.get('xlim', None)
        ylim = ax_props.get('ylim', None)
        if xlim is not None:
            ax_props['xlim'] = (xlim[0] - 0.04, xlim[1])
        if ylim is not None:
            ax_props['ylim'] = (ylim[0] - 0.04, ylim[1])
        ax.set(**ax_props)
        
    # Plot the constraints lines:
    ks = list(constraints.keys())
    for k, v in constraints.items():
        lbl = v[1]
        # Special boundaries:'zero lines'
        if k in ['x_0', 'y_0']:
            if k == 'x_0':
                l1 = ax.get_ylim()[1]
                l0 = np.arange(0, l1)
                lims = (np.zeros_like(l0), l0)
            elif k == 'y_0':
                l1 = ax.get_xlim()[1]
                l0 = np.arange(0, l1)
                lims = (l0, np.zeros_like(l0))
                
            ax.plot(lims[0], lims[1], 'k--', label=lbl)
            ks.pop(ks.index(k))    
        else:
            ax.plot(x, v[0], label=lbl)

    # Fill feasible region
    y_top, y_bot = get_fill_hi_lo_yseries(constraints, ks)
    ax.fill_between(x, y_top, y_bot, where=y_top>y_bot,
                    color='grey', alpha=0.2,
                   label='Feasible')

    # Tidy up
    despine()
    # Offset spines outward by 10 points
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_position(('outward', 10))

    ax.legend(title='Constraints',
              bbox_to_anchor=(1.05, 1),
              loc=2, borderaxespad=0.)
    plt.tight_layout()
    
    return ax
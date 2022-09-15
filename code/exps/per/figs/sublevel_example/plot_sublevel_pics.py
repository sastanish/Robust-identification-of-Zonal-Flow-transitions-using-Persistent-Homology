import numpy as np
import gudhi as gd
import matplotlib.pyplot as plt
import xarray as xr

from math import isfinite
import numpy as np
from functools import lru_cache

from gudhi.reader_utils import read_persistence_intervals_in_dimension
from gudhi.reader_utils import read_persistence_intervals_grouped_by_dimension

__author__ = "Vincent Rouvreau, Bertrand Michel, Theo Lacombe"
__copyright__ = "Copyright (C) 2016 Inria"
__license__ = "MIT"

_gudhi_matplotlib_use_tex = True

def __min_birth_max_death(persistence, band=0.0):
    """This function returns (min_birth, max_death) from the persistence.

    :param persistence: The persistence to plot.
    :type persistence: list of tuples(dimension, tuple(birth, death)).
    :param band: band
    :type band: float.
    :returns: (float, float) -- (min_birth, max_death).
    """
    # Look for minimum birth date and maximum death date for plot optimisation
    max_death = 0
    min_birth = persistence[0][1][0]
    for interval in reversed(persistence):
        if float(interval[1][1]) != float("inf"):
            if float(interval[1][1]) > max_death:
                max_death = float(interval[1][1])
        if float(interval[1][0]) > max_death:
            max_death = float(interval[1][0])
        if float(interval[1][0]) < min_birth:
            min_birth = float(interval[1][0])
    if band > 0.0:
        max_death += band
    return (min_birth, max_death)


def _array_handler(a):
    '''
    :param a: if array, assumes it is a (n x 2) np.array and return a
                persistence-compatible list (padding with 0), so that the
                plot can be performed seamlessly.
    '''
    if isinstance(a[0][1], np.float64) or isinstance(a[0][1], float):
        return [[0, x] for x in a]
    else:
        return a

@lru_cache(maxsize=1)
def _matplotlib_can_use_tex():
    """This function returns True if matplotlib can deal with LaTeX, False otherwise.
    The returned value is cached.
    """
    try:
        from matplotlib import checkdep_usetex
        return checkdep_usetex(True)
    except ImportError:
        print("This function is not available, you may be missing matplotlib.")

def plot_persistence_diagram(
    persistence=[],
    persistence_file="",
    alpha=0.6,
    band=0.0,
    max_intervals=1000,
    max_plots=1000,
    inf_delta=0.1,
    legend=False,
    colormap=None,
    axes=None,
    fontsize=16,
    greyblock=True
):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib import rc
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

        if persistence_file != "":
            if path.isfile(persistence_file):
                # Reset persistence
                persistence = []
                diag = read_persistence_intervals_grouped_by_dimension(
                    persistence_file=persistence_file
                )
                for key in diag.keys():
                    for persistence_interval in diag[key]:
                        persistence.append((key, persistence_interval))
            else:
                print("file " + persistence_file + " not found.")
                return None

        persistence = _array_handler(persistence)

        if max_plots != 1000:
            print("Deprecated parameter. It has been replaced by max_intervals")
            max_intervals = max_plots

        if max_intervals > 0 and max_intervals < len(persistence):
            # Sort by life time, then takes only the max_intervals elements
            persistence = sorted(
                persistence,
                key=lambda life_time: life_time[1][1] - life_time[1][0],
                reverse=True,
            )[:max_intervals]

        if colormap == None:
            colormap = plt.cm.Set1.colors
        if axes == None:
            fig, axes = plt.subplots(1, 1)

        (min_birth, max_death) = __min_birth_max_death(persistence, band)
        delta = (max_death - min_birth) * inf_delta
        # Replace infinity values with max_death + delta for diagram to be more
        # readable
        infinity = max_death + delta
        axis_end = max_death + delta / 2
        axis_start = min_birth - delta

        # bootstrap band
        if band > 0.0:
            x = np.linspace(axis_start, infinity, 1000)
            axes.fill_between(x, x, x + band, alpha=alpha, facecolor="red")
        # lower diag patch
        if greyblock:
            axes.add_patch(mpatches.Polygon([[axis_start, axis_start], [axis_end, axis_start], [axis_end, axis_end]], fill=True, color='lightgrey'))
        # Draw points in loop
        pts_at_infty = False  # Records presence of pts at infty
        for interval in reversed(persistence):
            if float(interval[1][1]) != float("inf"):
                # Finite death case
                axes.scatter(
                    interval[1][0],
                    interval[1][1],
                    alpha=alpha,
                    color=colormap[interval[0]],
                    marker='x',
                )
            else:
                pts_at_infty = True
                # Infinite death case for diagram to be nicer
                axes.scatter(
                    interval[1][0], infinity, alpha=alpha, marker='x', color=colormap[interval[0]]
                )
        if pts_at_infty:
            # infinity line and text
            axes.plot([axis_start, axis_end], [axis_start, axis_end], linewidth=1.0, color="k")
            axes.plot([axis_start, axis_end], [infinity, infinity], linewidth=1.0, color="k", alpha=alpha)
            # Infinity label
            yt = axes.get_yticks()
            yt = yt[np.where(yt < axis_end)] # to avoid ploting ticklabel higher than infinity
            yt = np.append(yt, infinity)
            ytl = ["%.3f" % e for e in yt]  # to avoid float precision error
            ytl[-1] = r'$+\infty$'
            axes.set_yticks(yt)
            axes.set_yticklabels(ytl)

        if legend:
            dimensions = list(set(item[0] for item in persistence))
            axes.legend(
                handles=[
                    mpatches.Patch(color=colormap[dim], label=str(dim))
                    for dim in dimensions
                ]
            )

        axes.set_xlabel("Birth", fontsize=fontsize)
        axes.set_ylabel("Death", fontsize=fontsize)
        axes.set_title("Persistence diagram", fontsize=fontsize)
        # Ends plot on infinity value and starts a little bit before min_birth
        axes.axis([axis_start, axis_end, axis_start, infinity + delta/2])
        return axes

    except ImportError:
        print("This function is not available, you may be missing matplotlib.")




ds = xr.open_dataset('../../../cut/normed_n_data.nc')
a = 0
t = -1
alpha = ds.coords['alpha'].to_numpy()
pic = ds['n'][a,t,:,0,:].to_numpy()

fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(pic)
plt.savefig(f'full_pic.svg')
plt.close()

(m,M) = (pic.min(),pic.max())
sublevels = [-0.1,0,0.1] #np.linspace(m,M,10)

for level in sublevels:
    fig, ax = plt.subplots(figsize=(2,2))
    ax.imshow(pic<=level,cmap='binary')
    plt.savefig(f'sublevel_{level}.svg')
    plt.close()

fig, ax = plt.subplots(figsize=(10,10))
cc = gd.PeriodicCubicalComplex(top_dimensional_cells=pic,periodic_dimensions=[False,True])
plot_persistence_diagram(cc.persistence(),axes=ax)
plt.savefig('per_dia.svg')



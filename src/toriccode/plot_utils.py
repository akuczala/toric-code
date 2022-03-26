import numpy as np
from matplotlib import pyplot as plt


def ax_kwarg(f):
    def f_ax(*args, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()
        return f(*args, ax=ax, **kwargs)

    return f_ax


@ax_kwarg
def plot_link(link, ax=None):
    points = link.points
    ax.plot([points[0][0], points[1][0]], [points[0][1], points[1][1]])


# todo single dispatch
@ax_kwarg
def plot_links(someone_with_links, ax=None):
    iter_over = someone_with_links if isinstance(someone_with_links, list) else someone_with_links.links
    for link in iter_over:
        plot_link(link, ax=ax)


@ax_kwarg
def plot_bwr(mat, ax=None, colorbar=True, show=True, cmap='bwr', **kwargs):
    vmax = np.max(np.abs(mat))
    out = ax.matshow(mat, vmax=vmax, vmin=-vmax, cmap=cmap, **kwargs)
    if colorbar:
        plt.colorbar(out)
    if show:
        plt.show()
    return out

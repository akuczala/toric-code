from typing import Union, List, Dict, Any

import numpy as np
from matplotlib import pyplot as plt

from toriccode.link import Link


def ax_kwarg(f):
    def f_ax(*args, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()
        return f(*args, ax=ax, **kwargs)

    return f_ax


@ax_kwarg
def plot_link(link, ax=None, **kwargs):
    p0, p1 = link.points
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], **kwargs)


def _map_components(n, x0, x1):
    return (x0, x1) if x0 <= x1 else (x0, x1 + n)


def link_position_periodic(link):
    p0, p1 = link.points
    lengths = link.GridPointClass.lengths

    return np.array([_map_components(length, x0, x1) for length, x0, x1 in zip(lengths, p0, p1)]).T


@ax_kwarg
def plot_link_periodic(link, ax=None, **kwargs):
    ax.plot(*link_position_periodic(link).T, **kwargs)


# todo single dispatch
@ax_kwarg
def plot_links(someone_with_links, plot_link_fn=plot_link, ax=None, **kwargs):
    iter_over = someone_with_links if isinstance(someone_with_links, list) else someone_with_links.links
    for link in iter_over:
        plot_link_fn(link, ax=ax, **kwargs)

@ax_kwarg
def plot_decorated_links(decorated_link_list: List[Link[Dict[str, Any]]], plot_link_fn=plot_link, ax=None, **kwargs):
    for link in decorated_link_list:
        plot_link_fn(link, ax=ax, **dict(**kwargs, **link.operator))

@ax_kwarg
def plot_qubit_basis_vector(qubits, basis_index, ax=None, **kwargs):
    site_basis_index = list(map(int, format(basis_index, f'0{len(qubits)}b')))
    color_map = {0: 'blue', 1: 'red'}
    plot_decorated_links([link.with_new_content({'c': color_map[i]}) for i, link in zip(site_basis_index, qubits)], plot_link_fn=plot_link_periodic, ax=ax, **kwargs)

@ax_kwarg
def plot_bwr(mat, ax=None, colorbar=False, show=False, cmap='bwr', **kwargs):
    vmax = np.max(np.abs(mat))
    out = ax.matshow(mat, vmax=vmax, vmin=-vmax, cmap=cmap, **kwargs)
    if colorbar:
        plt.colorbar(out)
    if show:
        plt.show()
    return out

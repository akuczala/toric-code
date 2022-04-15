from typing import Union, List, Dict, Any

import numpy as np
from matplotlib import pyplot as plt

from toriccode.link import Link
from toriccode.utils import int_to_bit_list, make_site_grid_basis_vector, nearest_bounding_rectangle


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
def plot_qubit_links_basis_vector(qubits, basis_index, ax=None, **kwargs):
    site_basis_index = int_to_bit_list(len(qubits), basis_index)
    color_map = {0: 'blue', 1: 'red'}
    plot_decorated_links([link.with_new_content({'c': color_map[i]}) for i, link in zip(site_basis_index, qubits)],
                         plot_link_fn=plot_link_periodic, ax=ax, **kwargs)


def plot_vec_links(vec, qubits):
    n_nonzero = np.count_nonzero(~np.isclose(vec, 0))
    fig, axes = plt.subplots(1, n_nonzero, figsize=(5 * max(n_nonzero, 10), 5))
    ax_iter = iter(axes.ravel()) if n_nonzero > 1 else iter([axes])
    for i, component in enumerate(vec):
        if not np.isclose(component, 0):
            ax = next(ax_iter)
            plot_qubit_links_basis_vector(qubits, i, ax=ax)
    return fig


def plot_vec_sites(vec, qubits, max_terms:int=32):
    n_nonzero = np.count_nonzero(~np.isclose(vec, 0))
    n_plots = min(1 + n_nonzero, max_terms)
    subplots_shape = nearest_bounding_rectangle(n_plots)
    fig, axes = plt.subplots(*subplots_shape, figsize=(2 * subplots_shape[0], 2 * subplots_shape[1]))
    ax_iter = iter(axes.ravel()) if n_plots > 1 else iter([axes])
    ax = next(ax_iter)
    nonzero_amplitudes = np.array([v for v in vec if not np.isclose(v, 0)])[:n_plots]
    amplitude_grid_shape = nearest_bounding_rectangle(len(nonzero_amplitudes))
    amplitude_grid = np.empty(amplitude_grid_shape).ravel()
    amplitude_grid[:n_plots] = nonzero_amplitudes
    amplitude_grid = amplitude_grid.reshape(amplitude_grid_shape)
    plot_bwr(amplitude_grid, ax=ax)
    for j, (i, component) in enumerate([(i, v) for i, v in enumerate(vec) if not np.isclose(v, 0)][:n_plots - 1]):
        if j < n_plots:
            ax = next(ax_iter)
            plot_bwr(make_site_grid_basis_vector(qubits, i), ax=ax)
            ax.set_title(f"{component:0.3f}")
    return fig

@ax_kwarg
def plot_bwr(mat, ax=None, colorbar=False, show=False, cmap='bwr', **kwargs):
    vmax = np.max(np.abs(mat))
    out = ax.matshow(mat, vmax=vmax, vmin=-vmax, cmap=cmap, **kwargs)
    if colorbar:
        plt.colorbar(out)
    if show:
        plt.show()
    return out

@ax_kwarg
def plot_hamiltonian_scatter(h, max_pts=5000, ax=None, **kwargs):
    i, j = h.nonzero()
    rnd_subset = np.arange(h.count_nonzero())
    np.random.shuffle(rnd_subset)
    rnd_subset = rnd_subset[:max_pts]
    out = ax.scatter(
        **{kw: arr[rnd_subset] for kw, arr in {'x': i, 'y': j, 'c': h.data}.items()},
        cmap='bwr', s=0.5
    )
    ax.set_aspect(1)
    return out
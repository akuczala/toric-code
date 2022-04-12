import itertools
from typing import Dict, List

import scipy.linalg as lin

from toriccode.env import *
from toriccode.plot_utils import *
from toriccode.toric_terms import Star, Plaquette
from toriccode.terms import Term
from toriccode.utils import tensor_product_flatten
from toriccode.operators import Operator, PauliOperator

GRID_POINT_CLASS = make_grid_point_torus(2, 2)


def test_stuff():
    plot_links(Plaquette(GRID_POINT_CLASS.zero))
    plot_links(Star(GRID_POINT_CLASS.new(3, 3)).boxed_operators)
    plt.gca().set_aspect(1)
    plt.show()

    def build_mini_H():
        links = Plaquette(GRID_POINT_CLASS.zero).boxed_operators
        return tensor_product_flatten((link.operator.matrix for link in links))

    h = build_mini_H()
    hamiltonian_plots()


def plot_vec(vec, qubits):
    n_nonzero = np.count_nonzero(~np.isclose(vec, 0))
    fig, axes = plt.subplots(1, n_nonzero, figsize=(5 * max(n_nonzero, 10), 5))
    ax_iter = iter(axes.ravel()) if n_nonzero > 1 else iter([axes])
    for i, component in enumerate(vec):
        if not np.isclose(component, 0):
            ax = next(ax_iter)
            plot_qubit_basis_vector(qubits, i, ax=ax)
    return fig


def hamiltonian_plots(h, qubits):
    plot_bwr(h)
    eigs, vecs = lin.eigh(h)
    plt.plot(eigs, marker='o');
    plt.title('ei(gs')
    plt.show()
    plot_bwr(vecs, show=False);
    plt.title('vecs')
    plt.show()

    for i in (1, 2, 3):
        plot_vec(np.eye(h.shape[0])[i], qubits)
        plt.title(str(qubits[i]))
        plt.show()
        pass
    return
    n_eigvec_terms = np.count_nonzero(~np.isclose(vecs, 0), axis=0)
    small_vec_locations = np.arange(len(eigs), dtype=int)[n_eigvec_terms < 8]
    for loc in small_vec_locations[:5]:
        fig = plot_vec(vecs[:, loc], qubits)
        fig.suptitle(eigs[loc])
        plt.show()


def build_H(qubit_terms: List[List[Operator]]) -> np.ndarray:
    return sum(tensor_product_flatten([op.matrix for op in term]) for term in qubit_terms)  # type: ignore


def test_dependent_types():
    GP3 = make_grid_point_torus([3, 3])
    GP2 = GP = make_grid_point_torus([2, 2])
    gp3 = GP3.zero + GP3.new(4, 2)
    gp2 = GP2.zero
    pass


def get_qubit_operators(term: Term, qubit_to_index_map) -> Dict[int, Operator]:
    # todo assert uniqueness on links in Term somewhere
    return {qubit_to_index_map[link.with_new_content(None)]: link.boxed_value for link in term.boxed_operators}


def identity_pad_operators(n_qubits, qubit_index_operator_map: Dict[int, Operator]) -> Dict[int, Operator]:
    return {
        i: qubit_index_operator_map.get(
            i,
            PauliOperator.I  # type: ignore
        ) for i in range(n_qubits)
    }


def operator_map_to_list(operator_map: Dict[int, Operator]) -> List[Operator]:
    return [operator_map[i] for i in range(len(operator_map))]


def test_stuff2():
    star_terms = [Star(GRID_POINT_CLASS.new(i, j)) for i, j in itertools.product([0, 1], [0, 1])]
    plaquette_terms = [Plaquette(GRID_POINT_CLASS.new(i, j)) for i, j in itertools.product([0, 1], [0, 1])]
    local_terms: List[Term] = plaquette_terms
    qubits: List[Link[None]] = list(set(
        link.with_new_content(None) for term in local_terms for link in term.boxed_operators
    ))
    # for i in range(254,256):
    #     plot_qubit_basis_vector(qubits, i)
    #     plt.show()

    qubit_to_index_map = {qubit: i for i, qubit in enumerate(qubits)}
    qubit_terms = [
        operator_map_to_list(identity_pad_operators(len(qubits), get_qubit_operators(term, qubit_to_index_map)))
        for term in local_terms
    ]

    # plot_kwargs = {
    #     Star: dict(c='red', linestyle='--'),
    #     Plaquette: dict(c='lime', linestyle='dotted')
    # }
    #
    # for term in local_terms:
    #     plot_links(term, plot_link_fn=plot_link_periodic, **plot_kwargs[type(term)])
    # plt.gca().set_aspect(1)
    # plt.show()

    h = build_H(qubit_terms)
    hamiltonian_plots(h, qubits)


test_stuff2()

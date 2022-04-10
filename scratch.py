import itertools
from typing import Dict, List

import scipy.linalg as lin
import numpy as np

from toriccode.env import *
from toriccode.plot_utils import *
from toriccode.toric_terms import Star, Plaquette, Term
from toriccode.utils import tensor_product
from toriccode.operators import Operator, PauliOperator

GRID_POINT_CLASS = make_grid_point_torus(2, 2)


def test_stuff():
    plot_links(Plaquette(GRID_POINT_CLASS.zero))
    plot_links(Star(GRID_POINT_CLASS.new(3, 3)).links)
    plt.gca().set_aspect(1)
    plt.show()

    def build_mini_H():
        links = Plaquette(GRID_POINT_CLASS.zero).links
        return tensor_product((link.operator.matrix for link in links)).reshape(16, 16)

    h = build_mini_H()
    hamiltonian_plots()


def hamiltonian_plots(h):
    plot_bwr(h)
    eigs, vecs = lin.eigh(h)
    plt.plot(eigs, marker='o');
    plt.show()
    plot_bwr(vecs);


def build_H(qubit_terms: List[List[Operator]]) -> np.ndarray:
    tensor_prod: np.ndarray = sum(tensor_product([op.matrix for op in term]) for term in qubit_terms)  # type: ignore
    dim = 2 ** len(qubit_terms[0])
    return tensor_prod.reshape(dim, dim)


def test_dependent_types():
    GP3 = make_grid_point_torus([3, 3])
    GP2 = GP = make_grid_point_torus([2, 2])
    gp3 = GP3.zero + GP3.new(4, 2)
    gp2 = GP2.zero
    pass


def get_qubit_operators(term: Term, qubit_to_index_map) -> Dict[int, Operator]:
    # todo assert uniqueness on links in Term somewhere
    return {qubit_to_index_map[link.with_new_content(None)]: link.operator for link in term.links}


def identity_pad_operators(n_qubits, qubit_index_operator_map: Dict[int, Operator]) -> Dict[int, Operator]:
    return {i: qubit_index_operator_map.get(i, PauliOperator.I) for i in range(n_qubits)}


def operator_map_to_list(operator_map: Dict[int, Operator]) -> List[Operator]:
    return [operator_map[i] for i in range(len(operator_map))]


def test_stuff2():
    local_terms: List[Term] = (
            [Star(GRID_POINT_CLASS.new(i, j)) for i, j in itertools.product([0, 1], [0, 1])]
            + [Plaquette(GRID_POINT_CLASS.new(i, j)) for i, j in itertools.product([0, 1], [0, 1])]
    )
    qubits: List[Link[None]] = list(set(
        link.with_new_content(None) for term in local_terms for link in term.links
    ))
    qubit_to_index_map = {qubit: i for i, qubit in enumerate(qubits)}
    qubit_terms = [
        operator_map_to_list(identity_pad_operators(len(qubits), get_qubit_operators(term, qubit_to_index_map)))
        for term in local_terms
    ]

    plot_kwargs = {
        Star: dict(c='red', linestyle='--'),
        Plaquette: dict(c='lime', linestyle='dotted')
    }

    for term in local_terms:
        plot_links(term, plot_link_fn=plot_link_periodic, **plot_kwargs[type(term)])
    plt.gca().set_aspect(1)
    plt.show()

    h = build_H(qubit_terms)
    hamiltonian_plots(h)


test_stuff2()

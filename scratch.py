import itertools
from typing import Dict, List

import scipy.linalg as lin

from toriccode.env import *
from toriccode.plot_utils import *
from toriccode.toric_terms import Star, Plaquette
from toriccode.utils import *

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
    plot_bwr(eigs.reshape(1, -1))
    plot_bwr(vecs);


def build_H(qubit_terms: Dict[Link[None], List[Link[Operator]]]):
    pass
    # todo build hamiltonian from qubits and terms
    # return sum(
    #     tensor_product(
    #
    #     for qubit, term_link in qubit_terms.items())
    # )


def test_dependent_types():
    GP3 = make_grid_point_torus([3, 3])
    GP2 = GP = make_grid_point_torus([2, 2])
    gp3 = GP3.zero + GP3.new(4, 2)
    gp2 = GP2.zero
    pass


def test_stuff2():
    local_terms = (
            [Star(GRID_POINT_CLASS.new(i, j)) for i, j in itertools.product([0, 1], [0, 1])]
            + [Plaquette(GRID_POINT_CLASS.new(i, j)) for i, j in itertools.product([0, 1], [0, 1])]
    )
    qubits: List[Link[None]] = list(set(
        Link.new(link.p0, link.direction, None) for term in local_terms for link in term.links
    ))
    qubit_terms = {
        qubit: [link for term in local_terms for link in term.links if link.same_link_position(qubit)]
        for qubit in qubits
    }
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

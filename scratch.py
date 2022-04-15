from typing import List

import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as lin
import scipy.sparse.linalg as slin
from scipy.sparse import coo_array

from toriccode.build_hamiltonian import HamiltonianBuilder
from toriccode.env import *
from toriccode.ising_terms import SiteTerm, Site, IsingBond
from toriccode.plot_utils import *
from toriccode.toric_terms import Star, Plaquette
from toriccode.terms import Term
from toriccode.utils import make_site_grid_basis_vector


def test_stuff():
    grid_point_class = make_grid_point_torus(2, 2)
    plot_links(Plaquette(grid_point_class.zero))
    plot_links(Star(grid_point_class.new(3, 3)).boxed_operators)
    plt.gca().set_aspect(1)
    plt.show()


def calc_eigs(h, n_eigs=3, max_dense=1000):
    eigs, vecs = lin.eigh(h.toarray()) if  h.shape[0] < max_dense else slin.eigsh(h.tocsc(), n_eigs)
    return (lambda argsort: (eigs[argsort], vecs[:, argsort]))(np.argsort(eigs))


def hamiltonian_plots(h: coo_array, qubits, n_eigs=3):
    fig, axes = plt.subplots(1, 3, figsize=(8, 4))
    axes = axes.ravel()
    plot_hamiltonian_matrix(h, axes[0])

    eigs, vecs = calc_eigs(h, n_eigs)

    axes[1].plot(eigs, marker='o')
    axes[1].set_title('eigs')
    closest_sqrt_dim = 2 ** np.round(np.log2(vecs.shape[0] * vecs.shape[1]) / 2).astype(int)
    print(vecs.reshape(closest_sqrt_dim, -1).shape)
    plot_bwr(vecs.reshape(closest_sqrt_dim, -1), ax=axes[2]);
    axes[2].set_aspect(1)
    # axes[2].set_title('vecs')
    plt.show()

    # for i in (1, 2, 3):
    #     plot_vec_links(np.eye(h.shape[0])[i], qubits)
    #     plt.title(str(qubits[i]))
    #     plt.show()
    #     pass
    # return
    # n_eigvec_terms = np.count_nonzero(~np.isclose(vecs, 0), axis=0)
    # print(min(n_eigvec_terms))
    # small_vec_locations = np.arange(len(eigs), dtype=int)[n_eigvec_terms < 8]
    # for loc in small_vec_locations[:5]:
    #     fig = plot_vec_links(vecs[:, loc], qubits)
    #     fig.suptitle(eigs[loc])
    #     plt.show()


def test_dependent_types():
    GP3 = make_grid_point_torus([3, 3])
    GP2 = GP = make_grid_point_torus([2, 2])
    gp3 = GP3.zero + GP3.new(4, 2)
    gp2 = GP2.zero
    pass


def get_toric_terms(n) -> List[Term]:  # hilbert space has dimension 2^(2 n^2) #be careful with PBC

    grid_point_class = make_grid_point_torus(n, n)
    star_terms = [Star.new(grid_point_class.new(i, j)) for i, j in itertools.product(range(n), range(n))]
    plaquette_terms = [Plaquette.new(grid_point_class.new(i, j)) for i, j in itertools.product(range(n), range(n))]
    return star_terms


def get_ising_terms(n) -> Tuple[List[Term], List[float]]:  # hilbert space has dimension 2^(n^2)
    grid_point_class = make_grid_point_torus(n, n)
    site_terms = [SiteTerm(Site[Operator].new(point, PauliOperator.X)) for point in
                  grid_point_class.get_site_iterator()]
    # there is some bond doubling here perhaps due to PBC
    bond_terms = [
        IsingBond(site_pair=(
            Site[Operator].new(pos=point, operator=PauliOperator.X),
            Site[Operator].new(pos=point + dp, operator=PauliOperator.X),
        ))
        for point in grid_point_class.get_site_iterator()
        for dp in (grid_point_class.unit(dir_) for dir_ in (Direction.HORIZONTAL, Direction.VERTICAL))
    ]
    #return bond_terms + site_terms, ([-1.0] * len(bond_terms)) + ([1.0] * len(site_terms))
    return bond_terms, ([-1.0] * len(bond_terms))


def test_stuff2(n_eig_plots):
    print("Building local terms")
    local_terms, coefs = get_ising_terms(3)

    # plot_kwargs = {
    #     Star: dict(c='red', linestyle='--'),
    #     Plaquette: dict(c='lime', linestyle='dotted')
    # }
    #
    # for term in local_terms:
    #     plot_links(term, plot_link_fn=plot_link_periodic, **plot_kwargs[type(term)])
    # plt.gca().set_aspect(1)
    # plt.show()
    h = HamiltonianBuilder(verbose=False).build_matrix(local_terms, coefs)

    qubits = Term.get_qubits(local_terms)
    hamiltonian_plots(h, Term.get_qubits(local_terms), n_eigs=50)
    eigs, vecs = calc_eigs(h, 1000)
    eigs, vecs = (lambda argsort: (eigs[argsort], vecs[:, argsort]))(np.argsort(eigs))
    for i in range(n_eig_plots):
        fig = plot_vec_sites(vecs[:, i], qubits, max_terms=64)
        #fig.suptitle(f"{eigs[i]:0.3f}")
        fig.axes[0].set_title(f"{eigs[i]:0.3f}")
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    test_stuff2(2)
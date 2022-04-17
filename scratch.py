from typing import List

import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as lin
import scipy.sparse.linalg as slin
from scipy.sparse import coo_array

from toriccode.build_hamiltonian import HamiltonianBuilder
from toriccode.env import *
from toriccode.hamiltonian import Hamiltonian
from toriccode.plot_utils import *
from toriccode.toric_terms import Star, Plaquette

def test_stuff():
    grid_point_class = make_grid_point_torus(2, 2)
    plot_links(Plaquette.new(grid_point_class.zero))
    plot_links(Star.new(grid_point_class.new(3, 3)).boxed_operators)
    plt.gca().set_aspect(1)
    plt.show()

def hamiltonian_plots(h: Hamiltonian, n_eigs=3):
    fig, axes = plt.subplots(1, 3, figsize=(8, 4))
    axes = axes.ravel()
    plot_hamiltonian_matrix(h.matrix, ax=axes[0])

    eigs, vecs = h.calc_eigs(n_eigs)

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
    GP3 = make_grid_point_torus(3, 3)
    GP2 = GP = make_grid_point_torus(2, 2)
    gp3 = GP3.zero + GP3.new(4, 2)
    gp2 = GP2.zero
    pass

def test_stuff2(n_eig_plots):
    print("Building local terms")
    local_terms, coefs = get_ising_terms(3, 1.0)

    h = HamiltonianBuilder(verbose=False).build(local_terms, coefs)

    hamiltonian_plots(h, n_eigs=50)
    eigs, vecs = h.calc_eigs(h, 1000)
    eigs, vecs = (lambda argsort: (eigs[argsort], vecs[:, argsort]))(np.argsort(eigs))
    for i in range(n_eig_plots):
        fig1, fig2 = plot_vec(vecs[:, i], h.qubits, max_terms=64)
        #fig.suptitle(f"{eigs[i]:0.3f}")
        fig2.axes[0].set_title(f"{eigs[i]:0.3f}")
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    test_stuff2(2)
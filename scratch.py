import scipy.linalg as lin
import scipy.sparse.linalg as slin

from toriccode.build_hamiltonian import HamiltonianBuilder
from toriccode.env import *
from toriccode.ising_terms import SiteTerm, Site, IsingBond
from toriccode.plot_utils import *
from toriccode.toric_terms import Star, Plaquette
from toriccode.terms import Term


def test_stuff():
    grid_point_class = make_grid_point_torus(2, 2)
    plot_links(Plaquette(grid_point_class.zero))
    plot_links(Star(grid_point_class.new(3, 3)).boxed_operators)
    plt.gca().set_aspect(1)
    plt.show()


def plot_vec(vec, qubits):
    n_nonzero = np.count_nonzero(~np.isclose(vec, 0))
    fig, axes = plt.subplots(1, n_nonzero, figsize=(5 * max(n_nonzero, 10), 5))
    ax_iter = iter(axes.ravel()) if n_nonzero > 1 else iter([axes])
    for i, component in enumerate(vec):
        if not np.isclose(component, 0):
            ax = next(ax_iter)
            plot_qubit_basis_vector(qubits, i, ax=ax)
    return fig


def hamiltonian_plots(h, qubits, n_eigs=3):
    fig, axes = plt.subplots(1,3, figsize=(8,4))
    axes = axes.ravel()
    #plot_bwr(h.toarray(), ax = axes[0])
    print("computing eigs")
    eigs, vecs = slin.eigsh(h, n_eigs)
    axes[1].plot(eigs, marker='o')
    axes[1].set_title('eigs')
    closest_sqrt_dim = 2 ** np.round(np.log2(vecs.shape[0] * vecs.shape[1]) / 2).astype(int)
    print(vecs.reshape(closest_sqrt_dim, -1).shape)
    plot_bwr(vecs.reshape(closest_sqrt_dim, -1), ax=axes[2]);
    axes[2].set_aspect(1)
    #axes[2].set_title('vecs')
    plt.show()

    # for i in (1, 2, 3):
    #     plot_vec(np.eye(h.shape[0])[i], qubits)
    #     plt.title(str(qubits[i]))
    #     plt.show()
    #     pass
    # return
    # n_eigvec_terms = np.count_nonzero(~np.isclose(vecs, 0), axis=0)
    # small_vec_locations = np.arange(len(eigs), dtype=int)[n_eigvec_terms < 8]
    # for loc in small_vec_locations[:5]:
    #     fig = plot_vec(vecs[:, loc], qubits)
    #     fig.suptitle(eigs[loc])
    #     plt.show()


def test_dependent_types():
    GP3 = make_grid_point_torus([3, 3])
    GP2 = GP = make_grid_point_torus([2, 2])
    gp3 = GP3.zero + GP3.new(4, 2)
    gp2 = GP2.zero
    pass


def get_toric_terms(n):  # hilbert space has dimension 2^(n^2)? #be careful with PBC

    grid_point_class = make_grid_point_torus(n, n)
    star_terms = [Star.new(grid_point_class.new(i, j)) for i, j in itertools.product(range(n), range(n))]
    plaquette_terms = [Plaquette.new(grid_point_class.new(i, j)) for i, j in itertools.product(range(n), range(n))]
    return plaquette_terms  # excluding star for now


def get_ising_terms(n):  # hilbert space has dimension 2^(n^2)
    grid_point_class = make_grid_point_torus(n, n)
    site_terms = [SiteTerm(Site[Operator].new(point, PauliOperator.X)) for point in
                  grid_point_class.get_site_iterator()]
    bond_terms = [
        IsingBond(site_pair=(
            Site[Operator].new(pos=point, operator=PauliOperator.Z),
            Site[Operator].new(pos=point + dp, operator=PauliOperator.Z),
        ))
        for point in grid_point_class.get_site_iterator()
        for dp in (grid_point_class.unit(dir_) for dir_ in (Direction.HORIZONTAL, Direction.VERTICAL))
    ]
    return bond_terms


def test_stuff2():
    print("Building local terms")
    local_terms = get_ising_terms(3)

    # plot_kwargs = {
    #     Star: dict(c='red', linestyle='--'),
    #     Plaquette: dict(c='lime', linestyle='dotted')
    # }
    #
    # for term in local_terms:
    #     plot_links(term, plot_link_fn=plot_link_periodic, **plot_kwargs[type(term)])
    # plt.gca().set_aspect(1)
    # plt.show()

    h = HamiltonianBuilder().build_matrix(local_terms)
    print("converting")
    h = h.tocsr()
    hamiltonian_plots(h, Term.get_qubits(local_terms))


test_stuff2()

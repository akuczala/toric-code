import scipy.linalg as lin

from toriccode.build_hamiltonian import HamiltonianBuilder
from toriccode.env import *
from toriccode.ising_terms import SiteTerm, Site
from toriccode.plot_utils import *
from toriccode.toric_terms import Star, Plaquette
from toriccode.terms import Term

GRID_POINT_CLASS = make_grid_point_torus(2, 2)


def test_stuff():
    plot_links(Plaquette(GRID_POINT_CLASS.zero))
    plot_links(Star(GRID_POINT_CLASS.new(3, 3)).boxed_operators)
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


def hamiltonian_plots(h, qubits):
    plot_bwr(h)
    eigs, vecs = lin.eigh(h)
    plt.plot(eigs, marker='o');
    plt.title('ei(gs')
    plt.show()
    plot_bwr(vecs, show=False);
    plt.title('vecs')
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

    grid_point_class = make_grid_point_torus(2, 2)
    star_terms = [Star.new(grid_point_class.new(i, j)) for i, j in itertools.product(range(n), range(n))]
    plaquette_terms = [Plaquette.new(grid_point_class.new(i, j)) for i, j in itertools.product(range(n), range(n))]
    return plaquette_terms  # excluding star for now


def get_ising_terms(n):  # hilbert space has dimension 2^(n^2)
    grid_point_class = make_grid_point_torus(n, n)
    site_terms = [SiteTerm(Site[Operator].new(grid_point_class.new(i, j), PauliOperator.Z)) for i, j in
                  itertools.product(range(n), range(n))]
    return site_terms


def test_stuff2():
    local_terms = get_toric_terms(3)

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
    hamiltonian_plots(h, Term.get_qubits(local_terms))


test_stuff2()

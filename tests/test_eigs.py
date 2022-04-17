import numpy as np
from toriccode.env import *


def test_ising_eigs():
    local_terms, coefs = get_ising_terms(3, 0.5)
    h = HamiltonianBuilder(verbose=False).build(local_terms, coefs)
    eigs, vecs = h.calc_eigs()

    first_20_expected_eigs = np.array([
        -18.28162062, -18.28161951, -10.47466519, -10.47166004,
        -10.37744076, -10.37744076, -10.37744076, -10.37744076,
        -10.37674551, -10.37674551, -10.37674551, -10.37674551,
        -10.28104542, -10.28104542, -10.28104542, -10.28104542,
        -10.28094321, -10.28094321, -10.28094321, -10.28094321])

    assert np.isclose(eigs[:20], first_20_expected_eigs).all()


def test_toric():
    local_terms, coefs = get_toric_terms(2)
    h = HamiltonianBuilder(verbose=False).build(local_terms, coefs)
    eigs, vecs = h.calc_eigs()
    assert all(
        np.count_nonzero(np.isclose(eigs[:60], energy)) == degeneracy
        for energy, degeneracy in [(-8.0, 4), (-4.0, 48)]
    )

    grid_point_class = h.local_terms[0].GridPointClass
    B = Plaquette.new(grid_point_class.new(0, 0)).generate_matrix(h.qubits).tocsc()

    # B^2 | gs > = | gs >
    for gs in vecs[:, 4:].T:
        assert np.isclose(B.dot(B.dot(gs)), gs).all()

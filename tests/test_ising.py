from toriccode.env import *


def test_ising_eigs():
    local_terms, coefs = get_ising_terms(3, 0.5)
    coefs = -np.ones(len(local_terms))
    h = HamiltonianBuilder(verbose=False).build(local_terms, coefs)
    eigs, vecs = h.calc_eigs()

    first_20_expected_eigs = np.array(
        [-19.13136681, -19.13086465, -12.03564768, -11.82655433,
         -11.55573353, -11.55573353, -11.55573353, -11.55573353,
         -11.49676525, -11.49676525, -11.49676525, -11.49676525,
         -11.12756972, -11.12756972, -11.12756972, -11.12756972,
         -11.11693861, -11.11693861, -11.11693861, -11.11693861])

    assert np.isclose(eigs[:20], first_20_expected_eigs).all()

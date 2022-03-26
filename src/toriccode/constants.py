import numpy as np


class Pauli:
    Z = np.array([[1, 0], [0, -1]])
    X = np.array([[0, 1], [1, 0]])
    I = np.eye(2)
from matplotlib import pyplot as plt
import scipy.linalg as lin

from toriccode.constants import Pauli
from toriccode.grid_point import GRID_POINT_CLASS
from toriccode.link import Plaquette, Star
from toriccode.plot_utils import plot_links, plot_bwr
from toriccode.utils import tensor_product

plot_links(Plaquette(GRID_POINT_CLASS.zero))
plot_links(Star(GRID_POINT_CLASS.new(3, 3)).links)
plt.gca().set_aspect(1)
plt.show()


def build_mini_H():
    links = Plaquette(GRID_POINT_CLASS.zero).links
    return tensor_product((Pauli.Z for _ in links)).reshape(16, 16)


h = build_mini_H()
plot_bwr(h)
eigs, vecs = lin.eigh(h)
plot_bwr(eigs.reshape(1, -1))
plot_bwr(vecs);

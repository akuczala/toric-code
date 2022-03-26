import scipy.linalg as lin

from toriccode.env import *
from toriccode.plot_utils import *
from toriccode.toric_terms import Star, Plaquette
from toriccode.utils import *

def test_stuff():
    GRID_POINT_CLASS = make_grid_point_torus(2,2)
    plot_links(Plaquette(GRID_POINT_CLASS.zero))
    plot_links(Star(GRID_POINT_CLASS.new(3, 3)).links)
    plt.gca().set_aspect(1)
    plt.show()


    def build_mini_H():
        links = Plaquette(GRID_POINT_CLASS.zero).links
        return tensor_product((link.operator.matrix for link in links)).reshape(16, 16)


    h = build_mini_H()
    plot_bwr(h)
    eigs, vecs = lin.eigh(h)
    plot_bwr(eigs.reshape(1, -1))
    plot_bwr(vecs);

def test_dependent_types():
    GP3 = make_grid_point_torus([3,3])
    GP2 = GP = make_grid_point_torus([2,2])
    gp3 = GP3.zero + GP3.new(4,2)
    gp2 = GP2.zero
    pass

test_stuff()
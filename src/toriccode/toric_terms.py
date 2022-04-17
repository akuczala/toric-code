from dataclasses import dataclass
from typing import List, Tuple

from toriccode.box import HasBox
from toriccode.grid_point import GridPoint, H, V, make_grid_point_torus
from toriccode.link import Link
from toriccode.operators import Operator, PauliOperator
from toriccode.terms import LocalTerm, Term


@dataclass(frozen=True)
class Star(LocalTerm):
    p0: GridPoint  # center site

    @property
    def boxed_operators(self) -> List[HasBox[Operator]]:
        return [
            Link.new(self.p0 + dp, dir, operator=PauliOperator.Z)
            for dp, dir in [
                (self.GridPointClass.zero, H), (self.GridPointClass.zero, V),
                (-self.GridPointClass.unit(H), H), (-self.GridPointClass.unit(V), V)
            ]
        ]


@dataclass(frozen=True)
class Plaquette(LocalTerm):
    p0: GridPoint  # lower-left site

    @property
    def boxed_operators(self) -> List[HasBox[Operator]]:
        return [
            Link.new(self.p0 + dp, dir, operator=PauliOperator.X)
            for dp, dir in [
                (self.GridPointClass.zero, H), (self.GridPointClass.zero, V),
                (self.GridPointClass.unit(H), V), (self.GridPointClass.unit(V), H)
            ]
        ]


def get_star_terms(grid_point_class):
    return [Star.new(pos) for pos in grid_point_class.get_site_iterator()]


def get_plaquette_terms(grid_point_class):
    return [Plaquette.new(pos) for pos in grid_point_class.get_site_iterator()]


def get_toric_terms(n) -> Tuple[List[Term], List[float]]:  # hilbert space has dimension 2^(2 n^2) #be careful with PBC

    grid_point_class = make_grid_point_torus(n, n)
    terms = get_star_terms(grid_point_class) + get_plaquette_terms(grid_point_class)
    coefs = [-1.0] * len(terms)
    return terms, coefs

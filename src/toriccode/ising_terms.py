from dataclasses import dataclass
from typing import List, TypeVar, Tuple

from toriccode.box import HasBox, S
from toriccode.grid_point import GridPoint, ContainsGridPoint, make_grid_point_torus, Direction
from toriccode.operators import Operator, PauliOperator
from toriccode.terms import Term

T = TypeVar("T")


@dataclass(frozen=True)
class Site(ContainsGridPoint, HasBox[T]):
    pos: GridPoint
    operator: T

    @property
    def boxed_value(self) -> T:
        return self.operator

    def with_new_content(self, value: S) -> "HasBox[S]":
        return Site.new(pos=self.pos, operator=value)


@dataclass(frozen=True)
class IsingBond(Term):
    site_pair: Tuple[Site[Operator]]

    @property
    def boxed_operators(self) -> List[HasBox[Operator]]:
        return list(self.site_pair)


@dataclass(frozen=True)
class SiteTerm(Term):
    site: Site[Operator]

    @property
    def boxed_operators(self) -> List[HasBox[Operator]]:
        return [self.site]


def get_site_terms(grid_point_class, operator: Operator):
    return [
        SiteTerm(Site[Operator].new(point, operator)) for point in
        grid_point_class.get_site_iterator()
    ]


def get_bond_terms(grid_point_class, operator: Operator):
    return [
        IsingBond(site_pair=(
            Site[Operator].new(pos=point, operator=operator),
            Site[Operator].new(pos=point + dp, operator=operator),
        ))
        for point in grid_point_class.get_site_iterator()
        for dp in (grid_point_class.unit(dir_) for dir_ in (Direction.HORIZONTAL, Direction.VERTICAL))
    ]


def get_ising_terms(n) -> Tuple[List[Term], List[float]]:  # hilbert space has dimension 2^(n^2)
    grid_point_class = make_grid_point_torus(n, n)
    site_terms = get_site_terms(grid_point_class, PauliOperator.X)
    bond_terms = get_bond_terms(grid_point_class, PauliOperator.Z)
    return bond_terms + site_terms, ([-1.0] * len(bond_terms)) + ([1.0] * len(site_terms))

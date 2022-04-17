from dataclasses import dataclass
from typing import List, TypeVar, Tuple

import numpy as np

from toriccode.box import HasBox
from toriccode.grid_point import GridPoint, ContainsGridPoint, make_grid_point_torus, Direction
from toriccode.operators import Operator, PauliOperator
from toriccode.terms import Term
from toriccode.utils import int_to_bit_list

_T = TypeVar("_T")
_S = TypeVar("_S")


@dataclass(frozen=True)
class Site(ContainsGridPoint, HasBox[_T]):
    pos: GridPoint
    operator: _T

    @property
    def boxed_value(self) -> _T:
        return self.operator

    def with_new_content(self, value: _S) -> "HasBox[_S]":
        return Site.new(pos=self.pos, operator=value)


@dataclass(frozen=True)
class BondTerm(Term):
    site_pair: Tuple[Site[Operator], Site[Operator]]

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
        BondTerm(site_pair=(
            Site[Operator].new(pos=point, operator=operator),
            Site[Operator].new(pos=point + dp, operator=operator),
        ))
        for point in grid_point_class.get_site_iterator()
        for dp in (grid_point_class.unit(dir_) for dir_ in (Direction.HORIZONTAL, Direction.VERTICAL))
    ]


def get_ising_terms(n: int, g: float) -> Tuple[List[Term], List[float]]:  # hilbert space has dimension 2^(n^2)
    grid_point_class = make_grid_point_torus(n, n)
    site_terms = get_site_terms(grid_point_class, PauliOperator.X)
    bond_terms = get_bond_terms(grid_point_class, PauliOperator.Z)
    return bond_terms + site_terms, ([-1.0] * len(bond_terms)) + ([g] * len(site_terms))


def make_site_grid_basis_vector(qubits: List[Site[None]], basis_index: int) -> np.ndarray:
    site_basis_index = int_to_bit_list(len(qubits), basis_index)
    grid_shape = next(iter(qubits.keys())).GridPointClass.lengths
    grid = np.empty(grid_shape)
    for i, qubit in zip(site_basis_index, qubits):
        grid[qubit.pos[0], qubit.pos[1]] = 2 * i - 1
    return grid

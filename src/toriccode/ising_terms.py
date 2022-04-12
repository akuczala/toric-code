from dataclasses import dataclass
from typing import List, TypeVar, Tuple

from toriccode.box import HasBox, S
from toriccode.grid_point import GridPoint, ContainsGridPoint
from toriccode.operators import Operator
from toriccode.terms import LocalTerm, Term

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
class IsingBond(LocalTerm):
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

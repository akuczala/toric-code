from dataclasses import dataclass
from typing import List, TypeVar, Tuple

from toriccode.box import HasBox, S
from toriccode.grid_point import GridPoint, ContainsGridPoint
from toriccode.operators import Operator
from toriccode.terms import LocalTerm

T = TypeVar("T")


@dataclass(frozen=True)
class Site(ContainsGridPoint, HasBox[T]):
    pos: GridPoint
    operator: T

    # todo make common to all ContainsGridPoint
    @classmethod
    def new(cls, pos, operator) -> "Site[T]":
        return cls(GridPointClass=type(pos), pos=pos, operator=operator)

    @property
    def boxed_value(self) -> T:
        return self.operator

    def with_new_content(self, value: S) -> "HasBox[S]":
        return Site.new(pos=self.pos, operator=value)


class IsingBond(LocalTerm):
    site_pair: Tuple[Site[Operator]]

    @property
    def boxed_operators(self) -> List[HasBox[Operator]]:
        return list(self.site_pair)

from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Tuple

from .box import HasBox
from .grid_point import GridPoint, Direction, ContainsGridPoint

T = TypeVar("T")
S = TypeVar("S")


@dataclass(frozen=True)
class Link(ContainsGridPoint, HasBox[T]):
    p0: GridPoint
    direction: Direction
    operator: T

    # todo make common to all ContainsGridPoint
    @classmethod
    def new(cls, p0, direction, operator) -> Link[T]:
        return cls(GridPointClass=type(p0), p0=p0, direction=direction, operator=operator)

    @property
    def boxed_value(self) -> T:
        return self.operator

    @property
    def points(self) -> Tuple[GridPoint, GridPoint]:
        return self.p0, self.p0 + self.GridPointClass.unit(self.direction)

    def same_link_position(self, other: Link[T]) -> bool:
        return self.p0 == other.p0 and self.direction == other.direction

    def with_new_content(self, content: S) -> Link[S]:
        return Link.new(self.p0, self.direction, content)

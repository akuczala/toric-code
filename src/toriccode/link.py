from __future__ import annotations
from dataclasses import dataclass
from typing import Type, TypeVar, Generic, Tuple

from .grid_point import GridPoint, Direction
from .utils import comma_separated_string


@dataclass(frozen=True)
class ContainsGridPoint:
    GridPointClass: Type[GridPoint]

    def __str__(self) -> str:
        arg_str = comma_separated_string((val for name, val in self.__dict__.items() if name != 'GridPointClass'))
        return f"{type(self).__name__}({arg_str})"

    def __repr__(self) -> str:
        return str(self)


T = TypeVar("T")
S = TypeVar("S")


@dataclass(frozen=True)
class Link(ContainsGridPoint, Generic[T]):
    p0: GridPoint
    direction: Direction
    operator: T

    # todo make common to all ContainsGridPoint
    @classmethod
    def new(cls, p0, direction, operator) -> Link[T]:
        return cls(GridPointClass=type(p0), p0=p0, direction=direction, operator=operator)

    @property
    def points(self) -> Tuple[GridPoint, GridPoint]:
        return self.p0, self.p0 + self.GridPointClass.unit(self.direction)

    def same_link_position(self, other: Link[T]) -> bool:
        return self.p0 == other.p0 and self.direction == other.direction

    def with_new_content(self, content: S) -> Link[S]:
        return Link.new(self.p0, self.direction, content)

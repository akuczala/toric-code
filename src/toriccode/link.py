from dataclasses import dataclass
from typing import List, Type

from .grid_point import GridPoint, Direction, H, V
from .utils import PrintDataclassMixin


@dataclass(frozen=True)
class ContainsGridPoint:
    GridPointClass: Type[GridPoint]


@dataclass(frozen=True)
class Link(ContainsGridPoint, PrintDataclassMixin):
    p0: GridPoint
    direction: Direction

    @classmethod
    def new(cls, p0, direction):
        return cls(GridPointClass=type(p0), p0=p0, direction=direction)

    @property
    def points(self):
        return self.p0, self.p0 + self.GridPointClass.unit(self.direction)


@dataclass(frozen=True, init=False)
class Star(ContainsGridPoint, PrintDataclassMixin):
    p0: GridPoint  # center site

    def __init__(self, p0):
        object.__setattr__(self, 'GridPointClass', type(p0))
        object.__setattr__(self, 'p0', p0)

    @classmethod
    def new(cls, p0):
        return cls(GridPointClass=type(p0), p0=p0)

    @property
    def links(self) -> List[Link]:
        return [
            Link.new(self.p0 + dp, dir)
            for dp, dir in [
                (self.GridPointClass.zero, H), (self.GridPointClass.zero, V),
                (-self.GridPointClass.unit(H), H), (-self.GridPointClass.unit(V), V)
            ]
        ]


@dataclass(frozen=True)
class Plaquette(ContainsGridPoint, PrintDataclassMixin):
    p0: GridPoint  # lower-left site

    def __init__(self, p0):
        object.__setattr__(self, 'GridPointClass', type(p0))
        object.__setattr__(self, 'p0', p0)

    @classmethod
    def new(cls, p0):
        return cls(GridPointClass=type(p0), p0=p0)

    @property
    def links(self) -> List[Link]:
        return [
            Link.new(self.p0 + dp, dir)
            for dp, dir in [
                (self.GridPointClass.zero, H), (self.GridPointClass.zero, V),
                (self.GridPointClass.unit(H), V), (self.GridPointClass.unit(V), H)
            ]
        ]

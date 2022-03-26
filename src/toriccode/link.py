from dataclasses import dataclass
from typing import List

from toriccode.grid_point import GRID_POINT_CLASS, GridPoint, Direction, H, V
from toriccode.utils import PrintDataclassMixin


@dataclass(frozen=True)
class Link(PrintDataclassMixin):
    GridPointClass = GRID_POINT_CLASS
    p0: GridPoint
    direction: Direction

    @classmethod
    def new(cls, p0, direction):
        return cls(p0, direction)

    @property
    def points(self):
        return self.p0, self.p0 + self.GridPointClass.unit(self.direction)


@dataclass(frozen=True)
class Star(PrintDataclassMixin):
    GridPointClass = GRID_POINT_CLASS
    p0: GridPoint  # center site

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
class Plaquette(PrintDataclassMixin):
    GridPointClass = GRID_POINT_CLASS
    p0: GridPoint  # lower-left site

    @property
    def links(self) -> List[Link]:
        return [
            Link.new(self.p0 + dp, dir)
            for dp, dir in [
                (self.GridPointClass.zero, H), (self.GridPointClass.zero, V),
                (self.GridPointClass.unit(H), V), (self.GridPointClass.unit(V), H)
            ]
        ]
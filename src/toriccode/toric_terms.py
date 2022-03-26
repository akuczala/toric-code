from dataclasses import dataclass
from typing import List

from toriccode.grid_point import GridPoint, H, V
from toriccode.link import ContainsGridPoint, Link
from toriccode.operators import Operator, PauliOperator


@dataclass(frozen=True, init=False)
class Star(ContainsGridPoint):
    p0: GridPoint  # center site

    # todo make common to all ContainsGridPoint
    def __init__(self, p0):
        object.__setattr__(self, 'GridPointClass', type(p0))
        object.__setattr__(self, 'p0', p0)

    @classmethod
    def new(cls, p0):
        return cls(GridPointClass=type(p0), p0=p0)

    @property
    def links(self) -> List[Link[Operator]]:
        return [
            Link.new(self.p0 + dp, dir, operator=PauliOperator.Z)
            for dp, dir in [
                (self.GridPointClass.zero, H), (self.GridPointClass.zero, V),
                (-self.GridPointClass.unit(H), H), (-self.GridPointClass.unit(V), V)
            ]
        ]


@dataclass(frozen=True)
class Plaquette(ContainsGridPoint):
    p0: GridPoint  # lower-left site

    def __init__(self, p0):
        object.__setattr__(self, 'GridPointClass', type(p0))
        object.__setattr__(self, 'p0', p0)

    @classmethod
    def new(cls, p0):
        return cls(GridPointClass=type(p0), p0=p0)

    @property
    def links(self) -> List[Link[Operator]]:
        return [
            Link.new(self.p0 + dp, dir, operator=PauliOperator.X)
            for dp, dir in [
                (self.GridPointClass.zero, H), (self.GridPointClass.zero, V),
                (self.GridPointClass.unit(H), V), (self.GridPointClass.unit(V), H)
            ]
        ]
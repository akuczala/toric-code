from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Tuple, List, Type, TypeVar
from enum import Enum

from .utils import comma_separated_string


class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

    def __str__(self):
        return {Direction.HORIZONTAL: 'H', Direction.VERTICAL: 'V'}[self]


H = Direction.HORIZONTAL
V = Direction.VERTICAL


@dataclass(frozen=True)  # type: ignore
class GridPoint(ABC):
    p: Tuple[int, ...]

    @classmethod
    def new(cls, *args: int) -> GridPoint:
        return cls(args)

    @classmethod
    @property
    def zero(cls) -> GridPoint:
        return cls.new(0, 0)

    @classmethod
    def unit(cls, direction: Direction) -> GridPoint:
        return {
            Direction.HORIZONTAL: lambda: cls.new(1, 0),
            Direction.VERTICAL: lambda: cls.new(0, 1)
        }[direction]()

    def __iter__(self):
        return iter(self.p)

    def __getitem__(self, i):
        return self.p[i]

    @abstractmethod
    def __add__(self, other) -> GridPoint:
        pass

    def __sub__(self, other) -> GridPoint:
        return self + (-other)

    def __rmul__(self, scalar: float):
        return type(self)(tuple(scalar * x for x in self))

    def __neg__(self) -> GridPoint:
        return (-1) * self

    def __str__(self) -> str:
        return f"{type(self).__name__}({comma_separated_string(self)})"


@dataclass(frozen=True)
class GridPointPlane(GridPoint):
    def __add__(self, other) -> GridPoint:
        return type(self)(tuple(s + o for s, o in zip(self, other)))


class GridPointTorus(GridPoint):
    lengths: List[int] = field(default_factory=list)

    def __add__(self, other) -> GridPoint:
        return type(self)(tuple((s + o) % length for s, o, length in zip(self, other, self.lengths)))


def make_grid_point_torus(*lengths: int) -> GridPointTorus:
    return type(
        f"{GridPointTorus.__name__}" + "".join(str(length) for length in lengths),
        (GridPointTorus,), {'lengths': lengths}
    )  # type: ignore


G = TypeVar('G', bound='ContainsGridPoint')


@dataclass(frozen=True)
class ContainsGridPoint:
    GridPointClass: Type[GridPoint]

    @classmethod
    def new(cls: Type[G], *args, **kwargs) -> G:
        grid_point_class = type(next(filter(
            lambda v: isinstance(v, GridPoint), itertools.chain(args, kwargs.values())
        )))
        return cls(grid_point_class, *args, **kwargs)

    def __str__(self) -> str:
        arg_str = comma_separated_string((val for name, val in self.__dict__.items() if name != 'GridPointClass'))
        return f"{type(self).__name__}({arg_str})"

    def __repr__(self) -> str:
        return str(self)

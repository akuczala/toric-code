from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')
S = TypeVar('S')


@dataclass
class Box(Generic[T]):
    value: T


class HasBox(Generic[T]):
    @property
    @abstractmethod
    def boxed_value(self) -> T:
        pass

    @abstractmethod
    def with_new_content(self, value: S) -> "HasBox[S]":
        pass

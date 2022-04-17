from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

_T = TypeVar('_T')
_S = TypeVar('_S')


@dataclass
class Box(Generic[_T]):
    value: _T


class HasBox(Generic[_T]):
    @property
    @abstractmethod
    def boxed_value(self) -> _T:
        pass

    @abstractmethod
    def with_new_content(self, value: _S) -> "HasBox[_S]":
        pass

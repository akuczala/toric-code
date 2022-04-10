from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from toriccode.link import ContainsGridPoint, Link
from toriccode.operators import Operator


class Term(ContainsGridPoint):

    @property
    @abstractmethod
    def links(self) -> List[Link[Operator]]:
        pass


@dataclass(frozen=True, init=False)
class GenericTerm(Term):
    _links: List[Link[Operator]]

    def __init__(self, links: List[Link[Operator]]):
        object.__setattr__(self, 'GridPointClass', type(p0))
        object.__setattr__(self, '_links', links)

    @property
    def links(self) -> List[Link[Operator]]:
        return self._links
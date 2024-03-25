from abc import ABC
from dataclasses import dataclass, field
from typing import List, Iterable


class ItemSource(ABC):
    ...


@dataclass(frozen=True)
class GameItem:
    name: str
    sources: List[ItemSource] = field(default_factory=list)

    def add_sources(self, sources: Iterable[ItemSource]):
        self.sources.extend(sources)

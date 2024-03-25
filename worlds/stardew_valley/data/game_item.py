import sys
from abc import ABC
from dataclasses import dataclass, field
from typing import List, Iterable

if sys.version_info >= (3, 10):
    source_dataclass_args = {"frozen": True, "kw_only": True}
else:
    source_dataclass_args = {"frozen": True}


@dataclass(**source_dataclass_args)
class ItemSource(ABC):
    ...


@dataclass(frozen=True)
class GameItem:
    name: str
    sources: List[ItemSource] = field(default_factory=list)

    def add_sources(self, sources: Iterable[ItemSource]):
        self.sources.extend(sources)

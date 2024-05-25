import enum
import sys
from abc import ABC
from dataclasses import dataclass, field
from types import MappingProxyType

from typing import List, Iterable, Set, ClassVar, Tuple, Mapping

if sys.version_info >= (3, 10):
    source_dataclass_args = {"frozen": True, "kw_only": True}
else:
    source_dataclass_args = {"frozen": True}

DEFAULT_REQUIREMENT_TAGS = MappingProxyType({})


class ItemTag(enum.Enum):
    CROPSANITY_SEED = enum.auto()
    CROPSANITY = enum.auto()
    FISH = enum.auto()
    FRUIT = enum.auto()
    VEGETABLE = enum.auto()
    EDIBLE_MUSHROOM = enum.auto()


@dataclass(**source_dataclass_args)
class ItemSource(ABC):
    add_tags: ClassVar[Tuple[ItemTag]] = ()

    @property
    def requirement_tags(self) -> Mapping[str, Tuple[ItemTag, ...]]:
        return DEFAULT_REQUIREMENT_TAGS


@dataclass(**source_dataclass_args)
class PermanentSource(ItemSource):
    regions: Tuple[str, ...] = ()
    """No region means it's available everywhere."""


@dataclass(**source_dataclass_args)
class GenericToolSource(ItemSource):
    """A source for something that requires tools, but does not really fit any category. Typically, won't give any xp."""
    regions: Tuple[str, ...]
    tools: Tuple[Tuple[str, str], ...]


@dataclass(**source_dataclass_args)
class CustomRuleSource(ItemSource):
    """A source just to make sure the item is not pruned, since its rule will be implemented directly in logic."""
    ...


@dataclass(frozen=True)
class GameItem:
    name: str
    sources: List[ItemSource] = field(default_factory=list)
    tags: Set[ItemTag] = field(default_factory=set)

    def add_sources(self, sources: Iterable[ItemSource]):
        self.sources.extend(sources)
        self.tags.update(tag for source in sources for tag in source.add_tags)

    def add_tags(self, tags: Iterable[ItemTag]):
        self.tags.update(tags)

    @property
    def has_custom_rule(self):
        return any(isinstance(source, CustomRuleSource) for source in self.sources)

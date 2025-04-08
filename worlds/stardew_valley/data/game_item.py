import enum
import sys
from abc import ABC
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import List, Iterable, Set, ClassVar, Tuple, Mapping, Callable, Any

from ..stardew_rule.protocol import StardewRule

if sys.version_info >= (3, 10):
    kw_only = {"kw_only": True}
else:
    kw_only = {}

DEFAULT_REQUIREMENT_TAGS = MappingProxyType({})


@dataclass(frozen=True)
class Requirement(ABC):
    ...


class ItemTag(enum.Enum):
    CROPSANITY_SEED = enum.auto()
    CROPSANITY = enum.auto()
    FISH = enum.auto()
    FRUIT = enum.auto()
    VEGETABLE = enum.auto()
    EDIBLE_MUSHROOM = enum.auto()
    BOOK = enum.auto()
    BOOK_POWER = enum.auto()
    BOOK_SKILL = enum.auto()


@dataclass(frozen=True)
class ItemSource(ABC):
    add_tags: ClassVar[Tuple[ItemTag]] = ()

    @property
    def requirement_tags(self) -> Mapping[str, Tuple[ItemTag, ...]]:
        return DEFAULT_REQUIREMENT_TAGS

    # FIXME this should just be an optional field, but kw_only requires python 3.10...
    @property
    def other_requirements(self) -> Iterable[Requirement]:
        return ()


@dataclass(frozen=True, **kw_only)
class GenericSource(ItemSource):
    regions: Tuple[str, ...] = ()
    """No region means it's available everywhere."""
    other_requirements: Tuple[Requirement, ...] = ()


@dataclass(frozen=True)
class CustomRuleSource(ItemSource):
    """Hopefully once everything is migrated to sources, we won't need these custom logic anymore."""
    create_rule: Callable[[Any], StardewRule]


@dataclass(frozen=True, **kw_only)
class CompoundSource(ItemSource):
    sources: Tuple[ItemSource, ...] = ()


class Tag(ItemSource):
    """Not a real source, just a way to add tags to an item. Will be removed from the item sources during unpacking."""
    tag: Tuple[ItemTag, ...]

    def __init__(self, *tag: ItemTag):
        self.tag = tag  # noqa

    @property
    def add_tags(self):
        return self.tag


@dataclass(frozen=True)
class GameItem:
    name: str
    sources: List[ItemSource] = field(default_factory=list)
    tags: Set[ItemTag] = field(default_factory=set)

    def add_sources(self, sources: Iterable[ItemSource]):
        self.sources.extend(source for source in sources if type(source) is not Tag)
        for source in sources:
            self.add_tags(source.add_tags)

    def add_tags(self, tags: Iterable[ItemTag]):
        self.tags.update(tags)

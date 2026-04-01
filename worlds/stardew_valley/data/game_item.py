import enum
from abc import ABC
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, ClassVar, Mapping, Callable, TYPE_CHECKING

from ..stardew_rule.protocol import StardewRule

if TYPE_CHECKING:
    from ..logic.logic import StardewLogic

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
    HAT = enum.auto()
    FORAGE = enum.auto()
    COOKING = enum.auto()


@dataclass(frozen=True)
class Source(ABC):
    add_tags: ClassVar[tuple[ItemTag]] = ()

    other_requirements: tuple[Requirement, ...] = field(kw_only=True, default=())

    @property
    def requirement_tags(self) -> Mapping[str, tuple[ItemTag, ...]]:
        return DEFAULT_REQUIREMENT_TAGS

    @property
    def all_requirements(self) -> Iterable[Requirement]:
        """Returns all requirements that are not directly part of the source."""
        return self.other_requirements


@dataclass(frozen=True, kw_only=True)
class GenericSource(Source):
    regions: tuple[str, ...] = ()
    """No region means it's available everywhere."""


@dataclass(frozen=True, kw_only=True)
class AllRegionsSource(Source):
    regions: tuple[str, ...] = ()


@dataclass(frozen=True)
class CustomRuleSource(Source):
    """Hopefully once everything is migrated to sources, we won't need these custom logic anymore."""
    create_rule: "Callable[[StardewLogic], StardewRule]"


class Tag(Source):
    """Not a real source, just a way to add tags to an item. Will be removed from the item sources during unpacking."""
    tag: tuple[ItemTag, ...]

    def __init__(self, *tag: ItemTag):
        self.tag = tag  # noqa

    @property
    def add_tags(self):
        return self.tag


@dataclass(frozen=True)
class GameItem:
    name: str
    sources: list[Source] = field(default_factory=list)
    tags: set[ItemTag] = field(default_factory=set)

    def add_sources(self, sources: Iterable[Source]):
        self.sources.extend(source for source in sources if type(source) is not Tag)
        for source in sources:
            self.add_tags(source.add_tags)

    def add_tags(self, tags: Iterable[ItemTag]):
        self.tags.update(tags)

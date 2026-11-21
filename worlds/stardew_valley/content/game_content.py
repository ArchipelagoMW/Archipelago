from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from types import MappingProxyType
from typing import Iterable, Set, Any, Mapping, Generator

from .feature import BooksanityFeature, BuildingProgressionFeature, CropsanityFeature, FishsanityFeature, FriendsanityFeature, HatsanityFeature, \
    MuseumsanityFeature, SkillProgressionFeature, ToolProgressionFeature
from .feature.base import DisableSourceHook, DisableRequirementHook, FeatureBase
from ..data.animal import Animal
from ..data.building import Building
from ..data.fish_data import FishItem
from ..data.game_item import GameItem, Source, ItemTag, Requirement
from ..data.hats_data import HatItem
from ..data.skill import Skill
from ..data.villagers_data import Villager


@dataclass(frozen=True)
class StardewContent:
    features: StardewFeatures
    registered_packs: Set[str] = field(default_factory=set)

    # regions -> To be used with can reach rule

    game_items: dict[str, GameItem] = field(default_factory=dict)
    fishes: dict[str, FishItem] = field(default_factory=dict)
    villagers: dict[str, Villager] = field(default_factory=dict)
    farm_buildings: dict[str, Building] = field(default_factory=dict)
    animals: dict[str, Animal] = field(default_factory=dict)
    skills: dict[str, Skill] = field(default_factory=dict)
    quests: dict[str, Any] = field(default_factory=dict)
    hats: dict[str, HatItem] = field(default_factory=dict)

    def find_sources_of_type(self, *types: type[Source]) -> Iterable[Source]:
        for item in self.game_items.values():
            for source in item.sources:
                if isinstance(source, types):
                    yield source

    def source_item(self, item_name: str, *sources: Source) -> GameItem:
        filtered_sources = list(self._filter_sources(sources))

        item = self.game_items.setdefault(item_name, GameItem(item_name))
        item.add_sources(filtered_sources)

        for source in filtered_sources:
            for requirement_name, tags in source.requirement_tags.items():
                self.tag_item(requirement_name, *tags)

        return item

    def tag_item(self, item_name: str, *tags: ItemTag):
        item = self.game_items.setdefault(item_name, GameItem(item_name))
        item.add_tags(tags)

    def untag_item(self, item_name: str, tag: ItemTag):
        self.game_items[item_name].tags.remove(tag)

    def find_tagged_items(self, tag: ItemTag) -> Generator[GameItem]:
        # TODO might be worth caching this, but it need to only be cached once the content is finalized...
        for item in self.game_items.values():
            if tag in item.tags:
                yield item

    def are_all_enabled(self, content_packs: frozenset[str]) -> bool:
        return content_packs.issubset(self.registered_packs)

    def is_enabled(self, content_pack: str | ContentPack) -> bool:
        if isinstance(content_pack, ContentPack):
            content_pack = content_pack.name

        return content_pack in self.registered_packs

    def _filter_sources(self, sources: Iterable[Source]) -> Generator[Source]:
        """Filters out sources that are disabled by features."""
        for source in sources:
            if not self._is_disabled(source):
                yield source

    def _is_disabled(self, source: Source) -> bool:
        """Checks if a source is disabled by any feature."""
        try:
            hook = self.features.disable_source_hooks[type(source)]
            if hook(source, content=self):
                return True
        except KeyError:
            pass

        for requirement in source.all_requirements:
            try:
                hook = self.features.disable_requirement_hooks[type(requirement)]
                if hook(requirement, content=self):
                    return True
            except KeyError:
                pass

        return False


@dataclass(frozen=True)
class StardewFeatures:
    booksanity: BooksanityFeature
    building_progression: BuildingProgressionFeature
    cropsanity: CropsanityFeature
    fishsanity: FishsanityFeature
    friendsanity: FriendsanityFeature
    hatsanity: HatsanityFeature
    museumsanity: MuseumsanityFeature
    skill_progression: SkillProgressionFeature
    tool_progression: ToolProgressionFeature

    @cached_property
    def all_features(self) -> Iterable[FeatureBase]:
        return (self.booksanity, self.building_progression, self.cropsanity, self.fishsanity, self.friendsanity, self.hatsanity, self.museumsanity,
                self.skill_progression, self.tool_progression)

    @cached_property
    def disable_source_hooks(self) -> Mapping[type[Source], DisableSourceHook]:
        """Returns a set of source types that are disabled by features. Need to be exact types, subclasses are not considered."""
        hooks = {}
        for feature in self.all_features:
            hooks.update(feature.disable_source_hooks)
        return MappingProxyType(hooks)

    @cached_property
    def disable_requirement_hooks(self) -> Mapping[type[Requirement], DisableRequirementHook]:
        """Returns a set of requirement types that are disabled by features. Need to be exact types, subclasses are not considered."""
        hooks = {}
        for feature in self.all_features:
            hooks.update(feature.disable_requirement_hooks)
        return MappingProxyType(hooks)


@dataclass(frozen=True)
class ContentPack:
    name: str

    dependencies: Iterable[str] = ()
    """ Hard requirement, generation will fail if it's missing. """
    weak_dependencies: Iterable[str] = ()
    """ Not a strict dependency, only used only for ordering the packs to make sure hooks are applied correctly. """

    # items
    # def item_hook
    # ...

    harvest_sources: Mapping[str, Iterable[Source]] = field(default_factory=dict)
    """Harvest sources contains both crops and forageables, but also fruits from trees, the cave farm and stuff harvested from tapping like maple syrup."""

    def harvest_source_hook(self, content: StardewContent):
        ...

    shop_sources: Mapping[str, Iterable[Source]] = field(default_factory=dict)

    def shop_source_hook(self, content: StardewContent):
        ...

    fishes: Iterable[FishItem] = ()

    def fish_hook(self, content: StardewContent):
        ...

    crafting_sources: Mapping[str, Iterable[Source]] = field(default_factory=dict)

    def crafting_hook(self, content: StardewContent):
        ...

    artisan_good_sources: Mapping[str, Iterable[Source]] = field(default_factory=dict)

    def artisan_good_hook(self, content: StardewContent):
        ...

    villagers: Iterable[Villager] = ()

    def villager_hook(self, content: StardewContent):
        ...

    farm_buildings: Iterable[Building] = ()

    def farm_building_hook(self, content: StardewContent):
        ...

    animals: Iterable[Animal] = ()

    def animal_hook(self, content: StardewContent):
        ...

    skills: Iterable[Skill] = ()

    def skill_hook(self, content: StardewContent):
        ...

    quests: Iterable[Any] = ()

    def quest_hook(self, content: StardewContent):
        ...
        ...

    hat_sources: Mapping[HatItem, Iterable[Source]] = field(default_factory=dict)

    def hat_source_hook(self, content: StardewContent):
        ...

    def finalize_hook(self, content: StardewContent):
        """Last hook called on the pack, once all other content packs have been registered.

        This is the place to do any final adjustments to the content, like adding rules based on tags applied by other packs.
        """
        ...

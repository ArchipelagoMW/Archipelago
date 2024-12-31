from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Set, Any, Mapping, Type, Tuple, Union

from .feature import booksanity, cropsanity, fishsanity, friendsanity, skill_progression
from ..data.fish_data import FishItem
from ..data.game_item import GameItem, ItemSource, ItemTag
from ..data.skill import Skill
from ..data.villagers_data import Villager


@dataclass(frozen=True)
class StardewContent:
    features: StardewFeatures
    registered_packs: Set[str] = field(default_factory=set)

    # regions -> To be used with can reach rule

    game_items: Dict[str, GameItem] = field(default_factory=dict)
    fishes: Dict[str, FishItem] = field(default_factory=dict)
    villagers: Dict[str, Villager] = field(default_factory=dict)
    skills: Dict[str, Skill] = field(default_factory=dict)
    quests: Dict[str, Any] = field(default_factory=dict)

    def find_sources_of_type(self, types: Union[Type[ItemSource], Tuple[Type[ItemSource]]]) -> Iterable[ItemSource]:
        for item in self.game_items.values():
            for source in item.sources:
                if isinstance(source, types):
                    yield source

    def source_item(self, item_name: str, *sources: ItemSource):
        item = self.game_items.setdefault(item_name, GameItem(item_name))
        item.add_sources(sources)

    def tag_item(self, item_name: str, *tags: ItemTag):
        item = self.game_items.setdefault(item_name, GameItem(item_name))
        item.add_tags(tags)

    def untag_item(self, item_name: str, tag: ItemTag):
        self.game_items[item_name].tags.remove(tag)

    def find_tagged_items(self, tag: ItemTag) -> Iterable[GameItem]:
        # TODO might be worth caching this, but it need to only be cached once the content is finalized...
        for item in self.game_items.values():
            if tag in item.tags:
                yield item


@dataclass(frozen=True)
class StardewFeatures:
    booksanity: booksanity.BooksanityFeature
    cropsanity: cropsanity.CropsanityFeature
    fishsanity: fishsanity.FishsanityFeature
    friendsanity: friendsanity.FriendsanityFeature
    skill_progression: skill_progression.SkillProgressionFeature


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

    harvest_sources: Mapping[str, Iterable[ItemSource]] = field(default_factory=dict)
    """Harvest sources contains both crops and forageables, but also fruits from trees, the cave farm and stuff harvested from tapping like maple syrup."""

    def harvest_source_hook(self, content: StardewContent):
        ...

    shop_sources: Mapping[str, Iterable[ItemSource]] = field(default_factory=dict)

    def shop_source_hook(self, content: StardewContent):
        ...

    fishes: Iterable[FishItem] = ()

    def fish_hook(self, content: StardewContent):
        ...

    crafting_sources: Mapping[str, Iterable[ItemSource]] = field(default_factory=dict)

    def crafting_hook(self, content: StardewContent):
        ...

    artisan_good_sources: Mapping[str, Iterable[ItemSource]] = field(default_factory=dict)

    def artisan_good_hook(self, content: StardewContent):
        ...

    villagers: Iterable[Villager] = ()

    def villager_hook(self, content: StardewContent):
        ...

    skills: Iterable[Skill] = ()

    def skill_hook(self, content: StardewContent):
        ...

    quests: Iterable[Any] = ()

    def quest_hook(self, content: StardewContent):
        ...

    def finalize_hook(self, content: StardewContent):
        """Last hook called on the pack, once all other content packs have been registered.

        This is the place to do any final adjustments to the content, like adding rules based on tags applied by other packs.
        """
        ...

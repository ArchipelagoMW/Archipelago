from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Set, Any, Mapping

from .feature import fishsanity, friendsanity
from ..data.fish_data import FishItem
from ..data.game_item import GameItem, ItemSource
from ..data.villagers_data import Villager


@dataclass(frozen=True)
class StardewContent:
    features: StardewFeatures
    registered_packs: Set[str] = field(default_factory=set)

    # regions -> To be used with can reach rule

    game_items: Dict[str, GameItem] = field(default_factory=dict)
    fishes: Dict[str, FishItem] = field(default_factory=dict)
    villagers: Dict[str, Villager] = field(default_factory=dict)
    skills: Dict[str, Any] = field(default_factory=dict)
    quests: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StardewFeatures:
    fishsanity: fishsanity.FishsanityFeature
    friendsanity: friendsanity.FriendsanityFeature


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

    villagers: Iterable[Villager] = ()

    def villager_hook(self, content: StardewContent):
        ...

    skills: Iterable[Any] = ()

    def skill_hook(self, content: StardewContent):
        ...

    quests: Iterable[Any] = ()

    def quest_hook(self, content: StardewContent):
        ...

from __future__ import annotations

import string
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Set, FrozenSet, Tuple, Union, List

import Utils
from . import FactorioOptions
from .FactorioUtils import FactorioElement, load_json_data
from .InternalItem import raw_recipes, InternalItem, recipe_sources, mining_with_fluid_sources, \
    all_ingredients, valid_ingredients, artifacts, invalid_ingredients

def always(state) -> bool:
    return True

class Technology(FactorioElement):  # maybe make subclass of Location?
    progressive: Tuple[str, ...]
    unlocks: Union[Set[str], bool]  # bool case is for progressive technologies
    modifiers: list[str]

    def __init__(self, technology_name: str, modpack: "FactorioModpack", progressive: Tuple[str, ...] = (),
                 modifiers: list[str] = None, unlocks: Union[Set[str], bool] = None):
        self.name = technology_name
        self.modpack = modpack
        self.progressive = progressive
        if modifiers is None:
            modifiers = []
        self.modifiers =  modifiers
        if unlocks:
            self.unlocks = unlocks
        else:
            self.unlocks = set()

    @property
    def has_modifier(self) -> bool:
        return bool(self.modifiers)

    def get_custom(self, world, allowed_packs: Set[str], player: int) -> CustomTechnology:
        return CustomTechnology(self, world, allowed_packs, player)

    def useful(self) -> bool:
        if self.name in self.modpack.force_useless_technologies:
            return self.modpack.override_useless_technologies[self.name]
        return self.has_modifier or self.unlocks


class CustomTechnology(Technology):
    """A particularly configured Technology for a world."""
    ingredients: Set[str]

    def __init__(self, origin: Technology, world, allowed_packs: Set[str], player: int):
        ingredients = allowed_packs
        self.player = player
        if origin.name not in world.special_nodes:
            ingredients = set(world.random.sample(list(ingredients), world.random.randint(1, len(ingredients))))
        self.ingredients = ingredients
        super(CustomTechnology, self).__init__(origin.name, origin.factorio_id)

    def get_prior_technologies(self) -> Set[Technology]:
        """Get Technologies that have to precede this one to resolve tree connections."""
        technologies = set()
        for ingredient in self.ingredients:
            technologies |= required_technologies[ingredient]  # technologies that unlock the recipes
        return technologies

excluded_automation_ingredients: Set[str] = {"bob-diamond-ore",
                                            "bob-amethyst-ore",
                                            "bob-emerald-ore",
                                            "bob-topaz-ore",
                                            "bob-sapphire-ore",
                                            "bob-ruby-ore",
                                            "bob-bauxite-ore",
                                            "bob-silver-ore",
                                            "bob-gold-ore",
                                            "bob-zinc-ore",
                                            "bob-tungsten-ore",
                                            "bob-nickel-ore",
                                            "bob-rutile-ore", }.union(artifacts)

def get_ordered_items(key: Callable[[InternalItem], int] = lambda item: item.get_score()) -> tuple[set[InternalItem], List[InternalItem]]:
    science_packs = FactorioOptions.MaxSciencePack.get_ordered_science_packs()
    valid_items = set(x for x in valid_ingredients.values() if all(raw.name not in invalid_ingredients for raw in x.get_raw_ingredients().keys())
                                                            and x.name not in science_packs)
    starting_pool = set()
    for item in valid_items:
        if not item.all_unlocking_technologies() and not item.is_fluid and all(raw.name not in excluded_automation_ingredients for raw in item.get_raw_ingredients().keys()):
            starting_pool.add(item)

    valid_items.difference_update(starting_pool)
    ordered_items: list[InternalItem] = list(sorted(valid_items, key=key))
    return starting_pool, ordered_items

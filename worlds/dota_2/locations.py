from __future__ import annotations

import json
from importlib import resources
import typing
from typing import TYPE_CHECKING, Dict, List
from dataclasses import dataclass, field
from .hero import Hero, get_all_heroes,get_starting_hero_pool

from BaseClasses import ItemClassification, Location

from . import items


@dataclass(frozen=True)
class LocationDef:
    name: str
    type: str = ""  # "HERO_WIN", "ITEM_BUY", "GAME_STAT", "GOAL"
    requirements: list[str] = field(default_factory=list)


class DOTA2Location(Location):
    game = "DOTA 2"


def load_hero_locations(self) -> List[LocationDef]:
    locs: List[LocationDef] = []

    all_heroes = get_all_heroes()
    starting_hero_pool = get_starting_hero_pool(self, 30, all_heroes)
    remaining_heroes =  [
        hero for hero in all_heroes
        if hero not in starting_hero_pool
    ]

    self.multiworld.random.shuffle(remaining_heroes)
    hero_groups = [
        remaining_heroes[i:i + 14]
        for i in range(0, len(remaining_heroes), 14)
    ]   

    self.hero_groups = hero_groups
    self.starting_hero_pool = starting_hero_pool
    
    self.unlocked_heroes = starting_hero_pool.copy()
    self.unique_heroes_won = []

    locs.append(LocationDef(name = "Win with hero from starting pool", type = "HERO_WIN"))
    for i, group in enumerate(hero_groups):
        name = f"Win with Hero from Group {i+1}"
        type = "HERO_WIN"
        locs.append(LocationDef(name = name, type=type))
    return locs

def load_item_locations() -> List[LocationDef]:
    locs: List[LocationDef] = []

    with resources.files(__package__).joinpath("data/dotaShopLocations.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

        for item_name, item_data in data.items():
            requirements = item_data.get("requirements") or []
            type = 'ITEM_BUY'
            name = item_data["dname"]

            locs.append(LocationDef(name = name, type=type, requirements=requirements))

    return locs

def build_item_name_to_dname() -> List[LocationDef]:
    item_name_to_dname: dict

    with resources.files(__package__).joinpath("data/dotaShopLocations.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

        item_name_to_dname = {item_name: item_data["dname"] for item_name, item_data in data.items() if item_data.get("dname")}

    return item_name_to_dname

def load_game_stat_locations() -> List[LocationDef]:
    locs: List[LocationDef] = []

    with resources.files(__package__).joinpath("data/gameStatLocations.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

        for item in data['game_stat_locations']:
            type = ''
            name = item['name']
            type = "GAME_STAT"

            locs.append(LocationDef(name = name, type=type))

    return locs

def build_location_name_to_id(base_id: int, location_defs: List[LocationDef], filter_fn: typing.Callable[[LocationDef], bool] | None = None,
    ) -> Dict[str, int]:
    """Build name -> id. If filter_fn is set, only include defs that pass it; IDs use index in full list."""
    if filter_fn is None:
        return {d.name: base_id + i for i, d in enumerate(location_defs)}
    return {d.name: base_id + i for i, d in enumerate(location_defs) if filter_fn(d)}

def load_static_hero_locations() -> List[LocationDef]:
    locs: List[LocationDef] = []

    all_heroes = get_all_heroes()

    # Starting pool is always 30 heroes.
    # The remaining heroes are divided into groups of 14.
    remaining_count = max(0, len(all_heroes) - 30)
    group_count = (remaining_count + 13) // 14

    locs.append(
        LocationDef(
            name="Win with hero from starting pool",
            type="HERO_WIN",
        )
    )

    for i in range(group_count):
        locs.append(
            LocationDef(
                name=f"Win with Hero from Group {i + 1}",
                type="HERO_WIN",
            )
        )

    return locs

def load_victory_location() -> List[LocationDef]:
    locs: List[LocationDef] = []

    locs.append(
        LocationDef(
            name="Goal Complete",
            type="GOAL",
        )
    )
    return locs



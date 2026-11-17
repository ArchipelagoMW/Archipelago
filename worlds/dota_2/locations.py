from __future__ import annotations

import json
from importlib import resources
import typing
from typing import TYPE_CHECKING, Dict, List
from dataclasses import dataclass, field
from .hero import Hero, get_all_heroes,get_starting_hero_pool

from BaseClasses import ItemClassification, Location

from . import items
from .challenges import CHALLENGE_CHECKS, STATS, MAX_STAT_CHECKS, ORIGINAL_STAT_CHECKS, stat_check
from .constants import MAX_HERO_GROUPS, ORIGINAL_HERO_GROUPS


@dataclass(frozen=True)
class LocationDef:
    name: str
    type: str = ""  # "HERO_WIN", "ITEM_BUY", "GAME_STAT", "GOAL", MINIGAME, CHALLENGE
    requirements: list[str] = field(default_factory=list)


class DOTA2Location(Location):
    game = "DOTA 2"


def load_hero_locations(self) -> List[LocationDef]:
    locs: List[LocationDef] = []

    all_heroes = get_all_heroes()
    starting_hero_pool = get_starting_hero_pool(self, self.options.starting_heroes.value, all_heroes)
    remaining_heroes =  [
        hero for hero in all_heroes
        if hero not in starting_hero_pool
    ]

    self.multiworld.random.shuffle(remaining_heroes)
    # Split evenly, larger groups first (30 starting heroes and 7 groups give the original groups of 14)
    group_count = min(self.options.hero_groups.value, len(remaining_heroes))
    size, extra = divmod(len(remaining_heroes), group_count)
    hero_groups = []
    for i in range(group_count):
        start = i * size + min(i, extra)
        hero_groups.append(remaining_heroes[start:start + size + (1 if i < extra else 0)])

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

def load_minigame_locations() -> List[LocationDef]:
    locs: List[LocationDef] = []

    with resources.files(__package__).joinpath("data/minigameLocations.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

        for minigame_name, minigame_data in data.items():
            requirements = minigame_data.get("requirements") or []
            type = 'MINIGAME'
            name = minigame_data["dname"]

            locs.append(LocationDef(name = name, type=type, requirements=requirements))

    return locs

def build_item_name_to_dname() -> List[LocationDef]:
    item_name_to_dname: dict

    with resources.files(__package__).joinpath("data/dotaShopLocations.json").open("r", encoding="utf-8") as f:
        data = json.load(f)

        item_name_to_dname = {item_name: item_data["dname"] for item_name, item_data in data.items() if item_data.get("dname")}

        # OpenDota reports purchases by internal item name, which is the image file name and can
        # differ from the key here: ancient_janggo (Drum of Endurance), assault (Assault Cuirass),
        # angels_demise (Khanda), devastator (Parasma)
        for item_data in data.values():
            img = item_data.get("img") or ""
            if "/items/" in img and item_data.get("dname"):
                item_name_to_dname.setdefault(img.split("/items/")[1].split(".png")[0], item_data["dname"])

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

    # Locations of the original 7 groups (30 starting heroes, groups of 14); more groups are in load_extra_group_locations
    group_count = ORIGINAL_HERO_GROUPS

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

def load_extra_group_locations() -> List[LocationDef]:
    """Wins with groups past the original 7, at the end so existing location ids don't move."""
    return [LocationDef(name=f"Win with Hero from Group {i}", type="HERO_WIN")
            for i in range(ORIGINAL_HERO_GROUPS + 1, MAX_HERO_GROUPS + 1)]

def load_extra_stat_locations() -> List[LocationDef]:
    """Stat checks past the original three per stat, at the end so existing location ids don't move."""
    return [LocationDef(name=stat_check(label, n), type="GAME_STAT")
            for label, _, _, _ in STATS for n in range(ORIGINAL_STAT_CHECKS + 1, MAX_STAT_CHECKS + 1)]

def load_challenge_locations() -> List[LocationDef]:
    return [LocationDef(name=name, type="CHALLENGE") for name in CHALLENGE_CHECKS]

def load_victory_location() -> List[LocationDef]:
    locs: List[LocationDef] = []

    locs.append(
        LocationDef(
            name="Goal Complete",
            type="GOAL",
        )
    )
    return locs



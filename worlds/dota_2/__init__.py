from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, List, Dict

from BaseClasses import Region, ItemClassification
from worlds.AutoWorld import World, WebWorld

# Imports of base Archipelago modules must be absolute.
from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld

# Imports of your world's files must be relative.
from .constants import DOTA2_BASE_ID
from .options import (DOTA2Options, GoalType, CrownFall)
from .items import DOTA2Item, ItemDef, load_hero_unlock_items, build_item_name_to_id, FILLER_ITEM_NAME,load_item_defs, load_shop_unlock_items, load_minigame_unlock_items
from .locations import DOTA2Location, LocationDef, load_hero_locations, build_location_name_to_id, load_item_locations, load_game_stat_locations,load_static_hero_locations, load_victory_location, load_minigame_locations, load_challenge_locations
from .rules import set_dota_rules
from .regions import create_regions_and_locations
from .hero import Hero, get_starting_hero_pool, get_all_heroes
from .challenges import resolve_disabled, VALUES
# For our game to display correctly on the website, we need to define a WebWorld subclass.
class DOTA2WebWorld(WebWorld):
    # We need to override the "game" field of the WebWorld superclass.
    # This must be the same string as the regular World class.
    game = "DOTA 2"

    # Your game pages will have a visual theme (affecting e.g. the background image).
    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "stone"

    # A WebWorld can have any number of tutorials, but should always have at least an English setup guide.
    # Many WebWorlds just have one setup guide, but some have multiple, e.g. for different languages.
    # We need to create a Tutorial object for every setup guide.
    # In order, we need to provide a title, a description, a language, a filepath, a link, and authors.
    # The filepath is relative to a "/docs/" directory in the root folder of your apworld.
    # The "link" parameter is unused, but we still need to provide it.
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up DOTA 2 for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CaptainBoscar"],
    )

    # We add these tutorials to our WebWorld by overriding the "tutorials" field.
    tutorials = [setup_en]


class DOTA2World(World):
    game = "DOTA 2"
    web = DOTA2WebWorld()
      # This is how we associate the options defined in our options.py with our world.
    options_dataclass = DOTA2Options
    options: DOTA2Options  # Common mistake: This has to be a colon (:), not an equals sign (=).

    starting_hero_pool: list[Hero] = field(default_factory=list)
    hero_groups: list[list[Hero]] = field(default_factory=list)
    unlocked_heroes: list[Hero] = field(default_factory=list)
    unique_heroes_won: list[Hero] = field(default_factory=list)
    all_heroes = get_all_heroes()

    progressive_hero_group_unlocks: int = 0
    items_received_index: int = 0 
    

    # Choose a stable, unique base_id range for your world.
    base_id = DOTA2_BASE_ID

    _location_defs = (
            load_static_hero_locations()
            + load_item_locations()
            + load_game_stat_locations()
            + load_victory_location()
            + load_minigame_locations()
            + load_challenge_locations()  # last, so the ids of older locations don't move
        )

    _item_defs = load_item_defs()

    location_name_to_id: Dict[str, int] = build_location_name_to_id(base_id + 10_000, _location_defs,)
    item_name_to_id: Dict[str, int] =  build_item_name_to_id(base_id, _item_defs)

    def create_item(self, name: str) -> DOTA2Item:
        # Determine classification from defs or fallback for special items.
        if name == FILLER_ITEM_NAME:
            classification = ItemClassification.filler
        else:
            d = next((x for x in self._item_defs if x.name == name), None)
            if d is None:
                raise KeyError(f"Unknown item '{name}'")
            classification = d.classification
        return DOTA2Item(name, classification, self.item_name_to_id.get(name), self.player)

    def create_event(self, name: str) -> DOTA2Item:
        # Event items have id=None (not part of item_name_to_id)
        return DOTA2Item(name, ItemClassification.progression, None, self.player)
    

    def generate_early(self) -> None:
        self._location_defs = []
        self._item_defs = []
        self._location_defs.extend(load_hero_locations(self))
        self._location_defs.extend(load_item_locations())
        self._location_defs.extend(load_game_stat_locations())
        self._location_defs.extend(load_victory_location())
        self._location_defs.extend(load_minigame_locations())
        self._location_defs.extend(load_challenge_locations())

        self._item_defs.extend(load_hero_unlock_items(self))
        self._item_defs.extend(load_shop_unlock_items())
        self._item_defs.extend(load_minigame_unlock_items())

        exclude_minigames = self.options.crownfall == CrownFall.option_off
        disabled_challenges = resolve_disabled(self.options.disabled_checks.value)

        # location_name_to_id is set per-instance in generate_early from filtered defs (see below).
        def location_type_valid(d: LocationDef) -> bool:
            if d.type == "CHALLENGE":
                return d.name not in disabled_challenges
            if not exclude_minigames: 
                return d.type == "HERO_WIN" or d.type ==  "ITEM_BUY" or d.type ==  "GAME_STAT" or d.type ==  "GOAL" or d.type ==  "MINIGAME"
            if exclude_minigames:
                 return d.type == "HERO_WIN" or d.type ==  "ITEM_BUY" or d.type ==  "GAME_STAT" or d.type ==  "GOAL"
                
    
        self._filtered_location_defs = [d for d in self._location_defs if location_type_valid(d)]
        self.location_name_to_id = build_location_name_to_id(
            self.base_id + 10_000, self._location_defs, filter_fn=location_type_valid
        )

    def create_regions(self) -> None:
        create_regions_and_locations(self, self._filtered_location_defs)

    def _max_primordial_fragments_placeable(self) -> int:
        """MacGuffin slots ~= non-Goal check locations (Goal holds locked Victory)."""
        return len(self._filtered_location_defs) - 1

    def _effective_primordial_fragments_to_unlock_final(self) -> int:
        """
        primordial fragments required before being able to release. Matches what we send in slot_data.
        """
        max_sp = self._max_primordial_fragments_placeable()
        v = min(self.options.primordial_fragments_to_unlock_final.value, max_sp)
    
        if self.options.goal_type.value == GoalType.option_win_with_character:
            v = min(v, max(1, max_sp - 1))
        return max(1, v)

    # def _goal_location_name(self) -> str:
    #     if self.options.goal_type == GoalType.option_unique_characters:
    #         x = self.options.unique_characters_to_win.value
    #         return f"Goal: Win with {x} Unique Characters"
    #     if self.options.goal_type == GoalType.option_total_wins:
    #         x = self.options.total_wins_to_win.value
    #         y = self.options.primordial_fragments_to_unlock_final.value
    #         return f"Goal: Win {x} Total Matches and Collect {y} Primordial Fragments "
    #     if self.options.goal_type == GoalType.option_win_with_character:
    #         x = self.options.primordial_fragments_to_unlock_final.value
    #         hero = _FINAL_CHARACTER_NAMES[self.options.final_character.value] if self.options.final_character.value < len(_FINAL_CHARACTER_NAMES) else "?"
    #         return f"Goal: Win with {hero} (after {x} Spirits)"
    #     x = self.options.spirits_to_win.value
    #     return f"Goal: Collect {x} Spirits"

    def fill_slot_data(self) -> Mapping[str, Any]:
        """Data sent to the client in the Connected packet so /goal and win condition use the correct options."""
        # Max fragmetns = number of check locations (pool size); Goal has locked Victory so pool size is locations - 1
        #max_primordial_fragments = self._max_primordial_fragments_placeable()
        #primordial_fragments_to_win = self.options.primordial_fragments_to_win.value
        #primordial_fragments_to_unlock_final = self._effective_primordial_fragments_to_unlock_final()
        # final_character_index = self.options.final_character.value
        # final_character_name = _FINAL_CHARACTER_NAMES[final_character_index] if final_character_index < len(_FINAL_CHARACTER_NAMES) else ""

        starting_hero_pool = [hero.name for hero in self.starting_hero_pool]
        hero_groups = [ [hero.name for hero in group] for group in self.hero_groups]
    

        return {
            "goal_type": self.options.goal_type.value,
            "unique_characters_to_win": self.options.unique_characters_to_win.value,
            "total_wins_to_win": self.options.total_wins_to_win.value,
            "primordial_fragments_to_win": self.options.primordial_fragments_to_win.value,
            "starting_hero_pool": starting_hero_pool,
            "hero_groups": hero_groups,
            "progressive_hero_group_unlocks": self.progressive_hero_group_unlocks,
            "items_received_index": self.items_received_index,
            "item_name_to_id": self.item_id_to_name,
            "check_values": {name: self.options.check_values.value.get(name, default) for name, (default, _, _) in VALUES.items()},
            # "game_mode": self.options.game_mode.value,
            # "exclude_hard_locations": self.options.exclude_hard_locations.value,
        }
    def create_items(self) -> None:
        # Add all defined items with copies
        pool = []
    
        for d in self._item_defs:
            for _ in range(d.copies):
                pool.append(self.create_item(d.name))

        # Pad pool so total items = locations that take an item (Goal Complete already holds its locked event)
        loc_count = len([loc for loc in self.multiworld.get_locations(self.player) if loc.address is not None])
        if len(pool) < loc_count:
            pool += [self.create_item(FILLER_ITEM_NAME) for _ in range(loc_count - len(pool))]

        self.multiworld.itempool += pool

    def set_rules(self) -> None:
        set_dota_rules(self)
    

   
def _launch_dota2_client(*args: str) -> None:
    from worlds import LauncherComponents
    from .Client import run_dota2_client
    LauncherComponents.launch(run_dota2_client, name="DOTA 2 Client", args=args)

def _register_dota2_icon() -> str:
    """
    Register our icon with LauncherComponents using the apworld format so the launcher
    loads it from inside the apworld (no cache folder or filesystem extraction needed).
    See: LauncherComponents.py comment re "ap:module.name/path/to/file.png"
    """
    try:
        from worlds import LauncherComponents
    except ImportError:
        return "icon"  # fallback to default

    icon_key = "dota2"
    if icon_key not in LauncherComponents.icon_paths:
        LauncherComponents.icon_paths[icon_key] = f"ap:{__name__}/icons/Dota2.png"
    return icon_key

def _register_launcher_component() -> None:
    try:
        from worlds.LauncherComponents import Component, components
    except ImportError:
        return

    components.append(Component(
        display_name="Dota 2 Client",
        func=_launch_dota2_client,
        game_name="Dota 2",
        supports_uri=True,
        description="DOTA 2 Archipelago client.",
        icon=_register_dota2_icon(),
    ))

_register_launcher_component()
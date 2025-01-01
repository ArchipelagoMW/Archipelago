import functools
import logging
from typing import Any, Dict, List

from BaseClasses import Entrance, CollectionState, Item, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from . import Items, Locations, Maps, Regions, Rules
from .Options import DOOM1993Options

logger = logging.getLogger("DOOM 1993")

DOOM_TYPE_LEVEL_COMPLETE = -2
DOOM_TYPE_COMPUTER_AREA_MAP = 2026


class DOOM1993Location(Location):
    game: str = "DOOM 1993"


class DOOM1993Item(Item):
    game: str = "DOOM 1993"


class DOOM1993Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the DOOM 1993 randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Daivuk"]
    )]
    theme = "dirt"


class DOOM1993World(World):
    """
    Developed by id Software, and originally released in 1993, DOOM pioneered and popularized the first-person shooter,
    setting a standard for all FPS games.
    """
    options_dataclass = DOOM1993Options
    options: DOOM1993Options
    game = "DOOM 1993"
    web = DOOM1993Web()
    required_client_version = (0, 3, 9)

    item_name_to_id = {data["name"]: item_id for item_id, data in Items.item_table.items()}
    item_name_groups = Items.item_name_groups

    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    location_name_groups = Locations.location_name_groups

    starting_level_for_episode: List[str] = [
        "Hangar (E1M1)",
        "Deimos Anomaly (E2M1)",
        "Hell Keep (E3M1)",
        "Hell Beneath (E4M1)"
    ]

    boss_level_for_espidoes: List[str] = [
        "Phobos Anomaly (E1M8)",
        "Tower of Babel (E2M8)",
        "Dis (E3M8)",
        "Unto the Cruel (E4M8)"
    ]

    # Item ratio that scales depending on episode count. These are the ratio for 3 episode.
    items_ratio: Dict[str, float] = {
        "Armor": 41,
        "Mega Armor": 25,
        "Berserk": 12,
        "Invulnerability": 10,
        "Partial invisibility": 18,
        "Supercharge": 28,
        "Medikit": 15,
        "Box of bullets": 13,
        "Box of rockets": 13,
        "Box of shotgun shells": 13,
        "Energy cell pack": 10
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        self.included_episodes = [1, 1, 1, 0]
        self.location_count = 0

        super().__init__(multiworld, player)

    def get_episode_count(self):
        return functools.reduce(lambda count, episode: count + episode, self.included_episodes)

    def generate_early(self):
        # Cache which episodes are included
        self.included_episodes[0] = self.options.episode1.value
        self.included_episodes[1] = self.options.episode2.value
        self.included_episodes[2] = self.options.episode3.value
        self.included_episodes[3] = self.options.episode4.value

        # If no episodes selected, select Episode 1
        if self.get_episode_count() == 0:
            self.included_episodes[0] = 1

    def create_regions(self):
        pro = self.options.pro.value

        # Main regions
        menu_region = Region("Menu", self.player, self.multiworld)
        hub_region = Region("Hub", self.player, self.multiworld)
        self.multiworld.regions += [menu_region, hub_region]
        menu_region.add_exits(["Hub"])

        # Create regions and locations
        main_regions = []
        connections = []
        for region_dict in Regions.regions:
            if not self.included_episodes[region_dict["episode"] - 1]:
                continue

            region_name = region_dict["name"]
            if region_dict["connects_to_hub"]:
                main_regions.append(region_name)

            region = Region(region_name, self.player, self.multiworld)
            region.add_locations({
                loc["name"]: loc_id
                for loc_id, loc in Locations.location_table.items()
                if loc["region"] == region_name and self.included_episodes[loc["episode"] - 1]
            }, DOOM1993Location)

            self.multiworld.regions.append(region)

            for connection_dict in region_dict["connections"]:
                # Check if it's a pro-only connection
                if connection_dict["pro"] and not pro:
                    continue
                connections.append((region, connection_dict["target"]))
        
        # Connect main regions to Hub
        hub_region.add_exits(main_regions)

        # Do the other connections between regions (They are not all both ways)
        for connection in connections:
            source = connection[0]
            target = self.multiworld.get_region(connection[1], self.player)

            entrance = Entrance(self.player, f"{source.name} -> {target.name}", source)
            source.exits.append(entrance)
            entrance.connect(target)

        # Sum locations for items creation
        self.location_count = len(self.multiworld.get_locations(self.player))

    def completion_rule(self, state: CollectionState):
        goal_levels = Maps.map_names
        if self.options.goal.value:
            goal_levels = self.boss_level_for_espidoes

        for map_name in goal_levels:
            if map_name + " - Exit" not in self.location_name_to_id:
                continue
            
            # Exit location names are in form: Hangar (E1M1) - Exit
            loc = Locations.location_table[self.location_name_to_id[map_name + " - Exit"]]
            if not self.included_episodes[loc["episode"] - 1]:
                continue

            # Map complete item names are in form: Hangar (E1M1) - Complete
            if not state.has(map_name + " - Complete", self.player, 1):
                return False
            
        return True

    def set_rules(self):
        pro = self.options.pro.value
        allow_death_logic = self.options.allow_death_logic.value

        Rules.set_rules(self, self.included_episodes, pro)
        self.multiworld.completion_condition[self.player] = lambda state: self.completion_rule(state)

        # Forbid progression items to locations that can be missed and can't be picked up. (e.g. One-time timed
        # platform) Unless the user allows for it.
        if not allow_death_logic:
            for death_logic_location in Locations.death_logic_locations:
                self.options.exclude_locations.value.add(death_logic_location)
    
    def create_item(self, name: str) -> DOOM1993Item:
        item_id: int = self.item_name_to_id[name]
        return DOOM1993Item(name, Items.item_table[item_id]["classification"], item_id, self.player)

    def create_items(self):
        itempool: List[DOOM1993Item] = []
        start_with_computer_area_maps: bool = self.options.start_with_computer_area_maps.value

        # Items
        for item_id, item in Items.item_table.items():
            if item["doom_type"] == DOOM_TYPE_LEVEL_COMPLETE:
                continue # We'll fill it manually later

            if item["doom_type"] == DOOM_TYPE_COMPUTER_AREA_MAP and start_with_computer_area_maps:
                continue # We'll fill it manually, and we will put fillers in place

            if item["episode"] != -1 and not self.included_episodes[item["episode"] - 1]:
                continue

            count = item["count"] if item["name"] not in self.starting_level_for_episode else item["count"] - 1
            itempool += [self.create_item(item["name"]) for _ in range(count)]

        # Place end level items in locked locations
        for map_name in Maps.map_names:
            loc_name = map_name + " - Exit"
            item_name = map_name + " - Complete"

            if loc_name not in self.location_name_to_id:
                continue

            if item_name not in self.item_name_to_id:
                continue

            loc = Locations.location_table[self.location_name_to_id[loc_name]]
            if not self.included_episodes[loc["episode"] - 1]:
                continue

            self.multiworld.get_location(loc_name, self.player).place_locked_item(self.create_item(item_name))
            self.location_count -= 1

        # Give starting levels right away
        for i in range(len(self.included_episodes)):
            if self.included_episodes[i]:
                self.multiworld.push_precollected(self.create_item(self.starting_level_for_episode[i]))
        
        # Give Computer area maps if option selected
        if self.options.start_with_computer_area_maps.value:
            for item_id, item_dict in Items.item_table.items():
                item_episode = item_dict["episode"]
                if item_episode > 0:
                    if item_dict["doom_type"] == DOOM_TYPE_COMPUTER_AREA_MAP and self.included_episodes[item_episode - 1]:
                        self.multiworld.push_precollected(self.create_item(item_dict["name"]))

        # Fill the rest starting with powerups, then fillers
        self.create_ratioed_items("Armor", itempool)
        self.create_ratioed_items("Mega Armor", itempool)
        self.create_ratioed_items("Berserk", itempool)
        self.create_ratioed_items("Invulnerability", itempool)
        self.create_ratioed_items("Partial invisibility", itempool)
        self.create_ratioed_items("Supercharge", itempool)

        while len(itempool) < self.location_count:
            itempool.append(self.create_item(self.get_filler_item_name()))

        # add itempool to multiworld
        self.multiworld.itempool += itempool

    def get_filler_item_name(self):
        return self.multiworld.random.choice([
            "Medikit",
            "Box of bullets",
            "Box of rockets",
            "Box of shotgun shells",
            "Energy cell pack"
        ])

    def create_ratioed_items(self, item_name: str, itempool: List[DOOM1993Item]):
        remaining_loc = self.location_count - len(itempool)
        ep_count = self.get_episode_count()

        # Was balanced for 3 episodes (We added 4th episode, but keep same ratio)
        count = min(remaining_loc, max(1, int(round(self.items_ratio[item_name] * ep_count / 3))))
        if count == 0:
            logger.warning("Warning, no ", item_name, " will be placed.")
            return

        for i in range(count):
            itempool.append(self.create_item(item_name))

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict("goal", "difficulty", "random_monsters", "random_pickups", "random_music", "flip_levels", "allow_death_logic", "pro", "start_with_computer_area_maps", "death_link", "reset_level_on_death", "episode1", "episode2", "episode3", "episode4")

        # E2M6 and E3M9 each have one way keydoor. You can enter, but required the keycard to get out.
        # We used to force place the keycard behind those doors. Limiting the randomness for those items. A change
        # was made to make those specific doors 2-ways keydoors. So the keycards are not shuffled in the pool like the
        # rest. The client needs to know about this so it can modify the door. If the multiworld was generated with
        # an older version, the player would end up stuck.
        slot_data["two_ways_keydoors"] = True

        return slot_data

import functools
import logging
from typing import Any, Dict, List, Set

from BaseClasses import Entrance, CollectionState, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from . import Items, Locations, Maps, Options, Regions, Rules

logger = logging.getLogger("Heretic")

HERETIC_TYPE_LEVEL_COMPLETE = -2
HERETIC_TYPE_MAP_SCROLL = 35


class HereticLocation(Location):
    game: str = "Heretic"


class HereticItem(Item):
    game: str = "Heretic"


class HereticWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Heretic randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Daivuk"]
    )]
    theme = "dirt"


class HereticWorld(World):
    """
    Heretic is a dark fantasy first-person shooter video game released in December 1994. It was developed by Raven Software.
    """
    option_definitions = Options.options
    game = "Heretic"
    web = HereticWeb()
    data_version = 3
    required_client_version = (0, 3, 9)

    item_name_to_id = {data["name"]: item_id for item_id, data in Items.item_table.items()}
    item_name_groups = Items.item_name_groups

    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    location_name_groups = Locations.location_name_groups

    starting_level_for_episode: List[str] = [
        "The Docks (E1M1)",
        "The Crater (E2M1)",
        "The Storehouse (E3M1)",
        "Catafalque (E4M1)",
        "Ochre Cliffs (E5M1)"
    ]

    boss_level_for_espidoes: List[str] = [
        "Hell's Maw (E1M8)",
        "The Portals of Chaos (E2M8)",
        "D'Sparil'S Keep (E3M8)",
        "Shattered Bridge (E4M8)",
        "Field of Judgement (E5M8)"
    ]

    # Item ratio that scales depending on episode count. These are the ratio for 1 episode.
    items_ratio: Dict[str, float] = {
        "Timebomb of the Ancients": 16,
        "Tome of Power": 16,
        "Silver Shield": 10,
        "Enchanted Shield": 5,
        "Morph Ovum": 3,
        "Mystic Urn": 2,
        "Chaos Device": 1,
        "Ring of Invincibility": 1,
        "Shadowsphere": 1
    }

    def __init__(self, world: MultiWorld, player: int):
        self.included_episodes = [1, 1, 1, 0, 0]
        self.location_count = 0

        super().__init__(world, player)

    def get_episode_count(self):
        return functools.reduce(lambda count, episode: count + episode, self.included_episodes)

    def generate_early(self):
        # Cache which episodes are included
        for i in range(5):
            self.included_episodes[i] = getattr(self.multiworld, f"episode{i + 1}")[self.player].value

        # If no episodes selected, select Episode 1
        if self.get_episode_count() == 0:
            self.included_episodes[0] = 1

    def create_regions(self):
        pro = getattr(self.multiworld, "pro")[self.player].value
        check_sanity = getattr(self.multiworld, "check_sanity")[self.player].value

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
                if loc["region"] == region_name and (not loc["check_sanity"] or check_sanity)
            }, HereticLocation)

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
        if getattr(self.multiworld, "goal")[self.player].value:
            goal_levels = self.boss_level_for_espidoes

        for map_name in goal_levels:
            if map_name + " - Exit" not in self.location_name_to_id:
                continue
            
            # Exit location names are in form: The Docks (E1M1) - Exit
            loc = Locations.location_table[self.location_name_to_id[map_name + " - Exit"]]
            if not self.included_episodes[loc["episode"] - 1]:
                continue

            # Map complete item names are in form: The Docks (E1M1) - Complete
            if not state.has(map_name + " - Complete", self.player, 1):
                return False
            
        return True

    def set_rules(self):
        pro = getattr(self.multiworld, "pro")[self.player].value
        allow_death_logic = getattr(self.multiworld, "allow_death_logic")[self.player].value

        Rules.set_rules(self, self.included_episodes, pro)
        self.multiworld.completion_condition[self.player] = lambda state: self.completion_rule(state)

        # Forbid progression items to locations that can be missed and can't be picked up. (e.g. One-time timed
        # platform) Unless the user allows for it.
        if not allow_death_logic:
            for death_logic_location in Locations.death_logic_locations:
                self.multiworld.exclude_locations[self.player].value.add(death_logic_location)
    
    def create_item(self, name: str) -> HereticItem:
        item_id: int = self.item_name_to_id[name]
        return HereticItem(name, Items.item_table[item_id]["classification"], item_id, self.player)

    def create_items(self):
        itempool: List[HereticItem] = []
        start_with_map_scrolls: bool = getattr(self.multiworld, "start_with_map_scrolls")[self.player].value

        # Items
        for item_id, item in Items.item_table.items():
            if item["doom_type"] == HERETIC_TYPE_LEVEL_COMPLETE:
                continue # We'll fill it manually later

            if item["doom_type"] == HERETIC_TYPE_MAP_SCROLL and start_with_map_scrolls:
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
        if getattr(self.multiworld, "start_with_map_scrolls")[self.player].value:
            for item_id, item_dict in Items.item_table.items():
                item_episode = item_dict["episode"]
                if item_episode > 0:
                    if item_dict["doom_type"] == HERETIC_TYPE_MAP_SCROLL and self.included_episodes[item_episode - 1]:
                        self.multiworld.push_precollected(self.create_item(item_dict["name"]))

        # Fill the rest starting with powerups, then fillers
        self.create_ratioed_items("Chaos Device", itempool)
        self.create_ratioed_items("Morph Ovum", itempool)
        self.create_ratioed_items("Mystic Urn", itempool)
        self.create_ratioed_items("Ring of Invincibility", itempool)
        self.create_ratioed_items("Shadowsphere", itempool)
        self.create_ratioed_items("Timebomb of the Ancients", itempool)
        self.create_ratioed_items("Tome of Power", itempool)
        self.create_ratioed_items("Silver Shield", itempool)
        self.create_ratioed_items("Enchanted Shield", itempool)

        while len(itempool) < self.location_count:
            itempool.append(self.create_item(self.get_filler_item_name()))

        # add itempool to multiworld
        self.multiworld.itempool += itempool

    def get_filler_item_name(self):
        return self.multiworld.random.choice([
            "Quartz Flask",
            "Crystal Geode",
            "Energy Orb",
            "Greater Runes",
            "Inferno Orb",
            "Pile of Mace Spheres",
            "Quiver of Ethereal Arrows"
        ])

    def create_ratioed_items(self, item_name: str, itempool: List[HereticItem]):
        remaining_loc = self.location_count - len(itempool)
        if remaining_loc <= 0:
            return

        episode_count = self.get_episode_count()
        count = min(remaining_loc, max(1, self.items_ratio[item_name] * episode_count))
        if count == 0:
            logger.warning("Warning, no " + item_name + " will be placed.")
            return

        for i in range(count):
            itempool.append(self.create_item(item_name))

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict("difficulty", "random_monsters", "random_pickups", "random_music", "allow_death_logic", "pro", "death_link", "reset_level_on_death", "check_sanity")

        # Make sure we send proper episode settings
        slot_data["episode1"] = self.included_episodes[0]
        slot_data["episode2"] = self.included_episodes[1]
        slot_data["episode3"] = self.included_episodes[2]
        slot_data["episode4"] = self.included_episodes[3]
        slot_data["episode5"] = self.included_episodes[4]

        return slot_data

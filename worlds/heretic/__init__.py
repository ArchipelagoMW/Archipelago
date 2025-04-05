import functools
import logging
from typing import Any, Dict, List, Set

from BaseClasses import Entrance, CollectionState, Item, Location, MultiWorld, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from . import Items, Locations, Maps, Regions, Rules
from .Options import HereticOptions

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
    options_dataclass = HereticOptions
    options: HereticOptions
    game = "Heretic"
    web = HereticWeb()
    required_client_version = (0, 5, 0)  # 1.2.0-prerelease or higher

    item_name_to_id = {data["name"]: item_id for item_id, data in Items.item_table.items()}
    item_name_groups = Items.item_name_groups

    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    location_name_groups = Locations.location_name_groups

    starting_level_for_episode: Dict[int, str] = {
        1: "The Docks (E1M1)",
        2: "The Crater (E2M1)",
        3: "The Storehouse (E3M1)",
        4: "Catafalque (E4M1)",
        5: "Ochre Cliffs (E5M1)"
    }

    all_boss_levels: List[str] = [
        "Hell's Maw (E1M8)",
        "The Portals of Chaos (E2M8)",
        "D'Sparil's Keep (E3M8)",
        "Shattered Bridge (E4M8)",
        "Field of Judgement (E5M8)"
    ]

    # Item ratio that scales depending on episode count. These are the ratio for 1 episode.
    items_ratio: Dict[str, float] = {
        "Timebomb of the Ancients": 16,
        "Tome of Power": 16,
        "Silver Shield": 10,
        "Enchanted Shield": 5,
        "Torch": 5,
        "Morph Ovum": 3,
        "Mystic Urn": 2,
        "Chaos Device": 1,
        "Ring of Invincibility": 1,
        "Shadowsphere": 1
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        self.included_episodes = [1, 1, 1, 0, 0]
        self.location_count = 0
        self.starting_levels = []

        super().__init__(multiworld, player)

    def get_episode_count(self):
        return functools.reduce(lambda count, episode: count + episode, self.included_episodes)

    def generate_early(self):
        # Cache which episodes are included
        self.included_episodes[0] = self.options.episode1.value
        self.included_episodes[1] = self.options.episode2.value
        self.included_episodes[2] = self.options.episode3.value
        self.included_episodes[3] = self.options.episode4.value
        self.included_episodes[4] = self.options.episode5.value

        # If no episodes selected, select Episode 1
        if self.get_episode_count() == 0:
            self.included_episodes[0] = 1

        self.starting_levels = [level_name for (episode, level_name) in self.starting_level_for_episode.items()
                                if self.included_episodes[episode - 1]]

        # For Solo Episode 1, place the Yellow Key for E1M1 early.
        # Gives the generator five potential placements (plus the forced key) instead of only two.
        if self.get_episode_count() == 1 and self.included_episodes[0]:
            self.multiworld.early_items[self.player]["The Docks (E1M1) - Yellow key"] = 1

    def create_regions(self):
        pro = self.options.pro.value
        check_sanity = self.options.check_sanity.value

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
        if self.options.goal.value:
            goal_levels = self.all_boss_levels

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
        pro = self.options.pro.value
        allow_death_logic = self.options.allow_death_logic.value

        Rules.set_rules(self, self.included_episodes, pro)
        self.multiworld.completion_condition[self.player] = lambda state: self.completion_rule(state)

        # Forbid progression items to locations that can be missed and can't be picked up. (e.g. One-time timed
        # platform) Unless the user allows for it.
        if not allow_death_logic:
            for death_logic_location in Locations.death_logic_locations:
                self.options.exclude_locations.value.add(death_logic_location)
    
    def create_item(self, name: str) -> HereticItem:
        item_id: int = self.item_name_to_id[name]
        return HereticItem(name, Items.item_table[item_id]["classification"], item_id, self.player)

    def create_items(self):
        itempool: List[HereticItem] = []
        start_with_map_scrolls: bool = self.options.start_with_map_scrolls.value

        # Items
        for item_id, item in Items.item_table.items():
            if item["doom_type"] == HERETIC_TYPE_LEVEL_COMPLETE:
                continue # We'll fill it manually later

            if item["doom_type"] == HERETIC_TYPE_MAP_SCROLL and start_with_map_scrolls:
                continue # We'll fill it manually, and we will put fillers in place

            if item["episode"] != -1 and not self.included_episodes[item["episode"] - 1]:
                continue

            count = item["count"] if item["name"] not in self.starting_levels else item["count"] - 1
            itempool += [self.create_item(item["name"]) for _ in range(count)]

        # Bag(s) of Holding based on options
        if self.options.split_bag_of_holding.value:
            itempool += [self.create_item("Crystal Capacity") for _ in range(self.options.bag_of_holding_count.value)]
            itempool += [self.create_item("Ethereal Arrow Capacity") for _ in range(self.options.bag_of_holding_count.value)]
            itempool += [self.create_item("Claw Orb Capacity") for _ in range(self.options.bag_of_holding_count.value)]
            itempool += [self.create_item("Rune Capacity") for _ in range(self.options.bag_of_holding_count.value)]
            itempool += [self.create_item("Flame Orb Capacity") for _ in range(self.options.bag_of_holding_count.value)]
            itempool += [self.create_item("Mace Sphere Capacity") for _ in range(self.options.bag_of_holding_count.value)]
        else:
            itempool += [self.create_item("Bag of Holding") for _ in range(self.options.bag_of_holding_count.value)]

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
        for map_name in self.starting_levels:
            self.multiworld.push_precollected(self.create_item(map_name))
        
        # Give Computer area maps if option selected
        if self.options.start_with_map_scrolls.value:
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
        self.create_ratioed_items("Torch", itempool)
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
            logger.warning(f"Warning, no {item_name} will be placed.")
            return

        for i in range(count):
            itempool.append(self.create_item(item_name))

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict("goal", "difficulty", "random_monsters", "random_pickups", "random_music", "allow_death_logic", "pro", "death_link", "reset_level_on_death", "check_sanity")

        # Make sure we send proper episode settings
        slot_data["episode1"] = self.included_episodes[0]
        slot_data["episode2"] = self.included_episodes[1]
        slot_data["episode3"] = self.included_episodes[2]
        slot_data["episode4"] = self.included_episodes[3]
        slot_data["episode5"] = self.included_episodes[4]

        # Send slot data for ammo capacity values; this must be generic because Doom uses it too
        slot_data["ammo1start"] = self.options.max_ammo_crystals.value
        slot_data["ammo2start"] = self.options.max_ammo_arrows.value
        slot_data["ammo3start"] = self.options.max_ammo_claw_orbs.value
        slot_data["ammo4start"] = self.options.max_ammo_runes.value
        slot_data["ammo5start"] = self.options.max_ammo_flame_orbs.value
        slot_data["ammo6start"] = self.options.max_ammo_spheres.value
        slot_data["ammo1add"] = self.options.added_ammo_crystals.value
        slot_data["ammo2add"] = self.options.added_ammo_arrows.value
        slot_data["ammo3add"] = self.options.added_ammo_claw_orbs.value
        slot_data["ammo4add"] = self.options.added_ammo_runes.value
        slot_data["ammo5add"] = self.options.added_ammo_flame_orbs.value
        slot_data["ammo6add"] = self.options.added_ammo_spheres.value

        return slot_data

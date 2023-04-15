from __future__ import annotations

import logging
from typing import List, Dict, Any, Set

from BaseClasses import LocationProgressType, Region, Entrance, Location, Item, Tutorial, ItemClassification, MultiWorld
from worlds.AutoWorld import World, WebWorld

from . import Items, Locations, Options, Rules, Events, Regions


logger = logging.getLogger("DOOM 1993")


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
    Developed by id Software, and originally released in 1993, DOOM pioneered and popularized the first-person shooter, setting a standard for all FPS games.
    """
    option_definitions = Options.options
    game = "DOOM 1993"
    web = DOOM1993Web()
    data_version = 1
    required_client_version = (0, 3, 9)

    item_name_to_id = {data["name"]: item_id for item_id, data in Items.item_table.items()}
    item_name_groups = Items.item_name_groups

    location_name_to_id = {data["name"]: loc_id for loc_id, data in Locations.location_table.items()}
    location_name_groups = Locations.location_name_groups

    starting_level_for_episode:List(str) = [
        'Hangar (E1M1)',
        'Deimos Anomaly (E2M1)',
        'Hell Keep (E3M1)'
    ]

    # Item ratio that scales depending on episode count. These are the ratio for 3 episode.
    items_ratio:Dict(str, float) = {
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


    def __init__(self, world: MultiWorld, player: int):
        self.included_episodes = [1, 1, 1]
        self.location_count = 0
        self.item_count = 0

        super().__init__(world, player)
    

    def get_episode_count(self):
        count = 0
        for ep in self.included_episodes:
            if ep:
                count +=1
        return count
    

    def generate_early(self):
        # Cache which episodes are included
        for i in range(0, 3):
            self.included_episodes[i] = getattr(self.multiworld, "episode" + str(i + 1))[self.player].value

        # If no episodes selected, select Episode 1
        if self.get_episode_count() == 0:
            self.included_episodes[0] = 1


    def create_regions(self):
        # Main regions
        self.multiworld.regions.append(Region("Menu", self.player, self.multiworld))
        self.multiworld.regions.append(Region("Mars", self.player, self.multiworld))

        # Maps' regions
        for region_name in Regions.regions:
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))
        
        # Add locations to regions
        for loc_id in Locations.location_table:
            loc = Locations.location_table[loc_id]
            if not self.included_episodes[loc["episode"] - 1]:
                continue
            if loc["index"] == -1:
                loc_id = None
            self.create_location(loc_id, loc, self.multiworld.get_region(loc["region"], self.player))
            self.location_count += 1
        
        # Create exits
        self.multiworld.get_region("Menu", self.player).exits.append(Entrance(self.player, "Menu -> Mars", self.multiworld.get_region("Menu", self.player)))
        self.multiworld.get_entrance("Menu -> Mars", self.player).connect(self.multiworld.get_region("Mars", self.player))

        # Rest of regions
        for region_name in Regions.regions:
            self.create_2way_exit("Mars", region_name)


    def create_2way_exit(self, region1_name, region2_name):
        region1 = self.multiworld.get_region(region1_name, self.player)
        region2 = self.multiworld.get_region(region2_name, self.player)

        entrance1 = Entrance(self.player, region1_name + " -> " + region2_name, region1)
        entrance2 = Entrance(self.player, region2_name + " -> " + region1_name, region2)

        region1.exits.append(entrance1)
        region2.exits.append(entrance2)

        entrance1.connect(region2)
        entrance2.connect(region1)


    def completion_rule(self, state):
        for event in Events.events:
            if not (event in self.location_name_to_id):
                continue
            loc = Locations.location_table[self.location_name_to_id[event]]
            if not self.included_episodes[loc["episode"] - 1]:
                continue
            if not state.has(event, self.player, 1):
                return False
        return True


    def set_rules(self):
        Rules.set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: self.completion_rule(state)
    
    
    def create_item(self, name: str) -> DOOM1993Item:
        item_id: int = self.item_name_to_id[name]
        doom_1993_item = DOOM1993Item(name, Items.item_table[item_id]["classification"], item_id, player=self.player)
        return doom_1993_item
    
    
    def create_item_with_classification(self, name: str, classification: ItemClassification) -> DOOM1993Item:
        item_id: int = self.item_name_to_id[name]
        doom_1993_item = DOOM1993Item(name, classification, item_id, player=self.player)
        return doom_1993_item
    

    def place_locked_item_in_locations(self, item_name, locations):
        location = self.multiworld.random.choice(locations)
        self.multiworld.get_location(location, self.player).place_locked_item(self.create_item(item_name))
        self.location_count -= 1


    def create_items(self):
        is_only_first_episode = self.get_episode_count() == 1 and self.included_episodes[0]

        # Items
        for item_id, item in Items.item_table.items():
            if item["episode"] != -1 and not self.included_episodes[item["episode"] - 1]:
                continue
            if (item["name"] == "BFG9000" or item["name"] == "Plasma Gun") and is_only_first_episode:
                continue # Don't include those guns in first episode
            count = item["count"]
            if str(item["name"]) in self.starting_level_for_episode:
                count -= 1
            for i in range(0, count):
                classification = item["classification"]
                doom_1993_item = self.create_item_with_classification(item["name"], classification)
                # See create_regions
                if item["name"] != "Warrens (E3M9) - Blue skull key" and \
                   item["name"] != "Halls of the Damned (E2M6) - Yellow skull key":
                    self.multiworld.itempool += [doom_1993_item]
                    self.item_count += 1

        # Place end level items in locked locations
        for event in Events.events:
            if not event in self.location_name_to_id:
                continue
            loc = Locations.location_table[self.location_name_to_id[event]]
            if not self.included_episodes[loc["episode"] - 1]:
                continue
            self.multiworld.get_location(event, self.player).place_locked_item(
                DOOM1993Item(event, ItemClassification.progression, None, player=self.player))
            self.location_count -= 1
    
        # Special case for E2M6 and E3M8, where you enter a normal door then get stuck behind with a key door.
        # We need to put the key in the locations available behind this door.
        if self.included_episodes[1]:
            self.place_locked_item_in_locations("Halls of the Damned (E2M6) - Yellow skull key", [
                "Halls of the Damned (E2M6) - Yellow skull key",
                "Halls of the Damned (E2M6) - Partial invisibility 2"
            ])
        if self.included_episodes[2]:
            self.place_locked_item_in_locations("Warrens (E3M9) - Blue skull key", [
                "Warrens (E3M9) - Rocket launcher",
                "Warrens (E3M9) - Rocket launcher 2",
                "Warrens (E3M9) - Partial invisibility",
                "Warrens (E3M9) - Invulnerability",
                "Warrens (E3M9) - Supercharge",
                "Warrens (E3M9) - Berserk",
                "Warrens (E3M9) - Chaingun"
            ])

        # Give starting levels right away
        for i in range(len(self.included_episodes)):
            if self.included_episodes[i]:
                self.multiworld.push_precollected(self.create_item(self.starting_level_for_episode[i]))

        # Fill the rest starting with weapons, powerups then fillers
        self.create_ratioed_items("Armor")
        self.create_ratioed_items("Mega Armor")
        self.create_ratioed_items("Berserk")
        self.create_ratioed_items("Invulnerability")
        self.create_ratioed_items("Partial invisibility")
        self.create_ratioed_items("Supercharge")

        remaining_loc = self.location_count - self.item_count
        fillers = [
            "Medikit",
            "Box of bullets",
            "Box of rockets",
            "Box of shotgun shells",
            "Energy cell pack"
        ]
        while remaining_loc > 0:
            remaining_loc -= 1
            item = self.create_item_with_classification(self.multiworld.random.choice(fillers), ItemClassification.filler)
            self.multiworld.itempool.append(item)
            self.item_count += 1


    def create_ratioed_items(self, item_name):
        remaining_loc = self.location_count - self.item_count
        ep_count = self.get_episode_count()
        count = min(remaining_loc, max(1, int(round(self.items_ratio[item_name] * ep_count / 3)))) # Was balanced for 3 episodes
        if count == 0:
            logger.warning("Warning, no ", item_name, " will be placed.")
        for i in range(count):
            classification = Items.item_table[self.item_name_to_id[item_name]]['classification']
            item = self.create_item_with_classification(item_name, classification)
            self.multiworld.itempool.append(item)
            self.item_count += 1


    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {}

        for option_name in self.option_definitions:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data


    def create_location(self, loc_id, loc, region):
        loc_name = loc["name"]
        doom1993_location = DOOM1993Location(self.player, loc_name, loc_id, region)

        # Forbid progression items to locations that can be missed and can't be picked up. (e.g. One-time timed platform)
        # Unless the user allows for it.
        if not getattr(self.multiworld, "allow_death_logic")[self.player].value and loc_name in Locations.death_logic_locations:
            doom1993_location.progress_type = LocationProgressType.EXCLUDED

        region.locations.append(doom1993_location)

"""
Archipelago init file for Pokepark
"""
import os
import zipfile
from base64 import b64encode
from typing import Any

import yaml

from BaseClasses import ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
from .items import FRIENDSHIP_ITEMS, PokeparkItem, UNLOCK_ITEMS, BERRIES, ALL_ITEMS_TABLE, PRISM_ITEM, POWERS, \
    REGION_UNLOCK, VICTORY
from .locations import ALL_LOCATIONS_TABLE, REGIONS
from .options import PokeparkOptions, pokepark_option_groups
from ..Files import APPlayerContainer


class PokeparkWebWorld(WebWorld):
    theme = "jungle"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Pokepark Randomizer software on your computer."
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        [""]
    )]
    options_presets = {
        "Default": {
            "power_randomizer": 3,
            "starting_zone": 0,
            "goal": 0
        }
    }
    option_groups = pokepark_option_groups


class PokeparkContainer(APPlayerContainer):
    """
    This class defines the container file for The Wind Waker.
    """

    game: str = "PokePark"
    patch_file_ending: str = ".appkprk"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "data" in kwargs:
            self.data = kwargs["data"]
            del kwargs["data"]

        super().__init__(*args, **kwargs)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        """
        Write the contents of the container file.
        """
        super().write_contents(opened_zipfile)

        # Record the data for the game under the key `plando`.
        opened_zipfile.writestr("plando", b64encode(bytes(yaml.safe_dump(self.data, sort_keys=False), "utf-8")))


class PokeparkWorld(World):
    """
    The first Pokepark game featuring 3D Gameplay controlling Pokemon.
    Lot of Minigames in the mission to save the Pokepark through the collection of Prism Shards.
    """
    game = "PokePark"

    options_dataclass = PokeparkOptions
    options: PokeparkOptions

    web = PokeparkWebWorld()

    item_name_to_id = ALL_ITEMS_TABLE
    location_name_to_id = ALL_LOCATIONS_TABLE
    location_name_groups = {
        "Friendship Locations": [f"{region.display} - {friendship.name}" for region in REGIONS
                                 for friendship in
                                 region.friendship_locations],
        "Unlock Locations": [f"{region.display} - {unlock.name}" for region in REGIONS for unlock
                             in
                             region.unlock_location],
        "Minigame Locations": [f"{region.display} - {minigame.name}" for region in REGIONS for
                               minigame in
                               region.minigame_location],
        "Quest Locations": [f"{region.display} - {ability.name}" for region in REGIONS for
                            ability in
                            region.quest_locations]
    }
    item_name_groups = {
        "Friendship Items": FRIENDSHIP_ITEMS.keys(),
        "Unlock Items": UNLOCK_ITEMS.keys(),
        "Currency Items": BERRIES.keys(),
        "Prisma Items": PRISM_ITEM.keys(),
        "Ability Items": POWERS.keys(),
        "Entrance Items": REGION_UNLOCK.keys()
    }

    data_version = 1

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output Pokeprk file that is used to randomize the ISO.

        :param output_directory: The output directory for the Pokeprk file.
        """
        multiworld = self.multiworld
        player = self.player

        # Output seed name and slot number to seed RNG in randomizer client.
        output_data = {
            "Seed": multiworld.seed_name,
            "Slot": player,
            "Name": self.player_name,
            "Options": self.options.get_output_dict(),
            "Locations": {},
            "Entrances": {},
        }

        # Output the plando details to file.
        aptww = PokeparkContainer(
            path=os.path.join(
                output_directory, f"{multiworld.get_out_file_name_base(player)}{PokeparkContainer.patch_file_ending}"
            ),
            player=player,
            player_name=self.player_name,
            data=output_data,
        )
        aptww.write()

    def create_regions(self):
        from .regions import create_regions
        create_regions(self)

    def create_items(self):
        pool = []

        # Handle power items
        self._handle_power_items(pool)

        # Handle starting zones
        self._handle_starting_zones(pool)

        # Add standard items
        self._add_standard_items(pool)

        # Fill remaining slots with berries
        self._fill_remaining_slots_with_berries(pool)

        # Add all items to the item pool
        self.multiworld.itempool.extend(pool)

    def _handle_power_items(self, pool):
        """Manages power items based on randomizer options."""
        # For "option_full", all power items are pre-collected
        if self.options.power_randomizer == self.options.power_randomizer.option_full:
            for name in POWERS.keys():
                for _ in range(3):
                    self.multiworld.push_precollected(self.create_item(name))
            self.multiworld.push_precollected(self.create_item("Progressive Thunderbolt"))
            self.multiworld.push_precollected(self.create_item("Progressive Dash"))
            return

        # Add power items to the pool
        for name in POWERS.keys():
            for _ in range(3):
                pool.append(self.create_item(name))

        # Define which special power items are pre-collected
        precollect_mapping = {
            self.options.power_randomizer.option_thunderbolt: ["Progressive Thunderbolt"],
            self.options.power_randomizer.option_dash: ["Progressive Dash"],
            self.options.power_randomizer.option_thunderbolt_dash: ["Progressive Thunderbolt", "Progressive Dash"]
        }

        # Current selected option
        current_option = self.options.power_randomizer

        # Handle Progressive Thunderbolt and Dash
        for power_name in ["Progressive Thunderbolt", "Progressive Dash"]:
            if current_option in precollect_mapping and power_name in precollect_mapping[current_option]:
                self.multiworld.push_precollected(self.create_item(power_name))
            else:
                pool.append(self.create_item(power_name))

    def _handle_starting_zones(self, pool):
        """Manages starting zones based on selected options."""

    def _add_standard_items(self, pool):
        """Adds standard item categories to the pool."""
        # Items excluded from normal unlocks
        unlock_item_exception = []

        pool.extend([self.create_item(name) for name in FRIENDSHIP_ITEMS.keys()])
        pool.extend([self.create_item(name) for name in UNLOCK_ITEMS.keys()
                     if name not in unlock_item_exception])
        pool.extend([self.create_item(name) for name in PRISM_ITEM.keys()])
        pool.extend([self.create_item(name) for name in REGION_UNLOCK.keys()])

    def _fill_remaining_slots_with_berries(self, pool):
        """Fills remaining slots with berry items."""
        remaining_slots = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)
        berry_items = list(BERRIES.keys())

        for i in range(remaining_slots):
            berry_name = berry_items[i % len(berry_items)]
            pool.append(self.create_item(berry_name))

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_item(self, name: str):
        if name.__contains__("Bidoof Unlock"):
            classification = ItemClassification.filler
        elif name in FRIENDSHIP_ITEMS or name in UNLOCK_ITEMS or name in PRISM_ITEM or name in REGION_UNLOCK or name in POWERS or name in VICTORY:
            classification = ItemClassification.progression
        elif name in BERRIES:
            classification = ItemClassification.filler
        else:
            classification = ItemClassification.filler

        return PokeparkItem(name, classification, ALL_ITEMS_TABLE[name], self.player)


def launch_client():
    from .PokeparkClient import main
    launch_component(main, name="Pokepark client")


components.append(Component("Pokepark Client", "PokeparkClient",
                            func=launch_client, component_type=Type.CLIENT))

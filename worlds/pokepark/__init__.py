"""
Archipelago init file for Pokepark
"""
import os
import zipfile
from base64 import b64encode
from typing import Any, ClassVar, Callable

import yaml

from BaseClasses import Tutorial, Region, CollectionState
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch as launch_component
from .items import item_name_groups, PokeparkItem, ITEM_TABLE
from .locations import LOCATION_TABLE, PokeparkLocation, PokeparkFlag
from .options import PokeparkOptions, pokepark_option_groups
from .regions import VANILLA_ENTRANCES_TO_EXITS, REGION_TO_ENTRANCES
from .rules import set_rules
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

    item_name_to_id: ClassVar[dict[str, int]] = {
        name: PokeparkItem.get_apid(data.code) for name, data in ITEM_TABLE.items() if data.code is not None
    }
    location_name_to_id = {
        name: PokeparkItem.get_apid(data.code) for name, data in LOCATION_TABLE.items() if data.code is not None
    }
    origin_region_name: str = "Treehouse"

    item_name_groups: ClassVar[dict[str, set[str]]] = item_name_groups

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.progress_locations: set[str] = set()
        self.nonprogress_locations: set[str] = set()

    def _determine_progress_and_nonprogress_locations(self) -> tuple[set[str], set[str]]:
        """
        Determine which locations are progress and nonprogress in the world based on the player's options.

        :return: A tuple of two sets, the first containing the names of the progress locations and the second containing
        the names of the nonprogress locations.
        """
        ignore_location: str = ""

        progress_locations: set[str] = set()
        nonprogress_locations: set[str] = set()
        for location, data in LOCATION_TABLE.items():
            if True:
                progress_locations.add(location)
            else:
                nonprogress_locations.add(location)
        assert progress_locations.isdisjoint(nonprogress_locations)

        return progress_locations, nonprogress_locations

    def generate_early(self) -> None:
        options = self.options
        self.progress_locations, self.nonprogress_locations = self._determine_progress_and_nonprogress_locations()

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
        multiworld = self.multiworld
        player = self.player
        options = self.options

        ENTRANCE_RULES: dict[str, Callable[[CollectionState], bool]] = {
            "Treehouse Meadow Zone Gate": lambda state: True,
            "Treehouse Drifblim Fast Travel Meadow Zone": lambda state: state.has("Meadow Zone Fast Travel", player),
            "Meadow Zone Main Area - Bulbasaur's Daring Dash Attraction": lambda state: True,
            "Meadow Zone Main Area - Venusaur's Gate": lambda state: state.has("Bulbasaur Prisma", player),
            "Meadow Zone Venusaur Area - Venusaur's Vine Swing Attraction": lambda state: True,

            "Treehouse Beach Zone Gate": lambda state: state.has("Venusaur Prisma", player),
            "Treehouse Drifblim Fast Travel Beach Zone": lambda state: state.has("Beach Zone Fast Travel", player),
            "Beach Zone Main Area - Pelipper's Circle Circuit Attraction": lambda state: True,
            "Beach Zone Main Area - Gyarado's Aqua Dash Attraction": lambda state: True,

            "Beach Zone Main Area Lapras Travel": lambda state: state.has("Gyarados Prisma", player),
            "Treehouse Drifblim Fast Travel Ice Zone": lambda state: state.has("Ice Zone Fast Travel", player),
            "Ice Zone Main Area Lift": lambda state: state.has("Prinplup Friendship", player),
            "Ice Zone Main Area Empoleon Gate": lambda state: True,
            "Ice Zone Empoleon Area - Empoleon's Snow Slide Attraction": lambda state: True,

            "Treehouse Cavern Zone Gate": lambda state: state.has("Empoleon Prisma", player),
            "Treehouse Drifblim Fast Travel Cavern Zone": lambda state: state.has("Cavern Zone Fast Travel", player),
            "Cavern Zone Main Area - Bastiodon's Panel Crush Attraction": lambda state: state.count_group(
                "Friendship Items",
                player
            ) > 50,

            "Cavern Zone Magma Zone Gate": lambda state: state.has("Bastiodon Prisma", player),
            "Treehouse Drifblim Fast Travel Magma Zone": lambda state: state.has("Magma Zone Fast Travel", player),
            "Magma Zone Main Area - Rhyperior's Bumper Burn Attraction": lambda state: True,
            "Magma Zone Main Area Blaziken Gate": lambda state: state.has("Rhyperior Prisma", player),
            "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction": lambda state: True,

            "Treehouse Haunted Zone Gate": lambda state: state.has("Blaziken Prisma", player),
            "Treehouse Drifblim Fast Travel Haunted Zone": lambda state: state.has("Haunted Zone Fast Travel", player),
            "Haunted Zone Main Area - Tangrowth's Swing-Along Attraction": lambda state: True,
            "Haunted Zone Mansion Entrance": lambda state: state.has("Tangrowth Prisma", player),
            "Haunted Zone Mansion Area - Dusknoir's Speed Slam Attraction": lambda state: state.has(
                "Dusknoir Unlock", player
            ),
            "Haunted Zone Mansion Rotom's Hidden Entrance": lambda state: state.has("Dusknoir Prisma", player),
            "Haunted Zone Rotom Area - Rotom's Spooky Shoot-'em-Up Attraction": lambda state: state.count_group(
                "Friendship Items",
                player
            ) > 65,

            "Treehouse Granite Zone Gate": lambda state: state.has("Rotom Prisma", player),
            "Treehouse Drifblim Fast Travel Granite Zone": lambda state: state.has("Granite Zone Fast Travel", player),
            "Granite Zone Main Area - Absol's Hurdle Bounce Attraction": lambda state: True,
            "Granite Zone Main Area - Salamence's Sky Race Attraction": lambda state: state.count_group(
                "Friendship Items",
                player
            ) > 80,

            "Granite Zone Flower Zone Entrance": lambda state: state.has("Salamence Prisma", player),
            "Treehouse Drifblim Fast Travel Flower Zone": lambda state: state.has("Flower Zone Fast Travel", player),
            "Flower Zone Main Area - Rayquaza's Balloon Panic Attraction": lambda state: state.has(
                "Rayquaza Unlock", player
            ),

            "Treehouse Piplup Air Balloon": lambda state: state.has("Rayquaza Prisma", player),
        }
        treehouse = Region("Treehouse", player, multiworld)
        multiworld.regions.append(treehouse)
        unique_region_names = set(VANILLA_ENTRANCES_TO_EXITS.values())
        for _region_name in unique_region_names:
            multiworld.regions.append(Region(_region_name, player, multiworld))
        for region_map, entrances in REGION_TO_ENTRANCES.items():
            for entrance in entrances:
                target_region_name = VANILLA_ENTRANCES_TO_EXITS.get(entrance)
                target_region = multiworld.get_region(target_region_name, player)
                print(f"{region_map} -> {target_region}")
                multiworld.get_region(region_map, player).connect(
                    target_region
                    , f"{entrance} ->"
                      f" {target_region_name}", ENTRANCE_RULES[entrance]
                )
        for location_name in sorted(self.progress_locations):
            data = LOCATION_TABLE[location_name]

            region = self.get_region(data.region)
            location = PokeparkLocation(player, location_name, region, data)

            region.locations.append(location)

    def set_rules(self) -> None:
        set_rules(self)

    def create_item(self, name: str) -> PokeparkItem:
        if name in ITEM_TABLE:
            return PokeparkItem(name, self.player, ITEM_TABLE[name], ITEM_TABLE[name].classification)
        raise KeyError(f"Invalid item name: {name}")

    def update_pool_with_precollected_items(self) -> tuple[list[str], list[str]]:
        options = self.options
        progressive_pool = []
        precollected_pool = []

        for item_name, data in ITEM_TABLE.items():
            if data.type == "Item":
                progressive_pool.extend([item_name] * data.quantity)

        if options.power_randomizer == options.power_randomizer.option_dash:
            precollected_pool.append("Progressive Dash")
            progressive_pool.remove("Progressive Dash")
        if options.power_randomizer == options.power_randomizer.option_thunderbolt:
            precollected_pool.append("Progressive Thunderbolt")
            progressive_pool.remove("Progressive Thunderbolt")
        if options.power_randomizer == options.power_randomizer.option_thunderbolt_dash:
            precollected_pool.append("Progressive Thunderbolt")
            progressive_pool.remove("Progressive Thunderbolt")
            precollected_pool.append("Progressive Dash")
            progressive_pool.remove("Progressive Dash")
        if options.power_randomizer == options.power_randomizer.option_full:
            for i in range(4):
                precollected_pool.append("Progressive Thunderbolt")
                progressive_pool.remove("Progressive Thunderbolt")
                precollected_pool.append("Progressive Dash")
                progressive_pool.remove("Progressive Dash")
            for i in range(3):
                precollected_pool.append("Progressive Iron Tail")
                progressive_pool.remove("Progressive Iron Tail")
                precollected_pool.append("Progressive Health")
                progressive_pool.remove("Progressive Health")
            precollected_pool.append("Double Dash")
            progressive_pool.remove("Double Dash")

        if options.starting_zone == options.starting_zone.option_ice_zone:
            precollected_pool.append("Ice Zone Fast Travel")
            progressive_pool.remove("Ice Zone Fast Travel")

        if options.starting_zone == options.starting_zone.option_one:
            fast_travel_items = [
                "Meadow Zone Fast Travel",
                "Beach Zone Fast Travel",
                "Ice Zone Fast Travel",
                "Cavern Zone Fast Travel",
                "Magma Zone Fast Travel",
                "Haunted Zone Fast Travel",
                "Granite Zone Fast Travel",
                "Flower Zone Fast Travel",
            ]
            self.random.shuffle(fast_travel_items)
            precollected_fast_travel = self.random.choice(fast_travel_items)
            precollected_pool.append(precollected_fast_travel)
            progressive_pool.remove(precollected_fast_travel)

        return progressive_pool, precollected_pool

    def create_items(self):

        progressive_pool, precollected_pool = self.update_pool_with_precollected_items()

        for item in precollected_pool:
            self.multiworld.push_precollected(self.create_item(item))

        if self.options.goal == self.options.goal.option_mew:
            location = self.get_location("Skygarden - Mew Power Competition -- Friendship")
            location.place_locked_item(
                self.create_item(
                    "Victory"
                )
            )
            location.address = None
        elif self.options.goal == self.options.goal.option_aftergame:
            location = self.get_location("Skygarden - Prisma Completion -- Completed")
            location.place_locked_item(
                self.create_item(
                    "Victory"
                )
            )
            location.address = None

        remaining_slots = len(self.multiworld.get_unfilled_locations(self.player)) - len(progressive_pool)
        for i in range(remaining_slots):
            if i % 20 == 0:
                progressive_pool.append("100 Berries")
            elif i % 8 == 0:
                progressive_pool.append("50 Berries")
            elif i % 4 == 0:
                progressive_pool.append("20 Berries")
            else:
                progressive_pool.append("10 Berries")

        self.random.shuffle(progressive_pool)
        for item in progressive_pool:
            self.multiworld.itempool.append(self.create_item(item))



def launch_client():
    from .PokeparkClient import main
    launch_component(main, name="Pokepark client")


components.append(Component("Pokepark Client", "PokeparkClient",
                            func=launch_client, component_type=Type.CLIENT))

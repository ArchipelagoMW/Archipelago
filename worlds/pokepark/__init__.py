"""
Archipelago init file for Pokepark
"""
import os
import zipfile
from base64 import b64encode
from typing import Any, ClassVar, Dict

import yaml

from BaseClasses import ItemClassification as IC, Region, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components, icon_paths, launch as launch_component
from .items import ITEM_TABLE, PokeparkItem, PokeparkItemData, item_name_groups, option_to_progression
from .locations import LOCATION_TABLE, MultiZoneFlag, PokeparkFlag, PokeparkLocation
from .options import PokeparkOptions, RemoveBattlePowerCompLocations, pokepark_option_groups
from .regions import EntranceRandomizer
from .rules import set_rules
from ..Files import APPlayerContainer

VERSION: tuple[int, int, int] = (1, 0, 0)

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
    topology_present: bool = True

    web = PokeparkWebWorld()
    required_client_version: tuple[int, int, int] = (0, 5, 1)

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

        self.locations: set[str] = set()
        self.progressive_pool: list[str] = list()
        self.useful_pool: list[str] = list()
        self.filler_pool: list[str] = list()
        self.precollected_pool: list[str] = list()
        self.item_classification_overrides: dict[str, IC] = {}
        self.entrances: EntranceRandomizer = EntranceRandomizer(self)

    def _determine_locations(self) -> set[str]:
        """
        Determine which locations included in the world based on the player's options.

        :return: A set containing the names of the locations
        """
        each_zone_filter = MultiZoneFlag.SINGLE if self.options.each_zone == self.options.each_zone.option_true else MultiZoneFlag.MULTI
        removable_location_flags = set()

        flag_options = [
            (PokeparkFlag.BATTLE, self.options.remove_battle_power_comp_locations),
            (PokeparkFlag.CHASE, self.options.remove_chase_power_comp_locations),
            (PokeparkFlag.QUIZ, self.options.remove_quiz_power_comp_locations),
            (PokeparkFlag.HIDEANDSEEK, self.options.remove_hide_and_seek_power_comp_locations),
            (PokeparkFlag.ERRAND, self.options.remove_errand_power_comp_locations),
            (PokeparkFlag.FRIENDSHIP, self.options.remove_misc_power_comp_locations),
            (PokeparkFlag.POWER_UP, self.options.remove_power_training_locations),
            (PokeparkFlag.ATTRACTION, self.options.remove_attraction_locations),
            (PokeparkFlag.ATTRACTION_PRISMA, self.options.remove_attraction_prisma_locations),
            (PokeparkFlag.POKEMON_UNLOCK, self.options.remove_pokemon_unlock_locations)
        ]

        for flag, option in flag_options:
            if option == option.option_true:
                removable_location_flags.add(flag)

        if self.options.goal == self.options.goal.option_mew:
            removable_location_flags.add(PokeparkFlag.POSTGAME)

        locations: set[str] = set()
        for location, data in LOCATION_TABLE.items():
            if (data.each_zone == each_zone_filter or
                    data.flags in removable_location_flags):
                pass
            else:
                locations.add(location)

        return locations

    def generate_early(self) -> None:
        # generate regions and entrances
        self.entrances.generate_entrance_data()

        # setup locations
        self.locations = self._determine_locations()
        for item_name, data in ITEM_TABLE.items():
            if data.type == "Item":
                self.progressive_pool.extend([item_name] * data.quantity)
        self._update_pool_with_precollected_items()

        self._determine_classification_dynamic()
        self._distribute_item_pools()

        if len(self.locations) <= len(self.progressive_pool):
            raise OptionError(
                "Invalid option combination: More progressive items than available locations. "
                "Consider adding more locations."
            )

    def _distribute_item_pools(self):
        filler_items = [name for name in self.progressive_pool
                        if self.item_classification_overrides.get(name) == IC.filler]
        useful_items = [name for name in self.progressive_pool
                        if self.item_classification_overrides.get(name) == IC.useful]
        progression_items = [name for name in self.progressive_pool
                             if self.item_classification_overrides.get(name) == IC.progression]

        self.filler_pool.extend(filler_items)
        self.useful_pool.extend(useful_items)
        self.progressive_pool = progression_items

    def _determine_classification_dynamic(self):
        progressive_items = [
            "Bulbasaur Prisma",
            "Venusaur Prisma",
            "Pelipper Prisma",
            "Gyarados Prisma",
            "Empoleon Prisma",
            "Bastiodon Prisma",
            "Rhyperior Prisma",
            "Blaziken Prisma",
            "Tangrowth Prisma",
            "Dusknoir Prisma",
            "Rotom Prisma",
            "Absol Prisma",
            "Salamence Prisma",
            "Rayquaza Prisma",

            "Beach Zone Fast Travel",
            "Ice Zone Fast Travel",
            "Cavern Zone Fast Travel",
            "Magma Zone Fast Travel",
            "Haunted Zone Fast Travel",
            "Granite Zone Fast Travel",
            "Flower Zone Fast Travel",

            "Beach Bridge 1 Unlock",
            "Beach Bridge 2 Unlock",
            "Magma Zone Fire Wall Unlock",
            "Haunted Zone Mansion Doors Unlock",
            "Ice Zone Lift Unlock",
            "Ice Zone Frozen Lake Unlock",

            "Progressive Dash",
            "Progressive Thunderbolt",
            "Progressive Iron Tail",
            "Progressive Health"
        ]
        useful_items = {
            "Double Dash",
            "Meadow Zone Fast Travel"
        }

        options = self.options
        option_names = [option_name for option_name, _ in option_to_progression.keys()]

        option_dict = options.as_dict(*option_names)
        min_required_friendship_count = 0

        for option, (min_friendship, progression_items) in option_to_progression.items():
            option_name, expected_value = option
            if option_dict.get(option_name) == expected_value:
                min_required_friendship_count = max(min_required_friendship_count, min_friendship)
                progressive_items.extend(progression_items)

        progressive_set = set(progressive_items)
        friendship_removable = []
        other_removable = []

        for name in self.progressive_pool:
            if name not in progressive_set:
                if "Friendship" in name:
                    friendship_removable.append(name)
                else:
                    other_removable.append(name)

        max_removable_friendship = 193 - min_required_friendship_count
        friendship_to_remove = friendship_removable[:max_removable_friendship]

        removable_items = set(friendship_to_remove + other_removable)

        overlap = progressive_set & removable_items
        assert not overlap, f"Items marked as both needed and removable: {overlap}"

        for name, data in ITEM_TABLE.items():
            if data.type != "Item":
                continue

            if name in progressive_set or name not in removable_items:
                self.item_classification_overrides[name] = IC.progression
            else:
                classification = IC.useful if name in useful_items else IC.filler
                self.item_classification_overrides[name] = classification

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output Pokeprk file that is used to randomize the ISO.

        :param output_directory: The output directory for the Pokeprk file.
        """
        multiworld = self.multiworld
        player = self.player

        # Output seed name and slot number to seed RNG in randomizer client.
        output_data = {
            "Version": list(VERSION),
            "Seed": multiworld.seed_name,
            "Slot": player,
            "Name": self.player_name,
            "Options": self.options.get_output_dict(),
            "Locations": {},
            "Entrances": {},
        }

        output_entrances = output_data["Entrances"]
        for zone_entrance, zone_exit in self.entrances.entrances_to_exits.items():
            output_entrances[zone_entrance] = zone_exit

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
        ENTRANCES_TO_EXITS = self.entrances.entrances_to_exits
        REGION_TO_ENTRANCES = self.entrances.region_to_entrances
        ENTRANCE_RULES = self.entrances.entrances_rules
        treehouse = Region("Treehouse", player, multiworld)
        multiworld.regions.append(treehouse)
        unique_region_names = set(ENTRANCES_TO_EXITS.values())
        for _region_name in unique_region_names:
            multiworld.regions.append(Region(_region_name, player, multiworld))
        for region_map, entrances in REGION_TO_ENTRANCES.items():
            for entrance in entrances:
                target_region_name = ENTRANCES_TO_EXITS.get(entrance)
                target_region = multiworld.get_region(target_region_name, player)
                multiworld.get_region(region_map, player).connect(
                    target_region
                    , f"{entrance} ->"
                      f" {target_region_name}", ENTRANCE_RULES[entrance]
                )

        for location_name in sorted(self.locations):
            data = LOCATION_TABLE[location_name]

            region = self.get_region(data.region)
            location = PokeparkLocation(player, location_name, region, data)

            region.locations.append(location)

    def set_rules(self) -> None:
        set_rules(self)

    def create_item(self, name: str) -> PokeparkItem:
        if name in ITEM_TABLE:
            if self.item_classification_overrides.__contains__(name):
                classification = self.item_classification_overrides.get(name)
            else:
                classification = ITEM_TABLE[name].classification
            return PokeparkItem(name, self.player, ITEM_TABLE[name], classification)
        raise KeyError(f"Invalid item name: {name}")

    def _update_pool_with_precollected_items(self):
        options = self.options

        if options.power_randomizer.value == options.power_randomizer.option_dash:
            self.precollected_pool.append("Progressive Dash")
            self.progressive_pool.remove("Progressive Dash")
        if options.power_randomizer.value == options.power_randomizer.option_thunderbolt:
            self.precollected_pool.append("Progressive Thunderbolt")
            self.progressive_pool.remove("Progressive Thunderbolt")

        if options.power_randomizer.value == options.power_randomizer.option_thunderbolt_dash:
            self.precollected_pool.append("Progressive Thunderbolt")
            self.progressive_pool.remove("Progressive Thunderbolt")
            self.precollected_pool.append("Progressive Dash")
            self.progressive_pool.remove("Progressive Dash")
        if options.power_randomizer.value == options.power_randomizer.option_full:
            for i in range(4):
                self.precollected_pool.append("Progressive Thunderbolt")
                self.progressive_pool.remove("Progressive Thunderbolt")
                self.precollected_pool.append("Progressive Dash")
                self.progressive_pool.remove("Progressive Dash")
            for i in range(3):
                self.precollected_pool.append("Progressive Iron Tail")
                self.progressive_pool.remove("Progressive Iron Tail")
                self.precollected_pool.append("Progressive Health")
                self.progressive_pool.remove("Progressive Health")

            self.precollected_pool.append("Double Dash")
            self.progressive_pool.remove("Double Dash")

        if options.starting_zone.value == options.starting_zone.option_one:
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
            self.precollected_pool.append(precollected_fast_travel)
            self.progressive_pool.remove(precollected_fast_travel)

        if options.starting_zone.value == options.starting_zone.option_all:
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
            for item in fast_travel_items:
                self.precollected_pool.append(item)
                self.progressive_pool.remove(item)

        if not options.in_zone_road_blocks.value:
            road_block_items = [
                "Beach Bridge 1 Unlock",
                "Beach Bridge 2 Unlock",
                "Magma Zone Fire Wall Unlock",
                "Haunted Zone Mansion Doors Unlock",
                "Ice Zone Lift Unlock",
                "Ice Zone Frozen Lake Unlock",
            ]
            for item in road_block_items:
                self.precollected_pool.append(item)
                self.progressive_pool.remove(item)

    def get_filler_item_name(self, strict: bool = True) -> str:
        if not strict and len(self.useful_pool) > 0:
            return self.useful_pool.pop()

        use_vanilla_item_as_filler = self.multiworld.random.choice([True, False])
        if len(self.filler_pool) > 0 and use_vanilla_item_as_filler:
            return self.filler_pool.pop()

        filler_consumables = ["10 Berries", "20 Berries", "50 Berries", "100 Berries"]
        filler_weights = [2, 4, 8, 20]

        return self.multiworld.random.choices(filler_consumables, weights=filler_weights, k=1)[0]

    def create_items(self):

        for item in self.precollected_pool:
            self.multiworld.push_precollected(self.create_item(item))

        if self.options.goal == self.options.goal.option_mew:
            location = self.get_location("Skygarden - Mew Power Competition -- Friendship")
            location.place_locked_item(
                self.create_item(
                    "Victory"
                )
            )
            location.address = None
        elif self.options.goal == self.options.goal.option_postgame:
            location = self.get_location("Skygarden - Prisma Completion -- Completed")
            location.place_locked_item(
                self.create_item(
                    "Victory"
                )
            )
            location.address = None

        remaining_slots = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.progressive_pool)

        self.progressive_pool.extend(
            [self.get_filler_item_name(strict=False) for _ in range(
                remaining_slots
            )]
        )

        self.random.shuffle(self.progressive_pool)
        for item in self.progressive_pool:
            self.multiworld.itempool.append(self.create_item(item))

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "goal",
            "num_required_prisma_count_skygarden",
            "remove_battle_power_comp_locations",
            "remove_chase_power_comp_locations",
            "remove_quiz_power_comp_locations",
            "remove_hide_and_seek_power_comp_locations",
            "remove_errand_power_comp_locations",
            "remove_misc_power_comp_locations",
            "remove_power_training_locations",
            "remove_attraction_locations",
            "remove_attraction_prisma_locations",
            "remove_pokemon_unlock_locations"

        )
        return slot_data

def launch_client():
    from .PokeparkClient import main
    launch_component(main, name="Pokepark client")


components.append(Component("Pokepark Client", "PokeparkClient",
                            func=launch_client, component_type=Type.CLIENT, icon="Pokepark"
                            )
                  )
icon_paths["Pokepark"] = "ap:worlds.pokepark/assets/icon.png"

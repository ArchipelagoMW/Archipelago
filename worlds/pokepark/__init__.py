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
from .items import ITEM_TABLE, PokeparkItem, PokeparkItemData, TOTAL_FRIENDSHIP_ITEMS, fast_travel_items, \
    item_name_groups, \
    option_to_progression, \
    road_block_items, static_progressive_items, static_useful_items
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

        self.all_items: list[str] = list()
        self.progressive_pool: list[str] = list()
        self.useful_pool: list[str] = list()
        self.filler_pool: list[str] = list()
        self.precollected_pool: list[str] = list()
        self.item_classifications: dict[str, IC] = {}

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
        if self.options.goal == self.options.goal.option_postgame:
            removable_location_flags.add(PokeparkFlag.MEW)

        local_locations: set[str] = set()
        for location, data in LOCATION_TABLE.items():
            if (data.each_zone == each_zone_filter or
                    data.flags in removable_location_flags):
                pass
            else:
                local_locations.add(location)

        return local_locations

    def generate_early(self) -> None:
        # generate regions and entrances
        self.entrances.generate_entrance_data()

        # setup locations
        self.locations = self._determine_locations()

        # setup items
        self._init_items_and_classification()
        self._update_pool_with_precollected_items()

        self._determine_item_classification()
        self._distribute_item_pools()

        if len(self.locations) <= len(self.progressive_pool):
            raise OptionError(
                "Invalid option combination: More progressive items than available locations. "
                "Consider adding more locations."
            )

    def _init_items_and_classification(self):
        """Initialize all items list and base classifications from ITEM_TABLE."""
        for item_name, data in ITEM_TABLE.items():
            if data.type == "Item":
                self.all_items.extend([item_name] * data.quantity)
                self.item_classifications[item_name] = data.classification

    def _update_pool_with_precollected_items(self):
        """Move items to precollected pool based on game options."""
        options = self.options
        if options.power_randomizer.value == options.power_randomizer.option_dash:
            self._precollect_item("Progressive Dash", 1)

        if options.power_randomizer.value == options.power_randomizer.option_thunderbolt:
            self._precollect_item("Progressive Thunderbolt", 1)

        if options.power_randomizer.value == options.power_randomizer.option_thunderbolt_dash:
            self._precollect_item("Progressive Thunderbolt", 1)
            self._precollect_item("Progressive Dash", 1)

        if options.power_randomizer.value == options.power_randomizer.option_full:
            self._precollect_item("Progressive Thunderbolt", 4)
            self._precollect_item("Progressive Dash", 4)
            self._precollect_item("Progressive Iron Tail", 3)
            self._precollect_item("Progressive Health", 3)
            self._precollect_item("Double Dash", 1)

        if options.starting_zone.value == options.starting_zone.option_one:
            self.random.shuffle(fast_travel_items)
            precollected_fast_travel = self.random.choice(fast_travel_items)
            self._precollect_item(precollected_fast_travel, 1)

        if options.starting_zone.value == options.starting_zone.option_all:
            for item in fast_travel_items:
                self._precollect_item(item, 1)

        if not options.in_zone_road_blocks.value:
            for item in road_block_items:
                self._precollect_item(item, 1)

    def _precollect_item(self, item_name: str, count: int = 1):
        """Move item(s) from all_items to precollected_pool."""
        for _ in range(count):
            self.precollected_pool.append(item_name)
            self.all_items.remove(item_name)

    def _distribute_item_pools(self):
        """Distribute all items into progression, useful, and filler pools based on their classifications."""
        for item_name in self.all_items:
            classification = self.item_classifications[item_name]

            if classification == IC.progression:
                self.progressive_pool.append(item_name)
            elif classification == IC.useful:
                self.useful_pool.append(item_name)
            elif classification == IC.filler:
                self.filler_pool.append(item_name)

    def _determine_item_classification(self):
        """Determine item classifications based on options"""
        progression_items = self._get_progression_items_from_options()

        removable_items = self._get_removable_items(progression_items)

        overlap = progression_items & removable_items
        assert not overlap, f"Items marked as both needed and removable: {overlap}"

        for item_name in self.item_classifications:
            if item_name in progression_items:
                self.item_classifications[item_name] = IC.progression
            elif item_name in removable_items:
                self.item_classifications[item_name] = IC.useful if item_name in static_useful_items else IC.filler

    def _get_progression_items_from_options(self) -> set[str]:
        """Get all items that must be progression based on static list and options."""
        progression_items = set(static_progressive_items)

        option_names = [option_name for option_name, _ in option_to_progression.keys()]
        option_dict = self.options.as_dict(*option_names)

        for option, (min_friendship, items) in option_to_progression.items():
            option_name, expected_value = option
            if option_dict.get(option_name) == expected_value:
                progression_items.update(items)

        return progression_items

    def _get_removable_items(self, required_progression: set[str]) -> set[str]:
        """Determine which items can be downgraded from progression to useful/filler."""
        min_required_friendship = self._calculate_min_friendship_requirement()
        max_removable_friendship = TOTAL_FRIENDSHIP_ITEMS - min_required_friendship

        friendship_removable = []
        other_removable = []

        for item_name in self.item_classifications:
            if item_name not in required_progression:
                if "Friendship" in item_name:
                    friendship_removable.append(item_name)
                else:
                    other_removable.append(item_name)

        friendship_to_remove = friendship_removable[:max_removable_friendship]

        return set(friendship_to_remove + other_removable)

    def _calculate_min_friendship_requirement(self) -> int:
        """Calculate minimum required friendship items based on options."""
        option_names = [option_name for option_name, _ in option_to_progression.keys()]
        option_dict = self.options.as_dict(*option_names)

        min_required_friendship = 0
        for option, (min_friendship, progression_items) in option_to_progression.items():
            option_name, expected_value = option
            if option_dict.get(option_name) == expected_value:
                min_required_friendship = max(min_required_friendship, min_friendship)

        return min_required_friendship

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
        appokepark = PokeparkContainer(
            path=os.path.join(
                output_directory, f"{multiworld.get_out_file_name_base(player)}{PokeparkContainer.patch_file_ending}"
            ),
            player=player,
            player_name=self.player_name,
            data=output_data,
        )
        appokepark.write()

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
            if self.item_classifications.__contains__(name):
                classification = self.item_classifications.get(name)
            else:
                classification = ITEM_TABLE[name].classification
            return PokeparkItem(name, self.player, ITEM_TABLE[name], classification)
        raise KeyError(f"Invalid item name: {name}")

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

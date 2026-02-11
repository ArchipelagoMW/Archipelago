import logging
import os
from multiprocessing import Process
from typing import Mapping, Any, TYPE_CHECKING

from BaseClasses import MultiWorld, Tutorial
from Options import Option, OptionError
from worlds.AutoWorld import WebWorld, World
from . import items, locations, options, output
from worlds.LauncherComponents import components, Component

if TYPE_CHECKING:
    from .generate.shapes import Processor
    from .data import AccessRule


def run_client():
    from .client import main
    p = Process(target=main)
    p.start()


components.append(Component("shapez 2 Client", func=run_client))


class Shapez2Web(WebWorld):
    rich_text_options_doc = True
    theme = "partyTime"
    game_info_languages = ['en']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing shapez 2 with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]


class Shapez2World(World):
    """
    shapez 2 is an automation game about cutting, rotating, stacking, and painting shapes, that you extract from
    randomly generated islands in an infinite space, without having to pay for building your factories.
    It is the successor to shapez and contains a variety of more features like crystals, space platforms and belts,
    trains, and an astounding new 3-dimensional gameplay environment in space.
    """
    game = "shapez 2"
    options_dataclass = options.Shapez2Options
    options: options.Shapez2Options
    topology_present = True
    web = Shapez2Web()
    item_name_to_id = items.lookup_table()
    location_name_to_id = locations.lookup_table()
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        from .data.version import ap_minimum
        from Utils import version_tuple
        if version_tuple < ap_minimum():
            raise Exception(f"Archipelago version too old for shapez 2 "
                            f"(requires minimum {ap_minimum()}, found {version_tuple}")

        self.seed: int = 0
        self.to_be_filled_locations: int = 0
        self.starting_processor: str | None = None
        self.starting_items: list[str] = []  # Contains actual items AND event items
        self.filler_nested: list[str | list] | None = None
        self.milestone_shapes: list[tuple[list[str], list[str]]] = []
        self.task_shapes: list[list[str]] = []
        self.operator_shapes: list[str | None | int] = []
        self.blueprint_shapes: list[str] = []
        self.blueprint_points: list[int] = []
        self.milestone_processors: list[list["Processor"]] = []
        self.task_processors: list[list[Processor]] = []
        self.operator_processors: list[list[Processor]] = []
        self.milestone_checks_counts: list[int] = []

        self.ut_active: bool = False
        self.location_id_to_alias: dict[int, str] = {}

    def generate_early(self) -> None:

        # Load values from UT if this is a regenerated world
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                from .data import version

                self.ut_active = True
                re_gen_slot_data: dict[str, Any] = self.multiworld.re_gen_passthrough[self.game]
                re_gen_options: dict[str, Any] = re_gen_slot_data["options"]
                # Populate options from UT
                for key, value in re_gen_options.items():
                    opt: Option | None = getattr(self.options, key, None)
                    if opt is not None:
                        setattr(self.options, key, opt.from_any(value))
                self.seed = re_gen_slot_data["seed"]
                loaded_ut_version = re_gen_slot_data.get("ut_compatibility", (0, 99, 0))
                if version.ut_compatibility() != loaded_ut_version:
                    raise Exception("The slot you're trying to track is entirely incompatible with this apworld "
                                    "version. Please update your apworld.")
                if version.ut_accuracy() != loaded_ut_version:
                    logging.warning("UT accuracy mismatch detected. You can continue tracking with this "
                                    "apworld version, but tracking might not be entirely accurate.")

        if not self.ut_active:
            self.seed = self.random.getrandbits(64)

        self.random.seed(self.seed)

        adjust = self.options.location_adjustments

        if self.options.goal == "operator_levels" and adjust["Operator level checks"] == 0:
            raise OptionError(f"{self.player_name}: Goal operator_levels requires at least 1 operator level check.")
        if adjust.count_min_locations() < (
            70 + (adjust["Task lines"] if "Lock task lines" in self.options.location_modifiers else 0) +
            (adjust["Operator lines"] if "Lock operator lines" in self.options.location_modifiers else 0)
        ):
            raise OptionError(f"{self.player_name}: Not enough guaranteed locations ({adjust.count_min_locations()}) "
                              f"for required items ({80 + adjust['Task lines'] + adjust['Operator lines']}).")

        locations.pre_generate_logic(self)
        items.pre_generate_logic(self)
        self.starting_items = items.get_starting_items(self)
        self.options.blueprint_shapes.verify_plando(self)

    def create_item(self, name: str) -> items.Shapez2Item:
        return items.generate_item(name, self)

    def get_filler_item_name(self) -> str:
        return items.generate_filler(self)

    def create_regions(self) -> None:
        regions = locations.get_regions(self)
        locations.connect_regions(self, regions)
        processor_rules_dict: dict[tuple[str, ...], "AccessRule"] = {}
        locations.create_events(self, regions, processor_rules_dict)
        locations.create_and_place_locations(self, regions, processor_rules_dict)
        self.to_be_filled_locations = sum(
            (0 if loc.item else 1)
            for reg in regions.values()
            for loc in reg.locations
        )
        self.multiworld.regions.extend(regions.values())

    def create_items(self) -> None:
        item_pool = items.get_main_item_pool(self)
        if len(item_pool) > self.to_be_filled_locations:
            raise Exception(f"Player {self.player_name} has more guaranteed items ({len(item_pool)}) "
                            f"than to-be-filled locations ({self.to_be_filled_locations})."
                            f"Please report this to the apworld dev and provide the yaml used for generating.")
        for _ in range(self.to_be_filled_locations-len(item_pool)):
            item_pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool.extend(item_pool)

    def generate_output(self, output_directory: str) -> None:
        output.Shapez2ScenarioContainer(self, output_directory).write()

    def fill_slot_data(self) -> Mapping[str, Any]:
        from .data import version

        # Some options and data are included for UT
        return {
            "options": {
                "goal": self.options.goal.current_key,
                "location_adjustments": self.options.location_adjustments.value,
                "shape_configuration": self.options.shape_configuration.current_key,
                "shape_generation_modifiers": self.options.shape_generation_modifiers.value,
                "shape_generation_adjustments": self.options.shape_generation_adjustments.value,
                "blueprint_shapes": self.options.blueprint_shapes.to_slot_data(),
                "item_pool_modifiers": self.options.item_pool_modifiers.value,
                "show_other_players_items": self.options.show_other_players_items.value,
                "start_inventory": self.options.start_inventory.value,
                "start_inventory_from_pool": self.options.start_inventory_from_pool.value,
            },
            # Needed for UT
            "seed": self.seed,
            "ut_compatibility": version.ut_compatibility(),
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        """Helper function for Universal Tracker"""
        return slot_data

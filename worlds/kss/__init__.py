import logging
import settings
import os
import base64
import threading
import math
from typing import Dict, List, ClassVar, Any, Mapping
from BaseClasses import Tutorial, MultiWorld, CollectionState, Item, ItemClassification
from worlds.AutoWorld import World, WebWorld
from Options import OptionError
from .items import (lookup_item_to_id, item_table, item_groups, KSSItem, filler_item_weights, copy_abilities,
                    sub_games, dyna_items, planets, treasures, sub_game_completion)
from .locations import location_table, KSSLocation
from .names import item_names
from .options import KSSOptions, subgame_mapping, IncludedSubgames, Consumables
from .regions import create_regions
from .rom import KSS_UHASH, KSSProcedurePatch, patch_rom, KSS_VCHASH
from .rules import set_rules
from .client import KSSSNIClient

logger = logging.getLogger("Kirby Super Star")


class KSSSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the KSS JP or EN rom"""
        description = "Kirby Super Star ROM File"
        copy_to = "Kirby Super Star.sfc"
        md5s = [KSS_UHASH, KSS_VCHASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class KSSWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kirby Super Star randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris"]
        )
    ]
    #options_presets = kss_options_presets
    #option_groups = kss_option_groups


class KSSWorld(World):
    game = "Kirby Super Star"
    item_name_to_id = lookup_item_to_id
    location_name_to_id = {location: data.code
                           for location, data in location_table.items() if data.code}
    item_name_groups = item_groups
    web = KSSWebWorld()
    settings: ClassVar[KSSSettings]
    options_dataclass = KSSOptions
    options: KSSOptions
    treasure_value: List[int]
    ut_can_gen_without_yaml: bool = True

    create_regions = create_regions

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.rom_name: bytearray = bytearray()
        self.rom_name_available_event = threading.Event()
        self.treasure_value = []

    def generate_early(self) -> None:
        # lots here
        if not self.options.included_subgames.value.intersection(
                {"The Great Cave Offensive", "Milky Way Wishes", "The Arena"}):
            raise OptionError(f"Kirby Super Star ({self.player_name}): At least one of The Great Cave Offensive, "
                              f"Milky Way Wishes, or The Arena must be included")

        for game in sorted(self.options.required_subgames.value):
            if game not in self.options.included_subgames.value:
                logger.warning(F"Kirby Super Star ({self.player_name}): Required subgame {game} not included, "
                               F"adding to included subgames")
                self.options.included_subgames.value.add(game)

        if self.options.starting_subgame.current_option_name not in self.options.included_subgames:
            logger.warning(f"Kirby Super Star ({self.player_name}): Starting subgame not included, choosing random.")
            self.options.starting_subgame.value = self.random.choice([value[0] for value in subgame_mapping.items()
                                                                      if value[1] in self.options.included_subgames])

        if self.options.required_subgame_completions > len(self.options.included_subgames.value):
            logger.warning(f"Kirby Super Star ({self.player_name}): Required subgame count greater than "
                           f"included subgames, reducing to all included.")
            self.options.required_subgame_completions.value = len(self.options.included_subgames.value)

        if "The Great Cave Offensive" in self.options.included_subgames:
            # gold threshold validation
            if (self.options.the_great_cave_offensive_gold_thresholds["Crystal"] >
                    self.options.the_great_cave_offensive_gold_thresholds["Old Tower"]):
                logger.warning(f"TGCO ({self.player_name}): Crystal threshold is greater than Old Tower, swapping")
                temp = self.options.the_great_cave_offensive_gold_thresholds["Old Tower"]
                self.options.the_great_cave_offensive_gold_thresholds.value["Old Tower"] =\
                    self.options.the_great_cave_offensive_gold_thresholds["Crystal"]
                self.options.the_great_cave_offensive_gold_thresholds.value["Crystal"] = temp
            if (self.options.the_great_cave_offensive_gold_thresholds["Old Tower"] >
                    self.options.the_great_cave_offensive_gold_thresholds["Garden"]):
                logger.warning(f"TGCO ({self.player_name}): Old Tower threshold is greater than Garden, swapping")
                temp = self.options.the_great_cave_offensive_gold_thresholds["Garden"]
                self.options.the_great_cave_offensive_gold_thresholds.value["Garden"] =\
                    self.options.the_great_cave_offensive_gold_thresholds["Old Tower"]
                self.options.the_great_cave_offensive_gold_thresholds.value["Old Tower"] = temp

        # proper UT support
        if hasattr(self.multiworld, "generation_is_fake"):
            self.options.included_subgames.valid_keys = IncludedSubgames.valid_keys
            self.options.consumables.value = Consumables.valid_keys
            self.options.essences.value = True

    def create_item(self, name: str, force_classification: ItemClassification | None = None) -> KSSItem:
        if name not in item_table:
            raise Exception(f"{name} is not a valid item name for Kirby Super Star.")
        data = item_table[name]
        classification = force_classification if force_classification else data.classification
        return KSSItem(name, classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()), weights=list(filler_item_weights.values()), k=1)[0]

    def create_items(self) -> None:
        itempool = []
        modes = [self.create_item(name) for name in sub_games if name in self.options.included_subgames]
        starting_mode = self.create_item(subgame_mapping[self.options.starting_subgame.value])
        modes.remove(starting_mode)
        self.multiworld.push_precollected(starting_mode)
        itempool.extend([self.create_item(name) for name in copy_abilities])
        itempool.extend(modes)

        treasure_value = 0

        if "Dyna Blade" in self.options.included_subgames:
            force = None
            if not self.options.essences and "Maxim Tomato" not in self.options.consumables:
                force = ItemClassification.useful
            itempool.extend([self.create_item(name, force if "Extra" in name else None)
                             for name, data in dyna_items.items()
                             for _num in range(data.num)
                             ])
        if "The Great Cave Offensive" in self.options.included_subgames:
            max_gold = (math.floor((9999990 - self.options.the_great_cave_offensive_required_gold.value) *
                                   (self.options.the_great_cave_offensive_excess_gold.value / 100))
                        + self.options.the_great_cave_offensive_required_gold.value)
            for name, treasure in sorted(treasures.items(), key=(lambda treasure: treasure[1].value), reverse=True):
                itempool.append(self.create_item(name))
                treasure_value += treasure.value
                if treasure_value >= max_gold:
                    break
        if "Milky Way Wishes" in self.options.included_subgames:
            planet = [self.create_item(name) for name in planets]
            starting_planet = self.random.choice(planet)
            planet.remove(starting_planet)
            self.multiworld.push_precollected(starting_planet)
            itempool.extend(planet)

            if self.options.milky_way_wishes_mode == "multiworld":
                itempool.extend(self.create_item(item_names.rainbow_star) for _ in range(7))

        location_count = len(list(self.multiworld.get_unfilled_locations(self.player))) - len(itempool)
        if location_count < 0:
            if "The Great Cave Offensive" in self.options.included_subgames:
                # with TGCO we can just remove treasures until we can hit 0
                sorted_treasures = sorted(treasures.items(), key=lambda treasure: treasure[1].value)
                while location_count < 0:
                    name, treasure = sorted_treasures.pop(0)
                    item = next((item for item in itempool if item.name == name), None)
                    if item:
                        itempool.remove(item)
                        treasure_value -= treasure.value
                        location_count += 1
            else:
                raise OptionError("Unable to create item pool with current settings.")
        itempool.extend([self.create_item(filler) for filler in
                         self.random.choices(list(filler_item_weights.keys()),
                                             weights=list(filler_item_weights.values()),
                                             k=location_count)])

        required_gold = min(self.options.the_great_cave_offensive_required_gold.value, treasure_value)

        self.treasure_value = [*[math.floor(required_gold *
                                            (self.options.the_great_cave_offensive_gold_thresholds[region] / 100))
                                for region in ["Crystal", "Old Tower", "Garden"]],
                               self.options.the_great_cave_offensive_required_gold.value]
        self.multiworld.itempool += itempool

    set_rules = set_rules

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = self.options.as_dict("included_subgames", "consumables", "essences", "milky_way_wishes_mode")
        slot_data.update({
            "treasure_value": self.treasure_value
        })
        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    def generate_output(self, output_directory: str) -> None:
        try:
            patch = KSSProcedurePatch(player=self.player, player_name=self.player_name)
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        assert isinstance(self.rom_name, bytearray)
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(self.rom_name).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        value = super().collect(state, item)

        if item.name in treasures:
            state.prog_items[self.player]["Gold"] += treasures[item.name].value

        return value

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        value = super().remove(state, item)

        if item.name in treasures:
            state.prog_items[self.player]["Gold"] -= treasures[item.name].value
            if not state.prog_items[self.player]["Gold"]:
                del state.prog_items[self.player]["Gold"]

        return value

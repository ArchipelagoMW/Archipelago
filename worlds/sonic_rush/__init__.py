import os
import pkgutil
import typing
from typing import Any, List, Dict, Mapping

import settings
from .Rom import SonicRushProcedurePatch, write_tokens
from .items import item_table, SonicRushItem, filler, progressive_level_selects, emeralds, zone_unlocks, traps, trap, \
    item_list
from .locations import act_locations, boss_locations, special_stage_locations, add_bosses, \
    add_special_stages, add_base_acts, add_menu_locations, all_locations
from .options import SonicRushOptions
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, MultiWorld
from .regions import create_regions
from . import data
from .client import SonicRushClient  # Unused, but required to register with BizHawkClient


class SonicRushWeb(WebWorld):
    rich_text_options_doc = True
    theme = "grass"
    game_info_languages = ['en']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Sonic Rush with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]
    # item_descriptions = item_descriptions
    # location_descriptions = location_description


class SonicRushSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Sonic Rush USA rom"""

        copy_to = "SONICRUSH_USA.nds"
        description = "Sonic Rush (USA) ROM File"
        md5s = ["bd4dcf6ad27de0e3212b8c67864df0ec"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class SonicRushWorld(World):
    """
    Sonic Rush is a 2.5D platformer for the Nintendo DS from 2005.
    It's the game that introduced Blaze the Cat and the boost ability.
    """
    game = "Sonic Rush"
    options_dataclass = SonicRushOptions
    options: SonicRushOptions
    web = SonicRushWeb()
    settings: typing.ClassVar[SonicRushSettings]
    item_name_to_id = {name: next_id for next_id, name in enumerate(item_list, data.base_id)}
    location_name_to_id = {name: next_id for next_id, name in enumerate(all_locations, data.base_id)}

    item_name_groups: typing.ClassVar[Dict[str, typing.Set[str]]] = {
        "Zone Unlocks": set(data.zone_names),
        "Emeralds": {
            f"{color} {dim} Emerald"
            for color in data.emerald_colors
            for dim in ["Chaos", "Sol"]
        },
        "Chaos Emeralds": {
            f"{color} Chaos Emerald"
            for color in data.emerald_colors
        },
        "Sol Emeralds": {
            f"{color} Sol Emerald"
            for color in data.emerald_colors
        },
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.location_count: int = 0

    def generate_early(self) -> None:
        pass

    def create_item(self, name: str) -> Item:
        return SonicRushItem(
            name,
            item_table[name](self.options, self.multiworld),
            self.item_name_to_id[name],
            self.player
        )

    def get_filler_item_name(self) -> str:
        return filler(self.random.random())

    def create_regions(self) -> None:
        # Create list of all included level and upgrade locations based on player options
        # This already includes the region to be placed in and the LocationProgressType
        included_locations = (
            add_base_acts(self.options) +
            add_bosses(self.options) +
            add_special_stages(self.options) +
            add_menu_locations(self.options)
        )

        # Save the final amount of to-be-filled locations
        self.location_count = len(included_locations)

        # Create regions and entrances based on included locations and player options
        self.multiworld.regions.extend(
            create_regions(
                self.player, self.multiworld, self.options, self.location_name_to_id, included_locations
            )
        )

    def create_items(self) -> None:
        # Multiworlds with very few slots regularly fail generation on default settings.
        # But a higher amount of starting zones tends to make goal reachable in sphere 1.
        # This raises that option to a higher minimum value if there are few worlds, so that unittests don't fail.
        # match len(self.multiworld.worlds):
        #     case 1:
        #         self.options.amount_of_starting_zones.value = max(10, self.options.amount_of_starting_zones.value)
        #     case 2:
        #         self.options.amount_of_starting_zones.value = max(6, self.options.amount_of_starting_zones.value)
        #     case 3:
        #         self.options.amount_of_starting_zones.value = max(4, self.options.amount_of_starting_zones.value)
        #     case 4:
        #         self.options.amount_of_starting_zones.value = max(2, self.options.amount_of_starting_zones.value)

        included_items: List[Item] = [self.create_item(name) for name in zone_unlocks]
        # self.multiworld.push_precollected(included_items.pop(-2))
        for _ in range(self.options.amount_of_starting_zones):
            self.multiworld.push_precollected(
                included_items.pop(self.random.randint(0, len(included_items)-1))
            )
        # if len(included_items):
        #     for _ in range(6):
        #         self.multiworld.early_items[self.player][self.random.choice(included_items).name] = 1
        included_items += (
            [self.create_item(name) for name in progressive_level_selects for _ in range(7)] +
            [self.create_item(name) for name in emeralds]
        )

        if self.options.tails_and_cream_substory == "always_present":
            self.multiworld.push_precollected(self.create_item("Tails"))
            self.multiworld.push_precollected(self.create_item("Cream"))
        elif self.options.tails_and_cream_substory == "appearing_later":
            included_items += [self.create_item("Tails"), self.create_item("Cream")]
        elif self.options.tails_and_cream_substory == "getting_kidnapped":
            self.multiworld.push_precollected(self.create_item("Tails"))
            self.multiworld.push_precollected(self.create_item("Cream"))
            included_items += [self.create_item("Kidnapping Tails"), self.create_item("Kidnapping Cream")]
        elif self.options.tails_and_cream_substory == "on_vacation":
            pass

        traps_probability = self.options.traps_percentage/100
        for _ in range(self.location_count - len(included_items)):
            if self.random.random() < traps_probability:
                # Fill with trap
                included_items.append(self.create_item(trap(self.random.random())))
            else:
                # Fil with random filler item
                included_items.append(self.create_item(self.get_filler_item_name()))

        # Add correct number of items to itempool
        self.multiworld.itempool += included_items

    def set_rules(self) -> None:
        # Rules get instantly applied after initializing the regions
        pass

    def generate_output(self, output_directory: str) -> None:
        patch = SonicRushProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/SonicRushAPPatch.bsdiff"))
        write_tokens(patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Options that are relevant to the client
        option_data = {
            "goal": self.options.goal.current_key,
            "screw_f_zone": bool(self.options.screw_f_zone.value),
            "include_s_rank_checks": self.options.include_s_rank_checks.current_key,
            "deathlink": bool(self.options.deathlink.value)
        }

        return option_data

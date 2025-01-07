import os
import typing

import settings
from BaseClasses import ItemClassification, Tutorial, Item, Location
from Fill import fast_fill
from typing import List

from worlds.AutoWorld import WebWorld, World

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
from .Arrays import item_dict
from .Items import GLItem, item_frequencies, item_list, item_table
from .Locations import LocationData, all_locations, location_table
from .Options import GLOptions
from .Regions import connect_regions, create_regions
from .Rom import GLProcedurePatch, write_files
from .Rules import set_rules


def launch_client(*args):
    from .GauntletLegendsClient import launch

    launch_subprocess(launch, name="GauntletLegendsClient")


components.append(
    Component(
        "Gauntlet Legends Client",
        "GauntletLegendsClient",
        func=launch_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apgl"),
    ),
)


class GauntletLegendsWebWorld(WebWorld):
    settings_page = "games/gl/info/en"
    theme = "partyTime"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to playing Gauntlet Legends",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["jamesbrq"],
        ),
    ]


class GLSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the GL US rom"""

        copy_to = "Gauntlet Legends (U) [!].z64"
        description = "Gauntlet Legends ROM File"

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = False


class GauntletLegendsWorld(World):
    """
    Gauntlet Legends
    """

    game = "Gauntlet Legends"
    web = GauntletLegendsWebWorld()
    options_dataclass = GLOptions
    options: GLOptions
    settings: typing.ClassVar[GLSettings]
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    death: List[Item] = []

    disabled_locations: typing.List[LocationData]

    def generate_early(self) -> None:
        self.options.max_difficulty_value.value = max(self.options.max_difficulty_value.value, self.options.local_players.value)

    def create_regions(self) -> None:
        self.disabled_locations = []
        if self.options.chests_barrels == 0:
            self.disabled_locations += [
                location.name
                for location in all_locations
                if "Chest" in location.name or ("Barrel" in location.name and "Barrel of Gold" not in location.name)
                and location.name not in self.disabled_locations
            ]
        elif self.options.chests_barrels == 1:
            self.disabled_locations += [
                location.name
                for location in all_locations
                if "Barrel" in location.name and "Barrel of Gold" not in location.name
                and location.name not in self.disabled_locations
            ]
        elif self.options.chests_barrels == 2:
            self.disabled_locations += [location.name for location in all_locations if "Chest" in location.name and location.name not in self.disabled_locations]

        if self.options.max_difficulty_toggle:
            self.disabled_locations += [location.name for location in all_locations
                                        if location.difficulty > self.options.max_difficulty_value
                                        and location.name not in self.disabled_locations]

        create_regions(self)
        connect_regions(self)
        if not self.options.infinite_keys:
            item = self.create_item("Key")
            self.get_location("Valley of Fire - Key 1").place_locked_item(item)
            self.get_location("Valley of Fire - Key 5").place_locked_item(item)
        if self.options.obelisks == 0:
            item = self.create_item("Mountain Obelisk 1")
            self.get_location("Valley of Fire - Obelisk").place_locked_item(item)
            item = self.create_item("Mountain Obelisk 2")
            self.get_location("Dagger Peak - Obelisk").place_locked_item(item)
            item = self.create_item("Mountain Obelisk 3")
            self.get_location("Cliffs of Desolation - Obelisk").place_locked_item(item)
            item = self.create_item("Castle Obelisk 1")
            self.get_location("Castle Courtyard - Obelisk").place_locked_item(item)
            item = self.create_item("Castle Obelisk 2")
            self.get_location("Dungeon of Torment - Obelisk").place_locked_item(item)
            item = self.create_item("Town Obelisk 1")
            self.get_location("Poisoned Fields - Obelisk").place_locked_item(item)
            item = self.create_item("Town Obelisk 2")
            self.get_location("Haunted Cemetery - Obelisk").place_locked_item(item)
        if self.options.mirror_shards == 0:
            item = self.create_item("Dragon Mirror Shard")
            self.get_location("Dragon's Lair - Dragon Mirror Shard").place_locked_item(item)
            item = self.create_item("Chimera Mirror Shard")
            self.get_location("Chimera's Keep - Chimera Mirror Shard").place_locked_item(item)
            item = self.create_item("Plague Fiend Mirror Shard")
            self.get_location("Vat of the Plague Fiend - Plague Fiend Mirror Shard").place_locked_item(item)
            item = self.create_item("Yeti Mirror Shard")
            self.get_location("Yeti's Cavern - Yeti Mirror Shard").place_locked_item(item)

    def fill_slot_data(self) -> dict:
        dshard = self.get_location("Dragon's Lair - Dragon Mirror Shard").item
        yshard = self.get_location("Yeti's Cavern - Yeti Mirror Shard").item
        cshard = self.get_location("Chimera's Keep - Chimera Mirror Shard").item
        fshard = self.get_location("Vat of the Plague Fiend - Plague Fiend Mirror Shard").item
        shard_values = [
            item_dict[dshard.code] if dshard.player == self.player else [0x27, 0x4],
            item_dict[yshard.code] if yshard.player == self.player else [0x27, 0x4],
            item_dict[cshard.code] if cshard.player == self.player else [0x27, 0x4],
            item_dict[fshard.code] if fshard.player == self.player else [0x27, 0x4],
        ]
        characters = [
            self.options.unlock_character_one.value,
            self.options.unlock_character_two.value,
            self.options.unlock_character_three.value,
            self.options.unlock_character_four.value,
        ]
        chests_barrels = self.options.chests_barrels.value
        return {
            "player": self.player,
            "players": self.options.local_players.value,
            "shards": shard_values,
            "chests": bool(chests_barrels == 3 or chests_barrels == 1),
            "barrels": bool(chests_barrels == 3 or chests_barrels == 2),
            "speed": self.options.permanent_speed.value,
            "keys": self.options.infinite_keys.value,
            "characters": characters,
            "max": (self.options.max_difficulty_value.value if self.options.max_difficulty_toggle else 4),
            "instant_max": self.options.instant_max.value,
            "death_link": bool((self.options.death_link.value == 1))
        }

    def create_items(self) -> None:
        # First add in all progression and useful items
        required_items = []
        precollected = [item for item in item_list if item in self.multiworld.precollected_items[self.player]]
        for item in item_list:
            if item.progression != ItemClassification.filler and item.progression != ItemClassification.trap and item not in precollected:
                if "Obelisk" in item.item_name and self.options.obelisks == 0:
                    continue
                if "Mirror" in item.item_name and self.options.mirror_shards == 0:
                    continue
                freq = item_frequencies.get(item.item_name, 1)
                required_items += [item.item_name for _ in range(freq)]

        for item_name in required_items:
            self.multiworld.itempool.append(self.create_item(item_name))

        # Then, get a random amount of fillers until we have as many items as we have locations
        filler_items = []
        trap_count = 0
        for item in item_list:
            if item.progression == ItemClassification.filler or item.progression == ItemClassification.trap:
                if "Key" in item.item_name and self.options.infinite_keys:
                    continue
                if "Boots" in item.item_name and self.options.permanent_speed:
                    continue
                if "Poison" in item.item_name and (self.options.traps_choice.value == self.options.traps_choice.option_only_death or self.options.traps_choice.value == self.options.traps_choice.option_none_active):
                    continue
                if "Death" in item.item_name and (self.options.traps_choice.value == self.options.traps_choice.option_only_fruit or self.options.traps_choice.value == self.options.traps_choice.option_none_active):
                    continue

                freq = item_frequencies.get(item.item_name, 1) + (30 if self.options.infinite_keys else 0) + (5 if self.options.permanent_speed else 0)

                if self.options.traps_frequency.value == self.options.traps_frequency.option_large and item.progression == ItemClassification.trap:
                    freq *= 2
                elif self.options.traps_frequency.value == self.options.traps_frequency.option_extreme and item.progression == ItemClassification.trap:
                    freq *= 5

                if item.item_name == "Invulnerability" or item.item_name == "Anti-Death Halo":
                    freq = item_frequencies.get(item.item_name, 1)
                if item.item_name == "Anti-Death Halo" and (self.options.traps_choice.value == self.options.traps_choice.option_only_death or self.options.traps_choice.value == self.options.traps_choice.option_all_active) and self.options.traps_frequency.value == self.options.traps_frequency.option_extreme:
                    freq *= 2
                if item.item_name == "Death":
                    trap_count += freq
                    self.death = []
                    for i in range(freq):
                        self.death += [self.create_item(item.item_name)]
                else:
                    filler_items += [item.item_name for _ in range(freq)]

        remaining = len(all_locations) - len(required_items) - len(self.disabled_locations) - trap_count - (2 if not self.options.infinite_keys else 0)
        if self.options.obelisks == 0:
            remaining -= 7
        if self.options.mirror_shards == 0:
            remaining -= 4
        for i in range(remaining):
            filler_item_name = self.multiworld.random.choice(filler_items)
            self.multiworld.itempool.append(self.create_item(filler_item_name))
            filler_items.remove(filler_item_name)

    def set_rules(self) -> None:
        set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach(
            "Gates of the Underworld", "Region", self.player,
        )

    def pre_fill(self) -> None:
        locations = [location for location in self.multiworld.get_unfilled_locations(self.player)]
        self.random.shuffle(locations)
        fast_fill(self.multiworld, self.death, locations)

    def create_item(self, name: str) -> GLItem:
        item = item_table[name]
        return GLItem(item.item_name, item.progression, item.code, self.player)

    def generate_output(self, output_directory: str) -> None:
        patch = GLProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        write_files(self, patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}",
        )
        patch.write(rom_path)

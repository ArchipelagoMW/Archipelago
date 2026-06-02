import os
from typing import ClassVar

from BaseClasses import MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World
import settings

from .constants import USA_ROM_HASH
from .items import CVAOSItem, item_name_to_id, create_item, create_itempool
from .locations import location_name_to_id
from .options import CVAOSOptions, Goal
from .regions import create_regions, can_reach_room


class CVAOSSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Castlevania AoS USA rom"""
        copy_to = "Castlevania - Aria of Sorrow (USA).gba"
        description = "Castlevania AoS (US) ROM File"
        md5s = [hex(USA_ROM_HASH)[2:]]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class CVAOSWebWorld(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up CVAoS in Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["dem1995"]
    )

    tutorials = [setup_en]


class CVAOSWorld(World):
    """
    Castlevania: Aria of Sorrow is a 2003 action-adventure game developed by Konami
    for the Game Boy Advance. Play as Soma Cruz and explore Dracula's castle,
    collecting souls from defeated enemies to gain their abilities.
    """

    game = "Castlevania - Aria of Sorrow"
    web = CVAOSWebWorld()

    options_dataclass = CVAOSOptions
    options: CVAOSOptions
    settings: ClassVar[CVAOSSettings]

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    topology_present = True
    origin_region_name = "Menu"

    # Both set in create_regions: enemy_number -> region name, and room id -> its door
    # region names. Used by the goal's reachability checks (regions.can_reach_*).
    enemy_region_name_by_number: dict[int, str]
    entrance_region_names_by_room: dict[str, list[str]]

    def create_regions(self) -> None:
        create_regions(self)
        player = self.player
        if self.options.goal == Goal.option_graham:
            # Bad ending: defeat Graham — reach his room (904).
            self.multiworld.completion_condition[player] = \
                lambda state: can_reach_room(state, self, "904")
        else:
            # True ending: reach the Chaos arena (room B14). The Chaotic Realm is reachable
            # only through the gated 507 -> 506 door, which already requires the Flame Demon,
            # Succubus, and Giant Bat souls plus beating Graham, so reaching B14 encodes the
            # whole true-ending requirement (see regions._chaotic_realm_gate).
            self.multiworld.completion_condition[player] = \
                lambda state: can_reach_room(state, self, "B14")

    def create_items(self) -> None:
        itempool = create_itempool(self)
        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> CVAOSItem:
        return create_item(self, name)

    def generate_output(self, output_directory: str) -> None:
        from .rom import CVAOSProcedurePatch, get_location_data, patch_rom

        active_locations = [loc for loc in self.multiworld.get_locations(self.player)
                            if loc.address is not None]
        offset_data = get_location_data(self, active_locations)

        patch = CVAOSProcedurePatch(player=self.player, player_name=self.player_name)
        patch_rom(self, patch, offset_data)

        rom_path = os.path.join(
            output_directory,
            f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}")
        patch.write(rom_path)

    def fill_slot_data(self) -> dict:
        return {
            "randomize_pickups": self.options.randomize_pickups.value,
            "goal": self.options.goal.value,
        }

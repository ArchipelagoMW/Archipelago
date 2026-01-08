from typing import Dict, Optional, Mapping, Any
import typing
import os

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
import settings
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, ItemClassification

from . import ItemPool
from .data import Items, Locations, Planets
from .data.Items import EquipmentData
from .data.Planets import PlanetData
from .Regions import create_regions
from .Container import Rac2ProcedurePatch, generate_patch
from .Rac2Options import Rac2Options


def run_client(_url: Optional[str] = None):
    from .Rac2Client import launch
    launch_subprocess(launch, name="Rac2Client")


components.append(
    Component("Ratchet & Clank 2 Client", func=run_client, component_type=Type.CLIENT,
              file_identifier=SuffixIdentifier(".aprac2"))
)


class Rac2Settings(settings.Group):
    class IsoFile(settings.UserFilePath):
        """File name of the Ratchet & Clank 2 ISO"""
        description = "Ratchet & Clank 2 PS2 ISO file"
        copy_to = "Ratchet & Clank 2.iso"

    class IsoStart(str):
        """
        Set this false to never autostart an iso (such as after patching),
        Set it to true to have the operating system default program open the iso
        Alternatively, set it to a path to a program to open the .iso file with (like PCSX2)
        """

    class GameINI(str):
        """ Set to file path to an existing PCSX2 game setting INI file to have the patcher
        create an appropriately named INI with the rest of the patch output. This can be used to
        allow you to use you own custom PCSX2 setting with patched ISO. """

    iso_file: IsoFile = IsoFile(IsoFile.copy_to)
    iso_start: typing.Union[IsoStart, bool] = False
    game_ini: GameINI = ""


class Rac2Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Ratchet & Clank 2 for Archipelago",
        "English",
        "setup.md",
        "setup/en",
        ["evilwb"]
    )]


class Rac2Item(Item):
    game: str = "Ratchet & Clank 2 - Going Commando"


class Rac2World(World):
    """
    Ratchet & Clank 2: Going Commando is a third-person shooter platform game originally for the PlayStation 2. Play as
    Ratchet and Clank as they attempt to unravel a conspiracy in a new galaxy involving a mysterious "pet project"
    orchestrated by the shadowy MegaCorp.
    """
    game = "Ratchet & Clank 2"
    web = Rac2Web()
    options_dataclass = Rac2Options
    options: Rac2Options
    topology_present = True
    item_name_to_id = {item.name: item.item_id for item in Items.ALL}
    location_name_to_id = {location.name: location.location_id for location in Planets.ALL_LOCATIONS if location.location_id}
    item_name_groups = Items.get_item_groups()
    location_name_groups = Planets.get_location_groups()
    settings: Rac2Settings
    starting_planet: Optional[PlanetData] = None
    starting_weapons: list[EquipmentData] = []
    prefilled_item_map: Dict[str, str] = {}  # Dict of location name to item name

    def get_filler_item_name(self) -> str:
        return Items.BOLT_PACK.name

    def create_regions(self) -> None:
        create_regions(self)

    def create_item(self, name: str, override: Optional[ItemClassification] = None) -> "Item":
        if override:
            return Rac2Item(name, override, self.item_name_to_id[name], self.player)
        item_data = Items.from_name(name)
        return Rac2Item(name, ItemPool.get_classification(item_data), self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> "Item":
        return Rac2Item(name, ItemClassification.progression, None, self.player)

    def pre_fill(self) -> None:
        for location_name, item_name in self.prefilled_item_map.items():
            location = self.get_location(location_name)
            item = self.create_item(item_name, ItemClassification.progression)
            location.place_locked_item(item)

    def create_items(self) -> None:
        items_to_add: list["Item"] = []
        items_to_add += ItemPool.create_planets(self)
        items_to_add += ItemPool.create_equipment(self)
        items_to_add += ItemPool.create_collectables(self)
        items_to_add += ItemPool.create_upgrades(self)

        # add platinum bolts in whatever slots we have left
        unfilled = [i for i in self.multiworld.get_unfilled_locations(self.player) if not i.is_event]
        remain = len(unfilled) - len(items_to_add)
        assert remain >= 0, "There are more items than locations. This is not supported."
        print(f"[RAC2 Debug] Not enough items to fill all locations. Adding {remain} filler items to the item pool")
        for _ in range(remain):
            items_to_add.append(self.create_item(Items.BOLT_PACK.name, ItemClassification.filler))

        self.multiworld.itempool += items_to_add

    def set_rules(self) -> None:
        boss_location = self.multiworld.get_location(Locations.YEEDIL_DEFEAT_MUTATED_PROTOPET.name, self.player)
        boss_location.place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str) -> None:
        aprac2 = Rac2ProcedurePatch(player=self.player, player_name=self.multiworld.get_player_name(self.player))
        generate_patch(self, aprac2)
        rom_path = os.path.join(output_directory,
                                f"{self.multiworld.get_out_file_name_base(self.player)}{aprac2.patch_file_ending}")
        aprac2.write(rom_path)

    def get_options_as_dict(self) -> Dict[str, Any]:
        return self.options.as_dict(
            "death_link",
            "skip_wupash_nebula",
            "extra_spaceship_challenge_locations",
            "starting_weapons",
            "randomize_megacorp_vendor",
            "randomize_gadgetron_vendor",
            "extend_weapon_progression",
        )

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.get_options_as_dict()
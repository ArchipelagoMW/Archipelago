import hashlib
import logging
from typing import Dict, Any, TYPE_CHECKING, Optional, Sequence, Tuple, ClassVar, List

from BaseClasses import Tutorial, ItemClassification, MultiWorld, Item, Location
from worlds.AutoWorld import World, WebWorld
from .names import (gamma, gemini_man_stage, needle_man_stage, hard_man_stage, magnet_man_stage, top_man_stage,
                    snake_man_stage, spark_man_stage, shadow_man_stage, rush_marine, rush_jet, rush_coil)
from .items import (item_table, item_names, MM3Item, filler_item_weights, robot_master_weapon_table,
                    stage_access_table, rush_item_table, lookup_item_to_id)
from .locations import (MM3Location, mm3_regions, MM3Region, energy_pickups, etank_1ups, lookup_location_to_id,
                        location_groups)
from .rom import patch_rom, MM3ProcedurePatch, MM3LCHASH, MM3VCHASH, PROTEUSHASH, MM3NESHASH
from .options import MM3Options
from .client import MegaMan3Client
from .rules import set_rules, weapon_damage, robot_masters, weapons_to_name, minimum_weakness_requirement
import os
import threading
import base64
import settings
logger = logging.getLogger("Mega Man 3")

if TYPE_CHECKING:
    from BaseClasses import CollectionState


class MM3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MM3 EN rom"""
        description = "Mega Man 3 ROM File"
        copy_to: Optional[str] = "Mega Man 3 (USA).nes"
        md5s = [MM3NESHASH, MM3LCHASH, PROTEUSHASH, MM3VCHASH]

        def browse(self: settings.T,
                   filetypes: Optional[Sequence[Tuple[str, Sequence[str]]]] = None,
                   **kwargs: Any) -> Optional[settings.T]:
            if not filetypes:
                file_types = [("NES", [".nes"]), ("Program", [".exe"])]  # LC1 is only a windows executable, no linux
                return super().browse(file_types, **kwargs)
            else:
                return super().browse(filetypes, **kwargs)

        @classmethod
        def validate(cls, path: str) -> None:
            """Try to open and validate file against hashes"""
            with open(path, "rb", buffering=0) as f:
                try:
                    f.seek(0)
                    if f.read(4) == b"NES\x1A":
                        f.seek(16)
                    else:
                        f.seek(0)
                    cls._validate_stream_hashes(f)
                    base_rom_bytes = f.read()
                    basemd5 = hashlib.md5()
                    basemd5.update(base_rom_bytes)
                    if basemd5.hexdigest() == PROTEUSHASH:
                        # we need special behavior here
                        cls.copy_to = None
                except ValueError:
                    raise ValueError(f"File hash does not match for {path}")

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MM3WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
           "Multiworld Setup Guide",
           "A guide to setting up the Mega Man 3 randomizer connected to an Archipelago Multiworld.",
           "English",
           "setup_en.md",
           "setup/en",
           ["Silvris"]
        )
    ]


class MM3World(World):
    """
    Mega Man 3 Description
    """

    game = "Mega Man 3"
    settings: ClassVar[MM3Settings]
    options_dataclass = MM3Options
    options: MM3Options
    item_name_to_id = lookup_item_to_id
    location_name_to_id = lookup_location_to_id
    item_name_groups = item_names
    location_name_groups = location_groups
    web = MM3WebWorld()
    rom_name: bytearray
    world_version: Tuple[int, int, int] = (0, 1, 0)

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)
        self.weapon_damage = weapon_damage.copy()
        self.wily_4_weapons: Dict[int, List[int]] = {}

    def create_regions(self) -> None:
        menu = MM3Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        for region in mm3_regions:
            stage = MM3Region(region, self.player, self.multiworld)
            required_items = mm3_regions[region][0]
            locations = mm3_regions[region][1]
            prev_stage = mm3_regions[region][2]
            if prev_stage is None:
                menu.connect(stage, f"To {region}",
                             lambda state, items=required_items: state.has_all(items, self.player))
            else:
                old_stage = self.multiworld.get_region(prev_stage, self.player)
                old_stage.connect(stage, f"To {region}",
                                  lambda state, items=required_items: state.has_all(items, self.player))
            stage.add_locations(locations)
            for location in stage.get_locations():
                if location.address is None and location.name is not gamma:
                    location.place_locked_item(MM3Item(location.name, ItemClassification.progression,
                                                       None, self.player))
            if self.options.consumables in (self.options.consumables.option_1up_etank,
                                            self.options.consumables.option_all):
                if region in etank_1ups:
                    stage.add_locations(etank_1ups[region], MM3Location)
            if self.options.consumables in (self.options.consumables.option_weapon_health,
                                            self.options.consumables.option_all):
                if region in energy_pickups:
                    stage.add_locations(energy_pickups[region], MM3Location)
            self.multiworld.regions.append(stage)

    def create_item(self, name: str, force_non_progression: bool = False) -> MM3Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        if item.useful:
            classification |= ItemClassification.useful
        return MM3Item(name, classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choices(list(filler_item_weights.keys()),
                                              weights=list(filler_item_weights.values()))[0]

    def create_items(self) -> None:
        itempool = []
        # grab first robot master
        robot_master = self.item_id_to_name[0x890101 + self.options.starting_robot_master.value]
        self.multiworld.push_precollected(self.create_item(robot_master))
        itempool.extend([self.create_item(name) for name in stage_access_table.keys()
                         if name != robot_master])
        itempool.extend([self.create_item(name) for name in robot_master_weapon_table.keys()])
        itempool.extend([self.create_item(name) for name in rush_item_table.keys()])
        total_checks = 31
        if self.options.consumables in (self.options.consumables.option_1up_etank,
                                        self.options.consumables.option_all):
            total_checks += 33
        if self.options.consumables in (self.options.consumables.option_weapon_health,
                                        self.options.consumables.option_all):
            total_checks += 105
        remaining = total_checks - len(itempool)
        itempool.extend([self.create_item(name)
                         for name in self.multiworld.random.choices(list(filler_item_weights.keys()),
                                                                    weights=list(filler_item_weights.values()),
                                                                    k=remaining)])
        self.multiworld.itempool += itempool

    set_rules = set_rules

    def generate_early(self) -> None:
        if (self.options.starting_robot_master.current_key == "gemini_man"
            and not any(item in self.options.start_inventory for item in rush_item_table.keys())) or \
                (self.options.starting_robot_master.current_key == "hard_man"
                 and not any(item in self.options.start_inventory for item in [rush_coil, rush_jet])):
            robot_master_pool = [0, 1, 4, 5, 6, 7, ]
            if rush_marine in self.options.start_inventory:
                robot_master_pool.append(2)
            self.options.starting_robot_master.value = self.random.choice(robot_master_pool)
            logger.warning(
                f"Incompatible starting Robot Master, changing to "
                f"{self.options.starting_robot_master.current_key.replace('_', ' ').title()}")

    def generate_basic(self) -> None:
        goal_location = self.multiworld.get_location(gamma, self.player)
        goal_location.place_locked_item(MM3Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_hook(self,
                  progitempool: List["Item"],
                  usefulitempool: List["Item"],
                  filleritempool: List["Item"],
                  fill_locations: List["Location"]) -> None:
        # on a solo gen, fill can try to force Wily into sphere 2, but for most generations this is impossible
        # since MM2 can have a 2 item sphere 1, and 3 items are required for Wily
        return # TODO: confirm the behaviors here

    def generate_output(self, output_directory: str) -> None:
        try:
            patch = MM3ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "death_link": self.options.death_link.value,
            "weapon_damage": self.weapon_damage
        }

    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> Dict[str, Any]:
        local_weapon = {int(key): value for key, value in slot_data["weapon_damage"].items()}
        return {"weapon_damage": local_weapon}

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]


import hashlib
import logging
from typing import Any, Sequence, ClassVar

from BaseClasses import Tutorial, ItemClassification, MultiWorld, Item, Location
from worlds.AutoWorld import World, WebWorld
from .names import (gamma, gemini_man_stage, needle_man_stage, hard_man_stage, magnet_man_stage, top_man_stage,
                    snake_man_stage, spark_man_stage, shadow_man_stage, rush_marine, rush_jet, rush_coil)
from .items import (item_table, item_names, MM3Item, filler_item_weights, robot_master_weapon_table,
                    stage_access_table, rush_item_table, lookup_item_to_id)
from .locations import (MM3Location, mm3_regions, MM3Region, energy_pickups, etank_1ups, lookup_location_to_id,
                        location_groups)
from .rom import patch_rom, MM3ProcedurePatch, MM3LCHASH, MM3VCHASH, PROTEUSHASH, MM3NESHASH
from .options import MM3Options, Consumables
from .client import MegaMan3Client
from .rules import set_rules, weapon_damage, robot_masters, weapons_to_name, minimum_weakness_requirement
import os
import threading
import base64
import settings
logger = logging.getLogger("Mega Man 3")


class MM3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MM3 EN rom"""
        description = "Mega Man 3 ROM File"
        copy_to: str | None = "Mega Man 3 (USA).nes"
        md5s = [MM3NESHASH, MM3LCHASH, PROTEUSHASH, MM3VCHASH]

        def browse(self: settings.T,
                   filetypes: Sequence[tuple[str, Sequence[str]]] | None = None,
                   **kwargs: Any) -> settings.T | None:
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
    world_version: tuple[int, int, int] = (0, 1, 2)

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)
        self.weapon_damage = weapon_damage.copy()
        self.wily_4_weapons: dict[int, list[int]] = {}

    def create_regions(self) -> None:
        menu = MM3Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        for region in mm3_regions:
            stage = MM3Region(region, self.player, self.multiworld)
            required_items = mm3_regions[region][0]
            stage_locations = mm3_regions[region][1]
            prev_stage = mm3_regions[region][2]
            if prev_stage is None:
                menu.connect(stage, f"To {region}",
                             lambda state, req=required_items: state.has_all(req, self.player))
            else:
                old_stage = self.multiworld.get_region(prev_stage, self.player)
                old_stage.connect(stage, f"To {region}",
                                  lambda state, req=required_items: state.has_all(req, self.player))
            stage.add_locations(stage_locations)
            for location in stage.get_locations():
                if location.address is None and location.name != gamma:
                    location.place_locked_item(MM3Item(location.name, ItemClassification.progression,
                                                       None, self.player))
            if self.options.consumables in (Consumables.option_1up_etank,
                                            Consumables.option_all):
                if region in etank_1ups:
                    stage.add_locations(etank_1ups[region], MM3Location)
            if self.options.consumables in (Consumables.option_weapon_health,
                                            Consumables.option_all):
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
        if self.options.consumables in (Consumables.option_1up_etank,
                                        Consumables.option_all):
            total_checks += 33
        if self.options.consumables in (Consumables.option_weapon_health,
                                        Consumables.option_all):
            total_checks += 106
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
                  prog_item_pool: list["Item"],
                  useful_item_pool: list["Item"],
                  filler_item_pool: list["Item"],
                  fill_locations: list["Location"]) -> None:
        # on a solo gen, fill can try to force Wily into sphere 2, but for most generations this is impossible
        # MM3 is worse than MM2 here, some of the RBMs can also require Rush
        if self.multiworld.players > 1:
            return  # Don't need to change anything on a multi gen, fill should be able to solve it with a 4 sphere 1
        rbm_to_item = {
            0: needle_man_stage,
            1: magnet_man_stage,
            2: gemini_man_stage,
            3: hard_man_stage,
            4: top_man_stage,
            5: snake_man_stage,
            6: spark_man_stage,
            7: shadow_man_stage
        }
        affected_rbm = [2, 3]  # Gemini and Hard will always have this happen
        possible_rbm = [0, 7]  # Needle and Shadow are always valid targets, due to Rush Marine/Jet receive
        if self.options.consumables:
            possible_rbm.extend([4, 5])  # every stage has at least one of each consumable
            if self.options.consumables in (Consumables.option_weapon_health, Consumables.option_all):
                possible_rbm.extend([1, 6])
            else:
                affected_rbm.extend([1, 6])
        else:
            affected_rbm.extend([1, 4, 5, 6])  # only two checks on non consumables
        if self.options.starting_robot_master.value in affected_rbm:
            rbm_names = list(map(lambda s: rbm_to_item[s], possible_rbm))
            valid_second = [item for item in prog_item_pool
                            if item.name in rbm_names
                            and item.player == self.player]
            placed_item = self.random.choice(valid_second)
            rbm_defeated = (f"{robot_masters[self.options.starting_robot_master.value].replace(' Defeated', '')}"
                            f" - Defeated")
            rbm_location = self.get_location(rbm_defeated)
            rbm_location.place_locked_item(placed_item)
            prog_item_pool.remove(placed_item)
            fill_locations.remove(rbm_location)
            target_rbm = (placed_item.code & 0xF) - 1
            if self.options.strict_weakness or (self.options.random_weakness
                                                and not (self.weapon_damage[0][target_rbm] > 0)):
                # we need to find a weakness for this boss
                weaknesses = [weapon for weapon in range(1, 9)
                              if self.weapon_damage[weapon][target_rbm] >= minimum_weakness_requirement[weapon]]
                weapons = list(map(lambda s: weapons_to_name[s], weaknesses))
                valid_weapons = [item for item in prog_item_pool
                                 if item.name in weapons
                                 and item.player == self.player]
                placed_weapon = self.random.choice(valid_weapons)
                weapon_name = next(name for name, idx in lookup_location_to_id.items()
                                   if idx == 0x890101 + self.options.starting_robot_master.value)
                weapon_location = self.get_location(weapon_name)
                weapon_location.place_locked_item(placed_weapon)
                prog_item_pool.remove(placed_weapon)
                fill_locations.remove(weapon_location)

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

    def fill_slot_data(self) -> dict[str, Any]:
        return {
            "death_link": self.options.death_link.value,
            "weapon_damage": self.weapon_damage
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        local_weapon = {int(key): value for key, value in slot_data["weapon_damage"].items()}
        return {"weapon_damage": local_weapon}

    def modify_multidata(self, multidata: dict[str, Any]) -> None:
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

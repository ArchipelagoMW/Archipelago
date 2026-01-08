import logging

from BaseClasses import Tutorial, ItemClassification, MultiWorld, CollectionState, Item
from Fill import fill_restrictive
from worlds.AutoWorld import World, WebWorld
from .items import item_table, item_names, copy_ability_table, filler_item_weights, K64Item, copy_ability_access_table,\
    power_combo_table, friend_table
from .locations import location_table, K64Location
from .names import LocationName, ItemName
from .regions import create_levels, default_levels
from .rom import K64ProcedurePatch, get_base_rom_path, RomData, patch_rom, K64UHASH
from .client import K64Client
from .options import K64Options
from .rules import set_rules
from typing import Dict, TextIO, Optional, List, Any, Mapping, ClassVar
from io import BytesIO
import os
import math
import threading
import base64
import settings

logger = logging.getLogger("Kirby 64: The Crystal Shards")


class K64Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the K64 EN rom"""
        description = "Kirby 64 - The Crystal Shards ROM File"
        copy_to = "Kirby 64 - The Crystal Shards (USA).z64"
        md5s = [K64UHASH]

        # another day, another UserFilePath reimplementation
        @classmethod
        def validate(cls, path: str) -> None:
            """Try to open and validate file against hashes"""
            with open(path, "rb", buffering=0) as f:
                if path.endswith(".n64"):
                    # little endian, byteswap on the half
                    byte_data = bytearray(f.read())
                    for i in range(0, len(byte_data), 2):
                        temp = byte_data[i]
                        byte_data[i] = byte_data[i + 1]
                        byte_data[i + 1] = temp
                    f = BytesIO(byte_data)
                elif path.endswith(".v64"):
                    # byteswapped, byteswap on the word
                    byte_data = bytearray(f.read())
                    for i in range(0, len(byte_data), 4):
                        temp = byte_data[i]
                        byte_data[i] = byte_data[i + 3]
                        byte_data[i + 1] = byte_data[i + 2]
                        byte_data[i + 2] = byte_data[i + 1]
                        byte_data[i + 3] = temp
                    f = BytesIO(byte_data)
                try:
                    cls._validate_stream_hashes(f)
                except ValueError:
                    raise ValueError(f"File hash does not match for {path}")

    rom_file: RomFile = RomFile(RomFile.copy_to)


class K64WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kirby 64 - The Crystal Shards randomizer connected to an Archipelago Multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Silvris"]
        )
    ]


class K64World(World):
    """
    After Dark Matter attacks the distant Ripple Star's crystal, the young Ribbon attempts to flee with the crystal to save it.
    The crystal shattered, stranding Ribbon in Dream Land. Now it's up to Kirby and friends to travel the galaxy in order to
    restore the shattered crystal, and bring peace to the world.
    """

    game = "Kirby 64 - The Crystal Shards"
    options_dataclass = K64Options
    options: K64Options
    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location_table[location]: location for location in location_table}
    item_name_groups = item_names
    web = K64WebWorld()
    settings: ClassVar[K64Settings]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.stage_shuffle_enabled: bool = False
        self.rom_name = None
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
        self.required_crystals: int = 0  # we fill this during create_items
        self.boss_requirements: List[int] = list()
        self.player_levels = default_levels.copy()

    create_regions = create_levels

    def create_item(self, name: str, force_non_progression=False) -> K64Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        elif item.trap:
            classification = ItemClassification.trap
        return K64Item(name, classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choices(list(filler_item_weights.keys()),
                                   weights=list(filler_item_weights.values()))[0]

    def create_items(self) -> None:
        itempool = []
        itempool.extend([self.create_item(name) for name in copy_ability_table])
        itempool.extend([self.create_item(name) for name in friend_table])
        if self.options.split_power_combos:
            itempool.extend([self.create_item(name) for name in power_combo_table])
        required_percentage = self.options.required_crystals / 100.0
        remaining_items = len(location_table) - len(itempool)
        total_crystals = min(remaining_items, self.options.total_crystals.value)
        required_crystals = max(math.floor(total_crystals * required_percentage), 5)
        # ensure at least 1 crystal shard required
        filler_items = total_crystals - required_crystals
        filler_amount = math.floor(filler_items * (self.options.filler_percentage / 100.0))
        non_required_crystals = filler_items - filler_amount
        self.required_crystals = required_crystals
        # handle boss requirements here
        requirements = [required_crystals]
        quotient = required_crystals // 6  # since we set the last manually, we can afford imperfect rounding
        if self.options.boss_requirement_random:
            for i in range(1, 6):
                max_stars = quotient * i
                requirements.insert(i, self.random.randint(
                    min(1, max_stars), max_stars))
            requirements.sort()
        else:
            for i in range(1, 6):
                requirements.insert(i - 1, quotient * i)
        self.boss_requirements = requirements
        itempool.extend([self.create_item(ItemName.crystal_shard) for _ in range(required_crystals)])
        itempool.extend([self.create_item(self.get_filler_item_name())
                         for _ in range(filler_amount + (remaining_items - total_crystals))])
        itempool.extend([self.create_item(ItemName.crystal_shard, True) for _ in range(non_required_crystals)])
        self.multiworld.itempool += itempool

    set_rules = set_rules

    def generate_basic(self) -> None:
        self.stage_shuffle_enabled = self.options.stage_shuffle.value > 0

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "player_levels": self.player_levels,
            "required_crystals": self.required_crystals,
            "boss_requirements": self.boss_requirements
        }

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]):
        local_levels = {int(key): value for key, value in slot_data["player_levels"].items()}
        return {"player_levels": local_levels}

    def generate_output(self, output_directory: str):
        try:
            rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                      f"{K64ProcedurePatch.patch_file_ending}")
            patch = K64ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch_rom(self, self.player, patch)
            self.rom_name = patch.name
            patch.write(rom_path)
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.stage_shuffle_enabled:
            spoiler_handle.write(f"\nLevel Layout ({self.multiworld.get_player_name(self.player)}):\n")
            for level in LocationName.level_names_inverse:
                for stage, i in zip(self.player_levels[LocationName.level_names_inverse[level]], range(1, 7)):
                    spoiler_handle.write(f"{level} {i}: {location_table[stage].replace(' - Complete', '')}\n")

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        value = super().collect(state, item)

        if not self.boss_requirements:
            return value

        crystals = state.prog_items[self.player][ItemName.crystal_shard]
        level_state = [crystals >= requirement for requirement in self.boss_requirements]
        if state.k64_level_state[self.player] != level_state:
            state.k64_stale[self.player] = True
        return value

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        value = super().remove(state, item)

        if not self.boss_requirements:
            return value

        crystals = state.prog_items[self.player][ItemName.crystal_shard]
        level_state = [crystals >= requirement for requirement in self.boss_requirements]
        if state.k64_level_state[self.player] != level_state:
            state.k64_stale[self.player] = True
        return value

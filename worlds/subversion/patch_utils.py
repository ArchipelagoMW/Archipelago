from dataclasses import dataclass
from enum import IntEnum
from itertools import chain
import json
from pathlib import Path
from typing import Dict, Final, List, Mapping, Optional, Set, Tuple, Union

from BaseClasses import ItemClassification, Location

from .config import base_id, open_file_apworld_compatible
from .item import SubversionItem, local_id_to_sv_item, name_to_id, sv_item_name_to_sm_item_id
from .location import SubversionLocation

from subversion_rando.game import Game as SvGame
from subversion_rando.ips import patch as ips_patch
from subversion_rando.item_data import Items
from subversion_rando.romWriter import RomWriter

LOGIC_LOCATION = 0xFEE4
LOGIC_LENGTH = 12

box_blue_tbl = {
    "A": 0x2CC0,
    "B": 0x2CC1,
    "C": 0x2CC2,
    "D": 0x2CC3,
    "E": 0x2CC4,
    "F": 0x2CC5,
    "G": 0x2CC6,
    "H": 0x2CC7,
    "I": 0x2CC8,
    "J": 0x2CC9,
    "K": 0x2CCA,
    "L": 0x2CCB,
    "M": 0x2CCC,
    "N": 0x2CCD,
    "O": 0x2CCE,
    "P": 0x2CCF,
    "Q": 0x2CD0,
    "R": 0x2CD1,
    "S": 0x2CD2,
    "T": 0x2CD3,
    "U": 0x2CD4,
    "V": 0x2CD5,
    "W": 0x2CD6,
    "X": 0x2CD7,
    "Y": 0x2CD8,
    "Z": 0x2CD9,
    " ": 0x2C0F,
    "!": 0x2CDF,
    "?": 0x2CDE,
    "'": 0x2CDC,
    ",": 0xACDC,
    ".": 0x2CDA,
    "-": 0x2CDD,
    "_": 0x000E,  # character used for edges of screen during text box
    "1": 0x2C01,
    "2": 0x2C02,
    "3": 0x2C03,
    "4": 0x2C04,
    "5": 0x2C05,
    "6": 0x2C06,
    "7": 0x2C07,
    "8": 0x2C08,
    "9": 0x2C09,
    "0": 0x2C00,
    "%": 0x2C0A,
}
""" item names use this, player names are ascii """


def get_word_array(w: int) -> Tuple[int, int]:
    """ little-endian convert a 16-bit number to an array of numbers <= 255 each """
    return (w & 0x00FF, (w & 0xFF00) >> 8)


def make_item_name_for_rom(item_name: str) -> bytearray:
    """ 64 bytes (32 chars) centered, encoded with box_blue.tbl """
    data = bytearray()

    item_name = item_name.upper()[:26]
    item_name = item_name.strip()
    item_name = item_name.replace("_", " ")
    item_name = item_name.center(26, " ")
    item_name = "___" + item_name + "___"
    assert len(item_name) == 32, f"{len(item_name)=}"

    for char in item_name:
        w0, w1 = get_word_array(box_blue_tbl.get(char, 0x2C0F))
        data.append(w0)
        data.append(w1)
    assert len(data) == 64, f"{len(data)=}"
    return data


_symbols: Optional[Dict[str, str]] = None


def offset_from_symbol(symbol: str) -> int:
    global _symbols
    if _symbols is None:
        path = Path(__file__).parent.resolve()
        json_path = path.joinpath("data", "ap_subversion_patch", "sm-basepatch-symbols.json")
        with open_file_apworld_compatible(json_path) as symbols_file:
            _symbols = json.load(symbols_file)
        assert _symbols

    snes_addr_str = _symbols[symbol]
    snes_addr_str = "".join(snes_addr_str.split(":"))
    snes_addr = int(snes_addr_str, 16)
    offset = RomWriter.snes_to_index_addr(snes_addr)
    return offset


_item_sprites = [
    {
        "fileName":          "off_world_prog_item.bin",
        "paletteSymbolName": "prog_item_eight_palette_indices",
        "dataSymbolName":    "offworld_graphics_data_progression_item"
    },
    {
        "fileName":          "off_world_item.bin",
        "paletteSymbolName": "nonprog_item_eight_palette_indices",
        "dataSymbolName":    "offworld_graphics_data_item"
    }
]


def patch_item_sprites(rom: Union[bytes, bytearray]) -> bytearray:
    """
    puts the 2 new off-world item sprites in the rom

    takes sprites from Super Metroid world directory
    """
    tr = bytearray(rom)

    path = Path(__file__).parent.resolve()

    for item_sprite in _item_sprites:
        palette_offset = offset_from_symbol(item_sprite["paletteSymbolName"])
        data_offset = offset_from_symbol(item_sprite["dataSymbolName"])
        with open_file_apworld_compatible(
            path.joinpath("data", "custom_sprite", item_sprite["fileName"]), 'rb'
        ) as file:
            offworld_data = file.read()
            tr[palette_offset:palette_offset + 8] = offworld_data[0:8]
            tr[data_offset:data_offset + 256] = offworld_data[8:264]
    return tr


# copied from SM
_SMZ3_name_to_SM_type: Dict[str, str] = {
    "ETank": "ETank", "Missile": "Missile", "Super": "Super", "PowerBomb": "PowerBomb", "Bombs": "Bomb",
    "Charge": "Charge", "Ice": "Ice", "HiJump": "HiJump", "SpeedBooster": "SpeedBooster",
    "Wave": "Wave", "Spazer": "Spazer", "SpringBall": "SpringBall", "Varia": "Varia", "Plasma": "Plasma",
    "Grapple": "Grapple", "Morph": "Morph", "ReserveTank": "Reserve", "Gravity": "Gravity",
    "XRay": "XRayScope", "SpaceJump": "SpaceJump", "ScrewAttack": "ScrewAttack"
}

try:
    from worlds.sm.variaRandomizer.rando.Items import ItemManager
    _SMZ3_name_to_SM_name: Dict[str, str] = {
        smz3_name: ItemManager.Items[sm_type].Name
        for smz3_name, sm_type in _SMZ3_name_to_SM_type.items()
    }
except ImportError:
    _SMZ3_name_to_SM_name = {}

_SM_name_to_subversion_name: Dict[str, str] = {
    "Energy Tank": Items.Energy.name,
    "Missile": Items.Missile.name,
    "Super Missile": Items.Super.name,
    "Power Bomb": Items.PowerBomb.name,
    "Bomb": Items.Bombs.name,
    "Charge Beam": Items.Charge.name,
    "Ice Beam": Items.Ice.name,
    "Hi-Jump Boots": Items.HiJump.name,
    "Speed Booster": Items.SpeedBooster.name,
    "Wave Beam": Items.Wave.name,
    "Spazer": Items.Spazer.name,
    "Spring Ball": Items.Speedball.name,
    "Varia Suit": Items.Varia.name,
    "Plasma Beam": Items.Plasma.name,
    "Grappling Beam": Items.Grapple.name,
    "Morph Ball": Items.Morph.name,
    "Reserve Tank": Items.Refuel.name,
    "Gravity Suit": Items.Aqua.name,
    "X-Ray Scope": Items.Xray.name,
    "Space Jump": Items.SpaceJump.name,
    "Screw Attack": Items.Screw.name,
}
""" for sprites that look the same """


class _DestinationType(IntEnum):
    Me = 0
    Other = 1
    LinkWithMe = 2


@dataclass
class _ItemTableEntry:
    destination: _DestinationType
    item_id: int
    player_index: int
    advancement: bool

    def to_bytes(self) -> bytes:
        return (self.destination.to_bytes(2, "little") +
                self.item_id.to_bytes(2, "little") +
                self.player_index.to_bytes(2, "little") +
                self.advancement.to_bytes(2, "little"))


SMZ3_ITEM_GAME_NAME = "SMZ3"
SM_ITEM_GAME_NAME = "Super Metroid"

NUM_ITEMS_WITH_ICONS = len(local_id_to_sv_item) + len(sv_item_name_to_sm_item_id)

ItemNames_ItemTable_PlayerNames_PlayerIDs = Tuple[List[bytearray], Dict[int, _ItemTableEntry], bytearray, List[int]]

ItemNames_ItemTable_PlayerNames_PlayerIDs_JSON = Tuple[List[List[int]], Dict[str, List[int]], List[int], List[int]]


class ItemRomData:
    player: Final[int]
    """ my AP id for this game """
    troll_ammo: Final[bool]
    """ whether I have the troll ammo option on """
    my_locations: List[SubversionLocation]
    """ locations in my world """
    player_ids: Set[int]
    """ all the players I interact with (including myself and 0 (the server player)) """
    player_id_to_name: Mapping[int, str]

    def __init__(self, my_player_id: int, troll_ammo: bool, player_id_to_name: Mapping[int, str]) -> None:
        self.player = my_player_id
        self.troll_ammo = troll_ammo
        self.my_locations = []
        self.player_ids = {0, my_player_id}
        self.player_id_to_name = player_id_to_name

    def register(self, loc: Location) -> None:
        """ call this with every multiworld location """
        if loc.player == self.player:
            # my location
            assert isinstance(loc, SubversionLocation)
            if not loc.item:
                # This function should only be called after fill is complete.
                raise ValueError("got a location with no item")
            self.player_ids.add(loc.item.player)
            self.my_locations.append(loc)
        else:  # not my location
            if loc.item and loc.item.player == self.player:
                # my item in someone else's location
                self.player_ids.add(loc.player)

    def _make_tables(self) -> ItemNames_ItemTable_PlayerNames_PlayerIDs:
        """ after all locations are registered """
        item_table: Dict[int, _ItemTableEntry] = {}

        item_names_after_constants: List[bytearray] = []

        sorted_player_ids = sorted(self.player_ids)
        if len(sorted_player_ids) > 246:  # magic number from asm patch
            from logging import getLogger
            logger = getLogger("Subversion")
            logger.warning(f"How am I interacting with {len(sorted_player_ids)} when I only have 122 locations?")
            # this should never happen
            sorted_player_ids = sorted_player_ids[:246]
            if self.player > sorted_player_ids[-1]:
                sorted_player_ids[-1] = self.player

        # id in this game to index in rom tables
        player_id_to_index = {
            id_: i
            for i, id_ in enumerate(sorted_player_ids)
        }

        for loc in self.my_locations:
            sv_loc = loc.sv_loc
            sv_loc_ids = [sv_loc["plmparamlo"]]
            if sv_loc["alternateplmparamlo"]:
                # 2 locations with the same item (example: aft battery and wrecked aft battery)
                sv_loc_ids.append(sv_loc["alternateplmparamlo"])
            assert loc.item
            progression = bool(loc.item.classification & ItemClassification.progression)
            player_index = player_id_to_index.get(loc.item.player, 0)  # 0 player is Archipelago
            if loc.item.player == self.player:
                # my item in my location
                assert loc.item.code
                table_entry = _ItemTableEntry(
                    _DestinationType.Me,
                    loc.item.code - base_id,
                    player_index,
                    progression
                )
            else:  # someone else's item in my location
                # TODO: check for item links that include me
                item_id = NUM_ITEMS_WITH_ICONS + len(item_names_after_constants)
                # items we can display from other games
                if loc.item.game == SMZ3_ITEM_GAME_NAME and loc.item.name in _SMZ3_name_to_SM_name:
                    sm_name = _SMZ3_name_to_SM_name[loc.item.name]
                    sv_name = _SM_name_to_subversion_name[sm_name]
                    if self.troll_ammo or (sv_name not in (Items.Missile.name, Items.Super.name, Items.PowerBomb.name)):
                        item_id = name_to_id[sv_name] - base_id
                        if sv_name in sv_item_name_to_sm_item_id:
                            # reserve tank or gravity suit or spring ball, because of the different names
                            item_id = sv_item_name_to_sm_item_id[sv_name]
                elif loc.item.game == SM_ITEM_GAME_NAME and loc.item.name in _SM_name_to_subversion_name:
                    sv_name = _SM_name_to_subversion_name[loc.item.name]
                    if self.troll_ammo or (sv_name not in (Items.Missile.name, Items.Super.name, Items.PowerBomb.name)):
                        item_id = name_to_id[sv_name] - base_id
                        if sv_name in sv_item_name_to_sm_item_id:
                            # reserve tank or gravity suit or spring ball, because of the different names
                            item_id = sv_item_name_to_sm_item_id[sv_name]
                elif isinstance(loc.item, SubversionItem):
                    # someone else's subversion item in my location
                    assert loc.item.code
                    item_id = loc.item.code - base_id
                if item_id == NUM_ITEMS_WITH_ICONS + len(item_names_after_constants):
                    # if we didn't find a subversion sprite for this item
                    item_names_after_constants.append(make_item_name_for_rom(loc.item.name))

                table_entry = _ItemTableEntry(
                    _DestinationType.Other,
                    item_id,
                    player_index,
                    progression
                )

            for loc_id in sv_loc_ids:
                item_table[loc_id] = table_entry

        player_names = bytearray()
        player_names.extend(b"  Archipelago   ")
        for player_id in sorted_player_ids[1:]:
            this_name = self.player_id_to_name[player_id].upper().encode("ascii", "ignore")[:16].center(16)
            player_names.extend(this_name)

        return item_names_after_constants, item_table, player_names, sorted_player_ids

    def patch_tables(self, rom: Union[bytes, bytearray]) -> bytearray:
        """
        after calling register on all locations

        input rom, output patched rom
        """
        tr = bytearray(rom)
        item_names_after_constants, item_table, player_names, sorted_player_ids = self._make_tables()

        item_names_offset = offset_from_symbol("item_names") + 64 * NUM_ITEMS_WITH_ICONS
        concat_bytes = b"".join(item_names_after_constants)
        tr[item_names_offset:item_names_offset + len(concat_bytes)] = concat_bytes

        item_table_offset = offset_from_symbol("rando_item_table")
        for index, entry in item_table.items():
            data = entry.to_bytes()
            this_offset = item_table_offset + index * len(data)
            tr[this_offset:this_offset + len(data)] = data

        player_name_offset = offset_from_symbol("rando_player_name_table")
        tr[player_name_offset:player_name_offset + len(player_names)] = player_names

        player_id_offset = offset_from_symbol("rando_player_id_table")
        for i, id_ in enumerate(sorted_player_ids):
            this_offset = player_id_offset + i * 2
            tr[this_offset:this_offset + 2] = id_.to_bytes(2, "little")

        return tr

    def get_jsonable_data(self) -> ItemNames_ItemTable_PlayerNames_PlayerIDs_JSON:
        """ data that can be encoded to json, and can be passed to `patch_from_json` """
        item_names_after_constants, item_table, player_names, sorted_player_ids = self._make_tables()

        return (
            [list(item_name) for item_name in item_names_after_constants],
            {str(loc_id): list(entry.to_bytes()) for loc_id, entry in item_table.items()},
            list(player_names),
            sorted_player_ids
        )

    @staticmethod
    def patch_from_json(
        rom: Union[bytes, bytearray],
        json_result: ItemNames_ItemTable_PlayerNames_PlayerIDs_JSON
    ) -> bytearray:
        tr = bytearray(rom)
        item_names_after_constants, item_table, player_names, sorted_player_ids = json_result

        item_names_offset = offset_from_symbol("item_names") + 64 * NUM_ITEMS_WITH_ICONS
        concat_bytes = bytes(chain.from_iterable(item_names_after_constants))
        tr[item_names_offset:item_names_offset + len(concat_bytes)] = concat_bytes

        item_table_offset = offset_from_symbol("rando_item_table")
        for index, entry in item_table.items():
            data = bytes(entry)
            this_offset = item_table_offset + int(index) * len(data)
            tr[this_offset:this_offset + len(data)] = data

        player_name_offset = offset_from_symbol("rando_player_name_table")
        tr[player_name_offset:player_name_offset + len(player_names)] = player_names

        player_id_offset = offset_from_symbol("rando_player_id_table")
        for i, id_ in enumerate(sorted_player_ids):
            this_offset = player_id_offset + i * 2
            tr[this_offset:this_offset + 2] = id_.to_bytes(2, "little")

        return tr


def ips_patch_from_file(ips_file_name: Union[str, Path], input_bytes: Union[bytes, bytearray]) -> bytearray:
    with open_file_apworld_compatible(ips_file_name, "rb") as ips_file:
        ips_data = ips_file.read()
    return ips_patch(input_bytes, ips_data)


def get_multi_patch_path() -> Path:
    """ multiworld-basepatch.ips """
    path = Path(__file__).parent.resolve()
    return path.joinpath("data", "ap_subversion_patch", "multiworld-basepatch.ips")


@dataclass
class GenData:
    item_rom_data: ItemNames_ItemTable_PlayerNames_PlayerIDs_JSON
    sv_game: SvGame
    player: int
    game_name_in_rom: Union[bytes, bytearray]


def make_gen_data(data: GenData) -> str:
    """ serialized data from generation needed to patch rom """
    jsonable = {
        "item_rom_data": data.item_rom_data,
        "sv_game": data.sv_game.to_jsonable(),
        "player": data.player,
        "game_name_in_rom": list(data.game_name_in_rom)
    }
    return json.dumps(jsonable)


def get_gen_data(gen_data_str: str) -> GenData:
    """ the reverse of `make_gen_data` """
    from_json = json.loads(gen_data_str)
    return GenData(
        from_json["item_rom_data"],
        SvGame.from_jsonable(from_json["sv_game"]),
        from_json["player"],
        bytes(from_json["game_name_in_rom"])
    )

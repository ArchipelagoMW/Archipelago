from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from .constants.game_data import navigation_text_ptrs
from .constants.reserved_space import ReservedConstantsMF
from ..rom import Rom
from ..text import Language, MessageType, encode_text

if TYPE_CHECKING:
    from .auto_generated_types import Hintlocks, MarsschemamfNavstationlocksKey
    from ..rom import Rom


class NavRoom(Enum):
    MAIN_DECK_WEST = 1
    MAIN_DECK_EAST = 2
    OPERATIONS_DECK = 3
    SECTOR1_ENTRANCE = 4
    SECTOR5_ENTRANCE = 5
    SECTOR2_ENTRANCE = 6
    SECTOR4_ENTRANCE = 7
    SECTOR3_ENTRANCE = 8
    SECTOR6_ENTRANCE = 9
    AUXILIARY_POWER = 10
    RESTRICTED_LABS = 11


# Later down the line, when/if Nav terminals don't have their
# confirm text patched out, combine these two.
class ShipText(Enum):
    INITIAL_TEXT = 0
    CONFIRM_TEXT = 1


class NavStationLockType(Enum):
    OPEN = 0xFF
    LOCKED = 0x05
    GREY = 0x00
    BLUE = 0x01
    GREEN = 0x02
    YELLOW = 0x03
    RED = 0x04


class NavigationText:
    LANG_ENUMS = {
        "JapaneseKanji": Language.JAPANESE_KANJI,
        "JapaneseHiragana": Language.JAPANESE_HIRAGANA,
        "English": Language.ENGLISH,
        "German": Language.GERMAN,
        "French": Language.FRENCH,
        "Italian": Language.ITALIAN,
        "Spanish": Language.SPANISH,
    }

    NAV_ROOM_ENUMS: dict[MarsschemamfNavstationlocksKey, NavRoom] = {
        "MainDeckWest": NavRoom.MAIN_DECK_WEST,
        "MainDeckEast": NavRoom.MAIN_DECK_EAST,
        "OperationsDeck": NavRoom.OPERATIONS_DECK,
        "Sector1Entrance": NavRoom.SECTOR1_ENTRANCE,
        "Sector2Entrance": NavRoom.SECTOR2_ENTRANCE,
        "Sector3Entrance": NavRoom.SECTOR3_ENTRANCE,
        "Sector4Entrance": NavRoom.SECTOR4_ENTRANCE,
        "Sector5Entrance": NavRoom.SECTOR5_ENTRANCE,
        "Sector6Entrance": NavRoom.SECTOR6_ENTRANCE,
        "AuxiliaryPower": NavRoom.AUXILIARY_POWER,
        "RestrictedLabs": NavRoom.RESTRICTED_LABS,
    }

    GAME_START_CHAR = "[GAME_START]"
    INITIAL_TEXT_KEY = "InitialText"
    NAV_TERMINALS_KEY = "NavigationTerminals"
    SHIP_TEXT_KEY = "ShipText"

    INFO_TEXT_ENUMS = {
        INITIAL_TEXT_KEY: ShipText.INITIAL_TEXT,
        "ConfirmText": ShipText.CONFIRM_TEXT,
    }

    def __init__(self, navigation_text: dict[Language, dict[str, dict[Enum, str]]]):
        self.navigation_text = navigation_text

    @classmethod
    def from_json(cls, data: dict) -> NavigationText:
        navigation_text: dict[Language, dict[str, dict[Enum, str]]] = {}
        for lang, lang_text in data.items():
            lang = cls.LANG_ENUMS[lang]
            navigation_text[lang] = {
                cls.NAV_TERMINALS_KEY: {
                    cls.NAV_ROOM_ENUMS[k]: v for k, v in lang_text[cls.NAV_TERMINALS_KEY].items()
                },
                cls.SHIP_TEXT_KEY: {
                    # Make sure initial text string starts with [GAME_START]
                    cls.INFO_TEXT_ENUMS[k]: cls.GAME_START_CHAR + v
                    if k == cls.INITIAL_TEXT_KEY and not v.startswith(cls.GAME_START_CHAR)
                    else v
                    for k, v in lang_text[cls.SHIP_TEXT_KEY].items()
                },
            }
        return cls(navigation_text)

    def write(self, rom: Rom) -> None:
        for lang, lang_texts in self.navigation_text.items():
            base_text_address = rom.read_ptr(navigation_text_ptrs(rom) + lang.value * 4)

            # Info Text
            for info_place, text in lang_texts["ShipText"].items():
                encoded_text = encode_text(rom, MessageType.CONTINUOUS, text)
                text_addr = rom.reserve_free_space(len(encoded_text) * 2)
                rom.write_ptr(base_text_address + info_place.value * 4, text_addr)
                rom.write_ptr(base_text_address + info_place.value * 4 + 4, text_addr)
                rom.write_16_list(text_addr, encoded_text)

            # Navigation Text
            for nav_room, text in lang_texts["NavigationTerminals"].items():
                encoded_text = encode_text(rom, MessageType.CONTINUOUS, text)
                text_addr = rom.reserve_free_space(len(encoded_text) * 2)
                rom.write_ptr(base_text_address + nav_room.value * 8, text_addr)
                rom.write_ptr(base_text_address + nav_room.value * 8 + 4, text_addr)
                rom.write_16_list(text_addr, encoded_text)

    @classmethod
    def apply_hint_security(
        cls, rom: Rom, locks: dict[MarsschemamfNavstationlocksKey, Hintlocks]
    ) -> None:
        """
        Applies an optional security level requirement to use Navigation Stations
        Defaults to OPEN if not provided in patch data JSON
        """
        default_lock_name = "OPEN"
        for location, offset in NavigationText.NAV_ROOM_ENUMS.items():
            rom.write_8(
                rom.read_ptr(ReservedConstantsMF.HINT_SECURITY_LEVELS_ADDR) + offset.value,
                NavStationLockType[locks.get(location, default_lock_name)].value,
            )

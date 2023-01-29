from __future__ import annotations

from typing import Dict

from Options import Choice, Option, DefaultOnToggle, DeathLink


class ItemRandoType(Choice):
    """Choose how items are placed in the game

    Not yet implemented.  Currently only Hidden supported
    Hidden: Adventure items are not in the map until
    they are collected (except local items) and are dropped
    on the player when collected.  Adventure items are not checks.
    Drained: Every item is placed, but is inactive until collected.
    Each item touched is a check.  The bat ignores inactive items.

    Supported values: traditional, inactive
    Default value: traditional
    """

    display_name = "Item type"
    option_traditional = 0x00
    option_inactive = 0x01
    default = option_traditional


class DragonSlayCheck(DefaultOnToggle):
    """If true, slaying each dragon for the first time is a check
    Not yet implemented
    """
    display_name = "Slay Dragon Checks"


class TrapBatCheck(Choice):
    """
    Locking the bat inside a castle may be a check

    Not yet implemented
    If set to yes, the bat will not start inside a castle.
    Setting with_key requires the matching castle key to also be
    in the castle with the bat, achieved by dropping the key in the
    path of the portcullis as it falls.  This setting is not recommended with the bat use_logic setting

    Supported values: no, yes, with_key
    Default value: yes
    """
    display_name = "Trap bat check"
    option_no_check = 0x0
    option_yes_key_optional = 0x1
    option_with_key = 0x2
    default = option_yes_key_optional


class BatLogic(Choice):
    """How the bat is considered for logic

    Not yet implemented
    With cannot_break, the bat cannot pick up an item that starts out-of-logic until the player touches it
    With can_break, the bat is free to pick up local adventure items, even if they are out-of-logic
    With use_logic, the bat itself is placed as an item and can be required for logic for some locations, such
    as the credits room.  This can make the bat required to get certain items, and potentially tedious.  And also
    is not recommended with TrapBatCheck set to with_key

    Supported values: cannot_break, can_break, use_logic
    Default value: cannot_break
    """
    display_name = "Bat Logic"
    option_cannot_break = 0x0
    option_can_break = 0x1
    option_use_logic = 0x2
    default = option_can_break


adventure_option_definitions: Dict[str, type(Option)] = {
    "item_rando_type": ItemRandoType,
    "dragon_slay_check": DragonSlayCheck,
    "trap_bat_check": TrapBatCheck,
    "death_link": DeathLink,
    "bat_logic": BatLogic

}
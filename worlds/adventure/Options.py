from __future__ import annotations

from typing import Dict

from Options import Choice, Option, DefaultOnToggle, DeathLink, Range, Toggle


class FreeincarnateMax(Range):
    """How many maximum freeincarnate items to allow

    When done generating items, any remaining item slots will be filled
    with freeincarnates, up to this maximum amount.  Any remaining item
    slots after that will be 'nothing' items placed locally, so in multigame
    multiworlds, keeping this value high will allow more items from other games
    into Adventure.
    """
    display_name = "Freeincarnate Maximum"
    range_start = 0
    range_end = 17
    default = 17


class ItemRandoType(Choice):
    """Choose how items are placed in the game

    Not yet implemented.  Currently only traditional supported
    Traditional: Adventure items are not in the map until
    they are collected (except local items) and are dropped
    on the player when collected.  Adventure items are not checks.
    Inactive: Every item is placed, but is inactive until collected.
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


class DragonRandoType(Choice):
    """
    How to randomize the dragon starting locations

    normal: Grundle is in the overworld, Yorgle in the white castle, and Rhindle in the black castle
    shuffle: A random dragon is placed in the overworld, one in the white castle, and one in the black castle
    overworldplus: Dragons can be placed anywhere, but at least one will be in the overworld
    randomized: Dragons can be anywhere except the credits room


    Supported values: normal, shuffle, overworldplus, randomized
    Default value: shuffle
    """
    display_name = "Dragon Randomization"
    option_normal = 0x0
    option_shuffle = 0x1
    option_overworldplus = 0x2
    option_randomized = 0x3
    default = option_shuffle


class BatLogic(Choice):
    """How the bat is considered for logic

    With cannot_break, the bat cannot pick up an item that starts out-of-logic until the player touches it
    With can_break, the bat is free to pick up any items, even if they are out-of-logic
    With use_logic, the bat can pick up anything just like can_break, and locations are no longer considered to require
      the magnet or bridge to collect, since the bat can retrieve these.
    A future option may allow the bat itself to be placed as an item.

    Supported values: cannot_break, can_break, use_logic
    Default value: can_break
    """
    display_name = "Bat Logic"
    option_cannot_break = 0x0
    option_can_break = 0x1
    option_use_logic = 0x2
    default = option_can_break


class YorgleStartingSpeed(Range):
    """
    Sets Yorgle's initial speed.  Yorgle has a speed of 2 in the original game
    Default value: 2
    """
    display_name = "Yorgle MaxSpeed"
    range_start = 1
    range_end = 9
    default = 2


class YorgleMinimumSpeed(Range):
    """
    Sets Yorgle's speed when all speed reducers are found.  Yorgle has a speed of 2 in the original game
    Default value: 2
    """
    display_name = "Yorgle Min Speed"
    range_start = 1
    range_end = 9
    default = 1


class GrundleStartingSpeed(Range):
    """
    Sets Grundle's initial speed.  Grundle has a speed of 2 in the original game
    Default value: 2
    """
    display_name = "Grundle MaxSpeed"
    range_start = 1
    range_end = 9
    default = 2


class GrundleMinimumSpeed(Range):
    """
    Sets Grundle's speed when all speed reducers are found.  Grundle has a speed of 2 in the original game
    Default value: 2
    """
    display_name = "Grundle Min Speed"
    range_start = 1
    range_end = 9
    default = 1


class RhindleStartingSpeed(Range):
    """
    Sets Rhindle's initial speed.  Rhindle has a speed of 3 in the original game
    Default value: 3
    """
    display_name = "Rhindle MaxSpeed"
    range_start = 1
    range_end = 9
    default = 3


class RhindleMinimumSpeed(Range):
    """
    Sets Rhindle's speed when all speed reducers are found.  Rhindle has a speed of 3 in the original game
    Default value: 2
    """
    display_name = "Rhindle Min Speed"
    range_start = 1
    range_end = 9
    default = 2


class ConnectorMultiSlot(Toggle):
    """If true, the client and lua connector will add lowest 8 bits of the player slot
    to the port number used to connect to each other, to simplify connecting multiple local
    clients to local EmuHawk instances.
    Set in the yaml, since the connector has to read this out of the rom file before connecting.
    """
    display_name = "Connector Multi-Slot"


class DifficultySwitchA(Choice):
    """Set availability of left difficulty switch
    This controls the speed of the dragons' bite animation

    """
    display_name = "Left Difficulty Switch"
    option_normal = 0x0
    option_locked_hard = 0x1
    option_hard_with_unlock_item = 0x2
    default = option_hard_with_unlock_item


class DifficultySwitchB(Choice):
    """Set availability of right difficulty switch
    On hard, dragons will run away from the sword

    """
    display_name = "Right Difficulty Switch"
    option_normal = 0x0
    option_locked_hard = 0x1
    option_hard_with_unlock_item = 0x2
    default = option_hard_with_unlock_item


class StartCastle(Choice):
    """Choose or randomize which castle to start in front of.

    This affects both normal start and reincarnation.  Starting
    at the black castle may give easy dot runs, while starting
    at the white castle may make them more dangerous!  Also, not
    starting at the yellow castle can make delivering the chalice
    with a full inventory slightly less trivial.

    This doesn't affect logic since all the castles are reachable
    from each other.
    """
    display_name = "Start Castle"
    option_yellow = 0
    option_black = 1
    option_white = 2
    default = option_yellow


adventure_option_definitions: Dict[str, type(Option)] = {
    "dragon_slay_check": DragonSlayCheck,
    "death_link": DeathLink,
    "bat_logic": BatLogic,
    "freeincarnate_max": FreeincarnateMax,
    "dragon_rando_type": DragonRandoType,
    "connector_multi_slot": ConnectorMultiSlot,
    "yorgle_speed": YorgleStartingSpeed,
    "yorgle_min_speed": YorgleMinimumSpeed,
    "grundle_speed": GrundleStartingSpeed,
    "grundle_min_speed": GrundleMinimumSpeed,
    "rhindle_speed": RhindleStartingSpeed,
    "rhindle_min_speed": RhindleMinimumSpeed,
    "difficulty_switch_a": DifficultySwitchA,
    "difficulty_switch_b": DifficultySwitchB,
    "start_castle": StartCastle,

}
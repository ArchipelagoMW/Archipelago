from dataclasses import dataclass

import typing
from Options import Option, DefaultOnToggle, Choice, Range, Toggle, PerGameCommonOptions


class StarPieceGoal(Choice):
    """
    Six or seven Star Pieces to fight Smithy.
    """
    display_name = "Star Piece Goal"
    option_six = 0
    option_seven = 1


class StarPiecesInBowsersKeep(DefaultOnToggle):
    """
    Star Pieces can be located on the Bowser's Keep boss slots: Magikoopa, Boomer, and Exor.
    If toggled off, Bowser's Keep will be unavailable until the requisite number of Star Pieces have been
    obtained and will be your route to the Factory. If toggled on, the Factory is opened as soon as the requisite
    number of Star Pieces have been obtained.
    """
    display_name = "Star Pieces in Bowser's Keep"


class BowsersKeepDoors(Range):
    """
    How many doors required to clear the middle of Bowser's Keep.
    """
    display_name = "Bowser's Keep Doors"
    range_start = 1
    range_end = 6
    default = 2


class ShuffleBowsersKeepDoors(DefaultOnToggle):
    """
    If toggled on, each door could contain any three rooms from the six doors. If toggled off, behaves like vanilla:
    two action doors, two battle doors, two puzzle doors.
    """
    display_name = "Shuffle Bowser's Keep Doors"


class IncludeCulex(DefaultOnToggle):
    """
    A Star Piece might be located on the boss in Culex's Lair, and Culex's reward (normally the Quartz Charm)
    might be required. Shuffles Culex into the boss pool.
    """
    display_name = "Include Culex"


class ExperienceMultiplier(Choice):
    """
    Multiplies the amount of experience points gained from battling enemies.
    """
    display_name = "Experience Multiplier"
    option_single = 0
    option_double = 1
    option_triple = 2
    default = 1

class RandomizeEnemies(Choice):
    """
    Randomize all enemies. Mild randomizes their drops and formations. Moderate includes enemy stats and attack
    stats and effects. Severe includes their spell lists. Extreme is Severe, but with no safety checks -- have fun!
    """
    display_name = "Randomize Enemies"
    option_none = 0
    option_mild = 1
    option_moderate = 2
    option_severe = 3
    option_extreme = 4
    default = 1


class RandomizeBosses(DefaultOnToggle):
    """
    Randomize boss locations. Bosses will have their stats scaled to their location. This doesn't include spell stats:
    Breaker Beam will still hurt coming from Croco's slot.
    """
    display_name = "Randomize Bosses"


class RandomizeCharacterStats(DefaultOnToggle):
    """
    Stats for each character will be randomized.
    """
    display_name = "Randomize Character Stats"


class RandomizeCharacterSpells(DefaultOnToggle):
    """
    Randomize character learned spells and their spell powers
    """
    display_name = "Randomize Character Spells"


class StartingCharacterCount(Choice):
    """
    Start with one or three characters. Clearing Forest Maze or Marrymore will recruit a new character. If starting
    with one character, clearing Mushroom Way or Moleville will recruit a new character as well.
    """
    display_name = "Starting Character Count"
    option_one = 0
    option_three = 1
    default = 1


class StartingCharacter(Choice):
    """
    Choose which character you start with. If starting with three characters, this chooses the first one.
    """
    display_name = "Starting Character"
    option_mario = 0
    option_mallow = 1
    option_geno = 2
    option_bowser = 3
    option_toadstool = 4
    default = "random"


class RandomizeCharacterPalettes(DefaultOnToggle):
    """
    Randomize character palettes. Some come with fun names!
    """
    display_name = "Randomize Character Palettes"


class RandomizeEquipment(Choice):
    """
    Randomize equipment. Mild randomizes who can equip each piece of gear. Moderate randomizes stats and buffs. Severe
    removes safety checks for the status protection pins guarding against their status and a minimum number of instant
    KO protection items.
    """
    display_name = "Randomize Equipment"
    option_none = 0
    option_mild = 1
    option_moderate = 2
    option_severe = 3
    default = 1

class ItemPool(Choice):
    """
    Adjusts the items available. Vanilla shuffles the vanilla item rewards around. Shuffled types will randomize
    items to be the same type of item (consumbles -> consumables, weapons -> weapons). Shuffled inventories randomizes
    items within their general category (items -> items, gear -> gear). Chaotic will fully randomize each item.
    """
    display_name = "Item Pool"
    option_vanilla = 0
    option_shuffled_types = 1
    option_shuffled_inventories = 2
    option_chaotic = 3
    default = 0


class SuperJumpsInLogic(Toggle):
    """
    Toggled on, this allows progression items to be at the rewards for thirty and one hundred Super Jumps.
    Toggled off, those locations will never be required (but could hold something useful)
    """
    display_name = "Super Jumps In Logic"


class FreeShops(Toggle):
    """
    Toggled on, this gives you 9999 Coins, 99 Frog Coins, and makes shop prices all be one Coin/Frog Coin.
    Toggled off, shops will charge normal prices and you'll start with no Coins or Frog Coins.
    """
    display_name = "Free Shops"

@dataclass
class SMRPGOptions(PerGameCommonOptions):
    StarPieceGoal: StarPieceGoal
    StarPiecesInBowsersKeep: StarPiecesInBowsersKeep
    BowsersKeepDoors: BowsersKeepDoors
    ShuffleBowsersKeepDoors: ShuffleBowsersKeepDoors
    IncludeCulex: IncludeCulex
    ExperienceMultiplier: ExperienceMultiplier
    RandomizeEnemies: RandomizeEnemies
    RandomizeBosses: RandomizeBosses
    RandomizeCharacterStats: RandomizeCharacterStats
    RandomizeCharacterSpells: RandomizeCharacterSpells
    StartingCharacterCount: StartingCharacterCount
    StartingCharacter: StartingCharacter
    RandomizeCharacterPalettes: RandomizeCharacterPalettes
    RandomizeEquipment: RandomizeEquipment
    ItemPool: ItemPool
    SuperJumpsInLogic: SuperJumpsInLogic
    FreeShops: FreeShops



def build_flag_string(options: typing.Dict[str, typing.Any]):
    key_flags = build_key_flags(options)
    character_flags = build_character_flags(options)
    treasure_flags = "Tca" # Special Archipelago flag
    shop_flags = build_shop_flags(options)
    battle_flags = build_battle_flags(options)
    enemy_flags = build_enemy_flags(options)
    equipment_flags = build_equipment_flags(options)
    challenge_flags = "P1 Nbmq"
    tweaks_flags = build_tweaks_flags(options)
    return f"{key_flags} {character_flags} {treasure_flags} {shop_flags}" \
           f" {battle_flags} {enemy_flags} {equipment_flags} {challenge_flags} {tweaks_flags}"


def build_key_flags(options: typing.Dict[str, typing.Any]):
    key_flags = "Ksb R"
    if options["StarPieceGoal"] == StarPieceGoal.option_seven:
        key_flags += "7"
    if options["StarPiecesInBowsersKeep"] == StarPiecesInBowsersKeep.option_true:
        key_flags += "k"
    if options["IncludeCulex"] == IncludeCulex.option_true:
        key_flags += "c"
    return key_flags


def build_character_flags(options: typing.Dict[str, typing.Any]):
    character_flags = "Cj"
    starting_character_lookup = {
        0: "Ym",
        1: "Yw",
        2: "Yg",
        3: "Yb",
        4: "Yt",
    }
    if options["RandomizeCharacterStats"] == RandomizeCharacterStats.option_true:
        character_flags += "s"
    if options["RandomizeCharacterSpells"] == RandomizeCharacterSpells.option_true:
        character_flags += "pl"
    if options["StartingCharacterCount"] == StartingCharacterCount.option_one:
        character_flags += " -nfc"
    if options["StartingCharacter"] in starting_character_lookup.keys():
        character_flags += f" {starting_character_lookup[options['StartingCharacter']]}"
    if options["RandomizeCharacterPalettes"] == RandomizeCharacterPalettes.option_true:
        character_flags += " -palette"
    return character_flags


def build_shop_flags(options: typing.Dict[str, typing.Any]):
    shop_flags = "Sc4"
    if options["FreeShops"] == FreeShops.option_true:
        shop_flags += " -freeshops"
    return shop_flags


def build_battle_flags(options: typing.Dict[str, typing.Any]):
    battle_flags = ""
    if options["ExperienceMultiplier"] == ExperienceMultiplier.option_double:
        battle_flags += "X2"
    if options["ExperienceMultiplier"] == ExperienceMultiplier.option_triple:
        battle_flags += "X3"
    return battle_flags


def build_enemy_flags(options: typing.Dict[str, typing.Any]):
    enemy_flags = ""
    if options["RandomizeEnemies"] == RandomizeEnemies.option_mild:
        enemy_flags += " Edf"
    if options["RandomizeEnemies"] == RandomizeEnemies.option_moderate:
        enemy_flags += " Edfsa"
    if options["RandomizeEnemies"] == RandomizeEnemies.option_severe:
        enemy_flags += " Edfsac"
    if options["RandomizeEnemies"] == RandomizeEnemies.option_extreme:
        enemy_flags += " Edfsac!"
    if options["RandomizeBosses"] == RandomizeBosses.option_true:
        enemy_flags += " B"
        if options["IncludeCulex"] == IncludeCulex.option_true:
            enemy_flags += "c"
    return enemy_flags


def build_equipment_flags(options: typing.Dict[str, typing.Any]):
    """
    Randomize equipment. Mild randomizes who can equip each piece of gear. Moderate randomizes stats and buffs. Severe
    removes safety checks for the status protection pins guarding against their status and a minimum number of instant
    KO protection items.
    """
    equipment_flags = ""
    if options["RandomizeEquipment"] == RandomizeEquipment.option_mild:
        equipment_flags += "Qa"
    if options["RandomizeEquipment"] == RandomizeEquipment.option_moderate:
        equipment_flags += "Qsba"
    if options["RandomizeEquipment"] == RandomizeEquipment.option_severe:
        equipment_flags += "Qsba!"
    return equipment_flags


def build_tweaks_flags(options: typing.Dict[str, typing.Any]):
    tweaks_flags= "W -showequips"
    door_count = options["BowsersKeepDoors"]
    tweaks_flags += f" D{door_count}"
    if options["ShuffleBowsersKeepDoors"] == ShuffleBowsersKeepDoors.option_true:
        tweaks_flags += "s"
    return tweaks_flags
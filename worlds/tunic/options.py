import logging
from dataclasses import dataclass
from typing import Dict, Any
from Options import (DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, TextChoice, PlandoConnections,
                     PerGameCommonOptions, OptionGroup)
from .er_data import portal_mapping


class SwordProgression(DefaultOnToggle):
    """
    Adds four sword upgrades to the item pool that will progressively grant stronger melee weapons, including two new swords with increased range and attack power.
    """
    internal_name = "sword_progression"
    display_name = "Sword Progression"


class StartWithSword(Toggle):
    """
    Start with a sword in the player's inventory. Does not count towards Sword Progression.
    """
    internal_name = "start_with_sword"
    display_name = "Start With Sword"


class KeysBehindBosses(Toggle):
    """
    Places the three hexagon keys behind their respective boss fight in your world.
    If playing Hexagon Quest, it will place three gold hexagons at the boss locations.
    """
    internal_name = "keys_behind_bosses"
    display_name = "Keys Behind Bosses"


class AbilityShuffling(Toggle):
    """
    Locks the usage of Prayer, Holy Cross*, and the Icebolt combo until the relevant pages of the manual have been found.
    If playing Hexagon Quest, abilities are instead randomly unlocked after obtaining 25%, 50%, and 75% of the required
    Hexagon goal amount, unless the option is set to have them unlock via pages instead.
    * Certain Holy Cross usages are still allowed, such as the free bomb codes, the seeking spell, and other player-facing codes.
    """
    internal_name = "ability_shuffling"
    display_name = "Shuffle Abilities"


class LogicRules(Choice):
    """
    Set which logic rules to use for your world.
    Restricted: Standard logic, no glitches.
    No Major Glitches: Sneaky Laurels zips, ice grapples through doors, shooting the west bell, and boss quick kills are included in logic.
    * Ice grappling through the Ziggurat door is not in logic since you will get stuck in there without Prayer.
    Unrestricted: Logic in No Major Glitches, as well as ladder storage to get to certain places early.
    * Torch is given to the player at the start of the game due to the high softlock potential with various tricks. Using the torch is not required in logic.
    * Using Ladder Storage to get to individual chests is not in logic to avoid tedium.
    * Getting knocked out of the air by enemies during Ladder Storage to reach places is not in logic, except for in Rooted Ziggurat Lower. This is so you're not punished for playing with enemy rando on.
    """
    internal_name = "logic_rules"
    display_name = "Logic Rules"
    option_restricted = 0
    option_no_major_glitches = 1
    alias_nmg = 1
    option_unrestricted = 2
    alias_ur = 2
    default = 0


class Lanternless(Toggle):
    """
    Choose whether you require the Lantern for dark areas.
    When enabled, the Lantern is marked as Useful instead of Progression.
    """
    internal_name = "lanternless"
    display_name = "Lanternless"


class Maskless(Toggle):
    """
    Choose whether you require the Scavenger's Mask for Lower Quarry.
    When enabled, the Scavenger's Mask is marked as Useful instead of Progression.
    """
    internal_name = "maskless"
    display_name = "Maskless"


class FoolTraps(Choice):
    """
    Replaces low-to-medium value money rewards in the item pool with fool traps, which cause random negative effects to the player.
    """
    internal_name = "fool_traps"
    display_name = "Fool Traps"
    option_off = 0
    option_normal = 1
    option_double = 2
    option_onslaught = 3
    default = 1


class HexagonQuest(Toggle):
    """
    An alternate goal that shuffles Gold "Questagon" items into the item pool and allows the game to be completed after collecting the required number of them.
    """
    internal_name = "hexagon_quest"
    display_name = "Hexagon Quest"


class HexagonGoal(Range):
    """
    How many Gold Questagons are required to complete the game on Hexagon Quest.
    """
    internal_name = "hexagon_goal"
    display_name = "Gold Hexagons Required"
    range_start = 1
    range_end = 100
    default = 20


class ExtraHexagonPercentage(Range):
    """
    How many extra Gold Questagons are shuffled into the item pool, taken as a percentage of the goal amount.
    The max number of Gold Questagons that can be in the item pool is 100, so this option may be overridden and/or
    reduced if the Hexagon Goal amount is greater than 50.
    """
    internal_name = "extra_hexagon_percentage"
    display_name = "Percentage of Extra Gold Hexagons"
    range_start = 0
    range_end = 100
    default = 50


class HexagonQuestAbilityUnlockType(Choice):
    """
    Determines how abilities are unlocked when playing Hexagon Quest with Shuffled Abilities enabled.

    Hexagons: A new ability is randomly unlocked after obtaining 25%, 50%, and 75% of the required Hexagon goal amount.
    Pages: Abilities are unlocked by finding specific pages in the manual.

    This option will default to Pages if the Hexagon Goal is fewer than 3, or fewer than 15 if Keys Behind Bosses is enabled.
    This option does nothing if Shuffled Abilities is not enabled.
    """
    internal_name = "hexagon_quest_ability_type"
    display_name = "Hexagon Quest Ability Unlocks"
    option_hexagons = 0
    option_pages = 1
    default = 0


class EntranceRando(TextChoice):
    """
    Randomize the connections between scenes.
    A small, very lost fox on a big adventure.

    If you set this option's value to a string, it will be used as a custom seed.
    Every player who uses the same custom seed will have the same entrances, choosing the most restrictive settings among these players for the purpose of pairing entrances.
    """
    internal_name = "entrance_rando"
    display_name = "Entrance Rando"
    alias_false = 0
    alias_off = 0
    option_no = 0
    alias_true = 1
    alias_on = 1
    option_yes = 1
    default = 0


class FixedShop(Toggle):
    """
    Forces the Windmill entrance to lead to a shop, and removes the remaining shops from the pool.
    Adds another entrance in Rooted Ziggurat Lower to keep an even number of entrances.
    Has no effect if Entrance Rando is not enabled.
    """
    internal_name = "fixed_shop"
    display_name = "Fewer Shops in Entrance Rando"


class LaurelsLocation(Choice):
    """
    Force the Hero's Laurels to be placed at a location in your world.
    For if you want to avoid or specify early or late Laurels.
    """
    internal_name = "laurels_location"
    display_name = "Laurels Location"
    option_anywhere = 0
    option_6_coins = 1
    option_10_coins = 2
    option_10_fairies = 3
    default = 0


class ShuffleLadders(Toggle):
    """
    Turns several ladders in the game into items that must be found before they can be climbed on.
    Adds more layers of progression to the game by blocking access to many areas early on.
    "Ladders were a mistake."
    —Andrew Shouldice
    """
    internal_name = "shuffle_ladders"
    display_name = "Shuffle Ladders"
    
    
class TunicPlandoConnections(PlandoConnections):
    """
    Generic connection plando. Format is:
    - entrance: "Entrance Name"
      exit: "Exit Name"
      percentage: 100
    Percentage is an integer from 0 to 100 which determines whether that connection will be made. Defaults to 100 if omitted.
    """
    entrances = {*(portal.name for portal in portal_mapping), "Shop", "Shop Portal"}
    exits = {*(portal.name for portal in portal_mapping), "Shop", "Shop Portal"}

    duplicate_exits = True


@dataclass
class TunicOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    sword_progression: SwordProgression
    start_with_sword: StartWithSword
    keys_behind_bosses: KeysBehindBosses
    ability_shuffling: AbilityShuffling
    shuffle_ladders: ShuffleLadders
    entrance_rando: EntranceRando
    fixed_shop: FixedShop
    logic_rules: LogicRules
    fool_traps: FoolTraps
    hexagon_quest: HexagonQuest
    hexagon_goal: HexagonGoal
    extra_hexagon_percentage: ExtraHexagonPercentage
    hexagon_quest_ability_type: HexagonQuestAbilityUnlockType
    lanternless: Lanternless
    maskless: Maskless
    laurels_location: LaurelsLocation
    plando_connections: TunicPlandoConnections
      

tunic_option_groups = [
    OptionGroup("Hexagon Quest Options", [
        HexagonQuest,
        HexagonGoal,
        ExtraHexagonPercentage,
        HexagonQuestAbilityUnlockType
    ]),
    OptionGroup("Logic Options", [
        LogicRules,
        Lanternless,
        Maskless,
    ]),
]

tunic_option_presets: Dict[str, Dict[str, Any]] = {
    "Sync": {
        "ability_shuffling": True,
    },
    "Async": {
        "progression_balancing": 0,
        "ability_shuffling": True,
        "shuffle_ladders": True,
        "laurels_location": "10_fairies",
    },
    "Glace Mode": {
        "accessibility": "minimal",
        "ability_shuffling": True,
        "entrance_rando": "yes",
        "fool_traps": "onslaught",
        "logic_rules": "unrestricted",
        "maskless": True,
        "lanternless": True,
    },
}


def check_options(world: "TunicWorld"):
    options = world.options
    if options.hexagon_quest:
        hexagon_goal = options.hexagon_goal.value
        if options.ability_shuffling and options.hexagon_quest_ability_type == "hexagons":
            if hexagon_goal < 3:
                logging.warning("TUNIC: Hexagon Quest goal is too low for Shuffled Abilities (Hexagons). Option will be switched to Pages.")
                world.options.hexagon_quest_ability_type = "pages"
            if hexagon_goal < 15 and options.keys_behind_bosses:
                logging.warning("TUNIC: Hexagon Quest goal is too low for Shuffled Abilities (Hexagons) + Keys Behind Bosses. Keys Behind Bosses will be ignored during generation.")
                world.options.keys_behind_bosses.value = 0


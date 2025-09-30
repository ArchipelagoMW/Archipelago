from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import logging
from typing import Any, TYPE_CHECKING

from Options import (DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, TextChoice, PlandoConnections,
                     PerGameCommonOptions, OptionGroup, Removed, Visibility, NamedRange)

from .er_data import portal_mapping

if TYPE_CHECKING:
    from . import TunicWorld


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


class AbilityShuffling(DefaultOnToggle):
    """
    Locks the usage of Prayer, Holy Cross*, and the Icebolt combo until the relevant pages of the manual have been found.
    If playing Hexagon Quest, abilities are instead randomly unlocked after obtaining 25%, 50%, and 75% of the required
    Hexagon goal amount, unless the option is set to have them unlock via pages instead.
    * Certain Holy Cross usages are still allowed, such as the free bomb codes, the seeking spell, and other player-facing codes.
    """
    internal_name = "ability_shuffling"
    display_name = "Shuffle Abilities"


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

    Hexagons: A new ability is randomly unlocked after obtaining 25%, 50%, and 75% of the required Hexagon goal amount. Requires at least 3 Gold Hexagons in the item pool, or 15 if Keys Behind Bosses is enabled.
    Pages: Abilities are unlocked by finding specific pages in the manual.

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


class EntranceLayout(Choice):
    """
    Decide how the Entrance Randomizer chooses how to pair the entrances.
    Standard: Entrances are randomly connected. There are 6 shops in the pool with this option.
    Fixed Shop: Forces the Windmill entrance to lead to a shop, and removes the other shops from the pool.
    Adds another entrance in Rooted Ziggurat Lower to keep an even number of entrances.
    Direction Pairs: Entrances facing opposite directions are paired together. There are 8 shops in the pool with this option.
    Note: For seed groups, if one player in a group chooses Fixed Shop and another chooses Direction Pairs, it will error out.
    Either of these options will override Standard within a seed group.
    """
    internal_name = "entrance_layout"
    display_name = "Entrance Layout"
    option_standard = 0
    option_fixed_shop = 1
    option_direction_pairs = 2
    default = 0


class Decoupled(Toggle):
    """
    Decouple the entrances, so that when you go from one entrance to another, the return trip won't necessarily bring you back to the same place.
    Note: For seed groups, all players in the group must have this option enabled or disabled.
    """
    internal_name = "decoupled"
    display_name = "Decoupled Entrances"


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


class ShuffleFuses(Toggle):
    """
    Praying at a fuse will reward a check instead of turning on the power. The power from each fuse gets turned into an
    item that must be found in order to restore power for that part of the path.
    """
    internal_name = "shuffle_fuses"
    display_name = "Shuffle Fuses"


class ShuffleBells(Toggle):
    """
    The East and West bells are shuffled into the item pool and must be found in order to unlock the Sealed Temple.
    Ringing the bells will instead now reward a check.
    """
    internal_name = "shuffle_bells"
    display_name = "Shuffle Bells"


class GrassRandomizer(Toggle):
    """
    Turns over 6,000 blades of grass and bushes in the game into checks.
    """
    internal_name = "grass_randomizer"
    display_name = "Grass Randomizer"


class LocalFill(NamedRange):
    """
    Choose the percentage of your filler/trap items that will be kept local or distributed to other TUNIC players with this option enabled.
    If you have Grass Randomizer enabled, this defaults to 95%. If you have Breakable Shuffle enabled, this defaults to 40%. If you have both enabled, this defaults to 96%.
    If you have Grass Randomizer enabled, this option must be set to 95% or higher to avoid flooding the item pool.
    The host can remove this restriction by turning off the limit_grass_rando setting in host.yaml. This setting can only be changed with local generation, it cannot be changed on the website.
    This option ignores items placed in your local_items or non_local_items.
    This option does nothing in single player games.
    """
    internal_name = "local_fill"
    display_name = "Local Fill Percent"
    range_start = 0
    range_end = 98
    special_range_names = {
        "default": -1
    }
    default = -1


class TunicPlandoConnections(PlandoConnections):
    """
    Generic connection plando. Format is:
    - entrance: Entrance Name
      exit: Exit Name
      direction: Direction
      percentage: 100
    Direction must be one of entrance, exit, or both, and defaults to both if omitted.
    Direction entrance means the entrance leads to the exit. Direction exit means the exit leads to the entrance.
    If you do not have Decoupled enabled, you do not need the direction line, as it will only use both.
    Percentage is an integer from 0 to 100 which determines whether that connection will be made. Defaults to 100 if omitted.
    If the Entrance Layout option is set to Standard or Fixed Shop, you can plando multiple shops.
    If the Entrance Layout option is set to Direction Pairs, your plando connections must be facing opposite directions.
    Shop Portal 1-6 are South portals, and Shop Portal 7-8 are West portals.
    This option does nothing if Entrance Rando is disabled.
    """
    shops = {f"Shop Portal {i + 1}" for i in range(500)}
    entrances = {portal.name for portal in portal_mapping}.union(shops)
    exits = {portal.name for portal in portal_mapping}.union(shops)

    duplicate_exits = True


class CombatLogic(Choice):
    """
    If enabled, the player will logically require a combination of stat upgrade items and equipment to get some checks or navigate to some areas, with a goal of matching the vanilla combat difficulty.
    The player may still be expected to run past enemies, reset aggro (by using a checkpoint or doing a scene transition), or find sneaky paths to checks.
    This option marks many more items as progression and may force weapons much earlier than normal.
    Bosses Only makes it so that additional combat logic is only added to the boss fights and the Gauntlet.
    If disabled, the standard, looser logic is used. The standard logic does not include stat upgrades, just minimal weapon requirements, such as requiring a Sword or Magic Wand for Quarry, or not requiring a weapon for Swamp.
    """
    internal_name = "combat_logic"
    display_name = "More Combat Logic"
    option_off = 0
    option_bosses_only = 1
    option_on = 2
    default = 0


class LaurelsZips(Toggle):
    """
    Choose whether to include using the Hero's Laurels to zip through gates, doors, and tricky spots.
    Notable inclusions are the Monastery gate, Ruined Passage door, Old House gate, Forest Grave Path gate, and getting from the Back of Swamp to the Middle of Swamp.
    """
    internal_name = "laurels_zips"
    display_name = "Laurels Zips Logic"


class IceGrappling(Choice):
    """
    Choose whether grappling frozen enemies is in logic.
    Easy includes ice grappling enemies that are in range without luring them. May include clips through terrain.
    Medium includes using ice grapples to push enemies through doors or off ledges without luring them. Also includes bringing an enemy over to the Temple Door to grapple through it.
    Hard includes luring or grappling enemies to get to where you want to go.
    Enabling any of these difficulty options will give the player the Torch to return to the Overworld checkpoint to avoid softlocks. Using the Torch is considered in logic.
    Note: You will still be expected to ice grapple to the slime in East Forest from below with this option off.
    """
    internal_name = "ice_grappling"
    display_name = "Ice Grapple Logic"
    option_off = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    default = 0


class LadderStorage(Choice):
    """
    Choose whether Ladder Storage is in logic.
    Easy includes uses of Ladder Storage to get to open doors over a long distance without too much difficulty. May include convenient elevation changes (going up Mountain stairs, stairs in front of Special Shop, etc.).
    Medium includes the above as well as changing your elevation using the environment and getting knocked down by melee enemies mid-LS.
    Hard includes the above as well as going behind the map to enter closed doors from behind, shooting a fuse with the magic wand to knock yourself down at close range, and getting into the Cathedral Secret Legend room mid-LS.
    Enabling any of these difficulty options will give the player the Torch to return to the Overworld checkpoint to avoid softlocks. Using the Torch is considered in logic.
    Opening individual chests while doing ladder storage is excluded due to tedium.
    Knocking yourself out of LS with a bomb is excluded due to the problematic nature of consumables in logic.
    """
    internal_name = "ladder_storage"
    display_name = "Ladder Storage Logic"
    option_off = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    default = 0


class LadderStorageWithoutItems(Toggle):
    """
    If disabled, you logically require Stick, Sword, Magic Orb, or Shield to perform Ladder Storage.
    If enabled, you will be expected to perform Ladder Storage without progression items.
    This can be done with the plushie code, a Golden Coin, Prayer, and many other options.

    This option has no effect if you do not have Ladder Storage Logic enabled.
    """
    internal_name = "ladder_storage_without_items"
    display_name = "Ladder Storage without Items"


class BreakableShuffle(Toggle):
    """
    Turns approximately 250 breakable objects in the game into checks.
    """
    internal_name = "breakable_shuffle"
    display_name = "Breakable Shuffle"


class HiddenAllRandom(Toggle):
    """
    Sets all options that can be random to random.
    For test gens.
    """
    internal_name = "all_random"
    display_name = "All Random Debug"
    visibility = Visibility.none


@dataclass
class TunicOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    sword_progression: SwordProgression
    start_with_sword: StartWithSword
    keys_behind_bosses: KeysBehindBosses
    ability_shuffling: AbilityShuffling

    fool_traps: FoolTraps
    laurels_location: LaurelsLocation

    hexagon_quest: HexagonQuest
    hexagon_goal: HexagonGoal
    extra_hexagon_percentage: ExtraHexagonPercentage
    hexagon_quest_ability_type: HexagonQuestAbilityUnlockType

    shuffle_ladders: ShuffleLadders
    shuffle_fuses: ShuffleFuses
    shuffle_bells: ShuffleBells
    grass_randomizer: GrassRandomizer
    breakable_shuffle: BreakableShuffle
    local_fill: LocalFill

    entrance_rando: EntranceRando
    entrance_layout: EntranceLayout
    decoupled: Decoupled

    combat_logic: CombatLogic
    lanternless: Lanternless
    maskless: Maskless
    laurels_zips: LaurelsZips
    ice_grappling: IceGrappling
    ladder_storage: LadderStorage
    ladder_storage_without_items: LadderStorageWithoutItems

    plando_connections: TunicPlandoConnections

    all_random: HiddenAllRandom

    fixed_shop: Removed
    logic_rules: Removed


tunic_option_groups = [
    OptionGroup("Hexagon Quest Options", [
        HexagonQuest,
        HexagonGoal,
        ExtraHexagonPercentage,
        HexagonQuestAbilityUnlockType
    ]),
    OptionGroup("Logic Options", [
        CombatLogic,
        Lanternless,
        Maskless,
        LaurelsZips,
        IceGrappling,
        LadderStorage,
        LadderStorageWithoutItems,
    ]),
    OptionGroup("Entrance Randomizer", [
        EntranceRando,
        EntranceLayout,
        Decoupled,
        TunicPlandoConnections,
    ]),
]

tunic_option_presets: dict[str, dict[str, Any]] = {
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
        "entrance_rando": True,
        "fool_traps": "onslaught",
        "laurels_zips": True,
        "ice_grappling": "hard",
        "ladder_storage": "hard",
        "ladder_storage_without_items": True,
        "maskless": True,
        "lanternless": True,
    },
}


def check_options(world: "TunicWorld"):
    options = world.options
    if (options.hexagon_quest and options.ability_shuffling
            and options.hexagon_quest_ability_type == HexagonQuestAbilityUnlockType.option_hexagons):
        total_hexes = get_hexagons_in_pool(world)
        min_hexes = 3

        if options.keys_behind_bosses:
            min_hexes = 15
        if total_hexes < min_hexes:
            logging.warning(f"TUNIC: Not enough Gold Hexagons in {world.player_name}'s item pool for Hexagon Ability "
                            "Shuffle with the selected options. Ability Shuffle mode will be switched to Pages.")
            options.hexagon_quest_ability_type.value = HexagonQuestAbilityUnlockType.option_pages


def get_hexagons_in_pool(world: "TunicWorld"):
    # Calculate number of hexagons in item pool
    options = world.options
    return min(int((Decimal(100 + options.extra_hexagon_percentage) / 100 * options.hexagon_goal)
                   .to_integral_value(rounding=ROUND_HALF_UP)), 100)

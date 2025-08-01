import random
from dataclasses import dataclass
from typing import List

from Options import DeathLinkMixin, Choice, Toggle, OptionDict, Range, PlandoBosses, DefaultOnToggle, \
    PerGameCommonOptions, Visibility, NamedRange, OptionGroup, PlandoConnections
from .names import location_name


class RemoteItems(DefaultOnToggle):
    """
    Enables receiving items from your own world, primarily for co-op play.
    """
    display_name = "Remote Items"


class KDL3PlandoConnections(PlandoConnections):
    entrances = exits = {f"{i} {j}" for i in location_name.level_names for j in range(1, 7)}


class Goal(Choice):
    """
    Zero: collect the Heart Stars, and defeat Zero in the Hyper Zone.
    Boss Butch: collect the Heart Stars, and then complete the boss rematches in the Boss Butch mode.
    MG5: collect the Heart Stars, and then complete a perfect run through the minigame gauntlet within the Super MG5
    Jumping: collect the Heart Stars, and then reach a designated score within the Jumping sub-game
    """
    display_name = "Goal"
    option_zero = 0
    option_boss_butch = 1
    option_MG5 = 2
    option_jumping = 3
    default = 0

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == 2:
            return cls.name_lookup[value].upper()
        return super().get_option_name(value)


class GoalSpeed(Choice):
    """
    Normal: the goal is unlocked after purifying the five bosses
    Fast: the goal is unlocked after acquiring the target number of Heart Stars
    """
    display_name = "Goal Speed"
    option_normal = 0
    option_fast = 1


class MaxHeartStars(Range):
    """
    Maximum number of heart stars to include in the pool of items.
    If fewer available locations exist in the pool than this number, the number of available locations will be used instead.
    """
    display_name = "Max Heart Stars"
    range_start = 5  # set to 5 so strict bosses does not degrade
    range_end = 99  # previously set to 50, set to highest it can be should there be less locations than heart stars
    default = 30


class HeartStarsRequired(Range):
    """
    Percentage of heart stars required to purify the five bosses and reach Zero.
    Each boss will require a differing amount of heart stars to purify.
    """
    display_name = "Required Heart Stars"
    range_start = 1
    range_end = 100
    default = 50


class LevelShuffle(Choice):
    """
    None: No stage shuffling.
    Same World: shuffles stages around their world.
    Pattern: shuffles stages according to the stage pattern (stage 3 will always be a minigame stage, etc.)
    Shuffled: shuffles stages across all worlds.
    """
    display_name = "Stage Shuffle"
    option_none = 0
    option_same_world = 1
    option_pattern = 2
    option_shuffled = 3
    default = 0


class BossShuffle(PlandoBosses):
    """
    None: Bosses will remain in their vanilla locations
    Shuffled: Bosses will be shuffled amongst each other
    Full: Bosses will be randomized
    Singularity: All (non-Zero) bosses will be replaced with a single boss
    Supports plando placement.
    """
    bosses = frozenset(location_name.boss_names.keys())

    locations = frozenset(location_name.level_names.keys())

    duplicate_bosses = True

    @classmethod
    def can_place_boss(cls, boss: str, location: str) -> bool:
        # Kirby has no logic about requiring bosses in specific locations (since we load in their stage)
        return True

    display_name = "Boss Shuffle"
    option_none = 0
    option_shuffled = 1
    option_full = 2
    option_singularity = 3


class BossShuffleAllowBB(Choice):
    """
    Allow Boss Butch variants of bosses in Boss Shuffle.
    Enabled: any boss placed will have a 50% chance of being the Boss Butch variant, including bosses not present
    Enforced: all bosses will be their Boss Butch variant.
    Boss Butch boss changes are only visual.
    """
    display_name = "Allow Boss Butch Bosses"
    option_disabled = 0
    option_enabled = 1
    option_enforced = 2
    default = 0


class AnimalRandomization(Choice):
    """
    Disabled: all animal positions will be vanilla.
    Shuffled: all animal positions will be shuffled amongst each other.
    Full: random animals will be placed across the levels. At least one of each animal is guaranteed.
    """
    display_name = "Animal Randomization"
    option_disabled = 0
    option_shuffled = 1
    option_full = 2
    default = 0


class CopyAbilityRandomization(Choice):
    """
    Disabled: enemies give regular copy abilities and health.
    Enabled: all enemies will have the copy ability received from them randomized.
    Enabled Plus Minus: enemies (except minibosses) can additionally give you anywhere from +2 health to -1 health when eaten.
    """
    display_name = "Copy Ability Randomization"
    option_disabled = 0
    option_enabled = 1
    option_enabled_plus_minus = 2


class StrictBosses(DefaultOnToggle):
    """
    If enabled, one will not be able to move onto the next world until the previous world's boss has been purified.
    """
    display_name = "Strict Bosses"


class OpenWorld(DefaultOnToggle):
    """
    If enabled, all 6 stages will be unlocked upon entering a world for the first time. A certain amount of stages
    will need to be completed in order to unlock the bosses
    """
    display_name = "Open World"


class OpenWorldBossRequirement(Range):
    """
    The amount of stages completed needed to unlock the boss of a world when Open World is turned on.
    """
    display_name = "Open World Boss Requirement"
    range_start = 1
    range_end = 6
    default = 3


class BossRequirementRandom(Toggle):
    """
    If enabled, boss purification will require a random amount of Heart Stars. Depending on options, this may have
    boss purification unlock in a random order.
    """
    display_name = "Randomize Purification Requirement"


class JumpingTarget(Range):
    """
    The required score needed to complete the Jumping minigame.
    """
    display_name = "Jumping Target Score"
    range_start = 1
    range_end = 25
    default = 10


class GameLanguage(Choice):
    """
    The language that the game should display. This does not have to match the given rom.
    """
    display_name = "Game Language"
    option_japanese = 0
    option_english = 1
    default = 1


class FillerPercentage(Range):
    """
    Percentage of non-required Heart Stars to be converted to filler items (1-Ups, Maxim Tomatoes, Invincibility Candy).
    """
    display_name = "Filler Percentage"
    range_start = 0
    range_end = 100
    default = 50


class TrapPercentage(Range):
    """
    Percentage of filler items to be converted to trap items (Gooey Bags, Slowness, Eject Ability).
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 50


class GooeyTrapPercentage(Range):
    """
    Chance that any given trap is a Gooey Bag (spawns Gooey when you receive it).
    """
    display_name = "Gooey Trap Percentage"
    range_start = 0
    range_end = 100
    default = 50


class SlowTrapPercentage(Range):
    """
    Chance that any given trap is Slowness (halves your max speed for 15 seconds when you receive it).
    """
    display_name = "Slowness Trap Percentage"
    range_start = 0
    range_end = 100
    default = 50


class AbilityTrapPercentage(Range):
    """
    Chance that any given trap is an Eject Ability (ejects your ability when you receive it).
    """
    display_name = "Ability Trap Percentage"
    range_start = 0
    range_end = 100
    default = 50


class ConsumableChecks(Toggle):
    """
    When enabled, adds all 1-Ups and Maxim Tomatoes as possible locations.
    """
    display_name = "Consumable-sanity"


class StarChecks(Toggle):
    """
    When enabled, every star in a given stage will become a check.
    Will increase the possible filler pool to include 1/3/5 stars.
    """
    display_name = "Starsanity"


class KirbyFlavorPreset(Choice):
    """
    The color of Kirby, from a list of presets.
    """
    display_name = "Kirby Flavor"
    option_default = 0
    option_bubblegum = 1
    option_cherry = 2
    option_blueberry = 3
    option_lemon = 4
    option_kiwi = 5
    option_grape = 6
    option_chocolate = 7
    option_marshmallow = 8
    option_licorice = 9
    option_watermelon = 10
    option_orange = 11
    option_lime = 12
    option_lavender = 13
    option_miku = 14
    option_custom = -1
    default = 0

    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            choice_list = list(cls.name_lookup)
            choice_list.remove(-1)
            return cls(random.choice(choice_list))
        return super().from_text(text)


class KirbyFlavor(OptionDict):
    """
    A custom color for Kirby. To use a custom color, set the preset to Custom and then define a dict of keys from "1" to
    "15", with their values being an HTML hex color.
    """
    display_name = "Custom Kirby Flavor"
    default = {
      "1": "B01810",
      "2": "F0E0E8",
      "3": "C8A0A8",
      "4": "A87070",
      "5": "E02018",
      "6": "F0A0B8",
      "7": "D07880",
      "8": "A85048",
      "9": "E8D0D0",
      "10": "E85048",
      "11": "D0C0C0",
      "12": "B08888",
      "13": "E87880",
      "14": "F8F8F8",
      "15": "B03830",
    }
    visibility = Visibility.template | Visibility.spoiler  # likely never supported on guis


class GooeyFlavorPreset(Choice):
    """
    The color of Gooey, from a list of presets.
    """
    display_name = "Gooey Flavor"
    option_default = 0
    option_bubblegum = 1
    option_cherry = 2
    option_blueberry = 3
    option_lemon = 4
    option_kiwi = 5
    option_grape = 6
    option_chocolate = 7
    option_marshmallow = 8
    option_licorice = 9
    option_watermelon = 10
    option_orange = 11
    option_lime = 12
    option_lavender = 13
    option_custom = -1
    default = 0

    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            choice_list = list(cls.name_lookup)
            choice_list.remove(-1)
            return cls(random.choice(choice_list))
        return super().from_text(text)


class GooeyFlavor(OptionDict):
    """
    A custom color for Gooey. To use a custom color, set the preset to Custom and then define a dict of keys from "1" to
    "15", with their values being an HTML hex color.
    """
    display_name = "Custom Gooey Flavor"
    default = {
        "1": "000808",
        "2": "102838",
        "3": "183048",
        "4": "183878",
        "5": "1838A0",
        "6": "B01810",
        "7": "E85048",
        "8": "D0C0C0",
        "9": "F8F8F8",
    }
    visibility = Visibility.template | Visibility.spoiler  # likely never supported on guis


class MusicShuffle(Choice):
    """
    None: default music will play
    Shuffled: music will be shuffled amongst each other
    Full: random music will play in each room
    Note that certain songs will not be chosen in shuffled or full
    """
    display_name = "Music Randomization"
    option_none = 0
    option_shuffled = 1
    option_full = 2
    default = 0


class VirtualConsoleChanges(Choice):
    """
    Adds the ability to enable 2 of the Virtual Console changes.
    Flash Reduction: reduces the flashing during the Zero battle.
    Color Changes: changes the color of the background within the Zero Boss Butch rematch.
    """
    display_name = "Virtual Console Changes"
    option_none = 0
    option_flash_reduction = 1
    option_color_changes = 2
    option_both = 3
    default = 1


class Gifting(Toggle):
    """
    When enabled, the goal game item will be sent to other compatible games as a gift,
    and you can receive gifts from other players. This can be enabled during gameplay
    using the client.
    """
    display_name = "Gifting"


class TotalHeartStars(NamedRange):
    """
    Deprecated. Use max_heart_stars instead. Supported for only one version.
    """
    default = -1
    range_start = 5
    range_end = 99
    special_range_names = {
        "default": -1
    }
    visibility = Visibility.none


@dataclass
class KDL3Options(PerGameCommonOptions, DeathLinkMixin):
    remote_items: RemoteItems
    plando_connections: KDL3PlandoConnections
    game_language: GameLanguage
    goal: Goal
    goal_speed: GoalSpeed
    max_heart_stars: MaxHeartStars
    heart_stars_required: HeartStarsRequired
    filler_percentage: FillerPercentage
    trap_percentage: TrapPercentage
    gooey_trap_weight: GooeyTrapPercentage
    slow_trap_weight: SlowTrapPercentage
    ability_trap_weight: AbilityTrapPercentage
    jumping_target: JumpingTarget
    stage_shuffle: LevelShuffle
    boss_shuffle: BossShuffle
    allow_bb: BossShuffleAllowBB
    animal_randomization: AnimalRandomization
    copy_ability_randomization: CopyAbilityRandomization
    strict_bosses: StrictBosses
    open_world: OpenWorld
    ow_boss_requirement: OpenWorldBossRequirement
    boss_requirement_random: BossRequirementRandom
    consumables: ConsumableChecks
    starsanity: StarChecks
    gifting: Gifting
    kirby_flavor_preset: KirbyFlavorPreset
    kirby_flavor: KirbyFlavor
    gooey_flavor_preset: GooeyFlavorPreset
    gooey_flavor: GooeyFlavor
    music_shuffle: MusicShuffle
    virtual_console: VirtualConsoleChanges

    total_heart_stars: TotalHeartStars  # remove in 2 versions


kdl3_option_groups: List[OptionGroup] = [
    OptionGroup("Goal Options", [Goal, GoalSpeed, MaxHeartStars, HeartStarsRequired, JumpingTarget, ]),
    OptionGroup("World Options", [RemoteItems, StrictBosses, OpenWorld, OpenWorldBossRequirement, ConsumableChecks,
                                  StarChecks, FillerPercentage, TrapPercentage, GooeyTrapPercentage,
                                  SlowTrapPercentage, AbilityTrapPercentage, LevelShuffle, BossShuffle,
                                  AnimalRandomization, CopyAbilityRandomization,  BossRequirementRandom,
                                  Gifting, ]),
    OptionGroup("Cosmetic Options", [GameLanguage, BossShuffleAllowBB, KirbyFlavorPreset, KirbyFlavor,
                                     GooeyFlavorPreset, GooeyFlavor, MusicShuffle, VirtualConsoleChanges, ]),
]

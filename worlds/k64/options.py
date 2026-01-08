import random
from dataclasses import dataclass

from Options import DeathLinkMixin, Choice, Toggle, OptionDict, Range, PlandoBosses, DefaultOnToggle, \
    PerGameCommonOptions, Visibility, StartInventoryPool, PlandoConnections
from .names import LocationName
import typing


class K64PlandoConnections(PlandoConnections):
    display_name = "Plando Connections"
    entrances = [f"{level} {i}"
                 for idx, level in LocationName.level_names.items()
                 for i in range(LocationName.level_max[idx])]
    exits = entrances


class GoalSpeed(Choice):
    """
    Normal: the goal is unlocked after defeating the 6 bosses
    Fast: the goal is unlocked after acquiring the target number of Crystal Shards
    """
    display_name = "Goal Speed"
    option_normal = 0
    option_fast = 1


class SplitPowerCombos(Toggle):
    """
    If enabled, Power Combos are added to the pool as separate items, and must be unlocked separate from
    its base abilities.
    """
    display_name = "Split Power Combos"


class TotalCrystalShards(Range):
    """
    Maximum number of crystal shards to include in the pool of items.
    """
    display_name = "Max Crystal Shards"
    range_start = 5  # set to 5 so strict bosses does not degrade
    range_end = 72  # 72 default locations, let's not push our luck
    default = 30


class CrystalShardsRequired(Range):
    """
    Percentage of crystal shards required to unlock the boss of Ripple Star, and grant access to Zero-Two.
    """
    display_name = "Required Crystal Shards"
    range_start = 1
    range_end = 100
    default = 50


class LevelShuffle(Choice):
    """
    None: No stage shuffling.
    Same World: shuffles stages around their world.
    Shuffled: shuffles stages across all worlds.
    """
    display_name = "Stage Shuffle"
    option_none = 0
    option_same_world = 1
    option_shuffled = 2
    default = 0


class BossShuffle(PlandoBosses):
    """
    None: Bosses will remain in their vanilla locations
    Shuffled: Bosses will be shuffled amongst each other
    Full: Bosses will be randomized
    Singularity: All (non-Zero-Two) bosses will be replaced with a single boss
    Supports plando placement.
    """
    bosses = frozenset(LocationName.boss_names.keys())

    locations = frozenset(LocationName.level_names_inverse.keys())

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


class BossRequirementRandom(Toggle):
    """
    If enabled, unlocking a boss will require a random amount of Crystal Shards, up to a certain amount per level.
    """
    display_name = "Randomize Boss Unlock Requirement"


class FillerPercentage(Range):
    """
    Percentage of non-required Crystal Shards to be converted to filler items (1-Ups, Maxim Tomatoes, Invincibility Candy).
    """
    display_name = "Filler Percentage"
    range_start = 0
    range_end = 100
    default = 50


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
    option_kusamochi = 16
    option_citrus = 23
    option_wafer = 24
    option_ice = 25
    option_cream = 26
    option_snowcone = 31
    option_cotton_candy = 48
    option_chocomint = 49
    option_cheeseburger = 50
    option_rose = 27
    option_daisy = 28
    option_lavender = 29
    option_lilac = 13
    option_blue_poppy = 32
    option_fuschia = 47
    option_canary = 22
    option_carbon = 17
    option_snow = 18
    option_ivory = 21
    option_chalk = 44
    option_sapphire = 19
    option_emerald = 20
    option_gameboy = 45
    option_nostalgic = 15
    option_halloween = 43
    option_bright = 30
    option_ocean = 42
    option_miku = 14
    option_rin = 51
    option_len = 52
    option_luka = 53
    option_meiko = 54
    option_kaito = 55
    option_mirror = 46
    option_dedede = 33
    option_waddle_dee = 34
    option_susie = 35
    option_mogeko = 36
    option_link = 37
    option_callie = 38
    option_marie = 39
    option_pearl = 40
    option_marina = 41
    option_custom = -1
    default = 0

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value in (cls.option_meiko, cls.option_kaito):
            return cls.name_lookup[value].upper()
        return super().get_option_name(value)

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
    "17", with their values being an HTML hex color.
    """
    default = {
      "1": "#080000",
      "2": "#F64A5A",
      "3": "#6A4152",
      "4": "#F6F6F6",
      "5": "#F7A5B5",
      "6": "#E66A62",
      "7": "#00085A",
      "8": "#EE8BA4",
      "9": "#733141",
      "10": "#D5D5D5",
      "11": "#312029",
      "12": "#8B949C",
      "13": "#0000D5",
      "14": "#8B626A",
      "15": "#BD838B",
      "16": "#FF6946",
      "17": "#FF2600",
    }
    visibility = Visibility.complex_ui | Visibility.template


@dataclass
class K64Options(PerGameCommonOptions, DeathLinkMixin):
    start_inventory_from_pool: StartInventoryPool
    plando_connections: PlandoConnections
    goal_speed: GoalSpeed
    split_power_combos: SplitPowerCombos
    stage_shuffle: LevelShuffle
    # boss_shuffle: BossShuffle
    boss_requirement_random: BossRequirementRandom
    total_crystals: TotalCrystalShards
    required_crystals: CrystalShardsRequired
    filler_percentage: FillerPercentage
    kirby_flavor_preset: KirbyFlavorPreset
    kirby_flavor: KirbyFlavor

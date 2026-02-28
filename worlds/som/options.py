import typing as t
from abc import abstractmethod
from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Range, Toggle

__all__ = (
    "SoMOptions",
    "SoMROptionProto",
    "Goal",
    "Logic",
    "FlammieDrum",
    "MTRSeedsRequired",
)

BOOL_VALUES = ["no", "yes"]


# meta types


@t.runtime_checkable
class SoMROptionProto(t.Protocol):
    somr_setting: t.ClassVar[str]

    @property
    @abstractmethod
    def somr_value(self) -> str: ...


class SoMRToggle(Toggle):
    somr_setting: t.ClassVar[str]
    somr_values = BOOL_VALUES

    @property
    def somr_value(self) -> str:
        return self.somr_values[self.value]


class SoMRDefaultOnToggle(SoMRToggle):
    default = 1


class SoMRInverseToggle(SoMRDefaultOnToggle):
    somr_values = list(reversed(BOOL_VALUES))


class SoMRChoice(Choice):
    somr_setting: t.ClassVar[str]
    somr_values: t.ClassVar[t.Sequence[str]]

    @property
    def somr_value(self) -> str:
        return self.somr_values[self.value]


class SoMRRange(Range):
    somr_setting: t.ClassVar[str]

    @property
    def somr_value(self) -> str:
        return str(self.value)


class SoMRDecimalRange(Range):
    somr_setting: t.ClassVar[str]

    @property
    def somr_value(self) -> str:
        return "%.2f" % (self.value / 100)


# option types


class Goal(SoMRChoice):
    """
    Vanilla Short: Beat the Mana Beast, Mana Fort available right away.
    Vanilla Long: Beat the Mana Beast, activate the Mana Fort in Grand Palace.
    Mana Tree Revival: Reach the end of Pure Land with enough Mana Seeds.
    """

    display_name = "Goal"
    option_vanilla_short = 0
    option_vanilla_long = 1
    option_mana_tree_revival = 2
    alias_vshort = option_vanilla_short
    alias_vlong = option_vanilla_long
    alias_mtr = option_mana_tree_revival
    default = option_vanilla_long
    somr_setting = "opGoal"
    somr_values = ["vshort", "vlong", "mtr"]


class Logic(SoMRChoice):
    """Restrictive logic requires the corresponding Mana Seed to get the palace rewards."""

    display_name = "Logic"
    option_basic = 0
    option_restrictive = 1
    default = option_restrictive
    somr_setting = "opLogic"
    somr_values = ["basic", "restrictive"]


class FlammieDrum(SoMRChoice):
    """Decides whether Flammie Drum is in the item pool or you start with it."""

    display_name = "Flammie Drum"
    option_start = 0
    option_find = 1
    default = option_start
    somr_setting = "opFlammieDrumInLogic"
    somr_values = BOOL_VALUES


class MTRSeedsRequired(SoMRRange):
    """Number of seeds required to finish Mana Tree Revival goal. Does nothing for other goals."""

    display_name = "MTR Seeds Required"
    range_start = 1
    range_end = 8
    default = 8
    somr_setting = "opNumSeeds"


class Role(SoMRChoice):
    """Base class for the character role selection."""

    option_boy = 0
    option_girl = 1
    option_sprite = 2
    option_random_any = 3
    option_random_unique = 4
    somr_values = ["OGboy", "OGgirl", "OGsprite", "random", "randomunique"]

    @classmethod
    def from_text(cls, text: str) -> Choice:
        if text == "random":
            return cls(cls.option_random_any)
        return super().from_text(text)


class BoyRole(Role):
    """Which stats and magic the boy should have."""

    display_name = "Boy Role"
    default = Role.option_boy
    somr_setting = "opBoyRole"


class GirlRole(Role):
    """Which stats and magic the girl should have."""

    display_name = "Girl Role"
    default = Role.option_girl
    somr_setting = "opGirlRole"


class SpriteRole(Role):
    """Which stats and magic the sprite should have."""

    display_name = "Sprite Role"
    default = Role.option_sprite
    somr_setting = "opSpriteRole"


class StartChar(SoMRChoice):
    """Which character to start with."""

    display_name = "Start Character"
    option_boy = 0
    option_girl = 1
    option_sprite = 2
    default = option_boy
    somr_setting = "opStartChar"
    somr_values = ["boy", "girl", "sprite"]


class OtherChars(SoMRChoice):
    """How to get other characters."""

    display_name = "Other Characters"
    option_start_with_all = 0
    option_find_both_at_level_1 = 1
    option_find_both_at_current_level = 2
    option_start_extra_find_one = 3
    option_start_extra_find_none = 4
    option_find_one_at_level_1 = 5
    option_find_one_at_current_level = 6
    option_none = 7
    default = option_find_both_at_level_1
    somr_setting = "opCharacters"
    somr_values = [
        "startboth",
        "findbothL1",
        "findbothCL",
        "start1find1",
        "start1only",
        "find1L1",
        "find1CL",
        "none",
    ]


class StartWeapon(SoMRChoice):
    """Which weapon to start with."""

    display_name = "Start Weapon"
    option_glove = 0
    option_sword = 1
    option_axe = 2
    option_spear = 3
    option_whip = 4
    option_bow = 5
    option_boomerang = 6
    option_javelin = 7
    default = "random"  # type: ignore[assignment,unused-ignore] # broken in Options types
    # Alternatively, we could do something like this:
    # option_any = -1
    # default = option_any
    # not sure what looks nicer
    somr_setting = "opStartWeapon"
    somr_values = list(map(str, range(0, 8)))  # + ["-1"]


class StartGold(SoMRRange):
    """
    How much money to start with.
    Recommended 100 when not starting with Flammie Drum.
    """

    display_name = "Start Gold"
    range_start = 0
    range_end = 10000  # actual limit: 65535
    default = 100
    somr_setting = "opStartGold"


class ExpMultiplier(SoMRDecimalRange):
    """How much Exp to get, in %"""

    display_name = "Exp %"
    range_start = 0
    range_end = 1000  # actual limit: 100000
    default = 200
    somr_setting = "opExp"


class GoldEnemyMultiplier(SoMRDecimalRange):
    """How much GP to get from defeating enemies, in %"""

    display_name = "Enemy Gold %"
    range_start = 0
    range_end = 1000  # actual limit: 100000
    default = 200
    somr_setting = "opGold"


class GoldCheckMultiplier(SoMRRange):
    """How much GP to get from item pool, as multiplier."""

    display_name = "Item Pool Gold Multiplier"
    range_start = 0
    range_end = 10  # actual limit: 50
    default = 2
    somr_setting = "opGoldCheckMul"


class GoldDropMultiplier(SoMRRange):
    """How much GP to get from enemy chests, as multiplier."""

    display_name = "Chest Gold Multiplier"
    range_start = 0
    range_end = 10  # actual limit: 255
    default = 2
    somr_setting = "opGoldDropMul"


class ChestDropFrequency(SoMRChoice):
    """Decides how many chests will be dropped by enemies."""

    display_name = "Chest Drops Frequency"
    option_none = 0
    option_low = 1
    option_normal = 2
    option_high = 3
    option_highest = 4
    default = option_normal
    somr_setting = "opChestFreq"
    somr_values = ["none", "low", "normal", "high", "highest"]


class ChestTrapsFrequency(SoMRChoice):
    """Decides how many chests will have a trap."""

    display_name = "Chest Traps Frequency"
    option_none = 0
    option_normal = 1
    option_many = 2
    default = option_normal
    somr_setting = "opTraps"
    somr_values = ["none", "normal", "many"]


class Bosses(SoMRChoice):
    """Decide which bosses should be placed where."""

    display_name = "Bosses"
    option_vanilla = 0
    option_swap = 1
    option_any_random = 2
    default = option_any_random
    somr_setting = "opBosses"
    somr_values = ["vanilla", "swap", "random"]


class BossElementRando(SoMRToggle):
    """Gives boss random elements."""

    display_name = "Randomize Boss Elements"
    somr_setting = "bossElementRando"


class Enemies(SoMRChoice):
    """Decide which enemies should be placed where."""

    display_name = "Enemies"
    option_vanilla = 0
    option_swap = 1
    option_random_spawns = 2
    option_oops_all = 3
    option_none = 4
    default = option_swap
    somr_setting = "opEnemies"
    somr_values = ["vanilla", "swap", "random", "oops", "none"]


class StatusAilments(SoMRChoice):
    """
    Status ailments caused by enemies are determined by:
    - Location: an enemy will cause the same conditions as the enemy that was originally there.
    - Enemy type: every enemy retains its status conditions regardless of location.
    - Random easy: randomize status effects with about the same distribution as vanilla.
    - Random annoying: randomize with about double the status ailments as vanilla.
    - Random awful: every enemy causes status ailments.
    """

    display_name = "Status Ailments"
    option_location = 0
    option_enemy_type = 1
    option_random_easy = 2
    option_random_annoying = 3
    option_random_awful = 4
    default = option_location
    somr_setting = "opStatusAilments"
    somr_values = ["location", "type", "easy", "annoying", "awful"]


class EnemyStatGrowth(SoMRChoice):
    """
    Decides how enemies level up.
    Do not pick "Timed", "No Future" or "Vanilla" unless you know what you are doing.
    """

    display_name = "Enemy Stat Growth"
    option_with_player = 0
    option_after_every_boss = 1
    option_timed = 2
    option_no_future = 3  # TODO: hide?
    option_vanilla = 4  # TODO: hide?
    somr_setting = "opStatGrowth"
    somr_values = ["player", "bosses", "timed", "nofuture", "vanilla"]


class EnemyDifficulty(SoMRChoice):
    """
    Decides how fast enemies level up.
    Do not pick "Impossible" unless you know what you are doing.
    """

    display_name = "Enemy Difficulty"
    option_easy = 0
    option_sorta_easy = 1
    option_normal = 2
    option_kinda_hard = 3
    option_hard = 4
    option_impossible = 5
    default = option_normal
    somr_setting = "opDifficulty"
    somr_values = ["easy", "sortaeasy", "normal", "kindahard", "hard", "impossible"]


class RandomizeWeapons(SoMRDefaultOnToggle):
    """
    Randomize names and properties of weapons.
    Mana sword will be preserved.
    """

    display_name = "Randomize Weapons"
    somr_setting = "opWeapons"


class RandomizeShops(SoMRDefaultOnToggle):
    """
    Randomize gear available in shops.
    """

    display_name = "Randomize Shops"
    somr_setting = "opShop"


class RandomizeMusic(SoMRDefaultOnToggle):
    """
    Mix up songs a bit.
    """

    display_name = "Randomize Music"
    somr_setting = "opMusic"


class Hints(SoMRInverseToggle):
    """Not implemented yet."""

    display_name = "Hints"
    somr_setting = "opDisableHints"


@dataclass
class SoMOptions(PerGameCommonOptions):
    goal: Goal
    logic: Logic
    flammie_drum: FlammieDrum
    mtr_seeds_required: MTRSeedsRequired
    boy_role: BoyRole
    girl_role: GirlRole
    sprite_role: SpriteRole
    start_char: StartChar
    other_chars: OtherChars
    start_weapon: StartWeapon
    start_gold: StartGold
    exp_multiplier: ExpMultiplier
    gold_enemy_multiplier: GoldEnemyMultiplier
    gold_check_multiplier: GoldCheckMultiplier
    gold_drop_multiplier: GoldDropMultiplier
    chest_drops: ChestDropFrequency
    chest_traps: ChestTrapsFrequency
    bosses: Bosses
    boss_element_rando: BossElementRando
    enemies: Enemies
    status_ailments: StatusAilments
    enemy_stat_growth: EnemyStatGrowth
    enemy_difficulty: EnemyDifficulty
    randomize_weapons: RandomizeWeapons
    randomize_shops: RandomizeShops
    randomize_music: RandomizeMusic

from dataclasses import dataclass

from Options import Choice, Range, Toggle, PerGameCommonOptions


def round_up_to(x, mod):
    return ((x + mod - 1) // mod) * mod


class PlayerRando(Toggle):
    """
    If enabled, playable units will be randomzied
    """

    display_name = "Randomize Player Units"
    default = 1


class PlayerMonsters(Toggle):
    """
    Allow playable units to randomize into monsters when enabled
    """

    display_name = "Enable Playable Monsters"
    default = 1


class SuperDemonKing(Toggle):
    """
    Buffs the final boss to have higher stats and to take less damage from
    non-holy weapons.

    If enabled, it is strongly recommended to set `Required Usable Holy
    Weapons` to at least 2.
    """

    display_name = "Super Demon King"


class SmoothLevelCapProgression(Toggle):
    """
    Tie level cap progression roughly against story progression.

    This may cause problems if enabled when `Minimum Endgame Level Cap` is
    below 30.
    """

    display_name = "Smooth Level Caps"
    default = 1


class MinimumEndgameLevelCapRange(Range):
    """
    Attempt to place level uncaps such that your level cap will be at least
    this high by the time you reach the final boss. Note that this is your
    level *cap*, not your actual party level. Rounds to the next highest
    multiple of 5. Promoted level caps are treated as 20+n (so promoted level
    10 would be level 30).

    Beware of setting this too low, especially if Super Demon King is enabled.
    Setting this too high may lead to level cap checks being placed late into
    progression if `Smooth Level Caps` is unset.
    """

    display_name = "Minimum Endgame Level Cap"
    range_start = 10
    range_end = 40
    default = 40

    def __init__(self, value: int):
        super().__init__(round_up_to(value, 5))


class MinimumUsableHolyWeapons(Range):
    """
    The expected number of holy weapons necessary to defeat the final boss.

    If nonzero, attempt to place holy weapons *and* the weapon rank boosts
    necessary to use them such that `n` holy weapons are accessible before the
    final boss. See also `Exclude Latona from holy weapon pool`.
    """

    display_name = "Required Usable Holy Weapons"
    range_start = 0
    range_end = 9
    default = 0


class ExcludeLatona(Toggle):
    """
    If enabled, don't count Latona as a holy weapon for the sake of
    `Required Usable Holy Weapons`.
    """

    display_name = "Exclude Latona from holy weapon pool"
    default = 1


# Cam: Should we make this a sliding scale?
class Easier5x(Toggle):
    """
    Give Ephraim, Forde and Kyle extra base stats. This is recommended to make
    chapter 5x significantly less of a slog.
    """

    display_name = "Buff Ephraim's party for chapter 5x"
    default = 1


class UnbreakableRegalia(Toggle):
    """
    Make all holy weapons other than Latona unbreakable.
    """

    display_name = "Unbreakable Regalia"
    default = 0


class EnableTower(Toggle):
    """
    Make each floor of the Tower of Valni a check. This can help balance the
    amount of early/lategame checks a bit more.
    """

    display_name = "Enable Tower of Valni checks"
    default = 0


class EnableRuins(Toggle):
    """
    Make each floor of the Lagdou Ruins a check.
    """

    display_name = "Enable Lagdou Ruins checks"
    default = 0


class ShuffleSkirmishTables(Toggle):
    """
    Shuffle enemy spawn tables for the Tower, Ruins and skirmishes.
    """

    display_name = "Shuffle internal randomizer tables"
    default = 1


class LockpickUsability(Choice):
    """
    Allow units other than thieves to use lockpicks and the Rogue's Pick
    command.

    - Vanilla: Only Thieves, Assassins and Rogues can use lockpicks.
    - Global Lockpicks: All characters can use lockpicks.
    - Global Rogue pick: In addition to global lockpicks, all characters can use
      the Rogue class's "Pick" command.
    """

    display_name = "Lockpick usability"
    option_Vanilla = 0
    option_GlobalLockpicks = 1
    option_GlobalRoguePick = 2


class NormalizeGenders(Toggle):
    """
    Adjust female classes to have identical base stats and caps to their male
    counterparts, if one exists.

    In most cases, this is a buff to those classes. However, some low-turn
    strategies may rely on the fact that female mounted units have more Aid.
    """

    display_name = "Normalize gendered class stats"
    default = 0


class DeathLink(Choice):
    """
    When you die, everyone dies. Of course the reverse is true, too.
    """

    display_name = "DeathLink"
    option_off = 0
    alias_no = 0
    option_OnGameOver = 1
    alias_gameover = 1
    option_OnEveryDeath = 2
    alias_death = 2


class GrowthRando(Choice):
    """
    Randomizes growth rates.

    - Redistribute: Preserves growth total, possibly adjusted (positive or negative)
      between GrowthRandoMin and GrowthRandoMax.
    - Delta: Adjusts vanilla growths by amounts between GrowthRandoMin and GrowthRandoMax
    - Full Random: Growths are assigned randomly between GrowthRandoMin and GrowthRandoMax

    GrowthRandoMin and GrowthRandoMax control the min/max of the adjustment.
    """

    display_name = "Growth Randomizing"

    option_Vanilla = 0
    alias_no = 0
    alias_off = 0
    option_Redistribute = 1
    option_Delta = 2
    option_Full = 3


class GrowthRandoMin(Range):
    """
    See Growth Rando.
    """

    display_name = "Growth Rando Min"
    range_start = 0
    range_end = 255
    default = 10


class GrowthRandoMax(Range):
    """
    See Growth Rando.
    """

    display_name = "Growth Rando Max"
    range_start = 0
    range_end = 255
    default = 70


# CR-someday cam: think about how this interacts with creature campaign mode
class Goal(Choice):
    """
    Set the goal of the game.

    - Defeat Fomortiis: Defeat the usual final boss, which can take a long time.
    - Clear Valni: Clear the 8th floor of the Tower of Valni. Implies Enable Tower.
      Recommended for short- to medium-length games.
    - Defeat Tirado: Clear Chapter 8. Recommended for short games.
    - Clear Lagdou: Clear the 10th floor of the Lagdou Ruins. Implies Enable Ruins.

    Note that this option only change which check is considered the goal and
    does not affect progression logic at all.
    """

    display_name = "Goal"
    option_DefeatFormortiis = 0
    option_ClearValni = 1
    option_DefeatTirado = 2
    option_ClearLagdou = 3


class MusicRando(Choice):
    """
    Randomizes music tracks.

    - Context: Music tracks will be shuffled within the same group (battle themes
      will be randomized to other battle themes, etc)
    - Chaos: Music tracks will be shuffled randomly
    """

    option_Vanilla = 0
    alias_no = 0
    alias_off = 0
    option_Context = 1
    option_Chaos = 2
    alias_full = 2
    alias_all = 2


# CR-someday cam: Eventually, it would be nice to be able to generate this.
@dataclass
class FE8Options(PerGameCommonOptions):
    player_unit_rando: PlayerRando
    player_unit_monsters: PlayerMonsters
    super_demon_king: SuperDemonKing
    smooth_level_caps: SmoothLevelCapProgression
    min_endgame_level_cap: MinimumEndgameLevelCapRange
    required_holy_weapons: MinimumUsableHolyWeapons
    exclude_latona: ExcludeLatona
    easier_5x: Easier5x
    unbreakable_regalia: UnbreakableRegalia
    tower_enabled: EnableTower
    ruins_enabled: EnableRuins
    shuffle_skirmish_tables: ShuffleSkirmishTables
    lockpick_usability: LockpickUsability
    normalize_genders: NormalizeGenders
    death_link: DeathLink
    growth_rando: GrowthRando
    growth_rando_min: GrowthRandoMin
    growth_rando_max: GrowthRandoMax
    music_rando: MusicRando
    goal: Goal

    # Convenience methods for options that imply each other

    def tower_checks_enabled(self):
        return bool(self.tower_enabled) or self.goal == Goal.option_ClearValni

    def ruins_checks_enabled(self):
        return bool(self.ruins_enabled) or self.goal == Goal.option_ClearLagdou

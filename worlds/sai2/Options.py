from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, PerGameCommonOptions

class WorldState(Choice):
    """Closed: All 5 gates start closed.
       Random Open: Opens 5 random gates by default.
       Open: All 5 gates start open.
       If not open, you will start with 1 random progression item."""
    display_name = "World State"
    option_closed = 0
    option_open = 1
    option_random_open = 2
    default = 0

class ExtraStartingHealth(DefaultOnToggle):
    """If enabled, you will start with two hearts rather than one."""
    display_name = "Extra Starting Health"

class DisableRandomEncounters(DefaultOnToggle):
    """Disables random encounters on the overworld map."""
    display_name = "No Random Encounters"

class FastShovel(DefaultOnToggle):
    """Allows easily swapping to the Shovel and back by pressing Select on the menu."""
    display_name = "Fast Shovel"

class MagicQuickswap(DefaultOnToggle):
    """Allows swapping between magic spells by pressing L and R."""
    display_name = "Magic Quickswap"

class DefaultSwitchStates(Choice):
    """Define the default state the Switches will be found in."""
    display_name = "Switch States"
    option_normal = 0
    option_inverted = 1
    option_random_set = 2

class ShortcutStates(Choice):
    """All Closed: All shortcuts start closed.
       All Open: All Shortcuts start open.
       Random Open: Ranom shortcuts start open.
       Exclude Fuwa: Fuwa-Fuwa shortcuts will start closed regardless.

       Shortcuts that start open can be entered from their opposite side."""
    display_name = "Shortcuts"
    option_all_closed = 0
    option_all_open = 1
    option_random_open = 2
    option_random_exclude_fuwa = 3
    option_all_exclude_fuwa = 4
    default = 0

class ForceSpells(Toggle):
    """If enabled, the 5 island bosses will each lock 1 of the 5 Spells."""
    display_name = "Force Spells on Bosses"

class CasinoChecks(Toggle):
    """If enabled, will place the 5 items normally found in the Casino into the pool,
    and add checks on their purchases. The prices have been severly reduced to reduce the amount of grinding,
    but some may still be required."""
    display_name = "Casino Checks"

class OpenFuwa(Toggle):
    """If enabled, you will be able to access Fuwa-Fuwa Island without needing the 5 spells."""
    display_name = "Early Fuwa-Fuwa"

class ShuffleSkills(Choice):
    """Determines if the 3 techniques are in their normal location, shuffled amongst the 3 shops, or anywhere."""
    display_name = "Skills"
    option_normal = 0
    option_shuffled = 1
    option_in_pool = 2

class SpellLockEnding(Toggle):
    """If enabled, you will need to have the 5 Spells in order to use the Sky Bell and fight Phantom. Recommended to be used with 'Early Fuwa-Fuwa'."""
    display_name = "Locked Phantom"



@dataclass
class SAI2Options(PerGameCommonOptions):
    world_state: WorldState
    switch_states: DefaultSwitchStates
    shortcut_states: ShortcutStates
    phantom_spells: SpellLockEnding
    early_fuwa: OpenFuwa
    shuffle_skills: ShuffleSkills
    boss_spells: ForceSpells
    casino_checks: CasinoChecks
    extra_health: ExtraStartingHealth
    disable_encounters: DisableRandomEncounters
    fast_shovel: FastShovel
    magic_swap: MagicQuickswap

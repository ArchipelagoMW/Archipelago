from Options import (
    DeathLink,
    StartInventoryPool,
    PerGameCommonOptions,
    Choice,
    DefaultOnToggle,
    Toggle,
    Range,
)
from dataclasses import dataclass


class StartingWeapons(Choice):
    """Randomize what two weapons you start the game with.
    Vanilla: Start with the Lancer and Gravity Bomb.
    Balanced: Start with two random weapons that are relatively balanced.
    Non-Broken: Start with two random weapons besides RYNO II and Zodiac.
    Unrestricted: Start with any two non-upgraded weapons.
    """
    display_name = "Starting Weapons"
    option_vanilla = 0
    option_balanced = 1
    option_non_broken = 2
    option_unrestricted = 3
    default = 0


class RandomizeGadgetronVendor(Toggle):
    """Randomize what items appear at the Gadgetron vendor on Barlow."""
    display_name = "Randomize Gadgetron Vendor"


class RandomizeMegacorpVendor(Toggle):
    """ Randomize what items appear at the Megacorp vendor. New items will get added as you visit more planets.
    When enabled, you can switch between buying items and buying ammo by pressing up/down when in the vendor."""
    display_name = "Randomize Megacorp Vendor"


class ExcludeVeryExpensiveItems(DefaultOnToggle):
    """Exclude RYNO II and Zodiac from the randomization leaving them at their vanilla locations.
    This will only take effect if the corresponding vendors are randomized"""
    display_name = "Exclude Very Expensive Items"


class SkipWupashNebula(DefaultOnToggle):
    """Skips the Wupash Nebula ship section that appears when first traveling to Maktar Nebula."""
    display_name = "Skip Wupash Nebula"


class EnableBoltMultiplier(Toggle):
    """Enables the bolt multiplier feature without being in New Game+."""
    display_name = "Enable Bolt Multiplier"


class NoRevisitRewardChange(Toggle):
    """In the vanilla game, rewards given when killing enemies change when you come back to a previously visited planet
    (bolts & experience). Enabling this option removes this behavior, making the experience and bolts obtained more
    stable throughout the seed.
    """
    display_name = "Remove Revisit Rewards Change"


class NoKillRewardDegradation(Toggle):
    """In the vanilla game, rewards given by a specific enemy decrease each time you kill it (bolts & experience).
    Enabling this option removes this behavior, making the experience and bolts obtained more stable throughout
    the seed.
    """
    display_name = "Remove Kill Rewards Degradation"


class FreeChallengeSelection(Toggle):
    """Makes all hoverbike and spaceship challenges selectable right away, which means you don't have to win a
    challenge to access the next one."""
    display_name = "Free Challenge Selection"


class NanotechExperienceMultiplier(Range):
    """A multiplier applied to experience gained for Nanotech levels, in percent."""
    display_name = "Nanotech XP Multiplier"
    range_start = 20
    range_end = 600
    default = 100


class WeaponExperienceMultiplier(Range):
    """A multiplier applied to experience gained for weapon levels, in percent."""
    display_name = "Weapon XP Multiplier"
    range_start = 30
    range_end = 600
    default = 100


class ExtraSpaceshipChallengeLocations(Toggle):
    """In the vanilla game, only the first challenge and the race challenge completed perfectly give an item as a
    reward. If enabled, this option makes all spaceship challenges reward an item on first completion."""
    display_name = "Extra Spaceship Challenge Locations"


class ExtendWeaponProgression(Toggle):
    """If enabled, make all weapon tiers obtainable through weapon experience. This means LV2 (orange) weapons can
    upgrade into LV3 (yellow) weapons, which can then upgrade into LV4 (blue) weapons.
    This effectively makes all weapons that are usually restricted to NG+ available with enough grinding."""
    display_name = "Extended Weapon Progression"


class FirstPersonModeGlitchInLogic(Choice):
    """Determines if logic should take first person mode glitches into account when evaluating which locations are
    reachable. Various difficulty levels can be picked:
    - Easy: simple climbs (e.g. getting the Platinum Bolt near Oozla scientist)
    - Medium: harder climbs and basic lateral movement (e.g. Getting to the Notak Worker Bots without the Heli-pack nor the Thermanator)
    - Hard: full navigation following walls (e.g. Getting to the Mutated Protopet only with the Infiltrator)"""
    display_name = "First Person Mode Glitch In Logic"
    option_disabled = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    default = 0


@dataclass
class Rac2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    starting_weapons: StartingWeapons
    randomize_megacorp_vendor: RandomizeMegacorpVendor
    randomize_gadgetron_vendor: RandomizeGadgetronVendor
    exclude_very_expensive_items: ExcludeVeryExpensiveItems
    skip_wupash_nebula: SkipWupashNebula
    enable_bolt_multiplier: EnableBoltMultiplier
    no_revisit_reward_change: NoRevisitRewardChange
    no_kill_reward_degradation: NoKillRewardDegradation
    free_challenge_selection: FreeChallengeSelection
    nanotech_xp_multiplier: NanotechExperienceMultiplier
    weapon_xp_multiplier: WeaponExperienceMultiplier
    extra_spaceship_challenge_locations: ExtraSpaceshipChallengeLocations
    extend_weapon_progression: ExtendWeaponProgression
    first_person_mode_glitch_in_logic: FirstPersonModeGlitchInLogic

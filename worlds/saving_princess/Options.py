from dataclasses import dataclass
from typing import Dict, Any

from Options import PerGameCommonOptions, DeathLink, StartInventoryPool, Choice, DefaultOnToggle, Range, Toggle, \
    OptionGroup


class ExpandedPool(DefaultOnToggle):
    """
    Determines if places other than chests and special weapons will be locations.
    This includes boss fights as well as powering the tesla orb and completing the console login.
    In Expanded Pool, system power is instead restored when receiving the System Power item.
    Similarly, the final area door will open once the four Key items, one for each main area, have been found.
    """
    display_name = "Expanded Item Pool"


class InstantSaving(DefaultOnToggle):
    """
    When enabled, save points activate with no delay when touched.
    This makes saving much faster, at the cost of being unable to pick and choose when to save in order to save warp.
    """
    display_name = "Instant Saving"


class SprintAvailability(Choice):
    """
    Determines under which conditions the debug sprint is made accessible to the player.
    To sprint, hold down Ctrl if playing on keyboard, or Left Bumper if on gamepad (remappable).
    With Jacket: you will not be able to sprint until after the Jacket item has been found.
    """
    display_name = "Sprint Availability"
    option_never_available = 0
    option_always_available = 1
    option_available_with_jacket = 2
    default = option_available_with_jacket


class CliffWeaponUpgrade(Choice):
    """
    Determines which weapon Cliff uses against you, base or upgraded.
    This does not change the available strategies all that much.
    Vanilla: Cliff adds fire to his grenades if Ace has been defeated.
    If playing with the expanded pool, the Arctic Key will trigger the change instead.
    """
    display_name = "Cliff Weapon Upgrade"
    option_never_upgraded = 0
    option_always_upgraded = 1
    option_vanilla = 2
    default = option_always_upgraded


class AceWeaponUpgrade(Choice):
    """
    Determines which weapon Ace uses against you, base or upgraded.
    Ace with his base weapon is very hard to dodge, the upgraded weapon offers a more balanced experience.
    Vanilla: Ace uses ice attacks if Cliff has been defeated.
    If playing with the expanded pool, the Volcanic Key will trigger the change instead.
    """
    display_name = "Ace Weapon Upgrade"
    option_never_upgraded = 0
    option_always_upgraded = 1
    option_vanilla = 2
    default = option_always_upgraded


class ScreenShakeIntensity(Range):
    """
    Percentage multiplier for screen shake effects.
    0% means the screen will not shake at all.
    100% means the screen shake will be the same as in vanilla.
    """
    display_name = "Screen Shake Intensity %"
    range_start = 0
    range_end = 100
    default = 50


class IFramesDuration(Range):
    """
    Percentage multiplier for Portia's invincibility frames.
    0% means you will have no invincibility frames.
    100% means invincibility frames will be the same as vanilla.
    """
    display_name = "IFrame Duration %"
    range_start = 0
    range_end = 400
    default = 100


class TrapChance(Range):
    """
    Likelihood of a filler item becoming a trap.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 50


class MusicShuffle(Toggle):
    """
    Enables music shuffling.
    The title screen song is not shuffled, as it plays before the client connects.
    """
    display_name = "Music Shuffle"



class BattleLog(Choice):
    """
    Determines if defeating each enemy type for the first time counts as a check.
    If extra goodies is selected, new items (5 of each) are added to the pool to help fill these new locations:
    - Armor Up, which increases Portia's iframes by 20%.
    - Weapon Up, which decreases enemy iframes by 10% and increases weapon damage by 20%.
    """
    display_name = "Battle Log Checks"
    option_disabled = 0
    option_enabled = 1
    option_extra_goodies = 2
    default = option_extra_goodies
    rich_text_doc = True

@dataclass
class SavingPrincessOptions(PerGameCommonOptions):
    # generation options
    start_inventory_from_pool: StartInventoryPool
    expanded_pool: ExpandedPool
    battle_log: BattleLog
    trap_chance: TrapChance
    # gameplay options
    death_link: DeathLink
    instant_saving: InstantSaving
    sprint_availability: SprintAvailability
    cliff_weapon_upgrade: CliffWeaponUpgrade
    ace_weapon_upgrade: AceWeaponUpgrade
    iframes_duration: IFramesDuration
    # aesthetic options
    shake_intensity: ScreenShakeIntensity
    music_shuffle: MusicShuffle


groups = [
    OptionGroup("Generation Options", [
        ExpandedPool,
        BattleLog,
        TrapChance,
    ]),
    OptionGroup("Gameplay Options", [
        DeathLink,
        InstantSaving,
        SprintAvailability,
        CliffWeaponUpgrade,
        AceWeaponUpgrade,
        IFramesDuration,
    ]),
    OptionGroup("Aesthetic Options", [
        ScreenShakeIntensity,
        MusicShuffle,
    ]),
]

presets = {
    "Vanilla-like": {
        "expanded_pool": False,
        "battle_log_checks": BattleLog.option_disabled,
        "trap_chance": 0,

        "instant_saving": False,
        "sprint_availability": SprintAvailability.option_never_available,
        "cliff_weapon_upgrade": CliffWeaponUpgrade.option_vanilla,
        "ace_weapon_upgrade": AceWeaponUpgrade.option_vanilla,
        "iframes_duration": 100,

        "shake_intensity": 100,
    },
    "Easy": {
        "expanded_pool": True,
        "battle_log_checks": BattleLog.option_extra_goodies,
        "trap_chance": 0,

        "instant_saving": True,
        "sprint_availability": SprintAvailability.option_always_available,
        "cliff_weapon_upgrade": CliffWeaponUpgrade.option_never_upgraded,
        "ace_weapon_upgrade": AceWeaponUpgrade.option_always_upgraded,
        "iframes_duration": 200,
    },
    "Hard": {
        "expanded_pool": True,
        "battle_log_checks": BattleLog.option_enabled,
        "trap_chance": 100,

        "instant_saving": True,
        "sprint_availability": SprintAvailability.option_never_available,
        "cliff_weapon_upgrade": CliffWeaponUpgrade.option_always_upgraded,
        "ace_weapon_upgrade": AceWeaponUpgrade.option_never_upgraded,
        "iframes_duration": 50,
    }
}

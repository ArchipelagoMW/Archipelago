from dataclasses import dataclass

from Options import PerGameCommonOptions, DeathLink, StartInventoryPool, Choice, DefaultOnToggle, Range, Toggle, \
    OptionGroup


class ExpandedPool(Choice):
    """
    Determines if clearing boss fights, powering the tesla orb and completing the console login will be checks.
    In Expanded Pool, system power is restored by the System Power item instead of by powering the tesla orb.
    Similarly, the final area door will open once enough of the four Key items, one for each main area, have been found.
    The number of Key items required is determined by the Final Area Locks option.

    Finally, if coop is selected, expanded pool locations will sync across players playing the same slot:
    - Boss kills will result in that boss being defeated for everyone playing that slot.
    - Checking the console at the start of the game will check it for all players on that slot.
    - Powering the tesla orb will do so for all players on that slot.
    """
    display_name = "Expanded Item Pool"
    option_disabled = 0
    option_enabled = 1
    option_coop = 2
    default = option_enabled
    rich_text_doc = True


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


class TrapLink(Toggle):
    """
    When you receive a trap, everyone who enabled trap link does. Of course, the reverse is true too.
    Games with trap link enabled will try to convert the trap to an equivalent one.

    If you receive a trap link that would be converted to a trap with a weight of 0, the trap link will be ignored.
    """
    display_name = "Trap Link"


class MusicShuffle(Toggle):
    """
    Enables music shuffling.
    The title screen song is not shuffled, as it plays before the client connects.
    """
    display_name = "Music Shuffle"


class FinalLockCount(Range):
    """
    Determines how many area bosses defeated or keys collected are needed to enter the final area.
    If Expanded Pool is disabled, area bosses will need to be defeated, like in vanilla.
    If Expanded Pool is enabled, keys will be needed instead.
    """
    display_name = "Final Area Locks"
    range_start = 0
    range_end = 4
    default = 2


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


class BlastDoors(Choice):
    """
    Determines the type of each of the three blast doors found in the hub.
    - Vanilla: All blast doors require the Powered Blaster.
    - Random without repeats: Each blast door requires a different randomly selected special weapon to open.
    - Random uniform: All blast doors require the same randomly selected special weapon to open.
    - Fully random: Each blast door requires a randomly selected special weapon to open.
    - Remove blast doors: There are no blast doors, so no special weapons are required to open them.
    """
    display_name = "Randomize Blast Doors"
    option_vanilla = 0
    option_random_without_repeats = 1
    option_random_uniform = 2
    option_fully_random = 3
    option_remove_blast_doors = 4
    default = option_random_without_repeats
    rich_text_doc = True


class TrapWeight(Choice):
    """
    Relative likelihood of this type of trap to be selected for the pool.
    For example, a trap with a weight of 4 will be twice as likely to be included as a trap with a weight of 2.

    Setting a trap's weight to 0 will prevent it from ever appearing, including as a result of Trap Link.

    Effect of this trap:
    """
    option_disabled = 0
    option_low = 1
    option_normal = 2
    option_high = 4
    default = option_normal


class IceTrapWeight(TrapWeight):
    __doc__ = TrapWeight.__doc__ + "\nFreezes Portia in place for a few seconds."
    display_name = "Ice Trap Weight"


class ShakeTrapWeight(TrapWeight):
    __doc__ = TrapWeight.__doc__ + "\n\nMakes the screen shake with (harmless) explosions for a few seconds."
    display_name = "Shake Trap Weight"


class NinjaTrapWeight(TrapWeight):
    __doc__ = TrapWeight.__doc__ + "\n\nSpawns the ninja to fight you."
    display_name = "Ninja Trap Weight"


class TextTrapWeight(TrapWeight):
    __doc__ = TrapWeight.__doc__ + "\n\nDisplays a bunch of text."
    display_name = "Text Trap Weight"


@dataclass
class SavingPrincessOptions(PerGameCommonOptions):
    # generation options
    start_inventory_from_pool: StartInventoryPool
    final_locks: FinalLockCount
    expanded_pool: ExpandedPool
    battle_log: BattleLog
    blast_doors: BlastDoors
    trap_chance: TrapChance
    # trap weight
    ice_weight: IceTrapWeight
    shake_weight: ShakeTrapWeight
    ninja_weight: NinjaTrapWeight
    text_weight: TextTrapWeight
    # gameplay options
    instant_saving: InstantSaving
    sprint_availability: SprintAvailability
    cliff_weapon_upgrade: CliffWeaponUpgrade
    ace_weapon_upgrade: AceWeaponUpgrade
    iframes_duration: IFramesDuration
    # link options
    death_link: DeathLink
    trap_link: TrapLink
    # aesthetic options
    shake_intensity: ScreenShakeIntensity
    music_shuffle: MusicShuffle


groups = [
    OptionGroup("Generation Options", [
        FinalLockCount,
        ExpandedPool,
        BattleLog,
        BlastDoors,
        TrapChance,
    ]),
    OptionGroup("Trap Weights", [
        IceTrapWeight,
        ShakeTrapWeight,
        NinjaTrapWeight,
        TextTrapWeight,
    ]),
    OptionGroup("Gameplay Options", [
        InstantSaving,
        SprintAvailability,
        CliffWeaponUpgrade,
        AceWeaponUpgrade,
        IFramesDuration,
    ]),
    OptionGroup("Link Options", [
        DeathLink,
        TrapLink,
    ]),
    OptionGroup("Aesthetic Options", [
        ScreenShakeIntensity,
        MusicShuffle,
    ]),
]

presets = {
    "Vanilla-like": {
        "final_locks": 4,
        "expanded_pool": ExpandedPool.option_disabled,
        "battle_log": BattleLog.option_disabled,
        "blast_doors": BlastDoors.option_vanilla,
        "trap_chance": 0,

        "instant_saving": False,
        "sprint_availability": SprintAvailability.option_never_available,
        "cliff_weapon_upgrade": CliffWeaponUpgrade.option_vanilla,
        "ace_weapon_upgrade": AceWeaponUpgrade.option_vanilla,
        "iframes_duration": 100,

        "shake_intensity": 100,
    },
    "Easy": {
        "final_locks": 2,
        "expanded_pool": ExpandedPool.option_enabled,
        "battle_log": BattleLog.option_extra_goodies,
        "blast_doors": BlastDoors.option_random_without_repeats,
        "trap_chance": 0,

        "instant_saving": True,
        "sprint_availability": SprintAvailability.option_always_available,
        "cliff_weapon_upgrade": CliffWeaponUpgrade.option_never_upgraded,
        "ace_weapon_upgrade": AceWeaponUpgrade.option_always_upgraded,
        "iframes_duration": 200,
    },
    "Hard": {
        "final_locks": 4,
        "expanded_pool": ExpandedPool.option_enabled,
        "battle_log": BattleLog.option_enabled,
        "blast_doors": BlastDoors.option_fully_random,
        "trap_chance": 100,

        "instant_saving": True,
        "sprint_availability": SprintAvailability.option_never_available,
        "cliff_weapon_upgrade": CliffWeaponUpgrade.option_always_upgraded,
        "ace_weapon_upgrade": AceWeaponUpgrade.option_never_upgraded,
        "iframes_duration": 50,
    }
}

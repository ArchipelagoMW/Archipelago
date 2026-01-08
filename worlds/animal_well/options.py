from dataclasses import dataclass
from typing import Dict, Any
from Options import (DefaultOnToggle, Toggle, StartInventoryPool, Choice, Range, PerGameCommonOptions, OptionGroup,
                     DeathLink, Removed)


class Goal(Choice):
    """
    What you need to do to beat the game.
    Fireworks requires you to get the 4 flames and defeat the Manticore. The House Key is placed in its vanilla location.
    Egg Hunt requires you to collect the amount of eggs you need to open the 4th Egg Door, then open the chest inside.
    """
    internal_name = "goal"
    display_name = "Goal"
    option_fireworks = 1
    # option_bunny_land = 2 TODO(Frank-Pasqualini)
    option_egg_hunt = 3
    default = 1


class FinalEggLocation(Toggle):
    """
    Choose whether the 65th Egg is shuffled into the multiworld item pool or placed in its vanilla location, requiring opening the 4th Egg Door to access it.
    This option is forced on if you have the egg hunt goal selected.
    """
    internal_name = "random_final_egg_location"
    display_name = "Randomize Final Egg"


# todo: client needs work to get this to work with other values - TODO(Frank-Pasqualini)
class EggsNeeded(Range):
    """
    How many Eggs you need to open the 4th Egg Door.
    The amount of Eggs you need for the other 3 doors will scale accordingly.
    This is intentionally locked at 64 until we can figure it out client-side.
    """
    internal_name = "eggs_needed"
    display_name = "Eggs Required"
    range_start = 64
    range_end = 64
    default = 64


class BunniesAsChecks(Choice):
    """
    Include the secret bunnies as checks.
    Exclude Tedious removes the Mural, Dream, UV, and Floor is Lava bunnies.
    The Disc Spike bunny will not be a check unless you have multiple disc hops or you have both precise tricks and wheel tricks enabled.
    """
    internal_name = "bunnies_as_checks"
    display_name = "Bunnies as Checks"
    option_off = 0
    option_exclude_tedious = 1
    option_all_bunnies = 2
    default = 0


class BunnyWarpsInLogic(Toggle):
    """
    Include the songs that warp you to Bunny spots in logic.
    If you have Bunnies as Checks enabled, this option is automatically enabled.
    """
    internal_name = "bunny_warps_in_logic"
    display_name = "Bunny Warps in Logic"


class CandleChecks(Toggle):
    """
    Lighting each of the candles sends a check.
    """
    internal_name = "candle_checks"
    display_name = "Candle Checks"


class Fruitsanity(Toggle):
    """
    All 115 fruits send a check after being eaten.
    Tip: Attempting to eat a fruit 3 times will eat it even if you have full health.
    """
    internal_name = "fruitsanity"
    display_name = "Fruitsanity"


class KeyRing(DefaultOnToggle):
    """
    Have one keyring which unlocks all normal key doors instead of individual key items.
    Note: Due to how consumable key logic works, if this option is not enabled, you logically require all 6 keys to open any of the key doors.
    """
    internal_name = "key_ring"
    display_name = "Key Ring"


class Matchbox(DefaultOnToggle):
    """
    Have one matchbox which can light all candles instead of individual match items.
    Note: Due to how consumable item logic works, if this option is not enabled, you logically require all 9 matches to light any of the candles.
    """
    internal_name = "matchbox"
    display_name = "Matchbox"


class BubbleJumping(Choice):
    """
    Include using the standard Bubble Wand and chaining bubble jumps together in logic.
    Short Chains means you may be expected to chain a few bubble jumps in a row.
    Long Chains means you may be expected to chain an unlimited number of bubble jumps in a row.
    """
    internal_name = "bubble_jumping"
    display_name = "Bubble Jumping"
    option_off = 0
    option_short_chains = 1
    alias_exclude_long_chains = 1
    option_long_chains = 2
    alias_on = 2
    default = 1


class DiscHopping(Choice):
    """
    Include jumping onto the disc without letting it bounce off of a wall first in logic.
    Single means doing it once from the ground.
    Multiple means having to chain them in midair.
    """
    internal_name = "disc_hopping"
    display_name = "Midair Disc Jumping"
    option_off = 0
    option_single = 1
    option_multiple = 2
    default = 0


class WheelTricks(Choice):
    """
    Include some tricks that involve using the wheel in unconventional ways.
    Simple means toggling wheel midair to "double jump", or mashing against walls to climb them.
    Advanced also adds more complicated tech, such as braking on walls or climbing walls out of jumps.
    Note: Tricks using wheel desyncs or wrong warps are not ever considered logical.
    """
    internal_name = "wheel_tricks"
    display_name = "Wheel Tricks"
    option_off = 0
    option_simple = 1
    option_advanced = 2
    default = 0


class BallThrowing(Choice):
    """
    Include using the ball to hit switches or buttons not "designed" for it in logic.
    Off means the ball will rarely be used for anything other than breaking blocks, spikes, or guard shields.
    Simple means the ball can be used to hit easy targets without any real rebound, setup, or movement. Most "yoyo chute" buttons are included here.
    Advanced means hitting your target may require bouncing off a wall or moving while throwing to adjust momentum/angle.
    Expert includes more complicated tricks including those that require specific setups or getting lucky.
    """									
    internal_name = "ball_throwing"
    display_name = "Ball Throwing"
    option_off = 0
    option_simple = 1
    option_advanced = 2
    option_expert = 3
    default = 1


class FluteJumps(Toggle):
    """
    Include sliding off of the edge of a platform while pulling out the flute so that you can jump mid-air while playing the flute.
    """
    internal_name = "flute_jumps"
    display_name = "Flute Jumps"


class ObscureTricks(Toggle):
    """
    Include solutions to puzzles that are obscure or hard to understand in logic.
    These tricks won't be harder to perform than other tricks in logic once you know them.
    """
    internal_name = "obscure_tricks"
    display_name = "Obscure Tricks"


class PreciseTricks(Toggle):
    """
    Include solutions to puzzles that are mechanically difficult to execute in logic.
    These tricks may require large amounts of attempts to get right, and there may be a higher than usual cost for failure.
    """
    internal_name = "precise_tricks"
    display_name = "Precise Tricks"


class TankingDamage(Toggle):
    """
    Include tricks which require you to voluntarily take damage in order to perform them in logic.
    You may be expected to take up to three points of damage to perform tricks enabled by this option.
    """
    internal_name = "tanking_damage"
    display_name = "Tanking Damage"


class ExcludeSongChests(DefaultOnToggle):
    """
    Exclude the Wheel chest and Office Key chests, so that you don't have to play their songs.
    They will contain either filler or traps.
    """
    internal_name = "exclude_song_chests"
    display_name = "Exclude Song Chests"


class AWDeathLink(DeathLink):
    __doc__ = (DeathLink.__doc__ + "\n\n    You can toggle this in the Client by using /deathlink, "
                                   "or in your host.yaml.")


@dataclass
class AnimalWellOptions(PerGameCommonOptions):
    goal: Goal
    eggs_needed: EggsNeeded
    key_ring: KeyRing
    matchbox: Matchbox
    
    candle_checks: CandleChecks
    bunnies_as_checks: BunniesAsChecks
    bunny_warps_in_logic: BunnyWarpsInLogic
    fruitsanity: Fruitsanity
    exclude_song_chests: ExcludeSongChests
    random_final_egg_location: FinalEggLocation

    tanking_damage: TankingDamage
    bubble_jumping: BubbleJumping
    disc_hopping: DiscHopping
    wheel_tricks: WheelTricks
    ball_throwing: BallThrowing
    flute_jumps: FluteJumps
    obscure_tricks: ObscureTricks
    precise_tricks: PreciseTricks
    
    death_link: AWDeathLink
    start_inventory_from_pool: StartInventoryPool

    wheel_hopping: Removed
    weird_tricks: Removed


aw_option_groups = [
    OptionGroup("Logic Options", [
        TankingDamage,
        BubbleJumping,
        DiscHopping,
        WheelTricks,
        BallThrowing,
        FluteJumps,
        ObscureTricks,
        PreciseTricks,
    ])
]

aw_option_presets: Dict[str, Dict[str, Any]] = {
    "Animal Hell": {
        "eggs_needed": 64,
        "bubble_jumping": BubbleJumping.option_long_chains,
        "disc_hopping": DiscHopping.option_multiple,
        "wheel_tricks": WheelTricks.option_advanced,
        "bunnies_as_checks": BunniesAsChecks.option_all_bunnies,
        "ball_throwing": BallThrowing.option_expert,
        "flute_jumps": FluteJumps.option_true,
        "obscure_tricks": ObscureTricks.option_true,
        "precise_tricks": PreciseTricks.option_true,
        "tanking_damage": TankingDamage.option_true,
        "fruitsanity": Fruitsanity.option_true,
    },
}

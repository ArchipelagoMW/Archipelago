from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Toggle, DeathLink, Range, OptionGroup, StartInventoryPool


class Goal(Choice):
    """
    Golden Diva: Defeat the four main passage bosses, reach the depths of the pyramid, and defeat the Golden Diva
    Golden Treasure Hunt: Find the golden treasures scattered in the world, and escape through the Sound Room
    Golden Diva Treasure Hunt: Find the golden treasures, and then defeat the Golden Diva
    Local Golden Treasure Hunt: Find the treasures scattered in the pyramid and escape through the Sound Room
    Local Golden Diva Treasure Hunt: Find the golden treasures in the pyramid and defeat the Golden Diva
    """
    display_name = 'Goal'
    option_golden_diva = 0
    option_golden_treasure_hunt = 1
    option_golden_diva_treasure_hunt = 2
    option_local_golden_treasure_hunt = 3
    option_local_golden_diva_treasure_hunt = 4
    alias_divahunt = option_golden_diva_treasure_hunt
    alias_local_divahunt = option_local_golden_diva_treasure_hunt
    default = option_golden_diva

    def needs_diva(self):
        return self == Goal.option_golden_diva or self.is_diva_hunt()

    def needs_treasure_hunt(self):
        return self.is_treasure_hunt() or self.is_diva_hunt()

    def is_treasure_hunt(self):
        return self in (Goal.option_golden_treasure_hunt, Goal.option_local_golden_treasure_hunt)

    def is_diva_hunt(self):
        return self in (Goal.option_golden_diva_treasure_hunt, Goal.option_local_golden_diva_treasure_hunt)


class GoldenTreasureCount(Range):
    """
    Number of treasures required to win in Golden Treasure Hunt.
    """
    display_name = 'Golden Treasure Count'
    range_start = 1
    range_end = 12
    default = 6  # Minimum for a good ending


class Difficulty(Choice):
    """
    The game's difficulty level.
    Hard and S-Hard have slightly fewer locations to check since some Full Health item boxes are missing on those difficulties.
    """
    display_name = 'Difficulty'
    option_normal = 0
    option_hard = 1
    option_s_hard = 2
    default = option_normal


class Logic(Choice):
    """
    Advanced logic enables some strategies that are more difficult or can risk forcing a Give Up, many of which involve Grab.
    A list of these strategies can be found on the game page.
    """
    display_name = 'Logic'
    option_basic = 0
    option_advanced = 1
    default = option_basic


class PoolJewels(Range):
    """
    Number of jewels in the item pool per passage for the main four.
    The number of pieces will be four times this number.
    """
    range_start = 0
    range_end = 4
    default = 3
    display_name = 'Jewels in Pool'


class GoldenJewels(Range):
    """
    Number of copies of the golden pyramid jewel in the item pool.
    """
    range_start = 0
    range_end = 2
    default = 1
    display_name = 'Golden Pyramid Jewels'


class RequiredJewels(Range):
    """
    Number of jewels required to fight the bosses.
    The Entry Passage and Golden Pyramid always require 1 unless this option is
    set to 0.
    """
    range_start = 0
    range_end = 4
    default = 2
    display_name = 'Required Jewels'


class RestrictSelfLockingJewelPieces(Toggle):
    """
    Restrict extra jewel pieces from being placed on their own bosses or in the
    Golden Passage in treasure hunt modes. The latter does not apply to the
    golden jewel pieces.
    """
    display_name = 'Restrict Self-Locking Jewel Pieces'


class OpenDoors(Choice):
    """
    Start with all doors in the passages unlocked. This skips the requirement
    to find Keyzer in each level, opening more locations earlier.
    """
    display_name = 'Open Level Doors'
    option_off = 0
    option_closed_diva = 1
    option_open = 2
    default = option_closed_diva


class Portal(Choice):
    """
    Behavior of the portal and item collection.
    Vanilla: The exit portal closes, and Wario must reopen it with the frog switch
    Open: The portal stays open, allowing Wario to leave at any time.
    """
    display_name = 'Portal'
    option_vanilla = 0
    option_open = 1
    default = option_vanilla


class DiamondShuffle(Toggle):
    """
    Shuffle the 1,000-point diamonds into the item pool.
    """
    display_name = 'Diamond Shuffle'


class SmashThroughHardBlocks(Toggle):
    """
    Break hard, teal blocks with the dash attack and super ground pound without stopping,
    as in Pizza Tower and Wario Land: Shake It!
    This option does not affect logic.
    """
    display_name = 'Smash Hard Blocks Without Stopping'


class MultiworldSend(Choice):
    """
    When to tell the server you've found items.
    On Escape: Only count your locations after the game saves. If you die or give up, the items you found will be hinted.
    Immediately: Count your locations as you take them from the box.
    Regardless of this setting, sending other players items from a level you can't clear is never in logic.
    """
    display_name = 'Send Locations to Server'
    option_on_escape = 0
    option_immediately = 1
    default = option_on_escape


class PrizeWeight(Range):
    """
    How often to place prizes (full health items, diamonds) when filling vacant spots in the item pool.
    """
    display_name = 'Prize Weight'
    range_start = 0
    range_end = 100
    default = 30


class JunkWeight(Range):
    """
    How often to place junk items (hearts, minigame medals) when filling vacant spots in the item pool.
    """
    display_name = 'Junk Weight'
    range_start = 0
    range_end = 100
    default = 60


class TrapWeight(Range):
    """
    How often to place traps when filling vacant spots in the item pool.
    """
    display_name = 'Trap Weight'
    range_start = 0
    range_end = 100
    default = 10


class TrapBehavior(Choice):
    """
    What happens if multiple traps get sent to you while you aren't playing a level.
    Accumulate: Every trap you receive will be applied the next time you enter.
    Apply Once: You will be forcibly transformed or hurt only once.
    If you die in a level with several traps accumulated, they will be limited to one each the next time you enter.
    """
    display_name = 'Trap Behavior'
    option_accumulate = 0
    option_apply_once = 1
    default = option_accumulate


class MusicShuffle(Choice):
    """
    Music shuffle type
    None: Music is not shuffled
    Levels Only: Only shuffle music between the main levels
    Levels And Extras: Shuffle any music that plays in levels, including the 'Hurry up!' and boss themes
    Full: Shuffle all music
    Disabled: Disable all music
    """
    display_name = 'Music Shuffle'
    option_none = 0
    option_levels_only = 1
    option_levels_and_extras = 2
    option_full = 3
    option_disabled = 4
    default = 0


class WarioVoiceShuffle(Toggle):
    """
    Randomize the things Wario says.
    """
    display_name = "Shuffle Wario's voices"


wl4_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        GoldenTreasureCount,
    ]),
    OptionGroup("World", [
        Difficulty,
        RequiredJewels,
        OpenDoors,
        Portal,
    ]),
    OptionGroup("Item Pool", [
        PoolJewels,
        GoldenJewels,
        RestrictSelfLockingJewelPieces,
        DiamondShuffle,
        PrizeWeight,
        JunkWeight,
        TrapWeight,
    ]),
    OptionGroup("Quality of Life", [
        MultiworldSend,
        TrapBehavior,
        SmashThroughHardBlocks,
    ]),
    OptionGroup("Cosmetic", [
        MusicShuffle,
        WarioVoiceShuffle,
    ]),
]


@dataclass
class WL4Options(PerGameCommonOptions):
    logic: Logic
    death_link: DeathLink
    goal: Goal
    golden_treasure_count: GoldenTreasureCount
    difficulty: Difficulty
    required_jewels: RequiredJewels
    open_doors: OpenDoors
    portal: Portal
    pool_jewels: PoolJewels
    golden_jewels: GoldenJewels
    restrict_self_locking_jewel_pieces: RestrictSelfLockingJewelPieces
    diamond_shuffle: DiamondShuffle
    prize_weight: PrizeWeight
    junk_weight: JunkWeight
    trap_weight: TrapWeight
    send_locations_to_server: MultiworldSend
    trap_behavior: TrapBehavior
    smash_through_hard_blocks: SmashThroughHardBlocks
    music_shuffle: MusicShuffle
    wario_voice_shuffle: WarioVoiceShuffle
    start_inventory_from_pool: StartInventoryPool

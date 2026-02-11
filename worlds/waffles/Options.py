from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionSet, OptionGroup, PerGameCommonOptions, Visibility, StartInventoryPool


class Goal(Choice):
    """
    Determines the goal of the seed

    Bowser: Find a certain number of Yoshi Eggs, reach Bowser's Castle and defeat Bowser

    Yoshi's House: Find a certain number of Yoshi Eggs and bring them back to Yoshi's House
    """
    display_name = "Goal"
    option_bowser = 0x01
    option_yoshi_house = 0x02
    default = 0x01


class NumberOfYoshiEggs(Range):
    """
    Amount of Golden Yoshi Eggs that can be found anywhere in the multiworld/itempool.

    The amount of eggs rolled by this option will be added to the amount of eggs created by the Local Golden Yoshi Eggs option
    and both of them will not exceed the 255 egg limit.
    """
    display_name = "Yoshi Egg Count"
    range_start = 0
    range_end = 255
    default = 50


class LocalYoshiEggPlacement(OptionSet):
    """
    Forces Golden Yoshi Eggs into specific level exits.
    This option will create a new location in each level that's valid, that way it doesn't disturb your potential Priority Locations
    in said regions. Similar to how Boss Tokens operated before.

    The "Every Level" option has priority over the others, creating an at least 96 egg game.

    The amount of eggs rolled by this option will be added to the amount of eggs created by the yoshi_egg_count option
    and both of them will not exceed the 255 egg limit.
    """
    display_name = "Local Yoshi Egg Placement"
    valid_keys = {
        "Every Level",
        "Castles",
        "Switch Palaces",
        "Ghost Houses",
        "Special Zone",
    }
    default = {
        "Castles",
        "Switch Palaces",
        "Ghost Houses",
        "Special Zone",
    }


class PercentageOfYoshiEggs(Range):
    """
    What Percentage of Yoshi Eggs are required to finish.

    This option will sum yoshi_egg_placement and yoshi_egg_count, then it'll calculate the required amount from that egg count.
    """
    display_name = "Required Percentage of Golden Yoshi Eggs"
    range_start = 1
    range_end = 100
    default = 85


class DragonCoinChecks(Toggle):
    """
    Whether collecting 5 Dragon Coins in each level will grant a check
    """
    display_name = "Dragon Coin Checks"


class MoonChecks(Toggle):
    """
    Whether collecting a 3-Up Moon in a level will grant a check
    """
    display_name = "3up Moon Checks"


class Hidden1UpChecks(Toggle):
    """
    Whether collecting a hidden 1-Up mushroom in a level will grant a check

    These checks are considered cryptic as there's no actual indicator that they're in their respective places
    
    Enable this option at your own risk
    """
    display_name = "Hidden 1-Up Checks"


class StarBlockChecks(Toggle):
    """
    Whether collecting a prize from a Star Block in a level will grant a check
    """
    display_name = "Star Block Checks"


class MidwayChecks(Toggle):
    """
    Whether collecting a Midway Point in a level will grant a check
    """
    display_name = "Midway Point Checks"


class RoomChecks(Toggle):
    """
    Whether visiting a room in levels will grant a check
    """
    display_name = "Room Checks"


class BlockChecks(OptionSet):
    """
    Whether hitting a block with an item or coin inside will grant a check
    
    Note that some blocks are excluded due to how the option and the game works!
    Exclusion list:
      * Blocks in Top Secret Area & Front Door/Bowser Castle
      * Blocks that are unreachable unless you glitch your way in
    """
    display_name = "Block Checks"
    default = {
        "Coin Blocks",
        "Item Blocks",
        "Yellow Switch Palace Blocks",
        "Green Switch Palace Blocks",
        "Invisible Blocks",
        "P-Switch Blocks",
        "Flying Blocks",
    }
    valid_keys = {
        "Coin Blocks",
        "Item Blocks",
        "Yellow Switch Palace Blocks",
        "Green Switch Palace Blocks",
        "Invisible Blocks",
        "P-Switch Blocks",
        "Flying Blocks",
    }


class BowserCastleDoors(Choice):
    """
    How the doors of Bowser's Castle behave

    Vanilla: Front and Back Doors behave as vanilla

    Fast: Both doors behave as the Back Door

    Slow: Both doors behave as the Front Door

    "Front Door" rooms depend on the `bowser_castle_rooms` option

    "Back Door" only requires going through the dark hallway to Bowser
    """
    display_name = "Bowser Castle Doors"
    option_vanilla = 0
    option_fast = 1
    option_slow = 2
    default = 0


class BowserCastleRooms(Choice):
    """
    How the rooms of Bowser's Castle Front Door behave

    Vanilla: You can choose which rooms to enter, as in vanilla

    Random Two Room: Two random rooms are chosen

    Random Five Room: Five random rooms are chosen

    Gauntlet: All eight rooms must be cleared

    Labyrinth: Which room leads to Bowser?
    """
    display_name = "Bowser Castle Rooms"
    option_vanilla = 0
    option_random_two_room = 1
    option_random_five_room = 2
    option_gauntlet = 3
    option_labyrinth = 4
    default = 1


class BossShuffle(Choice):
    """
    How bosses are shuffled

    None: Bosses are not shuffled

    Simple: Four Reznors and the seven Koopalings are shuffled around

    Full: Each boss location gets a fully random boss

    Singularity: One or two bosses are chosen and placed at every boss location
    """
    display_name = "Boss Shuffle"
    option_none = 0
    option_simple = 1
    option_full = 2
    option_singularity = 3
    default = 0


class LevelEffects(Range):
    """
    How many levels will receive a permanent random trap effect in them
    Which traps are going to be used is going to be determined by their trap weight

    Valid traps: Ice, Reverse, Screen Flip, Pixelate, Spotlight, Invisibility

    Setting Game Logic Difficulty option to easy or medium is recommended.
    """
    display_name = "Random Level Effects"
    range_start = 0
    range_end = 50
    default = 0


class LevelShuffle(Toggle):
    """
    Whether levels are shuffled
    """
    display_name = "Level Shuffle"


class StartingLocation(Choice):
    """
    Which location is your starting one
    May interact incorrectly with forced Collects
    Will throw errors on certain option combinations, please test your YAML
    """
    display_name = "Starting Location"
    option_yoshis_island = 0
    option_donut_plains = 1
    option_vanilla_dome = 2
    option_forest_of_illusion = 3
    option_special_zone = 4
    default = 0


class MapTeleportShuffle(Choice):
    """
    Whether map teleports (stars and pipes) are shuffled
    """
    display_name = "Map Teleport Shuffle"
    option_off = 0
    option_on_only_stars = 1
    option_on_only_pipes = 2
    option_on_both_same_type = 3
    option_on_both_mix = 4
    default = 0


class MapTransitionShuffle(Toggle):
    """
    Wheter map transitions are shuffled
    """
    display_name = "Map Transition Shuffle"
    

#class ExcludeSpecialZone(Toggle):
#    """
#    If active, this option will prevent any progression items from being placed in Special Zone levels.
#
#    Additionally, if Level Shuffle is active, Special Zone levels will not be shuffled away from their vanilla tiles.
#    """
#    display_name = "Exclude Special Zone"


class SwapDonutGhostHouseExits(DefaultOnToggle):
    """
    If enabled, this option will swap which overworld direction the two exits of the level at the Donut Ghost House overworld tile go:

    False: Normal Exit goes up, Secret Exit goes right.

    True: Normal Exit goes right, Secret Exit goes up.

    This option has priority over Swap Level Exits.
    """
    display_name = "Swap Donut GH Exits"


class CarrylessExits(Range):
    """
    Swaps some Keyholes with a Red Goal Orb which triggers the Secret Exit upon touching it
    """
    display_name = "Carryless Exit Count"
    range_start = 0
    range_end = 18
    default = 0


class SwapLevelExits(Toggle):
    """
    Swaps the destination of level exits in the map

    Star World 5 and Donut Secret House are excluded from this feature
    """
    display_name = "Swap Level Exits"


class SwapExitCount(Range):
    """
    How many swapped exits will exist in the game
    """
    display_name = "Swap Exit Count"
    range_start = 0
    range_end = 22
    default = 0


class EnemyShuffle(Toggle):
    """
    Shuffles around enemies.
    """
    display_name = "Enemy Shuffle"


class AbilityItemShuffle(OptionSet):
    """
    Which abilities and items will be added as items in the item pool
    If an ability is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Ability Shuffle"
    default = {
        "Run",
        "Carry",
        "Swim",
        "Spin Jump",
        "Climb",
        "P-Balloon",
        "Yoshi",
        "Powerups",
        "Super Star",
        "P-Switch",
        "Item Box",
        "Midway Points",
        "Yellow Switch Palace",
        "Green Switch Palace",
        "Red Switch Palace",
        "Blue Switch Palace",
        "Special World",
    }
    valid_keys = {
        "Run",
        "Carry",
        "Swim",
        "Spin Jump",
        "Climb",
        "P-Balloon",
        "Yoshi",
        "Powerups",
        "Super Star",
        "P-Switch",
        "Item Box",
        "Midway Points",
        "Yellow Switch Palace",
        "Green Switch Palace",
        "Red Switch Palace",
        "Blue Switch Palace",
        "Special World",
    }


class GameLogicDifficulty(Choice):
    """
    Makes difficult levels expect the player to have certain amount of powerups in order to beat them

    Easy: Hard levels require Mushroom + (Item box or Midway Points);
          Harder levels require Fire Flower + (Extra Defense or Item box or Midway Points)
    Medium: Hard levels require Mushroom;
            Harder levels require Mushroom + (Item box or Midway Points)
    Hard: No powerups or other items are required in any level to be beaten
    """
    display_name = "Game Logic Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    default = 0


class InventoryYoshiLogic(Toggle):
    """
    Whether being able to use Yoshi inventory items is considered in logic or not for Blue Yoshi logic
    """
    display_name = "Inventory Yoshi Logic"


class DisplayReceivedItemPopups(Choice):
    """
    What messages to display in-game for items received
    """
    display_name = "Display Received Item Popups"
    option_none = 0
    option_all = 1
    option_progression = 2
    option_progression_minus_yoshi_eggs = 3
    default = 3


class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required Yoshi Eggs in the item pool with random junk items
    """
    display_name = "Junk Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2


class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the level to become slippery
    """
    display_name = "Ice Trap Weight"


class StunTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which briefly stuns Mario
    """
    display_name = "Stun Trap Weight"


class LiteratureTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the player to read literature
    """
    display_name = "Literature Trap Weight"


class TimerTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the timer to run low
    """
    display_name = "Timer Trap Weight"


class ReverseTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the controls to be reversed in the current level
    """
    display_name = "Reverse Trap Weight"
    
    
class ThwimpTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes a Thwimp to spawn above the player
    """
    display_name = "Thwimp Trap Weight"
    

class FishinBooTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes a Fishin' Boo to spawn above the player
    """
    display_name = "Fishin' Boo Trap Weight"


class ScreenFlipTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the screen to flip vertically
    """
    display_name = "Screen Flip Trap Weight"

    
class StickyFloorTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the floor become sticky
    """
    display_name = "Sticky Floor Trap Weight"

    
class StickyHandsTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the player's hands become sticky
    """
    display_name = "Sticky Hands Trap Weight"

    
class PixelateTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes a the entire screen become pixelated
    """
    display_name = "Pixelate Trap Weight"
    

class SpotlightTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes a spotlight to appear on the player's position
    """
    display_name = "Spotlight Trap Weight"


class BulletTimeTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which slows down the game
    """
    display_name = "Bullet Time Trap Weight"


class InvisibilityTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which makes the player invisible
    """
    display_name = "Invisibility Trap Weight"


class EmptyItemBoxTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which removes the item in the item box
    """
    display_name = "Empty Item Box Trap Weight"


class EarlyClimb(Toggle):
    """
    Force Climb to appear early in the seed as a local item.

    This is particularly useful to prevent BK when Level Shuffle is disabled
    """
    display_name = "Early Climb"


class MusicShuffle(Choice):
    """
    Music shuffle type

    None: No Music is shuffled

    Consistent: Each music track is consistently shuffled throughout the game

    Full: Each individual level has a random music track

    Singularity: The entire game uses one song for overworld and one song for levels
    """
    display_name = "Music Shuffle"
    option_none = 0
    option_consistent = 1
    option_full = 2
    option_singularity = 3
    default = 0


class SFXShuffle(Choice):
    """
    Shuffles almost every instance of sound effect playback

    Archipelago elements that play sound effects aren't randomized

    None: No SFX are shuffled

    Full: Each individual SFX call has a random SFX

    Singularity: The entire game uses one SFX for every SFX call
    """
    display_name = "Sound Effect Shuffle"
    option_none = 0
    option_full = 1
    option_singularity = 2
    default = 0


class MarioPalette(Choice):
    """
    Mario palette color
    """
    display_name = "Mario Palette"
    option_mario = 0
    option_luigi = 1
    option_wario = 2
    option_waluigi = 3
    option_geno = 4
    option_princess = 5
    option_dark = 6
    option_sponge = 7
    default = 0


class EnergyLink(DefaultOnToggle):
    """
    Allows players to contribute to the EnergyLink pool by collecting coins

    Players can exchange EnergyLink coins for consumable items
    """
    display_name = "Energy Link"


class RingLink(Toggle):
    """
    Whether your in-level coin gain/loss is linked to other players

    DISABLED FOR NOW. Please wait for future updates that reenables this feature.
    """
    display_name = "Ring Link"


class TrapLink(Toggle):
    """
    Whether your received traps are linked to other players
    """
    display_name = "Trap Link"


class UngoldenEggs(DefaultOnToggle):
    """
    Does exactly what you're thinking of.
    """
    display_name = "No mas huevos dorados"
    visibility = Visibility.template | Visibility.simple_ui | Visibility.complex_ui


waffle_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        NumberOfYoshiEggs,
        LocalYoshiEggPlacement,
        PercentageOfYoshiEggs,
    ]),
    OptionGroup("Logic", [
        AbilityItemShuffle,
        GameLogicDifficulty,
        InventoryYoshiLogic,
    ]),
    OptionGroup("Location Options", [
        DragonCoinChecks,
        MoonChecks,
        Hidden1UpChecks,
        StarBlockChecks,
        MidwayChecks,
        RoomChecks,
        BlockChecks,
    ]),
    OptionGroup("Level Shuffling", [
        StartingLocation,
        LevelShuffle,
        LevelEffects,
        CarrylessExits,
        SwapLevelExits,
        SwapExitCount,
        SwapDonutGhostHouseExits,
        MapTeleportShuffle,
        MapTransitionShuffle,
        #ExcludeSpecialZone,
        EnemyShuffle,
        BowserCastleDoors,
        BowserCastleRooms,
        BossShuffle,
    ]),
    OptionGroup("Junk and Traps", [
        JunkFillPercentage,
        TrapFillPercentage,
        IceTrapWeight,
        StunTrapWeight,
        LiteratureTrapWeight,
        TimerTrapWeight,
        ReverseTrapWeight,
        ThwimpTrapWeight,
        FishinBooTrapWeight,
        ScreenFlipTrapWeight,
        StickyFloorTrapWeight,
        StickyHandsTrapWeight,
        PixelateTrapWeight,
        SpotlightTrapWeight,
        BulletTimeTrapWeight,
        InvisibilityTrapWeight,
        EmptyItemBoxTrapWeight,
    ]),
    OptionGroup("Aesthetics", [
        DisplayReceivedItemPopups,
        MusicShuffle,
        SFXShuffle,
        MarioPalette,
        UngoldenEggs,
    ]),
]


@dataclass
class WaffleOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    ring_link: RingLink
    trap_link: TrapLink
    energy_link: EnergyLink
    ability_shuffle: AbilityItemShuffle
    game_logic_difficulty: GameLogicDifficulty
    inventory_yoshi_logic: InventoryYoshiLogic
    goal: Goal
    yoshi_egg_count: NumberOfYoshiEggs
    percentage_of_yoshi_eggs: PercentageOfYoshiEggs
    yoshi_egg_placement: LocalYoshiEggPlacement
    dragon_coin_checks: DragonCoinChecks
    moon_checks: MoonChecks
    hidden_1up_checks: Hidden1UpChecks
    star_block_checks: StarBlockChecks
    midway_point_checks: MidwayChecks
    room_checks: RoomChecks
    block_checks: BlockChecks
    bowser_castle_doors: BowserCastleDoors
    bowser_castle_rooms: BowserCastleRooms
    level_effects: LevelEffects
    level_shuffle: LevelShuffle
    starting_location: StartingLocation
    map_teleport_shuffle: MapTeleportShuffle
    map_transition_shuffle: MapTransitionShuffle
    carryless_exits: CarrylessExits
    swap_level_exits: SwapLevelExits
    swap_exit_count: SwapExitCount
    swap_donut_gh_exits: SwapDonutGhostHouseExits
    #exclude_special_zone: ExcludeSpecialZone
    boss_shuffle: BossShuffle
    enemy_shuffle: EnemyShuffle
    display_received_item_popups: DisplayReceivedItemPopups
    junk_fill_percentage: JunkFillPercentage
    trap_fill_percentage: TrapFillPercentage
    ice_trap_weight: IceTrapWeight
    stun_trap_weight: StunTrapWeight
    literature_trap_weight: LiteratureTrapWeight
    timer_trap_weight: TimerTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    thwimp_trap_weight: ThwimpTrapWeight
    fishin_trap_weight: FishinBooTrapWeight
    screen_flip_trap_weight: ScreenFlipTrapWeight
    sticky_floor_trap_weight: StickyFloorTrapWeight
    sticky_hands_trap_weight: StickyHandsTrapWeight
    pixelate_trap_weight: PixelateTrapWeight
    spotlight_trap_weight: SpotlightTrapWeight
    bullet_time_trap_weight: BulletTimeTrapWeight
    invisibility_trap_weight: InvisibilityTrapWeight
    empty_item_box_trap_weight: EmptyItemBoxTrapWeight
    early_climb: EarlyClimb
    music_shuffle: MusicShuffle
    sfx_shuffle: SFXShuffle
    mario_palette: MarioPalette
    ungolden_eggs: UngoldenEggs

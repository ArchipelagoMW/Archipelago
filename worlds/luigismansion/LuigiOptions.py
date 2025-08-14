from dataclasses import dataclass

from Options import Toggle, Range, PerGameCommonOptions, Choice, StartInventoryPool, DeathLinkMixin, OptionSet, \
    DefaultOnToggle


class LuigiWalkSpeed(Choice):
    """Choose how fast Luigi moves. Speeds above normal may cause OoB issues"""
    display_name = "Walk Speed"
    internal_name = "walk_speed"
    option_normal_speed = 0
    option_kinda_fast = 1
    option_schmoovin = 2
    default = 0

class GameMode(Choice):
    """
    Enable alternate game modes:

    Default - Play through the mansion as usual

    Poltergust Hunt - You must first find the Poltergust 3000 inside a piece of furniture before use. Enabling this will
    automatically add certain pieces of furniture to the pool of locations even if other furniture options are turned off.
    This will also unlock all doors in the mansion. This is intended as a short form game mode
    """
    display_name = "Game Mode"
    internal_name = "game_mode"
    option_default = 0
    option_poltergust_hunt = 1
    default = 0


class RandomMusic(Toggle):
    """Randomize Music"""
    display_name = "Music Randomization"
    internal_name = "random_music"


class BundleWeight(Range):
    """Set the weight for how often coin & bill bundles get chosen as filler."""
    display_name = "Money Bundle Weight"
    internal_name = "bundle_weight"
    range_start = 0
    range_end = 100
    default = 10


class CoinWeight(Range):
    """Set the weight for how often coins get chosen as filler."""
    display_name = "Coin Weight"
    internal_name = "coin_weight"
    range_start = 0
    range_end = 100
    default = 15


class BillWeight(Range):
    """Set the weight for how often bills get chosen as filler."""
    display_name = "Bill Weight"
    internal_name = "bill_weight"
    range_start = 0
    range_end = 100
    default = 10


class BarsWeight(Range):
    """Set the weight for how often gold bars get chosen as filler."""
    display_name = "Gold Bars Weight"
    internal_name = "bars_weight"
    range_start = 0
    range_end = 100
    default = 10


class GemsWeight(Range):
    """Set the weight for how often gemstones get chosen as filler."""
    display_name = "Gems Weight"
    internal_name = "gems_weight"
    range_start = 0
    range_end = 100
    default = 5


class PoisonTrapWeight(Range):
    """Set the weight for how often poison mushrooms get chosen as traps."""
    display_name = "Poison Trap Weight"
    internal_name = "poison_trap_weight"
    range_start = 0
    range_end = 100
    default = 15


class BombWeight(Range):
    """Set the weight for how often bombs get chosen as traps."""
    display_name = "Bomb Weight"
    internal_name = "bomb_trap_weight"
    range_start = 0
    range_end = 100
    default = 15


class IceTrapWeight(Range):
    """Set the weight for how often ice traps get chosen as traps."""
    display_name = "Ice Trap Weight"
    internal_name = "ice_trap_weight"
    range_start = 0
    range_end = 100
    default = 15


class BananaTrapWeight(Range):
    """Set the weight for how often bananas get chosen as traps."""
    display_name = "Banana Trap Weight"
    internal_name = "banana_trap_weight"
    range_start = 0
    range_end = 100
    default = 15


class NothingWeight(Range):
    """Set the weight for how often dust is chosen as filler."""
    display_name = "Dust Weight"
    internal_name = "dust_weight"
    range_start = 0
    range_end = 100
    default = 40


class HeartWeight(Range):
    """Set the weight for how often hearts get chosen as filler."""
    display_name = "Heart Weight"
    internal_name = "heart_weight"
    range_start = 0
    range_end = 100
    default = 10


class BetterVacuum(Choice):
    """
    Choose whether to include the Poltergust 4000.

    If you start with the upgrade on a no-poltergust start, you will receive the base poltergust instead"""
    display_name = "Poltergust 4000"
    internal_name = "good_vacuum"
    option_start_with = 0
    option_include = 1
    option_exclude = 2
    default = 1


# These might end up being the same
class StartHiddenMansion(Toggle):
    """Begin in the Hidden Mansion"""
    display_name = "Hidden Mansion"
    internal_name = "hidden_mansion"


class SpeedySpirits(Toggle):
    """Adds Blue Ghosts to location pool. These have moved to be only available during blackout so they cannot be missed"""
    display_name = "Speedy Spirits"
    internal_name = "speedy_spirits"


class StartWithBooRadar(Choice):
    """
    Start with Boo Radar

    start_with: Start with Boo Radar

    include: Boo Radar in pool

    exclude: No Boo Radar - generation will fail if excluded while Boo Gates or Boosanity are enabled
    """
    display_name = "Boo Radar"
    internal_name = "boo_radar"
    option_start_with = 0
    option_include = 1
    option_exclude = 2
    default = 1


class PortraitHints(Toggle):
    """Choose to add hints to the scans of the Portrait Ghosts' Hearts in the mansions"""
    display_name = "Portrait Ghost Hints"
    internal_name = "portrait_hints"


class HintDistribution(Choice):
    """Choose the level of hint from in-game hints. Will affect Portrait Ghost hints if the option is on."""
    display_name = "Hint Distribution"
    internal_name = "hint_distribution"
    option_balanced = 0
    option_junk = 1
    option_chaos = 2
    option_strong = 3
    option_vague = 4
    option_disabled = 5
    default = 0

class PickupAnim(DefaultOnToggle):
    """Turn on Luigi's pickup animations.
    Set this to false if you want to turn these animations off."""
    display_name = "Enable Pickup Animation"
    internal_name = "enable_pickup_animation"


class Toadsanity(Toggle):
    """Add Toads as locations to be checked."""
    display_name = "Toadsanity"
    internal_name = "toadsanity"


class Lightsanity(Toggle):
    """Adds the act of lighting up rooms as locations."""
    display_name = "Lightsanity"
    internal_name = "lightsanity"


class Walksanity(Toggle):
    """Adds the act of visiting rooms as locations."""
    display_name = "Walksanity"
    internal_name = "walksanity"


class Furnisanity(OptionSet):
    """
    Adds interactable objects, such as dressers, paintings, candles, and light fixtures, to the location pool.

    Different sets of locations can be added within the list. Valid strings are:

    "Hangables" includes items on walls such as paintings and other decor

    "Decor" includes items such as instruments and suits of armor

    "Ceiling" includes ceiling fans and lights attached to the ceiling

    "Candles" includes any candles that can be interacted with

    "Seating" includes chairs, stools and other typs of seating

    "Surfaces" includes tables and other flat items

    "Storage" includes things like barrels, boxes and shelves

    "Plants" includes all waterable plants in the mansion

    "Drawers" includes dressers, drawers, end tables and similar items

    "Treasures" turns on only locations that contain treasure (including all plants) in the vanilla game. Does not create duplicate locations

    "Basement, 1st Floor, 2nd FLoor, Attic, and Roof can be used to turn on all furniture pieces on that level.

    "Full" turns on all furniture locations and will override any other specified groups
    """
    display_name = "Furnisanity"
    internal_name = "furnisanity"
    valid_keys = {"Hangables", "Ceiling", "Candles", "Seating", "Surfaces", "Plants", "Storage", "Drawers", "Decor", "Full", "Treasures", "Basement", "1st Floor", "2nd Floor", "Attic", "Roof"}


class EarlyFirstKey(Toggle):
    """
    If enabled, this will attempt to find a key that lets you out of your starting room and place it early in your own world.
    """
    display_name = "Early First Key"
    internal_name = "early_first_key"


class BooGates(Toggle):
    """
    Toggle the events that prevent progress unless a certain number of boos have been caught

    Default to on. If this is turned off, the Boo Count options are ignored.
    """
    display_name = "Boo Gates"
    internal_name = "boo_gates"
    default = 1


class MarioItems(Range):
    """How many Mario Items it takes to capture the Fortune-Teller. 0 = Starts Capturable"""
    display_name = "Fortune-Teller Requirements"
    internal_name = "mario_items"
    range_start = 0
    range_end = 5
    default = 5


# class WashroomBooCount(Range):
#     """Set the number of Boos required to reach the 1F Washroom. 0 = Starts Open"""
#     display_name = "Washroom Boo Count"
#     internal_name = "washroom_boo_count"
#     range_start = 0
#     range_end = 50
#     default = 5


class BalconyBooCount(Range):
    """Set the number of Boos required to reach the Balcony. 0 = Starts Open"""
    display_name = "Balcony Boo Count"
    internal_name = "balcony_boo_count"
    range_start = 0
    range_end = 36
    default = 20


class KingBooHealth(Range):
    """Set King Boo's health in the final fight."""
    display_name = "King Boo's Health"
    internal_name = "king_boo_health"
    range_start = 1
    range_end = 1000
    default = 500


class FinalBooCount(Range):
    """Set the number of Boos required to reach the Secret Altar. 0 = Starts Open"""
    display_name = "Altar Boo Count"
    internal_name = "final_boo_count"
    range_start = 0
    range_end = 50
    default = 40


class Boosanity(Toggle):
    """Turns Boos into Items and Locations."""
    display_name = "Boosanity"
    internal_name = "boosanity"


class Portrification(Toggle):
    """Turn Portrait Ghosts into checks in addition to their clear chests."""
    display_name = "Portrification"
    internal_name = "portrification"


class Enemizer(Choice):
    """
    Choose if and how ghosts are randomized.

    Vanilla - No ghost randomization

    Randomized Elements - Randomized ghost elements and waves

    No Elements - Remove ghost elements, randomize waves
    """
    display_name = "Enemizer"
    internal_name = "enemizer"
    option_vanilla = 0
    option_randomized_elements = 1
    option_no_elements = 2
    default = 0

class VacuumStart(DefaultOnToggle):
    """
    Enable Luigi to have the Poltergust 3000 at the start
    """
    display_name = "Starting Vacuum"
    internal_name = "vacuum_start"


class DoorRando(Choice):
    """
    Various options regarding which doors are locked or unlocked in the mansion.

    Off - Doors are in their vanilla state

    Randomized - All doors are randomly locked or unlocked

    Suit Doors - Randomize doors but guarantee the Suit Key Doors remain locked

    All Doors Unlocked - Unlocks all doors in the mansion. Without Boo gates, this will make King Boo immediately accessible.

    All Doors Locked - Locks all door in the mansion.
    """
    display_name = "Door Randomization"
    internal_name = "door_rando"
    option_off = 0
    option_randomized = 1
    option_suit_doors = 2
    option_all_doors_unlocked = 3
    option_all_doors_locked = 4
    default = 0



class LuigiFearAnim(DefaultOnToggle):
    """Turn on Luigi being scared by ghosts if they spawn close to him.
    Set this to false if you want to turn it off"""
    display_name = "Enable Fear Animation"
    internal_name = "enable_fear_animation"


class ChestTypes(Choice):
    """
    Determines how chest colors and size are chosen,

    vanilla: Chests are their original size and color

    default: Size and color are determined by attempting to match the item type to a representative color similar to the vanilla game

    full_random: Size and color are chosen completely at random.

    color: Chest color represents the AP item classification

    size_and_color: Both size and color are determined by AP item classification

    no_fuzzy_matching: Same as default but uses item classification for other players' items
    """
    display_name = "Chest Cosmetics"
    internal_name = "chest_types"
    option_vanilla = 0
    option_default = 1
    option_full_random = 2
    option_color = 3
    option_size_and_color = 4
    option_no_fuzzy_matching = 5
    default = 0


class TrapChestType(Choice):
    """
    Determines if chests containing traps can look like progression items

    filler: Trap chests only appear as traps

    progression: Trap chests only appear as progression

    anything: Trap chests can appear as anything
    """
    display_name = "Trap Appearance"
    internal_name = "trap_chests"
    option_filler = 0
    option_progression = 1
    option_anything = 2
    default = 0


class RankRequirement(Choice):
    """
    Choose the required rank (H to A) to complete the game, with A being the highest.

    Rank H requires any amount of money to finish the game, including 0

    Rank A requires 5 Gold Diamonds (or equivalent money) to finish the game
    """
    display_name = "Rank Requirement"
    internal_name = "rank_requirement"
    option_rank_h = 0
    option_rank_g = 1
    option_rank_f = 2
    option_rank_e = 3
    option_rank_d = 4
    option_rank_c = 5
    option_rank_b = 6
    option_rank_a = 7


class RandomSpawn(Toggle):
    """
    Allows Luigi to randomly spawn somewhere in the mansion.
    """
    display_name = "Random Spawn Location"
    internal_name = "random_spawn"
    default = 0


class BooHealthOption(Choice):
    """
    Choose how Boo Health is determined

    Choice: Use Boo Health Value to set all boos to the specified value

    Random Values: Every boo has a different, randomly chosen health value between 1 and the value set in Boo Health Value

    Boo Health by Sphere: Boos will receive health values based on the spheres they are in. Boo Health Value will determine the highest health a Boo can have

    Vanilla: No changes are made to Boos from the base game. Boos with HP over 150 may not be catchable within the current room and logic cannot account for where they move
    """
    display_name = "Boo Health Option"
    internal_name = "boo_health_option"
    option_choice = 0
    option_random_values = 1
    option_boo_health_by_sphere = 2
    option_vanilla = 3
    default = 0

class BooHealthValue(Range):
    """
    Choose the health value all Boos will have if the Boo Health Option is Choice. Range between 1 and 999

    Values over 150 may not be catchable within the current room and logic cannot account for where they move

    If you have a boo go into an area you cannot access yet, you may need to save and quit to main menu to reload them.
    """
    display_name = "Boo Health Value"
    internal_name = "boo_health_value"
    range_start = 1
    range_end = 999
    default = 30

class BooSpeed(Range):
    """
    Choose how fast boos move. Range from 1 to 36
    """
    display_name = "Boo Speed"
    internal_name = "boo_speed"
    range_start = 1
    range_end = 36
    default = 15


class BooEscapeTime(Range):
    """
    Choose how long before Boos leave the current room. Range between 1 and 300.

    Values below 90 may not be catchable within the current room and logic cannot account for where they move
    """
    display_name = "Boo Escape Time"
    internal_name = "boo_escape_time"
    range_start = 1
    range_end = 300
    default = 120

class BooAnger(Toggle):
    """
    Choose whether boos can damage Luigi.
    """
    display_name = "Angry Boos"
    internal_name = "boo_anger"
    default = 0

class EnergyLink(Toggle):
    """
    Games that support energylink will be able to send and retrieve 'energy' from the team's pool. 
    If no team is present, the default team will be used (0).
    
    'Energy' in the context of Luigi's Mansion will be money.
    """
    display_name = "EnergyLink"
    internal_name = "energy_link"

class TrapLink(Toggle):
    """
    Games that support traplink will all receive similar traps when a matching trap is sent from another traplink game
    """
    display_name = "TrapLink"
    internal_name = "trap_link"


class GoldMice(Toggle):
    """
    Adds Gold Mice as locations to be checked.

    Logic requires these to be obtained after blackout so they can't be missed. They can be acquired without black out, out of logic.
    """
    display_name = " Gold Mice"
    internal_name = "gold_mice"


class ExtraBooSpots(Toggle):
    """
    Adds extra spots for boos to hide in when furniture locations have been added to the pool
    """
    display_name = "Extra Boo Spots"
    internal_name = "extra_boo_spots"


class LuigiMaxHealth(Range):
    """
    Adjust Luigi's maximum health value, 1-1000. Values 5 or below should be treated as One-Hit KO
    """
    display_name = "Luigi's Maximum Health"
    internal_name = "luigi_max_health"
    range_start = 1
    range_end = 1000
    default = 100

class FearWeight(Range):
    """
    Set the weight for how often fear traps get chosen as traps.
    """
    display_name = "Fear Trap Weight"
    internal_name = "fear_weight"
    range_start = 0
    range_end = 100
    default = 25

class SpookyWeight(Range):
    """
    Set the weight for how often spooky time gets chosen as a trap.
    """
    display_name = "Spooky Time Weight"
    internal_name = "spooky_weight"
    range_start = 0
    range_end = 100
    default = 25

class SquashWeight(Range):
    """
    Set the weight for how often Squash traps get chosen as traps.
    """
    display_name = "Squash Trap Weight"
    internal_name = "squash_weight"
    range_start = 0
    range_end = 100
    default = 15

class VacTrapWeight(Range):
    """
    Set the weight for how often No Vac traps get chosen as traps.
    """
    display_name = "No Vac Trap Weight"
    internal_name = "vac_trap_weight"
    range_start = 0
    range_end = 100
    default = 5

class BoolossusDifficulty(Choice):
    """
    Alter the difficulty of the mini-boos in the Boolossus fight. Easy slows them down, Hard speeds them up.
    """
    display_name = "Boolossus Diffculty"
    internal_name = "boolossus_difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1

class PossTrapWeight(Range):
    """
    Set the weight for how often possession traps get chosen as traps.
    """
    display_name = "Possession Trap Weight"
    internal_name = "poss_trap_weight"
    range_start = 0
    range_end = 100
    default = 5

class BonkTrapWeight(Range):
    """
    Set the weight for how often bonk traps get chosen as traps.
    """
    display_name = "Bonk Trap Weight"
    internal_name = "bonk_trap_weight"
    range_start = 0
    range_end = 100
    default = 15

class GhostTrapWeight(Range):
    """
    Set the weight for how often ghosts get chosen as traps.
    """
    display_name = "Ghost Weight"
    internal_name = "ghost_weight"
    range_start = 0
    range_end = 100
    default = 15

class CallMario(Toggle):
    """
    Let everyone know you're looking for Mario in teh client!
    (CAUTION: THIS CAN EASILY SPAM THE CLIENT WITH MESSAGES)
    """
    display_name = "Press A to Mario"
    internal_name = "call_mario"

class DoorModelRando(Toggle):
    """
    Randomly choose models for every door in the mansion.
    """
    display_name = "Randomized Door Model"
    internal_name = "door_model_rando"


class TrapPercentage(Range):
    """
    Set the percentage of filler items that are traps. Default percentage is 0%
    """
    display_name = "Trap Percentage"
    internal_name = "trap_percentage"
    range_start = 0
    range_end = 100
    default = 0

@dataclass
class LMOptions(DeathLinkMixin, PerGameCommonOptions):
    rank_requirement: RankRequirement
    game_mode: GameMode
    vacuum_start: VacuumStart
    walk_speed: LuigiWalkSpeed
    good_vacuum: BetterVacuum
    boo_radar: StartWithBooRadar
    hidden_mansion: StartHiddenMansion
    enable_fear_animation: LuigiFearAnim
    enable_pickup_animation: PickupAnim
    luigi_max_health: LuigiMaxHealth
    random_music: RandomMusic
    door_model_rando: DoorModelRando
    early_first_key: EarlyFirstKey
    door_rando: DoorRando
    enemizer: Enemizer
    random_spawn: RandomSpawn
    portrait_hints: PortraitHints
    hint_distribution: HintDistribution
    toadsanity: Toadsanity
    gold_mice: GoldMice
    furnisanity: Furnisanity
    boosanity: Boosanity
    portrification: Portrification
    lightsanity: Lightsanity
    walksanity: Walksanity
    speedy_spirits: SpeedySpirits
    boo_gates: BooGates
    mario_items: MarioItems
    #washroom_boo_count: WashroomBooCount
    balcony_boo_count: BalconyBooCount
    final_boo_count: FinalBooCount
    king_boo_health: KingBooHealth
    boolossus_difficulty: BoolossusDifficulty
    boo_health_option: BooHealthOption
    boo_health_value: BooHealthValue
    boo_speed: BooSpeed
    boo_escape_time: BooEscapeTime
    boo_anger: BooAnger
    extra_boo_spots: ExtraBooSpots
    chest_types: ChestTypes
    trap_chests: TrapChestType
    call_mario: CallMario
    trap_link: TrapLink
    energy_link: EnergyLink
    trap_percentage: TrapPercentage
    bundle_weight: BundleWeight
    coin_weight: CoinWeight
    bill_weight: BillWeight
    bars_weight: BarsWeight
    gems_weight: GemsWeight
    poison_trap_weight: PoisonTrapWeight
    bomb_trap_weight: BombWeight
    ice_trap_weight: IceTrapWeight
    banana_trap_weight: BananaTrapWeight
    poss_trap_weight: PossTrapWeight
    bonk_trap_weight: BonkTrapWeight
    ghost_weight: GhostTrapWeight
    fear_weight: FearWeight
    spooky_weight: SpookyWeight
    squash_weight: SquashWeight
    vac_trap_weight: VacTrapWeight
    dust_weight: NothingWeight
    heart_weight: HeartWeight
    start_inventory_from_pool: StartInventoryPool

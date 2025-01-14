from dataclasses import dataclass
from Options import Toggle, DeathLink, PerGameCommonOptions, Choice, DefaultOnToggle, Range, StartInventoryPool, FreeText

class RandomizeBTMoveList(DefaultOnToggle):
    """Jamjars' & Roysten's Movelist are randomized."""
    display_name = "Randomize Banjo-Tooie Movelist"

class DialogCharacters(Choice):
    """Change the character that announces your obtained moves, worlds, etc."""
    display_name = "Dialog Character"
    option_GLOWBO = 0
    option_JIGGY = 1
    option_HONEYCOMB = 2
    option_SUB = 3
    option_WASHER = 4
    option_BANJO = 5
    option_KAZOOIE = 6
    option_BOTTLES = 7
    option_MUMBO = 8
    option_JINJO_YELLOW = 9
    option_JINJO_GREEN = 10
    option_JINJO_BLUE = 11
    option_JINJO_PURPLE = 12
    option_JINJO_ORANGE = 13
    option_BEEHIVE = 14
    option_GRUNTY = 15
    option_ZUBBA = 16
    option_JAMJARS = 17
    option_BOVINA = 18
    option_MINJO_WHITE = 19
    option_MINJO_ORANGE = 20
    option_MINJO_YELLOW = 21
    option_MINJO_BROWN = 22
    option_UNOGOPAZ = 23
    option_CHIEF_BLOATAZIN = 24
    option_DILBERTA = 25
    option_STONIES1 = 26
    option_CANARY_MARY = 27
    option_CHEATO = 28
    option_GOBI = 29
    option_DINO_KID1 = 30
    option_MR_PATCH = 31
    option_MOGGY = 32
    option_SOGGY = 33
    option_GROGGY = 34
    option_MRS_BOGGY = 35
    option_PROSPECTOR = 36
    option_HUMBA = 37
    option_UFO = 38
    option_OLD_KING_COAL = 39
    option_SSSLUMBER = 40
    option_BOGGY = 41
    option_BIG_AL = 42
    option_SALTY_JOE = 43
    option_CONGA = 44
    option_PAWNO = 45
    option_TIPTUP = 46
    option_JOLLY = 47
    option_MERRY_MAGGIE = 48
    option_TERRY = 49
    option_BARGASAURUS = 50
    option_YELLOW_STONY = 51
    option_ALIEN = 52
    option_CHRIS_P_BACON = 53
    option_CAPTAIN_BLUBBER = 54
    option_STYRACOSAURUS_MOM = 55
    option_ROYSTEN = 56
    option_SAFE = 57
    option_GUFFO = 58
    option_MR_FIT = 59
    option_CAPTAIN_BLACKEYE = 60
    option_JINJO_RED = 61
    option_JINJO_WHITE = 62
    option_JINJO_BLACK = 63
    option_JINJO_BROWN = 64
    option_CHILLY_WILLY = 65
    option_CHILLI_BILLI = 66
    option_MINGY_JONGO = 67
    option_YELLOW_DODGEM = 68
    option_MINGELLA = 69
    option_BLOBBELDA = 70
    option_KLUNGO = 71
    option_BOTTLES_DEAD = 72
    option_MINJO_GREEN = 73
    option_MINJO_RED = 74
    option_MINJO_BLUE = 75
    option_MINJO_PURPLE = 76
    option_MINJO_BLACK = 77
    option_RABBIT_WORKER1 = 78
    option_UNGA_BUNGA = 79
    option_JIGGYWIGGY = 80
    option_JIGGYWIGGY_DISCIPLE = 81
    option_HONEY_B = 82
    option_BANJO_KAZOOIE = 83
    option_PIG1 = 84
    option_OOGLE_BOOGLE = 85
    option_GI_ANNOUNCER = 86
    option_DINGPOT = 87
    option_KING_JINGALING_DEAD = 88
    option_ROCKNUT = 89
    option_MILDRED = 90
    option_BIGGA_FOOT = 91
    option_GEORGE = 92
    option_SABREMAN = 93
    option_DIPPY = 94
    option_LOGGO = 95
    option_KING_JINGALING = 96
    option_MRS_BOTTLES = 97
    option_SPECCY = 98
    option_GOGGLES = 99
    option_TARGITZAN = 100
    option_CHOMPA = 101
    option_LORD_WOO_FAK_FAK = 102
    option_WELDAR = 103
    option_ALIEN_CHILD = 104
    option_EVIL_BOTTLES = 105
    option_DINO_KID2 = 106
    option_DINO_SCRIT_SMALL = 107
    option_DINO_SCRIT_BIG = 108
    option_HEGGY = 109
    option_default_icons = 110
    option_complete_random = 255
    default = 110

class JamjarsSiloCosts(Choice):
    """Change how many notes it takes to use Jamjars' move silos. Requires the Banjo-Tooie move list to be randomized."""
    display_name = "Jamjars' Silo Costs"
    option_vanilla = 0
    option_randomize = 1
    option_progressive = 2
    default = 0

class RandomizeBKMoveList(Choice):
    """Banjo-Kazooie's Movelist are randomized.
    Mcjiggy Special - Talon Trot and Tall Jump are removed from the pool."""
    display_name = "Randomize Banjo-Kazooie Movelist"
    option_none = 0
    option_mcjiggy_special = 1
    option_all = 2
    default = 0

class ProgressiveBeakBuster(Toggle):
    """Beak Buster to Bill Drill. Randomize Moves and Randomize BK Moves are required."""
    display_name = "Progressive Beak Buster"

class EggsBehaviour(Choice):
    """Change the way Eggs work. Randomize Moves and Randomize BK Moves are required."""
    display_name = "Egg Behaviour"
    option_start_with_blue_eggs = 0
    option_random_starting_egg = 1
    option_progressive_eggs = 2
    default = 0

class ProgressiveShoes(Toggle):
    """Stilt Stride to Turbo Trainers to Spring Boots to Claw Climber Boots. Randomize Moves and Randomize BK Moves are required."""
    display_name = "Progressive Kazooie Shoes"

class ProgressiveWaterTraining(Choice):
    """Basic: Dive to Double Air to Faster Swimming.
    Advanced: Dive to Sub Aqua Aiming to Talon Torpedo to Double Air to Faster Swimming.
    Randomize Moves and Randomize BK Moves are required."""
    display_name = "Progressive Water Training"
    option_none = 0
    option_basic = 1
    option_advanced = 2

class ProgressiveEggAim(Choice):
    """Basic: Third Person Egg Shooting to Egg Aim.
    Advanced: Third Person Egg Shooting to Amaze-O-Gaze to Egg Aim to Breegull Blaster.
    Randomize Moves and Randomize BK Moves are required."""
    display_name = "Progressive Egg Aim"
    option_none = 0
    option_basic = 1
    option_advanced = 2

class ProgressiveFlight(Toggle):
    """Flight Pad to Beak Bomb to Airborne Egg Aim. Randomize Moves and Randomize BK Moves are required."""
    display_name = "Progressive Flight"

class ProgressiveBashAttack(Toggle):
    """Ground Rat-a-tat Rap to Breegull Bash. Randomize Stop N Swap and Randomize BK Moves are required"""
    display_name = "Progressive Bash Attack"

class EnableCheatoRewards(DefaultOnToggle):
    """Cheato rewards you with a cheat and an additional randomized reward.
    Cheato Pages are set to progression when this setting is enabled."""
    display_name = "Cheato Rewards"

class RandomizeJinjos(DefaultOnToggle):
    """Jinjos have fled to other worlds. Other players need to return them home."""
    display_name = "Randomize Jinjos"

class RandomizeDoubloons(Toggle):
    """Jolly Roger's Doubloons are randomized."""
    display_name = "Randomize Doubloons"

class RandomizeCheatoPages(DefaultOnToggle):
    """Cheato pages are randomized."""
    display_name = "Randomize Cheato Pages"

class RandomizeHoneycombs(DefaultOnToggle):
    """Honeycombs are randomized."""
    display_name = "Randomize Honeycombs"

class EnableHoneyBRewards(DefaultOnToggle):
    """Honey B gives you health and an additional randomized reward."""
    display_name = "Honey B Rewards"

class RandomizeGlowbos(DefaultOnToggle):
    """Glowbos are randomized."""
    display_name = "Randomize Glowbos"

class RandomizeTrebleClefs(DefaultOnToggle):
    """Treble Clefs are randomized."""
    display_name = "Randomize Treble Clefs"

class RandomizeTrainStationSwitches(Toggle):
    """Train Stations are randomized."""
    display_name = "Randomize Train Station Switches"

class RandomizeChuffyTrain(Toggle):
    """Chuffy is randomized.
    Once received, you can call Chuffy at any unlocked station without defeating Old King Coal."""
    display_name = "Chuffy as a Randomized AP Item"

class RandomizeNotes(Toggle):
    """Note Nests are randomized."""
    display_name = "Randomize Note Nests"

class BassClefNotes(Range):
    """Convert some 5 notes into Bass Clefs (10 notes). How many notes do you want converted?
       Be aware that 1 Bass Clef removes two 5 notes and adds an additional Big-O-Pants.
       Randomize Notes is required."""
    display_name = "Bass Clefs (10 notes) Amount"
    range_start = 0
    range_end = 30
    default = 0

class TrebleclefNotes(Range):
    """Convert some 5 notes into Treble Clefs (20 notes). How many notes do you want converted?
       Be aware that 1 Treble Clef removes four 5 notes and adds three additional Big-O-Pants.
       Randomize Notes is required."""
    display_name = "Add additional Treble Clefs (20 notes) Amount"
    range_start = 0
    range_end = 21
    default = 0

class Traps(Toggle):
    """Swaps out the Big-O-Pants with Traps!"""
    display_name = "Traps"

class RandomizeWorldDinoRoar(Toggle):
    """Baby T-Rex's Roar is lost across the MultiWorld. Other players need to help him learn to ROAR!"""
    display_name = "Baby T-Rex Roar"

class EnableNestsanity(Toggle):
    """Eggs and feather nests give checks when you collect them for the first time. They behave as regular egg nests after they have been collected."""
    display_name = "Nestsanity"

class TrapsToNestRatio(Range):
    """Select a percentage of feather and egg nests items to be replaced with trap items.
    Requires Traps and Nestsanity to have an effect."""
    display_name = "Traps to Nests Ratio"
    range_start = 0
    range_end = 100
    default = 0

class GoldenEggsWeight(Range):
    """The weight of Golden Eggs in the trap pool.
    Requires Traps and Nestsanity to have an effect"""
    display_name = "Golden Eggs Weight"
    range_start = 0
    range_end = 100
    default = 40

class TripTrapWeight(Range):
    """The weight of Trip Traps in the trap pool.
    Requires Traps to have an effect"""
    display_name = "Trip Trap Weight"
    range_start = 0
    range_end = 100
    default = 40

class SlipTrapWeight(Range):
    """The weight of Slip Traps in the trap pool.
    Requires Traps to have an effect"""
    display_name = "Slip Trap Weight"
    range_start = 0
    range_end = 100
    default = 40

class TransformTrapWeight(Range):
    """The weight of Transform Traps in the trap pool.
    Requires Traps to have an effect"""
    display_name = "Transform Trap Weight"
    range_start = 0
    range_end = 100
    default = 40

class SquishTrapWeight(Range):
    """The weight of Squish Traps in the trap pool.
    Requires Traps to have an effect"""
    display_name = "Squish Trap Weight"
    range_start = 0
    range_end = 100
    default = 20

class KingJingalingHasJiggy(DefaultOnToggle):
    """King Jingaling will always have a Jiggy for you."""
    display_name = "King Jingaling Jiggy"

class SkipPuzzles(DefaultOnToggle):
    """Open world entrances without having to go to Jiggywiggy."""
    display_name = "Skip Puzzles"

class Backdoors(Toggle):
    """Opens many one-way switches on game start, allowing for more backdoor access to levels.
    The following gates are preopened: MT -> TDL, MT -> HFP, GGM -> WW, WW -> TDL.
    For MT -> TDL, only the gate accessed from TDL's side is opened. For GGM -> WW, the boulders are still intact.
    The bridge from HFP's entrance is pre-moved to allow secondary access to Cliff Top.
    George is pre-dropped to make HFP -> JRL more accessible."""
    display_name = "Open Backdoors"

class OpenHag1(DefaultOnToggle):
    """HAG 1 boss fight is opened when Cauldron Keep is opened, requiring fewer Jiggies to win."""
    display_name = "HAG 1 Open"

class RandomizeWorlds(Toggle):
    """Worlds will open in a randomized order. Randomized Moves and Skip Puzzles required."""
    display_name = "Randomize Worlds"

class RandomizeWorldZones(Toggle):
    """World Entrances will warp you to a different world. This does not affect Chuffy."""
    display_name = "Randomize World Entrances"

class RandomizeStopnSwap(Toggle):
    """Mystery Eggs, their rewards, and the Ice Key are scattered across the MultiWorld."""
    display_name = "Randomize Stop n Swap"

class TowerOfTragedy(Choice):
    """Choose whether to play the full quiz, start at round 3, or skip it."""
    display_name = "Tower of Tragedy Quiz"
    option_full = 0
    option_skip = 1
    option_round_3 = 2
    default = 1

class LogicType(Choice):
    """Choose your logic difficulty and difficulty of tricks you are expected to perform to reach certain areas.
    Please be aware that if you plan on randomizing worlds with BK Moves in the pool, you cannot use "intended" logic."""
    display_name = "Logic Type"
    option_intended = 0
    option_easy_tricks = 1
    option_hard_tricks = 2
    option_glitches = 3
    default = 0

class OpenSilos(Choice):
    """Choose if you want IoH Silos to be closed, randomly open 1, or enable all. If you enabled Randomized Worlds with BK Moves randomized and
       silos set to none, it will be enforced to one."""
    display_name = "Open Silos"
    option_none = 0
    option_one = 1
    option_all = 2
    default = 0

class VictoryCondition(Choice):
    """Choose the victory condition.
    HAG1: Unlock the HAG1 fight and defeat Gruntilda.
    Minigame Hunt: Clear the 14 minigames and the final Canary Mary race in Cloud Cuckcoo Land to collect Mumbo Tokens.
    Boss Hunt: Defeat the 8 world bosses and collect their Mumbo Tokens.
    Jinjo Family Rescue: Rescue Jinjo Families to collect their prized Mumbo Tokens.
    Wonderwing Challenge: Collect all 32 Mumbo Tokens across all boss fights, mini games, and every Jinjo family
        to gain access to HAG1 and Defeat Grunty. The Ultimate Banjo Tooie experience!!
    Token Hunt: Mumbo's Tokens are scattered around the world. Help him find them!"""
    display_name = "Victory Condition"
    option_hag1 = 0
    option_minigame_hunt = 1
    option_boss_hunt = 2
    option_jinjo_family_rescue = 3
    option_wonderwing_challenge = 4
    option_token_hunt = 5
    default = 0

class MinigameHuntLength(Range):
    """How many Mumbo Tokens are needed to clear the Minigame Hunt.
    Choose a value between 1 and 15."""
    display_name = "Minigame Hunt Length"
    range_start = 1
    range_end = 15
    default = 14

class BossHuntLength(Range):
    """How many Mumbo Tokens are needed to clear the Boss Hunt.
    Choose a value between 1 and 8."""
    display_name = "Boss Hunt Length"
    range_start = 1
    range_end = 8
    default = 8

class JinjoFamilyRescueLength(Range):
    """How many Jinjo families' Mumbo Tokens are needed to clear the Jinjo family rescue.
    Choose a value between 1 and 9."""
    display_name = "Jinjo Family Rescue Length"
    range_start = 1
    range_end = 9
    default = 9

class TokenHuntLength(Range):
    """How many Mumbo Tokens of the 15 hidden throughout the world do you need to find.
    Choose a value between 1 and 15."""
    display_name = "Token Hunt Length"
    range_start = 1
    range_end = 15
    default = 5

class GameLength(Choice):
    """Choose how quickly the worlds open.
    quick: Worlds open at 1, 3, 6, 10, 15, 21, 28, 36, and 44 Jiggys
    normal: Worlds open at 1, 4, 8, 14, 20, 28, 36, 45, and 55 Jiggys
    long: Worlds open at 1, 8, 16, 25, 34, 43, 52, 61, and 70 Jiggys
    custom: You pick when worlds open
    """
    display_name = "World Requirements"
    option_quick = 0
    option_normal = 1
    option_long = 2
    option_custom = 3
    option_randomize = 4
    default = 1

class CustomWorlds(FreeText):
    """Enter a list of jiggy requirements you want for each world unlock. Max values of each world are: 1,20,30,40,50,60,70,80,90.
    This option only functions if the World Requirements option is set to custom."""
    display_name = "Custom World Cost List"
    default = "1,4,8,14,20,28,36,45,55"

class SpeedUpMinigames(DefaultOnToggle):
    """Start 3-round minigames at Round 3."""
    display_name = "Speed Up Minigames"

class SkipKlungo(Toggle):
    """Make it so you can skip Klungo 1 and 2."""
    display_name = "Skip Klungo"

@dataclass
class BanjoTooieOptions(PerGameCommonOptions):
    death_link: DeathLink

    logic_type: LogicType

    victory_condition: VictoryCondition
    minigame_hunt_length: MinigameHuntLength
    boss_hunt_length: BossHuntLength
    jinjo_family_rescue_length: JinjoFamilyRescueLength
    token_hunt_length: TokenHuntLength

    game_length: GameLength
    custom_worlds:CustomWorlds

    randomize_moves: RandomizeBTMoveList
    jamjars_silo_costs: JamjarsSiloCosts
    randomize_bk_moves: RandomizeBKMoveList
    egg_behaviour: EggsBehaviour

    progressive_beak_buster: ProgressiveBeakBuster
    progressive_shoes: ProgressiveShoes
    progressive_water_training: ProgressiveWaterTraining
    progressive_flight: ProgressiveFlight
    progressive_egg_aiming:ProgressiveEggAim
    progressive_bash_attack: ProgressiveBashAttack

    randomize_notes: RandomizeNotes
    randomize_treble: RandomizeTrebleClefs
    extra_trebleclefs_count: TrebleclefNotes
    bass_clef_amount: BassClefNotes

    randomize_jinjos: RandomizeJinjos
    randomize_doubloons: RandomizeDoubloons
    randomize_cheato: RandomizeCheatoPages
    cheato_rewards: EnableCheatoRewards
    randomize_honeycombs: RandomizeHoneycombs
    honeyb_rewards: EnableHoneyBRewards
    randomize_glowbos: RandomizeGlowbos
    randomize_stop_n_swap: RandomizeStopnSwap
    randomize_dino_roar: RandomizeWorldDinoRoar
    nestsanity: EnableNestsanity

    traps: Traps
    traps_nests_ratio: TrapsToNestRatio

    golden_eggs_weight: GoldenEggsWeight
    trip_trap_weight: TripTrapWeight
    slip_trap_weight: SlipTrapWeight
    transform_trap_weight: TransformTrapWeight
    squish_trap_weight: SquishTrapWeight

    randomize_stations: RandomizeTrainStationSwitches
    randomize_chuffy: RandomizeChuffyTrain
    jingaling_jiggy: KingJingalingHasJiggy
    skip_puzzles: SkipPuzzles
    randomize_worlds: RandomizeWorlds
    randomize_world_loading_zone: RandomizeWorldZones
    open_hag1: OpenHag1
    backdoors:Backdoors
    open_silos: OpenSilos

    speed_up_minigames: SpeedUpMinigames
    tower_of_tragedy: TowerOfTragedy
    skip_klungo: SkipKlungo
    dialog_character:DialogCharacters

    start_inventory_from_pool: StartInventoryPool


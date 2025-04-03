from dataclasses import dataclass

from Options import Choice, Range, Option, OptionGroup, Toggle, DeathLink, DefaultOnToggle, PerGameCommonOptions, PlandoBosses

from .Names import LocationName


class Goal(Choice):
    """
    Determines the goal of the seed

    Biolizard: Finish Cannon's Core and defeat the Biolizard and Finalhazard

    Chaos Emerald Hunt: Find the Seven Chaos Emeralds and reach Green Hill Zone

    Finalhazard Chaos Emerald Hunt: Find the Seven Chaos Emeralds and reach Green Hill Zone, then defeat Finalhazard

    Grand Prix: Win every race in Kart Race Mode (all standard levels are disabled)

    Boss Rush: Beat all of the bosses in the Boss Rush, ending with Finalhazard

    Cannon's Core Boss Rush: Beat Cannon's Core, then beat all of the bosses in the Boss Rush, ending with Finalhazard

    Boss Rush Chaos Emerald Hunt: Find the Seven Chaos Emeralds, then beat all of the bosses in the Boss Rush, ending with Finalhazard

    Chaos Chao: Raise a Chaos Chao to win

    Minigame Madness: Win a certain amount of each Minigame Trap, then defeat Finalhazard
    """
    display_name = "Goal"
    option_biolizard = 0
    option_chaos_emerald_hunt = 1
    option_finalhazard_chaos_emerald_hunt = 2
    option_grand_prix = 3
    option_boss_rush = 4
    option_cannons_core_boss_rush = 5
    option_boss_rush_chaos_emerald_hunt = 6
    option_chaos_chao = 7
    option_minigame_madness = 8
    default = 0

    @classmethod
    def get_option_name(cls, value) -> str:
        if cls.auto_display_name and value == 5:
            return "Cannon's Core Boss Rush"
        elif cls.auto_display_name:
            return cls.name_lookup[value].replace("_", " ").title()
        else:
            return cls.name_lookup[value]


class MissionShuffle(Toggle):
    """
    Determines whether missions order will be shuffled per level
    """
    display_name = "Mission Shuffle"


class BossRushShuffle(Choice):
    """
    Determines how bosses in Boss Rush Mode are shuffled

    Vanilla: Bosses appear in the Vanilla ordering

    Shuffled: The same bosses appear, but in a random order

    Chaos: Each boss is randomly chosen separately (one will always be King Boom Boo)

    Singularity: One boss is chosen and placed in every slot (one will always be replaced with King Boom Boo)
    """
    display_name = "Boss Rush Shuffle"
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2
    option_singularity = 3
    default = 0


class GateBossPlando(PlandoBosses):
    """
    Possible Locations:
    "Gate 1 Boss"
    "Gate 2 Boss"
    "Gate 3 Boss"
    "Gate 4 Boss"
    "Gate 5 Boss"

    Possible Bosses:
    "Sonic vs Shadow 1"
    "Sonic vs Shadow 2"
    "Tails vs Eggman 1"
    "Tails vs Eggman 2"
    "Knuckles vs Rouge 1"
    "BIG FOOT"
    "HOT SHOT"
    "FLYING DOG"
    "Egg Golem (Sonic)"
    "Egg Golem (Eggman)"
    "King Boom Boo"
    """
    bosses = frozenset(LocationName.boss_names.keys())

    locations = frozenset(LocationName.boss_gate_names.keys())

    duplicate_bosses = False

    @classmethod
    def can_place_boss(cls, boss: str, location: str) -> bool:
        return True

    display_name = "Boss Shuffle"
    option_plando = 0


class MinigameMadnessRequirement(Range):
    """
    Determines how many of each Minigame Trap must be won (for Minigame Madness goal)

    Receiving this many of a Minigame Trap will allow you to replay that minigame at-will in the Chao World lobby
    """
    display_name = "Minigame Madness Trap Requirement"
    range_start = 1
    range_end = 10
    default = 3


class MinigameMadnessMinimum(Range):
    """
    Determines the minimum number of each Minigame Trap that are created (for Minigame Madness goal)

    At least this many of each trap will be created as "Progression Traps", regardless of other trap option selections
    """
    display_name = "Minigame Madness Trap Minimum"
    range_start = 1
    range_end = 10
    default = 5


class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2


class OmochaoTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which spawns several Omochao around the player
    """
    display_name = "OmoTrap Weight"


class TimestopTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which briefly stops time
    """
    display_name = "Chaos Control Trap Weight"


class ConfusionTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which causes the controls to be skewed for a period of time
    """
    display_name = "Confusion Trap Weight"


class TinyTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which causes the player to become tiny
    """
    display_name = "Tiny Trap Weight"


class GravityTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which increases gravity
    """
    display_name = "Gravity Trap Weight"


class ExpositionTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which tells you the story
    """
    display_name = "Exposition Trap Weight"


class DarknessTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes the world dark
    """
    display_name = "Darkness Trap Weight"


class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes the world slippery
    """
    display_name = "Ice Trap Weight"


class SlowTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes you gotta go slow
    """
    display_name = "Slow Trap Weight"


class CutsceneTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes you watch an unskippable cutscene
    """
    display_name = "Cutscene Trap Weight"


class ReverseTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which reverses your controls
    """
    display_name = "Reverse Trap Weight"


class LiteratureTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to read
    """
    display_name = "Literature Trap Weight"


class ControllerDriftTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which causes your control sticks to drift
    """
    display_name = "Controller Drift Trap Weight"


class PoisonTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which causes you to lose rings over time
    """
    display_name = "Poison Trap Weight"


class BeeTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which spawns a swarm of bees
    """
    display_name = "Bee Trap Weight"


class PongTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Pong minigame
    """
    display_name = "Pong Trap Weight"


class BreakoutTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Breakout minigame
    """
    display_name = "Breakout Trap Weight"


class FishingTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Fishing minigame
    """
    display_name = "Fishing Trap Weight"


class TriviaTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Trivia minigame
    """
    display_name = "Trivia Trap Weight"


class PokemonTriviaTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Pokemon Trivia minigame
    """
    display_name = "Pokemon Trivia Trap Weight"


class PokemonCountTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Pokemon Count minigame
    """
    display_name = "Pokemon Count Trap Weight"


class NumberSequenceTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Number Sequence minigame
    """
    display_name = "Number Sequence Trap Weight"


class LightUpPathTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Light Up Path minigame
    """
    display_name = "Light Up Path Trap Weight"


class PinballTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Pinball minigame
    """
    display_name = "Pinball Trap Weight"


class MathQuizTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to solve a math problem
    """
    display_name = "Math Quiz Trap Weight"


class SnakeTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Snake minigame
    """
    display_name = "Snake Trap Weight"


class InputSequenceTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to press a sequence of inputs
    """
    display_name = "Input Sequence Trap Weight"


class MinigameTrapDifficulty(Choice):
    """
    How difficult any Minigame-style traps are
    Chaos causes the difficulty to be random per-minigame
    """
    display_name = "Minigame Trap Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_chaos = 3
    default = 1


class BigFishingDifficulty(Choice):
    """
    How difficult Big's Fishing Minigames are
    Chaos causes the difficulty to be random per-minigame
    """
    display_name = "Big Fishing Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_chaos = 3
    default = 1


class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required emblems in the item pool with random junk items
    """
    display_name = "Junk Fill Percentage"
    range_start = 0
    range_end = 100
    default = 50


class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class Keysanity(DefaultOnToggle):
    """
    Determines whether picking up Chao Keys grants checks
    (86 Locations)
    """
    display_name = "Keysanity"


class Whistlesanity(Choice):
    """
    Determines whether whistling at various spots grants checks

    None: No Whistle Spots grant checks

    Pipes: Whistling at Pipes grants checks (97 Locations)

    Hidden: Whistling at Hidden Whistle Spots grants checks (32 Locations)

    Both: Whistling at both Pipes and Hidden Whistle Spots grants checks (129 Locations)
    """
    display_name = "Whistlesanity"
    option_none = 0
    option_pipes = 1
    option_hidden = 2
    option_both = 3
    default = 0


class Beetlesanity(DefaultOnToggle):
    """
    Determines whether destroying Gold Beetles grants checks
    (27 Locations)
    """
    display_name = "Beetlesanity"


class Omosanity(Toggle):
    """
    Determines whether activating Omochao grants checks
    (192 Locations)
    """
    display_name = "Omosanity"


class Animalsanity(Toggle):
    """
    Determines whether unique counts of animals grant checks.
    (422 Locations)

    ALL animals must be collected in a single run of a mission to get all checks.
    """
    display_name = "Animalsanity"


class ItemBoxsanity(Choice):
    """
    Determines whether collecting Item Boxes grants checks
    None: No Item Boxes grant checks
    Extra Lives: Extra Life Boxes grant checks (94 Locations)
    All: All Item Boxes grant checks (502 Locations Total)
    """
    display_name = "Itemboxsanity"
    option_none = 0
    option_extra_lives = 1
    option_all = 2
    default = 0


class Bigsanity(Toggle):
    """
    Determines whether helping Big fish grants checks.
    (32 Locations)
    """
    display_name = "Bigsanity"


class KartRaceChecks(Choice):
    """
    Determines whether Kart Race Mode grants checks

    None: No Kart Races grant checks

    Mini: Each Kart Race difficulty must be beaten only once

    Full: Every Character must separately beat each Kart Race difficulty
    """
    display_name = "Kart Race Checks"
    option_none = 0
    option_mini = 1
    option_full = 2
    default = 0


class EmblemPercentageForCannonsCore(Range):
    """
    Allows logic to gate the final mission behind a number of Emblems
    """
    display_name = "Emblem Percentage for Cannon's Core"
    range_start = 0
    range_end = 75
    default = 50


class NumberOfLevelGates(Range):
    """
    The number emblem-locked gates which lock sets of levels
    """
    display_name = "Number of Level Gates"
    range_start = 0
    range_end = 5
    default = 3


class LevelGateDistribution(Choice):
    """
    Determines how levels are distributed between level gate regions

    Early: Earlier regions will have more levels than later regions

    Even: Levels will be evenly distributed between all regions

    Late: Later regions will have more levels than earlier regions
    """
    display_name = "Level Gate Distribution"
    option_early = 0
    option_even = 1
    option_late = 2
    default = 1


class LevelGateCosts(Choice):
    """
    Determines how many emblems are required to unlock level gates
    """
    display_name = "Level Gate Costs"
    option_low = 0
    option_medium = 1
    option_high = 2
    default = 0


class MaximumEmblemCap(Range):
    """
    Determines the maximum number of emblems that can be in the item pool.

    If fewer available locations exist in the pool than this number, the number of available locations will be used instead.

    Gate and Cannon's Core costs will be calculated based off of that number.
    """
    display_name = "Max Emblem Cap"
    range_start = 50
    range_end = 1000
    default = 180


class RequiredRank(Choice):
    """
    Determines what minimum Rank is required to send a check for a mission
    """
    display_name = "Required Rank"
    option_e = 0
    option_d = 1
    option_c = 2
    option_b = 3
    option_a = 4
    default = 0


class ChaoRaceDifficulty(Choice):
    """
    Determines the number of Chao Race difficulty levels included. Easier difficulty settings means fewer Chao Race checks

    None: No Chao Races have checks

    Beginner: Beginner Races

    Intermediate: Beginner, Challenge, Hero, and Dark Races

    Expert: Beginner, Challenge, Hero, Dark and Jewel Races
    """
    display_name = "Chao Race Difficulty"
    option_none = 0
    option_beginner = 1
    option_intermediate = 2
    option_expert = 3
    default = 0


class ChaoKarateDifficulty(Choice):
    """
    Determines the number of Chao Karate difficulty levels included. (Note: This setting requires purchase of the "Battle" DLC)
    """
    display_name = "Chao Karate Difficulty"
    option_none = 0
    option_beginner = 1
    option_standard = 2
    option_expert = 3
    option_super = 4
    default = 0


class ChaoStadiumChecks(Choice):
    """
    Determines which Chao Stadium activities grant checks

    All: Each individual race and karate fight grants a check

    Prize: Only the races which grant Chao Toys grant checks (final race of each Beginner and Jewel cup, 4th, 8th, and 12th Challenge Races, 2nd and 4th Hero and Dark Races, final fight of each Karate difficulty)
    """
    display_name = "Chao Stadium Checks"
    option_all = 0
    option_prize = 1
    default = 0


class ChaoStats(Range):
    """
    Determines the highest level in each Chao Stat that grants checks
    (Swim, Fly, Run, Power)
    """
    display_name = "Chao Stats"
    range_start = 0
    range_end = 99
    default = 0


class ChaoStatsFrequency(Range):
    """
    Determines how many levels in each Chao Stat grant checks (up to the maximum set in the `chao_stats` option)

    `1` means every level is included, `2` means every other level is included, `3` means every third, and so on
    """
    display_name = "Chao Stats Frequency"
    range_start = 1
    range_end = 20
    default = 5


class ChaoStatsStamina(Toggle):
    """
    Determines whether Stamina is included in the `chao_stats` option
    """
    display_name = "Chao Stats - Stamina"


class ChaoStatsHidden(Toggle):
    """
    Determines whether the hidden stats (Luck and Intelligence) are included in the `chao_stats` option
    """
    display_name = "Chao Stats - Luck and Intelligence"


class ChaoAnimalParts(Toggle):
    """
    Determines whether giving Chao various animal parts grants checks
    (73 Locations)
    """
    display_name = "Chao Animal Parts"


class ChaoKindergarten(Choice):
    """
    Determines whether learning the lessons from the Kindergarten Classroom grants checks
    (WARNING: VERY SLOW)

    None: No Kindergarten classes have checks

    Basics: One class from each category (Drawing, Dance, Song, and Instrument) is a check (4 Locations)

    Full: Every class is a check (23 Locations)
    """
    display_name = "Chao Kindergarten Checks"
    option_none = 0
    option_basics = 1
    option_full = 2
    default = 0


class BlackMarketSlots(Range):
    """
    Determines how many multiworld items are available to purchase from the Black Market
    """
    display_name = "Black Market Slots"
    range_start = 0
    range_end = 64
    default = 0


class BlackMarketUnlockCosts(Choice):
    """
    Determines how many Chao Coins are required to unlock sets of Black Market items
    """
    display_name = "Black Market Unlock Costs"
    option_low = 0
    option_medium = 1
    option_high = 2
    default = 1


class BlackMarketPriceMultiplier(Range):
    """
    Determines how many rings the Black Market items cost

    The base ring costs of items in the Black Market range from 50-100, and are then multiplied by this value
    """
    display_name = "Black Market Price Multiplier"
    range_start = 0
    range_end = 40
    default = 1


class ShuffleStartingChaoEggs(DefaultOnToggle):
    """
    Determines whether the starting Chao eggs in the gardens are random
    """
    display_name = "Shuffle Starting Chao Eggs"


class ChaoEntranceRandomization(Toggle):
    """
    Determines whether entrances in Chao World are randomized
    """
    display_name = "Chao Entrance Randomization"


class RequiredCannonsCoreMissions(Choice):
    """
    Determines how many Cannon's Core missions must be completed (for Biolizard or Cannon's Core goals)

    First: Only the first mission must be completed

    All Active: All active Cannon's Core missions must be completed
    """
    display_name = "Required Cannon's Core Missions"
    option_first = 0
    option_all_active = 1
    default = 0


class BaseMissionCount(Range):
    """
    Base class for mission count options
    """
    range_start = 1
    range_end = 5
    default = 2


class SonicMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Sonic stages
    """
    display_name = "Sonic Mission Count"


class SonicMission2(DefaultOnToggle):
    """
    Determines if the Sonic 100 rings missions should be included
    """
    display_name = "Sonic Mission 2"


class SonicMission3(DefaultOnToggle):
    """
    Determines if the Sonic lost chao missions should be included
    """
    display_name = "Sonic Mission 3"


class SonicMission4(DefaultOnToggle):
    """
    Determines if the Sonic time trial missions should be included
    """
    display_name = "Sonic Mission 4"


class SonicMission5(DefaultOnToggle):
    """
    Determines if the Sonic hard missions should be included
    """
    display_name = "Sonic Mission 5"


class ShadowMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Shadow stages
    """
    display_name = "Shadow Mission Count"


class ShadowMission2(DefaultOnToggle):
    """
    Determines if the Shadow 100 rings missions should be included
    """
    display_name = "Shadow Mission 2"


class ShadowMission3(DefaultOnToggle):
    """
    Determines if the Shadow lost chao missions should be included
    """
    display_name = "Shadow Mission 3"


class ShadowMission4(DefaultOnToggle):
    """
    Determines if the Shadow time trial missions should be included
    """
    display_name = "Shadow Mission 4"


class ShadowMission5(DefaultOnToggle):
    """
    Determines if the Shadow hard missions should be included
    """
    display_name = "Shadow Mission 5"


class TailsMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Tails stages
    """
    display_name = "Tails Mission Count"


class TailsMission2(DefaultOnToggle):
    """
    Determines if the Tails 100 rings missions should be included
    """
    display_name = "Tails Mission 2"


class TailsMission3(DefaultOnToggle):
    """
    Determines if the Tails lost chao missions should be included
    """
    display_name = "Tails Mission 3"


class TailsMission4(DefaultOnToggle):
    """
    Determines if the Tails time trial missions should be included
    """
    display_name = "Tails Mission 4"


class TailsMission5(DefaultOnToggle):
    """
    Determines if the Tails hard missions should be included
    """
    display_name = "Tails Mission 5"


class EggmanMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Eggman stages
    """
    display_name = "Eggman Mission Count"


class EggmanMission2(DefaultOnToggle):
    """
    Determines if the Eggman 100 rings missions should be included
    """
    display_name = "Eggman Mission 2"


class EggmanMission3(DefaultOnToggle):
    """
    Determines if the Eggman lost chao missions should be included
    """
    display_name = "Eggman Mission 3"


class EggmanMission4(DefaultOnToggle):
    """
    Determines if the Eggman time trial missions should be included
    """
    display_name = "Eggman Mission 4"


class EggmanMission5(DefaultOnToggle):
    """
    Determines if the Eggman hard missions should be included
    """
    display_name = "Eggman Mission 5"


class KnucklesMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Knuckles stages
    """
    display_name = "Knuckles Mission Count"


class KnucklesMission2(DefaultOnToggle):
    """
    Determines if the Knuckles 100 rings missions should be included
    """
    display_name = "Knuckles Mission 2"


class KnucklesMission3(DefaultOnToggle):
    """
    Determines if the Knuckles lost chao missions should be included
    """
    display_name = "Knuckles Mission 3"


class KnucklesMission4(DefaultOnToggle):
    """
    Determines if the Knuckles time trial missions should be included
    """
    display_name = "Knuckles Mission 4"


class KnucklesMission5(DefaultOnToggle):
    """
    Determines if the Knuckles hard missions should be included
    """
    display_name = "Knuckles Mission 5"


class RougeMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Rouge stages
    """
    display_name = "Rouge Mission Count"


class RougeMission2(DefaultOnToggle):
    """
    Determines if the Rouge 100 rings missions should be included
    """
    display_name = "Rouge Mission 2"


class RougeMission3(DefaultOnToggle):
    """
    Determines if the Rouge lost chao missions should be included
    """
    display_name = "Rouge Mission 3"


class RougeMission4(DefaultOnToggle):
    """
    Determines if the Rouge time trial missions should be included
    """
    display_name = "Rouge Mission 4"


class RougeMission5(DefaultOnToggle):
    """
    Determines if the Rouge hard missions should be included
    """
    display_name = "Rouge Mission 5"


class KartMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Route 101 and 280
    """
    display_name = "Kart Mission Count"


class KartMission2(DefaultOnToggle):
    """
    Determines if the Route 101 and 280 100 rings missions should be included
    """
    display_name = "Kart Mission 2"


class KartMission3(DefaultOnToggle):
    """
    Determines if the Route 101 and 280 avoid cars missions should be included
    """
    display_name = "Kart Mission 3"


class KartMission4(DefaultOnToggle):
    """
    Determines if the Route 101 and 280 avoid walls missions should be included
    """
    display_name = "Kart Mission 4"


class KartMission5(DefaultOnToggle):
    """
    Determines if the Route 101 and 280 hard missions should be included
    """
    display_name = "Kart Mission 5"


class CannonsCoreMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Cannon's Core
    """
    display_name = "Cannon's Core Mission Count"


class CannonsCoreMission2(DefaultOnToggle):
    """
    Determines if the Cannon's Core 100 rings mission should be included
    """
    display_name = "Cannon's Core Mission 2"


class CannonsCoreMission3(DefaultOnToggle):
    """
    Determines if the Cannon's Core lost chao mission should be included
    """
    display_name = "Cannon's Core Mission 3"


class CannonsCoreMission4(DefaultOnToggle):
    """
    Determines if the Cannon's Core time trial mission should be included
    """
    display_name = "Cannon's Core Mission 4"


class CannonsCoreMission5(DefaultOnToggle):
    """
    Determines if the Cannon's Core hard mission should be included
    """
    display_name = "Cannon's Core Mission 5"


class RingLoss(Choice):
    """
    How taking damage is handled

    Classic: You lose all of your rings when hit

    Modern: You lose 20 rings when hit

    OHKO: You die immediately when hit (NOTE: Some Hard or Expert Logic tricks may require damage boosts!)
    """
    display_name = "Ring Loss"
    option_classic = 0
    option_modern = 1
    option_ohko = 2
    default = 0

    @classmethod
    def get_option_name(cls, value) -> str:
        if cls.auto_display_name and value == 2:
            return cls.name_lookup[value].upper()
        else:
            return cls.name_lookup[value]


class RingLink(Toggle):
    """
    Whether your in-level ring gain/loss is linked to other players
    """
    display_name = "Ring Link"


class TrapLink(Toggle):
    """
    Whether your received traps are linked to other players

    You will also receive any linked traps from other players with Trap Link enabled,
    if you have a weight above "none" set for that trap
    """
    display_name = "Trap Link"


class SADXMusic(Choice):
    """
    Whether the randomizer will include Sonic Adventure DX Music in the music pool

    SA2B: Only SA2B music will be played

    SADX: Only SADX music will be played

    Both: Both SA2B and SADX music will be played

    NOTE: This option requires the player to own a PC copy of SADX and to follow the addition steps in the setup guide.
    """
    display_name = "SADX Music"
    option_sa2b = 0
    option_sadx = 1
    option_both = 2
    default = 0

    @classmethod
    def get_option_name(cls, value) -> str:
        if cls.auto_display_name and value != 2:
            return cls.name_lookup[value].upper()
        else:
            return cls.name_lookup[value]


class MusicShuffle(Choice):
    """
    What type of Music Shuffle is used

    None: No music is shuffled.

    Levels: Level music is shuffled.

    Full: Level, Menu, and Additional music is shuffled.

    Singularity: Level, Menu, and Additional music is all replaced with a single random song.
    """
    display_name = "Music Shuffle Type"
    option_none = 0
    option_levels = 1
    option_full = 2
    option_singularity = 3
    default = 0


class VoiceShuffle(Choice):
    """
    What type of Voice Shuffle is used

    None: No voices are shuffled.

    Shuffled: Voices are shuffled.

    Rude: Voices are shuffled, but some are replaced with rude words.

    Chao: All voices are replaced with chao sounds.

    Singularity: All voices are replaced with a single random voice.
    """
    display_name = "Voice Shuffle Type"
    option_none = 0
    option_shuffled = 1
    option_rude = 2
    option_chao = 3
    option_singularity = 4
    default = 0


class Narrator(Choice):
    """
    Which menu narrator is used
    """
    display_name = "Narrator"
    option_default = 0
    option_shadow = 1
    option_rouge = 2
    option_eggman = 3
    option_maria = 4
    option_secretary = 5
    option_omochao = 6
    option_amy = 7
    option_tails = 8
    option_knuckles = 9
    option_sonic = 10
    default = 0


class LogicDifficulty(Choice):
    """
    What set of Upgrade Requirement logic to use

    Standard: The logic assumes the "intended" usage of Upgrades to progress through levels

    Hard: Some simple skips or sequence breaks may be required, but no out-of-bounds

    Expert: If it is humanly possible, it may be required
    """
    display_name = "Logic Difficulty"
    option_standard = 0
    option_hard = 1
    option_expert = 2
    default = 0


sa2b_option_groups = [
    OptionGroup("General Options", [
        Goal,
        BossRushShuffle,
        MinigameMadnessRequirement,
        MinigameMadnessMinimum,
        LogicDifficulty,
        RequiredRank,
        MaximumEmblemCap,
        RingLoss,
    ]),
    OptionGroup("Stages", [
        MissionShuffle,
        EmblemPercentageForCannonsCore,
        RequiredCannonsCoreMissions,
        NumberOfLevelGates,
        LevelGateCosts,
        LevelGateDistribution,
    ]),
    OptionGroup("Sanity Options", [
        Keysanity,
        Whistlesanity,
        Beetlesanity,
        Omosanity,
        Animalsanity,
        ItemBoxsanity,
        Bigsanity,
        KartRaceChecks,
    ]),
    OptionGroup("Chao", [
        BlackMarketSlots,
        BlackMarketUnlockCosts,
        BlackMarketPriceMultiplier,
        ChaoRaceDifficulty,
        ChaoKarateDifficulty,
        ChaoStadiumChecks,
        ChaoAnimalParts,
        ChaoStats,
        ChaoStatsFrequency,
        ChaoStatsStamina,
        ChaoStatsHidden,
        ChaoKindergarten,
        ShuffleStartingChaoEggs,
        ChaoEntranceRandomization,
    ]),
    OptionGroup("Junk and Traps", [
        JunkFillPercentage,
        TrapFillPercentage,
        OmochaoTrapWeight,
        TimestopTrapWeight,
        ConfusionTrapWeight,
        TinyTrapWeight,
        GravityTrapWeight,
        ExpositionTrapWeight,
        IceTrapWeight,
        SlowTrapWeight,
        CutsceneTrapWeight,
        ReverseTrapWeight,
        LiteratureTrapWeight,
        ControllerDriftTrapWeight,
        PoisonTrapWeight,
        BeeTrapWeight,
    ]),
    OptionGroup("Minigames", [
        PongTrapWeight,
        BreakoutTrapWeight,
        FishingTrapWeight,
        TriviaTrapWeight,
        PokemonTriviaTrapWeight,
        PokemonCountTrapWeight,
        NumberSequenceTrapWeight,
        LightUpPathTrapWeight,
        PinballTrapWeight,
        MathQuizTrapWeight,
        SnakeTrapWeight,
        InputSequenceTrapWeight,
        MinigameTrapDifficulty,
        BigFishingDifficulty,
    ]),
    OptionGroup("Sonic Missions", [
        SonicMissionCount,
        SonicMission2,
        SonicMission3,
        SonicMission4,
        SonicMission5,
    ]),
    OptionGroup("Shadow Missions", [
        ShadowMissionCount,
        ShadowMission2,
        ShadowMission3,
        ShadowMission4,
        ShadowMission5,
    ]),
    OptionGroup("Tails Missions", [
        TailsMissionCount,
        TailsMission2,
        TailsMission3,
        TailsMission4,
        TailsMission5,
    ]),
    OptionGroup("Eggman Missions", [
        EggmanMissionCount,
        EggmanMission2,
        EggmanMission3,
        EggmanMission4,
        EggmanMission5,
    ]),
    OptionGroup("Knuckles Missions", [
        KnucklesMissionCount,
        KnucklesMission2,
        KnucklesMission3,
        KnucklesMission4,
        KnucklesMission5,
    ]),
    OptionGroup("Rouge Missions", [
        RougeMissionCount,
        RougeMission2,
        RougeMission3,
        RougeMission4,
        RougeMission5,
    ]),
    OptionGroup("Kart Missions", [
        KartMissionCount,
        KartMission2,
        KartMission3,
        KartMission4,
        KartMission5,
    ]),
    OptionGroup("Cannon's Core Missions", [
        CannonsCoreMissionCount,
        CannonsCoreMission2,
        CannonsCoreMission3,
        CannonsCoreMission4,
        CannonsCoreMission5,
    ]),
    OptionGroup("Aesthetics", [
        SADXMusic,
        MusicShuffle,
        VoiceShuffle,
        Narrator,
    ]),
]

@dataclass
class SA2BOptions(PerGameCommonOptions):
    goal: Goal
    boss_rush_shuffle: BossRushShuffle
    minigame_madness_requirement: MinigameMadnessRequirement
    minigame_madness_minimum: MinigameMadnessMinimum
    gate_boss_plando: GateBossPlando
    logic_difficulty: LogicDifficulty
    required_rank: RequiredRank
    max_emblem_cap: MaximumEmblemCap
    ring_loss: RingLoss

    mission_shuffle: MissionShuffle
    required_cannons_core_missions: RequiredCannonsCoreMissions
    emblem_percentage_for_cannons_core: EmblemPercentageForCannonsCore
    number_of_level_gates: NumberOfLevelGates
    level_gate_distribution: LevelGateDistribution
    level_gate_costs: LevelGateCosts

    keysanity: Keysanity
    whistlesanity: Whistlesanity
    beetlesanity: Beetlesanity
    omosanity: Omosanity
    animalsanity: Animalsanity
    itemboxsanity: ItemBoxsanity
    bigsanity: Bigsanity
    kart_race_checks: KartRaceChecks

    black_market_slots: BlackMarketSlots
    black_market_unlock_costs: BlackMarketUnlockCosts
    black_market_price_multiplier: BlackMarketPriceMultiplier
    chao_race_difficulty: ChaoRaceDifficulty
    chao_karate_difficulty: ChaoKarateDifficulty
    chao_stadium_checks: ChaoStadiumChecks
    chao_animal_parts: ChaoAnimalParts
    chao_stats: ChaoStats
    chao_stats_frequency: ChaoStatsFrequency
    chao_stats_stamina: ChaoStatsStamina
    chao_stats_hidden: ChaoStatsHidden
    chao_kindergarten: ChaoKindergarten
    shuffle_starting_chao_eggs: ShuffleStartingChaoEggs
    chao_entrance_randomization: ChaoEntranceRandomization

    junk_fill_percentage: JunkFillPercentage
    trap_fill_percentage: TrapFillPercentage
    omochao_trap_weight: OmochaoTrapWeight
    timestop_trap_weight: TimestopTrapWeight
    confusion_trap_weight: ConfusionTrapWeight
    tiny_trap_weight: TinyTrapWeight
    gravity_trap_weight: GravityTrapWeight
    exposition_trap_weight: ExpositionTrapWeight
    #darkness_trap_weight: DarknessTrapWeight
    ice_trap_weight: IceTrapWeight
    slow_trap_weight: SlowTrapWeight
    cutscene_trap_weight: CutsceneTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    literature_trap_weight: LiteratureTrapWeight
    controller_drift_trap_weight: ControllerDriftTrapWeight
    poison_trap_weight: PoisonTrapWeight
    bee_trap_weight: BeeTrapWeight
    pong_trap_weight: PongTrapWeight
    breakout_trap_weight: BreakoutTrapWeight
    fishing_trap_weight: FishingTrapWeight
    trivia_trap_weight: TriviaTrapWeight
    pokemon_trivia_trap_weight: PokemonTriviaTrapWeight
    pokemon_count_trap_weight: PokemonCountTrapWeight
    number_sequence_trap_weight: NumberSequenceTrapWeight
    light_up_path_trap_weight: LightUpPathTrapWeight
    pinball_trap_weight: PinballTrapWeight
    math_quiz_trap_weight: MathQuizTrapWeight
    snake_trap_weight: SnakeTrapWeight
    input_sequence_trap_weight: InputSequenceTrapWeight
    minigame_trap_difficulty: MinigameTrapDifficulty
    big_fishing_difficulty: BigFishingDifficulty

    sadx_music: SADXMusic
    music_shuffle: MusicShuffle
    voice_shuffle: VoiceShuffle
    narrator: Narrator

    sonic_mission_count: SonicMissionCount
    sonic_mission_2: SonicMission2
    sonic_mission_3: SonicMission3
    sonic_mission_4: SonicMission4
    sonic_mission_5: SonicMission5

    shadow_mission_count: ShadowMissionCount
    shadow_mission_2: ShadowMission2
    shadow_mission_3: ShadowMission3
    shadow_mission_4: ShadowMission4
    shadow_mission_5: ShadowMission5

    tails_mission_count: TailsMissionCount
    tails_mission_2: TailsMission2
    tails_mission_3: TailsMission3
    tails_mission_4: TailsMission4
    tails_mission_5: TailsMission5

    eggman_mission_count: EggmanMissionCount
    eggman_mission_2: EggmanMission2
    eggman_mission_3: EggmanMission3
    eggman_mission_4: EggmanMission4
    eggman_mission_5: EggmanMission5

    knuckles_mission_count: KnucklesMissionCount
    knuckles_mission_2: KnucklesMission2
    knuckles_mission_3: KnucklesMission3
    knuckles_mission_4: KnucklesMission4
    knuckles_mission_5: KnucklesMission5

    rouge_mission_count: RougeMissionCount
    rouge_mission_2: RougeMission2
    rouge_mission_3: RougeMission3
    rouge_mission_4: RougeMission4
    rouge_mission_5: RougeMission5

    kart_mission_count: KartMissionCount
    kart_mission_2: KartMission2
    kart_mission_3: KartMission3
    kart_mission_4: KartMission4
    kart_mission_5: KartMission5

    cannons_core_mission_count: CannonsCoreMissionCount
    cannons_core_mission_2: CannonsCoreMission2
    cannons_core_mission_3: CannonsCoreMission3
    cannons_core_mission_4: CannonsCoreMission4
    cannons_core_mission_5: CannonsCoreMission5

    ring_link: RingLink
    trap_link: TrapLink
    death_link: DeathLink

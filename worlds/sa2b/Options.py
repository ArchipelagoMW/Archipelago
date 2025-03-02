from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions


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


class PongTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which forces you to play a Pong minigame
    """
    display_name = "Pong Trap Weight"


class MinigameTrapDifficulty(Choice):
    """
    How difficult any Minigame-style traps are
    """
    display_name = "Minigame Trap Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
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


class Keysanity(Toggle):
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


class Beetlesanity(Toggle):
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
    (421 Locations)

    ALL animals must be collected in a single run of a mission to get all checks.
    """
    display_name = "Animalsanity"


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
    default = 2


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


class SpeedMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Sonic and Shadow stages
    """
    display_name = "Speed Mission Count"


class SpeedMission2(DefaultOnToggle):
    """
    Determines if the Sonic and Shadow 100 rings missions should be included
    """
    display_name = "Speed Mission 2"


class SpeedMission3(DefaultOnToggle):
    """
    Determines if the Sonic and Shadow lost chao missions should be included
    """
    display_name = "Speed Mission 3"


class SpeedMission4(DefaultOnToggle):
    """
    Determines if the Sonic and Shadow time trial missions should be included
    """
    display_name = "Speed Mission 4"


class SpeedMission5(DefaultOnToggle):
    """
    Determines if the Sonic and Shadow hard missions should be included
    """
    display_name = "Speed Mission 5"


class MechMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Tails and Eggman stages
    """
    display_name = "Mech Mission Count"


class MechMission2(DefaultOnToggle):
    """
    Determines if the Tails and Eggman 100 rings missions should be included
    """
    display_name = "Mech Mission 2"


class MechMission3(DefaultOnToggle):
    """
    Determines if the Tails and Eggman lost chao missions should be included
    """
    display_name = "Mech Mission 3"


class MechMission4(DefaultOnToggle):
    """
    Determines if the Tails and Eggman time trial missions should be included
    """
    display_name = "Mech Mission 4"


class MechMission5(DefaultOnToggle):
    """
    Determines if the Tails and Eggman hard missions should be included
    """
    display_name = "Mech Mission 5"


class HuntMissionCount(BaseMissionCount):
    """
    The number of active missions to include for Knuckles and Rouge stages
    """
    display_name = "Hunt Mission Count"


class HuntMission2(DefaultOnToggle):
    """
    Determines if the Knuckles and Rouge 100 rings missions should be included
    """
    display_name = "Hunt Mission 2"


class HuntMission3(DefaultOnToggle):
    """
    Determines if the Knuckles and Rouge lost chao missions should be included
    """
    display_name = "Hunt Mission 3"


class HuntMission4(DefaultOnToggle):
    """
    Determines if the Knuckles and Rouge time trial missions should be included
    """
    display_name = "Hunt Mission 4"


class HuntMission5(DefaultOnToggle):
    """
    Determines if the Knuckles and Rouge hard missions should be included
    """
    display_name = "Hunt Mission 5"


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

    OHKO: You die immediately when hit (NOTE: Some Hard Logic tricks may require damage boosts!)
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

    Hard: Some simple skips or sequence breaks may be required
    """
    display_name = "Logic Difficulty"
    option_standard = 0
    option_hard = 1
    default = 0


sa2b_option_groups = [
    OptionGroup("General Options", [
        Goal,
        BossRushShuffle,
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
        PongTrapWeight,
        MinigameTrapDifficulty,
    ]),
    OptionGroup("Speed Missions", [
        SpeedMissionCount,
        SpeedMission2,
        SpeedMission3,
        SpeedMission4,
        SpeedMission5,
    ]),
    OptionGroup("Mech Missions", [
        MechMissionCount,
        MechMission2,
        MechMission3,
        MechMission4,
        MechMission5,
    ]),
    OptionGroup("Hunt Missions", [
        HuntMissionCount,
        HuntMission2,
        HuntMission3,
        HuntMission4,
        HuntMission5,
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
    pong_trap_weight: PongTrapWeight
    minigame_trap_difficulty: MinigameTrapDifficulty

    sadx_music: SADXMusic
    music_shuffle: MusicShuffle
    voice_shuffle: VoiceShuffle
    narrator: Narrator

    speed_mission_count: SpeedMissionCount
    speed_mission_2: SpeedMission2
    speed_mission_3: SpeedMission3
    speed_mission_4: SpeedMission4
    speed_mission_5: SpeedMission5

    mech_mission_count: MechMissionCount
    mech_mission_2: MechMission2
    mech_mission_3: MechMission3
    mech_mission_4: MechMission4
    mech_mission_5: MechMission5

    hunt_mission_count: HuntMissionCount
    hunt_mission_2: HuntMission2
    hunt_mission_3: HuntMission3
    hunt_mission_4: HuntMission4
    hunt_mission_5: HuntMission5

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
    death_link: DeathLink

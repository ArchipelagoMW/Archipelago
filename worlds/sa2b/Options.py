import typing

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionList


class Goal(Choice):
    """
    Determines the goal of the seed
    Biolizard: Finish Cannon's Core and defeat the Biolizard and Finalhazard
    Chaos Emerald Hunt: Find the Seven Chaos Emeralds and reach Green Hill Zone
    Finalhazard Chaos Emerald Hunt: Find the Seven Chaos Emeralds and reach Green Hill Zone, then defeat Finalhazard
    Grand Prix: Win every race in Kart Race Mode (all standard levels are disabled)
    """
    display_name = "Goal"
    option_biolizard = 0
    option_chaos_emerald_hunt = 1
    option_finalhazard_chaos_emerald_hunt = 2
    option_grand_prix = 3
    default = 0


class MissionShuffle(Toggle):
    """
    Determines whether missions order will be shuffled per level
    """
    display_name = "Mission Shuffle"


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
    Likelihood of a receiving a trap which spawns several Omochao around the player
    """
    display_name = "OmoTrap Weight"


class TimestopTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which briefly stops time
    """
    display_name = "Chaos Control Trap Weight"


class ConfusionTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the controls to be skewed for a period of time
    """
    display_name = "Confusion Trap Weight"


class TinyTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the player to become tiny
    """
    display_name = "Tiny Trap Weight"


class GravityTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which increases gravity
    """
    display_name = "Gravity Trap Weight"


class ExpositionTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which tells you the story
    """
    display_name = "Exposition Trap Weight"


class DarknessTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which makes the world dark
    """
    display_name = "Darkness Trap Weight"


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


class IncludeMissions(Range):
    """
    Allows logic to place items in a range of Missions for each level
    Each mission setting includes lower settings
    1: Base Story Missions
    2: 100 Ring Missions
    3: Lost Chao Missions
    4: Timer Missions
    5: Hard Mode Missions
    """
    display_name = "Include Missions"
    range_start = 1
    range_end = 5
    default = 2


class Keysanity(Toggle):
    """
    Determines whether picking up Chao Keys grants checks
    """
    display_name = "Keysanity"


class Whistlesanity(Choice):
    """
    Determines whether whistling at various spots grants checks
    None: No Whistle Spots grant checks
    Pipes: Whistling at Pipes grants checks
    Hidden: Whistling at Hidden Whistle Spots grants checks
    Both: Whistling at both Pipes and Hidden Whistle Spots grants checks
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
    """
    display_name = "Beetlesanity"


class Omosanity(Toggle):
    """
    Determines whether activating Omochao grants checks
    """
    display_name = "Omosanity"


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


class ChaoGardenDifficulty(Choice):
    """
    Determines the number of chao garden difficulty levels included. Easier difficulty settings means fewer chao garden checks
    None: No Chao Garden Activities have checks
    Beginner: Beginner Races
    Intermediate: Beginner and Jewel Races
    Expert: Beginner, Jewel, Challenge, Hero, and Dark Races
    """
    display_name = "Chao Garden Difficulty"
    option_none = 0
    option_beginner = 1
    option_intermediate = 2
    option_expert = 3
    default = 0


class IncludeChaoKarate(Toggle):
    """
    Determines whether the Chao Karate should be included as checks (Note: This setting requires purchase of the "Battle" DLC)
    """
    display_name = "Include Chao Karate"


class ChaoRaceChecks(Choice):
    """
    Determines which Chao Races grant checks
    All: Each individual race grants a check
    Prize: Only the races which grant Chao Toys grant checks (final race of each Beginner and Jewel cup, 4th, 8th, and
           12th Challenge Races, 2nd and 4th Hero and Dark Races)
    """
    display_name = "Chao Race Checks"
    option_all = 0
    option_prize = 1
    default = 0


class RequiredCannonsCoreMissions(Choice):
    """
    Determines how many Cannon's Core missions must be completed to unlock the Biolizard (for the "Biolizard" goal)
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
    Off: No music is shuffled.
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


sa2b_options: typing.Dict[str, type(Option)] = {
    "goal": Goal,
    "mission_shuffle": MissionShuffle,
    "keysanity": Keysanity,
    "whistlesanity": Whistlesanity,
    "beetlesanity": Beetlesanity,
    "omosanity": Omosanity,
    "kart_race_checks": KartRaceChecks,
    "required_rank": RequiredRank,
    "emblem_percentage_for_cannons_core": EmblemPercentageForCannonsCore,
    "required_cannons_core_missions": RequiredCannonsCoreMissions,
    "number_of_level_gates": NumberOfLevelGates,
    "level_gate_distribution": LevelGateDistribution,
    "level_gate_costs": LevelGateCosts,
    "chao_garden_difficulty": ChaoGardenDifficulty,
    "include_chao_karate": IncludeChaoKarate,
    "chao_race_checks": ChaoRaceChecks,
    "junk_fill_percentage": JunkFillPercentage,
    "trap_fill_percentage": TrapFillPercentage,
    "omochao_trap_weight": OmochaoTrapWeight,
    "timestop_trap_weight": TimestopTrapWeight,
    "confusion_trap_weight": ConfusionTrapWeight,
    "tiny_trap_weight": TinyTrapWeight,
    "gravity_trap_weight": GravityTrapWeight,
    "exposition_trap_weight": ExpositionTrapWeight,
    #"darkness_trap_weight": DarknessTrapWeight,
    "pong_trap_weight": PongTrapWeight,
    "minigame_trap_difficulty": MinigameTrapDifficulty,
    "ring_loss": RingLoss,
    "sadx_music": SADXMusic,
    "music_shuffle": MusicShuffle,
    "narrator": Narrator,
    "logic_difficulty": LogicDifficulty,
    "speed_mission_count": SpeedMissionCount,
    "speed_mission_2": SpeedMission2,
    "speed_mission_3": SpeedMission3,
    "speed_mission_4": SpeedMission4,
    "speed_mission_5": SpeedMission5,
    "mech_mission_count": MechMissionCount,
    "mech_mission_2": MechMission2,
    "mech_mission_3": MechMission3,
    "mech_mission_4": MechMission4,
    "mech_mission_5": MechMission5,
    "hunt_mission_count": HuntMissionCount,
    "hunt_mission_2": HuntMission2,
    "hunt_mission_3": HuntMission3,
    "hunt_mission_4": HuntMission4,
    "hunt_mission_5": HuntMission5,
    "kart_mission_count": KartMissionCount,
    "kart_mission_2": KartMission2,
    "kart_mission_3": KartMission3,
    "kart_mission_4": KartMission4,
    "kart_mission_5": KartMission5,
    "cannons_core_mission_count": CannonsCoreMissionCount,
    "cannons_core_mission_2": CannonsCoreMission2,
    "cannons_core_mission_3": CannonsCoreMission3,
    "cannons_core_mission_4": CannonsCoreMission4,
    "cannons_core_mission_5": CannonsCoreMission5,
    "death_link": DeathLink,
}

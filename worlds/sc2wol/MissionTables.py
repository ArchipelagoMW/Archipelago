from typing import NamedTuple, Dict, List, Set
from enum import IntEnum, Enum


class SC2Race(IntEnum):
    ANY = 0
    TERRAN = 1
    ZERG = 2
    PROTOSS = 3


class MissionPools(IntEnum):
    STARTER = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3
    VERY_HARD = 4
    FINAL = 5


class SC2CampaignGoalPriority(IntEnum):
    """
    Campaign's priority to goal election
    """
    NONE = 0
    MINI_CAMPAIGN = 1  # A goal shouldn't be in a mini-campaign if there's at least one 'big' campaign
    HARD = 2  # A campaign ending with a hard mission
    VERY_HARD = 3  # A campaign ending with a very hard mission
    EPILOGUE = 4  # Epilogue shall be always preferred as the goal if present


class SC2Campaign(Enum):

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, campaign_id: int, name: str, goal_priority: SC2CampaignGoalPriority,  race: SC2Race):
        self.id = campaign_id
        self.campaign_name = name
        self.goal_priority = goal_priority
        race: race

    GLOBAL = 0, "Global", SC2CampaignGoalPriority.NONE, SC2Race.ANY
    WOL = 1, "Wings of Liberty", SC2CampaignGoalPriority.VERY_HARD, SC2Race.TERRAN
    PROPHECY = 2, "Prophecy", SC2CampaignGoalPriority.MINI_CAMPAIGN, SC2Race.PROTOSS
    HOTS = 3, "Heart of the Swarm", SC2CampaignGoalPriority.HARD, SC2Race.ZERG


class SC2Mission(Enum):

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, mission_id: int, name: str, campaign: SC2Campaign, area: str, race: SC2Race, pool: MissionPools, map_file: str, build: bool = True):
        self.id = mission_id
        self.mission_name = name
        self.campaign = campaign
        self.area = area
        self.race = race
        self.pool = pool
        self.map_file = map_file
        self.build = build

    # Wings of Liberty
    LIBERATION_DAY = 1, "Liberation Day", SC2Campaign.WOL, "Mar Sara", SC2Race.TERRAN, MissionPools.STARTER, "ap_liberation_day", False
    THE_OUTLAWS = 2, "The Outlaws", SC2Campaign.WOL, "Mar Sara", SC2Race.TERRAN, MissionPools.EASY, "ap_the_outlaws"
    ZERO_HOUR = 3, "Zero Hour", SC2Campaign.WOL, "Mar Sara",  SC2Race.TERRAN, MissionPools.EASY, "ap_zero_hour"
    EVACUATION = 4, "Evacuation", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.EASY, "ap_evacuation"
    OUTBREAK = 5, "Outbreak", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.EASY, "ap_outbreak"
    SAFE_HAVEN = 6, "Safe Haven", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_safe_haven"
    HAVENS_FALL = 7, "Haven's Fall", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_havens_fall"
    SMASH_AND_GRAB = 8, "Smash and Grab", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.EASY, "ap_smash_and_grab"
    THE_DIG = 9, "The Dig", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_dig"
    THE_MOEBIUS_FACTOR = 10, "The Moebius Factor", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_moebius_factor"
    SUPERNOVA = 11, "Supernova", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.HARD, "ap_supernova"
    MAW_OF_THE_VOID = 12, "Maw of the Void", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.HARD, "ap_maw_of_the_void"
    DEVILS_PLAYGROUND = 13, "Devil's Playground", SC2Campaign.WOL, "Covert", SC2Race.TERRAN, MissionPools.EASY, "ap_devils_playground"
    WELCOME_TO_THE_JUNGLE = 14, "Welcome to the Jungle", SC2Campaign.WOL, "Covert", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_welcome_to_the_jungle"
    BREAKOUT = 15, "Breakout", SC2Campaign.WOL, "Covert", SC2Race.TERRAN, MissionPools.STARTER, "ap_breakout", False
    GHOST_OF_A_CHANCE = 16, "Ghost of a Chance", SC2Campaign.WOL, "Covert", SC2Race.TERRAN, MissionPools.STARTER, "ap_ghost_of_a_chance", False
    THE_GREAT_TRAIN_ROBBERY = 17, "The Great Train Robbery", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_great_train_robbery"
    CUTTHROAT = 18, "Cutthroat", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_cutthroat"
    ENGINE_OF_DESTRUCTION = 19, "Engine of Destruction", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.HARD, "ap_engine_of_destruction"
    MEDIA_BLITZ = 20, "Media Blitz", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_media_blitz"
    PIERCING_OF_THE_SHROUD = 21, "Piercing the Shroud", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.STARTER, "ap_piercing_the_shroud", False
    GATES_OF_HELL = 26, "Gates of Hell", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.HARD, "ap_gates_of_hell"
    BELLY_OF_THE_BEAST = 27, "Belly of the Beast", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.STARTER, "ap_belly_of_the_beast", False
    SHATTER_THE_SKY = 28, "Shatter the Sky", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.HARD, "ap_shatter_the_sky"
    ALL_IN = 29, "All-In", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_all_in"

    # Prophecy
    WHISPERS_OF_DOOM = 22, "Whispers of Doom", SC2Campaign.PROPHECY, "_1", SC2Race.PROTOSS, MissionPools.STARTER, "ap_whispers_of_doom", False
    A_SINISTER_TURN = 23, "A Sinister Turn", SC2Campaign.PROPHECY, "_2", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_a_sinister_turn"
    ECHOES_OF_THE_FUTURE = 24, "Echoes of the Future", SC2Campaign.PROPHECY, "_3", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_echoes_of_the_future"
    IN_UTTER_DARKNESS = 25, "In Utter Darkness", SC2Campaign.PROPHECY, "_4", SC2Race.PROTOSS, MissionPools.HARD, "ap_in_utter_darkness"

    # Heart of the Swarm
    LAB_RAT = 30, "Lab Rat", SC2Campaign.HOTS, "Umoja", SC2Race.ZERG, MissionPools.STARTER, "ap_lab_rat"
    BACK_IN_THE_SADDLE = 31, "Back in the Saddle", SC2Campaign.HOTS, "Umoja", SC2Race.ZERG, MissionPools.STARTER, "ap_back_in_the_saddle", False
    RENDEZVOUS = 32, "Rendezvous", SC2Campaign.HOTS, "Umoja", SC2Race.ZERG, MissionPools.EASY, "ap_rendezvous"
    HARVEST_OF_SCREAMS = 33, "Harvest of Screams", SC2Campaign.HOTS, "Kaldir", SC2Race.ZERG, MissionPools.EASY, "ap_harvest_of_screams"
    SHOOT_THE_MESSENGER = 34, "Shoot the Messenger", SC2Campaign.HOTS, "Kaldir", SC2Race.ZERG, MissionPools.EASY, "ap_shoot_the_messenger"
    ENEMY_WITHIN = 35, "Enemy Within", SC2Campaign.HOTS, "Kaldir", SC2Race.ZERG, MissionPools.STARTER, "ap_enemy_within", False
    DOMINATION = 36, "Domination", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.EASY, "ap_domination"
    FIRE_IN_THE_SKY = 37, "Fire in the Sky", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.MEDIUM, "ap_fire_in_the_sky"
    OLD_SOLDIERS = 38, "Old Soldiers", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.MEDIUM, "ap_old_soldiers"
    WAKING_THE_ANCIENT = 39, "Waking the Ancient", SC2Campaign.HOTS, "Zerus", SC2Race.ZERG, MissionPools.MEDIUM, "ap_waking_the_ancient"
    THE_CRUCIBLE = 40, "The Crucible", SC2Campaign.HOTS, "Zerus", SC2Race.ZERG, MissionPools.MEDIUM, "ap_the_crucible"
    SUPREME = 41, "Supreme", SC2Campaign.HOTS, "Zerus", SC2Race.ZERG, MissionPools.MEDIUM, "ap_supreme", False
    INFESTED = 42, "Infested", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.MEDIUM, "ap_infested"
    HAND_OF_DARKNESS = 43, "Hand of Darkness", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.HARD, "ap_hand_of_darkness"
    PHANTOMS_OF_THE_VOID = 44, "Phantoms of the Void", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.HARD, "ap_phantoms_of_the_void"
    WITH_FRIENDS_LIKE_THESE = 45, "With Friends Like These", SC2Campaign.HOTS, "Dominion Space", SC2Race.ZERG, MissionPools.STARTER, "ap_with_friends_like_these", False
    CONVICTION = 46, "Conviction", SC2Campaign.HOTS, "Dominion Space", SC2Race.ZERG, MissionPools.MEDIUM, "ap_conviction", False
    PLANETFALL = 47, "Planetfall", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.HARD, "ap_planetfall"
    DEATH_FROM_ABOVE = 48, "Death From Above", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.HARD, "ap_death_from_above"
    THE_RECKONING = 49, "The Reckoning", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.HARD, "ap_the_reckoning"

class MissionConnection:
    campaign: SC2Campaign
    connect_to: int  # -1 connects to Menu

    def __init__(self, connect_to, campaign = SC2Campaign.GLOBAL):
        self.campaign = campaign
        self.connect_to = connect_to

    def _asdict(self):
        return {
            "campaign": self.campaign.id,
            "connect_to": self.connect_to
        }

class MissionInfo(NamedTuple):
    mission: SC2Mission
    required_world: List[MissionConnection]
    category: str
    number: int = 0  # number of worlds need beaten
    completion_critical: bool = False  # missions needed to beat game
    or_requirements: bool = False  # true if the requirements should be or-ed instead of and-ed


class FillMission(NamedTuple):
    type: MissionPools
    connect_to: List[MissionConnection]
    category: str
    number: int = 0  # number of worlds need beaten
    completion_critical: bool = False  # missions needed to beat game
    or_requirements: bool = False  # true if the requirements should be or-ed instead of and-ed
    removal_priority: int = 0  # how many missions missing from the pool required to remove this mission


vanilla_shuffle_order: Dict[SC2Campaign, List[FillMission]] = {
    SC2Campaign.WOL: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.WOL)], "Mar Sara", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.WOL)], "Mar Sara", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(1, SC2Campaign.WOL)], "Mar Sara", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(2, SC2Campaign.WOL)], "Colonist"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.WOL)], "Colonist"),
        FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.WOL)], "Colonist", number=7),
        FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.WOL)], "Colonist", number=7, removal_priority=1),
        FillMission(MissionPools.EASY, [MissionConnection(2, SC2Campaign.WOL)], "Artifact", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(7, SC2Campaign.WOL)], "Artifact", number=8, completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(8, SC2Campaign.WOL)], "Artifact", number=11, completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(9, SC2Campaign.WOL)], "Artifact", number=14, completion_critical=True, removal_priority=7),
        FillMission(MissionPools.HARD, [MissionConnection(10, SC2Campaign.WOL)], "Artifact", completion_critical=True, removal_priority=6),
        FillMission(MissionPools.MEDIUM, [MissionConnection(2, SC2Campaign.WOL)], "Covert", number=4),
        FillMission(MissionPools.MEDIUM, [MissionConnection(12, SC2Campaign.WOL)], "Covert"),
        FillMission(MissionPools.HARD, [MissionConnection(13, SC2Campaign.WOL)], "Covert", number=8, removal_priority=3),
        FillMission(MissionPools.HARD, [MissionConnection(13, SC2Campaign.WOL)], "Covert", number=8, removal_priority=2),
        FillMission(MissionPools.MEDIUM, [MissionConnection(2, SC2Campaign.WOL)], "Rebellion", number=6),
        FillMission(MissionPools.HARD, [MissionConnection(16, SC2Campaign.WOL)], "Rebellion"),
        FillMission(MissionPools.HARD, [MissionConnection(17, SC2Campaign.WOL)], "Rebellion"),
        FillMission(MissionPools.HARD, [MissionConnection(18, SC2Campaign.WOL)], "Rebellion", removal_priority=8),
        FillMission(MissionPools.HARD, [MissionConnection(19, SC2Campaign.WOL)], "Rebellion", removal_priority=5),
        FillMission(MissionPools.HARD, [MissionConnection(11, SC2Campaign.WOL)], "Char", completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(21, SC2Campaign.WOL)], "Char", completion_critical=True, removal_priority=4),
        FillMission(MissionPools.HARD, [MissionConnection(21, SC2Campaign.WOL)], "Char", completion_critical=True),
        FillMission(MissionPools.FINAL, [MissionConnection(22, SC2Campaign.WOL), MissionConnection(23, SC2Campaign.WOL)], "Char", completion_critical=True, or_requirements=True)
    ],
    SC2Campaign.PROPHECY: [
        FillMission(MissionPools.MEDIUM, [MissionConnection(8, SC2Campaign.WOL)], "_1"),
        FillMission(MissionPools.HARD, [MissionConnection(0, SC2Campaign.PROPHECY)], "_2", removal_priority=2),
        FillMission(MissionPools.HARD, [MissionConnection(1, SC2Campaign.PROPHECY)], "_3", removal_priority=1),
        FillMission(MissionPools.FINAL, [MissionConnection(2, SC2Campaign.PROPHECY)], "_4"),
    ],
    SC2Campaign.HOTS: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.HOTS)], "Umoja", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.HOTS)], "Umoja", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(1, SC2Campaign.HOTS)], "Umoja", completion_critical=True, removal_priority=1),
        FillMission(MissionPools.EASY, [MissionConnection(2, SC2Campaign.HOTS)], "Kaldir", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.HOTS)], "Kaldir", completion_critical=True, removal_priority=2),
        FillMission(MissionPools.MEDIUM, [MissionConnection(4, SC2Campaign.HOTS)], "Kaldir", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(2, SC2Campaign.HOTS)], "Char", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(6, SC2Campaign.HOTS)], "Char", completion_critical=True, removal_priority=3),
        FillMission(MissionPools.MEDIUM, [MissionConnection(7, SC2Campaign.HOTS)], "Char", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(5, SC2Campaign.HOTS), MissionConnection(8, SC2Campaign.HOTS)], "Zerus", completion_critical=True, or_requirements=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(9, SC2Campaign.HOTS)], "Zerus", completion_critical=True, removal_priority=4),
        FillMission(MissionPools.MEDIUM, [MissionConnection(10, SC2Campaign.HOTS)], "Zerus", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(5, SC2Campaign.HOTS), MissionConnection(8, SC2Campaign.HOTS), MissionConnection(11, SC2Campaign.HOTS)], "Skygeirr Station", completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(12, SC2Campaign.HOTS)], "Skygeirr Station", completion_critical=True, removal_priority=5),
        FillMission(MissionPools.HARD, [MissionConnection(13, SC2Campaign.HOTS)], "Skygeirr Station", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(5, SC2Campaign.HOTS), MissionConnection(8, SC2Campaign.HOTS), MissionConnection(11, SC2Campaign.HOTS)], "Dominion Space", completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(15, SC2Campaign.HOTS)], "Dominion Space", completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(14, SC2Campaign.HOTS), MissionConnection(16, SC2Campaign.HOTS)], "Korhal", completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(17, SC2Campaign.HOTS)], "Korhal", completion_critical=True),
        FillMission(MissionPools.FINAL, [MissionConnection(18, SC2Campaign.HOTS)], "Korhal", completion_critical=True),
    ]
}

mini_campaign_order: Dict[SC2Campaign, List[FillMission]] = {
    SC2Campaign.WOL: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.WOL)], "Mar Sara", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.WOL)], "Colonist"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(1, SC2Campaign.WOL)], "Colonist"),
        FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.WOL)], "Artifact", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.WOL)], "Artifact", number=4, completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(4, SC2Campaign.WOL)], "Artifact", number=8, completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.WOL)], "Covert", number=2),
        FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.WOL)], "Covert"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.WOL)], "Rebellion", number=3),
        FillMission(MissionPools.HARD, [MissionConnection(8, SC2Campaign.WOL)], "Rebellion"),
        FillMission(MissionPools.HARD, [MissionConnection(5, SC2Campaign.WOL)], "Char", completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(5, SC2Campaign.WOL)], "Char", completion_critical=True),
        FillMission(MissionPools.FINAL, [MissionConnection(10, SC2Campaign.WOL), MissionConnection(11, SC2Campaign.WOL)], "Char", completion_critical=True, or_requirements=True)
    ],
    SC2Campaign.PROPHECY: [
        FillMission(MissionPools.MEDIUM, [MissionConnection(4, SC2Campaign.WOL)], "_1"),
        FillMission(MissionPools.FINAL, [MissionConnection(0, SC2Campaign.PROPHECY)], "_2"),
    ],
    SC2Campaign.HOTS: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1, SC2Campaign.HOTS)], "Umoja", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.HOTS)], "Kaldir"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(1, SC2Campaign.HOTS)], "Kaldir"),
        FillMission(MissionPools.EASY, [MissionConnection(0, SC2Campaign.HOTS)], "Char"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(3, SC2Campaign.HOTS)], "Char"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(0, SC2Campaign.HOTS)], "Zerus", number=3),
        FillMission(MissionPools.MEDIUM, [MissionConnection(5, SC2Campaign.HOTS)], "Zerus"),
        FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.HOTS)], "Skygeirr Station", number=5),
        FillMission(MissionPools.HARD, [MissionConnection(7, SC2Campaign.HOTS)], "Skygeirr Station"),
        FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.HOTS)], "Dominion Space", number=5),
        FillMission(MissionPools.HARD, [MissionConnection(9, SC2Campaign.HOTS)], "Dominion Space"),
        FillMission(MissionPools.HARD, [MissionConnection(6, SC2Campaign.HOTS)], "Korhal", completion_critical=True, number=8),
        FillMission(MissionPools.FINAL, [MissionConnection(11, SC2Campaign.HOTS)], "Korhal", completion_critical=True),
    ]
}

gauntlet_order: Dict[SC2Campaign, List[FillMission]] = {
    SC2Campaign.GLOBAL: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1)], "I", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(0)], "II", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(1)], "III", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(2)], "IV", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(3)], "V", completion_critical=True),
        FillMission(MissionPools.HARD, [MissionConnection(4)], "VI", completion_critical=True),
        FillMission(MissionPools.FINAL, [MissionConnection(5)], "Final", completion_critical=True)
    ]
}

mini_gauntlet_order: Dict[SC2Campaign, List[FillMission]] = {
    SC2Campaign.GLOBAL: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1)], "I", completion_critical=True),
        FillMission(MissionPools.EASY, [MissionConnection(0)], "II", completion_critical=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(1)], "III", completion_critical=True),
        FillMission(MissionPools.FINAL, [MissionConnection(2)], "Final", completion_critical=True)
    ]
}

grid_order: Dict[SC2Campaign, List[FillMission]] = {
    SC2Campaign.GLOBAL: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1)], "_1"),
        FillMission(MissionPools.EASY, [MissionConnection(0)], "_1"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(1), MissionConnection(6), MissionConnection( 3)], "_1", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(2), MissionConnection(7)], "_1", or_requirements=True),
        FillMission(MissionPools.EASY, [MissionConnection(0)], "_2"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(1), MissionConnection(4)], "_2", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(2), MissionConnection(5), MissionConnection(10), MissionConnection(7)], "_2", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(3), MissionConnection(6), MissionConnection(11)], "_2", or_requirements=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(4), MissionConnection(9), MissionConnection(12)], "_3", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(5), MissionConnection(8), MissionConnection(10), MissionConnection(13)], "_3", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(6), MissionConnection(9), MissionConnection(11), MissionConnection(14)], "_3", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(7), MissionConnection(10)], "_3", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(8), MissionConnection(13)], "_4", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(9), MissionConnection(12), MissionConnection(14)], "_4", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(10), MissionConnection(13)], "_4", or_requirements=True),
        FillMission(MissionPools.FINAL, [MissionConnection(11), MissionConnection(14)], "_4", or_requirements=True)
    ]
}

mini_grid_order: Dict[SC2Campaign, List[FillMission]] = {
    SC2Campaign.GLOBAL: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1)], "_1"),
        FillMission(MissionPools.EASY, [MissionConnection(0)], "_1"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(1), MissionConnection(5)], "_1", or_requirements=True),
        FillMission(MissionPools.EASY, [MissionConnection(0)], "_2"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(1), MissionConnection(3)], "_2", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(2), MissionConnection(4)], "_2", or_requirements=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(3), MissionConnection(7)], "_3", or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(4), MissionConnection(6)], "_3", or_requirements=True),
        FillMission(MissionPools.FINAL, [MissionConnection(5), MissionConnection(7)], "_3", or_requirements=True)
    ]
}

tiny_grid_order: Dict[SC2Campaign, List[FillMission]] = {
    SC2Campaign.GLOBAL: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1)], "_1"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(0)], "_1"),
        FillMission(MissionPools.EASY, [MissionConnection(0)], "_2"),
        FillMission(MissionPools.FINAL, [MissionConnection(1), MissionConnection(2)], "_2", or_requirements=True),
    ]
}

blitz_order: Dict[SC2Campaign, List[FillMission]] = {
    SC2Campaign.GLOBAL: [
        FillMission(MissionPools.STARTER, [MissionConnection(-1)], "I"),
        FillMission(MissionPools.EASY, [MissionConnection(-1)], "I"),
        FillMission(MissionPools.MEDIUM, [MissionConnection(0), MissionConnection(1)], "II", number=1, or_requirements=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(0), MissionConnection(1)], "II", number=1, or_requirements=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(0), MissionConnection(1)], "III", number=2, or_requirements=True),
        FillMission(MissionPools.MEDIUM, [MissionConnection(0), MissionConnection(1)], "III", number=2, or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(0), MissionConnection(1)], "IV", number=3, or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(0), MissionConnection(1)], "IV", number=3, or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(0), MissionConnection(1)], "V", number=4, or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(0), MissionConnection(1)], "V", number=4, or_requirements=True),
        FillMission(MissionPools.HARD, [MissionConnection(0), MissionConnection(1)], "Final", number=5, or_requirements=True),
        FillMission(MissionPools.FINAL, [MissionConnection(0), MissionConnection(1)], "Final", number=5, or_requirements=True)
    ]
}


mission_orders: List[Dict[SC2Campaign, List[FillMission]]] = [
    vanilla_shuffle_order,
    vanilla_shuffle_order,
    mini_campaign_order,
    grid_order,
    mini_grid_order,
    blitz_order,
    gauntlet_order,
    mini_gauntlet_order,
    tiny_grid_order
]


vanilla_mission_req_table: Dict[SC2Campaign, Dict[str, MissionInfo]] = {
    SC2Campaign.WOL: {
        SC2Mission.LIBERATION_DAY.mission_name: MissionInfo(SC2Mission.LIBERATION_DAY, [], SC2Mission.LIBERATION_DAY.area, completion_critical=True),
        SC2Mission.THE_OUTLAWS.mission_name: MissionInfo(SC2Mission.THE_OUTLAWS, [MissionConnection(1, SC2Campaign.WOL)], SC2Mission.THE_OUTLAWS.area, completion_critical=True),
        SC2Mission.ZERO_HOUR.mission_name: MissionInfo(SC2Mission.ZERO_HOUR, [MissionConnection(2, SC2Campaign.WOL)], SC2Mission.ZERO_HOUR.area, completion_critical=True),
        SC2Mission.EVACUATION.mission_name: MissionInfo(SC2Mission.EVACUATION, [MissionConnection(3, SC2Campaign.WOL)], SC2Mission.EVACUATION.area),
        SC2Mission.OUTBREAK.mission_name: MissionInfo(SC2Mission.OUTBREAK, [MissionConnection(4, SC2Campaign.WOL)], SC2Mission.OUTBREAK.area),
        SC2Mission.SAFE_HAVEN.mission_name: MissionInfo(SC2Mission.SAFE_HAVEN, [MissionConnection(5, SC2Campaign.WOL)], SC2Mission.SAFE_HAVEN.area, number=7),
        SC2Mission.HAVENS_FALL.mission_name: MissionInfo(SC2Mission.HAVENS_FALL, [MissionConnection(5, SC2Campaign.WOL)], SC2Mission.HAVENS_FALL.area, number=7),
        SC2Mission.SMASH_AND_GRAB.mission_name: MissionInfo(SC2Mission.SMASH_AND_GRAB, [MissionConnection(3, SC2Campaign.WOL)], SC2Mission.SMASH_AND_GRAB.area, completion_critical=True),
        SC2Mission.THE_DIG.mission_name: MissionInfo(SC2Mission.THE_DIG, [MissionConnection(8, SC2Campaign.WOL)], SC2Mission.THE_DIG.area, number=8, completion_critical=True),
        SC2Mission.THE_MOEBIUS_FACTOR.mission_name: MissionInfo(SC2Mission.THE_MOEBIUS_FACTOR, [MissionConnection(9, SC2Campaign.WOL)], SC2Mission.THE_MOEBIUS_FACTOR.area, number=11, completion_critical=True),
        SC2Mission.SUPERNOVA.mission_name: MissionInfo(SC2Mission.SUPERNOVA, [MissionConnection(10, SC2Campaign.WOL)], SC2Mission.SUPERNOVA.area, number=14, completion_critical=True),
        SC2Mission.MAW_OF_THE_VOID.mission_name: MissionInfo(SC2Mission.MAW_OF_THE_VOID, [MissionConnection(11, SC2Campaign.WOL)], SC2Mission.MAW_OF_THE_VOID.area, completion_critical=True),
        SC2Mission.DEVILS_PLAYGROUND.mission_name: MissionInfo(SC2Mission.DEVILS_PLAYGROUND, [MissionConnection(3, SC2Campaign.WOL)], SC2Mission.DEVILS_PLAYGROUND.area, number=4),
        SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name: MissionInfo(SC2Mission.WELCOME_TO_THE_JUNGLE, [MissionConnection(13, SC2Campaign.WOL)], SC2Mission.WELCOME_TO_THE_JUNGLE.area),
        SC2Mission.BREAKOUT.mission_name: MissionInfo(SC2Mission.BREAKOUT, [MissionConnection(14, SC2Campaign.WOL)], SC2Mission.BREAKOUT.area, number=8),
        SC2Mission.GHOST_OF_A_CHANCE.mission_name: MissionInfo(SC2Mission.GHOST_OF_A_CHANCE, [MissionConnection(14, SC2Campaign.WOL)], SC2Mission.GHOST_OF_A_CHANCE.area, number=8),
        SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name: MissionInfo(SC2Mission.THE_GREAT_TRAIN_ROBBERY, [MissionConnection(3, SC2Campaign.WOL)], SC2Mission.THE_GREAT_TRAIN_ROBBERY.area, number=6),
        SC2Mission.CUTTHROAT.mission_name: MissionInfo(SC2Mission.CUTTHROAT, [MissionConnection(17, SC2Campaign.WOL)], SC2Mission.THE_GREAT_TRAIN_ROBBERY.area),
        SC2Mission.ENGINE_OF_DESTRUCTION.mission_name: MissionInfo(SC2Mission.ENGINE_OF_DESTRUCTION, [MissionConnection(18, SC2Campaign.WOL)], SC2Mission.ENGINE_OF_DESTRUCTION.area),
        SC2Mission.MEDIA_BLITZ.mission_name: MissionInfo(SC2Mission.MEDIA_BLITZ, [MissionConnection(19, SC2Campaign.WOL)], SC2Mission.MEDIA_BLITZ.area),
        SC2Mission.PIERCING_OF_THE_SHROUD.mission_name: MissionInfo(SC2Mission.PIERCING_OF_THE_SHROUD, [MissionConnection(20, SC2Campaign.WOL)], SC2Mission.PIERCING_OF_THE_SHROUD.area),
        SC2Mission.GATES_OF_HELL.mission_name: MissionInfo(SC2Mission.GATES_OF_HELL, [MissionConnection(12, SC2Campaign.WOL)], SC2Mission.GATES_OF_HELL.area, completion_critical=True),
        SC2Mission.BELLY_OF_THE_BEAST.mission_name: MissionInfo(SC2Mission.BELLY_OF_THE_BEAST, [MissionConnection(22, SC2Campaign.WOL)], SC2Mission.BELLY_OF_THE_BEAST.area, completion_critical=True),
        SC2Mission.SHATTER_THE_SKY.mission_name: MissionInfo(SC2Mission.SHATTER_THE_SKY, [MissionConnection(22, SC2Campaign.WOL)], SC2Mission.SHATTER_THE_SKY.area, completion_critical=True),
        SC2Mission.ALL_IN.mission_name: MissionInfo(SC2Mission.ALL_IN, [MissionConnection(23, SC2Campaign.WOL), MissionConnection(24, SC2Campaign.WOL)], SC2Mission.ALL_IN.area, or_requirements=True, completion_critical=True)
    },
    SC2Campaign.PROPHECY: {
        SC2Mission.WHISPERS_OF_DOOM.mission_name: MissionInfo(SC2Mission.WHISPERS_OF_DOOM, [MissionConnection(9, SC2Campaign.WOL)], SC2Mission.WHISPERS_OF_DOOM.area),
        SC2Mission.A_SINISTER_TURN.mission_name: MissionInfo(SC2Mission.A_SINISTER_TURN, [MissionConnection(1, SC2Campaign.PROPHECY)], SC2Mission.A_SINISTER_TURN.area),
        SC2Mission.ECHOES_OF_THE_FUTURE.mission_name: MissionInfo(SC2Mission.ECHOES_OF_THE_FUTURE, [MissionConnection(2, SC2Campaign.PROPHECY)], SC2Mission.A_SINISTER_TURN.area),
        SC2Mission.IN_UTTER_DARKNESS.mission_name: MissionInfo(SC2Mission.IN_UTTER_DARKNESS, [MissionConnection(3, SC2Campaign.PROPHECY)], SC2Mission.IN_UTTER_DARKNESS.area)
    },
    SC2Campaign.HOTS: {
        SC2Mission.LAB_RAT.mission_name: MissionInfo(SC2Mission.LAB_RAT, [], SC2Mission.LAB_RAT.area, completion_critical=True),
        SC2Mission.BACK_IN_THE_SADDLE.mission_name: MissionInfo(SC2Mission.BACK_IN_THE_SADDLE, [MissionConnection(1, SC2Campaign.HOTS)], SC2Mission.BACK_IN_THE_SADDLE.area, completion_critical=True),
        SC2Mission.RENDEZVOUS.mission_name: MissionInfo(SC2Mission.RENDEZVOUS, [MissionConnection(2, SC2Campaign.HOTS)], SC2Mission.RENDEZVOUS.area, completion_critical=True),
        SC2Mission.HARVEST_OF_SCREAMS.mission_name: MissionInfo(SC2Mission.HARVEST_OF_SCREAMS, [MissionConnection(3, SC2Campaign.HOTS)], SC2Mission.HARVEST_OF_SCREAMS.area),
        SC2Mission.SHOOT_THE_MESSENGER.mission_name: MissionInfo(SC2Mission.SHOOT_THE_MESSENGER, [MissionConnection(4, SC2Campaign.HOTS)], SC2Mission.SHOOT_THE_MESSENGER.area),
        SC2Mission.ENEMY_WITHIN.mission_name: MissionInfo(SC2Mission.ENEMY_WITHIN, [MissionConnection(5, SC2Campaign.HOTS)], SC2Mission.ENEMY_WITHIN.area),
        SC2Mission.DOMINATION.mission_name: MissionInfo(SC2Mission.DOMINATION, [MissionConnection(3, SC2Campaign.HOTS)], SC2Mission.DOMINATION.area),
        SC2Mission.FIRE_IN_THE_SKY.mission_name: MissionInfo(SC2Mission.FIRE_IN_THE_SKY, [MissionConnection(7, SC2Campaign.HOTS)], SC2Mission.FIRE_IN_THE_SKY.area),
        SC2Mission.OLD_SOLDIERS.mission_name: MissionInfo(SC2Mission.OLD_SOLDIERS, [MissionConnection(8, SC2Campaign.HOTS)], SC2Mission.OLD_SOLDIERS.area),
        SC2Mission.WAKING_THE_ANCIENT.mission_name: MissionInfo(SC2Mission.WAKING_THE_ANCIENT, [MissionConnection(6, SC2Campaign.HOTS), MissionConnection(9, SC2Campaign.HOTS)], SC2Mission.WAKING_THE_ANCIENT.area, completion_critical=True, or_requirements=True),
        SC2Mission.THE_CRUCIBLE.mission_name: MissionInfo(SC2Mission.THE_CRUCIBLE, [MissionConnection(10, SC2Campaign.HOTS)], SC2Mission.THE_CRUCIBLE.area, completion_critical=True),
        SC2Mission.SUPREME.mission_name: MissionInfo(SC2Mission.SUPREME, [MissionConnection(11, SC2Campaign.HOTS)], SC2Mission.SUPREME.area, completion_critical=True),
        SC2Mission.INFESTED.mission_name: MissionInfo(SC2Mission.INFESTED, [MissionConnection(6, SC2Campaign.HOTS), MissionConnection(9, SC2Campaign.HOTS), MissionConnection(12, SC2Campaign.HOTS)], SC2Mission.INFESTED.area),
        SC2Mission.HAND_OF_DARKNESS.mission_name: MissionInfo(SC2Mission.HAND_OF_DARKNESS, [MissionConnection(13, SC2Campaign.HOTS)], SC2Mission.HAND_OF_DARKNESS.area),
        SC2Mission.PHANTOMS_OF_THE_VOID.mission_name: MissionInfo(SC2Mission.PHANTOMS_OF_THE_VOID, [MissionConnection(14, SC2Campaign.HOTS)], SC2Mission.PHANTOMS_OF_THE_VOID.area),
        SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name: MissionInfo(SC2Mission.WITH_FRIENDS_LIKE_THESE, [MissionConnection(6, SC2Campaign.HOTS), MissionConnection(9, SC2Campaign.HOTS), MissionConnection(12, SC2Campaign.HOTS)], SC2Mission.WITH_FRIENDS_LIKE_THESE.area),
        SC2Mission.CONVICTION.mission_name: MissionInfo(SC2Mission.CONVICTION, [MissionConnection(16, SC2Campaign.HOTS)], SC2Mission.CONVICTION.area),
        SC2Mission.PLANETFALL.mission_name: MissionInfo(SC2Mission.PLANETFALL, [MissionConnection(15, SC2Campaign.HOTS), MissionConnection(17, SC2Campaign.HOTS)], SC2Mission.PLANETFALL.area, completion_critical=True),
        SC2Mission.DEATH_FROM_ABOVE.mission_name: MissionInfo(SC2Mission.DEATH_FROM_ABOVE, [MissionConnection(18, SC2Campaign.HOTS)], SC2Mission.DEATH_FROM_ABOVE.area, completion_critical=True),
        SC2Mission.THE_RECKONING.mission_name: MissionInfo(SC2Mission.THE_RECKONING, [MissionConnection(19, SC2Campaign.HOTS)], SC2Mission.THE_RECKONING.area, completion_critical=True),
    },
}

lookup_id_to_mission: Dict[int, SC2Mission] = {
    mission.id: mission for mission in SC2Mission
}

lookup_name_to_mission: Dict[str, SC2Mission] = {
    mission.mission_name: mission for mission in SC2Mission
}

lookup_id_to_campaign: Dict[int, SC2Campaign] = {
    campaign.id: campaign for campaign in SC2Campaign
}


campaign_mission_table: Dict[SC2Campaign, Set[SC2Mission]] = {
    campaign: set() for campaign in SC2Campaign
}
for mission in SC2Mission:
    campaign_mission_table[mission.campaign].add(mission)


def get_campaign_difficulty(campaign: SC2Campaign, excluded_missions: Set[SC2Mission] = None) -> MissionPools:
    """

    :param campaign:
    :param excluded_missions:
    :return: Campaign's the most difficult non-excluded mission
    """
    if excluded_missions is None:
        excluded_missions = []
    excluded_mission_set = set(excluded_missions)
    included_missions = campaign_mission_table[campaign].difference(excluded_mission_set)
    return max([mission.pool for mission in included_missions])


def get_campaign_goal_priority(campaign: SC2Campaign, excluded_missions: Set[SC2Mission] | frozenset[SC2Mission] = None) -> SC2CampaignGoalPriority:
    """
    Gets a modified campaign goal priority.
    If all the campaign's goal missions are excluded, it's ineligible to have the goal
    If the campaign's very hard missions are excluded, the priority is lowered to hard
    :param campaign:
    :param excluded_missions:
    :return:
    """
    if excluded_missions is None:
        return campaign.goal_priority
    else:
        goal_missions = set(get_campaign_potential_goal_missions(campaign))
        excluded_mission_set = set(excluded_missions)
        remaining_goals = goal_missions.difference(excluded_mission_set)
        if remaining_goals == set():
            # All potential goals are excluded, the campaign can't be a goal
            return SC2CampaignGoalPriority.NONE
        elif campaign.goal_priority == SC2CampaignGoalPriority.VERY_HARD:
            # Check if a very hard campaign doesn't get rid of it's last very hard mission
            difficulty = get_campaign_difficulty(campaign, excluded_missions)
            if difficulty == MissionPools.VERY_HARD:
                return SC2CampaignGoalPriority.VERY_HARD
            else:
                return SC2CampaignGoalPriority.HARD
        else:
            return campaign.goal_priority


starting_mission_locations = {
    # WoL
    "Liberation Day": "Liberation Day: Victory",
    "Breakout": "Breakout: Victory",
    "Ghost of a Chance": "Ghost of a Chance: Victory",
    "Piercing the Shroud": "Piercing the Shroud: Victory",
    "Whispers of Doom": "Whispers of Doom: Victory",
    "Belly of the Beast": "Belly of the Beast: Victory",
    "Zero Hour": "Zero Hour: First Group Rescued",
    "Evacuation": "Evacuation: Reach Hanson",
    "Devil's Playground": "Devil's Playground: Tosh's Miners",
    "Smash and Grab": "Smash and Grab: First Relic",
    "The Great Train Robbery": "The Great Train Robbery: North Defiler",
    # HotS
    "Lab Rat": "Lab Rat: Gather Minerals",
    "Back in the Saddle": "Back in the Saddle: Victory",
    "Harvest of Screams": "Harvest of Screams: First Ursadon Matriarch",
    "Shoot the Messenger": "Shoot the Messenger: Center Stasis Chamber",
    "Domination": "Domination: Repel Zagara",
    "Fire in the Sky": "Fire in the Sky: West Biomass",
    "Old Soldiers": "Old Soldiers: Get Nuked",
    "Enemy Within": "Enemy Within: Victory",
    "Waking the Ancient": "Waking the Ancient: Center Essence Pool",
    "Supreme": "Supreme: Victory",
    "With Friends Like These": "With Friends Like These: Victory",
    "Conviction": "Conviction: Victory",
}


class SC2CampaignGoal(NamedTuple):
    mission: SC2Mission
    location: str


campaign_final_mission_locations: Dict[SC2Campaign, SC2CampaignGoal] = {
    SC2Campaign.WOL: SC2CampaignGoal(SC2Mission.ALL_IN, "All-In: Victory"),
    SC2Campaign.PROPHECY: SC2CampaignGoal(SC2Mission.IN_UTTER_DARKNESS, "In Utter Darkness: Kills"),
    SC2Campaign.HOTS: SC2CampaignGoal(SC2Mission.THE_RECKONING, "The Reckoning: Victory")
}

campaign_alt_final_mission_locations: Dict[SC2Campaign, Dict[SC2Mission, str]] = {
    SC2Campaign.WOL: {
        SC2Mission.MAW_OF_THE_VOID: "Maw of the Void: Victory",
        SC2Mission.ENGINE_OF_DESTRUCTION: "Engine of Destruction: Victory",
        SC2Mission.SUPERNOVA: "Supernova: Victory",
        SC2Mission.GATES_OF_HELL: "Gates of Hell: Victory",
        SC2Mission.SHATTER_THE_SKY: "Shatter the Sky: Victory"
    },
    SC2Campaign.PROPHECY: None,
    SC2Campaign.HOTS: {
        SC2Mission.THE_CRUCIBLE: "The Crucible: Victory",
        SC2Mission.HAND_OF_DARKNESS: "Hand of Darkness: Victory",
        SC2Mission.PHANTOMS_OF_THE_VOID: "Phantoms of the Void: Victory",
        SC2Mission.PLANETFALL: "Planetfall: Victory",
        SC2Mission.DEATH_FROM_ABOVE: "Death From Above: Victory"
    },
}


def get_goal_location(mission: SC2Mission) -> str | None:
    """

    :param mission:
    :return: Goal location assigned to the goal mission
    """
    campaign = mission.campaign
    primary_campaign_goal = campaign_final_mission_locations[campaign]
    if primary_campaign_goal is not None:
        if primary_campaign_goal.mission == mission:
            return primary_campaign_goal.location

    campaign_alt_goals = campaign_alt_final_mission_locations[campaign]
    if campaign_alt_goals is not None:
        return campaign_alt_goals.get(mission)

    return None


def get_campaign_potential_goal_missions(campaign: SC2Campaign) -> List[SC2Mission]:
    """

    :param campaign:
    :return: All missions that can be the campaign's goal
    """
    missions: List[SC2Mission] = list()
    primary_goal_mission = campaign_final_mission_locations[campaign]
    if primary_goal_mission is not None:
        missions.append(primary_goal_mission.mission)
    alt_goal_locations = campaign_alt_final_mission_locations[campaign]
    if alt_goal_locations is not None:
        for mission in alt_goal_locations.keys():
            missions.append(mission)

    return missions


def get_no_build_missions() -> List[SC2Mission]:
    return [mission for mission in SC2Mission if not mission.build]

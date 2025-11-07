from typing import NamedTuple, Dict, List, Set, Union, Literal, Iterable, Optional
from enum import IntEnum, Enum, IntFlag, auto


class SC2Race(IntEnum):
    ANY = 0
    TERRAN = 1
    ZERG = 2
    PROTOSS = 3

    def get_title(self):
        return self.name.lower().capitalize()

    def get_mission_flag(self):
        return MissionFlag.__getitem__(self.get_title())

class MissionPools(IntEnum):
    STARTER = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3
    VERY_HARD = 4
    FINAL = 5


class MissionFlag(IntFlag):
    none          = 0
    Terran        = auto()
    Zerg          = auto()
    Protoss       = auto()
    NoBuild       = auto()
    Defense       = auto()
    AutoScroller  = auto()  # The mission is won by waiting out a timer or victory is gated behind a timer
    Countdown     = auto()  # Overall, the mission must be beaten before a loss timer counts down
    Kerrigan      = auto()  # The player controls Kerrigan in the mission
    VanillaSoa    = auto()  # The player controls the Spear of Adun in the vanilla version of the mission
    Nova          = auto()  # The player controls NCO Nova in the mission
    AiTerranAlly  = auto()  # The mission has a Terran AI ally that can be taken over
    AiZergAlly    = auto()  # The mission has a Zerg AI ally that can be taken over
    AiProtossAlly = auto()  # The mission has a Protoss AI ally that can be taken over
    VsTerran      = auto()
    VsZerg        = auto()
    VsProtoss     = auto()
    HasRaceSwap   = auto()  # The mission has variants that use different factions from the vanilla experience.
    RaceSwap      = auto()  # The mission uses different factions from the vanilla experience.
    WoLNova       = auto()  # The player controls WoL Nova in the mission

    AiAlly        = AiTerranAlly|AiZergAlly|AiProtossAlly
    TimedDefense  = AutoScroller|Defense
    VsTZ          = VsTerran|VsZerg
    VsTP          = VsTerran|VsProtoss
    VsPZ          = VsProtoss|VsZerg
    VsAll         = VsTerran|VsProtoss|VsZerg


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
        self.race = race

    def __lt__(self, other: "SC2Campaign"):
        return self.id < other.id

    GLOBAL = 0, "Global", SC2CampaignGoalPriority.NONE, SC2Race.ANY
    WOL = 1, "Wings of Liberty", SC2CampaignGoalPriority.VERY_HARD, SC2Race.TERRAN
    PROPHECY = 2, "Prophecy", SC2CampaignGoalPriority.MINI_CAMPAIGN, SC2Race.PROTOSS
    HOTS = 3, "Heart of the Swarm", SC2CampaignGoalPriority.VERY_HARD, SC2Race.ZERG
    PROLOGUE = 4, "Whispers of Oblivion (Legacy of the Void: Prologue)", SC2CampaignGoalPriority.MINI_CAMPAIGN, SC2Race.PROTOSS
    LOTV = 5, "Legacy of the Void", SC2CampaignGoalPriority.VERY_HARD, SC2Race.PROTOSS
    EPILOGUE = 6, "Into the Void (Legacy of the Void: Epilogue)", SC2CampaignGoalPriority.EPILOGUE, SC2Race.ANY
    NCO = 7, "Nova Covert Ops", SC2CampaignGoalPriority.HARD, SC2Race.TERRAN


class SC2Mission(Enum):

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, mission_id: int, name: str, campaign: SC2Campaign, area: str, race: SC2Race, pool: MissionPools, map_file: str, flags: MissionFlag):
        self.id = mission_id
        self.mission_name = name
        self.campaign = campaign
        self.area = area
        self.race = race
        self.pool = pool
        self.map_file = map_file
        self.flags = flags

    def get_short_name(self):
        if self.mission_name.find(' (') == -1:
            return self.mission_name
        else:
            return self.mission_name[:self.mission_name.find(' (')]

    # Wings of Liberty
    LIBERATION_DAY = 1, "Liberation Day", SC2Campaign.WOL, "Mar Sara", SC2Race.ANY, MissionPools.STARTER, "ap_liberation_day", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsTerran
    THE_OUTLAWS = 2, "The Outlaws (Terran)", SC2Campaign.WOL, "Mar Sara", SC2Race.TERRAN, MissionPools.EASY, "ap_the_outlaws", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    ZERO_HOUR = 3, "Zero Hour (Terran)", SC2Campaign.WOL, "Mar Sara", SC2Race.TERRAN, MissionPools.EASY, "ap_zero_hour", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    EVACUATION = 4, "Evacuation (Terran)", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.EASY, "ap_evacuation", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    OUTBREAK = 5, "Outbreak (Terran)", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.EASY, "ap_outbreak", MissionFlag.Terran|MissionFlag.Defense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    SAFE_HAVEN = 6, "Safe Haven (Terran)", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_safe_haven", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    HAVENS_FALL = 7, "Haven's Fall (Terran)", SC2Campaign.WOL, "Colonist", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_havens_fall", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    SMASH_AND_GRAB = 8, "Smash and Grab (Terran)", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.EASY, "ap_smash_and_grab", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsPZ|MissionFlag.HasRaceSwap
    THE_DIG = 9, "The Dig (Terran)", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_dig", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    THE_MOEBIUS_FACTOR = 10, "The Moebius Factor (Terran)", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_moebius_factor", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    SUPERNOVA = 11, "Supernova (Terran)", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.HARD, "ap_supernova", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    MAW_OF_THE_VOID = 12, "Maw of the Void (Terran)", SC2Campaign.WOL, "Artifact", SC2Race.TERRAN, MissionPools.HARD, "ap_maw_of_the_void", MissionFlag.Terran|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    DEVILS_PLAYGROUND = 13, "Devil's Playground (Terran)", SC2Campaign.WOL, "Covert", SC2Race.TERRAN, MissionPools.EASY, "ap_devils_playground", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    WELCOME_TO_THE_JUNGLE = 14, "Welcome to the Jungle (Terran)", SC2Campaign.WOL, "Covert", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_welcome_to_the_jungle", MissionFlag.Terran|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    BREAKOUT = 15, "Breakout", SC2Campaign.WOL, "Covert", SC2Race.ANY, MissionPools.STARTER, "ap_breakout", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsTerran
    GHOST_OF_A_CHANCE = 16, "Ghost of a Chance", SC2Campaign.WOL, "Covert", SC2Race.ANY, MissionPools.STARTER, "ap_ghost_of_a_chance", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsTerran|MissionFlag.WoLNova
    THE_GREAT_TRAIN_ROBBERY = 17, "The Great Train Robbery (Terran)", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.EASY, "ap_the_great_train_robbery", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    CUTTHROAT = 18, "Cutthroat (Terran)", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_cutthroat", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    ENGINE_OF_DESTRUCTION = 19, "Engine of Destruction (Terran)", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.HARD, "ap_engine_of_destruction", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    MEDIA_BLITZ = 20, "Media Blitz (Terran)", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_media_blitz", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    PIERCING_OF_THE_SHROUD = 21, "Piercing the Shroud", SC2Campaign.WOL, "Rebellion", SC2Race.TERRAN, MissionPools.STARTER, "ap_piercing_the_shroud", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsAll
    GATES_OF_HELL = 26, "Gates of Hell (Terran)", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.HARD, "ap_gates_of_hell", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    BELLY_OF_THE_BEAST = 27, "Belly of the Beast", SC2Campaign.WOL, "Char", SC2Race.ANY, MissionPools.STARTER, "ap_belly_of_the_beast", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsZerg
    SHATTER_THE_SKY = 28, "Shatter the Sky (Terran)", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_shatter_the_sky", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    ALL_IN = 29, "All-In (Terran)", SC2Campaign.WOL, "Char", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_all_in", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap

    # Prophecy
    WHISPERS_OF_DOOM = 22, "Whispers of Doom", SC2Campaign.PROPHECY, "_1", SC2Race.ANY, MissionPools.STARTER, "ap_whispers_of_doom", MissionFlag.Protoss|MissionFlag.NoBuild|MissionFlag.VsZerg
    A_SINISTER_TURN = 23, "A Sinister Turn (Protoss)", SC2Campaign.PROPHECY, "_2", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_a_sinister_turn", MissionFlag.Protoss|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    ECHOES_OF_THE_FUTURE = 24, "Echoes of the Future (Protoss)", SC2Campaign.PROPHECY, "_3", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_echoes_of_the_future", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    IN_UTTER_DARKNESS = 25, "In Utter Darkness (Protoss)", SC2Campaign.PROPHECY, "_4", SC2Race.PROTOSS, MissionPools.HARD, "ap_in_utter_darkness", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap

    # Heart of the Swarm
    LAB_RAT = 30, "Lab Rat (Zerg)", SC2Campaign.HOTS, "Umoja", SC2Race.ZERG, MissionPools.STARTER, "ap_lab_rat", MissionFlag.Zerg|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    BACK_IN_THE_SADDLE = 31, "Back in the Saddle", SC2Campaign.HOTS, "Umoja", SC2Race.ANY, MissionPools.STARTER, "ap_back_in_the_saddle", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.NoBuild|MissionFlag.VsTZ
    RENDEZVOUS = 32, "Rendezvous (Zerg)", SC2Campaign.HOTS, "Umoja", SC2Race.ZERG, MissionPools.EASY, "ap_rendezvous", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    HARVEST_OF_SCREAMS = 33, "Harvest of Screams (Zerg)", SC2Campaign.HOTS, "Kaldir", SC2Race.ZERG, MissionPools.EASY, "ap_harvest_of_screams", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    SHOOT_THE_MESSENGER = 34, "Shoot the Messenger (Zerg)", SC2Campaign.HOTS, "Kaldir", SC2Race.ZERG, MissionPools.EASY, "ap_shoot_the_messenger", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.TimedDefense|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    ENEMY_WITHIN = 35, "Enemy Within", SC2Campaign.HOTS, "Kaldir", SC2Race.ANY, MissionPools.EASY, "ap_enemy_within", MissionFlag.Zerg|MissionFlag.NoBuild|MissionFlag.VsProtoss
    DOMINATION = 36, "Domination (Zerg)", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.EASY, "ap_domination", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.Countdown|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    FIRE_IN_THE_SKY = 37, "Fire in the Sky (Zerg)", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.MEDIUM, "ap_fire_in_the_sky", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    OLD_SOLDIERS = 38, "Old Soldiers (Zerg)", SC2Campaign.HOTS, "Char", SC2Race.ZERG, MissionPools.MEDIUM, "ap_old_soldiers", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    WAKING_THE_ANCIENT = 39, "Waking the Ancient (Zerg)", SC2Campaign.HOTS, "Zerus", SC2Race.ZERG, MissionPools.MEDIUM, "ap_waking_the_ancient", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    THE_CRUCIBLE = 40, "The Crucible (Zerg)", SC2Campaign.HOTS, "Zerus", SC2Race.ZERG, MissionPools.MEDIUM, "ap_the_crucible", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    SUPREME = 41, "Supreme", SC2Campaign.HOTS, "Zerus", SC2Race.ANY, MissionPools.MEDIUM, "ap_supreme", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.NoBuild|MissionFlag.VsZerg
    INFESTED = 42, "Infested (Zerg)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.MEDIUM, "ap_infested", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    HAND_OF_DARKNESS = 43, "Hand of Darkness (Zerg)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.HARD, "ap_hand_of_darkness", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    PHANTOMS_OF_THE_VOID = 44, "Phantoms of the Void (Zerg)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.ZERG, MissionPools.MEDIUM, "ap_phantoms_of_the_void", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    WITH_FRIENDS_LIKE_THESE = 45, "With Friends Like These", SC2Campaign.HOTS, "Dominion Space", SC2Race.ANY, MissionPools.STARTER, "ap_with_friends_like_these", MissionFlag.Terran|MissionFlag.NoBuild|MissionFlag.VsTerran
    CONVICTION = 46, "Conviction", SC2Campaign.HOTS, "Dominion Space", SC2Race.ANY, MissionPools.MEDIUM, "ap_conviction", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.NoBuild|MissionFlag.VsTerran
    PLANETFALL = 47, "Planetfall (Zerg)", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.HARD, "ap_planetfall", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    DEATH_FROM_ABOVE = 48, "Death From Above (Zerg)", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.HARD, "ap_death_from_above", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    THE_RECKONING = 49, "The Reckoning (Zerg)", SC2Campaign.HOTS, "Korhal", SC2Race.ZERG, MissionPools.VERY_HARD, "ap_the_reckoning", MissionFlag.Zerg|MissionFlag.Kerrigan|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.HasRaceSwap

    # Prologue
    DARK_WHISPERS = 50, "Dark Whispers (Protoss)", SC2Campaign.PROLOGUE, "_1", SC2Race.PROTOSS, MissionPools.EASY, "ap_dark_whispers", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsTZ|MissionFlag.HasRaceSwap
    GHOSTS_IN_THE_FOG = 51, "Ghosts in the Fog (Protoss)", SC2Campaign.PROLOGUE, "_2", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_ghosts_in_the_fog", MissionFlag.Protoss|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    EVIL_AWOKEN = 52, "Evil Awoken", SC2Campaign.PROLOGUE, "_3", SC2Race.PROTOSS, MissionPools.STARTER, "ap_evil_awoken", MissionFlag.Protoss|MissionFlag.NoBuild|MissionFlag.VsProtoss

    # LotV
    FOR_AIUR = 53, "For Aiur!", SC2Campaign.LOTV, "Aiur", SC2Race.ANY, MissionPools.STARTER, "ap_for_aiur", MissionFlag.Protoss|MissionFlag.NoBuild|MissionFlag.VsZerg
    THE_GROWING_SHADOW = 54, "The Growing Shadow (Protoss)", SC2Campaign.LOTV, "Aiur", SC2Race.PROTOSS, MissionPools.EASY, "ap_the_growing_shadow", MissionFlag.Protoss|MissionFlag.VsPZ|MissionFlag.HasRaceSwap
    THE_SPEAR_OF_ADUN = 55, "The Spear of Adun (Protoss)", SC2Campaign.LOTV, "Aiur", SC2Race.PROTOSS, MissionPools.EASY, "ap_the_spear_of_adun", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsPZ|MissionFlag.HasRaceSwap
    SKY_SHIELD = 56, "Sky Shield (Protoss)", SC2Campaign.LOTV, "Korhal", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_sky_shield", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.HasRaceSwap
    BROTHERS_IN_ARMS = 57, "Brothers in Arms (Protoss)", SC2Campaign.LOTV, "Korhal", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_brothers_in_arms", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.HasRaceSwap
    AMON_S_REACH = 58, "Amon's Reach (Protoss)", SC2Campaign.LOTV, "Shakuras", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_amon_s_reach", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    LAST_STAND = 59, "Last Stand (Protoss)", SC2Campaign.LOTV, "Shakuras", SC2Race.PROTOSS, MissionPools.HARD, "ap_last_stand", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    FORBIDDEN_WEAPON = 60, "Forbidden Weapon (Protoss)", SC2Campaign.LOTV, "Purifier", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_forbidden_weapon", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    TEMPLE_OF_UNIFICATION = 61, "Temple of Unification (Protoss)", SC2Campaign.LOTV, "Ulnar", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_temple_of_unification", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsTP|MissionFlag.HasRaceSwap
    THE_INFINITE_CYCLE = 62, "The Infinite Cycle", SC2Campaign.LOTV, "Ulnar", SC2Race.ANY, MissionPools.HARD, "ap_the_infinite_cycle", MissionFlag.Protoss|MissionFlag.Kerrigan|MissionFlag.NoBuild|MissionFlag.VsTP
    HARBINGER_OF_OBLIVION = 63, "Harbinger of Oblivion (Protoss)", SC2Campaign.LOTV, "Ulnar", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_harbinger_of_oblivion", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.Countdown|MissionFlag.VsTP|MissionFlag.AiZergAlly|MissionFlag.HasRaceSwap
    UNSEALING_THE_PAST = 64, "Unsealing the Past (Protoss)", SC2Campaign.LOTV, "Purifier", SC2Race.PROTOSS, MissionPools.HARD, "ap_unsealing_the_past", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    PURIFICATION = 65, "Purification (Protoss)", SC2Campaign.LOTV, "Purifier", SC2Race.PROTOSS, MissionPools.HARD, "ap_purification", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsZerg|MissionFlag.HasRaceSwap
    STEPS_OF_THE_RITE = 66, "Steps of the Rite (Protoss)", SC2Campaign.LOTV, "Tal'darim", SC2Race.PROTOSS, MissionPools.HARD, "ap_steps_of_the_rite", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    RAK_SHIR = 67, "Rak'Shir (Protoss)", SC2Campaign.LOTV, "Tal'darim", SC2Race.PROTOSS, MissionPools.HARD, "ap_rak_shir", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsProtoss|MissionFlag.HasRaceSwap
    TEMPLAR_S_CHARGE = 68, "Templar's Charge (Protoss)", SC2Campaign.LOTV, "Moebius", SC2Race.PROTOSS, MissionPools.HARD, "ap_templar_s_charge", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsTerran|MissionFlag.HasRaceSwap
    TEMPLAR_S_RETURN = 69, "Templar's Return", SC2Campaign.LOTV, "Return to Aiur", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_templar_s_return", MissionFlag.Protoss|MissionFlag.NoBuild|MissionFlag.VsPZ
    THE_HOST = 70, "The Host (Protoss)", SC2Campaign.LOTV, "Return to Aiur", SC2Race.PROTOSS, MissionPools.VERY_HARD, "ap_the_host", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsAll|MissionFlag.HasRaceSwap
    SALVATION = 71, "Salvation (Protoss)", SC2Campaign.LOTV, "Return to Aiur", SC2Race.PROTOSS, MissionPools.VERY_HARD, "ap_salvation", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.TimedDefense|MissionFlag.VsPZ|MissionFlag.AiProtossAlly|MissionFlag.HasRaceSwap

    # Epilogue
    INTO_THE_VOID = 72, "Into the Void", SC2Campaign.EPILOGUE, "_1", SC2Race.PROTOSS, MissionPools.VERY_HARD, "ap_into_the_void", MissionFlag.Protoss|MissionFlag.VanillaSoa|MissionFlag.VsAll|MissionFlag.AiTerranAlly|MissionFlag.AiZergAlly
    THE_ESSENCE_OF_ETERNITY = 73, "The Essence of Eternity", SC2Campaign.EPILOGUE, "_2", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_the_essence_of_eternity", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsAll|MissionFlag.AiZergAlly|MissionFlag.AiProtossAlly
    AMON_S_FALL = 74, "Amon's Fall", SC2Campaign.EPILOGUE, "_3", SC2Race.ZERG, MissionPools.VERY_HARD, "ap_amon_s_fall", MissionFlag.Zerg|MissionFlag.AutoScroller|MissionFlag.VsAll|MissionFlag.AiTerranAlly|MissionFlag.AiProtossAlly

    # Nova Covert Ops
    THE_ESCAPE = 75, "The Escape", SC2Campaign.NCO, "_1", SC2Race.ANY, MissionPools.MEDIUM, "ap_the_escape", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.NoBuild|MissionFlag.VsTerran
    SUDDEN_STRIKE = 76, "Sudden Strike", SC2Campaign.NCO, "_1", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_sudden_strike", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.TimedDefense|MissionFlag.VsZerg
    ENEMY_INTELLIGENCE = 77, "Enemy Intelligence", SC2Campaign.NCO, "_1", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_enemy_intelligence", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.Defense|MissionFlag.VsZerg
    TROUBLE_IN_PARADISE = 78, "Trouble In Paradise", SC2Campaign.NCO, "_2", SC2Race.TERRAN, MissionPools.HARD, "ap_trouble_in_paradise", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.Countdown|MissionFlag.VsPZ
    NIGHT_TERRORS = 79, "Night Terrors", SC2Campaign.NCO, "_2", SC2Race.TERRAN, MissionPools.HARD, "ap_night_terrors", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.VsPZ
    FLASHPOINT = 80, "Flashpoint", SC2Campaign.NCO, "_2", SC2Race.TERRAN, MissionPools.HARD, "ap_flashpoint", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.VsZerg
    IN_THE_ENEMY_S_SHADOW = 81, "In the Enemy's Shadow", SC2Campaign.NCO, "_3", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_in_the_enemy_s_shadow", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.NoBuild|MissionFlag.VsTerran
    DARK_SKIES = 82, "Dark Skies", SC2Campaign.NCO, "_3", SC2Race.TERRAN, MissionPools.HARD, "ap_dark_skies", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.TimedDefense|MissionFlag.VsProtoss
    END_GAME = 83, "End Game", SC2Campaign.NCO, "_3", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_end_game", MissionFlag.Terran|MissionFlag.Nova|MissionFlag.Defense|MissionFlag.VsTerran

    # Race-Swapped Variants
    # 84/85 - Liberation Day
    THE_OUTLAWS_Z = 86, "The Outlaws (Zerg)", SC2Campaign.WOL, "Mar Sara", SC2Race.ZERG, MissionPools.EASY, "ap_the_outlaws", MissionFlag.Zerg|MissionFlag.VsTerran|MissionFlag.RaceSwap
    THE_OUTLAWS_P = 87, "The Outlaws (Protoss)", SC2Campaign.WOL, "Mar Sara", SC2Race.PROTOSS, MissionPools.EASY, "ap_the_outlaws", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.RaceSwap
    ZERO_HOUR_Z = 88, "Zero Hour (Zerg)", SC2Campaign.WOL, "Mar Sara", SC2Race.ZERG, MissionPools.MEDIUM, "ap_zero_hour", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    ZERO_HOUR_P = 89, "Zero Hour (Protoss)", SC2Campaign.WOL, "Mar Sara", SC2Race.PROTOSS, MissionPools.EASY, "ap_zero_hour", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    EVACUATION_Z = 90, "Evacuation (Zerg)", SC2Campaign.WOL, "Colonist", SC2Race.ZERG, MissionPools.EASY, "ap_evacuation", MissionFlag.Zerg|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.RaceSwap
    EVACUATION_P = 91, "Evacuation (Protoss)", SC2Campaign.WOL, "Colonist", SC2Race.PROTOSS, MissionPools.EASY, "ap_evacuation", MissionFlag.Protoss|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.RaceSwap
    OUTBREAK_Z = 92, "Outbreak (Zerg)", SC2Campaign.WOL, "Colonist", SC2Race.ZERG, MissionPools.MEDIUM, "ap_outbreak", MissionFlag.Zerg|MissionFlag.Defense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    OUTBREAK_P = 93, "Outbreak (Protoss)", SC2Campaign.WOL, "Colonist", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_outbreak", MissionFlag.Protoss|MissionFlag.Defense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    SAFE_HAVEN_Z = 94, "Safe Haven (Zerg)", SC2Campaign.WOL, "Colonist", SC2Race.ZERG, MissionPools.MEDIUM, "ap_safe_haven", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    SAFE_HAVEN_P = 95, "Safe Haven (Protoss)", SC2Campaign.WOL, "Colonist", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_safe_haven", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    HAVENS_FALL_Z = 96, "Haven's Fall (Zerg)", SC2Campaign.WOL, "Colonist", SC2Race.ZERG, MissionPools.MEDIUM, "ap_havens_fall", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    HAVENS_FALL_P = 97, "Haven's Fall (Protoss)", SC2Campaign.WOL, "Colonist", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_havens_fall", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.RaceSwap
    SMASH_AND_GRAB_Z = 98, "Smash and Grab (Zerg)", SC2Campaign.WOL, "Artifact", SC2Race.ZERG, MissionPools.EASY, "ap_smash_and_grab", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsPZ|MissionFlag.RaceSwap
    SMASH_AND_GRAB_P = 99, "Smash and Grab (Protoss)", SC2Campaign.WOL, "Artifact", SC2Race.PROTOSS, MissionPools.EASY, "ap_smash_and_grab", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsPZ|MissionFlag.RaceSwap
    THE_DIG_Z = 100, "The Dig (Zerg)", SC2Campaign.WOL, "Artifact", SC2Race.ZERG, MissionPools.MEDIUM, "ap_the_dig", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    THE_DIG_P = 101, "The Dig (Protoss)", SC2Campaign.WOL, "Artifact", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_the_dig", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    THE_MOEBIUS_FACTOR_Z = 102, "The Moebius Factor (Zerg)", SC2Campaign.WOL, "Artifact", SC2Race.ZERG, MissionPools.MEDIUM, "ap_the_moebius_factor", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsZerg|MissionFlag.RaceSwap
    THE_MOEBIUS_FACTOR_P = 103, "The Moebius Factor (Protoss)", SC2Campaign.WOL, "Artifact", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_the_moebius_factor", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsZerg|MissionFlag.RaceSwap
    SUPERNOVA_Z = 104, "Supernova (Zerg)", SC2Campaign.WOL, "Artifact", SC2Race.ZERG, MissionPools.HARD, "ap_supernova", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    SUPERNOVA_P = 105, "Supernova (Protoss)", SC2Campaign.WOL, "Artifact", SC2Race.PROTOSS, MissionPools.HARD, "ap_supernova", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    MAW_OF_THE_VOID_Z = 106, "Maw of the Void (Zerg)", SC2Campaign.WOL, "Artifact", SC2Race.ZERG, MissionPools.HARD, "ap_maw_of_the_void", MissionFlag.Zerg|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    MAW_OF_THE_VOID_P = 107, "Maw of the Void (Protoss)", SC2Campaign.WOL, "Artifact", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_maw_of_the_void", MissionFlag.Protoss|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    DEVILS_PLAYGROUND_Z = 108, "Devil's Playground (Zerg)", SC2Campaign.WOL, "Covert", SC2Race.ZERG, MissionPools.EASY, "ap_devils_playground", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    DEVILS_PLAYGROUND_P = 109, "Devil's Playground (Protoss)", SC2Campaign.WOL, "Covert", SC2Race.PROTOSS, MissionPools.EASY, "ap_devils_playground", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.RaceSwap
    WELCOME_TO_THE_JUNGLE_Z = 110, "Welcome to the Jungle (Zerg)", SC2Campaign.WOL, "Covert", SC2Race.ZERG, MissionPools.HARD, "ap_welcome_to_the_jungle", MissionFlag.Zerg|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    WELCOME_TO_THE_JUNGLE_P = 111, "Welcome to the Jungle (Protoss)", SC2Campaign.WOL, "Covert", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_welcome_to_the_jungle", MissionFlag.Protoss|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    # 112/113 - Breakout
    # 114/115 - Ghost of a Chance
    THE_GREAT_TRAIN_ROBBERY_Z = 116, "The Great Train Robbery (Zerg)", SC2Campaign.WOL, "Rebellion", SC2Race.ZERG, MissionPools.EASY, "ap_the_great_train_robbery", MissionFlag.Zerg|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    THE_GREAT_TRAIN_ROBBERY_P = 117, "The Great Train Robbery (Protoss)", SC2Campaign.WOL, "Rebellion", SC2Race.PROTOSS, MissionPools.EASY, "ap_the_great_train_robbery", MissionFlag.Protoss|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    CUTTHROAT_Z = 118, "Cutthroat (Zerg)", SC2Campaign.WOL, "Rebellion", SC2Race.ZERG, MissionPools.MEDIUM, "ap_cutthroat", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.RaceSwap
    CUTTHROAT_P = 119, "Cutthroat (Protoss)", SC2Campaign.WOL, "Rebellion", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_cutthroat", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.RaceSwap
    ENGINE_OF_DESTRUCTION_Z = 120, "Engine of Destruction (Zerg)", SC2Campaign.WOL, "Rebellion", SC2Race.ZERG, MissionPools.HARD, "ap_engine_of_destruction", MissionFlag.Zerg|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    ENGINE_OF_DESTRUCTION_P = 121, "Engine of Destruction (Protoss)", SC2Campaign.WOL, "Rebellion", SC2Race.PROTOSS, MissionPools.HARD, "ap_engine_of_destruction", MissionFlag.Protoss|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    MEDIA_BLITZ_Z = 122, "Media Blitz (Zerg)", SC2Campaign.WOL, "Rebellion", SC2Race.ZERG, MissionPools.HARD, "ap_media_blitz", MissionFlag.Zerg|MissionFlag.VsTerran|MissionFlag.RaceSwap
    MEDIA_BLITZ_P = 123, "Media Blitz (Protoss)", SC2Campaign.WOL, "Rebellion", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_media_blitz", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.RaceSwap
    # 124/125 - Piercing the Shroud
    # 126/127 - Whispers of Doom
    A_SINISTER_TURN_T = 128, "A Sinister Turn (Terran)", SC2Campaign.PROPHECY, "_2", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_a_sinister_turn", MissionFlag.Terran|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    A_SINISTER_TURN_Z = 129, "A Sinister Turn (Zerg)", SC2Campaign.PROPHECY, "_2", SC2Race.ZERG, MissionPools.MEDIUM, "ap_a_sinister_turn", MissionFlag.Zerg|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    ECHOES_OF_THE_FUTURE_T = 130, "Echoes of the Future (Terran)", SC2Campaign.PROPHECY, "_3", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_echoes_of_the_future", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.RaceSwap
    ECHOES_OF_THE_FUTURE_Z = 131, "Echoes of the Future (Zerg)", SC2Campaign.PROPHECY, "_3", SC2Race.ZERG, MissionPools.MEDIUM, "ap_echoes_of_the_future", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    IN_UTTER_DARKNESS_T = 132, "In Utter Darkness (Terran)", SC2Campaign.PROPHECY, "_4", SC2Race.TERRAN, MissionPools.HARD, "ap_in_utter_darkness", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    IN_UTTER_DARKNESS_Z = 133, "In Utter Darkness (Zerg)", SC2Campaign.PROPHECY, "_4", SC2Race.ZERG, MissionPools.HARD, "ap_in_utter_darkness", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    GATES_OF_HELL_Z = 134, "Gates of Hell (Zerg)", SC2Campaign.WOL, "Char", SC2Race.ZERG, MissionPools.HARD, "ap_gates_of_hell", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    GATES_OF_HELL_P = 135, "Gates of Hell (Protoss)", SC2Campaign.WOL, "Char", SC2Race.PROTOSS, MissionPools.HARD, "ap_gates_of_hell", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.RaceSwap
    # 136/137 - Belly of the Beast
    SHATTER_THE_SKY_Z = 138, "Shatter the Sky (Zerg)", SC2Campaign.WOL, "Char", SC2Race.ZERG, MissionPools.HARD, "ap_shatter_the_sky", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    SHATTER_THE_SKY_P = 139, "Shatter the Sky (Protoss)", SC2Campaign.WOL, "Char", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_shatter_the_sky", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.RaceSwap
    ALL_IN_Z = 140, "All-In (Zerg)", SC2Campaign.WOL, "Char", SC2Race.ZERG, MissionPools.VERY_HARD, "ap_all_in", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    ALL_IN_P = 141, "All-In (Protoss)", SC2Campaign.WOL, "Char", SC2Race.PROTOSS, MissionPools.VERY_HARD, "ap_all_in", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    LAB_RAT_T = 142, "Lab Rat (Terran)", SC2Campaign.HOTS, "Umoja", SC2Race.TERRAN, MissionPools.STARTER, "ap_lab_rat", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.RaceSwap
    LAB_RAT_P = 143, "Lab Rat (Protoss)", SC2Campaign.HOTS, "Umoja", SC2Race.PROTOSS, MissionPools.STARTER, "ap_lab_rat", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.RaceSwap
    # 144/145 - Back in the Saddle
    RENDEZVOUS_T = 146, "Rendezvous (Terran)", SC2Campaign.HOTS, "Umoja", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_rendezvous", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    RENDEZVOUS_P = 147, "Rendezvous (Protoss)", SC2Campaign.HOTS, "Umoja", SC2Race.PROTOSS, MissionPools.EASY, "ap_rendezvous", MissionFlag.Protoss|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    HARVEST_OF_SCREAMS_T = 148, "Harvest of Screams (Terran)", SC2Campaign.HOTS, "Kaldir", SC2Race.TERRAN, MissionPools.EASY, "ap_harvest_of_screams", MissionFlag.Terran|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    HARVEST_OF_SCREAMS_P = 149, "Harvest of Screams (Protoss)", SC2Campaign.HOTS, "Kaldir", SC2Race.PROTOSS, MissionPools.EASY, "ap_harvest_of_screams", MissionFlag.Protoss|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    SHOOT_THE_MESSENGER_T = 150, "Shoot the Messenger (Terran)", SC2Campaign.HOTS, "Kaldir", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_shoot_the_messenger", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    SHOOT_THE_MESSENGER_P = 151, "Shoot the Messenger (Protoss)", SC2Campaign.HOTS, "Kaldir", SC2Race.PROTOSS, MissionPools.EASY, "ap_shoot_the_messenger", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    # 152/153 - Enemy Within
    DOMINATION_T = 154, "Domination (Terran)", SC2Campaign.HOTS, "Char", SC2Race.TERRAN, MissionPools.EASY, "ap_domination", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsZerg|MissionFlag.RaceSwap
    DOMINATION_P = 155, "Domination (Protoss)", SC2Campaign.HOTS, "Char", SC2Race.PROTOSS, MissionPools.EASY, "ap_domination", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsZerg|MissionFlag.RaceSwap
    FIRE_IN_THE_SKY_T = 156, "Fire in the Sky (Terran)", SC2Campaign.HOTS, "Char", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_fire_in_the_sky", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.RaceSwap
    FIRE_IN_THE_SKY_P = 157, "Fire in the Sky (Protoss)", SC2Campaign.HOTS, "Char", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_fire_in_the_sky", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.RaceSwap
    OLD_SOLDIERS_T = 158, "Old Soldiers (Terran)", SC2Campaign.HOTS, "Char", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_old_soldiers", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.RaceSwap
    OLD_SOLDIERS_P = 159, "Old Soldiers (Protoss)", SC2Campaign.HOTS, "Char", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_old_soldiers", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.RaceSwap
    WAKING_THE_ANCIENT_T = 160, "Waking the Ancient (Terran)", SC2Campaign.HOTS, "Zerus", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_waking_the_ancient", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.RaceSwap
    WAKING_THE_ANCIENT_P = 161, "Waking the Ancient (Protoss)", SC2Campaign.HOTS, "Zerus", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_waking_the_ancient", MissionFlag.Protoss|MissionFlag.VsZerg|MissionFlag.RaceSwap
    THE_CRUCIBLE_T = 162, "The Crucible (Terran)", SC2Campaign.HOTS, "Zerus", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_crucible", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    THE_CRUCIBLE_P = 163, "The Crucible (Protoss)", SC2Campaign.HOTS, "Zerus", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_the_crucible", MissionFlag.Protoss|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    # 164/165 - Supreme
    INFESTED_T = 166, "Infested (Terran)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_infested", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.RaceSwap
    INFESTED_P = 167, "Infested (Protoss)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_infested", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.RaceSwap
    HAND_OF_DARKNESS_T = 168, "Hand of Darkness (Terran)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.TERRAN, MissionPools.HARD, "ap_hand_of_darkness", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.RaceSwap
    HAND_OF_DARKNESS_P = 169, "Hand of Darkness (Protoss)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.PROTOSS, MissionPools.HARD, "ap_hand_of_darkness", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.RaceSwap
    PHANTOMS_OF_THE_VOID_T = 170, "Phantoms of the Void (Terran)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_phantoms_of_the_void", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    PHANTOMS_OF_THE_VOID_P = 171, "Phantoms of the Void (Protoss)", SC2Campaign.HOTS, "Skygeirr Station", SC2Race.PROTOSS, MissionPools.MEDIUM, "ap_phantoms_of_the_void", MissionFlag.Protoss|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    # 172/173 - With Friends Like These
    # 174/175 - Conviction
    PLANETFALL_T = 176, "Planetfall (Terran)", SC2Campaign.HOTS, "Korhal", SC2Race.TERRAN, MissionPools.HARD, "ap_planetfall", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    PLANETFALL_P = 177, "Planetfall (Protoss)", SC2Campaign.HOTS, "Korhal", SC2Race.PROTOSS, MissionPools.HARD, "ap_planetfall", MissionFlag.Protoss|MissionFlag.AutoScroller|MissionFlag.VsTerran|MissionFlag.RaceSwap
    DEATH_FROM_ABOVE_T = 178, "Death From Above (Terran)", SC2Campaign.HOTS, "Korhal", SC2Race.TERRAN, MissionPools.HARD, "ap_death_from_above", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.RaceSwap
    DEATH_FROM_ABOVE_P = 179, "Death From Above (Protoss)", SC2Campaign.HOTS, "Korhal", SC2Race.PROTOSS, MissionPools.HARD, "ap_death_from_above", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.RaceSwap
    THE_RECKONING_T = 180, "The Reckoning (Terran)", SC2Campaign.HOTS, "Korhal", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_the_reckoning", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.RaceSwap
    THE_RECKONING_P = 181, "The Reckoning (Protoss)", SC2Campaign.HOTS, "Korhal", SC2Race.PROTOSS, MissionPools.VERY_HARD, "ap_the_reckoning", MissionFlag.Protoss|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.RaceSwap
    DARK_WHISPERS_T = 182, "Dark Whispers (Terran)", SC2Campaign.PROLOGUE, "_1", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_dark_whispers", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsTZ|MissionFlag.RaceSwap
    DARK_WHISPERS_Z = 183, "Dark Whispers (Zerg)", SC2Campaign.PROLOGUE, "_1", SC2Race.ZERG, MissionPools.MEDIUM, "ap_dark_whispers", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsTZ|MissionFlag.RaceSwap
    GHOSTS_IN_THE_FOG_T = 184, "Ghosts in the Fog (Terran)", SC2Campaign.PROLOGUE, "_2", SC2Race.TERRAN, MissionPools.HARD, "ap_ghosts_in_the_fog", MissionFlag.Terran|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    GHOSTS_IN_THE_FOG_Z = 185, "Ghosts in the Fog (Zerg)", SC2Campaign.PROLOGUE, "_2", SC2Race.ZERG, MissionPools.HARD, "ap_ghosts_in_the_fog", MissionFlag.Zerg|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    # 186/187 - Evil Awoken
    # 188/189 - For Aiur!
    THE_GROWING_SHADOW_T = 190, "The Growing Shadow (Terran)", SC2Campaign.LOTV, "Aiur", SC2Race.TERRAN, MissionPools.EASY, "ap_the_growing_shadow", MissionFlag.Terran|MissionFlag.VsPZ|MissionFlag.RaceSwap
    THE_GROWING_SHADOW_Z = 191, "The Growing Shadow (Zerg)", SC2Campaign.LOTV, "Aiur", SC2Race.ZERG, MissionPools.EASY, "ap_the_growing_shadow", MissionFlag.Zerg|MissionFlag.VsPZ|MissionFlag.RaceSwap
    THE_SPEAR_OF_ADUN_T = 192, "The Spear of Adun (Terran)", SC2Campaign.LOTV, "Aiur", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_the_spear_of_adun", MissionFlag.Terran|MissionFlag.VsPZ|MissionFlag.RaceSwap
    THE_SPEAR_OF_ADUN_Z = 193, "The Spear of Adun (Zerg)", SC2Campaign.LOTV, "Aiur", SC2Race.ZERG, MissionPools.MEDIUM, "ap_the_spear_of_adun", MissionFlag.Zerg|MissionFlag.VsPZ|MissionFlag.RaceSwap
    SKY_SHIELD_T = 194, "Sky Shield (Terran)", SC2Campaign.LOTV, "Korhal", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_sky_shield", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.RaceSwap
    SKY_SHIELD_Z = 195, "Sky Shield (Zerg)", SC2Campaign.LOTV, "Korhal", SC2Race.ZERG, MissionPools.MEDIUM, "ap_sky_shield", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.RaceSwap
    BROTHERS_IN_ARMS_T = 196, "Brothers in Arms (Terran)", SC2Campaign.LOTV, "Korhal", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_brothers_in_arms", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.RaceSwap
    BROTHERS_IN_ARMS_Z = 197, "Brothers in Arms (Zerg)", SC2Campaign.LOTV, "Korhal", SC2Race.ZERG, MissionPools.MEDIUM, "ap_brothers_in_arms", MissionFlag.Zerg|MissionFlag.VsTerran|MissionFlag.AiTerranAlly|MissionFlag.RaceSwap
    AMON_S_REACH_T = 198, "Amon's Reach (Terran)", SC2Campaign.LOTV, "Shakuras", SC2Race.TERRAN, MissionPools.MEDIUM, "ap_amon_s_reach", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.RaceSwap
    AMON_S_REACH_Z = 199, "Amon's Reach (Zerg)", SC2Campaign.LOTV, "Shakuras", SC2Race.ZERG, MissionPools.MEDIUM, "ap_amon_s_reach", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    LAST_STAND_T = 200, "Last Stand (Terran)", SC2Campaign.LOTV, "Shakuras", SC2Race.TERRAN, MissionPools.HARD, "ap_last_stand", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    LAST_STAND_Z = 201, "Last Stand (Zerg)", SC2Campaign.LOTV, "Shakuras", SC2Race.ZERG, MissionPools.HARD, "ap_last_stand", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsZerg|MissionFlag.RaceSwap
    FORBIDDEN_WEAPON_T = 202, "Forbidden Weapon (Terran)", SC2Campaign.LOTV, "Purifier", SC2Race.TERRAN, MissionPools.HARD, "ap_forbidden_weapon", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    FORBIDDEN_WEAPON_Z = 203, "Forbidden Weapon (Zerg)", SC2Campaign.LOTV, "Purifier", SC2Race.ZERG, MissionPools.HARD, "ap_forbidden_weapon", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    TEMPLE_OF_UNIFICATION_T = 204, "Temple of Unification (Terran)", SC2Campaign.LOTV, "Ulnar", SC2Race.TERRAN, MissionPools.HARD, "ap_temple_of_unification", MissionFlag.Terran|MissionFlag.VsTP|MissionFlag.RaceSwap
    TEMPLE_OF_UNIFICATION_Z = 205, "Temple of Unification (Zerg)", SC2Campaign.LOTV, "Ulnar", SC2Race.ZERG, MissionPools.HARD, "ap_temple_of_unification", MissionFlag.Zerg|MissionFlag.VsTP|MissionFlag.RaceSwap
    # 206/207 - The Infinite Cycle
    HARBINGER_OF_OBLIVION_T = 208, "Harbinger of Oblivion (Terran)", SC2Campaign.LOTV, "Ulnar", SC2Race.TERRAN, MissionPools.HARD, "ap_harbinger_of_oblivion", MissionFlag.Terran|MissionFlag.Countdown|MissionFlag.VsTP|MissionFlag.AiZergAlly|MissionFlag.RaceSwap
    HARBINGER_OF_OBLIVION_Z = 209, "Harbinger of Oblivion (Zerg)", SC2Campaign.LOTV, "Ulnar", SC2Race.ZERG, MissionPools.HARD, "ap_harbinger_of_oblivion", MissionFlag.Zerg|MissionFlag.Countdown|MissionFlag.VsTP|MissionFlag.AiZergAlly|MissionFlag.RaceSwap
    UNSEALING_THE_PAST_T = 210, "Unsealing the Past (Terran)", SC2Campaign.LOTV, "Purifier", SC2Race.TERRAN, MissionPools.HARD, "ap_unsealing_the_past", MissionFlag.Terran|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.RaceSwap
    UNSEALING_THE_PAST_Z = 211, "Unsealing the Past (Zerg)", SC2Campaign.LOTV, "Purifier", SC2Race.ZERG, MissionPools.HARD, "ap_unsealing_the_past", MissionFlag.Zerg|MissionFlag.AutoScroller|MissionFlag.VsZerg|MissionFlag.RaceSwap
    PURIFICATION_T = 212, "Purification (Terran)", SC2Campaign.LOTV, "Purifier", SC2Race.TERRAN, MissionPools.HARD, "ap_purification", MissionFlag.Terran|MissionFlag.VsZerg|MissionFlag.RaceSwap
    PURIFICATION_Z = 213, "Purification (Zerg)", SC2Campaign.LOTV, "Purifier", SC2Race.ZERG, MissionPools.HARD, "ap_purification", MissionFlag.Zerg|MissionFlag.VsZerg|MissionFlag.RaceSwap
    STEPS_OF_THE_RITE_T = 214, "Steps of the Rite (Terran)", SC2Campaign.LOTV, "Tal'darim", SC2Race.TERRAN, MissionPools.HARD, "ap_steps_of_the_rite", MissionFlag.Terran|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    STEPS_OF_THE_RITE_Z = 215, "Steps of the Rite (Zerg)", SC2Campaign.LOTV, "Tal'darim", SC2Race.ZERG, MissionPools.HARD, "ap_steps_of_the_rite", MissionFlag.Zerg|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    RAK_SHIR_T = 216, "Rak'Shir (Terran)", SC2Campaign.LOTV, "Tal'darim", SC2Race.TERRAN, MissionPools.HARD, "ap_rak_shir", MissionFlag.Terran|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    RAK_SHIR_Z = 217, "Rak'Shir (Zerg)", SC2Campaign.LOTV, "Tal'darim", SC2Race.ZERG, MissionPools.HARD, "ap_rak_shir", MissionFlag.Zerg|MissionFlag.VsProtoss|MissionFlag.RaceSwap
    TEMPLAR_S_CHARGE_T = 218, "Templar's Charge (Terran)", SC2Campaign.LOTV, "Moebius", SC2Race.TERRAN, MissionPools.HARD, "ap_templar_s_charge", MissionFlag.Terran|MissionFlag.VsTerran|MissionFlag.RaceSwap
    TEMPLAR_S_CHARGE_Z = 219, "Templar's Charge (Zerg)", SC2Campaign.LOTV, "Moebius", SC2Race.ZERG, MissionPools.HARD, "ap_templar_s_charge", MissionFlag.Zerg|MissionFlag.VsTerran|MissionFlag.RaceSwap
    # 220/221 - Templar's Return
    THE_HOST_T = 222, "The Host (Terran)", SC2Campaign.LOTV, "Return to Aiur", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_the_host", MissionFlag.Terran|MissionFlag.VsAll|MissionFlag.RaceSwap
    THE_HOST_Z = 223, "The Host (Zerg)", SC2Campaign.LOTV, "Return to Aiur", SC2Race.ZERG, MissionPools.VERY_HARD, "ap_the_host", MissionFlag.Zerg|MissionFlag.VsAll|MissionFlag.RaceSwap
    SALVATION_T = 224, "Salvation (Terran)", SC2Campaign.LOTV, "Return to Aiur", SC2Race.TERRAN, MissionPools.VERY_HARD, "ap_salvation", MissionFlag.Terran|MissionFlag.TimedDefense|MissionFlag.VsPZ|MissionFlag.AiProtossAlly|MissionFlag.RaceSwap
    SALVATION_Z = 225, "Salvation (Zerg)", SC2Campaign.LOTV, "Return to Aiur", SC2Race.ZERG, MissionPools.VERY_HARD, "ap_salvation", MissionFlag.Zerg|MissionFlag.TimedDefense|MissionFlag.VsPZ|MissionFlag.AiProtossAlly|MissionFlag.RaceSwap
    # 226/227 - Into the Void
    # 228/229 - The Essence of Eternity
    # 230/231 - Amon's Fall
    # 232/233 - The Escape
    # 234/235 - Sudden Strike
    # 236/237 - Enemy Intelligence
    # 238/239 - Trouble In Paradise
    # 240/241 - Night Terrors
    # 242/243 - Flashpoint
    # 244/245 - In the Enemy's Shadow
    # 246/247 - Dark Skies
    # 248/249 - End Game


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
    required_world: List[Union[MissionConnection, Dict[Literal["campaign", "connect_to"], int]]]
    category: str
    number: int = 0  # number of worlds need beaten
    completion_critical: bool = False  # missions needed to beat game
    or_requirements: bool = False  # true if the requirements should be or-ed instead of and-ed
    ui_vertical_padding: int = 0   # How many blank padding tiles go above this mission in the launcher



lookup_id_to_mission: Dict[int, SC2Mission] = {
    mission.id: mission for mission in SC2Mission
}

lookup_name_to_mission: Dict[str, SC2Mission] = {
    mission.mission_name: mission for mission in SC2Mission
}
for mission in SC2Mission:
    if MissionFlag.HasRaceSwap in mission.flags and ' (' in mission.mission_name:
        # Short names for non-race-swapped missions for client compatibility
        short_name = mission.get_short_name()
        lookup_name_to_mission[short_name] = mission

lookup_id_to_campaign: Dict[int, SC2Campaign] = {
    campaign.id: campaign for campaign in SC2Campaign
}


campaign_mission_table: Dict[SC2Campaign, Set[SC2Mission]] = {
    campaign: set() for campaign in SC2Campaign
}
for mission in SC2Mission:
    campaign_mission_table[mission.campaign].add(mission)


def get_campaign_difficulty(campaign: SC2Campaign, excluded_missions: Iterable[SC2Mission] = ()) -> MissionPools:
    """

    :param campaign:
    :param excluded_missions:
    :return: Campaign's the most difficult non-excluded mission
    """
    excluded_mission_set = set(excluded_missions)
    included_missions = campaign_mission_table[campaign].difference(excluded_mission_set)
    return max([mission.pool for mission in included_missions])


def get_campaign_goal_priority(campaign: SC2Campaign, excluded_missions: Iterable[SC2Mission] = ()) -> SC2CampaignGoalPriority:
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


class SC2CampaignGoal(NamedTuple):
    mission: SC2Mission
    location: str


campaign_final_mission_locations: Dict[SC2Campaign, Optional[SC2CampaignGoal]] = {
    SC2Campaign.WOL: SC2CampaignGoal(SC2Mission.ALL_IN, f'{SC2Mission.ALL_IN.mission_name}: Victory'),
    SC2Campaign.PROPHECY: SC2CampaignGoal(SC2Mission.IN_UTTER_DARKNESS, f'{SC2Mission.IN_UTTER_DARKNESS.mission_name}: Defeat'),
    SC2Campaign.HOTS: SC2CampaignGoal(SC2Mission.THE_RECKONING, f'{SC2Mission.THE_RECKONING.mission_name}: Victory'),
    SC2Campaign.PROLOGUE: SC2CampaignGoal(SC2Mission.EVIL_AWOKEN, f'{SC2Mission.EVIL_AWOKEN.mission_name}: Victory'),
    SC2Campaign.LOTV: SC2CampaignGoal(SC2Mission.SALVATION, f'{SC2Mission.SALVATION.mission_name}: Victory'),
    SC2Campaign.EPILOGUE: None,
    SC2Campaign.NCO: SC2CampaignGoal(SC2Mission.END_GAME, f'{SC2Mission.END_GAME.mission_name}: Victory'),
}

campaign_alt_final_mission_locations: Dict[SC2Campaign, Dict[SC2Mission, str]] = {
    SC2Campaign.WOL: {
        SC2Mission.MAW_OF_THE_VOID: f'{SC2Mission.MAW_OF_THE_VOID.mission_name}: Victory',
        SC2Mission.ENGINE_OF_DESTRUCTION: f'{SC2Mission.ENGINE_OF_DESTRUCTION.mission_name}: Victory',
        SC2Mission.SUPERNOVA: f'{SC2Mission.SUPERNOVA.mission_name}: Victory',
        SC2Mission.GATES_OF_HELL: f'{SC2Mission.GATES_OF_HELL.mission_name}: Victory',
        SC2Mission.SHATTER_THE_SKY: f'{SC2Mission.SHATTER_THE_SKY.mission_name}: Victory',

        SC2Mission.MAW_OF_THE_VOID_Z: f'{SC2Mission.MAW_OF_THE_VOID_Z.mission_name}: Victory',
        SC2Mission.ENGINE_OF_DESTRUCTION_Z: f'{SC2Mission.ENGINE_OF_DESTRUCTION_Z.mission_name}: Victory',
        SC2Mission.SUPERNOVA_Z: f'{SC2Mission.SUPERNOVA_Z.mission_name}: Victory',
        SC2Mission.GATES_OF_HELL_Z: f'{SC2Mission.GATES_OF_HELL_Z.mission_name}: Victory',
        SC2Mission.SHATTER_THE_SKY_Z: f'{SC2Mission.SHATTER_THE_SKY_Z.mission_name}: Victory',

        SC2Mission.MAW_OF_THE_VOID_P: f'{SC2Mission.MAW_OF_THE_VOID_P.mission_name}: Victory',
        SC2Mission.ENGINE_OF_DESTRUCTION_P: f'{SC2Mission.ENGINE_OF_DESTRUCTION_P.mission_name}: Victory',
        SC2Mission.SUPERNOVA_P: f'{SC2Mission.SUPERNOVA_P.mission_name}: Victory',
        SC2Mission.GATES_OF_HELL_P: f'{SC2Mission.GATES_OF_HELL_P.mission_name}: Victory',
        SC2Mission.SHATTER_THE_SKY_P: f'{SC2Mission.SHATTER_THE_SKY_P.mission_name}: Victory'
    },
    SC2Campaign.PROPHECY: {},
    SC2Campaign.HOTS: {
        SC2Mission.THE_CRUCIBLE: f'{SC2Mission.THE_CRUCIBLE.mission_name}: Victory',
        SC2Mission.HAND_OF_DARKNESS: f'{SC2Mission.HAND_OF_DARKNESS.mission_name}: Victory',
        SC2Mission.PHANTOMS_OF_THE_VOID: f'{SC2Mission.PHANTOMS_OF_THE_VOID.mission_name}: Victory',
        SC2Mission.PLANETFALL: f'{SC2Mission.PLANETFALL.mission_name}: Victory',
        SC2Mission.DEATH_FROM_ABOVE: f'{SC2Mission.DEATH_FROM_ABOVE.mission_name}: Victory',

        SC2Mission.THE_CRUCIBLE_T: f'{SC2Mission.THE_CRUCIBLE_T.mission_name}: Victory',
        SC2Mission.HAND_OF_DARKNESS_T: f'{SC2Mission.HAND_OF_DARKNESS_T.mission_name}: Victory',
        SC2Mission.PHANTOMS_OF_THE_VOID_T: f'{SC2Mission.PHANTOMS_OF_THE_VOID_T.mission_name}: Victory',
        SC2Mission.PLANETFALL_T: f'{SC2Mission.PLANETFALL_T.mission_name}: Victory',
        SC2Mission.DEATH_FROM_ABOVE_T: f'{SC2Mission.DEATH_FROM_ABOVE_T.mission_name}: Victory',

        SC2Mission.THE_CRUCIBLE_P: f'{SC2Mission.THE_CRUCIBLE_P.mission_name}: Victory',
        SC2Mission.HAND_OF_DARKNESS_P: f'{SC2Mission.HAND_OF_DARKNESS_P.mission_name}: Victory',
        SC2Mission.PHANTOMS_OF_THE_VOID_P: f'{SC2Mission.PHANTOMS_OF_THE_VOID_P.mission_name}: Victory',
        SC2Mission.PLANETFALL_P: f'{SC2Mission.PLANETFALL_P.mission_name}: Victory',
        SC2Mission.DEATH_FROM_ABOVE_P: f'{SC2Mission.DEATH_FROM_ABOVE_P.mission_name}: Victory'
    },
    SC2Campaign.PROLOGUE: {
        SC2Mission.GHOSTS_IN_THE_FOG: f'{SC2Mission.GHOSTS_IN_THE_FOG.mission_name}: Victory',
        SC2Mission.GHOSTS_IN_THE_FOG_T: f'{SC2Mission.GHOSTS_IN_THE_FOG_T.mission_name}: Victory',
        SC2Mission.GHOSTS_IN_THE_FOG_Z: f'{SC2Mission.GHOSTS_IN_THE_FOG_Z.mission_name}: Victory'
    },
    SC2Campaign.LOTV: {
        SC2Mission.THE_HOST: f'{SC2Mission.THE_HOST.mission_name}: Victory',
        SC2Mission.TEMPLAR_S_CHARGE: f'{SC2Mission.TEMPLAR_S_CHARGE.mission_name}: Victory',

        SC2Mission.THE_HOST_T: f'{SC2Mission.THE_HOST_T.mission_name}: Victory',
        SC2Mission.TEMPLAR_S_CHARGE_T: f'{SC2Mission.TEMPLAR_S_CHARGE_T.mission_name}: Victory',

        SC2Mission.THE_HOST_Z: f'{SC2Mission.THE_HOST_Z.mission_name}: Victory',
        SC2Mission.TEMPLAR_S_CHARGE_Z: f'{SC2Mission.TEMPLAR_S_CHARGE_Z.mission_name}: Victory'
    },
    SC2Campaign.EPILOGUE: {
        SC2Mission.AMON_S_FALL: f'{SC2Mission.AMON_S_FALL.mission_name}: Victory',
        SC2Mission.INTO_THE_VOID: f'{SC2Mission.INTO_THE_VOID.mission_name}: Victory',
        SC2Mission.THE_ESSENCE_OF_ETERNITY: f'{SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name}: Victory',
    },
    SC2Campaign.NCO: {
        SC2Mission.FLASHPOINT: f'{SC2Mission.FLASHPOINT.mission_name}: Victory',
        SC2Mission.DARK_SKIES: f'{SC2Mission.DARK_SKIES.mission_name}: Victory',
        SC2Mission.NIGHT_TERRORS: f'{SC2Mission.NIGHT_TERRORS.mission_name}: Victory',
        SC2Mission.TROUBLE_IN_PARADISE: f'{SC2Mission.TROUBLE_IN_PARADISE.mission_name}: Victory'
    }
}

campaign_race_exceptions: Dict[SC2Mission, SC2Race] = {
    SC2Mission.WITH_FRIENDS_LIKE_THESE: SC2Race.TERRAN
}


def get_goal_location(mission: SC2Mission) -> Union[str, None]:
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
    if mission in campaign_alt_goals:
        return campaign_alt_goals.get(mission)

    return (mission.mission_name + ": Defeat") \
        if mission in [SC2Mission.IN_UTTER_DARKNESS, SC2Mission.IN_UTTER_DARKNESS_T, SC2Mission.IN_UTTER_DARKNESS_Z] \
        else mission.mission_name + ": Victory"


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
    if alt_goal_locations:
        for mission in alt_goal_locations.keys():
            missions.append(mission)

    return missions


def get_missions_with_any_flags_in_list(flags: MissionFlag) -> List[SC2Mission]:
    return [mission for mission in SC2Mission if flags & mission.flags]

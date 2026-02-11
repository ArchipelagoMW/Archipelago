"""
A list of Constant Vars used by the APWorld.
Can be used by multiple worlds in a generation (no instance vars allowed here)
"""
from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import TYPE_CHECKING
import BaseClasses

if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld


#from .sanity import *
#from .sanitykey import *


class RejectDictionaryReturnToMonke(dict):
    """
    This is an awful idea.
    """
    def __setitem__(self, key, value):
        try:
            self.__getitem__(key)
            #if value != self.__getitem__(key):
            raise ValueError(f"Key ({key}: {self.__getitem__(key)}) is already present in dictionary. New Value: {value}")
            #else:
                #return super(RejectDictionaryReturnToMonke, self).__setitem__(key, value)
        except KeyError:
            return super(RejectDictionaryReturnToMonke, self).__setitem__(key, value)


@dataclass
class ItemData:
    """
    Holds information about an item.
    ID, Name, Classification, Amount, Fillerweight
    """
    code: int
    name: str
    classification: BaseClasses.ItemClassification = BaseClasses.ItemClassification.useful
    amount: int = 1
    fillerweight: int = 50


"""
@dataclass
class LocationData:
    #optionNeeded: str
    #consider list of str for multiple
    #optionValue: set[int]
    #consider list of set[int] for multiple
    name: str
    code: int
    team: str
    level: str
    region: str
    rule: CollectionState
    rulestr: str

    def __lt__(self, other):
        return self.code < other.code


@dataclass
class EntranceData:
    name: str
    sourceReg: str
    targetReg: str
    rule: CollectionState = None


@dataclass
class RegionData:
    name: str
    numberofObjChecks: int
"""


@dataclass
class RegionCSVData:
    """
    Holds information about a region.
    Team, Level, Name, ObjChecks
    """
    team: str
    level: str
    name: str
    objchecks: int


@dataclass
class ConnectionCSVData:
    """
    Holds information about a connection.
    A Connection connects 2 Regions together one-way (source and target)
    Name, Team, Level, Source, Target, rulestr
    """
    name: str
    team: str
    level: str
    source: str
    target: str
    #rule: CollectionState
    rulestr: str


@dataclass
class LocationCSVData:
    """
    Holds information about a location.
    Name, Code (ID), Team, Level, Act, Region, rulestr, loc_type, hint_info, notes
    """
    name: str
    code: int
    team: str
    level: str
    act: int
    region: str
    rulestr: str
    #rule: CollectionState
    loc_type: str
    hint_info: str
    notes: str

    def __lt__(self, other):
        return self.code < other.code

    def __repr__(self):
        return f"<{self.name} 0x{self.code:x} {self.team} {self.level} {self.act} {self.region} {self.rulestr} {self.loc_type} {self.hint_info} {self.notes}>"


#class StrConst:
SONICHEROES: str = "Sonic Heroes"
PARTYTIMETHEME: str = "partyTime"
AND: str = "And"

TUTORIALNAME: str = "Multiworld Setup Guide"
TUTORIALDESC: str = ("A guide to setting up the Sonic Heroes "
                     "randomizer connected to an Archipelago Multiworld.")
TUTORIALLANGUAGE: str = "English"
TUTORIALFILENAME: str = "setup_en.md"
TUTORIALLINK: str = "setup/en"
TUTORIALAUTHORS: list[str] = ["EthicalLogic"]

SONIC: str = "Sonic"
DARK: str = "Dark"
ROSE: str = "Rose"
CHAOTIX: str = "Chaotix"
SUPERHARDMODE: str = "Super Hard Mode"

ANYTEAM: str = "Any Team"

SPEED: str = "Speed"
FLYING: str = "Flying"
POWER: str = "Power"
PROGRESSIVE: str = "Progressive"
PROGRESSIVELEVELUP: str = f"{PROGRESSIVE} Level-Up"
TWOCHARACTERS: str = "2 Characters"
THREECHARACTERS: str = "3 Characters"

PLAYABLE: str = "Playable"
CHARACTER: str = "Character"
CHARSONIC: str = "Sonic"
CHARTAILS: str = "Tails"
CHARKNUCKLES: str = "Knuckles"
CHARSHADOW: str = "Shadow"
CHARROUGE: str = "Rouge"
CHAROMEGA: str = "Omega"
CHARAMY: str = "Amy"
CHARCREAM: str = "Cream"
CHARBIG: str = "Big"
CHARESPIO: str = "Espio"
CHARCHARMY: str = "Charmy"
CHARVECTOR: str = "Vector"
CHARSUPERHARDSONIC: str = f"{SUPERHARDMODE} Sonic"
CHARSUPERHARDTAILS: str = f"{SUPERHARDMODE} Tails"
CHARSUPERHARDKNUCKLES: str = f"{SUPERHARDMODE} Knuckles"

SEASIDEHILL: str = "Seaside Hill"
OCEANPALACE: str = "Ocean Palace"
GRANDMETROPOLIS: str = "Grand Metropolis"
POWERPLANT: str = "Power Plant"
CASINOPARK: str = "Casino Park"
BINGOHIGHWAY: str = "Bingo Highway"
RAILCANYON: str = "Rail Canyon"
BULLETSTATION: str = "Bullet Station"
FROGFOREST: str = "Frog Forest"
LOSTJUNGLE: str = "Lost Jungle"
HANGCASTLE: str = "Hang Castle"
MYSTICMANSION: str = "Mystic Mansion"
EGGFLEET: str = "Egg Fleet"
FINALFORTRESS: str = "Final Fortress"
EGGHAWK: str = "Egg Hawk"
TEAMFIGHT1: str = "Team Fight 1"
ROBOTCARNIVAL: str = "Robot Carnival"
EGGALBATROSS: str = "Egg Albatross"
TEAMFIGHT2: str = "Team Fight 2"
ROBOTSTORM: str = "Robot Storm"
EGGEMPEROR: str = "Egg Emperor"
METALMADNESS: str = "Metal Madness"
METALOVERLORD: str = "Metal Overlord"



bonus_keys_per_team_level: dict[str, dict[str, tuple[int, int]]] = \
{
    SONIC:
        {
            SEASIDEHILL: (3, 3),
            OCEANPALACE: (3, 3),
            GRANDMETROPOLIS: (2, 3),
            POWERPLANT: (3, 3),
            CASINOPARK: (3, 3),
            BINGOHIGHWAY: (3, 3),
            RAILCANYON: (3, 3),
            BULLETSTATION: (3, 3),
            FROGFOREST: (3, 3),
            LOSTJUNGLE: (3, 3),
            HANGCASTLE: (3, 3),
            MYSTICMANSION: (3, 3),
            EGGFLEET: (3, 3),
            FINALFORTRESS: (3, 3),
        },
    DARK:
        {
            SEASIDEHILL: (3, 3),
            OCEANPALACE: (3, 3),
            GRANDMETROPOLIS: (3, 3),
            POWERPLANT: (3, 3),
            CASINOPARK: (3, 3),
            BINGOHIGHWAY: (3, 3),
            RAILCANYON: (3, 3),
            BULLETSTATION: (3, 3),
            FROGFOREST: (3, 3),
            LOSTJUNGLE: (3, 3),
            HANGCASTLE: (3, 3),
            MYSTICMANSION: (3, 3),
            EGGFLEET: (3, 3),
            FINALFORTRESS: (3, 3),
        },
    ROSE:
        {
            SEASIDEHILL: (2, 2),
            OCEANPALACE: (3, 3),
            GRANDMETROPOLIS: (3, 3),
            POWERPLANT: (3, 3),
            CASINOPARK: (3, 3), #super secret hidden
            BINGOHIGHWAY: (3, 3),
            RAILCANYON: (3, 3),
            BULLETSTATION: (3, 3),
            FROGFOREST: (3, 3),
            LOSTJUNGLE: (3, 3),
            HANGCASTLE: (3, 3),
            MYSTICMANSION: (3, 3),
            EGGFLEET: (3, 3),
            FINALFORTRESS: (3, 3),
        },
    CHAOTIX:
        {
            SEASIDEHILL: (3, 3),
            OCEANPALACE: (3, 3),
            GRANDMETROPOLIS: (3, 3),
            POWERPLANT: (3, 3),
            CASINOPARK: (3, 3),
            BINGOHIGHWAY: (3, 3),
            RAILCANYON: (2, 2),
            BULLETSTATION: (3, 3),
            FROGFOREST: (3, 3),
            LOSTJUNGLE: (3, 3),
            HANGCASTLE: (3, 3),
            MYSTICMANSION: (3, 3),
            EGGFLEET: (3, 3),
            FINALFORTRESS: (3, 3),
        },
    SUPERHARDMODE:
        {
            SEASIDEHILL: (0, 0),
            OCEANPALACE: (0, 0),
            GRANDMETROPOLIS: (0, 0),
            POWERPLANT: (0, 0),
            CASINOPARK: (0, 0),
            BINGOHIGHWAY: (0, 0),
            RAILCANYON: (0, 0),
            BULLETSTATION: (0, 0),
            FROGFOREST: (0, 0),
            LOSTJUNGLE: (0, 0),
            HANGCASTLE: (0, 0),
            MYSTICMANSION: (0, 0),
            EGGFLEET: (0, 0),
            FINALFORTRESS: (0, 0),
        },
}
"""
number of bonus keys in specific team and level
has a tuple with first value being normal and second being with secret locations
"""

checkpoints_per_team_level: dict[str, dict[str, tuple[int, int]]] = \
{
    SONIC:
        {
            SEASIDEHILL: (5, 5),
            OCEANPALACE: (4, 4),
            GRANDMETROPOLIS: (4, 5),
            POWERPLANT: (4, 4),
            CASINOPARK: (3, 3),
            BINGOHIGHWAY: (4, 4),
            RAILCANYON: (6, 6),
            BULLETSTATION: (4, 4),
            FROGFOREST: (3, 3),
            LOSTJUNGLE: (5, 5),
            HANGCASTLE: (3, 3),
            MYSTICMANSION: (4, 4),
            EGGFLEET: (5, 5),
            FINALFORTRESS: (3, 3),
        },
    DARK:
        {
            SEASIDEHILL: (4, 4),
            OCEANPALACE: (5, 5),
            GRANDMETROPOLIS: (4, 4),
            POWERPLANT: (4, 4),
            CASINOPARK: (3, 3),
            BINGOHIGHWAY: (4, 4),
            RAILCANYON: (6, 6),
            BULLETSTATION: (5, 5),
            FROGFOREST: (3, 3),
            LOSTJUNGLE: (5, 5),
            HANGCASTLE: (3, 3),
            MYSTICMANSION: (4, 4),
            EGGFLEET: (5, 5),
            FINALFORTRESS: (3, 3),
        },
    ROSE:
        {
            SEASIDEHILL: (2, 2),
            OCEANPALACE: (2, 2),
            GRANDMETROPOLIS: (3, 3),
            POWERPLANT: (2, 2),
            CASINOPARK: (1, 1), #super secret hidden
            BINGOHIGHWAY: (3, 3),
            RAILCANYON: (4, 4),
            BULLETSTATION: (2, 2),
            FROGFOREST: (2, 2),
            LOSTJUNGLE: (2, 2),
            HANGCASTLE: (2, 2),
            MYSTICMANSION: (2, 2),
            EGGFLEET: (3, 3),
            FINALFORTRESS: (2, 2),
        },
    CHAOTIX:
        {
            SEASIDEHILL: (4, 4),
            OCEANPALACE: (2, 2),
            GRANDMETROPOLIS: (4, 4),
            POWERPLANT: (3, 3),
            CASINOPARK: (3, 3),
            BINGOHIGHWAY: (2, 2),
            RAILCANYON: (5, 5),
            BULLETSTATION: (4, 4),
            FROGFOREST: (3, 3),
            LOSTJUNGLE: (2, 2),
            HANGCASTLE: (2, 2),
            MYSTICMANSION: (4, 4),
            EGGFLEET: (4, 4),
            FINALFORTRESS: (3, 3),
        },
    SUPERHARDMODE:
        {
            SEASIDEHILL: (4, 4),
            OCEANPALACE: (5, 5),
            GRANDMETROPOLIS: (4, 4),
            POWERPLANT: (4, 4),
            CASINOPARK: (3, 3),
            BINGOHIGHWAY: (4, 4),
            RAILCANYON: (6, 6),
            BULLETSTATION: (4, 4),
            FROGFOREST: (3, 3),
            LOSTJUNGLE: (5, 5),
            HANGCASTLE: (3, 3),
            MYSTICMANSION: (5, 5),
            EGGFLEET: (5, 5),
            FINALFORTRESS: (3, 3),
        },
}
"""
number of checkpoints in specific team and level
has a tuple with first value being normal and second being with secret locations
"""


chaotix_obj_sanity_checks_per_level_act: dict[str, tuple[int, int]] = \
{
    SEASIDEHILL: (5, 10),
    OCEANPALACE: (0, 0),
    GRANDMETROPOLIS: (85, 85),
    POWERPLANT: (3, 5),
    CASINOPARK: (200, 500),
    BINGOHIGHWAY: (10, 20),
    RAILCANYON: (0, 0),
    BULLETSTATION: (30, 50),
    FROGFOREST: (3, 10),
    LOSTJUNGLE: (10, 20),
    HANGCASTLE: (10, 10),
    MYSTICMANSION: (60, 46),
    EGGFLEET: (0, 0),
    FINALFORTRESS: (5, 10),
}
"""
number of sanity checks for the specific Chaotix level
has a tuple with first value being Act A and the second being Act B
"""



BONUSSTAGE: str = "Bonus Stage"
EMERALDSTAGE: str = "Emerald Stage"
SEASIDEHILLBONUSSTAGE: str = f"{SEASIDEHILL} {BONUSSTAGE}"
OCEANPALACEEMERALDSTAGE: str = f"{OCEANPALACE} {EMERALDSTAGE}"
GRANDMETROPOLISBONUSSTAGE: str = f"{GRANDMETROPOLIS} {BONUSSTAGE}"
POWERPLANTEMERALDSTAGE: str = f"{POWERPLANT} {EMERALDSTAGE}"
CASINOPARKBONUSSTAGE: str = f"{CASINOPARK} {BONUSSTAGE}"
BINGOHIGHWAYEMERALDSTAGE: str = f"{BINGOHIGHWAY} {EMERALDSTAGE}"
RAILCANYONBONUSSTAGE: str = f"{RAILCANYON} {BONUSSTAGE}"
BULLETSTATIONEMERALDSTAGE: str = f"{BULLETSTATION} {EMERALDSTAGE}"
FROGFORESTBONUSSTAGE: str = f"{FROGFOREST} {BONUSSTAGE}"
LOSTJUNGLEEMERALDSTAGE: str = f"{LOSTJUNGLE} {EMERALDSTAGE}"
HANGCASTLEBONUSSTAGE: str = f"{HANGCASTLE} {BONUSSTAGE}"
MYSTICMANSIONEMERALDSTAGE: str = f"{MYSTICMANSION} {EMERALDSTAGE}"
EGGFLEETBONUSSTAGE: str = f"{EGGFLEET} {BONUSSTAGE}"
FINALFORTRESSEMERALDSTAGE: str = f"{FINALFORTRESS} {EMERALDSTAGE}"

bonus_and_emerald_stages: list[str] = \
[
    SEASIDEHILLBONUSSTAGE,
    OCEANPALACEEMERALDSTAGE,
    GRANDMETROPOLISBONUSSTAGE,
    POWERPLANTEMERALDSTAGE,
    CASINOPARKBONUSSTAGE,
    BINGOHIGHWAYEMERALDSTAGE,
    RAILCANYONBONUSSTAGE,
    BULLETSTATIONEMERALDSTAGE,
    FROGFORESTBONUSSTAGE,
    LOSTJUNGLEEMERALDSTAGE,
    HANGCASTLEBONUSSTAGE,
    MYSTICMANSIONEMERALDSTAGE,
    EGGFLEETBONUSSTAGE,
    FINALFORTRESSEMERALDSTAGE,
]

emerald_levels: list[str] = \
[
    OCEANPALACE,
    POWERPLANT,
    BINGOHIGHWAY,
    BULLETSTATION,
    LOSTJUNGLE,
    MYSTICMANSION,
    FINALFORTRESS,
]

bonus_emerald_stage_to_level: dict[str, str] = \
{
    SEASIDEHILLBONUSSTAGE: SEASIDEHILL,
    OCEANPALACEEMERALDSTAGE: OCEANPALACE,
    GRANDMETROPOLISBONUSSTAGE: GRANDMETROPOLIS,
    POWERPLANTEMERALDSTAGE: POWERPLANT,
    CASINOPARKBONUSSTAGE: CASINOPARK,
    BINGOHIGHWAYEMERALDSTAGE: BINGOHIGHWAY,
    RAILCANYONBONUSSTAGE: RAILCANYON,
    BULLETSTATIONEMERALDSTAGE: BULLETSTATION,
    FROGFORESTBONUSSTAGE: FROGFOREST,
    LOSTJUNGLEEMERALDSTAGE: LOSTJUNGLE,
    HANGCASTLEBONUSSTAGE: HANGCASTLE,
    MYSTICMANSIONEMERALDSTAGE: MYSTICMANSION,
    EGGFLEETBONUSSTAGE: EGGFLEET,
    FINALFORTRESSEMERALDSTAGE: FINALFORTRESS,
}



OCEANREGION: str = "Ocean Region"
HOTPLANTREGION: str = "HotPlant Region"
CASINOREGION: str = "Casino Region"
TRAINREGION: str = "Train Region"
BIGPLANTREGION: str = "BigPlant Region"
GHOSTREGION: str = "Ghost Region"
SKYREGION: str = "Sky Region"
SPECIALSTAGEREGION: str = "Special Stage Region"
BOSSREGION: str = "Boss Region"
FINALBOSSREGION: str = "Final Boss Region"

EMBLEM: str = "Emblem"
GREEN: str = "Green"
BLUE: str = "Blue"
YELLOW: str = "Yellow"
WHITE: str = "White"
CYAN: str = "Cyan"
PURPLE: str = "Purple"
RED: str = "Red"
CHAOSEMERALD: str = "Chaos Emerald"
GREENCHAOSEMERALD: str = f"{GREEN} {CHAOSEMERALD}"
BLUECHAOSEMERALD: str = f"{BLUE} {CHAOSEMERALD}"
YELLOWCHAOSEMERALD: str = f"{YELLOW} {CHAOSEMERALD}"
WHITECHAOSEMERALD: str = f"{WHITE} {CHAOSEMERALD}"
CYANCHAOSEMERALD: str = f"{CYAN} {CHAOSEMERALD}"
PURPLECHAOSEMERALD: str = f"{PURPLE} {CHAOSEMERALD}"
REDCHAOSEMERALD: str = f"{RED} {CHAOSEMERALD}"




EMBLEMS: str = "Emblems"
EMERALDS: str = "Emeralds"
LEVELCOMPLETIONSALLTEAMS: str = "Level Completions All Teams"
UNIQUELEVELCCOMPLETIONS: str = "Unique Level Completions"
LEVELCOMPLETIONSPERSTORY: str = "Level Completions Per Story"

goal_unlock_options: list[str] = \
[
    EMBLEMS,
    EMERALDS,
    LEVELCOMPLETIONSALLTEAMS,
    #UNIQUELEVELCCOMPLETIONS,
    LEVELCOMPLETIONSPERSTORY,
]


SONICACTA: str = "Sonic Act A"
SONICACTB: str = "Sonic Act B"
SONICKEYSANITY1SET: str = "Sonic KeySanity 1 Set"
SONICKEYSANITYBOTHACTS: str = "Sonic KeySanity Both Acts"
SONICCHECKPOINTSANITY1SET: str = "Sonic CheckpointSanity 1 Set"
SONICCHECKPOINTSANITYBOTHACTS: str = "Sonic CheckpointSanity Both Acts"

DARKACTA: str = "Dark Act A"
DARKACTB: str = "Dark Act B"
DARKOBJSANITY: str = "Dark ObjSanity"
DARKKEYSANITY1SET: str = "Dark KeySanity 1 Set"
DARKKEYSANITYBOTHACTS: str = "Dark KeySanity Both Acts"
DARKCHECKPOINTSANITY1SET: str = "Dark CheckpointSanity 1 Set"
DARKCHECKPOINTSANITYBOTHACTS: str = "Dark CheckpointSanity Both Acts"

ROSEACTA: str = "Rose Act A"
ROSEACTB: str = "Rose Act B"
ROSEOBJSANITY: str = "Rose ObjSanity"
ROSEKEYSANITY1SET: str = "Rose KeySanity 1 Set"
ROSEKEYSANITYBOTHACTS: str = "Rose KeySanity Both Acts"
ROSECHECKPOINTSANITY1SET: str = "Rose CheckpointSanity 1 Set"
ROSECHECKPOINTSANITYBOTHACTS: str = "Rose CheckpointSanity Both Acts"

CHAOTIXACTA: str = "Chaotix Act A"
CHAOTIXACTB: str = "Chaotix Act B"
CHAOTIXOBJSANITY: str = "Chaotix ObjSanity"
CHAOTIXKEYSANITY1SET: str = "Chaotix KeySanity 1 Set"
CHAOTIXKEYSANITYBOTHACTS: str = "Chaotix KeySanity Both Acts"
CHAOTIXCHECKPOINTSANITY1SET: str = "Chaotix CheckpointSanity 1 Set"
CHAOTIXCHECKPOINTSANITYBOTHACTS: str = "Chaotix CheckpointSanity Both Acts"

#SUPERHARDMODE: str = "Super Hard Mode"
SUPERHARDCHECKPOINTSANITY: str = "Super Hard CheckpointSanity"


features_in_rando: list[str] = \
[
    SONICACTA,
    SONICACTB,
    SONICKEYSANITY1SET,
    SONICKEYSANITYBOTHACTS,
    SONICCHECKPOINTSANITY1SET,
    SONICCHECKPOINTSANITYBOTHACTS,

    DARKACTA,
    DARKACTB,
    DARKOBJSANITY,
    DARKKEYSANITY1SET,
    DARKKEYSANITYBOTHACTS,
    DARKCHECKPOINTSANITY1SET,
    DARKCHECKPOINTSANITYBOTHACTS,

    ROSEACTA,
    ROSEACTB,
    ROSEOBJSANITY,
    ROSEKEYSANITY1SET,
    ROSEKEYSANITYBOTHACTS,
    ROSECHECKPOINTSANITY1SET,
    ROSECHECKPOINTSANITYBOTHACTS,

    CHAOTIXACTA,
    CHAOTIXACTB,
    CHAOTIXOBJSANITY,
    CHAOTIXKEYSANITY1SET,
    CHAOTIXKEYSANITYBOTHACTS,
    CHAOTIXCHECKPOINTSANITY1SET,
    CHAOTIXCHECKPOINTSANITYBOTHACTS,

    SUPERHARDMODE,
    SUPERHARDCHECKPOINTSANITY,
]

features_in_rando_default: list[str] = \
[
    SONICACTA,
    SONICKEYSANITY1SET,
    SONICCHECKPOINTSANITY1SET,
]

features_in_rando_story_options: list[str] = \
[
    SONICACTA,
    SONICACTB,
    DARKACTA,
    DARKACTB,
    ROSEACTA,
    ROSEACTB,
    CHAOTIXACTA,
    CHAOTIXACTB,
    SUPERHARDMODE,
]



emeralds: list[str] = \
[
    GREENCHAOSEMERALD,
    BLUECHAOSEMERALD,
    YELLOWCHAOSEMERALD,
    WHITECHAOSEMERALD,
    CYANCHAOSEMERALD,
    PURPLECHAOSEMERALD,
    REDCHAOSEMERALD,
]

#CHECKPOINT: str = "Checkpoint" <- defined below
#BONUSKEY: str = "Bonus Key" <- defined below


PLAYABLESONIC: str = f"{PLAYABLE} {CHARSONIC}"
PLAYABLETAILS: str = f"{PLAYABLE} {CHARTAILS}"
PLAYABLEKNUCKLES: str = f"{PLAYABLE} {CHARKNUCKLES}"
PLAYABLESHADOW: str = f"{PLAYABLE} {CHARSHADOW}"
PLAYABLEROUGE: str = f"{PLAYABLE} {CHARROUGE}"
PLAYABLEOMEGA: str = f"{PLAYABLE} {CHAROMEGA}"
PLAYABLEAMY: str = f"{PLAYABLE} {CHARAMY}"
PLAYABLECREAM: str = f"{PLAYABLE} {CHARCREAM}"
PLAYABLEBIG: str = f"{PLAYABLE} {CHARBIG}"
PLAYABLEESPIO: str = f"{PLAYABLE} {CHARESPIO}"
PLAYABLECHARMY: str = f"{PLAYABLE} {CHARCHARMY}"
PLAYABLEVECTOR: str = f"{PLAYABLE} {CHARVECTOR}"
PLAYABLESUPERHARDSONIC: str = f"{PLAYABLE} {CHARSUPERHARDSONIC}"
PLAYABLESUPERHARDTAILS: str = f"{PLAYABLE} {CHARSUPERHARDTAILS}"
PLAYABLESUPERHARDKNUCKLES: str = f"{PLAYABLE} {CHARSUPERHARDKNUCKLES}"

FILLER: str = "Filler"
EXTRALIFE: str = "Extra Life"
RINGS5: str = "5 Ring Bundle"
RINGS10: str = "10 Ring Bundle"
RINGS20: str = "20 Ring Bundle"
SHIELD: str = "Shield"
INVINCIBILITY: str = "Invincibility"
SPEEDLEVELUP: str = "Speed Level Up"
POWERLEVELUP: str = "Power Level Up"
FLYINGLEVELUP: str = "Flying Level Up"
TEAMLEVELUP: str = "Team Level Up"
TEAMBLASTREFILL: str = "Team Blast Refill"

TRAP: str = "Trap"
STEALTHTRAP: str = "Stealth Trap"
FREEZETRAP: str = "Freeze Trap"
NOSWAPTRAP: str = "No Swap Trap"
RINGTRAP: str = "Ring Trap"
CHARMYTRAP: str = "Charmy Trap"

MENU: str = "Menu"
MENUREGIONHINT: str = "This is Menu Region"
METALMADNESSREGIONHINT: str = "This is Metal Madness Region"
VICTORY: str = "Victory"
VICTORYITEM: str = f"{VICTORY} Item"
VICTORYLOCATION: str = f"{VICTORY} Location"

GOALUNLOCKITEM: str = "Goal Unlock Item"
COMPLETIONEVENT: str = "Completion Event"

ABILITY: str = "Ability"
NOTHING: str = "Nothing"
AMYHAMMERHOVER: str = "Amy Hammer Hover"
HOMINGATTACK: str = "Homing Attack"
TORNADO: str = "Tornado"
ROCKETACCEL: str = "Rocket Accel"
LIGHTDASH: str = "Light Dash"
TRIANGLEJUMP: str = "Triangle Jump"
LIGHTATTACK: str = "Light Attack"
INVISIBILITY: str = "Invisibility"
SHURIKEN: str = "Shuriken"

DUMMYRINGS: str = "Dummy Rings"
CHEESECANNON: str = "Cheese Cannon"
THUNDERSHOOT: str = "Thunder Shoot"
FLIGHT: str = "Flight"
FLOWERSTING: str = "Flower Sting"
FLYINGCHARACTERSPECIALMOVE: str = "Flying Character Special Move"

POWERATTACK: str = "Power Attack"
BREAK: str = "Break"
BELLYFLOP: str = "Belly Flop"
BREAKKEYCAGE: str = "Break Key Cage"
FIREDUNK: str = "Fire Dunk"
SLAM: str = "Slam"
ULTIMATEFIREDUNK: str = "Ultimate Fire Dunk"
#SLAM: str = "Slam"
GLIDE: str = "Glide"
TRIANGLEDIVE: str = "Triangle Dive"
COMBOFINISHER: str = "Combo Finisher"

ALLABILITIES: str = "All Abilities"

TEAMBLAST: str = "Team Blast"
GROUNDENEMY: str = "Ground Enemy"

SECRET: str = "Secret"
#NORMAL: str = "Normal"
#LEVEL: str = "Level"
BOSS: str = "Boss"
EMERALD: str = "Emerald"
EMERALDLOCATION: str = "Emerald Location"
OBJSANITY: str = "ObjSanity"
KEYSANITY: str = "KeySanity"
CHECKPOINTSANITY: str = "CheckpointSanity"

LOCATION: str = "Location"
LOCATIONS: str = "Locations"
SECRETLOCATIONS: str = f"{SECRET} {LOCATIONS}"
REGION: str = "Region"
REGIONS: str = "Regions"
ALLREGIONS: str = ""
CONNECTION: str = "Connection"
CONNECTIONS: str = "Connections"
SECRETREGION: str = f"{SECRET} {REGION}"
SECRETCONNECTION: str = f"{SECRET} {CONNECTION}"

TEAM: str = "Team"
LEVEL: str = "Level"
NAME: str = "Name"
CODE: str = "Code"
RULE: str = "Rule"
ACT: str = "Act"
SOURCE: str = "Source"
TARGET: str = "Target"
NOTES: str = "Notes"
OBJCHECKS: str = "ObjChecks"
LOCATIONTYPE: str = "Location Type"
HINTINFO: str = "Hint Info"


STAGEOBJECT: str = "Stage Object"
ALLSTAGEOBJS: str = "All Stage Objects"
SINGLESPRING: str = "Single Spring"
TRIPLESPRING: str = "Triple Spring"
RINGS: str = "Rings"
HINTRING: str = "Hint Ring"
REGULARSWITCH: str = "Regular Switch"
PUSHANDPULLSWITCH: str = "Push And Pull Switch"
TARGETSWITCH: str = "Target Switch"
DASHPANEL: str = "Dash Panel"
DASHRING: str = "Dash Ring"
RAINBOWHOOPS: str = "Rainbow Hoops"
CHECKPOINT: str = "Checkpoint"
DASHRAMP: str = "Dash Ramp"
CANNON: str = "Cannon"
REGULARWEIGHT: str = "Regular Weight"
BREAKABLEWEIGHT: str = "Breakable Weight"
ITEMBOX: str = "Item Box"
ITEMBALLOON: str = "Item Balloon"
GOALRING: str = "Goal Ring"
PULLEY: str = "Pulley"
WOODCONTAINER: str = "Wood Container"
IRONCONTAINER: str = "Iron Container"
UNBREAKABLECONTAINER: str = "Unbreakable Container"
LOSTCHAO: str = "Lost Chao"
PROPELLER: str = "Propeller"
POLE: str = "Pole"
GONG: str = "Gong"
FAN: str = "Fan"
WARPFLOWER: str = "Warpflower"
BONUSKEY: str = "Bonus Key"
TELEPORTTRIGGER: str = "Teleport Trigger"
CEMENTBLOCKONRAILS: str = "Cement Block On Rails"
CEMENTSLIDINGBLOCK: str = "Cement Sliding Block"
CEMENTBLOCK: str = "Cement Block"
MOVINGRUINPLATFORM: str = "Moving Ruin Platform"
HERMITCRAB: str = "Hermit Crab"
SMALLSTONEPLATFORM: str = "Small Stone Platform"
CRUMBLINGSTONEPILLAR: str = "Crumbling Stone Pillar"
ENERGYROADSECTION: str = "Energy Road Section"
FALLINGDRAWBRIDGE: str = "Falling Drawbridge"
TILTINGBRIDGE: str = "Tilting Bridge"
BLIMPPLATFORM: str = "Blimp Platform"
ENERGYROADSPEEDEFFECT: str = "Energy Road Speed Effect"
ENERGYROADUPWARDSECTION: str = "Energy Road Upward Section"
ENERGYCOLUMN: str = "Energy Column"
ELEVATOR: str = "Elevator"
LAVAPLATFORM: str = "Lava Platform"
LIQUIDLAVA: str = "Liquid Lava"
ENERGYROADUPWARDEFFECT: str = "Energy Road Upward Effect"
SMALLBUMPER: str = "Small Bumper"
GREENFLOATINGBUMPER: str = "Green Floating Bumper"
PINBALLFLIPPER: str = "Pinball Flipper"
SMALLTRIANGLEBUMPER: str = "Small Triangle Bumper"
STARGLASSPANEL: str = "Star Glass Panel"
STARGLASSAIRPANEL: str = "Star Glass Air Panel"
LARGETRIANGLEBUMPER: str = "Large Triangle Bumper"
BREAKABLEGLASSFLOOR: str = "Breakable Glass Floor"
FLOATINGDICE: str = "Floating Dice"
TRIPLESLOTS: str = "Triple Slots"
SINGLESLOTS: str = "Single Slots"
BINGOCHART: str = "Bingo Chart"
BINGOCHIP: str = "Bingo Chip"
DASHARROW: str = "Dash Arrow"
POTATOCHIP: str = "Potato Chip"
SWITCHABLERAIL: str = "Switchable Rail"
RAILSWITCH: str = "Rail Switch"
SWITCHABLEARROW: str = "Switchable Arrow"
RAILBOOSTER: str = "Rail Booster"
RAILCROSSINGROADBLOCK: str = "Rail Crossing Roadblock"
CAPSULE: str = "Capsule"
RAILPLATFORM: str = "Rail Platform"
TRAINTRAIN: str = "Train Train"
ENGINECORE: str = "Engine Core"
BIGGUNINTERIOR: str = "Big Gun Interior"
BARREL: str = "Barrel"
CANYONBRIDGE: str = "Canyon Bridge"
TRAINTOP: str = "Train Top"
GREENFROG: str = "Green Frog"
SMALLGREENRAINPLATFORM: str = "Small Green Rain Platform"
SMALLBOUNCYMUSHROOM: str = "Small Bouncy Mushroom"
TALLVERTICALVINE: str = "Tall Vertical Vine"
TALLTREEWITHPLATFORMS: str = "Tall Tree With Platforms"
GRINDABLEGROWINGIVY: str = "Grindable Growing Ivy"
LARGEYELLOWPLATFORM: str = "Large Yellow Platform"
BOUNCYFRUIT: str = "Bouncy Fruit"
BIGBOUNCYMUSHROOM: str = "Big Bouncy Mushroom"
SWINGINGVINE: str = "Swinging Vine"
BLACKFROG: str = "Black Frog"
BOUNCYFALLINGFRUIT: str = "Bouncy Falling Fruit"
TELEPORTERSWITCH: str = "Teleporter Switch"
CASTLEFLOATINGPLATFORM: str = "Castle Floating Platform"
FLAMETORCH: str = "Flame Torch"
PUMPKINGHOST: str = "Pumpkin Ghost"
MANSIONFLOATINGPLATFORM: str = "Mansion Floating Platform"
CASTLEKEY: str = "Castle Key"
RECTANGULARFLOATINGPLATFORM: str = "Rectangular Floating Platform"
SQUAREFLOATINGPLATFORM: str = "Square Floating Platform"
FALLINGPLATFORM: str = "Falling Platform"
SELFDESTRUCTSWITCH: str = "Self Destruct Switch"
EGGMANCELLKEY: str = "Eggman Cell Key"
EGGFLAPPER: str = "Egg Flapper"
EGGPAWN: str = "Egg Pawn"
KLAGEN: str = "Klagen"
FALCO: str = "Falco"
EGGHAMMER: str = "Egg Hammer"
CAMERON: str = "Cameron"
RHINOLINER: str = "Rhino Liner"
EGGBISHOP: str = "Egg Bishop"
E2000: str = "E2000"
SPECIALSTAGEORBS: str = "Special Stage Orbs"
APPEAREMERALD: str = "Appear Emerald"
SPECIALSTAGESPRING: str = "Special Stage Spring"
SPECIALSTAGEDASHPANEL: str = "Special Stage Dash Panel"
SPECIALSTAGEDASHRING: str = "Special Stage Dash Ring"

team_char_names: dict[str, list[str]] = \
    {
        SONIC:
            [
                CHARSONIC,
                CHARKNUCKLES,
                CHARTAILS,
            ],
    }

char_name_to_formation: dict[str, str] = \
    {
        CHARSONIC: SPEED,
        CHARKNUCKLES: POWER,
        CHARTAILS: FLYING,
    }

csv_file_headers: dict[str, list[str]] = \
    {
        REGION:
            [
                TEAM,
                LEVEL,
                NAME,
                OBJCHECKS
            ],

        CONNECTION:
            [
                TEAM,
                LEVEL,
                SOURCE,
                TARGET,
                RULE,
                NOTES
            ],
        LOCATION:
            [
                TEAM,
                LEVEL,
                NAME,
                CODE,
                ACT,
                REGION,
                RULE,
                LOCATIONTYPE,
                HINTINFO,
                NOTES
            ]
    }

sonic_heroes_story_names: dict[int, str] = \
    {
        0: SONIC,
        1: DARK,
        2: ROSE,
        3: CHAOTIX,
        4: SUPERHARDMODE,
    }

team_code_to_team: dict[str, str] = \
{
    'S': SONIC,
    'D': DARK,
    'R': ROSE,
    'C': CHAOTIX,
}

sonic_heroes_level_names: dict[int, str] = \
{
    1: SEASIDEHILL,
    2: OCEANPALACE,
    3: GRANDMETROPOLIS,
    4: POWERPLANT,
    5: CASINOPARK,
    6: BINGOHIGHWAY,
    7: RAILCANYON,
    8: BULLETSTATION,
    9: FROGFOREST,
    10: LOSTJUNGLE,
    11: HANGCASTLE,
    12: MYSTICMANSION,
    13: EGGFLEET,
    14: FINALFORTRESS,
}

sonic_heroes_regular_levels_index: dict[str, int] = \
{
    SEASIDEHILL: 0,
    OCEANPALACE: 1,
    GRANDMETROPOLIS: 2,
    POWERPLANT: 3,
    CASINOPARK: 4,
    BINGOHIGHWAY: 5,
    RAILCANYON: 6,
    BULLETSTATION: 7,
    FROGFOREST: 8,
    LOSTJUNGLE: 9,
    HANGCASTLE: 10,
    MYSTICMANSION: 11,
    EGGFLEET: 12,
    FINALFORTRESS: 13,
}





bonus_key_amounts: dict[str, dict[str, tuple[int, int]]] = \
    {
        SONIC:
            {
                SEASIDEHILL: (3, 3),
                OCEANPALACE: (3, 3),
                GRANDMETROPOLIS: (2, 3),
                POWERPLANT: (3, 3),
                CASINOPARK: (3, 3),
                BINGOHIGHWAY: (3, 3),
                RAILCANYON: (3, 3),
                BULLETSTATION: (3, 3),
                FROGFOREST: (3, 3),
                LOSTJUNGLE: (3, 3),
                HANGCASTLE: (3, 3),
                MYSTICMANSION: (3, 3),
                EGGFLEET: (3, 3),
                FINALFORTRESS: (3, 3),
            },
        DARK:
            {
                SEASIDEHILL: (3, 3),
                OCEANPALACE: (3, 3),
                GRANDMETROPOLIS: (3, 3),
                POWERPLANT: (3, 3),
                CASINOPARK: (3, 3),
                BINGOHIGHWAY: (3, 3),
                RAILCANYON: (3, 3),
                BULLETSTATION: (3, 3),
                FROGFOREST: (3, 3),
                LOSTJUNGLE: (3, 3),
                HANGCASTLE: (3, 3),
                MYSTICMANSION: (3, 3),
                EGGFLEET: (3, 3),
                FINALFORTRESS: (3, 3),
            },
        ROSE:
            {
                SEASIDEHILL: (2, 2), #1 before start of level
                OCEANPALACE: (3, 3),
                GRANDMETROPOLIS: (3, 3),
                POWERPLANT: (3, 3),
                CASINOPARK: (3, 3), #1 after (VIP table)
                BINGOHIGHWAY: (3, 3),
                RAILCANYON: (3, 3),
                BULLETSTATION: (3, 3),
                FROGFOREST: (3, 3),
                LOSTJUNGLE: (3, 3),
                HANGCASTLE: (3, 3),
                MYSTICMANSION: (3, 3),
                EGGFLEET: (3, 3),
                FINALFORTRESS: (3, 3),
            },
        CHAOTIX:
            {
                SEASIDEHILL: (3, 3),
                OCEANPALACE: (3, 3),
                GRANDMETROPOLIS: (3, 3),
                POWERPLANT: (3, 3),
                CASINOPARK: (3, 3),
                BINGOHIGHWAY: (3, 3),
                RAILCANYON: (2, 2), #1 way OOB (last)
                BULLETSTATION: (3, 3),
                FROGFOREST: (3, 3),
                LOSTJUNGLE: (3, 3),
                HANGCASTLE: (3, 3),
                MYSTICMANSION: (3, 3),
                EGGFLEET: (3, 3),
                FINALFORTRESS: (3, 3),
            },
        SUPERHARDMODE:
            {
                SEASIDEHILL: (0, 0),
                OCEANPALACE: (0, 0),
                GRANDMETROPOLIS: (0, 0),
                POWERPLANT: (0, 0),
                CASINOPARK: (0, 0),
                BINGOHIGHWAY: (0, 0),
                RAILCANYON: (0, 0),
                BULLETSTATION: (0, 0),
                FROGFOREST: (0, 0),
                LOSTJUNGLE: (0, 0),
                HANGCASTLE: (0, 0),
                MYSTICMANSION: (0, 0),
                EGGFLEET: (0, 0),
                FINALFORTRESS: (0, 0),
            },
    }
"""
The Mapping of Team and Level to number of bonus keys.
The first index is without secret and the second index is with secret
"""

sonic_heroes_extra_names: dict[int, str] = \
    {
        0: EGGHAWK,
        1: TEAMFIGHT1,
        2: ROBOTCARNIVAL,
        3: EGGALBATROSS,
        4: TEAMFIGHT2,
        5: ROBOTSTORM,
        6: EGGEMPEROR,
    }

boss_name_to_slot_data_id: dict[str, int] = \
    {
        EGGHAWK: 16,
        TEAMFIGHT1: 17,
        ROBOTCARNIVAL: 18,
        EGGALBATROSS: 19,
        TEAMFIGHT2: 20,
        ROBOTSTORM: 21,
        EGGEMPEROR: 22,
        METALMADNESS: 23,
    }

item_teams: list[str] = \
    [
        ANYTEAM,
        SONIC,
        DARK,
        ROSE,
        CHAOTIX,
        SUPERHARDMODE,
    ]

item_regions: list[str] = \
    [
        ALLREGIONS,
        OCEANREGION,
        HOTPLANTREGION,
        CASINOREGION,
        TRAINREGION,
        BIGPLANTREGION,
        GHOSTREGION,
        SKYREGION,
        SPECIALSTAGEREGION,
        BOSSREGION,
        FINALBOSSREGION,
    ]

item_abilities: list[str] = \
    [
        ALLABILITIES,
        HOMINGATTACK,
        TORNADO,
        ROCKETACCEL,
        LIGHTDASH,
        TRIANGLEJUMP,
        LIGHTATTACK,
        AMYHAMMERHOVER,
        INVISIBILITY,
        SHURIKEN,
        THUNDERSHOOT,
        FLIGHT,
        DUMMYRINGS,
        CHEESECANNON,
        FLOWERSTING,
        POWERATTACK,
        COMBOFINISHER,
        GLIDE,
        FIREDUNK,
        BELLYFLOP,
    ]

stage_objs: list[str] = \
    [
        ALLSTAGEOBJS,
        SINGLESPRING,
        TRIPLESPRING,
        RINGS,
        HINTRING,
        REGULARSWITCH,
        PUSHANDPULLSWITCH,
        TARGETSWITCH,
        DASHPANEL,
        DASHRING,
        RAINBOWHOOPS,
        CHECKPOINT,
        DASHRAMP,
        CANNON,
        REGULARWEIGHT,
        BREAKABLEWEIGHT,
        ITEMBOX,
        ITEMBALLOON,
        GOALRING,
        PULLEY,
        WOODCONTAINER,
        IRONCONTAINER,
        UNBREAKABLECONTAINER,
        LOSTCHAO,
        PROPELLER,
        POLE,
        GONG,
        FAN,
        WARPFLOWER,
        BONUSKEY,
        TELEPORTTRIGGER,
        CEMENTBLOCKONRAILS,
        CEMENTSLIDINGBLOCK,
        CEMENTBLOCK,
        MOVINGRUINPLATFORM,
        HERMITCRAB,
        SMALLSTONEPLATFORM,
        CRUMBLINGSTONEPILLAR,
        ENERGYROADSECTION,
        FALLINGDRAWBRIDGE,
        TILTINGBRIDGE,
        BLIMPPLATFORM,
        ENERGYROADSPEEDEFFECT,
        ENERGYROADUPWARDSECTION,
        ENERGYCOLUMN,
        ELEVATOR,
        LAVAPLATFORM,
        LIQUIDLAVA,
        ENERGYROADUPWARDEFFECT,
        SMALLBUMPER,
        GREENFLOATINGBUMPER,
        PINBALLFLIPPER,
        SMALLTRIANGLEBUMPER,
        STARGLASSPANEL,
        STARGLASSAIRPANEL,
        LARGETRIANGLEBUMPER,
        BREAKABLEGLASSFLOOR,
        FLOATINGDICE,
        TRIPLESLOTS,
        SINGLESLOTS,
        BINGOCHART,
        BINGOCHIP,
        DASHARROW,
        POTATOCHIP,
        SWITCHABLERAIL,
        RAILSWITCH,
        SWITCHABLEARROW,
        RAILBOOSTER,
        RAILCROSSINGROADBLOCK,
        CAPSULE,
        RAILPLATFORM,
        TRAINTRAIN,
        ENGINECORE,
        BIGGUNINTERIOR,
        BARREL,
        CANYONBRIDGE,
        TRAINTOP,
        GREENFROG,
        SMALLGREENRAINPLATFORM,
        SMALLBOUNCYMUSHROOM,
        TALLVERTICALVINE,
        TALLTREEWITHPLATFORMS,
        GRINDABLEGROWINGIVY,
        LARGEYELLOWPLATFORM,
        BOUNCYFRUIT,
        BIGBOUNCYMUSHROOM,
        SWINGINGVINE,
        BLACKFROG,
        BOUNCYFALLINGFRUIT,
        TELEPORTERSWITCH,
        CASTLEFLOATINGPLATFORM,
        FLAMETORCH,
        PUMPKINGHOST,
        MANSIONFLOATINGPLATFORM,
        CASTLEKEY,
        RECTANGULARFLOATINGPLATFORM,
        SQUAREFLOATINGPLATFORM,
        FALLINGPLATFORM,
        SELFDESTRUCTSWITCH,
        EGGMANCELLKEY,
        EGGFLAPPER,
        EGGPAWN,
        KLAGEN,
        FALCO,
        EGGHAMMER,
        CAMERON,
        RHINOLINER,
        EGGBISHOP,
        E2000,
        SPECIALSTAGEORBS,
        APPEAREMERALD,
        SPECIALSTAGESPRING,
        SPECIALSTAGEDASHPANEL,
        SPECIALSTAGEDASHRING,
    ]

level_to_game_region: dict[str, str] = \
    {
        SEASIDEHILL: OCEANREGION,
        OCEANPALACE: OCEANREGION,
        GRANDMETROPOLIS: HOTPLANTREGION,
        POWERPLANT: HOTPLANTREGION,
        CASINOPARK: CASINOREGION,
        BINGOHIGHWAY: CASINOREGION,
        RAILCANYON: TRAINREGION,
        BULLETSTATION: TRAINREGION,
        FROGFOREST: BIGPLANTREGION,
        LOSTJUNGLE: BIGPLANTREGION,
        HANGCASTLE: GHOSTREGION,
        MYSTICMANSION: GHOSTREGION,
        EGGFLEET: SKYREGION,
        FINALFORTRESS: SKYREGION,
    }

game_region_to_level: dict[str, list[str]] = \
    {
        OCEANREGION:
            [
                SEASIDEHILL,
                OCEANPALACE
            ],
        HOTPLANTREGION:
            [
                GRANDMETROPOLIS,
                POWERPLANT,
            ],
        CASINOREGION:
            [
                CASINOPARK,
                BINGOHIGHWAY,
            ],
        TRAINREGION:
            [
                RAILCANYON,
                BULLETSTATION,
            ],
        BIGPLANTREGION:
            [
                FROGFOREST,
                LOSTJUNGLE,
            ],
        GHOSTREGION:
            [
                HANGCASTLE,
                MYSTICMANSION,
            ],
        SKYREGION:
            [
                EGGFLEET,
                FINALFORTRESS,
            ],
    }

ability_item_req_counts: dict[str, int] = \
    {
        AMYHAMMERHOVER: 0,
        HOMINGATTACK: 1,
        TORNADO: 2,
        ROCKETACCEL: 2,
        LIGHTDASH: 3,
        TRIANGLEJUMP: 3,  #maybe separate tri jump and light dash
        LIGHTATTACK: 3,

        DUMMYRINGS: 1,
        CHEESECANNON: 1,
        FLOWERSTING: 1,
        THUNDERSHOOT: 2,
        FLIGHT: 3,

        BREAK: 0,
        COMBOFINISHER: 1,
        GLIDE: 2,
        FIREDUNK: 3,
        ULTIMATEFIREDUNK: 3,
        BELLYFLOP: 3,
    }

character_abilities: dict[str, list[str]] = \
    {
        SPEED:
            [
                HOMINGATTACK,
                TORNADO,
                ROCKETACCEL,
            ],
        FLYING:
            [
                THUNDERSHOOT,
                FLIGHT,
            ],
        POWER:
            [
                #POWERATTACK,
                GLIDE,
                COMBOFINISHER,
                FIREDUNK,
            ],
        CHARSONIC:
            [
                LIGHTDASH,
                TRIANGLEJUMP,
                LIGHTATTACK,
            ],
        CHARTAILS:
            [
                DUMMYRINGS
            ],
        CHARKNUCKLES:
            [],
    }


def get_csv_file_name(team: str, level: str, file_type: str, secret: bool = False) -> str:
    """
    Gets the csv file name for the given team and level and file type and secret.
    """
    if secret:
        return f"{level} {SECRET} {team} {file_type}".replace(" ", "")

    return f"{level} {team} {file_type}".replace(" ", "")


def is_there_a_secret_csv_file(team: str, level: str) -> bool:
    """
    Check if a secret csv file exists for the team and level.
    """
    if team == SONIC and level == GRANDMETROPOLIS:
        return True
    return False


def get_char_name_from_team(team: str, speed=False, flying=False, power=False):
    """
    Returns the character name for a given team and formation.
    """
    if sum([speed, flying, power]) > 1:
        print(f"Get Char Name From Team called with multiple chars. "
              f"team {team} speed {speed} flying {flying} power {power}")
        return ""
    if speed:
        return team_char_names[team][0]
    if power:
        return team_char_names[team][1]
    if flying:
        return team_char_names[team][2]
    return ""


def get_region_name_from_level(world: SonicHeroesWorld, level: str) -> str:
    """
    Returns the region name for a given level.
    """
    region: str = level_to_game_region[level]
    if world.options.ability_unlocks == 1:
        region = ALLREGIONS
    return region


def get_playable_char_item_name(char: str) -> str:
    """
    Returns the item name for a given character.
    """
    return f"{PLAYABLE} {char}"


def get_all_abilities_for_team(team: str):
    """
    Returns all abilities for a given team.
    """
    result = []
    result += [abilities for char_name in team_char_names[team]
               for abilities in get_all_abilities_for_character(char_name)]
    return result


def get_all_abilities_for_character(char_name: str):
    """
    Returns all abilities for a given character.
    """
    result = []
    result += character_abilities[char_name_to_formation[char_name]]
    result += character_abilities[char_name]
    return result


def get_ability_item_name(world: SonicHeroesWorld, team: str, region: str, ability: str) -> str:
    """
    Returns the item name for a given ability.
    This uses world to check for options.
    """
    if world.options.ability_unlocks == 1:
        region = ALLREGIONS
    return get_ability_item_name_without_world(team, region, ability)


def get_ability_item_name_without_world(team: str, region: str, ability: str) -> str:
    """
    Returns the item name for a given ability.
    This does not use world and requires the correct region name for the world options.
    """
    result = ""
    if team != ANYTEAM:
        result += f"{team} "

    result += f"{ability}"

    if region != ALLREGIONS:
        result += f" {region}"
    return result


def get_all_ability_item_names_for_character_and_region(world: SonicHeroesWorld, team: str,
                                                        char_name: str, region: str) -> list[str]:
    """
    Returns a list of all ability item names for a given character and region.
    """
    result = []
    abilities = get_all_abilities_for_character(char_name)

    if world.options.ability_unlocks == 1:
        region = ALLREGIONS

    for ability in abilities:
        result.append(get_ability_item_name(world, team, region, ability))
    return result


def get_stage_obj_item_name(world: SonicHeroesWorld, team: str, region: str, stage_obj: str) -> str:
    """
    Returns the item name for a given stage object.
    This uses world to check for options.
    """
    if world.options.ability_unlocks == 1:
        region = ALLREGIONS
    return get_stage_obj_item_name_without_world(team, region, stage_obj)


def get_stage_obj_item_name_without_world(team: str, region: str, stage_obj: str) -> str:
    """
    Returns the item name for a given stage object.
    This does not use world and requires the correct region name for the world options.
    """
    result = ""
    if team != ANYTEAM:
        result += f"{team} "

    result += f"{stage_obj}"

    if region != ALLREGIONS:
        result += f" {region}"
    return result

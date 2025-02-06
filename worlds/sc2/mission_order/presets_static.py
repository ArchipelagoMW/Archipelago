from typing import Dict, Any, Callable, List, Tuple
import copy

from ..mission_groups import MissionGroupNames
from ..mission_tables import SC2Mission, SC2Campaign

preset_mini_wol_with_prophecy = {
    "global": {
        "type": "column",
        "mission_pool": [
            MissionGroupNames.WOL_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Mar Sara": {
        "size": 1
    },
    "Colonist": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Artifact": {
        "size": 3,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 1, "entry_rules": [{ "scope": "../..", "amount": 4 }, { "items": { "Key": 1 }}] },
            { "index": 2, "entry_rules": [{ "scope": "../..", "amount": 8 }, { "items": { "Key": 1 }}] }
        ]
    },
    "Prophecy": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Artifact/1" },
            { "items": { "Key": 1 }}
        ],
        "mission_pool": [
            MissionGroupNames.PROPHECY_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Covert": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "scope": "..", "amount": 2 },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Rebellion": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "scope": "..", "amount": 3 },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Char": {
        "size": 3,
        "entry_rules": [
            { "scope": "../Artifact" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "next": [2] },
            { "index": 1, "entrance": True }
        ]
    }
}

preset_mini_wol = copy.deepcopy(preset_mini_wol_with_prophecy)
preset_mini_prophecy = { "Prophecy": preset_mini_wol.pop("Prophecy") }
preset_mini_prophecy["Prophecy"].pop("entry_rules")
preset_mini_prophecy["Prophecy"]["type"] = "gauntlet"
preset_mini_prophecy["Prophecy"]["display_name"] = ""
preset_mini_prophecy["Prophecy"]["missions"].append({ "index": "entrances", "entry_rules": [] })

preset_mini_hots = {
    "global": {
        "type": "column",
        "mission_pool": [
            MissionGroupNames.HOTS_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Umoja": {
        "size": 1,
    },
    "Kaldir": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Umoja" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Char": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Umoja" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Zerus": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Umoja" },
            { "scope": "..", "amount": 3 },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Skygeirr Station": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Zerus" },
            { "scope": "..", "amount": 5 },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Dominion Space": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Zerus" },
            { "scope": "..", "amount": 5 },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Korhal": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Zerus" },
            { "scope": "..", "amount": 8 },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    }
}

preset_mini_lotv_prologue = {
    "min_difficulty": "easy",
    "Prologue": {
        "display_name": "",
        "type": "gauntlet",
        "size": 2,
        "mission_pool": [
            MissionGroupNames.PROLOGUE_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ],
        "missions": [
            { "index": 1, "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    }
}

preset_mini_lotv = {
    "global": {
        "type": "column",
        "mission_pool": [
            MissionGroupNames.LOTV_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Aiur": {
        "size": 2,
        "missions": [
            { "index": 1, "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Korhal": {
        "size": 1,
        "entry_rules": [
            { "scope": "../Aiur" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Shakuras": {
        "size": 1,
        "entry_rules": [
            { "scope": "../Aiur" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Purifier": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Korhal" },
            { "scope": "../Shakuras" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 1, "entry_rules": [{ "scope": "../../Ulnar" }, { "items": { "Key": 1 }}] }
        ]
    },
    "Ulnar": {
        "size": 1,
        "entry_rules": [
            { "scope": "../Purifier/0" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Tal'darim": {
        "size": 1,
        "entry_rules": [
            { "scope": "../Ulnar" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Return to Aiur": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Purifier" },
            { "scope": "../Tal'darim" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    }
}

preset_mini_lotv_epilogue = {
    "min_difficulty": "very hard",
    "Epilogue": {
        "display_name": "",
        "type": "gauntlet",
        "size": 2,
        "mission_pool": [
            MissionGroupNames.EPILOGUE_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ],
        "missions": [
            { "index": 1, "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    }
}

preset_mini_nco = {
    "min_difficulty": "easy",
    "global": {
        "type": "column",
        "mission_pool": [
            MissionGroupNames.NCO_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Mission Pack 1": {
        "size": 2,
        "missions": [
            { "index": 1, "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Mission Pack 2": {
        "size": 1,
        "entry_rules": [
            { "scope": "../Mission Pack 1" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Mission Pack 3": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Mission Pack 2" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
}

preset_wol_with_prophecy = {
    "global": {
        "type": "column",
        "mission_pool": [
            MissionGroupNames.WOL_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Mar Sara": {
        "size": 3,
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.LIBERATION_DAY.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_OUTLAWS.mission_name },
            { "index": 2, "mission_pool": SC2Mission.ZERO_HOUR.mission_name },
            { "index": [1, 2], "entry_rules": [{ "items": { "Key": 1 }}] }
        ]
    },
    "Colonist": {
        "size": 4,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": 1, "next": [2, 3] },
            { "index": 2, "next": [] },
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": [2, 3], "entry_rules": [{ "scope": "../..", "amount": 7 }, { "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.EVACUATION.mission_name },
            { "index": 1, "mission_pool": SC2Mission.OUTBREAK.mission_name },
            { "index": 2, "mission_pool": SC2Mission.SAFE_HAVEN.mission_name },
            { "index": 3, "mission_pool": SC2Mission.HAVENS_FALL.mission_name },
        ]
    },
    "Artifact": {
        "size": 5,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 1, "entry_rules": [{ "scope": "../..", "amount": 8 }, { "items": { "Key": 1 }}] },
            { "index": 2, "entry_rules": [{ "scope": "../..", "amount": 11 }, { "items": { "Key": 1 }}] },
            { "index": 3, "entry_rules": [{ "scope": "../..", "amount": 14 }, { "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.SMASH_AND_GRAB.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_DIG.mission_name },
            { "index": 2, "mission_pool": SC2Mission.THE_MOEBIUS_FACTOR.mission_name },
            { "index": 3, "mission_pool": SC2Mission.SUPERNOVA.mission_name },
            { "index": 4, "mission_pool": SC2Mission.MAW_OF_THE_VOID.mission_name },
        ]
    },
    "Prophecy": {
        "size": 4,
        "entry_rules": [
            { "scope": "../Artifact/1" },
            { "items": { "Key": 1 }}
        ],
        "mission_pool": [
            MissionGroupNames.PROPHECY_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.WHISPERS_OF_DOOM.mission_name },
            { "index": 1, "mission_pool": SC2Mission.A_SINISTER_TURN.mission_name },
            { "index": 2, "mission_pool": SC2Mission.ECHOES_OF_THE_FUTURE.mission_name },
            { "index": 3, "mission_pool": SC2Mission.IN_UTTER_DARKNESS.mission_name },
        ]
    },
    "Covert": {
        "size": 4,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "scope": "..", "amount": 4 },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": 1, "next": [2, 3] },
            { "index": 2, "next": [] },
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": [2, 3], "entry_rules": [{ "scope": "../..", "amount": 8 }, { "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.DEVILS_PLAYGROUND.mission_name },
            { "index": 1, "mission_pool": SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.BREAKOUT.mission_name },
            { "index": 3, "mission_pool": SC2Mission.GHOST_OF_A_CHANCE.mission_name },
        ]
    },
    "Rebellion": {
        "size": 5,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "scope": "..", "amount": 6 },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name },
            { "index": 1, "mission_pool": SC2Mission.CUTTHROAT.mission_name },
            { "index": 2, "mission_pool": SC2Mission.ENGINE_OF_DESTRUCTION.mission_name },
            { "index": 3, "mission_pool": SC2Mission.MEDIA_BLITZ.mission_name },
            { "index": 4, "mission_pool": SC2Mission.PIERCING_OF_THE_SHROUD.mission_name },
        ]
    },
    "Char": {
        "size": 4,
        "entry_rules": [
            { "scope": "../Artifact" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": 0, "next": [1, 2] },
            { "index": [1, 2], "next": [3] },
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.GATES_OF_HELL.mission_name },
            { "index": 1, "mission_pool": SC2Mission.BELLY_OF_THE_BEAST.mission_name },
            { "index": 2, "mission_pool": SC2Mission.SHATTER_THE_SKY.mission_name },
            { "index": 3, "mission_pool": SC2Mission.ALL_IN.mission_name },
        ]
    }
}

preset_wol = copy.deepcopy(preset_wol_with_prophecy)
preset_prophecy = { "Prophecy": preset_wol.pop("Prophecy") }
preset_prophecy["Prophecy"].pop("entry_rules")
preset_prophecy["Prophecy"]["type"] = "gauntlet"
preset_prophecy["Prophecy"]["display_name"] = ""
preset_prophecy["Prophecy"]["missions"].append({ "index": "entrances", "entry_rules": [] })

preset_hots = {
    "global": {
        "type": "column",
        "mission_pool": [
            MissionGroupNames.HOTS_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Umoja": {
        "size": 3,
        "missions": [
            { "index": [1, 2], "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.LAB_RAT.mission_name },
            { "index": 1, "mission_pool": SC2Mission.BACK_IN_THE_SADDLE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.RENDEZVOUS.mission_name },
        ]
    },
    "Kaldir": {
        "size": 3,
        "entry_rules": [
            { "scope": "../Umoja" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.HARVEST_OF_SCREAMS.mission_name },
            { "index": 1, "mission_pool": SC2Mission.SHOOT_THE_MESSENGER.mission_name },
            { "index": 2, "mission_pool": SC2Mission.ENEMY_WITHIN.mission_name },
        ]
    },
    "Char": {
        "size": 3,
        "entry_rules": [
            { "scope": "../Umoja" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.DOMINATION.mission_name },
            { "index": 1, "mission_pool": SC2Mission.FIRE_IN_THE_SKY.mission_name },
            { "index": 2, "mission_pool": SC2Mission.OLD_SOLDIERS.mission_name },
        ]
    },
    "Zerus": {
        "size": 3,
        "entry_rules": [
            {
                "rules": [
                    { "scope": "../Kaldir" },
                    { "scope": "../Char" }
                ],
                "amount": 1
            },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.WAKING_THE_ANCIENT.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_CRUCIBLE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.SUPREME.mission_name },
        ]
    },
    "Skygeirr Station": {
        "size": 3,
        "entry_rules": [
            { "scope": ["../Kaldir", "../Char", "../Zerus"] },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.INFESTED.mission_name },
            { "index": 1, "mission_pool": SC2Mission.HAND_OF_DARKNESS.mission_name },
            { "index": 2, "mission_pool": SC2Mission.PHANTOMS_OF_THE_VOID.mission_name },
        ]
    },
    "Dominion Space": {
        "size": 2,
        "entry_rules": [
            { "scope": ["../Kaldir", "../Char", "../Zerus"] },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name },
            { "index": 1, "mission_pool": SC2Mission.CONVICTION.mission_name },
        ]
    },
    "Korhal": {
        "size": 3,
        "entry_rules": [
            { "scope": ["../Skygeirr Station", "../Dominion Space"] },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.PLANETFALL.mission_name },
            { "index": 1, "mission_pool": SC2Mission.DEATH_FROM_ABOVE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.THE_RECKONING.mission_name },
        ]
    }
}

preset_lotv_prologue = {
    "min_difficulty": "easy",
    "Prologue": {
        "display_name": "",
        "type": "gauntlet",
        "size": 3,
        "mission_pool": [
            MissionGroupNames.PROLOGUE_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ],
        "missions": [
            { "index": [1, 2], "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.DARK_WHISPERS.mission_name },
            { "index": 1, "mission_pool": SC2Mission.GHOSTS_IN_THE_FOG.mission_name },
            { "index": 2, "mission_pool": SC2Mission.EVIL_AWOKEN.mission_name },
        ]
    }
}

preset_lotv = {
    "global": {
        "type": "column",
        "mission_pool": [
            MissionGroupNames.LOTV_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Aiur": {
        "size": 3,
        "missions": [
            { "index": [1, 2], "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.FOR_AIUR.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_GROWING_SHADOW.mission_name },
            { "index": 2, "mission_pool": SC2Mission.THE_SPEAR_OF_ADUN.mission_name },
        ]
    },
    "Korhal": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Aiur" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.SKY_SHIELD.mission_name },
            { "index": 1, "mission_pool": SC2Mission.BROTHERS_IN_ARMS.mission_name },
        ]
    },
    "Shakuras": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Aiur" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.AMON_S_REACH.mission_name },
            { "index": 1, "mission_pool": SC2Mission.LAST_STAND.mission_name },
        ]
    },
    "Purifier": {
        "size": 3,
        "entry_rules": [
            {
                "rules": [
                    { "scope": "../Korhal" },
                    { "scope": "../Shakuras" }
                ],
                "amount": 1
            },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 1, "entry_rules": [{ "scope": "../../Ulnar" }, { "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.FORBIDDEN_WEAPON.mission_name },
            { "index": 1, "mission_pool": SC2Mission.UNSEALING_THE_PAST.mission_name },
            { "index": 2, "mission_pool": SC2Mission.PURIFICATION.mission_name },
        ]
    },
    "Ulnar": {
        "size": 3,
        "entry_rules": [
            {
                "scope": [
                    "../Korhal",
                    "../Shakuras",
                    "../Purifier/0"
                ]
            },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.TEMPLE_OF_UNIFICATION.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_INFINITE_CYCLE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.HARBINGER_OF_OBLIVION.mission_name },
        ]
    },
    "Tal'darim": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Ulnar" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.STEPS_OF_THE_RITE.mission_name },
            { "index": 1, "mission_pool": SC2Mission.RAK_SHIR.mission_name },
        ]
    },
    "Moebius": {
        "size": 1,
        "entry_rules": [
            {
                "rules": [
                    { "scope": "../Purifier" },
                    { "scope": "../Tal'darim" }
                ],
                "amount": 1
            },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.TEMPLAR_S_CHARGE.mission_name },
        ]
    },
    "Return to Aiur": {
        "size": 3,
        "entry_rules": [
            { "scope": "../Purifier" },
            { "scope": "../Tal'darim" },
            { "scope": "../Moebius" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.TEMPLAR_S_RETURN.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_HOST.mission_name },
            { "index": 2, "mission_pool": SC2Mission.SALVATION.mission_name },
        ]
    }
}

preset_lotv_epilogue = {
    "min_difficulty": "very hard",
    "Epilogue": {
        "display_name": "",
        "type": "gauntlet",
        "size": 3,
        "mission_pool": [
            MissionGroupNames.EPILOGUE_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ],
        "missions": [
            { "index": [1, 2], "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.INTO_THE_VOID.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name },
            { "index": 2, "mission_pool": SC2Mission.AMON_S_FALL.mission_name },
        ]
    }
}

preset_nco = {
    "min_difficulty": "easy",
    "global": {
        "type": "column",
        "mission_pool": [
            MissionGroupNames.NCO_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Mission Pack 1": {
        "size": 3,
        "missions": [
            { "index": [1, 2], "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.THE_ESCAPE.mission_name },
            { "index": 1, "mission_pool": SC2Mission.SUDDEN_STRIKE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.ENEMY_INTELLIGENCE.mission_name },
        ]
    },
    "Mission Pack 2": {
        "size": 3,
        "entry_rules": [
            { "scope": "../Mission Pack 1" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.TROUBLE_IN_PARADISE.mission_name },
            { "index": 1, "mission_pool": SC2Mission.NIGHT_TERRORS.mission_name },
            { "index": 2, "mission_pool": SC2Mission.FLASHPOINT.mission_name },
        ]
    },
    "Mission Pack 3": {
        "size": 3,
        "entry_rules": [
            { "scope": "../Mission Pack 2" },
            { "items": { "Key": 1 }}
        ],
        "missions": [
            { "index": "all", "entry_rules": [{ "items": { "Key": 1 }}] },
            { "index": 0, "mission_pool": SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name },
            { "index": 1, "mission_pool": SC2Mission.DARK_SKIES.mission_name },
            { "index": 2, "mission_pool": SC2Mission.END_GAME.mission_name },
        ]
    },
}

def _build_static_preset(preset: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
    # Raceswap shuffling
    raceswaps = options.pop("shuffle_raceswaps", False)
    if not isinstance(raceswaps, bool):
        raise ValueError(
            f"Preset option \"shuffle_raceswaps\" received unknown value \"{raceswaps}\".\n"
            "Valid values are: true, false"
        )
    elif raceswaps == True:
        # Remove "~ Raceswap Missions" operation from mission pool options
        # Also add raceswap variants to plando'd vanilla missions
        for layout in preset.values():
            if type(layout) == dict:
                # Currently mission pools in layouts are always ["X campaign missions", "~ raceswap missions"]
                layout_mission_pool: List[str] = layout.get("mission_pool", None)
                if layout_mission_pool is not None:
                    layout_mission_pool.pop()
                    layout["mission_pool"] = layout_mission_pool
                if "missions" in layout:
                    for slot in layout["missions"]:
                        # Currently mission pools in slots are always strings
                        slot_mission_pool: str = slot.get("mission_pool", None)
                        # Identify raceswappable missions by their race in brackets
                        if slot_mission_pool is not None and slot_mission_pool[-1] == ")":
                            mission_name = slot_mission_pool[:slot_mission_pool.rfind("(")]
                            new_mission_pool = [f"{mission_name}({race})" for race in ["Terran", "Zerg", "Protoss"]]
                            slot["mission_pool"] = new_mission_pool
    # The presets are set up for no raceswaps, so raceswaps == False doesn't need to be covered

    # Mission pool selection
    missions = options.pop("missions", "random")
    if missions == "vanilla":
        pass # use preset as it is
    elif missions == "vanilla_shuffled":
        # remove pre-set missions
        for layout in preset.values():
            if type(layout) == dict and "missions" in layout:
                for slot in layout["missions"]:
                    slot.pop("mission_pool", ())
    elif missions == "random":
        # remove pre-set missions and mission pools
        for layout in preset.values():
            if type(layout) == dict:
                layout.pop("mission_pool", ())
                if "missions" in layout:
                    for slot in layout["missions"]:
                        slot.pop("mission_pool", ())
    else:
        raise ValueError(
            f"Preset option \"missions\" received unknown value \"{missions}\".\n"
            "Valid values are: random, vanilla, vanilla_shuffled"
        )
    
    # Key rule selection
    keys = options.pop("keys", "none")
    if keys == "layouts":
        # remove keys from mission entry rules
        for layout in preset.values():
            if type(layout) == dict and "missions" in layout:
                for slot in layout["missions"]:
                    if "entry_rules" in slot:
                        slot["entry_rules"] = _remove_key_rules(slot["entry_rules"])
    elif keys == "missions":
        # remove keys from layout entry rules
        for layout in preset.values():
            if type(layout) == dict and "entry_rules" in layout:
                layout["entry_rules"] = _remove_key_rules(layout["entry_rules"])
    elif keys == "progressive_layouts":
        # remove keys from mission entry rules, replace keys in layout entry rules with unique-track keys
        for layout in preset.values():
            if type(layout) == dict:
                if "entry_rules" in layout:
                    layout["entry_rules"] = _make_key_rules_progressive(layout["entry_rules"], 0)
                if "missions" in layout:
                    for slot in layout["missions"]:
                        if "entry_rules" in slot:
                            slot["entry_rules"] = _remove_key_rules(slot["entry_rules"])
    elif keys == "progressive_missions":
        # remove keys from layout entry rules, replace keys in mission entry rules
        for layout in preset.values():
            if type(layout) == dict:
                if "entry_rules" in layout:
                    layout["entry_rules"] = _remove_key_rules(layout["entry_rules"])
                if "missions" in layout:
                    for slot in layout["missions"]:
                        if "entry_rules" in slot:
                            slot["entry_rules"] = _make_key_rules_progressive(slot["entry_rules"], 1)
    elif keys == "progressive_per_layout":
        # remove keys from layout entry rules, replace keys in mission entry rules with unique-track keys
        # specifically ignore layouts that have no entry rules (and are thus the first of their campaign)
        for layout in preset.values():
            if type(layout) == dict and "entry_rules" in layout:
                layout["entry_rules"] = _remove_key_rules(layout["entry_rules"])
                if "missions" in layout:
                    for slot in layout["missions"]:
                        if "entry_rules" in slot:
                            slot["entry_rules"] = _make_key_rules_progressive(slot["entry_rules"], 0)
    elif keys == "none":
        # remove keys from both layout and mission entry rules
        for layout in preset.values():
            if type(layout) == dict:
                if "entry_rules" in layout:
                    layout["entry_rules"] = _remove_key_rules(layout["entry_rules"])
                if "missions" in layout:
                    for slot in layout["missions"]:
                        if "entry_rules" in slot:
                            slot["entry_rules"] = _remove_key_rules(slot["entry_rules"])
    else:
        raise ValueError(
            f"Preset option \"keys\" received unknown value \"{keys}\".\n"
            "Valid values are: none, missions, layouts, progressive_missions, progressive_layouts, progressive_per_layout"
        )
    
    return preset

def _remove_key_rules(entry_rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [rule for rule in entry_rules if not ("items" in rule and "Key" in rule["items"])]

def _make_key_rules_progressive(entry_rules: List[Dict[str, Any]], track: int) -> List[Dict[str, Any]]:
    for rule in entry_rules:
        if "items" in rule and "Key" in rule["items"]:
            new_items: Dict[str, Any] = {}
            for (item, amount) in rule["items"].items():
                if item == "Key":
                    new_items["Progressive Key"] = track
                else:
                    new_items[item] = amount
            rule["items"] = new_items
    return entry_rules

def static_preset(preset: Dict[str, Any]) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    return lambda options: _build_static_preset(copy.deepcopy(preset), options)

def get_used_layout_names() -> Dict[SC2Campaign, Tuple[int, List[str]]]:
    campaign_to_preset: Dict[SC2Campaign, Dict[str, Any]] = {
        SC2Campaign.WOL: preset_wol_with_prophecy,
        SC2Campaign.PROPHECY: preset_prophecy,
        SC2Campaign.HOTS: preset_hots,
        SC2Campaign.PROLOGUE: preset_lotv_prologue,
        SC2Campaign.LOTV: preset_lotv,
        SC2Campaign.EPILOGUE: preset_lotv_epilogue,
        SC2Campaign.NCO: preset_nco
    }
    campaign_to_layout_names: Dict[SC2Campaign, Tuple[int, List[str]]] = { SC2Campaign.GLOBAL: (0, []) }
    for campaign in SC2Campaign:
        if campaign == SC2Campaign.GLOBAL:
            continue
        previous_campaign = [prev for prev in SC2Campaign if prev.id == campaign.id - 1][0]
        previous_size = campaign_to_layout_names[previous_campaign][0]
        preset = campaign_to_preset[campaign]
        new_layouts = [value for value in preset.keys() if isinstance(preset[value], dict) and value != "global"]
        campaign_to_layout_names[campaign] = (previous_size + len(campaign_to_layout_names[previous_campaign][1]), new_layouts)
    campaign_to_layout_names.pop(SC2Campaign.GLOBAL)
    return campaign_to_layout_names

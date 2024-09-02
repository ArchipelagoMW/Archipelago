from typing import Dict, Any, Callable
import copy

from ..mission_groups import MissionGroupNames
from ..mission_tables import SC2Mission

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
        "entry_rules": [{ "scope": "../Mar Sara" }]
    },
    "Artifact": {
        "size": 3,
        "entry_rules": [{ "scope": "../Mar Sara" }],
        "missions": [
            { "index": 1, "entry_rules": [{ "scope": "../..", "amount": 4 }] },
            { "index": 2, "entry_rules": [{ "scope": "../..", "amount": 8 }] }
        ]
    },
    "Prophecy": {
        "size": 2,
        "entry_rules": [{ "scope": "../Artifact/1" }],
        "mission_pool": [
            MissionGroupNames.PROPHECY_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ]
    },
    "Covert": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "scope": "..", "amount": 2 }
        ]
    },
    "Rebellion": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Mar Sara" },
            { "scope": "..", "amount": 3 }
        ]
    },
    "Char": {
        "size": 3,
        "entry_rules": [{ "scope": "../Artifact" }],
        "missions": [
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
        "entry_rules": [{ "scope": "../Umoja" }]
    },
    "Char": {
        "size": 2,
        "entry_rules": [{ "scope": "../Umoja" }]
    },
    "Zerus": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Umoja" },
            { "scope": "..", "amount": 3 }
        ]
    },
    "Skygeirr Station": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Zerus" },
            { "scope": "..", "amount": 5 }
        ]
    },
    "Dominion Space": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Zerus" },
            { "scope": "..", "amount": 5 }
        ]
    },
    "Korhal": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Zerus" },
            { "scope": "..", "amount": 8 }
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
        "size": 2
    },
    "Korhal": {
        "size": 1,
        "entry_rules": [{ "scope": "../Aiur" }]
    },
    "Shakuras": {
        "size": 1,
        "entry_rules": [{ "scope": "../Aiur" }]
    },
    "Purifier": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Korhal" },
            { "scope": "../Shakuras" }
        ],
        "missions": [
            { "index": 1, "entry_rules": [{ "scope": "../../Ulnar" }] }
        ]
    },
    "Ulnar": {
        "size": 1,
        "entry_rules": [{ "scope": "../Purifier/0" }]
    },
    "Tal'darim": {
        "size": 1,
        "entry_rules": [{ "scope": "../Ulnar" }]
    },
    "Return to Aiur": {
        "size": 2,
        "entry_rules": [
            { "scope": "../Purifier" },
            { "scope": "../Tal'darim" },
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
        ]
    }
}

# Entry rules in NCO point at specific missions since the columns don't have visible titles
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
        "display_name": "",
        "size": 2,
    },
    "Mission Pack 2": {
        "display_name": "",
        "size": 1,
        "entry_rules": [{ "scope": "../Mission Pack 1/1" }],
    },
    "Mission Pack 3": {
        "display_name": "",
        "size": 2,
        "entry_rules": [{ "scope": "../Mission Pack 2/0" }],
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
        ]
    },
    "Colonist": {
        "size": 4,
        "entry_rules": [{ "scope": "../Mar Sara" }],
        "missions": [
            { "index": 1, "next": [2, 3] },
            { "index": 2, "next": [] },
            { "index": [2, 3], "entry_rules": [{ "scope": "../..", "amount": 7 }] },
            { "index": 0, "mission_pool": SC2Mission.EVACUATION.mission_name },
            { "index": 1, "mission_pool": SC2Mission.OUTBREAK.mission_name },
            { "index": 2, "mission_pool": SC2Mission.SAFE_HAVEN.mission_name },
            { "index": 3, "mission_pool": SC2Mission.HAVENS_FALL.mission_name },
        ]
    },
    "Artifact": {
        "size": 5,
        "entry_rules": [{ "scope": "../Mar Sara" }],
        "missions": [
            { "index": 1, "entry_rules": [{ "scope": "../..", "amount": 8 }] },
            { "index": 2, "entry_rules": [{ "scope": "../..", "amount": 11 }] },
            { "index": 3, "entry_rules": [{ "scope": "../..", "amount": 14 }] },
            { "index": 0, "mission_pool": SC2Mission.SMASH_AND_GRAB.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_DIG.mission_name },
            { "index": 2, "mission_pool": SC2Mission.THE_MOEBIUS_FACTOR.mission_name },
            { "index": 3, "mission_pool": SC2Mission.SUPERNOVA.mission_name },
            { "index": 4, "mission_pool": SC2Mission.MAW_OF_THE_VOID.mission_name },
        ]
    },
    "Prophecy": {
        "size": 4,
        "entry_rules": [{ "scope": "../Artifact/1" }],
        "mission_pool": [
            MissionGroupNames.PROPHECY_MISSIONS,
            "~ " + MissionGroupNames.RACESWAP_MISSIONS
        ],
        "missions": [
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
            { "scope": "..", "amount": 4 }
        ],
        "missions": [
            { "index": 1, "next": [2, 3] },
            { "index": 2, "next": [] },
            { "index": [2, 3], "entry_rules": [{ "scope": "../..", "amount": 8 }] },
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
            { "scope": "..", "amount": 6 }
        ],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.THE_GREAT_TRAIN_ROBBERY.mission_name },
            { "index": 1, "mission_pool": SC2Mission.CUTTHROAT.mission_name },
            { "index": 2, "mission_pool": SC2Mission.ENGINE_OF_DESTRUCTION.mission_name },
            { "index": 3, "mission_pool": SC2Mission.MEDIA_BLITZ.mission_name },
            { "index": 4, "mission_pool": SC2Mission.PIERCING_OF_THE_SHROUD.mission_name },
        ]
    },
    "Char": {
        "size": 4,
        "entry_rules": [{ "scope": "../Artifact" }],
        "missions": [
            { "index": 0, "next": [1, 2] },
            { "index": [1, 2], "next": [3] },
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
            { "index": 0, "mission_pool": SC2Mission.LAB_RAT.mission_name },
            { "index": 1, "mission_pool": SC2Mission.BACK_IN_THE_SADDLE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.RENDEZVOUS.mission_name },
        ]
    },
    "Kaldir": {
        "size": 3,
        "entry_rules": [{ "scope": "../Umoja" }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.HARVEST_OF_SCREAMS.mission_name },
            { "index": 1, "mission_pool": SC2Mission.SHOOT_THE_MESSENGER.mission_name },
            { "index": 2, "mission_pool": SC2Mission.ENEMY_WITHIN.mission_name },
        ]
    },
    "Char": {
        "size": 3,
        "entry_rules": [{ "scope": "../Umoja" }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.DOMINATION.mission_name },
            { "index": 1, "mission_pool": SC2Mission.FIRE_IN_THE_SKY.mission_name },
            { "index": 2, "mission_pool": SC2Mission.OLD_SOLDIERS.mission_name },
        ]
    },
    "Zerus": {
        "size": 3,
        "entry_rules": [{
            "rules": [
                { "scope": "../Kaldir" },
                { "scope": "../Char" }
            ],
            "amount": 1
        }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.WAKING_THE_ANCIENT.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_CRUCIBLE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.SUPREME.mission_name },
        ]
    },
    "Skygeirr Station": {
        "size": 3,
        "entry_rules": [{ "scope": ["../Kaldir", "../Char", "../Zerus"] }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.INFESTED.mission_name },
            { "index": 1, "mission_pool": SC2Mission.HAND_OF_DARKNESS.mission_name },
            { "index": 2, "mission_pool": SC2Mission.PHANTOMS_OF_THE_VOID.mission_name },
        ]
    },
    "Dominion Space": {
        "size": 2,
        "entry_rules": [{ "scope": ["../Kaldir", "../Char", "../Zerus"] }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.WITH_FRIENDS_LIKE_THESE.mission_name },
            { "index": 1, "mission_pool": SC2Mission.CONVICTION.mission_name },
        ]
    },
    "Korhal": {
        "size": 3,
        "entry_rules": [{ "scope": ["../Skygeirr Station", "../Dominion Space"] }],
        "missions": [
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
            { "index": 0, "mission_pool": SC2Mission.FOR_AIUR.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_GROWING_SHADOW.mission_name },
            { "index": 2, "mission_pool": SC2Mission.THE_SPEAR_OF_ADUN.mission_name },
        ]
    },
    "Korhal": {
        "size": 2,
        "entry_rules": [{ "scope": "../Aiur" }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.SKY_SHIELD.mission_name },
            { "index": 1, "mission_pool": SC2Mission.BROTHERS_IN_ARMS.mission_name },
        ]
    },
    "Shakuras": {
        "size": 2,
        "entry_rules": [{ "scope": "../Aiur" }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.AMON_S_REACH.mission_name },
            { "index": 1, "mission_pool": SC2Mission.LAST_STAND.mission_name },
        ]
    },
    "Purifier": {
        "size": 3,
        "entry_rules": [{
            "rules": [
                { "scope": "../Korhal" },
                { "scope": "../Shakuras" }
            ],
            "amount": 1
        }],
        "missions": [
            { "index": 1, "entry_rules": [{ "scope": "../../Ulnar" }] },
            { "index": 0, "mission_pool": SC2Mission.FORBIDDEN_WEAPON.mission_name },
            { "index": 1, "mission_pool": SC2Mission.UNSEALING_THE_PAST.mission_name },
            { "index": 2, "mission_pool": SC2Mission.PURIFICATION.mission_name },
        ]
    },
    "Ulnar": {
        "size": 3,
        "entry_rules": [{
            "scope": [
                "../Korhal",
                "../Shakuras",
                "../Purifier/0"
            ]
        }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.TEMPLE_OF_UNIFICATION.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_INFINITE_CYCLE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.HARBINGER_OF_OBLIVION.mission_name },
        ]
    },
    "Tal'darim": {
        "size": 2,
        "entry_rules": [{ "scope": "../Ulnar" }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.STEPS_OF_THE_RITE.mission_name },
            { "index": 1, "mission_pool": SC2Mission.RAK_SHIR.mission_name },
        ]
    },
    "Moebius": {
        "size": 1,
        "entry_rules": [{
            "rules": [
                { "scope": "../Purifier" },
                { "scope": "../Tal'darim" }
            ],
            "amount": 1
        }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.TEMPLAR_S_CHARGE.mission_name },
        ]
    },
    "Return to Aiur": {
        "size": 3,
        "entry_rules": [
            { "scope": "../Purifier" },
            { "scope": "../Tal'darim" },
            { "scope": "../Moebius" },
        ],
        "missions": [
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
            { "index": 0, "mission_pool": SC2Mission.INTO_THE_VOID.mission_name },
            { "index": 1, "mission_pool": SC2Mission.THE_ESSENCE_OF_ETERNITY.mission_name },
            { "index": 2, "mission_pool": SC2Mission.AMON_S_FALL.mission_name },
        ]
    }
}

# Entry rules in NCO point at specific missions since the columns don't have visible titles
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
        "display_name": "",
        "size": 3,
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.THE_ESCAPE.mission_name },
            { "index": 1, "mission_pool": SC2Mission.SUDDEN_STRIKE.mission_name },
            { "index": 2, "mission_pool": SC2Mission.ENEMY_INTELLIGENCE.mission_name },
        ]
    },
    "Mission Pack 2": {
        "display_name": "",
        "size": 3,
        "entry_rules": [{ "scope": "../Mission Pack 1/2" }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.TROUBLE_IN_PARADISE.mission_name },
            { "index": 1, "mission_pool": SC2Mission.NIGHT_TERRORS.mission_name },
            { "index": 2, "mission_pool": SC2Mission.FLASHPOINT.mission_name },
        ]
    },
    "Mission Pack 3": {
        "display_name": "",
        "size": 3,
        "entry_rules": [{ "scope": "../Mission Pack 2/2" }],
        "missions": [
            { "index": 0, "mission_pool": SC2Mission.IN_THE_ENEMY_S_SHADOW.mission_name },
            { "index": 1, "mission_pool": SC2Mission.DARK_SKIES.mission_name },
            { "index": 2, "mission_pool": SC2Mission.END_GAME.mission_name },
        ]
    },
}

def _build_static_preset(preset: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
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
        raise ValueError(f"Preset option \"missions\" received unknown value \"{missions}\".")
    return preset

def static_preset(preset: Dict[str, Any]) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    return lambda options: _build_static_preset(copy.deepcopy(preset), options)

from typing import Dict, Any, Callable
import copy

from ..mission_groups import MissionGroupNames

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
            {
                "index": 1,
                "entry_rules": [{
                    "scope": "../..",
                    "amount": 4
                }]
            },
            {
                "index": 2,
                "entry_rules": [{
                    "scope": "../..",
                    "amount": 8
                }]
            }
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
            {
                "index": 0,
                "next": [2]
            },
            {
                "index": 1,
                "entrance": True
            }
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
        "missions": [{
            "index": 1,
            "entry_rules": [{ "scope": "../../Ulnar" }]
        }]
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
# Contains information about every level and map

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import BabaIsYouWorld

from .options import LogicDifficulty
from rule_builder.rules import And, CanReachRegion, Has, HasAny, HasAll, Or, Rule, True_, OptionFilter

hard_logic_filter = [OptionFilter(LogicDifficulty, LogicDifficulty.option_hard)]

def can_win(level : str, logic_diff : int):
    data = LEVEL_DATA.get(level)

    # Clears for maps
    wins = data.get("clearCount")
    if wins != None:
        return Has(f"{level} Win", count=wins)

    rule = data.get("winLogic")
    advRule = data.get("winLogicAdv")
    if (advRule is not None) and (logic_diff != 0):
        rule = advRule
    if rule is None: return True_()
    return rule

LEVEL_DATA = {
    "Map": {
        "name": "Map",
        "map": True,
        "connects": {
            "Map-0": None,
        },
    },
    "Map-0": {
        "name": "Baba Is You",
        "parent": "Map",
        "starting": True,
        "connects": {
            "Map-1": can_win,
        },
    },
    "Map-1": {
        "name": "Where Do I Go?",
        "parent": "Map",
        "starting": True,
        "connects": {
            "Map-2": can_win,
            "Map-3": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Wall", "Stop", "Flag", "Win"), # Basic logic; need all interactable words
        "winLogicAdv": (Has("Win") & HasAny("Wall", "Is", "Stop")) | (Has("Is") & HasAny("Wall, Flag")),
        "defaultWordOnlyDiff": 0, # Set as clearable immediately if we have default words on and the difficulty is >= this
    },
    "Map-2": {
        "name": "Now What Is This?",
        "parent": "Map",
        "starting": True,
        "connects": {
            "Map-1": can_win,
            "Map-4": can_win,
            "Map-5": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Wall", "Stop", "Flag", "Win"),
        "winLogicAdv": (Has("Win") & HasAny("Flag", "Is", "Stop")) | (Has("Is") & HasAny("Flag, Baba")),
        "defaultWordOnlyDiff": 0,
    },
    "Map-3": {
        "name": "Out Of Reach",
        "parent": "Map",
        "starting": True,
        "connects": {
            "Map-1": can_win,
            "Map-4": can_win,
            "Map-6": can_win,
            "Map-Finale": can_win,
        },
        "winLogic": HasAll("Rock", "Is", "Push", "Flag", "Win"),
        "winLogicAdv": HasAll("Push", "Win") | (Has("Rock") & HasAny("Flag", "Win")) | (Has("Is") & HasAny("Win", "Rock", "Flag")),
        "defaultWordOnlyDiff": 0,
    },
    "Map-4": {
        "name": "Still Out Of Reach",
        "parent": "Map",
        "starting": True,
        "connects": {
            "Map-2": can_win,
            "Map-3": can_win,
            "Map-6": can_win,
            "Map-7": can_win,
        },
        "winLogic": HasAll("Rock", "Is", "Push", "Skull", "Defeat"),
        "winLogicAdv": HasAny("Skull", "Is", "Defeat"),
        "defaultWordOnlyDiff": 1,
    },
    "Map-5": {
        "name": "Volcano",
        "parent": "Map",
        "starting": True,
        "connects": {
            "Map-2": can_win,
            "Map-7": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Lava", "Push"),
        "winLogicAdv": HasAll("Baba", "Is", "You") & HasAny("Lava", "Push"),
        "defaultWordOnlyDiff": 1,
    },
    "Map-6": {
        "name": "Off Limits",
        "parent": "Map",
        "starting": True,
        "connects": {
            "Map-3": can_win,
            "Map-4": can_win,
            "Map-7": can_win,
            "Lake": can_win,
            "Map-Finale": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Wall", "Stop"),
        "winLogicAdv": Has("Wall") & HasAny("Is", "Baba"),
        "defaultWordOnlyDiff": 0,
    },
    "Map-7": {
        "name": "Grass Yard",
        "parent": "Map",
        "starting": True,
        "connects": {
            "Map-4": can_win,
            "Map-5": can_win,
            "Map-6": can_win,
            "Lake": can_win,
            "Map-Finale": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Flag", "Win"),
        "winLogicAdv": HasAll("Flag", "Win"),
        "defaultWordOnlyDiff": 0,
    },
    "Map-Finale": {
        "name": "A Way Out?",
        "parent": "Map",
        "winLogic": HasAll("Keke", "Is", "Push", "Belt", "Shift", "Rock", "Win"),
        "winLogicAdv": HasAll("Keke", "Is", "You", "Rock", "Push"),
    },
    "Lake": {
        "name": "1. The Lake",
        "parent": "Map",
        "key": "Lake Key",
        "map": True,
        "connects": {
            "Map": None,
            "Lake-1": None,
            "Island": can_win,
        },
        "clearCount": 8,
        "completeCount": 15,
    },
    "Lake-1": {
        "name": "Icy Waters",
        "parent": "Lake",
        "starting": True,
        "connects": {
            "Lake": None,
            "Lake-2": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "And", "Sink", "Wall"),
        "winLogicAdv": Has("Sink"),
    },
    "Lake-2": {
        "name": "Turns",
        "parent": "Lake",
        "connects": {
            "Lake-3": can_win,
            "Lake-4": can_win,
        },
        "winLogic": HasAll("Star", "Is", "Sink", "And", "Rock", "Push", "Crab"),
        "winLogicAdv": Has("Crab") & HasAny("Is", "And") & (HasAny("Rock", "Star", "Sink") | HasAll("Push", "And")),
    },
    "Lake-3": {
        "name": "Affection",
        "parent": "Lake",
        "connects": {
            "Lake-2": can_win,
            "Lake-5": can_win,
        },
        "winLogic": HasAll("Keke", "Is", "Move", "Love", "Push"),
        "winLogicAdv": (Has("Is") & HasAny("Keke", "Move", "Push", "Love")) | (HasAny("Keke", "Move") & HasAny("Love", "Push")),
        "defaultWordOnlyDiff": 1,
    },
    "Lake-4": {
        "name": "Pillar Yard",
        "parent": "Lake",
        "connects": {
            "Lake-2": can_win,
            "Lake-5": can_win,
            "Lake-6": can_win,
            "Lake-8": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Pillar", "Push"),
        "winLogicAdv": Has("Pillar") & HasAny("Baba", "Is"),
    },
    "Lake-5": {
        "name": "Brick Wall",
        "parent": "Lake",
        "connects": {
            "Lake-3": can_win,
            "Lake-4": can_win,
            "Lake-Extra 1": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Flag", "Win"),
        "winLogicAdv": HasAll("Is", "Win"),
        "defaultWordOnlyDiff": 0,
    },
    "Lake-6": {
        "name": "Lock",
        "parent": "Lake",
        "connects": {
            "Lake-4": can_win,
            "Lake-7": can_win,
            "Lake-8": can_win,
            "Lake-10": can_win,
        },
        "winLogic": HasAll("Key", "Is", "Open", "Push", "Rock"),
        "winLogicAdv": HasAll("Rock", "Is"),
        "defaultWordOnlyDiff": 1,
    },
    "Lake-7": {
        "name": "Novice Locksmith",
        "parent": "Lake",
        "connects": {
            "Lake-6": can_win,
            "Lake-13": can_win,
        },
        "winLogic": HasAll("Key", "Is", "Open", "Push", "Door", "Shut"),
        "winLogicAdv": HasAll("Key", "Is") & HasAny("Open", "Push"),
    },
    "Lake-8": {
        "name": "Locked In",
        "parent": "Lake",
        "connects": {
            "Lake-4": can_win,
            "Lake-6": can_win,
            "Lake-9": can_win,
        },
        "winLogic": HasAll("Wall", "Is", "Stop", "Jelly", "Baba", "You", "Flag", "Win"),
        "winLogicAdv": (Has("Jelly") & HasAny("Wall", "Stop") & HasAny("Flag", "Is", "Win")) | (HasAll("Wall", "Is") & HasAny("Flag", "Win")),
    },
    "Lake-9": {
        "name": "Changeless",
        "parent": "Lake",
        "connects": {
            "Lake-8": can_win,
            "Lake-11": can_win,
        },
        "winLogic": HasAll("Flag", "Is", "Rock"),
        "winLogicAdv": HasAll("Is", "Rock"),
        "defaultWordOnlyDiff": 0,
    },
    "Lake-10": {
        "name": "Two Doors",
        "parent": "Lake",
        "connects": {
            "Lake-6": can_win,
            "Lake-13": can_win,
        },
        "winLogic": HasAll("Keke", "Is", "You", "Door", "Shut", "Flag"),
        "winLogicAdv": HasAll("Flag", "Door", "Is") & HasAny("Keke", "Shut", "You"),
    },
    "Lake-11": {
        "name": "Jelly Throne",
        "parent": "Lake",
        "connects": {
            "Lake-9": can_win,
            "Lake-12": can_win,
        },
        "winLogic": HasAll("Flag", "Is", "Push", "Jelly", "Stop", "Win"),
        "winLogicAdv": HasAll("Jelly", "Is", "Flag"),
    },
    "Lake-12": {
        "name": "Crab Storage",
        "parent": "Lake",
        "connects": {
            "Lake-11": can_win,
        },
        "winLogic": HasAll("Flag", "Is", "Push", "Baba", "Open", "Crab"),
        "winLogicAdv": HasAll("Crab", "Is", "Baba") & HasAny("Push", "Open", "Flag"),
    },
    "Lake-13": {
        "name": "Burglary",
        "parent": "Lake",
        "connects": {
            "Lake-7": can_win,
            "Lake-10": can_win,
        },
        "winLogic": HasAll("Key", "Is", "Open", "Shut"),
        "winLogicAdv": HasAll("Key", "Is") & HasAny("Star", "Stop", "Open", "Shut"),
    },
    "Lake-Extra 1": {
        "name": "Submerged Ruins",
        "parent": "Lake",
        "connects": {
            "Lake-5": can_win,
            "Lake-Extra 2": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Crab", "Flag", "Rock", "Push"),
        "winLogicAdv": HasAll("Crab", "Flag", "Rock") & (Has("Is") | HasAll("Baba", "Push"))
    },
    "Lake-Extra 2": {
        "name": "Sunken Temple",
        "parent": "Lake",
        "connects": {
            "Lake-Extra 1": can_win,
        },
        "winLogic": HasAll("Baba", "Is", "You", "Crab", "Flag", "Rock", "Push"),
        "winLogicAdv": HasAll("Crab", "Flag", "Rock", "Is", "Baba", "Push")
    },
    "Island": {
        "name": "2. Solitary Island",
        "map": True,
        "parent": "Map",
        "key": "Island Key",
        "clearCount": 8,
        "completeCount": 18,
        "connects": {
            "Lake": None,
            "Island-0": None,
            "Island-1": None,
            "Ruins": can_win,
            "Fall": can_win,
        },
    },
    "Island-0": {
        "name": "Poem",
        "parent": "Island",
        "starting": True,
        "winLogic": HasAll("Rose", "Is", "Red", "Violet", "Blue", "Flag", "Win", "Baba", "You"),
        "winLogicAdv": HasAll("Rose", "Is", "Violet"),
        "connects": {
            "Island": None,
        },
    },
    "Island-1": {
        "name": "Float",
        "parent": "Island",
        "starting": True,
        "winLogic": HasAll("Baba", "Is", "You", "Flag", "Win", "Wall", "Stop", "Rock", "Push"),
        "winLogicAdv": Has("Is") & (HasAll("Flag", "Win") | HasAll("Wall", "Stop") | HasAll("Rock", "Push")),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Island": None,
            "Island-2": can_win,
        },
    },
    "Island-2": {
        "name": "Warm River",
        "parent": "Island",
        "winLogic": HasAll("Baba", "Is", "You", "And", "Float"),
        "winLogicAdv": Has("And") & (Has("Float") | HasAll("Baba", "Is", "You")),
        "connects": {
            "Island-1": can_win,
            "Island-3": can_win,
            "Island-Extra 1": can_win,
        },
    },
    "Island-3": {
        "name": "Bridge Building",
        "parent": "Island",
        "winLogic": HasAll("Is", "You", "Rock", "Push", "Flag", "Win"),
        "winLogicAdv": Has("Is"),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Island-2": can_win,
            "Island-4": can_win,
        },
    },
    "Island-4": {
        "name": "Bridge Building?", # NOT the same as the previous level
        "parent": "Island",
        "winLogic": HasAll("Is", "You", "Rock", "Push", "Flag", "Win"),
        "winLogicAdv": HasAll("Rock", "Push") | HasAll("Rock", "Is") | HasAll("Is", "Push") | HasAll("Flag", "Is", "Win"),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Island-3": can_win,
            "Island-5": can_win,
            "Island-Extra 2": can_win,
        },
    },
    "Island-5": {
        "name": "Victory Spring",
        "parent": "Island",
        "winLogic": HasAll("Text", "Is", "Float", "Win"), # min logic
        "connects": {
            "Island-4": can_win,
            "Island-6": can_win,
            "Island-8": can_win,
        },
    },
    "Island-6": {
        "name": "Assembly Team",
        "parent": "Island",
        "winLogic": HasAll("Baba", "Is", "You"),
        "winLogicAdv": HasAll("Is", "You"),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Island-5": can_win,
            "Island-7": can_win,
        },
    },
    "Island-7": {
        "name": "Catch The Thief!",
        "parent": "Island",
        "winLogic": HasAll("Baba", "Is", "You", "Robot", "Move", "Win"),
        "winLogicAdv": HasAll("Baba", "Is", "Robot", "Win"),
        "connects": {
            "Island-6": can_win,
            "Island-8": can_win,
            "Island-9": can_win,
            "Island-11": can_win,
        },
    },
    "Island-8": {
        "name": "Tiny Pond",
        "parent": "Island",
        "winLogic": HasAll("Baba", "Is", "You", "And", "Open", "Flag", "Key", "Win"),
        "winLogicAdv": HasAll("Baba", "Is", "You", "And", "Open", "Flag", "Key"),
        "connects": {
            "Island-5": can_win,
            "Island-7": can_win,
            "Island-10": can_win,
            "Island-Extra 3": can_win,
        },
    },
    "Island-9": {
        "name": "Research Facility",
        "parent": "Island",
        "winLogic": HasAll("Bolt", "Is", "Push", "Move", "Defeat", "Skull", "Hot", "Win"),
        "winLogicAdv": HasAll("Defeat", "Hot", "Win", "Skull") & (HasAll("Bolt", "Move") | HasAll("Move", "Push") | HasAll("Bolt", "Push", "Is") | HasAll("Move", "Is")),
        "connects": {
            "Island-7": can_win,
            "Island-10": can_win,
            "Island-11": can_win,
            "Island-Extra 6": can_win,
        },
    },
    "Island-10": {
        "name": "Wireless Connection",
        "parent": "Island",
        "winLogic": HasAll("Cog", "Is", "Stop", "Move", "And", "Robot", "Push"),
        "winLogicAdv": HasAll("Is", "And") & (HasAny("Robot", "Cog") | HasAll("Move", "Push")),
        "connects": {
            "Island-8": can_win,
            "Island-9": can_win,
            "Island-Extra 4": can_win,
        },
    },
    "Island-11": {
        "name": "Prison",
        "parent": "Island",
        "winLogic": HasAll("Baba", "Is", "You", "Keke", "Push", "Wall", "Stop", "Win"),
        "winLogicAdv": HasAll("Baba", "Is", "Keke", "Push", "Wall", "Stop"),
        "connects": {
            "Island-7": can_win,
            "Island-9": can_win,
            "Island-Extra 5": can_win,
            "Island-Extra 6": can_win,
        },
    },
    "Island-Extra 1": {
        "name": "Boiling River",
        "parent": "Island",
        "winLogic": HasAll("Baba", "Is", "You", "And", "Float"), # min logic
        "connects": {
            "Island-2": can_win,
        },
    },
    "Island-Extra 2": {
        "name": "...Bridges?",
        "parent": "Island",
        "winLogic": HasAll("Is", "You", "Rock", "Push", "Flag", "Win"),
        "winLogicAdv": Has("Is") & (HasAll("Win", "Rock") | HasAll("Win", "Push") | HasAll("Push", "Rock") | HasAll("Rock", "Flag") | HasAll("Push", "Flag") | HasAll("Rock", "You")),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Island-4": can_win,
        },
    },
    "Island-Extra 3": {
        "name": "Tiny Isle",
        "parent": "Island",
        "winLogic": HasAll("Baba", "Is", "You", "And", "Open", "Flag", "Key", "Win"),
        "winLogicAdv": HasAll("Baba", "Is", "You", "And", "Open", "Flag", "Key"),
        "connects": {
            "Island-8": can_win,
        },
    },
    "Island-Extra 4": {
        "name": "Dim Signal",
        "parent": "Island",
        "winLogic": HasAll("Cog", "Is", "Stop", "Move", "And", "Robot", "Push"),
        "winLogicAdv": HasAll("Is", "And") & (HasAll("Move", "Push") | HasAll("Robot", "Cog") | (((HasAny("Robot", "Cog") & HasAny("Push", "Move", "Stop")) | HasAll("Move", "Stop")) & hard_logic_filter)),
        "connects": {
            "Island-10": can_win,
        },
    },
    "Island-Extra 5": {
        "name": "Dungeon",
        "parent": "Island",
        "winLogic": HasAll("Baba", "Is", "You", "Keke", "Wall", "Stop", "Win"),
        "winLogicAdv": HasAll("Is", "Keke", "Wall", "Stop"),
        "connects": {
            "Island-11": can_win,
        },
    },
    "Island-Extra 6": {
        "name": "Evaporating River",
        "parent": "Island",
        "winLogic": HasAll("Water", "Is", "Sink", "Flag"), # min logic
        "connects": {
            "Island-9": can_win,
            "Island-11": can_win,
        },
    },
    "Ruins": {
        "name": "3. Temple Ruins",
        "map": True,
        "parent": "Map",
        "key": "Ruins Key",
        "clearCount": 6,
        "completeCount": 10,
        "connects": {
            "Island": None,
            "Ruins-1": None,
            #"Map-8": can_win,
            "Forest": can_win,
            "Space": can_win,
            "Garden": can_win,
            "Cavern": can_win,
        },
    },
    "Ruins-1": {
        "name": "Fragility",
        "parent": "Ruins",
        "starting": True,
        "winLogic": HasAll("Baba", "Is", "You", "Weak"),
        "winLogicAdv": HasAll("Is", "Weak"),
        "connects": {
            "Ruins": None,
            "Ruins-2": can_win,
        },
    },
    "Ruins-2": {
        "name": "Tunnel Vision",
        "parent": "Ruins",
        "winLogic": HasAll("Baba", "Has", "Rock", "Is", "Move"),
        "winLogicAdv": HasAny("Baba", "Rock") & HasAny("Is", "Has"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Ruins-1": can_win,
            "Ruins-3": can_win,
        },
    },
    "Ruins-3": {
        "name": "A Present For You",
        "parent": "Ruins",
        "winLogic": HasAll("Love", "Is", "You", "Box", "Push", "Water", "Hot", "Melt"),
        "winLogicAdv": Has("Box") & (Has("Love") | HasAll("Is", "You")),
        "connects": {
            "Ruins-2": can_win,
            "Ruins-4": can_win,
            "Ruins-5": can_win,
            "Ruins-6": can_win,
        },
    },
    "Ruins-4": {
        "name": "Unreachable Shores",
        "parent": "Ruins",
        "winLogic": HasAll("Box", "Is", "Push", "Keke", "Has", "Love"),
        "winLogicAdv": HasAny("Keke", "Is") & HasAll("Box", "Has"),
        "connects": {
            "Ruins-3": can_win,
            "Ruins-7": can_win,
        },
    },
    "Ruins-5": {
        "name": "But Where's The Key",
        "parent": "Ruins",
        "winLogic": HasAll("Box", "Is", "Weak", "And", "Has", "Key", "Baba", "You"),
        "winLogicAdv": HasAll("Is", "Weak", "Has", "Box") & (Has("And" & HasAny("Key", "You")) | (HasAll("Baba", "You") & hard_logic_filter)),
        "connects": {
            "Ruins-3": can_win,
            "Ruins-9": can_win,
        },
    },
    "Ruins-6": {
        "name": "Love Is Out There",
        "parent": "Ruins",
        "winLogic": HasAll("Box", "Is", "Push", "And", "Has", "Key", "Weak"),
        "winLogicAdv": HasAll("Box", "Is", "Push", "And", "Key", "Weak"),
        "connects": {
            "Ruins-3": can_win,
            "Ruins-7": can_win,
            "Ruins-8": can_win,
            "Ruins-9": can_win,
        },
    },
    "Ruins-7": {
        "name": "Perilous Gang",
        "parent": "Ruins",
        "winLogic": HasAll("Ghost", "Is", "Push", "Move", "Skull", "Defeat", "Flag", "Win"),
        "winLogicAdv": Has("Is") & ((Has("Ghost") & (HasAny("Push", "Move"))) | (HasAll("Push", "Move") & (HasAny("Skull", "Flag", "Win")))),
        "connects": {
            "Ruins-4": can_win,
            "Ruins-6": can_win,
        },
    },
    "Ruins-8": {
        "name": "Double Moat",
        "parent": "Ruins",
        "winLogic": HasAll("Baba", "Is", "You", "Has", "Keke", "Move"),
        "winLogicAdv": HasAll("Baba", "Is", "Keke", "Has") & HasAny("You", "Move"),
        "connects": {
            "Ruins-6": can_win,
            "Ruins-9": can_win,
            "Ruins-Extra 1": can_win,
        },
    },
    "Ruins-9": {
        "name": "Walls Of Gold",
        "parent": "Ruins",
        "winLogic": HasAll("Wall", "Is", "Win", "Rock"),
        "winLogicAdv": HasAny("Rock", "Wall") & HasAll("Is", "Win"),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Ruins-8": can_win,
            "Ruins-Extra 1": can_win,
        },
    },
    "Ruins-Extra 1": {
        "name": "Further Fields",
        "parent": "Ruins",
        "winLogic": HasAll("Baba", "Is", "Move", "Keke", "You", "Push"),
        "winLogicAdv": HasAll("Keke", "Is", "You") & (Has("Push") | HasAll("Baba", "Move")),
        "connects": {
            "Ruins-8": can_win,
            "Ruins-9": can_win,
        },
    },
    "Fall": {
        "name": "4. Forest Of Fall",
        "map": True,
        "parent": "Map",
        "key": "Fall Key",
        "clearCount": 7,
        "completeCount": 20,
        "connects": {
            "Island": None,
            "Fall-1": None,
        },
    },
    "Fall-1": {
        "name": "Hop",
        "parent": "Fall",
        "starting": True,
        "winLogic": HasAll("Love", "Is", "Tele", "Push"),
        "winLogicAdv": Has("Push") & HasAny("Love", "Is", "Tele"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Fall": None,
            "Fall-2": can_win,
            "Fall-3": can_win,
            "Fall-Extra 1": can_win,
        },
    },
    "Fall-2": {
        "name": "Grand Stream",
        "parent": "Fall",
        "winLogic": HasAll("Key", "Is", "Pull", "Keke"),
        "winLogicAdv": HasAll("Key", "Is", "Pull"),
        "connects": {
            "Fall-1": can_win,
            "Fall-5": can_win,
            "Fall-7": can_win,
        },
    },
    "Fall-3": {
        "name": "Rocky Road",
        "parent": "Fall",
        "winLogic": HasAll("Love", "Is", "Tele", "Push"),
        "winLogicAdv": HasAny("Is", "Push"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Fall-1": can_win,
            "Fall-4": can_win,
        },
    },
    "Fall-4": {
        "name": "Telephone",
        "parent": "Fall",
        "winLogic": HasAll("Baba", "Is", "You", "Ice", "Tele", "Key", "Push"),
        "connects": {
            "Fall-3": can_win,
            "Fall-5": can_win,
            "Fall-8": can_win,
            "Fall-10": can_win,
            "Fall-11": can_win,
        },
    },
    "Fall-5": {
        "name": "Haunt",
        "parent": "Fall",
        "winLogic": HasAll("Leaf", "Is", "Defeat", "Baba", "You", "Ghost", "Tele", "Push"),
        "connects": {
            "Fall-2": can_win,
            "Fall-4": can_win,
            "Fall-6": can_win,
        },
    },
    "Fall-6": {
        "name": "Crate Square",
        "parent": "Fall",
        "winLogic": HasAll("Hot", "Defeat", "Win", "And"),
        "connects": {
            "Fall-5": can_win,
            "Fall-7": can_win,
            "Fall-8": can_win,
            "Fall-9": can_win,
            "Fall-A": can_win,
            "Fall-B": can_win,
        },
    },
    "Fall-7": {
        "name": "Ghost Friend",
        "parent": "Fall",
        "winLogic": HasAll("Ghost", "Is", "Pull", "Move", "Flag"),
        "winLogicAdv": HasAll("Flag", "Is"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Fall-2": can_win,
            "Fall-6": can_win,
        },
    },
    "Fall-8": {
        "name": "Ghost Guard",
        "parent": "Fall",
        "winLogic": HasAll("Rock", "Is", "Push", "Leaf", "Tele"),
        "connects": {
            "Fall-4": can_win,
            "Fall-6": can_win,
            "Fall-9": can_win,
        },
    },
    "Fall-9": {
        "name": "Leaf Chamber",
        "parent": "Fall",
        "winLogic": HasAll("Leaf", "Is", "Move", "Key", "Push", "Pull"),
        "connects": {
            "Fall-6": can_win,
            "Fall-8": can_win,
            "Fall-A": can_win,
            "Fall-B": can_win,
        },
    },
    "Fall-10": {
        "name": "Not There",
        "parent": "Fall",
        "winLogic": HasAll("Baba", "Is", "You", "Stop", "Fence", "Not", "Win"),
        "connects": {
            "Fall-4": can_win,
            "Fall-11": can_win,
            "Fall-12": can_win,
            "Fall-Extra 2": can_win,
        },
    },
    "Fall-11": {
        "name": "Catch",
        "parent": "Fall",
        "winLogic": HasAll("Not", "Rock", "Is", "Push", "Baba", "You"),
        "connects": {
            "Fall-4": can_win,
            "Fall-10": can_win,
            "Fall-12": can_win,
        },
    },
    "Fall-12": {
        "name": "Dead End",
        "parent": "Fall",
        "winLogic": HasAll("Flag", "Is", "Not", "Box"),
        "connects": {
            "Fall-10": can_win,
            "Fall-11": can_win,
        },
    },
    "Fall-A": {
        "name": "Literacy",
        "parent": "Fall",
        "winLogic": HasAll("Me", "Is", "You", "Text", "Wall"),
        "connects": {
            "Fall-6": can_win,
            "Fall-9": can_win,
            "Fall-B": can_win,
        },
    },
    "Fall-B": {
        "name": "Broken Playground",
        "parent": "Fall",
        "winLogic": HasAll("Box", "Text", "Flag", "Keke", "Is", "You", "Win"),
        "connects": {
            "Fall-6": can_win,
            "Fall-9": can_win,
            "Fall-A": can_win,
            "Fall-C": can_win,
            "Fall-D": can_win,
        },
    },
    "Fall-C": {
        "name": "Fetching",
        "parent": "Fall",
        "winLogic": HasAll("Text", "Is", "Push", "Keke", "Hot", "Flag"), # Reevaluate if we decide to make unobtained text "safe"
        "connects": {
            "Fall-A": can_win,
            "Fall-B": can_win,
            "Fall-E": can_win,
        },
    },
    "Fall-D": {
        "name": "Scenic Pond",
        "parent": "Fall",
        "winLogic": HasAll("Baba", "Is", "You", "Keke", "Has", "Text", "Float", "Flag"),
        "connects": {
            "Fall-B": can_win,
            "Fall-E": can_win,
            "Fall-Extra 3": can_win,
        },
    },
    "Fall-E": {
        "name": "Skeletal Door",
        "parent": "Fall",
        "winLogic": HasAll("Baba", "Is", "You", "Text", "Push"), # min logic
        "connects": {
            "Fall-C": can_win,
            "Fall-D": can_win,
        },
    },
    "Fall-Extra 1": {
        "name": "Jump",
        "parent": "Fall",
        "winLogic": HasAll("Love", "Is", "Tele", "Push"),
        "winLogicAdv": Has("Push") & HasAny("Love", "Is", "Tele"),
        "connects": {
            "Fall-1": can_win,
        },
    },
    "Fall-Extra 2": {
        "name": "Even Less There",
        "parent": "Fall",
        "winLogic": HasAll("Baba", "Is", "You", "Stop", "Fence", "Not", "Win"),
        "connects": {
            "Fall-10": can_win,
        },
    },
    "Fall-Extra 3": {
        "name": "Deep Pool",
        "parent": "Fall",
        "winLogic": HasAll("Baba", "Is", "You", "Keke", "Has", "Text", "Flag"),
        "connects": {
            "Fall-D": can_win,
        },
    },
    "Forest": {
        "name": "5. Deep Forest",
        "map": True,
        "parent": "Map",
        "key": "Forest Key",
        "clearCount": 9,
        "completeCount": 21,
        "connects": {
            "Ruins": None,
            "Space": None,
            "Forest-1": None,
            "Chasm": can_win,
        },
    },
    "Forest-1": {
        "name": "Renovating",
        "parent": "Forest",
        "starting": True,
        "winLogic": HasAll("Belt", "Is", "Shift", "Push"),
        "winLogicAdv": (Has("Push") & HasAny("Belt", "Is", "Shift")) | HasAll("Belt", "Is"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Forest": None,
            "Forest-2": can_win,
            "Forest-3": can_win,
            "Forest-4": can_win,
        },
    },
    "Forest-2": {
        "name": "Toolshed",
        "parent": "Forest",
        "winLogic": HasAll("Key", "Is", "Open", "Door", "Shut"),
        "connects": {
            "Forest-1": can_win,
            "Forest-4": can_win,
            "Forest-5": can_win,
            "Forest-6": can_win,
        },
    },
    "Forest-3": {
        "name": "Keep Out!",
        "parent": "Forest",
        "winLogic": HasAll("Tree", "Is", "Pull"),
        "connects": {
            "Forest-1": can_win,
            "Forest-7": can_win,
            "Forest-9": can_win,
        },
    },
    "Forest-4": {
        "name": "Baba Doesn't Respond",
        "parent": "Forest",
        "winLogic": HasAll("Baba", "Is", "Push", "Shut", "Defeat"),
        "connects": {
            "Forest-1": can_win,
            "Forest-2": can_win,
            "Forest-5": can_win,
            "Forest-10": can_win,
        },
    },
    "Forest-5": {
        "name": "Patrol",
        "parent": "Forest",
        "winLogic": HasAll("Tree", "Is", "Push", "Door", "Sink", "Has"),
        "connects": {
            "Forest-2": can_win,
            "Forest-4": can_win,
            "Forest-13": can_win,
        },
    },
    "Forest-6": {
        "name": "Canyon",
        "parent": "Forest",
        "winLogic": HasAll("Belt", "Is", "Shift", "Up"),
        "connects": {
            "Forest-2": can_win,
            "Forest-8": can_win,
        },
    },
    "Forest-7": {
        "name": "Concrete Goals",
        "parent": "Forest",
        "winLogic": HasAll("Belt", "Is", "Shift", "Push", "Wall", "Stop"),
        "winLogicAdv": HasAll("Is", "Push"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Forest-3": can_win,
            "Forest-12": can_win,
            "Forest-A": can_win,
        },
    },
    "Forest-8": {
        "name": "Victory In The Open",
        "parent": "Forest",
        "winLogic": HasAll("Keke", "Is", "Move", "Right", "Win"),
        "winLogicAdv": HasAll("Keke", "Is", "Win"),
        "connects": {
            "Forest-6": can_win,
            "Forest-11": can_win,
        },
    },
    "Forest-9": {
        "name": "Moving Floor",
        "parent": "Forest",
        "winLogic": HasAll("Flag", "Is", "Push", "Win"), # min logic
        "connects": {
            "Forest-3": can_win,
            "Forest-12": can_win,
            "Forest-Extra 1": can_win,
        },
    },
    "Forest-10": {
        "name": "Lovely House",
        "parent": "Forest",
        "winLogic": HasAll("Baba", "Is", "You", "Key", "And", "Rock", "Push"),
        "winLogicAdv": Has("Is") & ((HasAll("Baba", "You") & HasAny("Rock", "Key")) | HasAll("Rock", "And", "Key")),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Forest-4": can_win,
            "Forest-13": can_win,
            "Forest-14": can_win,
            "Forest-Extra 2": can_win,
        },
    },
    "Forest-11": {
        "name": "Supermarket",
        "parent": "Forest",
        "winLogic": HasAll("Belt", "Is", "Right", "Up", "Wall", "Win"),
        "connects": {
            "Forest-8": can_win,
        },
    },
    "Forest-12": {
        "name": "Lock The Door",
        "parent": "Forest",
        "winLogic": HasAll("Bug", "Is", "Push", "Belt", "Shift", "Fungus", "Love"),
        "connects": {
            "Forest-7": can_win,
            "Forest-9": can_win,
        },
    },
    "Forest-13": {
        "name": "Factory",
        "parent": "Forest",
        "winLogic": HasAll("Box", "Has", "Key", "Is", "You", "And", "Weak"),
        "connects": {
            "Forest-5": can_win,
            "Forest-10": can_win,
            "Forest-14": can_win,
        },
    },
    "Forest-14": {
        "name": "Tiny Pasture",
        "parent": "Forest",
        "winLogic": HasAll("Keke", "Is", "Push", "Flag", "Tele", "Shift", "Win"),
        "connects": {
            "Forest-10": can_win,
            "Forest-13": can_win,
            "Forest-Extra 2": can_win,
        },
    },
    "Forest-Extra 1": {
        "name": "Crumbling Floor",
        "parent": "Forest",
        "winLogic": HasAll("Flag", "Is", "Push", "Win"), # min logic
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Forest-9": can_win,
        },
    },
    "Forest-Extra 2": {
        "name": "Skull House",
        "parent": "Forest",
        "winLogic": HasAll("Baba", "Is", "You", "Key", "Rock", "Push"),
        "winLogicAdv": Has("Is") & ((HasAll("Baba", "You") & HasAny("Rock", "Key")) | HasAll("Rock", "Key")),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Forest-10": can_win,
            "Forest-14": can_win,
        },
    },
    "Forest-A": {
        "name": "Nearly",
        "parent": "Forest",
        "winLogic": HasAll("Baba", "Is", "You", "Flag", "Win", "Swap"),
        "winLogicAdv": HasAny("Baba", "Is", "Win", "Swap"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Forest-B": can_win,
            "Forest-C": can_win,
        },
    },
    "Forest-B": {
        "name": "Not Quite",
        "parent": "Forest",
        "winLogic": HasAll("Baba", "Is", "You", "Flag", "Win", "Swap"),
        "winLogicAdv": HasAny("Flag", "Win"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Forest-A": can_win,
            "Forest-D": can_win,
        },
    },
    "Forest-C": {
        "name": "Passing Through",
        "parent": "Forest",
        "winLogic": HasAll("Keke", "Is", "Push", "Skull", "Move"),
        "connects": {
            "Forest-A": can_win,
            "Forest-D": can_win,
        },
    },
    "Forest-D": {
        "name": "Salvage",
        "parent": "Forest",
        "winLogic": HasAll("Text", "Flag", "Is", "Win", "Swap", "And", "Pull"),
        "winLogicAdv": HasAll("Text", "Is", "Swap", "And", "Pull"),
        "connects": {
            "Forest-B": can_win,
            "Forest-C": can_win,
            "Forest-E": can_win,
        },
    },
    "Forest-E": {
        "name": "Insulation",
        "parent": "Forest",
        "winLogic": HasAll("Keke", "Is", "Push", "Up", "Skull", "Wall"),
        "connects": {
            "Forest-B": can_win,
            "Forest-C": can_win,
            "Forest-E": can_win,
        },
    },
    "Space": {
        "name": "6. Rocket Trip",
        "map": True,
        "parent": "Map",
        "key": "Space Key",
        "clearCount": 8,
        "completeCount": 15,
        "connects": {
            "Ruins": None,
            "Forest": None,
            "Space-1": None,
            "Space-4": None,
        },
    },
    "Space-1": {
        "name": "Empty",
        "parent": "Space",
        "starting": True,
        "winLogic": HasAll("Is", "Empty"), # min logic
        "connects": {
            "Space": None,
            "Space-2": can_win,
            "Space-5": can_win,
        },
    },
    "Space-2": {
        "name": "Lonely Flag",
        "parent": "Space",
        "winLogic": HasAll("Is", "Empty"), # min logic
        "connects": {
            "Space-1": can_win,
            "Space-3": can_win,
        },
    },
    "Space-3": {
        "name": "Babas Are You",
        "parent": "Space",
        "winLogic": HasAll("Rock", "Is", "Push", "Ice", "Win"),
        "connects": {
            "Space-2": can_win,
            "Space-5": can_win,
            "Space-8": can_win,
        },
    },
    "Space-4": {
        "name": "Please Hold My Key",
        "parent": "Space",
        "starting": True,
        "winLogic": HasAll("Baba", "Is", "You", "Key", "Open"),
        "winLogicAdv": HasAll("Baba", "Is", "You", "Key"),
        "connects": {
            "Space": None,
            "Space-6": can_win,
            "Space-7": can_win,
        },
    },
    "Space-5": {
        "name": "Horror Story",
        "parent": "Space",
        "winLogic": HasAll("Baba", "Is", "You", "Empty"), # min logic
        "connects": {
            "Space-1": can_win,
            "Space-3": can_win,
            "Space-Extra 1": can_win,
        },
    },
    "Space-6": {
        "name": "Aiming High",
        "parent": "Space",
        "winLogic": HasAll("Baba", "Is", "You", "Cloud", "Stop"),
        "winLogicAdv": Has("Is") & (HasAll("Baba", "You") | HasAny("Cloud", "Stop")),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Space-4": can_win,
            "Space-9": can_win,
            "Space-11": can_win,
        },
    },
    "Space-7": {
        "name": "Trio",
        "parent": "Space",
        "winLogic": HasAll("Me", "Is", "Push", "And", "Keke", "Move", "Skull", "Defeat"),
        "connects": {
            "Space-4": can_win,
            "Space-9": can_win,
        },
    },
    "Space-8": {
        "name": "Bottleneck",
        "parent": "Space",
        "winLogic": HasAll("Star", "And", "Rocket", "Is", "Push", "Empty", "Win", "Defeat"),
        "connects": {
            "Space-3": can_win,
            "Space-12": can_win,
        },
    },
    "Space-9": {
        "name": "Platformer",
        "parent": "Space",
        "winLogic": HasAll("Rocket", "And", "UFO", "Open"), # min logic
        "connects": {
            "Space-6": can_win,
            "Space-7": can_win,
            "Space-10": can_win,
        },
    },
    "Space-10": {
        "name": "The Pit",
        "parent": "Space",
        "winLogic": HasAll("Moon", "Is", "You", "And", "Star", "Fall", "Push"),
        "connects": {
            "Space-9": can_win,
            "Space-11": can_win,
        },
    },
    "Space-11": {
        "name": "Heavy Words",
        "parent": "Space",
        "winLogic": HasAll("Star", "Is", "Push", "Win", "Moon", "Weak", "Dust"),
        "connects": {
            "Space-6": can_win,
            "Space-10": can_win,
            "Space-Extra 2": can_win,
        },
    },
    "Space-12": {
        "name": "Guardians",
        "parent": "Space",
        "winLogic": HasAll("Empty", "Is", "Text", "Pull", "Ice", "Win"),
        "connects": {
            "Space-5": can_win,
            "Space-8": can_win,
            "Space-13": can_win,
        },
    },
    "Space-13": {
        "name": "Sky Hold",
        "parent": "Space",
        "winLogic": HasAll("Has", "Key", "Is", "Shut", "Empty"),
        "connects": {
            "Space-12": can_win,
        },
    },
    "Space-Extra 1": {
        "name": "Existential Crisis",
        "parent": "Space",
        "winLogic": HasAll("Baba", "Is", "You", "Empty", "Push", "Win"),
        "winLogicAdv": HasAll("Empty", "Is", "You", "Win"),
        "connects": {
            "Space-5": can_win,
        },
    },
    "Space-Extra 2": {
        "name": "Heavy Cloud",
        "parent": "Space",
        "winLogic": HasAll("Star", "Is", "Push", "Win", "Moon", "Weak", "Dust"),
        "connects": {
            "Space-11": can_win,
        },
    },
    "Garden": {
        "name": "7. Flower Garden",
        "map": True,
        "parent": "Map",
        "key": "Garden Key",
        "clearCount": 4,
        "completeCount": 12,
        "connects": {
            "Ruins": None,
            "Cavern": None,
            #"Map-8": None,
            "Garden-1": None,
            "Garden-2": None,
        },
    },
    "Garden-1": {
        "name": "Condition",
        "parent": "Garden",
        "starting": True,
        "winLogic": HasAll("Keke", "Is", "You", "On", "Grass", "Defeat", "Key"),
        "connects": {
            "Garden": None,
            "Garden-3": can_win,
        },
    },
    "Garden-2": {
        "name": "Thicket",
        "parent": "Garden",
        "starting": True,
        "winLogic": HasAll("Moon", "Make", "Flag", "Is", "Open", "Win", "Defeat"),
        "connects": {
            "Garden": None,
            "Garden-6": can_win,
        },
    },
    "Garden-3": {
        "name": "Sorting Facility",
        "parent": "Garden",
        "winLogic": HasAll("Rock", "Is", "Push", "Belt", "On"),
        "connects": {
            "Garden-1": can_win,
            "Garden-4": can_win,
        },
    },
    "Garden-4": {
        "name": "Relaxing Spot",
        "parent": "Garden",
        "winLogic": HasAll("Rock", "Is", "Push", "Keke", "On", "Text", "Flag"),
        "connects": {
            "Garden-3": can_win,
            "Garden-5": can_win,
            "Garden-7": can_win,
            "Garden-Extra 1": can_win,
        },
    },
    "Garden-5": {
        "name": "Maritime Adventures",
        "parent": "Garden",
        "winLogic": HasAll("Baba", "Is", "You", "Hand", "Move", "On", "Wall", "Push", "Defeat"),
        "connects": {
            "Garden-4": can_win,
            "Garden-8": can_win,
            "Garden-9": can_win,
        },
    },
    "Garden-6": {
        "name": "Ruined Orchard",
        "parent": "Garden",
        "winLogic": HasAll("Keke", "Make", "Key", "Is", "Push", "Belt"),
        "connects": {
            "Garden-2": can_win,
            "Garden-8": can_win,
        },
    },
    "Garden-7": {
        "name": "Blockade",
        "parent": "Garden",
        "winLogic": HasAll("Rock", "On", "Pillar", "Is", "Push"),
        "connects": {
            "Garden-4": can_win,
            "Garden-9": can_win,
        },
    },
    "Garden-8": {
        "name": "Jaywalkers United",
        "parent": "Garden",
        "winLogic": HasAll("Flag", "On", "Rock", "Is", "Me", "Push"),
        "connects": {
            "Garden-5": can_win,
            "Garden-6": can_win,
            "Garden-10": can_win,
        },
    },
    "Garden-9": {
        "name": "Overgrowth",
        "parent": "Garden",
        "winLogic": HasAll("Key", "Is", "Push", "On", "Fruit", "Grass", "Baba"),
        "connects": {
            "Garden-5": can_win,
            "Garden-7": can_win,
            "Garden-10": can_win,
            "Garden-Extra 2": can_win,
        },
    },
    "Garden-10": {
        "name": "Adventurers",
        "parent": "Garden",
        "winLogic": HasAll("Hand", "Make", "Belt", "Defeat", "Win"),
        "connects": {
            "Garden-8": can_win,
            "Garden-9": can_win,
        },
    },
    "Garden-Extra 1": {
        "name": "Secret Garden",
        "parent": "Garden",
        "winLogic": HasAll("Rock", "Is", "Keke", "On", "Text", "Flag"),
        "connects": {
            "Garden-4": can_win,
        },
    },
    "Garden-Extra 2": {
        "name": "Out At Sea",
        "parent": "Garden",
        "winLogic": HasAll("Text", "Is", "Push", "Lava", "On", "Ice"),
        "connects": {
            "Garden-9": can_win,
        },
    },
    "Chasm": {
        "name": "8. Chasm",
        "map": True,
        "parent": "Map",
        "key": "Chasm Key",
        "clearCount": 9,
        "completeCount": 16,
        "connects": {
            "Forest": None,
            "Chasm-A": None,
            "Chasm-B": None,
            "Chasm-Extra 1": None,
        },
    },
    "Chasm-A": {
        "name": "Rocky Prison",
        "parent": "Chasm",
        "starting": True,
        "winLogic": HasAll("Skull", "Is", "You", "Water", "Sink", "All", "Win"),
        "connects": {
            "Chasm": None,
            "Chasm-C": can_win,
        },
    },
    "Chasm-B": {
        "name": "Siege",
        "parent": "Chasm",
        "starting": True,
        "winLogic": HasAll("Rock", "Is", "Push", "And", "More", "Baba", "You"),
        "winLogicAdv": HasAll("Is", "More") & HasAny("Rock", "And", "Push"), # definitely not correct
        "connects": {
            "Chasm": None,
            "Chasm-D": can_win,
        },
    },
    "Chasm-C": {
        "name": "Elusive Condition",
        "parent": "Chasm",
        "winLogic": HasAll("Hand", "Is", "Empty", "All"),
        "winLogicAdv": Has("Is") & HasAny("All", "Hand"),
        "connects": {
            "Chasm": None,
            "Chasm-A": can_win,
            "Chasm-E": can_win,
        },
    },
    "Chasm-D": {
        "name": "Treasury",
        "parent": "Chasm",
        "winLogic": HasAll("Rock", "Is", "Push", "More"),
        "winLogicAdv": HasAll("More", "Push"),
        "connects": {
            "Chasm-B": can_win,
            "Chasm-F": can_win,
        },
    },
    "Chasm-E": {
        "name": "Looking For A Heart",
        "parent": "Chasm",
        "winLogic": HasAll("Love", "Is", "Push", "Rock", "Move", "Open", "All"),
        "connects": {
            "Chasm-C": can_win,
            "Chasm-G": can_win,
        },
    },
    "Chasm-F": {
        "name": "Lava Flood",
        "parent": "Chasm",
        "winLogic": HasAll("Flag", "Is", "Win", "Melt"),
        "winLogicAdv": HasAny("Flag", "Is"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Chasm-D": can_win,
            "Chasm-H": can_win,
        },
    },
    "Chasm-G": {
        "name": "Entropy",
        "parent": "Chasm",
        "winLogic": HasAll("Rock", "Has", "Baba", "Is", "You", "Open", "Weak"),
        "connects": {
            "Chasm-E": can_win,
        },
    },
    "Chasm-H": {
        "name": "Floodgates",
        "parent": "Chasm",
        "winLogic": HasAll("Star", "Is", "More", "Love"),
        "connects": {
            "Chasm-F": can_win,
            "Chasm-I": can_win,
        },
    },
    "Chasm-I": {
        "name": "Lonely Sight",
        "parent": "Chasm",
        "winLogic": HasAll("Baba", "Is", "You", "Rock", "Love", "Flag", "More", "On"),
        "connects": {
            "Chasm-H": can_win,
        },
    },
    "Chasm-Extra 1": {
        "name": "Metacognition",
        "parent": "Chasm",
        "starting": True,
        "winLogic": HasAll("Baba", "Is", "You", "Key", "Push", "Word", "Open"),
        "connects": {
            "Chasm": None,
            "Chasm-Extra 2": can_win,
            "Chasm-Extra 3": can_win,
        },
    },
    "Chasm-Extra 2": {
        "name": "Multitool",
        "parent": "Chasm",
        "winLogic": HasAll("Rock", "Is", "Push"), # min logic
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Chasm-Extra 1": can_win,
            "Chasm-Extra 6": can_win,
        },
    },
    "Chasm-Extra 3": {
        "name": "Broken",
        "parent": "Chasm",
        "winLogic": HasAll("Text", "Is", "Not", "Push", "Rock", "Ice", "Tele", "Win"),
        "winLogicAdv": HasAny("Is", "Win"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Chasm-Extra 1": can_win,
            "Chasm-Extra 5": can_win,
        },
    },
    "Chasm-Extra 4": {
        "name": "Alley",
        "parent": "Chasm",
        "winLogic": HasAll("Water", "Is", "Rock", "Push"), # min logic
        "connects": {
            "Chasm-Extra 1": can_win,
            "Chasm-Extra 5": can_win,
            "Chasm-Extra 6": can_win,
            "Chasm-Extra 7": can_win,
        },
    },
    "Chasm-Extra 5": {
        "name": "Keke And The Star",
        "parent": "Chasm",
        "winLogic": HasAll("Lava", "Is", "Word", "Baba", "You", "Keke", "Sleep"),
        "connects": {
            "Chasm-Extra 3": can_win,
            "Chasm-Extra 4": can_win,
        },
    },
    "Chasm-Extra 6": {
        "name": "Visiting Baba",
        "parent": "Chasm",
        "winLogic": HasAll("Fungus", "Is", "Word", "Rock", "Push"),
        "winLogicAdv": HasAll("Rock", "Is"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Chasm-Extra 2": can_win,
            "Chasm-Extra 4": can_win,
        },
    },
    "Chasm-Extra 7": {
        "name": "Automated Doors",
        "parent": "Chasm",
        "winLogic": HasAll("Rock", "Is", "Word", "You", "Not", "Flag"),
        "connects": {
            "Chasm-Extra 4": can_win,
        },
    },
    "Cavern": {
        "name": "9. Volcanic Cavern",
        "map": True,
        "parent": "Map",
        "key": "Cavern Key",
        "clearCount": 9,
        "completeCount": 15,
        "connects": {
            "Ruins": None,
            "Garden": None,
            "Cavern-1": None,
            "Cavern-2": None,
            #"Map-8": None,
            "Mountain": can_win,
        },
    },
    "Cavern-1": {
        "name": "Tour",
        "parent": "Cavern",
        "winLogic": HasAll("Keke", "Is", "You", "Baba", "Flag"),
        "winLogicAdv": HasAll("Keke", "Is", "Baba", "Flag"),
        "connects": {
            "Cavern": None,
            "Cavern-2": None,
            "Cavern-3": can_win,
            "Cavern-4": can_win,
            "Cavern-7": can_win,
        },
    },
    "Cavern-2": {
        "name": "Peril At Every Turn",
        "parent": "Cavern",
        "winLogic": HasAll("Baba", "Is", "You", "Keke", "Push"),
        "connects": {
            "Cavern": None,
            "Cavern-1": None,
            "Cavern-4": can_win,
        },
    },
    "Cavern-3": {
        "name": "Pillarwork",
        "parent": "Cavern",
        "winLogic": HasAll("Baba", "Is", "Pull", "Flag", "Push", "Grass"),
        "connects": {
            "Cavern-1": can_win,
            "Cavern-5": can_win,
            "Cavern-7": can_win,
            "Cavern-11": can_win,
        },
    },
    "Cavern-4": {
        "name": "Mouse Hole",
        "parent": "Cavern",
        "winLogic": HasAll("Bat", "Rock", "Is", "Push"), # min logic
        "connects": {
            "Cavern-1": can_win,
            "Cavern-2": can_win,
            "Cavern-8": can_win,
        },
    },
    "Cavern-5": {
        "name": "Torn Apart",
        "parent": "Cavern",
        "winLogic": HasAll("Baba", "Is", "Group", "You"), # min logic
        "connects": {
            "Cavern-3": can_win,
            "Cavern-6": can_win,
            "Cavern-7": can_win,
            "Cavern-9": can_win,
            "Cavern-11": can_win,
        },
    },
    "Cavern-6": {
        "name": "Vital Ingredients",
        "parent": "Cavern",
        "winLogic": HasAll("Skull", "Is", "Open", "Group", "Bat", "Push"),
        "connects": {
            "Cavern-5": can_win,
            "Cavern-10": can_win,
        },
    },
    "Cavern-7": {
        "name": "Backstage",
        "parent": "Cavern",
        "winLogic": HasAll("Baba", "Is", "You", "Keke", "Ghost", "Push", "Flag", "Win"),
        "connects": {
            "Cavern-1": can_win,
            "Cavern-3": can_win,
            "Cavern-5": can_win,
            "Cavern-8": can_win,
            "Cavern-11": can_win,
            "Cavern-14": can_win,
            "Cavern-Extra 1": can_win,
        },
    },
    "Cavern-8": {
        "name": "The Heist",
        "parent": "Cavern",
        "winLogic": HasAll("Flag", "On", "Fire", "Is", "Push", "Text", "Open"),
        "connects": {
            "Cavern-4": can_win,
            "Cavern-7": can_win,
            "Cavern-14": can_win,
            "Cavern-Extra 1": can_win,
        },
    },
    "Cavern-9": {
        "name": "Join The Crew",
        "parent": "Cavern",
        "winLogic": HasAll("Baba", "Is", "Group", "Bat", "Rock"),
        "connects": {
            "Cavern-5": can_win,
            "Cavern-10": can_win,
        },
    },
    "Cavern-10": {
        "name": "Automaton", # NOT "Automation"
        "parent": "Cavern",
        "winLogic": HasAll("Box", "Is", "Me", "Group", "Baba", "Melt", "Defeat"),
        "connects": {
            "Cavern-6": can_win,
            "Cavern-9": can_win,
        },
    },
    "Cavern-11": {
        "name": "Trick Door",
        "parent": "Cavern",
        "winLogic": HasAll("Ghost", "Facing", "Wall", "Is", "Push", "Key", "Not", "Tile", "Flag"),
        "connects": {
            "Cavern-3": can_win,
            "Cavern-5": can_win,
            "Cavern-7": can_win,
            "Cavern-12": can_win,
        },
    },
    "Cavern-12": {
        "name": "Trapped",
        "parent": "Cavern",
        "winLogic": HasAll("Flag", "Belt", "Is", "Shift", "Baba", "Box", "Tele"),
        "connects": {
            "Cavern-11": can_win,
            "Cavern-13": can_win,
        },
    },
    "Cavern-13": {
        "name": "Tunnel",
        "parent": "Cavern",
        "winLogic": HasAll("Skull", "Facing", "Is", "Not"), # min logic
        "connects": {
            "Cavern-12": can_win,
        },
    },
    "Cavern-14": {
        "name": "Broken Expectations",
        "parent": "Cavern",
        "winLogic": HasAll("Text", "Is", "Not", "Push", "Rock", "Win"),
        "connects": {
            "Cavern-7": can_win,
            "Cavern-8": can_win,
            "Cavern-Extra 1": can_win,
        },
    },
    "Cavern-Extra 1": {
        "name": "Coronation",
        "parent": "Cavern",
        "winLogic": HasAll("Rock", "Is", "Win", "Text", "Push", "Swap"),
        "connects": {
            "Cavern-7": can_win,
            "Cavern-8": can_win,
            "Cavern-14": can_win,
        },
    },
    "Mountain": {
        "name": "10. Mountaintop",
        "map": True,
        "parent": "Map",
        "key": "Mountain Key",
        "clearCount": 6,
        "completeCount": 9,
        "connects": {
            "Cavern": None,
            "Mountain-1": None,
        },
    },
    "Mountain-1": {
        "name": "Shuffle",
        "parent": "Mountain",
        "winLogic": HasAll("Lonely", "Baba", "Is", "You", "Skull", "Defeat"), # min logic
        "connects": {
            "Mountain": None,
            "Mountain-2": can_win,
            "Mountain-3": can_win,
        },
    },
    "Mountain-2": {
        "name": "Love At First Sight",
        "parent": "Mountain",
        "winLogic": HasAll("Bird", "Is", "Push", "Flag", "Win"),
        "winLogicAdv": HasAll("Bird", "Is", "Push", "Flag"),
        "connects": {
            "Mountain-1": can_win,
            "Mountain-4": can_win,
        },
    },
    "Mountain-3": {
        "name": "Solitude",
        "parent": "Mountain",
        "winLogic": HasAll("Rock", "Is", "Push", "Lonely", "Key", "Open"),
        "winLogicAdv": HasAll("Rock", "Is", "Push", "Lonely", "Key"),
        "connects": {
            "Mountain-1": can_win,
            "Mountain-4": can_win,
        },
    },
    "Mountain-4": {
        "name": "What Is Baba?",
        "parent": "Mountain",
        "winLogic": HasAll("Baba", "Is", "You", "Win"),
        "winLogicAdv": HasAll("Baba", "Is") & HasAny("You", "Win"),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Mountain-2": can_win,
            "Mountain-3": can_win,
            "Mountain-6": can_win,
            "Mountain-7": can_win,
        },
    },
    "Mountain-5": {
        "name": "Connector",
        "parent": "Mountain",
        "winLogic": HasAll("Sun", "Baba", "Is", "You", "Shut", "Text"), # min logic
        "connects": {
            "Mountain-2": can_win,
            "Mountain-6": can_win,
        },
    },
    "Mountain-6": {
        "name": "Floaty Platforms",
        "parent": "Mountain",
        "winLogic": HasAll("Rock", "Is", "Push"),
        "winLogicAdv": HasAny("Rock", "Is", "Push"),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Mountain-4": can_win,
            "Mountain-5": can_win,
            "Mountain-8": can_win,
            "Mountain-Extra 1": can_win,
        },
    },
    "Mountain-7": {
        "name": "Seeking Acceptance",
        "parent": "Mountain",
        "winLogic": HasAll("Lonely", "Baba", "Is", "Tile", "On", "Flag"), # min logic
        "connects": {
            "Mountain-6": can_win,
            "Mountain-7": can_win,
        },
    },
    "Mountain-8": {
        "name": "Tectonic Movements",
        "parent": "Mountain",
        "winLogic": HasAll("Pillar", "Is", "Push"),
        "winLogicAdv": Has("Is") & HasAny("Pillar", "Push"),
        "defaultWordOnlyDiff": 1,
        "connects": {
            "Mountain-6": can_win,
            "Mountain-7": can_win,
        },
    },
    "Mountain-Extra 1": {
        "name": "The Floatiest Platforms",
        "parent": "Mountain",
        "winLogic": HasAll("Rock", "Is", "Push"),
        "winLogicAdv": HasAny("Rock", "Is", "Push"),
        "defaultWordOnlyDiff": 0,
        "connects": {
            "Mountain-6": can_win,
        },
    },
}
from typing import Dict, TypedDict, List, Set

#from worlds.evn.rezdata.misns import MisnDict, misn_table

# PREFACE:
# The biggest part of EVN that doesn't work well with AP is the potential to permanently lock out a mission, and therefore lock out a location/check.
# This often is due to the branching nature and choices made available to the player. If you take path B, you can't go back and do path A - that doesn't make sense for the story.
# Consequently, we have to protect against that in the logic less some poor (other) player's important item is forever locked.
# I would love to say I found an elegant solution to this problem, but alas, I am still hard coding paths :(

# From Regions (originally):
# REGION_KEYS = {
#     "Universe" : [],
#     "Fed" : ["Fed"], # Fed story mission string
#     "Vellos" : ["Vellos", "Vell-os"],
#     "Polaris" : ["Polaris"],
#     "Auroran" : ["Auroran"],
#     "Rebel" : ["Rebel"],
#     "Pirate" : ["Pirate"],
# }

# This should be a bit that will NEVER be set. Use it to perm block missions in the seed.
MISSION_BLOCKING_BIT = 9955

misns_to_ignore: List[int] = [
    # for our sanity, we're going to ignore "Link" missions - they do barely more than add some text and connect missions. But can *also* be branches to bring the player back to one mission.
    783,
    788,
    789,
    790, 
    797,
    798,
    800,
    801,
    804,
    811,
    812,
    814,
    816,
    818,
    819,
    836,
    837,
    838,
    839,
    905,
    784, # NOTE: Special case as this is actually a mission instead of a link. Auroran 2nd try, but forcing first instead.
    796, # NOTE: Another Auroran mission that requires previous failure, so won't include.
]

# I thought about offshoots that require a mission refusal, just setting the mission to auto-abort if accepted (one flag, easy)
# but that would be confusing to the player I think. So, instead going to try and edit the mission to look like it has one button (cannot refuse flag) that is modelled to look like the specific option, such as "refuse" instead of "okay"
class MisnSafetyLogic(TypedDict, total=False):
    misn_id: int    # the id of the target mission, ex: 129
    #column_name: str    # the misn.MisnDict column name, ex: on_accept
    #replacement_logic: str  # 
    column_edits: Dict[str, str] # ex: on_accept, "b511" - NOTE: The value type is still checked by the output logic, so do NOT wrap with quotes


# Region class: What info do we need to know about a given segment of an overall story route?
#   Note: EVNRegion would imply inheritance from AP's region class (whether it actually did or not), so let's be more specific
class EVNRegionData(TypedDict, total=False):
    id: int
    name: str
    #story_keywords: List[str] #ex: Fed, Vellos, etc.
    #missions: Dict[int, MisnDict] # the missions that can take place in this segment of the overall story route
    missions: List[int]
    #safeties: Dict[int, MisnSafetyLogic] # mission edits req to enforce the storyline
    misn_edits: Dict[int, Dict[str, str]] # The typing was nice, but id was redundant...

# NOTE: This is universe and story, but may just become story if I decide to handle side stories more.
# TODO: With stories that can come from side stories, edit the branches of those side stories. Ex: If Pirate - WB pirate branch needs to be blocked (and auroran too...)
possible_regions: Dict[int, EVNRegionData] = {
    0: {
        "id": 0,  # I don't know if we need this one here. It is our default starting region that all story lines start from.
        "name": "Universe",
        "missions": [],  # I would like to dynamically populate this by adding all missions in misn_table not in any other region's list
        "misn_edits": {}
    },
    1: {
        "id": 1,
        "name": "Vellos - Start and End",
        "missions": [
            128, 129, 130, 131, 142, 143, 144, 145, 146, 147, 148, 149, 
            193, 194, 195, 196, 197, 198, 199,
            318, 319, 320, 321, 322,
            323, 324, 325, 326, 327, 355, 356, 357, 358, 359, 360, 361, 362, 363, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380,
            402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417,
            649,
            849, 850,
        ],
        "misn_edits": {
            129: {
                "refuse_button": "Don't pick this",
                "on_refuse": "!b511",
                "on_abort":  "!b511",
            }
        }
    },
    2: {
        "id": 2,
        "name": "Polaris - Start",
        "missions": [
            150,
            179, # later in story, but not worth making own node
        ],
        "misn_edits": {}
    },
    3: {
        "id": 3,
        "name": "Polaris Start as Vellos Offshoot",
        "missions": [
            128,
            129, # must refuse this mission
            782,
            873, # later in story, but not worth making own node
        ],
        "misn_edits": {
            129: {
                "accept_button": "Don't pick this",
                "on_success": f"!b511", # set same as failure, allowing mission to be redone. Abort is acceptable.
                "on_refuse": "CHECK_TARGET"
            }
        }
    },
    4: {
        "id": 4,
        "name": "Polaris - Pt 1",
        "missions": [
            151, 152, 153, 717,
        ],
        "misn_edits": {}
    },
    # Screw it - a path pick feds at end, and b path picks aurorans at end. I don't want to duplicate just for that choice...
    5: {
        "id": 5,
        "name": "Polaris - Pt 2 - Path A",
        "missions": [
            154, 155, 156, 843, 844, 845, 157, 158, 159, 
        ],
        "misn_edits": {
            154: {
                "on_success": "b279"
            }
        }
    },
    6: {
        "id": 6,
        "name": "Polaris - Pt 2 - Path B",
        "missions": [
            154, 601, 602, 603, 598, 599, 843, 844, 845, 753, 604, 
        ],
        "misn_edits": {
            154: {
                "on_success": "b316"
            }
        }
    },
    7: {
        "id": 7,
        "name": "Polaris - Pt 3",
        "missions": [
            160, 600, 161, 162, 163, 164, 165, 166, 167, 168, 846, 847, 169, 170, 171, 172,
            180, 173, 174, 175, 176, 177, 178, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 
            #887,
        ],
        "misn_edits": {
        }
    },
    8: {
        "id": 8,
        "name": "Polaris - Fed Ending",
        "missions": [
            192, 882, 885, 887,
        ],
        "misn_edits": {
            "refuse_button": "Don't pick this",
            "on_refuse": "!b315",
        }
    },
    9: {
        "id": 9,
        "name": "Polaris - Auroran Ending",
        "missions": [
            192, 888, 889, 893, 887,
        ],
        "misn_edits": {
            192: {
                "accept_button": "Don't pick this",
                "on_success": f"!b315", # set same as failure, allowing mission to be redone. Abort is acceptable.
                "on_refuse": "CHECK_TARGET",
            }
        }
    },
    10: {
        "id": 10,
        "name": "Auroran - Start",
        "missions": [
            653, 785, 654, 655,
            669, # auroran 12c - non WG route
            684, # same, but this is a deep mission, might cause logic blocks unnecessarily. If so, will need to create new zones :(
        ],
        "misn_edits": {
            635: {
                "on_refuse": "",
                "on_failure": "!b511 A749 A750 A751 A752",
                "on_abort": "!b511 A749 A750 A751 A752",
            }
        }
    },
    11: {
        "id": 11,
        "name": "Auroran - From WG",
        "missions": [
            687,
            688, # mission 12c in auroran if you've gone this route
            690, 916, 917, 918, # deep into auroran, might cause logic blocks unnecessarily by having here.
        ],
        "misn_edits": {
        }
    },
    12: {
        "id": 12,
        "name": "Auroran - Pt 2",
        "missions": [
            656, 657, 658, 
        ],
        "misn_edits": {
        }
    },
    13: {
        "id": 13,
        "name": "Auroran - From Bounty Hunter",
        "missions": [
            691, 692,  
            669, # auroran 12c - non WG route
            684, # same, but this is a deep mission, might cause logic blocks unnecessarily. If so, will need to create new zones :(
        ],
        "misn_edits": {
        }
    },
    14: {
        "id": 14,
        "name": "Auroran - Pt 3",
        "missions": [
            659, 660, 780, 855, 856, 661, 662, 663, 664, 665, 666, 667, 668, 
            734, 735, 736, 737, 739, # offshoot
        ],
        "misn_edits": {
        }
    },
    15: { # A lot of optional quests get locked if you don't do them before mission 13 (670), so marking this as a different zone
        "id": 15,
        "name": "Auroran - Pt 4",
        "missions": [
            670, 671, 672, 673, 674, 857, 675, 676, 677, 
            741, 742, 743, 744, 745, 746, 747, 748, # offshoot
        ],
        "misn_edits": {
        }
    }, 
    16: { # Again, offshoot must be done before this
        "id": 16,
        "name": "Auroran - End",
        "missions": [
            678, 679, 680, 681, 682, 683, 685, 686, 
        ],
        "misn_edits": {
        }
    },
    20: {
        "id": 20,
        "name": "Wild Geese - Good Ending",
        "missions": [
            634, 635, 642, 643, 644, 645, 646,
        ],
        "misn_edits": {
            635: {
                "on_success": "b802 b805"
            },
            645: {
                "on_success": "b816"
            }
        }
    },
    21: {
        "id": 21,
        "name": "Wild Geese - Into Auroran",
        "missions": [
            634, 635, 636, 637, 638, 639, 640, 641,
        ],
        "misn_edits": {
            635: {
                "on_success": "b802 b804"
            },
            640: {
                "accept_button": "Don't pick this",
                "on_success": "", 
                "on_refuse": "CHECK_TARGET"
            }
        }
    },
    22: {
        "id": 22,
        "name": "Wild Geese - Into Pirate",
        "missions": [
            634, 635, 642, 643, 644, 645, 647, 648,
        ],
        "misn_edits": {
            635: {
                "on_success": "b802 b805"
            },
            645: {
                "on_success": "b817"
            }
        }
    }, # For these blocking missions - only add the edits. Don't add the mission ID otherwise it'll get assigned an item / check
    100: {
        "id": 100,
        "name": "Vellos - Block Start",
        "missions": [],
        "misn_edits": {
            128: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            }
        }
    },
    101: {
        "id": 101,
        "name": "Polaris - Block Start",
        "missions": [],
        "misn_edits": {
            150: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            }
        }
    },
    102: {
        "id": 102,
        "name": "Auroran - Block Start",
        "missions": [],
        "misn_edits": {
            653: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            }
        }
    }
}

class EVNStoryRoute(TypedDict, total=False):
    id: int # NOTE: This will be used as the value for the options selection!
    name: str # I dunno, w/e we wanna call this to clue in what it is
    option_name: str # this will be prefaced by option_, and will be in the format of [word]_[word], ex: "wg_pirate" will become "option_wg_pirate" and indicate that the player will have to go through the WG storyline into the Pirate storyline
    regions: List[int] # NOTE: ORDER MATTERS. If we need to, we'll reorg to have each define their entrance and exit regions, but for now, will make the assumption that these are in order and connect in that order.
    region_connections: Dict[int, List[int]] # Dict[FromID, ToIDs] - Use 0 for Universe
    final_mission: int | None # The mission ID that we need to assign the victory condition to
    

# Dictionary of our possible storylines / region routes
# NOTE: IDs MUST be sequential due to how they are referenced elsewhere!
story_routes: Dict[int, EVNStoryRoute] = {
    1: {
        "id": 1,
        "name": "Vellos - Standard",
        "option_name": "vellos",
        "regions": [
            0, # always include universe as our default start!
            1, 101, 102, 20,
        ],
        #"region_connections": { 0: [1, 101, 102, 20] }, # I don't think we need to add the blocking missions
        "region_connections": { 0: [1, 20] },
        "final_mission": 417,
    },
    2: {
        "id": 2,
        "name": "Polaris - Standard - Path A",
        "option_name": "polaris",
        "regions": [
            0, 100, 102, 2, 4, 5, 7, 9, 20,
        ],
        "region_connections": { 0: [2, 20], 2: [4], 4: [5], 5: [7], 7: [9] },
        "final_mission": 887,
    },
    3: {    # So, there's 2 starting options, and 2 paths, for 4 combos. May implement all 4, may not.
        "id": 3,
        "name": "Polaris - From Vellos - Path B",
        "option_name": "vellos_polaris",
        "regions": [
            0, 101, 102, 3, 4, 6, 7, 8, 20,
        ],
        "region_connections": { 0: [3, 20], 3: [4], 4: [6], 6: [7], 7: [8] },
        "final_mission": 887,
    },
    4: {    # Auroran options
        "id": 4,
        "name": "Auroran",
        "option_name": "auroran",
        "regions": [
            0, 100, 101, 20, 10, 12, 14, 15, 16,
        ],
        "region_connections": { 0: [10, 20], 10: [12], 12: [14], 14: [15], 15: [16] },
        "final_mission": 686,
    },
    5: {    # Auroran options
        "id": 5,
        "name": "Auroran - From WG",
        "option_name": "wg_auroran",
        "regions": [
            0, 100, 101, 102, 21, 11, 12, 14, 15, 16,
        ],
        "region_connections": { 0: [11, 21], 11: [12], 12: [14], 14: [15], 15: [16] },
        "final_mission": 686,
    },
    # TODO: Needs BH setup first
#     6: {    # Auroran options
#         "id": 6,
#         "name": "Auroran - From Bounty Hunter",
#         "option_name": "bh_auroran",
#         "regions": [
#             0, 100, 101, 102, 20, 13, 12, 14, 15, 16,
#         ],
#         "region_connections": { 0: [20, 13], 13: [12], 12: [14], 14: [15], 15: [16] },
#         "final_mission": 686,
#     }
}

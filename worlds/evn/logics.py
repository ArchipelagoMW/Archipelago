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
    783, 786, 787, 788, 789, 790, 797, 798, 799, 800, 801, 804, 805, 806, 807, 811, 812,
    813, 814, 816, 817, 818, 819, 836, 837, 838, 839, 879, 905,
    784, # NOTE: Special case as this is actually a mission instead of a link. Auroran 2nd try, but forcing first instead.
    796, # NOTE: Another Auroran mission that requires previous failure, so won't include.
    901,    # NOTE: "You Need to Register..." requests. Not going to happen, so remove.
    902,
    903,
    904,
    609, # drop bear - "haha"...
    610, 

    # Were these debug missions or something?

    # Silent missions. They don't have a success, so... Don't help with checks.
    606, 607, # "silent missions"
    711, 713, 714, 715, 718, 731, 733, 738, 740, 749, 750, 751, 752, 755,   
    781, # hmm
    791, 792, 793, 795, 808, 809, 827, 848, 854, 858, 875, 879, 895, 896,
    899, 900, 905, 913,   # silent misn
    880, 881, 883, 884,    # pursuit groups of enemies
    886, 894, 890, 891, 892, 
    # invisible misn - again, don't seem to have ability to complete
    802, 803, 833, 
    # Krypt mind attack string from Polars32... Could have on success, but I'm unclear what it takes to meet that req...
    862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 875,
    # ???
    872, 
    # generic post game missions (but victory will already have released, so can't get to before end.)
    874, 876, 877, 878, 910, 911, 
]

# Introducing this logic caused the number of available missions to drop below the item count
# when also using outf. As such, we need to cut down on these.
# I'm starting with "bad apple" variants (that are more of traps than helpful), then maybe cutting into variants in general.

# TODO: Implement in items, and change default in world so they aren't provided if not found in items bank.
ships_to_ignore: List[int] = [
    168, 169, 170, 171, 185, # wraith
    176, # krypt pod
    895, # escape pod
    173, 174, 175, # AI specific Vellos ships (they come with vellos weapons and abilities...), the 300 ones are the real ones.
    
    # ships with disabling weapons:
    384, 385, 386, 387, 388, 389, # abominations
    390, # pheonix

    # removing "economy at work"
    391, 392, 393,
    # poor variants
    361, 363, 365, 367, 369, 371,

    # removing cloaking ships. I'm not 100% on this, but I figure the cloak should come from the outf once found anyways...
    # this does also remove some variants that had a non-0 buy chance
    259, 319, 267, 326, 408, # arachnid
    260, 320, 269, 327, 409, # dragon
    263, 265, 323, 325, 272, 330, 406, 411, # raven
    358, 359, 360, # reb dest
    355, 357, 405, # reb drag
    261, 321, 270, 328, 407, # scarab
    262, 322, 271, 329, 410, # striker
    256, 257, 258, 376, 266, # zephyr

    # removing variants
    # dani / tekel / vella
    243, 244, 245, # abom
    252, 253, 254, # cruser
    299, 300, 301, # carrier

    # deduping, particularly the never-could-be-bought dupes
    # Note: I am keeping some variants - mostly removing those with *the same name*
    205, 207, # argosy
    297, 396, 247, 397, # aur carr / cruis
    210, # enterprise
    278, # lightning
    390, # pheonix
    402, # pir argosy
    238, 403, # pir enterprise
    232, 233, 235, 400, # pir startbridge
    288, 290, 401, # pir valk
    404, # pir viper
    373, # rage gunboat
    264, 324, # raven
    184, # reb dest (because rebel II string checks)
    183, # reb drag
    341, # reb starbridge
    352, 353, # reb thunderhead
    394, 273, # sprite
    198, 199, 398, # starbridge
    281, 399, # valk
    375, # zephyr
]   # removed 111?

outf_to_ignore: List[int] = [
    187, 188, # escape pod and auto launcher - may need to readd for deathlink hard core? bleh
    204, 433, 434, # very specific map
    229, 230, 231, 232, 233, 266, 267, 339, # nanites + wraith weapons
    314, 315, 316, 317, 318, # ship upgrades - sorry
    319, # drop bear repellent
    320, 321, 322, 323, 324, 325, 326, 327, 332, # illegal outf
    328, 329, 330, # "disabling" weapons
    331, # user modified ionic particle cannon? what's that?
    348, # bureau bomb outfit - pretty sure this is a trap anyways 33
    358, 359, 360, 361, 362, # "cheap" stuff
    363, 364, 439, # forged licenses
    374, # thorium reactor - bomb, ah so this is the trap one
    375, 376, 377, 378, # degraded or disabled
    257, 258, 259, 260, 263, 264, 265, # Licenses; I'm removing these... unlocking things except these would suck - still couldn't get something that was unlocked? Not worth for the randomizer.
    # ???
    236, # what is "fuel transfers"? 0% avail anyways
    261, # thorium reactor - ionisation
    # duplicates that aren't necessary due to changes
    247, 273, 
    254, 345, 255, 346, # wraithii cannons and ammo that were gained by other factions. Let's just keep the core polaris versions.
    # not clear on why these two were options, but not avail. Likely ship specific outfits?
    267, 266,
] # removed 63?

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
            192: {
                "refuse_button": "Don't pick this",
                "on_refuse": "!b315",
            }
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
    },
    23: {
        "id": 23,
        "name": "Bounty Hunter - Start",
        "missions": [
            257, 258, 259, 260, 261, 262, 140, 263, 264, 265, 267, 268, 269, 270, 271, 272, 273, 
            276, 274, 275, 277, 278, 
        ],
        "misn_edits": {
            266: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            },
        }
    },
    24: {
        "id": 24,
        "name": "Bounty Hunter - Start - Into Auroran",
        "missions": [
            257, 258, 259, 260, 261, 262, 140, 263, 264, 265, 266,
        ],
        "misn_edits": {
            267: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            },
        }
    },
    25: { # I don't like this one - don't like that you have to fail
        "id": 25,
        "name": "Bounty Hunter - Into Fed (Req. Failing Misn.)",
        "missions": [
            279,
        ],
        "misn_edits": {
            279: {
                "on_success": "!b511"
            },
        }
    },
    26: { 
        "id": 26,
        "name": "Bounty Hunter - Into Rebels",
        "missions": [
            279, 280,
        ],
        "misn_edits": {
            279: {
                "on_failure": "!b511"
            },
        }
    }, 
    27: {  # Don't use last two missions so that the player can't be branched into another storyline before starting the intended one.
        "id": 27,
        "name": "Bounty Hunter - End (Trunc To Not Branch)",
        "missions": [
            
        ],
        "misn_edits": {
            279: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            },
        }
    }, 
    30: {  
        "id": 30,
        "name": "Pirate - Start",
        "missions": [
            693, 694, 695, 696,
        ],
        "misn_edits": {
            694: {
                "on_refuse": ""
            },
        }
    }, 
    31: {  
        "id": 31,
        "name": "Pirate - From WG",
        "missions": [
            810, 840, 695, 841,
        ],
        "misn_edits": {
            840: {
                "on_refuse": ""
            },
        }
    }, 
    32: {  
        "id": 32,
        "name": "Pirate - Pt 2",
        "missions": [
            697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 712, 
            300, 720, 718, 721, 722, 723, 724, 
            842, # some kind of link or something, but has on_success bits
            # ?
            # 874, 876, # i think postgame
        ],
        "misn_edits": {
            694: {
                "on_refuse": ""
            },
        }
    }, 
    33: {  
        "id": 33,
        "name": "Pirate - Offshoot End A",
        "missions": [
            725, 727,
        ],
        "misn_edits": {
            724: {
                "refuse_button": "Don't pick this",
                "on_refuse": ""
            },
        }
    }, 
    34: {  
        "id": 34,
        "name": "Pirate - Offshoot End B",
        "missions": [
            726, 728, 729, 730,
            912, # Hmm, this one may cause problems?
        ],
        "misn_edits": {
            724: {
                "accept_button": "Don't pick this",
                "on_accept": "b435", # force into refusal
                "on_refuse": "CHECK_TARGET"
            },
        }
    }, 
    40: {  
        "id": 40,
        "name": "Fed - Start",
        "missions": [
            428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 443,
            439, # rebel branch missions we aren't going to utilize for now. 
        ],
        "misn_edits": {
            439: {
                "refuse_button": "Don't pick this",
                "on_refuse": ""
            }
        }
    }, 
    41: {  
        "id": 41, # TODO: Implement. Requires failing a BH mission which is why I don't like trying to enforce it.
        "name": "Fed - From BH (NOT USING)",
        "missions": [
            440,
        ],
        "misn_edits": {
        }
    }, 
    42: {  
        "id": 42,
        "name": "Fed - Pt 2",
        "missions": [
            441, 442, 444, 445, 446, 447, 450, 452, 451, 453, 454, 455, 456, 457, 458, 459, 460,
            461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 474,
            473, # NON Gli-Tec-Nia path. 613 would be the alt, but not dealing with it.
        ],
        "misn_edits": {
            473: {
                "available_bits": "(P0 & b87) & !b88" # Remove glitecnia check
            },
            613: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}" # block the glitecnia version of the mission
            }
        }
    }, 
    43: {  
        "id": 43, # I'm not implementing these for now, but I need them out of the pool (aka: in at least 1 region)
        "name": "Fed - From Rebels or BH (NOT USING)",
        "missions": [
            448, 449,
        ],
        "misn_edits": {
        }
    }, 
    44: {  
        "id": 44, # For now, I'm not implementing this one. Again, need them out of the pool.
        "name": "Fed - Forced (NOT USING)",
        "missions": [
            575, 576, 590, 592, 591, 593, 594, 595, 596,
        ],
        "misn_edits": {
        }
    }, 
    45: {  
        "id": 45, # Not implementing this branch for now, sorry. Need it out of the pool.
        "name": "Fed - Gli-Tec-Nia Missions (NOT USING)",
        "missions": [
            613,
        ],
        "misn_edits": {
        }
    }, 
    50: {  # Rebels
        "id": 50, # Too many links, not dealing with this for now. Other ways into rebels.
        "name": "Rebel - From Fed (NOT USING)",
        "missions": [
            330, 
            611, # technically *to* feds?
        ],
        "misn_edits": {
        }
    }, 
    51: {  # Rebels
        "id": 51, # 
        "name": "Rebel - From BH",
        "missions": [
            328, 329, 331, 332, 333, 334, 335, 336, 337, 338, 853,
        ],
        "misn_edits": {
            611: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}" # dunno if I need this, but extra protection
            },
            608: { # due to lockout conditions, cutting off this option. do sigma
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            }
        }
    }, 
    52: {  # Rebels
        "id": 50, # If you want hyper gates, do sigma story line
        "name": "Rebel - Give Gates (NOT USING)",
        "missions": [
            608,
        ],
        "misn_edits": {
        }
    }, 
    53: {  # Rebels
        "id": 53, 
        "name": "Rebel I",
        "missions": [
            339, 612, 340, 341, 859, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 
            353, 354, 
            914, # not sure on this one...
        ],
        "misn_edits": {
            339: {
                "accept_button": "Must Succeed",
                "on_failure": ""
            }
        }
    }, 
    54: {  # Rebels
        "id": 54, # Forced fail... bleh
        "name": "Rebel II",
        "missions": [
            339, 612, 401, 400, 399, 398, 397, 396, 395, 394, 393, 392, 391, 390, 389, 388, 
            387, 386, 385, 384, 383, 382, 381,
            915, # not sure on this one...
        ],
        "misn_edits": {
            339: {
                "accept_button": "Must FAIL",
                "on_success": ""
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
    },
    103: {
        "id": 103,
        "name": "Pirate - Block Start",
        "missions": [],
        "misn_edits": {
            693: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            }
        }
    },
    104: {
        "id": 104,
        "name": "Feds - Block Start",
        "missions": [],
        "misn_edits": {
            428: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            }
        }
    },
    200: {  # Due to checks vs blocking nature of missions, pulling out some paths of side quests
        "id": 200,
        "name": "Side Misn - (NOT USING)",
        "missions": [
            834, 835, # "meh" cunjo hunt branch
            597, # fed req glitechnia mission
            758, # Huh, you can abort Barry (kinda)
            577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, # second half of United Shipping due to polaris req :(
        ],
        "misn_edits": {
        }
    },
    201: {
        "id": 201,
        "name": "Side Misn - Block unused routes",
        "missions": [],
        "misn_edits": {
            834: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            },
            597: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            },
            577: {
                "available_bits": f"b{MISSION_BLOCKING_BIT}"
            },
            756: {
                "on_abort": ""
            }
        }
    },
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
            101, 102, 103, 104, 201, # blocking (don't connect)
            20, 23, 27, # WG + BH
            1, # Story
        ],
        #"region_connections": { 0: [1, 101, 102, 20] }, # I don't think we need to add the blocking missions
        "region_connections": { 0: [1, 20, 23, 27] },
        "final_mission": 417,
    },
    2: {
        "id": 2,
        "name": "Polaris - Standard - Path A",
        "option_name": "polaris",
        "regions": [
            0, 
            100, 102, 103, 104, 201, 
            20, 23, 27,
            2, 4, 5, 7, 9,
        ],
        "region_connections": { 0: [2, 20, 23, 27], 2: [4], 4: [5], 5: [7], 7: [9] },
        "final_mission": 887,
    },
    3: {    # So, there's 2 starting options, and 2 paths, for 4 combos. May implement all 4, may not.
        "id": 3,
        "name": "Polaris - From Vellos - Path B",
        "option_name": "vellos_polaris",
        "regions": [
            0, 
            101, 102, 103, 104, 201,
            20, 23, 27,
            3, 4, 6, 7, 8, 
        ],
        "region_connections": { 0: [3, 20, 23, 27], 3: [4], 4: [6], 6: [7], 7: [8] },
        "final_mission": 887,
    },
    4: {    # Auroran options
        "id": 4,
        "name": "Auroran",
        "option_name": "auroran",
        "regions": [
            0, 
            100, 101, 103, 104, 201,
            20, 23, 27,
            10, 12, 14, 15, 16, 
        ],
        "region_connections": { 0: [10, 20, 23, 27], 10: [12], 12: [14], 14: [15], 15: [16] },
        "final_mission": 686,
    },
    5: {    # Auroran options
        "id": 5,
        "name": "Auroran - From WG",
        "option_name": "wg_auroran",
        "regions": [
            0, 
            100, 101, 102, 103, 104, 201,
            23, 27,
            21, 11, 12, 14, 15, 16, 
        ],
        "region_connections": { 0: [11, 21, 23, 27], 11: [12], 12: [14], 14: [15], 15: [16] },
        "final_mission": 686,
    },
    6: {    # Auroran options
        "id": 6,
        "name": "Auroran - From Bounty Hunter",
        "option_name": "bh_auroran",
        "regions": [
            0, 
            100, 101, 102, 103, 104, 201,
            20, 
            24, 13, 12, 14, 15, 16, 
        ],
        "region_connections": { 0: [20, 24], 24: [13], 13: [12], 12: [14], 14: [15], 15: [16] },
        "final_mission": 686,
    },
    7: {    # Pirates
        "id": 7,
        "name": "Pirate",
        "option_name": "pirate",
        "regions": [
            0, # universe
            100, 101, 102, 104, 201, # blocking other strings (don't connect)
            20, 23, 27, # WG + BH
            30, 32, 34, # Story
        ],
        "region_connections": { 0: [20, 23, 27, 30], 30: [32], 32: [34] },
        "final_mission": 712,
    },
    8: {   
        "id": 8,
        "name": "Pirates - From WG",
        "option_name": "wg_pirate",
        "regions": [
            0, 
            100, 101, 102, 103, 104, 201, # blocking
            23, 27, # BH
            22, 31, 32, 34, # WG -> Story
        ],
        "region_connections": { 0: [22, 23, 27], 22: [31], 31: [32], 32: [34] },
        "final_mission": 712,
    },
    9: {   
        "id": 9,
        "name": "Feds",
        "option_name": "feds",
        "regions": [
            0, 
            100, 101, 102, 103, 201, # blocking
            20, 23, 27, # BH
            40, 42, # Story
        ],
        "region_connections": { 0: [20, 23, 27, 40], 40: [42] },
        "final_mission": 474,
    },
    10: {   
        "id": 10,
        "name": "Rebel I - From BH",
        "option_name": "bh_rebel1",
        "regions": [
            0, 
            100, 101, 102, 103, 104, 201, # blocking
            20, # WG
            23, 26, 51, 53, # BH -> Story
        ],
        "region_connections": { 0: [20, 23], 23: [26], 26: [51], 51: [53] },
        "final_mission": 354,
    },
    11: {   
        "id": 11,
        "name": "Rebel II - From BH",
        "option_name": "bh_rebel2",
        "regions": [
            0, 
            100, 101, 102, 103, 104, 201, # blocking
            20, # WG
            23, 26, 51, 54, # BH -> Story
        ],
        "region_connections": { 0: [20, 23], 23: [26], 26: [51], 51: [54] },
        "final_mission": 381,
    }
}

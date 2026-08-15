# Nova uses bits 0-9999
# However, not all those reserved bits are used by the original scenario
# We are borrowing ranges for our purposes
# Different things (ships, outf, misn, etc.) are going to use different ranges
# This is in part due to most of these data types starting at the same id of 128
# Meaning they would just overwrite each other in our tables otherwise
# I had these in multiple places, so they've been pooled here instead

from decimal import Decimal
from typing import Dict, TypedDict

STARTING_ID = 128
MAX_OUTFITS = 512
# We *could* get this dynamically from max(outfits.outf_table), but I'm avoiding extra imports this way for now (and being lazy...)
HIGHEST_OUTFIT_ID = 443 

offsets_table: Dict[str, int] = {
    "Credits": 9900, # Special case! These won't actually be set - the client will check for these ids and make its own adjustment.
    "ship": 1550 - STARTING_ID,   # 1550 - 1999 will be ships. We have 288/450 ships, so this should be safe.
    "outf": 3100 - STARTING_ID,   # 3100 - 3500 for outfs. We have 242/400 outf, should be good
    "misn": 2000 - STARTING_ID,   # 2000 - 2999 will be missions. We have 791/1000 misns, so this should be safe.
    "outf_cks": 4100 - STARTING_ID, # 4100 - 4150 for custom outf (as locations/checks).
    "desc": 3000, # this is the true desc offset, not a custom set we're trying to use.
    "desc_alt": 3000 - STARTING_ID, # used in print out
}

class CustLocData(TypedDict, total=False):
    name: str
    cost: int
    display_weight: int
    chance: Decimal

custom_outfits_ratio: Dict[int, CustLocData] = {
    1: {
        "name": "5k Unlock",    # ID will be concat to name to ensure uniqueness.
        "cost": 5_000,
        "display_weight": -1,
        "chance": Decimal("0.025"),
    },
    2: {
        "name": "10k Unlock",
        "cost": 10_000,
        "display_weight": -2,
        "chance": Decimal("0.025"),
    },
    3: {
        "name": "15k Unlock",
        "cost": 15_000,
        "display_weight": -3,
        "chance": Decimal("0.025"),
    },
    4: {
        "name": "20k Unlock",
        "cost": 20_000,
        "display_weight": -4,
        "chance": Decimal("0.025"),
    },
    5: {
        "name": "25k Unlock",
        "cost": 25_000,
        "display_weight": -5,
        "chance": Decimal("0.05"),
    },
    6: {
        "name": "50k Unlock",
        "cost": 50_000,
        "display_weight": -6,
        "chance": Decimal("0.05"),
    },
    7: {
        "name": "75k Unlock",
        "cost": 75_000,
        "display_weight": -7,
        "chance": Decimal("0.05"),
    },
    8: {
        "name": "100k Unlock",
        "cost": 100_000,
        "display_weight": -8,
        "chance": Decimal("0.05"),
    },
    9: {
        "name": "125k Unlock",
        "cost": 125_000,
        "display_weight": -9,
        "chance": Decimal("0.05"),
    },
    10: {
        "name": "150k Unlock",
        "cost": 150_000,
        "display_weight": -10,
        "chance": Decimal("0.05"),
    },
    11: {
        "name": "175k Unlock",
        "cost": 175_000,
        "display_weight": -11,
        "chance": Decimal("0.05"),
    },
    12: {
        "name": "200k Unlock",
        "cost": 200_000,
        "display_weight": -12,
        "chance": Decimal("0.05"),
    },
    13: {
        "name": "250k Unlock",
        "cost": 250_000,
        "display_weight": -13,
        "chance": Decimal("0.1"),
    },
    14: {
        "name": "500k Unlock",
        "cost": 500_000,
        "display_weight": -14,
        "chance": Decimal("0.05"),
    },
    15: {
        "name": "750k Unlock",
        "cost": 750_000,
        "display_weight": -15,
        "chance": Decimal("0.05"),
    },
    16: {
        "name": "1M Unlock",
        "cost": 1_000_000,
        "display_weight": -16,
        "chance": Decimal("0.15"),
    },
    17: {
        "name": "1.25M Unlock",
        "cost": 1_250_000,
        "display_weight": -17,
        "chance": Decimal("0.025"),
    },
    18: {
        "name": "1.5M Unlock",
        "cost": 1_500_000,
        "display_weight": -18,
        "chance": Decimal("0.025"),
    },
    19: {
        "name": "1.75M Unlock",
        "cost": 1_750_000,
        "display_weight": -19,
        "chance": Decimal("0.025"),
    },
    20: {
        "name": "2M Unlock",
        "cost": 2_000_000,
        "display_weight": -20,
        "chance": Decimal("0.025"),
    },
    21: {
        "name": "2.5M Unlock",
        "cost": 2_500_000,
        "display_weight": -21,
        "chance": Decimal("0.025"),
    },
    22: {
        "name": "5M Unlock",
        "cost": 5_000_000,
        "display_weight": -22,
        "chance": Decimal("0.025"),
    }
}
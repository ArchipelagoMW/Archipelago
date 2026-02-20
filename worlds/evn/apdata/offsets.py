# Nova uses bits 0-9999
# However, not all those reserved bits are used by the original scenario
# We are borrowing ranges for our purposes
# Different things (ships, outf, misn, etc.) are going to use different ranges
# This is in part due to most of these data types starting at the same id of 128
# Meaning they would just overwrite each other in our tables otherwise
# I had these in multiple places, so they've been pooled here instead

from typing import Dict

STARTING_ID = 128

offsets_table: Dict[str, int] = {
    "Credits": 9900, # Special case! These won't actually be set - the client will check for these ids and make its own adjustment.
    "ship": 1550 - STARTING_ID,   # 1550 - 1999 will be ships. We have 288/450 ships, so this should be safe.
    "outf": 3100 - STARTING_ID,   # 3100 - 3500 for outfs. We have 242/400 outf, should be good
    "misn": 2000 - STARTING_ID,   # 2000 - 2999 will be missions. We have 791/1000 misns, so this should be safe.
    "outf_cks": 4100 - STARTING_ID, # 4100 - 4150 for custom outf (as locations/checks).
    "desc": 3000, # this is the true desc offset, not a custom set we're trying to use.
    "desc_alt": 3000 - STARTING_ID, # used in print out
}
# These custom outf are used to introduce checks to the outfitter shop for the player.
# This gives us a few more checks to pad with, which is helpful for the shorter storylines (pirate)
# Additionally, it is an alternate way for the player to engage with checks.
# Very similar to shops in other games.
# They are done here instead of in the outf data file because:
#   1. They are not part of the original game data
#   2. We may use none/some/all
#   3. They require special handling as we'll be pumping players' world data into them.
# NOTE: We have too many items (rewards) and not enough locations (checks). So, we create these to artificially increase number of locations/checks.
#   Do not be confused by these being shop items (since outfits can also be shuffled). These are "shop checks", locations completed by the player
#   purchasing them from the game shop.

from typing import Dict
from ..rezdata.outfits import OutfDict

# IMPORTANT: Start at the END of the last outfit data's ID range.
cust_outf_table: Dict[int, OutfDict] = {
    450: {
        "resource_type": "outf",
        "id": "450",
        "name": "Unlock 5k",
        "display_weight": "-1",
        "mass": "0",
        "tech_level": "1",
        "mod_type_1": "-1",
        "mod_value_1": "-1",
        "mod_type_2": "-1",
        "mod_value_2": "-1",
        "mod_type_3": "-1",
        "mod_value_3": "-1",
        "mod_type_4": "-1",
        "mod_value_4": "-1",
        "max_count": "1",
        "cost": "5000",
        "item_class": "0",
        "scan_mask": "0x0000",
        "buy_random": "100",
        "availability": "",
        "on_purchase": "",  # the bit to unlock the check
        "on_sell": "",
        "contribute_bits": "0x0000000000000000",
        "require_bits": "0x0000000000000001",
        "short_name": "Unlock 5k\\\\n- Player -",   # put in that player's name for recognition?
        "lower_case_name": "Unlock 5k",
        "lower_case_plural_name": "Unlocks 5k",
        "requirments_government": "127",
        "flags": "0x000C",
        "end_of_resource": "EOR"
    },
}
# Outf descriptions work by matching id offset from 3k in desc to the id of outfit - 128 (ex: 3000 -> 128, 3001 -> 129, etc.)

from typing import Dict
from ..rezdata.desc import DescDict

# IMPORTANT: Start at the END of the last outfit data's ID range.
cust_desc_table: Dict[int, DescDict] = {
    # This is a special description for our "Clean Rep" item. It is intended to be a helper item for players who are stuck because they can't get to a check due to a government being too mad at them. This item clears their legal record with all governments, allowing them to access the checks they need. Players will only receive one of these items, and it is meant to prevent them from getting stuck in the game.
    3316: {
        "resource_type": "desc",
        "id": "3316",
        "name": "Clean Rep",
        "text": "This clears your legal record with all governments. The point of this item is if you need to get to a check, but can't because a government is too mad, this is your 'get out of jail' card so you can go get that check. You only get ONE. It is intended to keep players from getting stuck.",
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    # Template description for the dynamically created unlock items.
    3322: {
        "resource_type": "desc",
        "id": "3322",
        "name": "Unlock 5k",
        "text": "[player_name]'s [item_name]", # we'll overwrite, just leave blank. But I left this as template example.
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
}
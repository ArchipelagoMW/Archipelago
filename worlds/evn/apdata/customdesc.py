# Outf descriptions work by matching id offset from 3k in desc to the id of outfit - 128 (ex: 3000 -> 128, 3001 -> 129, etc.)

from typing import Dict
from ..rezdata.desc import DescDict

# IMPORTANT: Start at the END of the last outfit data's ID range.
cust_desc_table: Dict[int, DescDict] = {
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
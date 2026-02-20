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
    3323: {
        "resource_type": "desc",
        "id": "3323",
        "name": "Unlock 10k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3324: {
        "resource_type": "desc",
        "id": "3324",
        "name": "Unlock 15k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3325: {
        "resource_type": "desc",
        "id": "3325",
        "name": "Unlock 25k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3326: {
        "resource_type": "desc",
        "id": "3326",
        "name": "Unlock 50k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3327: {
        "resource_type": "desc",
        "id": "3327",
        "name": "Unlock 75k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3328: {
        "resource_type": "desc",
        "id": "3328",
        "name": "Unlock 100k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3329: {
        "resource_type": "desc",
        "id": "3329",
        "name": "Unlock 125k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3330: {
        "resource_type": "desc",
        "id": "3330",
        "name": "Unlock 150k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3331: {
        "resource_type": "desc",
        "id": "3331",
        "name": "Unlock 175k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3332: {
        "resource_type": "desc",
        "id": "3332",
        "name": "Unlock 200k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3333: {
        "resource_type": "desc",
        "id": "3333",
        "name": "Unlock 250k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3334: {
        "resource_type": "desc",
        "id": "3334",
        "name": "Unlock 500k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3335: {
        "resource_type": "desc",
        "id": "3335",
        "name": "Unlock 750k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3336: {
        "resource_type": "desc",
        "id": "3336",
        "name": "Unlock 1M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3337: {
        "resource_type": "desc",
        "id": "3337",
        "name": "Unlock 5M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    }
}
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
        "name": "Unlock 20k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3326: {
        "resource_type": "desc",
        "id": "3326",
        "name": "Unlock 25k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3327: {
        "resource_type": "desc",
        "id": "3327",
        "name": "Unlock 50k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3328: {
        "resource_type": "desc",
        "id": "3328",
        "name": "Unlock 75k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3329: {
        "resource_type": "desc",
        "id": "3329",
        "name": "Unlock 100k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3330: {
        "resource_type": "desc",
        "id": "3330",
        "name": "Unlock 175k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3331: {
        "resource_type": "desc",
        "id": "3331",
        "name": "Unlock 200k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3332: {
        "resource_type": "desc",
        "id": "3332",
        "name": "Unlock 250k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3333: {
        "resource_type": "desc",
        "id": "3333",
        "name": "Unlock 500k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3334: {
        "resource_type": "desc",
        "id": "3334",
        "name": "Unlock 750k",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3335: {
        "resource_type": "desc",
        "id": "3335",
        "name": "Unlock 1M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3336: {
        "resource_type": "desc",
        "id": "3336",
        "name": "Unlock 1.25M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3337: {
        "resource_type": "desc",
        "id": "3337",
        "name": "Unlock 1.5M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3342: {
        "resource_type": "desc",
        "id": "3342",
        "name": "Unlock 1.75M",
        "text": "[player_name]'s [item_name]", # we'll overwrite, just leave blank. But I left this as template example.
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3343: {
        "resource_type": "desc",
        "id": "3343",
        "name": "Unlock 2M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3344: {
        "resource_type": "desc",
        "id": "3344",
        "name": "Unlock 2.25M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3345: {
        "resource_type": "desc",
        "id": "3345",
        "name": "Unlock 2.5M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3346: {
        "resource_type": "desc",
        "id": "3346",
        "name": "Unlock 5M",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3347: {
        "resource_type": "desc",
        "id": "3347",
        "name": "Unlock 500k B",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3348: {
        "resource_type": "desc",
        "id": "3348",
        "name": "Unlock 500k C",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3349: {
        "resource_type": "desc",
        "id": "3349",
        "name": "Unlock 500k D",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3350: {
        "resource_type": "desc",
        "id": "3350",
        "name": "Unlock 1M B",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3351: {
        "resource_type": "desc",
        "id": "3351",
        "name": "Unlock 1M C",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3352: {
        "resource_type": "desc",
        "id": "3352",
        "name": "Unlock 1M D",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3353: {
        "resource_type": "desc",
        "id": "3353",
        "name": "Unlock 1M E",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3354: {
        "resource_type": "desc",
        "id": "3354",
        "name": "Unlock 1M F",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3355: {
        "resource_type": "desc",
        "id": "3355",
        "name": "Unlock 1M G",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3356: {
        "resource_type": "desc",
        "id": "3356",
        "name": "Unlock 1M H",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3357: {
        "resource_type": "desc",
        "id": "3357",
        "name": "Unlock 1M I",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3358: {
        "resource_type": "desc",
        "id": "3358",
        "name": "Unlock 1M J",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3359: {
        "resource_type": "desc",
        "id": "3359",
        "name": "Unlock 2.5M B",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3360: {
        "resource_type": "desc",
        "id": "3360",
        "name": "Unlock 2.5M C",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3361: {
        "resource_type": "desc",
        "id": "3361",
        "name": "Unlock 2.5M D",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3362: {
        "resource_type": "desc",
        "id": "3362",
        "name": "Unlock 2.5M E",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3363: {
        "resource_type": "desc",
        "id": "3363",
        "name": "Unlock 2.5M F",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3364: {
        "resource_type": "desc",
        "id": "3364",
        "name": "Unlock 5M B",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3365: {
        "resource_type": "desc",
        "id": "3365",
        "name": "Unlock 5M C",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3366: {
        "resource_type": "desc",
        "id": "3366",
        "name": "Unlock 5M D",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    },
    3366: {
        "resource_type": "desc",
        "id": "3366",
        "name": "Unlock 5M E",
        "text": "", 
        "graphics": "0",
        "movie_file": "",
        "flags": "0x0000",
        "end_of_resource": "EOR"
    }
}
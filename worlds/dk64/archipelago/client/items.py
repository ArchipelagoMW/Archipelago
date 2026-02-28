"""Items module for Archipelago."""

from typing import Dict, Any

# AP_ID, Name, Flag Id (Hex int), Count ID (CountStruct field mapping)
item_ids: Dict[int, Dict[str, Any]] = {
    14041089: {"name": "No Item", "count_id": None, "flag_id": 0},
    14041090: {"name": "Fill Helper Item - SHOULD NOT BE PLACED", "count_id": None, "flag_id": None},
    14041091: {"name": "Donkey", "count_id": {"field": "kong_bitfield", "bit": 0}, "flag_id": None, "progression": True},
    14041092: {"name": "Diddy", "count_id": {"field": "kong_bitfield", "bit": 1}, "flag_id": None, "progression": True},
    14041093: {"name": "Lanky", "count_id": {"field": "kong_bitfield", "bit": 2}, "flag_id": None, "progression": True},
    14041094: {"name": "Tiny", "count_id": {"field": "kong_bitfield", "bit": 3}, "flag_id": None, "progression": True},
    14041095: {"name": "Chunky", "count_id": {"field": "kong_bitfield", "bit": 4}, "flag_id": None, "progression": True},
    14041096: {"name": "Vines", "count_id": {"field": "flag_moves", "bit": "vines"}, "flag_id": None, "progression": True},
    14041097: {"name": "Diving", "count_id": {"field": "flag_moves", "bit": "diving"}, "flag_id": None, "progression": True},
    14041098: {"name": "Oranges", "count_id": {"field": "flag_moves", "bit": "oranges"}, "flag_id": None, "progression": True},
    14041099: {"name": "Barrels", "count_id": {"field": "flag_moves", "bit": "barrels"}, "flag_id": None, "progression": True},
    14041100: {"name": "Climbing", "count_id": None, "flag_id": 671, "progression": True},
    14041101: {"name": "progression Slam", "count_id": {"item": 2, "level": 3}, "flag_id": None, "progression": True},
    14041102: {"name": "progression Slam ", "count_id": {"item": 2, "level": 3}, "flag_id": None, "progression": True},
    14041260: {"name": "progression Slam  ", "count_id": {"item": 2, "level": 3}, "flag_id": None, "progression": True},
    14041103: {"name": "progression Donkey Potion", "count_id": None, "flag_id": None, "progression": True},
    14041104: {"name": "Baboon Blast", "count_id": {"item": 26, "level": 1}, "flag_id": None, "progression": True},
    14041105: {"name": "Strong Kong", "count_id": {"item": 27, "level": 1}, "flag_id": None, "progression": True},
    14041106: {"name": "Gorilla Grab", "count_id": {"item": 28, "level": 1}, "flag_id": None, "progression": True},
    14041107: {"name": "progression Diddy Potion", "count_id": None, "flag_id": None, "progression": True},
    14041108: {"name": "Chimpy Charge", "count_id": {"item": 29, "level": 1}, "flag_id": None, "progression": True},
    14041109: {"name": "Rocketbarrel Boost", "count_id": {"item": 30, "level": 1}, "flag_id": None, "progression": True},
    14041110: {"name": "Simian Spring", "count_id": {"item": 31, "level": 1}, "flag_id": None, "progression": True},
    14041111: {"name": "progression Lanky Potion", "count_id": None, "flag_id": None, "progression": True},
    14041112: {"name": "Orangstand", "count_id": {"item": 32, "level": 1}, "flag_id": None, "progression": True},
    14041113: {"name": "Baboon Balloon", "count_id": {"item": 33, "level": 1}, "flag_id": None, "progression": True},
    14041114: {"name": "Orangstand Sprint", "count_id": {"item": 34, "level": 1}, "flag_id": None, "progression": True},
    14041115: {"name": "progression Tiny Potion", "count_id": None, "flag_id": None, "progression": True},
    14041116: {"name": "Mini Monkey", "count_id": {"item": 35, "level": 1}, "flag_id": None, "progression": True},
    14041117: {"name": "Pony Tail Twirl", "count_id": {"item": 36, "level": 1}, "flag_id": None, "progression": True},
    14041118: {"name": "Monkeyport", "count_id": {"item": 37, "level": 1}, "flag_id": None, "progression": True},
    14041119: {"name": "progression Chunky Potion", "count_id": None, "flag_id": None, "progression": True},
    14041120: {"name": "Hunky Chunky", "count_id": {"item": 38, "level": 1}, "flag_id": None, "progression": True},
    14041121: {"name": "Primate Punch", "count_id": {"item": 39, "level": 1}, "flag_id": None, "progression": True},
    14041122: {"name": "Gorilla Gone", "count_id": {"item": 40, "level": 1}, "flag_id": None, "progression": True},
    14041123: {"name": "Coconut", "count_id": {"item": 46, "level": 1}, "flag_id": None, "progression": True},
    14041124: {"name": "Peanut", "count_id": {"item": 47, "level": 1}, "flag_id": None, "progression": True},
    14041125: {"name": "Grape", "count_id": {"item": 48, "level": 1}, "flag_id": None, "progression": True},
    14041126: {"name": "Feather", "count_id": {"item": 49, "level": 1}, "flag_id": None, "progression": True},
    14041127: {"name": "Pineapple", "count_id": {"item": 50, "level": 1}, "flag_id": None, "progression": True},
    14041128: {"name": "Homing Ammo", "count_id": {"item": 52, "level": 1}, "flag_id": None, "progression": True},
    14041129: {"name": "Sniper Sight", "count_id": {"item": 53, "level": 1}, "flag_id": None, "progression": True},
    14041130: {"name": "progression Ammo Belt", "count_id": {"item": 54, "level": 1}, "flag_id": None, "progression": True},
    14041131: {"name": "progression Ammo Belt ", "count_id": {"item": 54, "level": 2}, "flag_id": None, "progression": True},
    14041132: {"name": "Bongos", "count_id": {"item": 41, "level": 1}, "flag_id": None, "progression": True},
    14041133: {"name": "Guitar", "count_id": {"item": 42, "level": 1}, "flag_id": None, "progression": True},
    14041134: {"name": "Trombone", "count_id": {"item": 43, "level": 1}, "flag_id": None, "progression": True},
    14041135: {"name": "Saxophone", "count_id": {"item": 44, "level": 1}, "flag_id": None, "progression": True},
    14041136: {"name": "Triangle", "count_id": {"item": 45, "level": 1}, "flag_id": None, "progression": True},
    14041137: {"name": "progression Instrument Upgrade", "count_id": {"item": 55, "level": 1}, "flag_id": None, "progression": True},
    14041138: {"name": "progression Instrument Upgrade ", "count_id": {"item": 55, "level": 2}, "flag_id": None, "progression": True},
    14041139: {"name": "progression Instrument Upgrade  ", "count_id": {"item": 55, "level": 3}, "flag_id": None, "progression": True},
    14041140: {"name": "Fairy Camera", "count_id": {"field": "flag_moves", "bit": "camera"}, "flag_id": None, "progression": True},
    14041141: {"name": "Shockwave", "count_id": {"field": "flag_moves", "bit": "shockwave"}, "flag_id": None, "progression": True},
    14041142: {"name": "Camera and Shockwave", "count_id": [{"field": "flag_moves", "bit": "camera"}, {"field": "flag_moves", "bit": "shockwave"}], "flag_id": None, "progression": True},
    14041143: {"name": "Nintendo Coin", "count_id": {"field": "special_items", "bit": "nintendo_coin"}, "flag_id": None, "progression": True},
    14041144: {"name": "Rareware Coin", "count_id": {"field": "special_items", "bit": "rareware_coin"}, "flag_id": None, "progression": True},
    14041145: {"name": "Key 1", "count_id": {"field": "key_bitfield", "bit": 0}, "flag_id": None, "progression": True},
    14041146: {"name": "Key 2", "count_id": {"field": "key_bitfield", "bit": 1}, "flag_id": None, "progression": True},
    14041147: {"name": "Key 3", "count_id": {"field": "key_bitfield", "bit": 2}, "flag_id": None, "progression": True},
    14041148: {"name": "Key 4", "count_id": {"field": "key_bitfield", "bit": 3}, "flag_id": None, "progression": True},
    14041149: {"name": "Key 5", "count_id": {"field": "key_bitfield", "bit": 4}, "flag_id": None, "progression": True},
    14041150: {"name": "Key 6", "count_id": {"field": "key_bitfield", "bit": 5}, "flag_id": None, "progression": True},
    14041151: {"name": "Key 7", "count_id": {"field": "key_bitfield", "bit": 6}, "flag_id": None, "progression": True},
    14041152: {"name": "Key 8", "count_id": {"field": "key_bitfield", "bit": 7}, "flag_id": None, "progression": True},
    14041153: {"name": "Helm Donkey Barrel 1", "count_id": None, "flag_id": None},
    14041154: {"name": "Helm Donkey Barrel 2", "count_id": None, "flag_id": None},
    14041155: {"name": "Helm Diddy Barrel 1", "count_id": None, "flag_id": None},
    14041156: {"name": "Helm Diddy Barrel 2", "count_id": None, "flag_id": None},
    14041157: {"name": "Helm Lanky Barrel 1", "count_id": None, "flag_id": None},
    14041158: {"name": "Helm Lanky Barrel 2", "count_id": None, "flag_id": None},
    14041159: {"name": "Helm Tiny Barrel 1", "count_id": None, "flag_id": None},
    14041160: {"name": "Helm Tiny Barrel 2", "count_id": None, "flag_id": None},
    14041161: {"name": "Helm Chunky Barrel 1", "count_id": None, "flag_id": None},
    14041162: {"name": "Helm Chunky Barrel 2", "count_id": None, "flag_id": None},
    14041270: {"name": "Golden Banana", "count_id": {"item": 1, "level": 1}, "flag_id": None},
    14041271: {"name": "Banana Fairy", "count_id": {"field": "fairies", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041273: {"name": "Banana Medal", "count_id": {"field": "medals", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041272: {"name": "Battle Crown", "count_id": {"field": "crowns", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041167: {"name": "Bean", "count_id": {"field": "special_items", "bit": "bean"}, "flag_id": None, "progression": True},
    14041353: {"name": "Forest Second Anthill Reward", "count_id": {"field": "special_items", "bit": "bean"}, "flag_id": None},
    14041269: {"name": "Pearl", "count_id": {"field": "pearls", "increment": 1}, "flag_id": None, "progression": True},
    14041354: {"name": "Rainbow Coin", "count_id": {"field": "rainbow_coins", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041170: {"name": "Bubble Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "bubble"}, "flag_id": None, "extended_whitelist": True},
    14041171: {"name": "Reverse Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "reverse"}, "flag_id": None, "extended_whitelist": True},
    14041172: {"name": "Slow Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "slow"}, "flag_id": None, "extended_whitelist": True},
    14041262: {"name": "Ice Trap (Bubble - Bean)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "bubble"}, "flag_id": None, "extended_whitelist": True},
    14041263: {"name": "Ice Trap (Reverse - Bean)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "reverse"}, "flag_id": None, "extended_whitelist": True},
    14041264: {"name": "Ice Trap (Slow - Bean)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "slow"}, "flag_id": None, "extended_whitelist": True},
    14041265: {"name": "Ice Trap (Bubble - Key)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "bubble"}, "flag_id": None, "extended_whitelist": True},
    14041266: {"name": "Ice Trap (Reverse - Key)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "reverse"}, "flag_id": None, "extended_whitelist": True},
    14041267: {"name": "Ice Trap (Slow - Key)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "slow"}, "flag_id": None, "extended_whitelist": True},
    14041274: {"name": "Disable A Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_a"}, "flag_id": None, "extended_whitelist": True},
    14041275: {"name": "Ice Trap (Disable A - Bean)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_a"}, "flag_id": None, "extended_whitelist": True},
    14041276: {"name": "Ice Trap (Disable A - Key)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_a"}, "flag_id": None, "extended_whitelist": True},
    14041277: {"name": "Disable B Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_b"}, "flag_id": None, "extended_whitelist": True},
    14041278: {"name": "Ice Trap (Disable B - Bean)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_b"}, "flag_id": None, "extended_whitelist": True},
    14041279: {"name": "Ice Trap (Disable B - Key)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_b"}, "flag_id": None, "extended_whitelist": True},
    14041280: {"name": "Disable Z Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_z"}, "flag_id": None, "extended_whitelist": True},
    14041281: {"name": "Ice Trap (Disable Z - Bean)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_z"}, "flag_id": None, "extended_whitelist": True},
    14041282: {"name": "Ice Trap (Disable Z - Key)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_z"}, "flag_id": None, "extended_whitelist": True},
    14041283: {"name": "Disable C Up Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_c_up"}, "flag_id": None, "extended_whitelist": True},
    14041284: {"name": "Ice Trap (Disable C Up - Bean)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_c_up"}, "flag_id": None, "extended_whitelist": True},
    14041285: {"name": "Ice Trap (Disable C Up - Key)", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disable_c_up"}, "flag_id": None, "extended_whitelist": True},
    14041323: {"name": "Get Out Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "get_out"}, "flag_id": None, "extended_whitelist": True},
    14041326: {"name": "Dry Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "dry"}, "flag_id": None, "extended_whitelist": True},
    14041329: {"name": "Flip Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "flip"}, "flag_id": None, "extended_whitelist": True},
    14041342: {"name": "Ice Floor Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "icefloor"}, "flag_id": None, "extended_whitelist": True},
    14041346: {"name": "Paper Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "paper"}, "flag_id": None, "extended_whitelist": True},
    14041350: {"name": "Slip Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "slip"}, "flag_id": None, "extended_whitelist": True},
    14041369: {"name": "Animal Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "animal"}, "flag_id": None, "extended_whitelist": True},
    14041373: {"name": "Rockfall Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "rockfall"}, "flag_id": None, "extended_whitelist": True},
    14041377: {"name": "Disable Tag Trap", "count_id": {"field": "ice_traps", "increment": 1, "ice_trap_type": "disabletag"}, "flag_id": None, "extended_whitelist": True},
    14041173: {"name": "Junk Item (Crystal)", "count_id": {"field": "junk_items", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041174: {"name": "Junk Item (Melon Slice)", "count_id": {"field": "junk_items", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041175: {"name": "Junk Item (Ammo Crate)", "count_id": {"field": "junk_items", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041176: {"name": "Junk Item (Film)", "count_id": {"field": "junk_items", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041177: {"name": "Junk Item (Orange)", "count_id": {"field": "junk_items", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041178: {"name": "Crate Melon", "count_id": {"field": "junk_items", "increment": 1}, "flag_id": None, "extended_whitelist": True},
    14041179: {"name": "Enemy Item", "count_id": None, "flag_id": None},
    14041180: {"name": "Cranky", "count_id": None, "flag_id": 962, "progression": True},
    14041181: {"name": "Funky", "count_id": None, "flag_id": 963, "progression": True},
    14041182: {"name": "Candy", "count_id": None, "flag_id": 964, "progression": True},
    14041183: {"name": "Snide", "count_id": None, "flag_id": 965, "progression": True},
    14041358: {"name": "Donkey Blueprint", "count_id": {"field": "bp_count", "kong": 0}, "flag_id": None, "extended_whitelist": True},
    14041359: {"name": "Diddy Blueprint", "count_id": {"field": "bp_count", "kong": 1}, "flag_id": None, "extended_whitelist": True},
    14041360: {"name": "Lanky Blueprint", "count_id": {"field": "bp_count", "kong": 2}, "flag_id": None, "extended_whitelist": True},
    14041361: {"name": "Tiny Blueprint", "count_id": {"field": "bp_count", "kong": 3}, "flag_id": None, "extended_whitelist": True},
    14041362: {"name": "Chunky Blueprint", "count_id": {"field": "bp_count", "kong": 4}, "flag_id": None, "extended_whitelist": True},
    14041185: {"name": "Japes Donkey Hint", "count_id": {"field": "hint_bitfield", "kong": 0, "level": 0}, "flag_id": None, "extended_whitelist": True},
    14041186: {"name": "Japes Diddy Hint", "count_id": {"field": "hint_bitfield", "kong": 1, "level": 0}, "flag_id": None, "extended_whitelist": True},
    14041187: {"name": "Japes Lanky Hint", "count_id": {"field": "hint_bitfield", "kong": 2, "level": 0}, "flag_id": None, "extended_whitelist": True},
    14041188: {"name": "Japes Tiny Hint", "count_id": {"field": "hint_bitfield", "kong": 3, "level": 0}, "flag_id": None, "extended_whitelist": True},
    14041189: {"name": "Japes Chunky Hint", "count_id": {"field": "hint_bitfield", "kong": 4, "level": 0}, "flag_id": None, "extended_whitelist": True},
    14041190: {"name": "Aztec Donkey Hint", "count_id": {"field": "hint_bitfield", "kong": 0, "level": 1}, "flag_id": None, "extended_whitelist": True},
    14041191: {"name": "Aztec Diddy Hint", "count_id": {"field": "hint_bitfield", "kong": 1, "level": 1}, "flag_id": None, "extended_whitelist": True},
    14041192: {"name": "Aztec Lanky Hint", "count_id": {"field": "hint_bitfield", "kong": 2, "level": 1}, "flag_id": None, "extended_whitelist": True},
    14041193: {"name": "Aztec Tiny Hint", "count_id": {"field": "hint_bitfield", "kong": 3, "level": 1}, "flag_id": None, "extended_whitelist": True},
    14041194: {"name": "Aztec Chunky Hint", "count_id": {"field": "hint_bitfield", "kong": 4, "level": 1}, "flag_id": None, "extended_whitelist": True},
    14041195: {"name": "Factory Donkey Hint", "count_id": {"field": "hint_bitfield", "kong": 0, "level": 2}, "flag_id": None, "extended_whitelist": True},
    14041196: {"name": "Factory Diddy Hint", "count_id": {"field": "hint_bitfield", "kong": 1, "level": 2}, "flag_id": None, "extended_whitelist": True},
    14041197: {"name": "Factory Lanky Hint", "count_id": {"field": "hint_bitfield", "kong": 2, "level": 2}, "flag_id": None, "extended_whitelist": True},
    14041198: {"name": "Factory Tiny Hint", "count_id": {"field": "hint_bitfield", "kong": 3, "level": 2}, "flag_id": None, "extended_whitelist": True},
    14041199: {"name": "Factory Chunky Hint", "count_id": {"field": "hint_bitfield", "kong": 4, "level": 2}, "flag_id": None, "extended_whitelist": True},
    14041200: {"name": "Galleon Donkey Hint", "count_id": {"field": "hint_bitfield", "kong": 0, "level": 3}, "flag_id": None, "extended_whitelist": True},
    14041201: {"name": "Galleon Diddy Hint", "count_id": {"field": "hint_bitfield", "kong": 1, "level": 3}, "flag_id": None, "extended_whitelist": True},
    14041202: {"name": "Galleon Lanky Hint", "count_id": {"field": "hint_bitfield", "kong": 2, "level": 3}, "flag_id": None, "extended_whitelist": True},
    14041203: {"name": "Galleon Tiny Hint", "count_id": {"field": "hint_bitfield", "kong": 3, "level": 3}, "flag_id": None, "extended_whitelist": True},
    14041204: {"name": "Galleon Chunky Hint", "count_id": {"field": "hint_bitfield", "kong": 4, "level": 3}, "flag_id": None, "extended_whitelist": True},
    14041205: {"name": "Forest Donkey Hint", "count_id": {"field": "hint_bitfield", "kong": 0, "level": 4}, "flag_id": None, "extended_whitelist": True},
    14041206: {"name": "Forest Diddy Hint", "count_id": {"field": "hint_bitfield", "kong": 1, "level": 4}, "flag_id": None, "extended_whitelist": True},
    14041207: {"name": "Forest Lanky Hint", "count_id": {"field": "hint_bitfield", "kong": 2, "level": 4}, "flag_id": None, "extended_whitelist": True},
    14041208: {"name": "Forest Tiny Hint", "count_id": {"field": "hint_bitfield", "kong": 3, "level": 4}, "flag_id": None, "extended_whitelist": True},
    14041209: {"name": "Forest Chunky Hint", "count_id": {"field": "hint_bitfield", "kong": 4, "level": 4}, "flag_id": None, "extended_whitelist": True},
    14041210: {"name": "Caves Donkey Hint", "count_id": {"field": "hint_bitfield", "kong": 0, "level": 5}, "flag_id": None, "extended_whitelist": True},
    14041211: {"name": "Caves Diddy Hint", "count_id": {"field": "hint_bitfield", "kong": 1, "level": 5}, "flag_id": None, "extended_whitelist": True},
    14041212: {"name": "Caves Lanky Hint", "count_id": {"field": "hint_bitfield", "kong": 2, "level": 5}, "flag_id": None, "extended_whitelist": True},
    14041213: {"name": "Caves Tiny Hint", "count_id": {"field": "hint_bitfield", "kong": 3, "level": 5}, "flag_id": None, "extended_whitelist": True},
    14041214: {"name": "Caves Chunky Hint", "count_id": {"field": "hint_bitfield", "kong": 4, "level": 5}, "flag_id": None, "extended_whitelist": True},
    14041215: {"name": "Castle Donkey Hint", "count_id": {"field": "hint_bitfield", "kong": 0, "level": 6}, "flag_id": None, "extended_whitelist": True},
    14041216: {"name": "Castle Diddy Hint", "count_id": {"field": "hint_bitfield", "kong": 1, "level": 6}, "flag_id": None, "extended_whitelist": True},
    14041217: {"name": "Castle Lanky Hint", "count_id": {"field": "hint_bitfield", "kong": 2, "level": 6}, "flag_id": None, "extended_whitelist": True},
    14041218: {"name": "Castle Tiny Hint", "count_id": {"field": "hint_bitfield", "kong": 3, "level": 6}, "flag_id": None, "extended_whitelist": True},
    14041219: {"name": "Castle Chunky Hint", "count_id": {"field": "hint_bitfield", "kong": 4, "level": 6}, "flag_id": None, "extended_whitelist": True},
    14041184: {"name": "Banana Hoard", "count_id": None, "flag_id": None},
    14041088: {"name": "Victory", "count_id": None, "flag_id": None},
    14041314: {"name": "Treasure Chest Far Left Clam", "count_id": None, "flag_id": 0xBA},
    14041315: {"name": "Treasure Chest Center Clam", "count_id": None, "flag_id": 0xBB},
    14041316: {"name": "Treasure Chest Far Right Clam", "count_id": None, "flag_id": 0xBC},
    14041317: {"name": "Treasure Chest Close Right Clam", "count_id": None, "flag_id": 0xBD},
    14041318: {"name": "Treasure Chest Close Left Clam", "count_id": None, "flag_id": 0xBE},
    14041695: {"name": "Aztec Crate: On Llama Temple", "count_id": None, "flag_id": 0x3B2},
    14041696: {"name": "Aztec Crate: Near Gong Tower", "count_id": None, "flag_id": 0x3B3},
    14041691: {"name": "Aztec Crate: Llama Temple Entrance", "count_id": None, "flag_id": 0x3AE},
    14041701: {"name": "Castle Crate: Behind Mausoleum Entrance", "count_id": None, "flag_id": 0x3B8},
    14041697: {"name": "Forest Crate: Near Owl Tree", "count_id": None, "flag_id": 0x3B4},
    14041699: {"name": "Forest Crate: Behind Dark Attic", "count_id": None, "flag_id": 0x3B6},
    14041698: {"name": "Forest Crate: Near Thornvine Barn", "count_id": None, "flag_id": 0x3B5},
    14041700: {"name": "Forest Crate: In Thornvine Barn", "count_id": None, "flag_id": 0x3B7},
    14041689: {"name": "Japes Crate: Behind the Mountain", "count_id": None, "flag_id": 0x3AC},
    14041690: {"name": "Japes Crate: In the Rambi Cave", "count_id": None, "flag_id": 0x3AD},
    14041692: {"name": "Factory Crate: Near Funky", "count_id": None, "flag_id": 0x3AF},
    14041693: {"name": "Factory Crate: Near Candy", "count_id": None, "flag_id": 0x3B0},
    14041694: {"name": "Galleon Crate: Near Cactus", "count_id": None, "flag_id": 0x3B1},
}


# Automatically create another table that is the Name to the key
item_names_to_id = {item_ids[key]["name"]: key for key in item_ids}

# For TrapLink
trap_name_to_index: dict[str, int] = {
    # Our native Traps
    "Bubble Trap": 1,
    "Reverse Trap": 2,
    "Slow Trap": 3,
    "Disable A Trap": 5,
    "Disable B Trap": 6,
    "Disable Z Trap": 7,
    "Disable C Up Trap": 8,
    "Get Out Trap": 9,
    "Dry Trap": 10,
    "Flip Trap": 11,
    "Ice Floor Trap": 12,
    "Paper Trap": 13,
    "Slip Trap": 15,
    "Animal Trap": 16,
    "Rockfall Trap": 17,
    "Disable Tag Trap": 18,
    # Common other trap names
    "Banana Peel Trap": 15,  # Slip Trap
    "Bee Trap": 6,  # Disable B Trap
    "Blue Balls Curse": 1,  # Bubble Trap
    "Buyon Trap": 9,  # Get Out Trap
    "Camera Rotate Trap": 11,  # Flip Trap
    "Chaos Control Trap": 1,  # Bubble Trap
    "Confound Trap": 2,  # Reverse Trap
    "Confuse Trap": 2,  # Reverse Trap
    "Confusion Trap": 2,  # Reverse Trap
    "Damage Trap": 9,  # Get Out Trap
    "Deisometric Trap": 13,  # Paper Trap
    "Depletion Trap": 10,  # Dry Trap
    "Eject Ability": 10,  # Dry Trap
    "Fear Trap": 3,  # Slow Trap
    "Freeze Trap": 1,  # Bubble Trap
    "Frozen Trap": 1,  # Bubble Trap
    "Fuzzy Trap": 2,  # Reverse Trap
    "Home Trap": 9,  # Get Out Trap
    "Honey Trap": 5,  # Disable A Trap
    "Ice Trap": 12,  # Ice Floor Trap
    "Instant Crystal Trap": 1,  # Bubble Trap
    "Instant Death Trap": 9,  # Get Out Trap
    "Invisible Trap": 13,  # Paper Trap
    "Iron Boots Trap": 5,  # Disable A Trap
    "Jump Trap": 5,  # Disable A Trap
    "Literature Trap": 13,  # Paper Trap
    "Mirror Trap": 11,  # Flip Trap
    "Monkey Mash Trap": 2,  # Reverse Trap
    "No Stocks": 10,  # Dry Trap
    "No Vac Trap": 7,  # Disable Z Trap
    "Paralyze Trap": 1,  # Bubble Trap
    "Poison Mushroom": 3,  # Slow Trap
    "Poison Trap": 10,  # Dry Trap
    "Police Trap": 9,  # Get Out Trap
    "PowerPoint Trap": 13,  # Paper Trap
    "Push Trap": 12,  # Ice Floor Trap
    "Resistance Trap": 9,  # Get Out Trap
    "Reversal Trap": 2,  # Reverse Trap
    "Screen Flip Trap": 11,  # Flip Trap
    "Slowness Trap": 3,  # Slow Trap
    "Spike Ball Trap": 9,  # Get Out Trap
    "Spooky Time": 13,  # Paper Trap
    "Sticky Floor Trap": 5,  # Disable A Trap
    "Stun Trap": 1,  # Bubble Trap
    "Time Limit": 9,  # Get Out Trap
    "Timer Trap": 9,  # Slow Trap
    "Tiny Trap": 13,  # Paper Trap
    "W I D E Trap": 13,  # Paper Trap
}

trap_index_to_name: dict[int, str] = {
    1: "Bubble Trap",
    2: "Reverse Trap",
    3: "Slow Trap",
    5: "Disable A Trap",
    6: "Disable B Trap",
    7: "Disable Z Trap",
    8: "Disable C Up Trap",
    9: "Get Out Trap",
    10: "Dry Trap",
    11: "Flip Trap",
    12: "Ice Floor Trap",
    13: "Paper Trap",
    15: "Slip Trap",
    16: "Animal Trap",
    17: "Rockfall Trap",
    18: "Disable Tag Trap",
}

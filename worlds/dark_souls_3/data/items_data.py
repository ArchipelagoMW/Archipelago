class ItemData:
    pass


rings_table = {
    "Covetous Silver Serpent Ring": 0x20004FB0,
    "Estus Ring": 0x200050DC,
    "Flame Stoneplate Ring": 0x20004E52,
    "Fire Clutch Ring": 0x2000501E,
}

weapons_table = {
    "Rapier": 0x002E14E0,
    "East-West Shield": 0x0142B930,
    "Longbow": 0x00D689E0,
    "Mail Breaker": 0x002DEDD0,
    "Astora Straight Sword": 0x002191C0,
    "Broken Straight Sword": 0x001EF9B0,
}

flask_items_table = {
    "Estus Flask Shard": 0x4000085D,
    "Ash Estus Flask": 0x400000BF,
    "Undead Bone Shard": 0x4000085F,
}

dictionary_table = {**rings_table, **weapons_table, **flask_items_table }
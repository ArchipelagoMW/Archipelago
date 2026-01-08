from enum import IntFlag


class MinishootPool(IntFlag):
    default = 0
    xp_crystals = 1
    npc = 2
    scarab = 4
    spirit = 8
    dungeon_small_key = 16
    dungeon_big_key = 32
    dungeon_reward = 64
    goal = 128

def get_item_pool(item_name: str) -> MinishootPool:
    item_pool_mapping = {
        'Default': MinishootPool.default,
        'XP Crystals': MinishootPool.xp_crystals,
        'NPC': MinishootPool.npc,
        'Scarab': MinishootPool.scarab,
        'Spirit': MinishootPool.spirit,
        'Dungeon Small Key': MinishootPool.dungeon_small_key,
        'Dungeon Big Key': MinishootPool.dungeon_big_key,
        'Dungeon Reward': MinishootPool.dungeon_reward,
        'Goal': MinishootPool.goal,
    }

    if item_name not in item_pool_mapping:
        return MinishootPool.default

    return item_pool_mapping[item_name]

from typing import Dict, List
from .zones import zone_table

dungeon_reward_location_mapping: Dict[str, str] = {
    "Dungeon 1 Reward": "Dungeon 1 - Dungeon reward",
    "Dungeon 2 Reward": "Dungeon 2 - Dungeon reward",
    "Dungeon 3 Reward": "Dungeon 3 - Dungeon reward",
    "Dungeon 4 Reward": "Dungeon 4 - Dungeon reward",
}

dungeon_item_mapping: Dict[str, List[str]] = {
    "Dungeon 1": ["Small Key (Dungeon 1)", "Boss Key (Dungeon 1)"],
    "Dungeon 2": ["Small Key (Dungeon 2)", "Boss Key (Dungeon 2)"],
    "Dungeon 3": ["Small Key (Dungeon 3)", "Boss Key (Dungeon 3)"],
}

def get_dungeons() -> List[str]:
    return list(dungeon_item_mapping.keys())

def get_dungeon_for_item(item_name: str) -> str:
    for dungeon_name, items in dungeon_item_mapping.items():
        if item_name in items:
            return dungeon_name
    return None

def get_dungeon_for_location(location_name: str) -> str:
    for dungeon_name in dungeon_item_mapping.keys():
        if dungeon_name not in zone_table.keys():
            continue
        zone = zone_table[dungeon_name]
        if location_name in zone.locations:
            return dungeon_name

    return None
    
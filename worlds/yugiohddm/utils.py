import typing

from dataclasses import dataclass

@dataclass
class Constants:
    # YGO DDM constants!
    GAME_NAME: str = "Yu-Gi-Oh! Dungeon Dice Monsters"
    VICTORY_ITEM_ID: int = 0x03E30A # Data is 2 Byte size
    VICTORY_ITEM_NAME: str = "Yami Yugi Defeated"
    DUEL_WINS_OFFSET: int = 0x03E30A # Data is 2 Byte size, technically a copy of Victory Item ID
    DUELIST_UNLOCK_OFFSET: int = 0x03E64E # Data is 1 Byte size
    DICE_COLLECTION_OFFSET: int = 0x03E565 # Data is 1 Byte size
    RECEIVED_DICE_COUNT_OFFSET: int = 0x03E3C4 # Data is 1 Byte size

    GENERATED_WITH_KEY: str = "k"
    DUELIST_UNLOCK_ORDER_KEY: str = "d"
    GAME_OPTIONS_KEY: str = "g"
from BaseClasses import Item
import typing
from typing import Dict


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


item_table: Dict[str, ItemData] = {
    'Boomerang': ItemData(100, False),
    'Bow': ItemData(101, True),
    'Magical Boomerang': ItemData(102, False),
    'Raft': ItemData(103, True),
    'Stepladder': ItemData(104, True),
    'Recorder': ItemData(105, True),
    'Magical Rod': ItemData(106, True),
    'Red Candle': ItemData(107, True),
    'Book of Magic': ItemData(108, True),
    'Magical Key': ItemData(109, False),
    'Red Ring': ItemData(110, False),
    'Silver Arrow': ItemData(111, True),
    'Sword': ItemData(112, True),
    'White Sword': ItemData(113, True),
    'Magical Sword': ItemData(114, True),
    'Heart Container': ItemData(115, True),
    'Letter': ItemData(116, False),
    'Magical Shield': ItemData(117, False),
    'Candle': ItemData(118, True),
    'Arrow': ItemData(119, True),
    'Food': ItemData(120, True),
    'Water of Life (Blue)': ItemData(121, False),
    'Water of Life (Red)': ItemData(122, False),
    'Blue Ring': ItemData(123, False),
    'Triforce Fragment': ItemData(124, True),
    'Power Bracelet': ItemData(125, False),
    'Small Key': ItemData(126, False),
    'Bomb': ItemData(127, False),
    'Recovery Heart': ItemData(128, False),
    'Five Rupees': ItemData(129, False),
    'Rupee': ItemData(129, False),
}

item_amounts_all = {
    "Heart Container": 13,
    "Magical Shield": 3,
    "Food": 2,
    "Triforce Fragment": 8,
    "Small Key": 27,
    "Bomb": 18,
    "Five Rupees": 13,
    "Water of Life (Red)": 5,
    "Silver Arrow": 2,
    "Rupee": 0
}

item_amounts_standard = {
    "Heart Container": 9,
    "Magical Shield": 3,
    "Food": 2,
    "Bomb": 0,
    "Five Rupees": 0,
    "Triforce Fragment": 8,
    "Silver Arrow": 2,
    "Rupee": 0
}

item_game_ids = {
    "Bomb": 0x00,
    "Sword": 0x01,
    "White Sword": 0x02,
    "Magical Sword": 0x03,
    "Food": 0x04,
    "Recorder": 0x05,
    "Candle": 0x06,
    "Red Candle": 0x07,
    "Arrow": 0x08,
    "Silver Arrow": 0x09,
    "Bow": 0x0A,
    "Magical Key": 0x0B,
    "Raft": 0x0C,
    "Stepladder": 0x0D,
    "Five Rupees": 0x0F,
    "Magical Rod": 0x10,
    "Book of Magic": 0x11,
    "Blue Ring": 0x12,
    "Red Ring": 0x13,
    "Power Bracelet": 0x14,
    "Letter": 0x15,
    "Small Key": 0x19,
    "Heart Container": 0x1A,
    "Triforce Fragment": 0x1B,
    "Magical Shield": 0x1C,
    "Boomerang": 0x1D,
    "Magical Boomerang": 0x1E,
    "Water of Life (Blue)": 0x1F,
    "Water of Life (Red)": 0x20,
    "Recovery Heart": 0x22,
    "Rupee": 0x18
}

item_prices = {
    "Bomb": 10,
    "Sword": 10,
    "White Sword": 40,
    "Magical Sword": 160,
    "Food": 30,
    "Recorder": 25,
    "Candle": 30,
    "Red Candle": 60,
    "Arrow": 40,
    "Silver Arrow": 160,
    "Bow": 40,
    "Magical Key": 250,
    "Raft": 80,
    "Stepladder": 80,
    "Five Rupees": 255,
    "Magical Rod": 100,
    "Book of Magic": 60,
    "Blue Ring": 125,
    "Red Ring": 250,
    "Power Bracelet": 25,
    "Letter": 20,
    "Small Key": 40,
    "Heart Container": 80,
    "Triforce Fragment": 80,
    "Magical Shield": 45,
    "Boomerang": 5,
    "Magical Boomerang": 20,
    "Water of Life (Blue)": 20,
    "Water of Life (Red)": 34,
    "Recovery Heart": 5,
    "Rupee": 50
}
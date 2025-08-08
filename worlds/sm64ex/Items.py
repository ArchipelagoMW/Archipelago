from typing import NamedTuple

from BaseClasses import Item, ItemClassification

sm64ex_base_id: int = 3626000

class SM64Item(Item):
    game: str = "Super Mario 64"

class SM64ItemData(NamedTuple):
    code: int | None = None
    classification: ItemClassification = ItemClassification.progression

generic_item_data_table: dict[str, SM64ItemData] = {
    "Power Star": SM64ItemData(sm64ex_base_id + 0, ItemClassification.progression_skip_balancing),
    "Basement Key": SM64ItemData(sm64ex_base_id + 178),
    "Second Floor Key": SM64ItemData(sm64ex_base_id + 179),
    "Progressive Key": SM64ItemData(sm64ex_base_id + 180),
    "Wing Cap": SM64ItemData(sm64ex_base_id + 181),
    "Metal Cap": SM64ItemData(sm64ex_base_id + 182),
    "Vanish Cap": SM64ItemData(sm64ex_base_id + 183),
    "1Up Mushroom": SM64ItemData(sm64ex_base_id + 184, ItemClassification.filler),
}

action_item_data_table: dict[str, SM64ItemData] = {
    "Double Jump": SM64ItemData(sm64ex_base_id + 185),
    "Triple Jump": SM64ItemData(sm64ex_base_id + 186),
    "Long Jump": SM64ItemData(sm64ex_base_id + 187),
    "Backflip": SM64ItemData(sm64ex_base_id + 188),
    "Side Flip": SM64ItemData(sm64ex_base_id + 189),
    "Wall Kick": SM64ItemData(sm64ex_base_id + 190),
    "Dive": SM64ItemData(sm64ex_base_id + 191),
    "Ground Pound": SM64ItemData(sm64ex_base_id + 192),
    "Kick": SM64ItemData(sm64ex_base_id + 193),
    "Climb": SM64ItemData(sm64ex_base_id + 194),
    "Ledge Grab": SM64ItemData(sm64ex_base_id + 195),
}

cannon_item_data_table: dict[str, SM64ItemData] = {
    "Cannon Unlock BoB": SM64ItemData(sm64ex_base_id + 200),
    "Cannon Unlock WF": SM64ItemData(sm64ex_base_id + 201),
    "Cannon Unlock JRB": SM64ItemData(sm64ex_base_id + 202),
    "Cannon Unlock CCM": SM64ItemData(sm64ex_base_id + 203),
    "Cannon Unlock SSL": SM64ItemData(sm64ex_base_id + 207),
    "Cannon Unlock SL": SM64ItemData(sm64ex_base_id + 209),
    "Cannon Unlock WDW": SM64ItemData(sm64ex_base_id + 210),
    "Cannon Unlock TTM": SM64ItemData(sm64ex_base_id + 211),
    "Cannon Unlock THI": SM64ItemData(sm64ex_base_id + 212),
    "Cannon Unlock RR": SM64ItemData(sm64ex_base_id + 214),
}

painting_unlock_item_data_table: dict[str, SM64ItemData] = {
    "Painting Unlock WF": SM64ItemData(sm64ex_base_id + 231),
    "Painting Unlock JRB": SM64ItemData(sm64ex_base_id + 232),
    "Painting Unlock CCM": SM64ItemData(sm64ex_base_id + 233),
    "Painting Unlock LLL": SM64ItemData(sm64ex_base_id + 236),
    "Painting Unlock SSL": SM64ItemData(sm64ex_base_id + 237),
    "Painting Unlock DDD": SM64ItemData(sm64ex_base_id + 238),
    "Painting Unlock SL": SM64ItemData(sm64ex_base_id + 239),
    "Painting Unlock WDW": SM64ItemData(sm64ex_base_id + 240),
    "Painting Unlock TTM": SM64ItemData(sm64ex_base_id + 241),
    "Painting Unlock THI": SM64ItemData(sm64ex_base_id + 242),
    "Painting Unlock TTC": SM64ItemData(sm64ex_base_id + 243),
}

item_data_table = {
    **generic_item_data_table,
    **action_item_data_table,
    **cannon_item_data_table,
    **painting_unlock_item_data_table
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

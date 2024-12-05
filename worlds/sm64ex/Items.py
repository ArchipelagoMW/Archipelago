from typing import NamedTuple

from BaseClasses import Item, ItemClassification

sm64ex_base_id: int = 3626000

class SM64Item(Item):
    game: str = "Super Mario 64"

class SM64ItemData(NamedTuple):
    code: int | None = None
    classification: ItemClassification = ItemClassification.filler
    description: str = ""

generic_item_data_table: dict[str, SM64ItemData] = {
    "Power Star": SM64ItemData(sm64ex_base_id + 0, ItemClassification.progression_skip_balancing, "Collectable reward for course objectives and secrets. Needed to unlock parts of the castle."),
    "Basement Key": SM64ItemData(sm64ex_base_id + 178, ItemClassification.progression, "The key to the basement."),
    "Second Floor Key": SM64ItemData(sm64ex_base_id + 179, ItemClassification.progression, "The key to the second floor. Also necessary to reach the third floor."),
    "Progressive Key": SM64ItemData(sm64ex_base_id + 180, ItemClassification.progression, "A key to another floor of the castle."),
    "Wing Cap": SM64ItemData(sm64ex_base_id + 181, ItemClassification.progression, "A powerup for Mario. Grants flight."),
    "Metal Cap": SM64ItemData(sm64ex_base_id + 182, ItemClassification.progression, "A powerup for Mario. Grants passage through certain walls."),
    "Vanish Cap": SM64ItemData(sm64ex_base_id + 183, ItemClassification.progression, "A powerup for Mario. Grants increased strength and weight."),
    "1Up Mushroom": SM64ItemData(sm64ex_base_id + 184, ItemClassification.filler, "An extra life."),
}

action_item_data_table: dict[str, SM64ItemData] = {
    "Double Jump": SM64ItemData(sm64ex_base_id + 185, ItemClassification.progression),
    "Triple Jump": SM64ItemData(sm64ex_base_id + 186, ItemClassification.progression),
    "Long Jump": SM64ItemData(sm64ex_base_id + 187, ItemClassification.progression),
    "Backflip": SM64ItemData(sm64ex_base_id + 188, ItemClassification.progression),
    "Side Flip": SM64ItemData(sm64ex_base_id + 189, ItemClassification.progression),
    "Wall Kick": SM64ItemData(sm64ex_base_id + 190, ItemClassification.progression),
    "Dive": SM64ItemData(sm64ex_base_id + 191, ItemClassification.progression),
    "Ground Pound": SM64ItemData(sm64ex_base_id + 192, ItemClassification.progression),
    "Kick": SM64ItemData(sm64ex_base_id + 193, ItemClassification.progression),
    "Climb": SM64ItemData(sm64ex_base_id + 194, ItemClassification.progression),
    "Ledge Grab": SM64ItemData(sm64ex_base_id + 195, ItemClassification.progression),
}

cannon_item_data_table: dict[str, SM64ItemData] = {
    "Cannon Unlock BoB": SM64ItemData(sm64ex_base_id + 200, ItemClassification.progression),
    "Cannon Unlock WF": SM64ItemData(sm64ex_base_id + 201, ItemClassification.progression),
    "Cannon Unlock JRB": SM64ItemData(sm64ex_base_id + 202, ItemClassification.progression),
    "Cannon Unlock CCM": SM64ItemData(sm64ex_base_id + 203, ItemClassification.progression),
    "Cannon Unlock SSL": SM64ItemData(sm64ex_base_id + 207, ItemClassification.progression),
    "Cannon Unlock SL": SM64ItemData(sm64ex_base_id + 209, ItemClassification.progression),
    "Cannon Unlock WDW": SM64ItemData(sm64ex_base_id + 210, ItemClassification.progression),
    "Cannon Unlock TTM": SM64ItemData(sm64ex_base_id + 211, ItemClassification.progression),
    "Cannon Unlock THI": SM64ItemData(sm64ex_base_id + 212, ItemClassification.progression),
    "Cannon Unlock RR": SM64ItemData(sm64ex_base_id + 214, ItemClassification.progression),
}

item_data_table = {
    **generic_item_data_table,
    **action_item_data_table,
    **cannon_item_data_table
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

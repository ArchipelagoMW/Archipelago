from BaseClasses import Item, ItemClassification
import typing

class ShiversItem(Item):
    game: str = "Shivers"

class ItemData(typing.NamedTuple):
    code: int
    type: str
    classification: ItemClassification = ItemClassification.progression

def get_full_item_list():
    return item_table

SHIVERS_ITEM_ID_OFFSET = 20000

item_table = {
    #Pot Pieces
    "Water Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 0, "pot"),
    "Wax Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 1, "pot"),
    "Ash Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 2, "pot"),
    "Oil Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 3, "pot"),
    "Cloth Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 4, "pot"),
    "Wood Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 5, "pot"),
    "Crystal Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 6, "pot"),
    "Lightning Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 7, "pot"),
    "Sand Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 8, "pot"),
    "Metal Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 9, "pot"),
    "Water Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 10, "pot"),
    "Wax Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 11, "pot"),
    "Ash Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 12, "pot"),
    "Oil Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 13, "pot"),
    "Cloth Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 14, "pot"),
    "Wood Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 15, "pot"),
    "Crystal Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 16, "pot"),
    "Lightning Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 17, "pot"),
    "Sand Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 18, "pot"),
    "Metal Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 19, "pot"),

    #Keys
    "Elevator Key: Office": ItemData(SHIVERS_ITEM_ID_OFFSET + 20, "key"),
    "Elevator Key: Bedroom": ItemData(SHIVERS_ITEM_ID_OFFSET + 21, "key"),
    "Elevator Key: Three Floor": ItemData(SHIVERS_ITEM_ID_OFFSET + 22, "key"),
    "Key: Workshop": ItemData(SHIVERS_ITEM_ID_OFFSET + 23, "key"),
    "Key: Prehistoric Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 24, "key"),
    "Key: Plants Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 25, "key"),
    "Key: Ocean Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 26, "key"),
    "Key: Projector Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 27, "key"),
    "Key: Generator Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 28, "key"),
    "Key: Library Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 29, "key"),
    "Key: Tiki Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 30, "key"),
    "Key: UFO Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 31, "key"),
    "Key: Torture Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 32, "key"),
    "Key: Puzzle Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 33, "key"),
    "Key: Bedroom Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 34, "key"),
    "Key: Underground Lake Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 35, "key"),

    #Abilities
    "Crawling": ItemData(SHIVERS_ITEM_ID_OFFSET + 50, "ability"),

    #Filler
    "Filler 1": ItemData(SHIVERS_ITEM_ID_OFFSET + 70, "filler"),
    "Filler 2": ItemData(SHIVERS_ITEM_ID_OFFSET + 71, "filler")
}

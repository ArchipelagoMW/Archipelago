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
    "Metal Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 19, "pot"),

    #Keys
    "Key for Office Elevator": ItemData(SHIVERS_ITEM_ID_OFFSET + 20, "key"),
    "Key for Bedroom Elevator": ItemData(SHIVERS_ITEM_ID_OFFSET + 21, "key"),
    "Key for Three Floor Elevator": ItemData(SHIVERS_ITEM_ID_OFFSET + 22, "key"),
    "Key for Workshop": ItemData(SHIVERS_ITEM_ID_OFFSET + 23, "key"),
    "Key for Lobby": ItemData(SHIVERS_ITEM_ID_OFFSET + 24, "key"),
    "Key for Prehistoric Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 25, "key"),
    "Key for Plants Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 26, "key"),
    "Key for Ocean Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 27, "key"),
    "Key for Projector Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 28, "key"),
    "Key for Generator Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 29, "key"),
    "Key for Egypt Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 30, "key"),
    "Key for Library Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 31, "key"),
    "Key for Tiki Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 32, "key"),
    "Key for UFO Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 33, "key"),
    "Key for Torture Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 34, "key"),
    "Key for Puzzle Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 35, "key"),
    "Key for Bedroom Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 36, "key"),
    "Key for Underground Lake Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 37, "key"),

    #Abilities
    "Crawling": ItemData(SHIVERS_ITEM_ID_OFFSET + 50, "ability"),

    #Event Items
    "Victory": ItemData(SHIVERS_ITEM_ID_OFFSET + 60, "victory"),

    #Duplicate pot pieces for fill_Restrictive
    "Water Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 70, "potduplicate"),
    "Wax Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 71, "potduplicate"),
    "Ash Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 72, "potduplicate"),
    "Oil Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 73, "potduplicate"),
    "Cloth Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 74, "potduplicate"),
    "Wood Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 75, "potduplicate"),
    "Crystal Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 76, "potduplicate"),
    "Lightning Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 77, "potduplicate"),
    "Sand Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 78, "potduplicate"),
    "Metal Pot Bottom DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 79, "potduplicate"),
    "Water Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 80, "potduplicate"),
    "Wax Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 81, "potduplicate"),
    "Ash Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 82, "potduplicate"),
    "Oil Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 83, "potduplicate"),
    "Cloth Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 84, "potduplicate"),
    "Wood Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 85, "potduplicate"),
    "Crystal Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 86, "potduplicate"),
    "Lightning Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 87, "potduplicate"),
    "Sand Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 88, "potduplicate"),
    "Metal Pot Top DUPE": ItemData(SHIVERS_ITEM_ID_OFFSET + 89, "potduplicate"),

    #Filler
    "Empty": ItemData(SHIVERS_ITEM_ID_OFFSET + 90, "filler"),
    "Filler Item": ItemData(SHIVERS_ITEM_ID_OFFSET + 91, "filler")

}

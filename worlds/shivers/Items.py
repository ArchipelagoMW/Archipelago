import enum
from typing import NamedTuple, Optional

from BaseClasses import Item, ItemClassification
from . import Constants


class ShiversItem(Item):
    game: str = "Shivers"


class ItemType(enum.Enum):
    POT = "pot"
    POT_COMPLETE = "pot-complete"
    POT_DUPLICATE = "pot-duplicate"
    POT_COMPLETE_DUPLICATE = "pot-complete-duplicate"
    KEY = "key"
    KEY_OPTIONAL = "key-optional"
    ABILITY = "ability"
    FILLER = "filler"
    IXUPI_AVAILABILITY = "ixupi-availability"
    GOAL = "goal"


class ItemData(NamedTuple):
    code: Optional[int]
    type: ItemType
    classification: ItemClassification = ItemClassification.progression


SHIVERS_ITEM_ID_OFFSET = 27000

# To allow for an item with a name that changes over time (once a year)
# while keeping the id unique we can generate a small range of them.
goal_items = {
    f"Mt. Pleasant Tribune: {Constants.years_since_sep_30_1980 + year_offset} year Old Mystery Solved!": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 100 + Constants.years_since_sep_30_1980 + year_offset, ItemType.GOAL
    ) for year_offset in range(-1, 2)
}

item_table = {
    # Pot Pieces
    "Water Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 0, ItemType.POT),
    "Wax Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 1, ItemType.POT),
    "Ash Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 2, ItemType.POT),
    "Oil Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 3, ItemType.POT),
    "Cloth Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 4, ItemType.POT),
    "Wood Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 5, ItemType.POT),
    "Crystal Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 6, ItemType.POT),
    "Lightning Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 7, ItemType.POT),
    "Sand Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 8, ItemType.POT),
    "Metal Pot Bottom": ItemData(SHIVERS_ITEM_ID_OFFSET + 9, ItemType.POT),
    "Water Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 10, ItemType.POT),
    "Wax Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 11, ItemType.POT),
    "Ash Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 12, ItemType.POT),
    "Oil Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 13, ItemType.POT),
    "Cloth Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 14, ItemType.POT),
    "Wood Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 15, ItemType.POT),
    "Crystal Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 16, ItemType.POT),
    "Lightning Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 17, ItemType.POT),
    "Sand Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 18, ItemType.POT),
    "Metal Pot Top": ItemData(SHIVERS_ITEM_ID_OFFSET + 19, ItemType.POT),
    "Water Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 20, ItemType.POT_COMPLETE),
    "Wax Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 21, ItemType.POT_COMPLETE),
    "Ash Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 22, ItemType.POT_COMPLETE),
    "Oil Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 23, ItemType.POT_COMPLETE),
    "Cloth Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 24, ItemType.POT_COMPLETE),
    "Wood Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 25, ItemType.POT_COMPLETE),
    "Crystal Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 26, ItemType.POT_COMPLETE),
    "Lightning Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 27, ItemType.POT_COMPLETE),
    "Sand Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 28, ItemType.POT_COMPLETE),
    "Metal Pot Complete": ItemData(SHIVERS_ITEM_ID_OFFSET + 29, ItemType.POT_COMPLETE),

    # Keys
    "Key for Office Elevator": ItemData(SHIVERS_ITEM_ID_OFFSET + 30, ItemType.KEY),
    "Key for Bedroom Elevator": ItemData(SHIVERS_ITEM_ID_OFFSET + 31, ItemType.KEY),
    "Key for Three Floor Elevator": ItemData(SHIVERS_ITEM_ID_OFFSET + 32, ItemType.KEY),
    "Key for Workshop": ItemData(SHIVERS_ITEM_ID_OFFSET + 33, ItemType.KEY),
    "Key for Office": ItemData(SHIVERS_ITEM_ID_OFFSET + 34, ItemType.KEY),
    "Key for Prehistoric Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 35, ItemType.KEY),
    "Key for Greenhouse": ItemData(SHIVERS_ITEM_ID_OFFSET + 36, ItemType.KEY),
    "Key for Ocean Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 37, ItemType.KEY),
    "Key for Projector Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 38, ItemType.KEY),
    "Key for Generator Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 39, ItemType.KEY),
    "Key for Egypt Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 40, ItemType.KEY),
    "Key for Library": ItemData(SHIVERS_ITEM_ID_OFFSET + 41, ItemType.KEY),
    "Key for Shaman Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 42, ItemType.KEY),
    "Key for UFO Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 43, ItemType.KEY),
    "Key for Torture Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 44, ItemType.KEY),
    "Key for Puzzle Room": ItemData(SHIVERS_ITEM_ID_OFFSET + 45, ItemType.KEY),
    "Key for Bedroom": ItemData(SHIVERS_ITEM_ID_OFFSET + 46, ItemType.KEY),
    "Key for Underground Lake": ItemData(SHIVERS_ITEM_ID_OFFSET + 47, ItemType.KEY),
    "Key for Janitor Closet": ItemData(SHIVERS_ITEM_ID_OFFSET + 48, ItemType.KEY),
    "Key for Front Door": ItemData(SHIVERS_ITEM_ID_OFFSET + 49, ItemType.KEY_OPTIONAL),

    # Abilities
    "Crawling": ItemData(SHIVERS_ITEM_ID_OFFSET + 50, ItemType.ABILITY),

    # Duplicate pot pieces for fill_Restrictive
    "Water Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Wax Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Ash Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Oil Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Cloth Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Wood Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Crystal Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Lightning Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Sand Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Metal Pot Bottom DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Water Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Wax Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Ash Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Oil Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Cloth Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Wood Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Crystal Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Lightning Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Sand Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Metal Pot Top DUPE": ItemData(None, ItemType.POT_DUPLICATE),
    "Water Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Wax Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Ash Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Oil Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Cloth Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Wood Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Crystal Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Lightning Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Sand Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),
    "Metal Pot Complete DUPE": ItemData(None, ItemType.POT_COMPLETE_DUPLICATE),

    # Filler
    "Empty": ItemData(None, ItemType.FILLER, ItemClassification.filler),
    "Easier Lyre": ItemData(SHIVERS_ITEM_ID_OFFSET + 91, ItemType.FILLER, ItemClassification.useful),
    "Water Always Available in Lobby": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 92, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Wax Always Available in Library": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 93, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Wax Always Available in Anansi Room": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 94, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Wax Always Available in Shaman Room": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 95, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Ash Always Available in Office": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 96, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Ash Always Available in Burial Room": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 97, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Oil Always Available in Prehistoric Room": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 98, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Cloth Always Available in Egypt": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 99, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Cloth Always Available in Burial Room": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 100, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Wood Always Available in Workshop": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 101, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Wood Always Available in Blue Maze": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 102, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Wood Always Available in Pegasus Room": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 103, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Wood Always Available in Gods Room": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 104, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Crystal Always Available in Lobby": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 105, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Crystal Always Available in Ocean": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 106, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Sand Always Available in Greenhouse": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 107, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Sand Always Available in Ocean": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 108, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Metal Always Available in Projector Room": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 109, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Metal Always Available in Bedroom": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 110, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Metal Always Available in Prehistoric": ItemData(
        SHIVERS_ITEM_ID_OFFSET + 111, ItemType.IXUPI_AVAILABILITY, ItemClassification.filler
    ),
    "Heal": ItemData(SHIVERS_ITEM_ID_OFFSET + 112, ItemType.FILLER, ItemClassification.filler),

    # Goal items
    **goal_items
}

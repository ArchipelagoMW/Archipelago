import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class YachtDiceItem(Item):
    game: str = "Yacht Dice"


# the starting index is chosen semi-randomly to be 16871244000


item_table = {
    "Dice": ItemData(16871244000, ItemClassification.progression | ItemClassification.useful),
    "Dice Fragment": ItemData(16871244001, ItemClassification.progression),
    "Roll": ItemData(16871244002, ItemClassification.progression),
    "Roll Fragment": ItemData(16871244003, ItemClassification.progression),
    "Fixed Score Multiplier": ItemData(16871244005, ItemClassification.progression),
    "Step Score Multiplier": ItemData(16871244006, ItemClassification.progression),
    "Category Ones": ItemData(16871244103, ItemClassification.progression),
    "Category Twos": ItemData(16871244104, ItemClassification.progression),
    "Category Threes": ItemData(16871244105, ItemClassification.progression),
    "Category Fours": ItemData(16871244106, ItemClassification.progression),
    "Category Fives": ItemData(16871244107, ItemClassification.progression),
    "Category Sixes": ItemData(16871244108, ItemClassification.progression),
    "Category Choice": ItemData(16871244109, ItemClassification.progression),
    "Category Inverse Choice": ItemData(16871244110, ItemClassification.progression),
    "Category Pair": ItemData(16871244111, ItemClassification.progression),
    "Category Three of a Kind": ItemData(16871244112, ItemClassification.progression),
    "Category Four of a Kind": ItemData(16871244113, ItemClassification.progression),
    "Category Tiny Straight": ItemData(16871244114, ItemClassification.progression),
    "Category Small Straight": ItemData(16871244115, ItemClassification.progression),
    "Category Large Straight": ItemData(16871244116, ItemClassification.progression),
    "Category Full House": ItemData(16871244117, ItemClassification.progression),
    "Category Yacht": ItemData(16871244118, ItemClassification.progression),
    "Category Distincts": ItemData(16871244123, ItemClassification.progression),
    "Category Two times Ones": ItemData(16871244124, ItemClassification.progression),
    "Category Half of Sixes": ItemData(16871244125, ItemClassification.progression),
    "Category Twos and Threes": ItemData(16871244126, ItemClassification.progression),
    "Category Sum of Odds": ItemData(16871244127, ItemClassification.progression),
    "Category Sum of Evens": ItemData(16871244128, ItemClassification.progression),
    "Category Double Threes and Fours": ItemData(16871244129, ItemClassification.progression),
    "Category Quadruple Ones and Twos": ItemData(16871244130, ItemClassification.progression),
    "Category Micro Straight": ItemData(16871244131, ItemClassification.progression),
    "Category Three Odds": ItemData(16871244132, ItemClassification.progression),
    "Category 1-2-1 Consecutive": ItemData(16871244133, ItemClassification.progression),
    "Category Three Distinct Dice": ItemData(16871244134, ItemClassification.progression),
    "Category Two Pair": ItemData(16871244135, ItemClassification.progression),
    "Category 2-1-2 Consecutive": ItemData(16871244136, ItemClassification.progression),
    "Category Five Distinct Dice": ItemData(16871244137, ItemClassification.progression),
    "Category 4&5 Full House": ItemData(16871244138, ItemClassification.progression),
    # filler items
    "Encouragement": ItemData(16871244200, ItemClassification.filler),
    "Fun Fact": ItemData(16871244201, ItemClassification.filler),
    "Story Chapter": ItemData(16871244202, ItemClassification.filler),
    "Good RNG": ItemData(16871244203, ItemClassification.filler),
    "Bad RNG": ItemData(16871244204, ItemClassification.trap),
    "Bonus Point": ItemData(16871244205, ItemClassification.useful),  # not included in logic
    # These points are included in the logic and might be necessary to progress.
    "1 Point": ItemData(16871244301, ItemClassification.progression_skip_balancing),
    "10 Points": ItemData(16871244302, ItemClassification.progression),
    "100 Points": ItemData(16871244303, ItemClassification.progression | ItemClassification.useful),
}

# item groups for better hinting
item_groups = {
    "Score Multiplier": {
        "Step Score Multiplier", 
        "Fixed Score Multiplier"
    },
    "Categories": {
        "Category Ones",
        "Category Twos",
        "Category Threes",
        "Category Fours",
        "Category Fives",
        "Category Sixes",
        "Category Choice",
        "Category Inverse Choice",
        "Category Pair",
        "Category Three of a Kind",
        "Category Four of a Kind",
        "Category Tiny Straight",
        "Category Small Straight",
        "Category Large Straight",
        "Category Full House",
        "Category Yacht",
        "Category Distincts",
        "Category Two times Ones",
        "Category Half of Sixes",
        "Category Twos and Threes",
        "Category Sum of Odds",
        "Category Sum of Evens",
        "Category Double Threes and Fours",
        "Category Quadruple Ones and Twos",
        "Category Micro Straight",
        "Category Three Odds",
        "Category 1-2-1 Consecutive",
        "Category Three Distinct Dice",
        "Category Two Pair",
        "Category 2-1-2 Consecutive",
        "Category Five Distinct Dice",
        "Category 4&5 Full House",
    },
    "Points": {
        "100 Points", 
        "10 Points", 
        "1 Point", 
        "Bonus Point"
    },
}

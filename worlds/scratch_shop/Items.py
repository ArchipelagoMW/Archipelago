from BaseClasses import Item, ItemClassification

class TemplateItem(Item):
    game: str = "Scratch Shop"

# Update your item dictionary to use the actual Enum classes instead of strings
item_data = {
    "Red Coin": (50001, ItemClassification.progression),
    "Blue Coin": (50002, ItemClassification.progression),
    "Orange Coin": (50003, ItemClassification.progression),
    "Yellow Coin": (50004, ItemClassification.progression),
    "Maroon Coin": (50005, ItemClassification.progression),
    "Purple Coin": (50006, ItemClassification.progression),
    "Green Coin": (50007, ItemClassification.progression),
    "Lime Coin": (50008, ItemClassification.progression),
    "Teal Coin": (50009, ItemClassification.progression),
    "Gold Coin": (50010, ItemClassification.progression),
    "Silver Coin": (50011, ItemClassification.progression),
    "Bronze Coin": (50012, ItemClassification.progression),
    "Iron Coin": (50013, ItemClassification.progression),
    "Copper Coin": (50014, ItemClassification.progression),
    "Indigo Coin": (50015, ItemClassification.progression),
    "Regular Coin": (50016, ItemClassification.progression),
    "Cat Coin": (50017, ItemClassification.progression),
    "Dog Coin": (50018, ItemClassification.progression),
    "Invisible Coin": (50019, ItemClassification.progression),
    "Rizz": (50020, ItemClassification.filler),
}
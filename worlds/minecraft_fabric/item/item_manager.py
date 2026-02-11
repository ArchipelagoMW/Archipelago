from dataclasses import dataclass
from BaseClasses import ItemClassification

@dataclass
class UnprocessedMinecraftItem:
    name: str
    classification: ItemClassification
    fill_type: int

@dataclass
class ProcessedMinecraftItem:
    name: str
    classification: ItemClassification
    fill_type: int
    item_id: int

def needed(name: str):
    return UnprocessedMinecraftItem(name, ItemClassification.progression, 0)

def needed_bl(name: str):
    return UnprocessedMinecraftItem(name, ItemClassification.progression, 1)

def useful(name: str):
    return UnprocessedMinecraftItem(name, ItemClassification.useful, 0)

def filler(name: str):
    return UnprocessedMinecraftItem(name, ItemClassification.filler, 0)

def blank_filler(name: str):
    return UnprocessedMinecraftItem(name, ItemClassification.filler, 2)

def trap(name: str):
    return UnprocessedMinecraftItem(name, ItemClassification.trap, 0)

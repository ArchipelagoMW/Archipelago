from enum import IntFlag
from dataclasses import dataclass
from BaseClasses import ItemClassification


class ItemGroups(IntFlag):
    Parts = 1 << 1
    Equipment = 1 << 2
    Ammo = 1 << 3
    Recipe = 1 << 4
    Building = 1 << 5
    Trap = 1 << 6
    Lights = 1 << 7
    Foundations = 1 << 8
    Transport = 1 << 9
    Trains = 1 << 10
    ConveyorMk1 = 1 << 11
    ConveyorMk2 = 1 << 12
    ConveyorMk3 = 1 << 13
    ConveyorMk4 = 1 << 14
    ConveyorMk5 = 1 << 15
    ConveyorSupports = 1 << 16
    PipesMk1 = 1 << 17
    PipesMk2 = 1 << 18
    PipelineSupports = 1 << 19
    HyperTubes = 1 << 20
    Signs = 1 << 21
    Pilars = 1 << 22
    Beams = 1 << 23
    Walls = 1 << 24
    Upgrades = 1 << 25
    Vehicles = 1 << 26
    Customizer = 1 << 27
    ConveyorMk6 = 1 << 28
    NeverExclude = 1 << 29


@dataclass
class ItemData:
    """Represents an item in the pool, it could be a resource bundle, production recipe, trap, etc."""
    category: ItemGroups
    code: int
    type: ItemClassification = ItemClassification.filler
    count: int = 1
    """How many of this item exists in the pool. 0 means none, but still defines the item so it can be added in the 
    starting inventory for example"""

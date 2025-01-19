from enum import Enum
from typing import NamedTuple, Set
from BaseClasses import ItemClassification

class ItemGroups(str, Enum):
    Parts = 1
    Equipment = 2
    Ammo = 3
    Recipe = 4
    Building = 5
    Trap = 6
    Lights = 7
    Foundations = 8
    Transport = 9
    Trains = 10
    ConveyorMk1 = 11
    ConveyorMk2 = 12
    ConveyorMk3 = 13
    ConveyorMk4 = 14
    ConveyorMk5 = 15
    ConveyorSupports = 16
    PipesMk1 = 17
    PipesMk2 = 18
    PipelineSupports = 19
    HyperTubes = 20
    Signs = 21
    Pilars = 22
    Beams = 23
    Walls = 24
    Upgrades = 25
    Vehicles = 26
    Customizer = 27
    ConveyorMk6 = 28

class ItemData(NamedTuple):
    """Represents an item in the pool, it could be a resource bundle, production recipe, trap, etc."""
    category: Set[ItemGroups]
    code: int
    type: ItemClassification = ItemClassification.filler
    count: int = 1
    """How many of this item exists in the pool. 0 means none, but still defines the item so it can be added in the starting inventory for example"""

from dataclasses import dataclass
from typing import Literal


Block = tuple[int, int, int]
""" (tile, type, bts) """

BlockKey = Literal[
    "Screw",
    "Ice",
    "Hyper",
    "Spazer",
    "Plasma",
    "Grapple",
    "Speed",
    "PB",
    "Super"
]


@dataclass
class DaphneBlocks:
    one: BlockKey
    two: BlockKey

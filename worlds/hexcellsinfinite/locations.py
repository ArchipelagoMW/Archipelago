from typing import TYPE_CHECKING
from .types import LocData

if TYPE_CHECKING:
    from . import HexcellsInfiniteWorld

def get_total_locations(world: "HexcellsInfiniteWorld") -> int:
    return sum(1 for _ in location_table)

def get_location_names() -> dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items()}
    return names

location_table: dict[str, LocData] = {}

for worldNum in range(1, 7):
    for levelNum in range(1, 7):
        name = f"Hexcells {worldNum}-{levelNum}"
        location_table[name] = LocData(len(location_table)+1, f"Level Group {worldNum}")

for worldNum in range(1, 7):
    for levelNum in range(1, 7):
        name = f"Hexcells Level {worldNum}-{levelNum}"
        location_table[name] = LocData(len(location_table)+1, f"{name}")

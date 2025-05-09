from typing import NamedTuple, Dict

from BaseClasses import Location


class PaintLocation(Location):
    game = "Paint"


class PaintLocationData(NamedTuple):
    region: str
    address: int


location_data_table: Dict[str, PaintLocationData] = {
    # f"Similarity: {i}%": PaintLocationData("Canvas", 198500 + i) for i in range(1, 96)
    f"Similarity: {i/4}%": PaintLocationData("Canvas", 198600 + i) for i in range(1, 381)
}

location_table = {name: data.address for name, data in location_data_table.items()}

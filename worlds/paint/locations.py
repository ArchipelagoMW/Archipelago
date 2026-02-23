from typing import NamedTuple, Dict, Optional

from BaseClasses import CollectionState, Location, Region

from .rules import paint_percent_available


class PaintLocation(Location):
    game = "Paint"

    required_percent: float

    def __init__(self, player: int, name: str = '', address: Optional[int] = None, parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        assert self.address is not None
        self.required_percent = (self.address % 198600) / 4

    def access_rule(self, state: CollectionState):
        return paint_percent_available(state, state.multiworld.worlds[self.player], self.player) >=\
               self.required_percent


class PaintLocationData(NamedTuple):
    region: str
    address: int


location_data_table: Dict[str, PaintLocationData] = {
    # f"Similarity: {i}%": PaintLocationData("Canvas", 198500 + i) for i in range(1, 96)
    f"Similarity: {i/4}%": PaintLocationData("Canvas", 198600 + i) for i in range(1, 381)
}

location_table = {name: data.address for name, data in location_data_table.items()}

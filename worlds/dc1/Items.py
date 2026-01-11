import json
import pkgutil

from BaseClasses import Item, ItemClassification
from worlds.dc1.game_id import dc1_name

prog_map = json.loads(pkgutil.get_data(__name__, "data/progressive.json").decode())

progressive_item_list = {}
for prog_item in prog_map:
    progressiveName = prog_map[prog_item]
    if progressiveName not in progressive_item_list:
        progressive_item_list[progressiveName] = []
    progressive_item_list[progressiveName].append(prog_item)

class DarkCloudItem(Item):
    # type = None
    game: str = dc1_name

    def __init__(self, name: str,
                 classification: ItemClassification,
                 code: int | None,
                 player: int):
        super().__init__(name, classification, code, player)
        self.game = dc1_name

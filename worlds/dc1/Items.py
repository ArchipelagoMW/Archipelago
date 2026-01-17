import json
import pkgutil
import re

from BaseClasses import Item, ItemClassification
from .game_id import dc1_name

prog_map = json.loads(pkgutil.get_data(__name__, "data/progressive.json").decode())

progressive_item_list = {}
for prog_item in prog_map:
    progressiveName = prog_map[prog_item]
    if progressiveName not in progressive_item_list:
        progressive_item_list[progressiveName] = []
    progressive_item_list[progressiveName].append(prog_item)

class DarkCloudItem(Item):
    game = dc1_name

class ItemData:
    classification = ItemClassification.trap # Should never see a Trap currently
    name = None
    ap_id = 0
    count = 0

    def __init__(self, name: str, ap_id: int, classification: ItemClassification, counts):
        self.name = name
        self.ap_id = ap_id
        self.counts = counts
        self.classification = classification

    def to_items(self, player: int, world) -> list[DarkCloudItem]:
        items = []

        for j in range(0, min(5, world.options.boss_goal)):
            # Randomize the +x value for attack, speed, endurance, magic attachments on the server
            if 971112000 < self.ap_id <= 971112033:
                for i in range(self.counts[j]):
                    temp_ap_id = self.ap_id
                    rand = world.random.randint(0, 2)
                    temp_ap_id = temp_ap_id + rand
                    temp_name = re.search('(.*\\+)', self.name).group(0) + str(rand+1)
                    items.append(DarkCloudItem(temp_name, self.classification, temp_ap_id, player))
            else:
                for i in range(self.counts[j]):
                    items.append(DarkCloudItem(self.name, self.classification, self.ap_id, player))

        return items

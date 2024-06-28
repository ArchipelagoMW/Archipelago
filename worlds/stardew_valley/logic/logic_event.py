from dataclasses import dataclass

from ..strings.ap_names import event_names
from ..strings.metal_names import MetalBar, Ore
from ..strings.region_names import Region

all_events = event_names.all_events.copy()
all_logic_events = list()


@dataclass(frozen=True)
class LogicEvent:
    name: str
    region: str


@dataclass(frozen=True)
class LogicItemEvent(LogicEvent):
    item: str

    def __init__(self, item: str, region: str):
        super().__init__(f"{item} (Logic event)", region)
        super().__setattr__("item", item)


def register_item_event(item: str, region: str = Region.farm):
    event = LogicItemEvent(item, region)
    all_logic_events.append(event)
    all_events.add(event.name)


for i in (MetalBar.copper, MetalBar.iron, MetalBar.gold, MetalBar.iridium, Ore.copper, Ore.iron, Ore.gold, Ore.iridium):
    register_item_event(i)

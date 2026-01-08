import typing as t
from collections import defaultdict

from BaseClasses import Item

from .item_data import item_data
from .constants import AVItemType


class AVItem(Item):
    game = "Axiom Verge"


item_groups = defaultdict(set)
for group_name in AVItemType:
    item_groups[group_name.value] = {item.name for item in item_data.values() if item.group_name == group_name}
item_groups["Drill"] |= {"Remote Drone"}
item_groups["Health"] = item_groups[AVItemType.HEALTH_NODE] | item_groups[AVItemType.HEALTH_NODE_FRAGMENT]
item_groups["Power"] = item_groups[AVItemType.POWER_NODE] | item_groups[AVItemType.POWER_NODE_FRAGMENT]
item_groups["Powerups"] = item_groups["Health"] | item_groups["Power"]
item_groups["Movement + Coat"] = item_groups[AVItemType.MOVEMENT] | item_groups[AVItemType.COAT]
item_groups["Abilities"] = item_groups["Movement + Coat"] | item_groups[AVItemType.DRONE] | item_groups[AVItemType.DRILL] | item_groups[AVItemType.GLITCH] | item_groups[AVItemType.KEY] | item_groups[AVItemType.TENDRILS]

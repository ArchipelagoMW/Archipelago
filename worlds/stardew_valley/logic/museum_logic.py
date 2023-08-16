from typing import List

from .action_logic import ActionLogic
from .has_logic import HasLogic
from .. import options
from ..data.museum_data import MuseumItem, all_museum_items, all_museum_artifacts, all_museum_minerals
from ..stardew_rule import StardewRule, And, False_, Count
from .received_logic import ReceivedLogic
from .region_logic import RegionLogic
from ..strings.region_names import Region


class MuseumLogic:
    player: int
    museum_option: int
    received = ReceivedLogic
    has: HasLogic
    region: RegionLogic
    action: ActionLogic

    def __init__(self, player: int, museum_option: int, received: ReceivedLogic, has: HasLogic, region: RegionLogic, action: ActionLogic):
        self.player = player
        self.museum_option = museum_option
        self.received = received
        self.has = has
        self.region = region
        self.action = action

    def can_donate_museum_item(self, item: MuseumItem) -> StardewRule:
        return self.region.can_reach(Region.museum) & self.can_find_museum_item(item)

    def can_donate_museum_items(self, number: int) -> StardewRule:
        return self.region.can_reach(Region.museum) & self.can_find_museum_items(number)

    def can_donate_museum_artifacts(self, number: int) -> StardewRule:
        return self.region.can_reach(Region.museum) & self.can_find_museum_artifacts(number)

    def can_donate_museum_minerals(self, number: int) -> StardewRule:
        return self.region.can_reach(Region.museum) & self.can_find_museum_minerals(number)

    def can_find_museum_item(self, item: MuseumItem) -> StardewRule:
        region_rule = self.region.can_reach_all_except_one(item.locations)
        geodes_rule = And([self.action.can_open_geode(geode) for geode in item.geodes])
        # monster_rule = self.can_farm_monster(item.monsters)
        # extra_rule = True_()
        pan_rule = False_()
        if item.name == "Earth Crystal" or item.name == "Fire Quartz" or item.name == "Frozen Tear":
            pan_rule = self.action.can_do_panning()
        return pan_rule | (region_rule & geodes_rule)  # & monster_rule & extra_rule

    def can_find_museum_artifacts(self, number: int) -> StardewRule:
        rules = []
        for artifact in all_museum_artifacts:
            rules.append(self.can_find_museum_item(artifact))

        return Count(number, rules)

    def can_find_museum_minerals(self, number: int) -> StardewRule:
        rules = []
        for mineral in all_museum_minerals:
            rules.append(self.can_find_museum_item(mineral))

        return Count(number, rules)

    def can_find_museum_items(self, number: int) -> StardewRule:
        rules = []
        for donation in all_museum_items:
            rules.append(self.can_find_museum_item(donation))

        return Count(number, rules)

    def can_complete_museum(self) -> StardewRule:
        rules = [self.region.can_reach(Region.museum)]

        if self.museum_option != options.Museumsanity.option_none:
            rules.append(self.received("Traveling Merchant Metal Detector", 4))

        for donation in all_museum_items:
            rules.append(self.can_find_museum_item(donation))
        return And(rules) & self.region.can_reach(Region.museum)

    def can_donate(self, item: str) -> StardewRule:
        return self.has(item) & self.region.can_reach(Region.museum)

    def can_donate_many(self, items: List[str], amount: int = -1) -> StardewRule:
        if amount <= -1:
            amount = len(items)
        return self.has(items, amount) & self.region.can_reach(Region.museum)

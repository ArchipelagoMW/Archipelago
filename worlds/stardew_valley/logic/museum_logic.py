from typing import Union

from Utils import cache_self1
from .action_logic import ActionLogicMixin
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .. import options
from ..data.museum_data import MuseumItem, all_museum_items, all_museum_artifacts, all_museum_minerals
from ..stardew_rule import StardewRule, And, False_
from ..strings.region_names import Region


class MuseumLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.museum = MuseumLogic(*args, **kwargs)


class MuseumLogic(BaseLogic[Union[ReceivedLogicMixin, HasLogicMixin, RegionLogicMixin, ActionLogicMixin, MuseumLogicMixin]]):

    def can_donate_museum_items(self, number: int) -> StardewRule:
        return self.logic.region.can_reach(Region.museum) & self.logic.museum.can_find_museum_items(number)

    def can_donate_museum_artifacts(self, number: int) -> StardewRule:
        return self.logic.region.can_reach(Region.museum) & self.logic.museum.can_find_museum_artifacts(number)

    @cache_self1
    def can_find_museum_item(self, item: MuseumItem) -> StardewRule:
        if item.locations:
            region_rule = self.logic.region.can_reach_all_except_one(item.locations)
        else:
            region_rule = False_()
        if item.geodes:
            geodes_rule = And(*(self.logic.action.can_open_geode(geode) for geode in item.geodes))
        else:
            geodes_rule = False_()
        # monster_rule = self.can_farm_monster(item.monsters)
        # extra_rule = True_()
        pan_rule = False_()
        if item.item_name == "Earth Crystal" or item.item_name == "Fire Quartz" or item.item_name == "Frozen Tear":
            pan_rule = self.logic.action.can_pan()
        return pan_rule | region_rule | geodes_rule  # & monster_rule & extra_rule

    def can_find_museum_artifacts(self, number: int) -> StardewRule:
        rules = []
        for artifact in all_museum_artifacts:
            rules.append(self.logic.museum.can_find_museum_item(artifact))

        return self.logic.count(number, *rules)

    def can_find_museum_minerals(self, number: int) -> StardewRule:
        rules = []
        for mineral in all_museum_minerals:
            rules.append(self.logic.museum.can_find_museum_item(mineral))

        return self.logic.count(number, *rules)

    def can_find_museum_items(self, number: int) -> StardewRule:
        rules = []
        for donation in all_museum_items:
            rules.append(self.logic.museum.can_find_museum_item(donation))

        return self.logic.count(number, *rules)

    def can_complete_museum(self) -> StardewRule:
        rules = [self.logic.region.can_reach(Region.museum)]

        if self.options.museumsanity == options.Museumsanity.option_none:
            rules.append(self.logic.received("Traveling Merchant Metal Detector", 2))
        else:
            rules.append(self.logic.received("Traveling Merchant Metal Detector", 3))

        for donation in all_museum_items:
            rules.append(self.logic.museum.can_find_museum_item(donation))
        return And(*rules) & self.logic.region.can_reach(Region.museum)

    def can_donate(self, item: str) -> StardewRule:
        return self.logic.has(item) & self.logic.region.can_reach(Region.museum)

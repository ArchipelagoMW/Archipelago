from functools import cached_property
from typing import Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from ..stardew_rule import StardewRule, true_
from ..strings.building_names import Building
from ..strings.region_names import Region

has_group = "building"


class BuildingLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.building = BuildingLogic(*args, **kwargs)


class BuildingLogic(BaseLogic[Union[BuildingLogicMixin, MoneyLogicMixin, RegionLogicMixin, ReceivedLogicMixin, HasLogicMixin, 'SourceLogicMixin']]):

    @cache_self1
    def can_build(self, building: str) -> StardewRule:
        building = self.content.farm_buildings.get(building)
        assert building is not None, f"Building {building} not found."

        source_rule = self.logic.source.has_access_to_any(building.sources)
        if not building.is_upgrade:
            return source_rule

        upgrade_rule = self.logic.building.has_building(building.upgrade_from)
        return self.logic.and_(upgrade_rule, source_rule)

    @cache_self1
    def has_building(self, building: str) -> StardewRule:
        building_progression = self.content.features.building_progression

        if building in building_progression.starting_buildings:
            return true_

        if not building_progression.is_progressive:
            return self.logic.building.can_build(building)

        # Shipping bin is special. The mod auto-builds it when received, no need to go to Robin.
        if building == Building.shipping_bin:
            return self.logic.received(Building.shipping_bin)

        carpenter_rule = self.logic.building.can_construct_buildings
        item, count = building_progression.to_progressive_item(building)
        return self.logic.received(item, count) & carpenter_rule

    @cached_property
    def can_construct_buildings(self) -> StardewRule:
        return self.logic.region.can_reach(Region.carpenter)

from typing import Union, Iterable

from Utils import cache_self1
from .base_logic import BaseLogicMixin, BaseLogic
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .region_logic import RegionLogicMixin
from .season_logic import SeasonLogicMixin
from ..options import ExcludeGingerIsland
from ..stardew_rule import StardewRule, False_, false_
from ..strings.region_names import Region


class CropLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crop = CropLogic(*args, **kwargs)


class CropLogic(BaseLogic[Union[HasLogicMixin, ReceivedLogicMixin, RegionLogicMixin, SeasonLogicMixin, CropLogicMixin]]):

    @cache_self1
    def can_plant_and_grow_item(self, seasons: Union[str, Iterable[str]]) -> StardewRule:
        # TODO this should be an event in a "season+farming" region.
        #  There would be an entrance without condition in greenhouse + island_farm + farm given you have season
        if isinstance(seasons, str):
            seasons = [seasons]

        greenhouse_rule = self.logic.region.can_reach(Region.greenhouse)
        island_farm_rule = self.logic.crop.has_island_farm()

        if seasons:
            farm_with_right_season_rule = self.logic.season.has_any(seasons) & self.logic.region.can_reach(Region.farm)
        else:
            # Because no season means it can't be grown in the farm.
            # FIXME this should be handled by has_any
            farm_with_right_season_rule = false_

        return greenhouse_rule | island_farm_rule | farm_with_right_season_rule

    def has_island_farm(self) -> StardewRule:
        if self.options.exclude_ginger_island == ExcludeGingerIsland.option_false:
            return self.logic.region.can_reach(Region.island_west)
        return False_()

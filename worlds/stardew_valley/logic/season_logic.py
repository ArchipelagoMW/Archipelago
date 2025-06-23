from functools import cached_property
from typing import Iterable, Union

from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .received_logic import ReceivedLogicMixin
from .time_logic import TimeLogicMixin
from ..options import SeasonRandomization
from ..stardew_rule import StardewRule, True_, true_
from ..strings.generic_names import Generic
from ..strings.season_names import Season


class SeasonLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.season = SeasonLogic(*args, **kwargs)


class SeasonLogic(BaseLogic):

    @cached_property
    def has_spring(self) -> StardewRule:
        return self.logic.season.has(Season.spring)

    @cached_property
    def has_summer(self) -> StardewRule:
        return self.logic.season.has(Season.summer)

    @cached_property
    def has_fall(self) -> StardewRule:
        return self.logic.season.has(Season.fall)

    @cached_property
    def has_winter(self) -> StardewRule:
        return self.logic.season.has(Season.winter)

    @cache_self1
    def has(self, season: str) -> StardewRule:
        if season == Generic.any:
            return True_()
        seasons_order = [Season.spring, Season.summer, Season.fall, Season.winter]
        if self.options.season_randomization == SeasonRandomization.option_progressive:
            return self.logic.received(Season.progressive, seasons_order.index(season))
        if self.options.season_randomization == SeasonRandomization.option_disabled:
            if season == Season.spring:
                return True_()
            return self.logic.time.has_lived_months(1)
        return self.logic.received(season)

    def has_any(self, seasons: Iterable[str]):
        if seasons == Season.all:
            return true_
        if not seasons:
            # That should be false, but I'm scared.
            return True_()
        return self.logic.or_(*(self.logic.season.has(season) for season in seasons))

    def has_any_not_winter(self):
        return self.logic.season.has_any([Season.spring, Season.summer, Season.fall])

    def has_all(self):
        seasons = [Season.spring, Season.summer, Season.fall, Season.winter]
        return self.logic.and_(*(self.logic.season.has(season) for season in seasons))

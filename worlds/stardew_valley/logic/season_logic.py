from typing import Iterable

from .received_logic import ReceivedLogic
from .time_logic import TimeLogic
from ..options import SeasonRandomization
from ..stardew_rule import StardewRule, True_, And, Or
from ..strings.generic_names import Generic
from ..strings.season_names import Season


class SeasonLogic:
    player: int
    season_option: SeasonRandomization
    received: ReceivedLogic
    time: TimeLogic

    def __init__(self, player: int, season_option: SeasonRandomization, received_logic: ReceivedLogic, time: TimeLogic):
        self.player = player
        self.season_option = season_option
        self.received = received_logic
        self.time = time
        self.has_season_rules = {
            Generic.any: True_()
        }
        self.has_any_season_rules = {}
        self.has_all_season_rules = {}
        self.has_any_not_winter_rule = self.has_any([Season.spring, Season.summer, Season.fall])

    def has(self, season: str) -> StardewRule:
        if season in self.has_season_rules:
            return self.has_season_rules[season]
        seasons_order = [Season.spring, Season.summer, Season.fall, Season.winter]
        if self.season_option == SeasonRandomization.option_progressive:
            self.has_season_rules[season] = self.received(Season.progressive, seasons_order.index(season))
        elif self.season_option == SeasonRandomization.option_disabled:
            if season == Season.spring:
                self.has_season_rules[season] = True_()
            else:
                self.has_season_rules[season] = self.time.has_lived_months(1)
        else:
            self.has_season_rules[season] = self.received(season)
        return self.has_season_rules[season]

    def has_any(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        key = ",".join(seasons)
        if key not in self.has_any_season_rules:
            self.has_any_season_rules[key] = Or([self.has(season) for season in seasons])
        return self.has_any_season_rules[key]

    def has_any_not_winter(self):
        return self.has_any_not_winter_rule

    def has_all(self, seasons: Iterable[str]):
        if not seasons:
            return True_()
        key = ",".join(seasons)
        if key not in self.has_all_season_rules:
            self.has_all_season_rules[key] = And([self.has(season) for season in seasons])
        return self.has_all_season_rules[key]


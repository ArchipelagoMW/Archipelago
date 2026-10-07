from worlds.stardew_valley.strings.entrance_names import LogicEntrance
from worlds.stardew_valley.strings.region_names import LogicRegion
from worlds.stardew_valley.strings.season_names import Season


class FestivalData:
    name: str
    entrance: str
    season: str
    day: int
    duration: int

    def __init__(self, name: str, entrance: str, season: str, day: int, duration: int = 1):
        self.name = name
        self.entrance = entrance
        self.season = season
        self.duration = duration
        self.day = max(1, min(29-duration, day))


main_festival_data = [
    FestivalData(LogicRegion.egg_festival, LogicEntrance.attend_egg_festival, Season.spring, 13),
    FestivalData(LogicRegion.flower_dance, LogicEntrance.attend_flower_dance, Season.spring, 24),
    FestivalData(LogicRegion.luau, LogicEntrance.attend_luau, Season.summer, 11),
    FestivalData(LogicRegion.moonlight_jellies, LogicEntrance.attend_moonlight_jellies, Season.summer, 28),
    FestivalData(LogicRegion.fair, LogicEntrance.attend_fair, Season.fall, 16),
    FestivalData(LogicRegion.spirit_eve, LogicEntrance.attend_spirit_eve, Season.fall, 27),
    FestivalData(LogicRegion.festival_of_ice, LogicEntrance.attend_festival_of_ice, Season.winter, 8),
    FestivalData(LogicRegion.winter_star, LogicEntrance.attend_winter_star, Season.winter, 25),
]

mini_festival_data = [
    FestivalData(LogicRegion.night_market, LogicEntrance.attend_night_market, Season.winter, 15, 3),
    FestivalData(LogicRegion.desert_festival, LogicEntrance.attend_desert_festival, Season.spring, 15, 3),
    FestivalData(LogicRegion.trout_derby, LogicEntrance.attend_trout_derby, Season.summer, 20, 2),
    FestivalData(LogicRegion.squidfest, LogicEntrance.attend_squidfest, Season.winter, 12, 2),
]

all_festival_data = dict()
all_festival_data.update({festival.name: festival for festival in main_festival_data})
all_festival_data.update({festival.name: festival for festival in mini_festival_data})

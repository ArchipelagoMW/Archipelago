from enum import Enum, IntEnum
from typing import List


class Overcooked2Dlc(Enum):
    STORY = "Story"
    SEASONAL = "Seasonal"
    SURF_N_TURF = "Surf 'n' Turf"
    CAMPFIRE_COOK_OFF = "Campfire Cook Off"
    NIGHT_OF_THE_HANGRY_HORDE = "Night of the Hangry Horde"
    CARNIVAL_OF_CHAOS = "Carnival of Chaos"
    # CHRISTMAS = "Christmas"
    # CHINESE_NEW_YEAR = "Chinese New Year"
    # WINTER_WONDERLAND = "Winter Wonderland"
    # MOON_HARVEST = "Moon Harvest"
    # SPRING_FRESTIVAL = "Spring Festival"
    # SUNS_OUT_BUNS_OUT = "Sun's Out Buns Out"

    def __int__(self) -> int:
        if self == Overcooked2Dlc.STORY:
            return 0
        if self == Overcooked2Dlc.SURF_N_TURF:
            return 1
        if self == Overcooked2Dlc.CAMPFIRE_COOK_OFF:
            return 2
        if self == Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE:
            return 3
        if self == Overcooked2Dlc.CARNIVAL_OF_CHAOS:
            return 4
        if self == Overcooked2Dlc.SEASONAL:
            return 5
        assert False

    # inclusive
    @property
    def start_level_id(self) -> int:
        return 0

    # exclusive
    @property
    def end_level_id(self) -> int:
        id = None
        if self == Overcooked2Dlc.STORY:
            id = 1 + 6*6 + 8 # tutorial + world_count*level_count + kevin count
        if self == Overcooked2Dlc.SURF_N_TURF:
            id = 3*4 + 1
        if self == Overcooked2Dlc.CAMPFIRE_COOK_OFF:
            id = 3*4 + 3
        if self == Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE:
            id = 3*3 + 3 + 8
        if self == Overcooked2Dlc.CARNIVAL_OF_CHAOS:
            id = 3*4 + 3
        if self == Overcooked2Dlc.SEASONAL:
            id = 31 + 1

        return self.start_level_id + id

    # Tutorial + Horde Levels + Endgame
    def excluded_levels(self) -> List[int]:
        if self == Overcooked2Dlc.STORY:
            return [0, 36]

        return []

    def horde_levels(self) -> List[int]:
        if self == Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE:
            return [12, 13, 14, 15, 16, 17, 18, 19]
        if self == Overcooked2Dlc.SEASONAL:
            return [13, 15]

        return []

    def prep_levels(self) -> List[int]:
        if self == Overcooked2Dlc.STORY:
            return [1, 2, 5, 10, 12, 13, 28, 31]
        if self == Overcooked2Dlc.SURF_N_TURF:
            return [0, 4]
        if self == Overcooked2Dlc.CAMPFIRE_COOK_OFF:
            return [0, 2, 4, 9]
        if self == Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE:
            return [0, 1, 4]
        if self == Overcooked2Dlc.CARNIVAL_OF_CHAOS:
            return [0, 1, 3, 4, 5]
        if self == Overcooked2Dlc.SEASONAL:
            # moon 1-1 is a prep level for 1P only, but we can't make that assumption here
            return [0, 1, 5, 6, 12, 14, 16, 17, 18, 22, 23, 24, 27, 29]

        return []


class Overcooked2GameWorld(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    KEVIN = 7

    @property
    def as_str(self) -> str:
        if self == Overcooked2GameWorld.KEVIN:
            return "Kevin"

        return str(self.value)

    @property
    def sublevel_count(self) -> int:
        if self == Overcooked2GameWorld.KEVIN:
            return 8

        return 6

    @property
    def base_id(self) -> int:
        if self == Overcooked2GameWorld.ONE:
            return 1

        prev = Overcooked2GameWorld(self - 1)
        return prev.base_id + prev.sublevel_count

    @property
    def name(self) -> str:
        if self == Overcooked2GameWorld.KEVIN:
            return "Kevin"

        return "World " + self.as_str


class Overcooked2GenericLevel():
    dlc: Overcooked2Dlc
    level_id: int

    def __init__(self, level_id: int, dlc: Overcooked2Dlc = Overcooked2Dlc("Story")):
        self.dlc = dlc
        self.level_id = level_id

    def __str__(self) -> str:
        return f"{self.dlc.value}|{self.level_id}"

    def __repr__(self) -> str:
        return f"{self}"

    @property
    def shortname(self) -> str:
        return level_id_to_shortname[(self.dlc, self.level_id)]

    @property
    def is_horde(self) -> bool:
        return self.level_id in self.dlc.horde_levels()


class Overcooked2Level:
    """
    Abstraction for a playable levels in Overcooked 2. By default constructor
    it can be used as an iterator for all locations in the Story map.
    """
    world: Overcooked2GameWorld
    sublevel: int

    def __init__(self):
        self.world = Overcooked2GameWorld.ONE
        self.sublevel = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.sublevel += 1
        if self.sublevel > self.world.sublevel_count:
            if self.world == Overcooked2GameWorld.KEVIN:
                raise StopIteration
            self.world = Overcooked2GameWorld(self.world + 1)
            self.sublevel = 1

        return self

    @property
    def level_id(self) -> int:
        return self.world.base_id + (self.sublevel - 1)

    @property
    def level_name(self) -> str:
        return self.world.as_str + "-" + str(self.sublevel)

    @property
    def location_name_item(self) -> str:
        return self.level_name + " Completed"

    @property
    def location_name_level_complete(self) -> str:
        return self.level_name + " Level Completed"

    @property
    def event_name_level_complete(self) -> str:
        return self.level_name + " Level Complete"

    def location_name_star_event(self, stars: int) -> str:
        return "%s (%d-Star)" % (self.level_name, stars)

    @property
    def as_generic_level(self) -> Overcooked2GenericLevel:
        return Overcooked2GenericLevel(self.level_id)


# Note that there are valid levels beyond what is listed here, but they are all
# Onion King Dialogs
level_id_to_shortname = {
    (Overcooked2Dlc.STORY                     , 0  ): "Tutorial"      ,
    (Overcooked2Dlc.STORY                     , 1  ): "Story 1-1"     ,
    (Overcooked2Dlc.STORY                     , 2  ): "Story 1-2"     ,
    (Overcooked2Dlc.STORY                     , 3  ): "Story 1-3"     ,
    (Overcooked2Dlc.STORY                     , 4  ): "Story 1-4"     ,
    (Overcooked2Dlc.STORY                     , 5  ): "Story 1-5"     ,
    (Overcooked2Dlc.STORY                     , 6  ): "Story 1-6"     ,
    (Overcooked2Dlc.STORY                     , 7  ): "Story 2-1"     ,
    (Overcooked2Dlc.STORY                     , 8  ): "Story 2-2"     ,
    (Overcooked2Dlc.STORY                     , 9  ): "Story 2-3"     ,
    (Overcooked2Dlc.STORY                     , 10 ): "Story 2-4"     ,
    (Overcooked2Dlc.STORY                     , 11 ): "Story 2-5"     ,
    (Overcooked2Dlc.STORY                     , 12 ): "Story 2-6"     ,
    (Overcooked2Dlc.STORY                     , 13 ): "Story 3-1"     ,
    (Overcooked2Dlc.STORY                     , 14 ): "Story 3-2"     ,
    (Overcooked2Dlc.STORY                     , 15 ): "Story 3-3"     ,
    (Overcooked2Dlc.STORY                     , 16 ): "Story 3-4"     ,
    (Overcooked2Dlc.STORY                     , 17 ): "Story 3-5"     ,
    (Overcooked2Dlc.STORY                     , 18 ): "Story 3-6"     ,
    (Overcooked2Dlc.STORY                     , 19 ): "Story 4-1"     ,
    (Overcooked2Dlc.STORY                     , 20 ): "Story 4-2"     ,
    (Overcooked2Dlc.STORY                     , 21 ): "Story 4-3"     ,
    (Overcooked2Dlc.STORY                     , 22 ): "Story 4-4"     ,
    (Overcooked2Dlc.STORY                     , 23 ): "Story 4-5"     ,
    (Overcooked2Dlc.STORY                     , 24 ): "Story 4-6"     ,
    (Overcooked2Dlc.STORY                     , 25 ): "Story 5-1"     ,
    (Overcooked2Dlc.STORY                     , 26 ): "Story 5-2"     ,
    (Overcooked2Dlc.STORY                     , 27 ): "Story 5-3"     ,
    (Overcooked2Dlc.STORY                     , 28 ): "Story 5-4"     ,
    (Overcooked2Dlc.STORY                     , 29 ): "Story 5-5"     ,
    (Overcooked2Dlc.STORY                     , 30 ): "Story 5-6"     ,
    (Overcooked2Dlc.STORY                     , 31 ): "Story 6-1"     ,
    (Overcooked2Dlc.STORY                     , 32 ): "Story 6-2"     ,
    (Overcooked2Dlc.STORY                     , 33 ): "Story 6-3"     ,
    (Overcooked2Dlc.STORY                     , 34 ): "Story 6-4"     ,
    (Overcooked2Dlc.STORY                     , 35 ): "Story 6-5"     ,
    (Overcooked2Dlc.STORY                     , 36 ): "Story 6-6"     ,
    (Overcooked2Dlc.STORY                     , 37 ): "Story K-1"     ,
    (Overcooked2Dlc.STORY                     , 38 ): "Story K-2"     ,
    (Overcooked2Dlc.STORY                     , 39 ): "Story K-3"     ,
    (Overcooked2Dlc.STORY                     , 40 ): "Story K-4"     ,
    (Overcooked2Dlc.STORY                     , 41 ): "Story K-5"     ,
    (Overcooked2Dlc.STORY                     , 42 ): "Story K-6"     ,
    (Overcooked2Dlc.STORY                     , 43 ): "Story K-7"     ,
    (Overcooked2Dlc.STORY                     , 44 ): "Story K-8"     ,
    (Overcooked2Dlc.SURF_N_TURF               , 0  ): "Surf 1-1"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 1  ): "Surf 1-2"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 2  ): "Surf 1-3"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 3  ): "Surf 1-4"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 4  ): "Surf 2-1"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 5  ): "Surf 2-2"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 6  ): "Surf 2-3"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 7  ): "Surf 2-4"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 8  ): "Surf 3-1"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 9  ): "Surf 3-2"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 10 ): "Surf 3-3"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 11 ): "Surf 3-4"      ,
    (Overcooked2Dlc.SURF_N_TURF               , 12 ): "Surf K-1"      ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 0  ): "Campfire 1-1"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 1  ): "Campfire 1-2"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 2  ): "Campfire 1-3"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 3  ): "Campfire 1-4"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 4  ): "Campfire 2-1"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 5  ): "Campfire 2-2"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 6  ): "Campfire 2-3"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 7  ): "Campfire 2-4"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 8  ): "Campfire 3-1"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 9  ): "Campfire 3-2"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 10 ): "Campfire 3-3"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 11 ): "Campfire 3-4"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 12 ): "Campfire K-1"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 13 ): "Campfire K-2"  ,
    (Overcooked2Dlc.CAMPFIRE_COOK_OFF         , 14 ): "Campfire K-3"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 0  ): "Carnival 1-1"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 1  ): "Carnival 1-2"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 2  ): "Carnival 1-3"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 3  ): "Carnival 1-4"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 4  ): "Carnival 2-1"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 5  ): "Carnival 2-2"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 6  ): "Carnival 2-3"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 7  ): "Carnival 2-4"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 8  ): "Carnival 3-1"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 9  ): "Carnival 3-2"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 10 ): "Carnival 3-3"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 11 ): "Carnival 3-4"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 12 ): "Carnival K-1"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 13 ): "Carnival K-2"  ,
    (Overcooked2Dlc.CARNIVAL_OF_CHAOS         , 14 ): "Carnival K-3"  ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 0  ): "Horde 1-1"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 1  ): "Horde 1-2"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 2  ): "Horde 1-3"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 3  ): "Horde 2-1"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 4  ): "Horde 2-2"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 5  ): "Horde 2-3"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 6  ): "Horde 3-1"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 7  ): "Horde 3-2"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 8  ): "Horde 3-3"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 9  ): "Horde K-1"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 10 ): "Horde K-2"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 11 ): "Horde K-3"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 12 ): "Horde H-1"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 13 ): "Horde H-2"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 14 ): "Horde H-3"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 15 ): "Horde H-4"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 16 ): "Horde H-5"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 17 ): "Horde H-6"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 18 ): "Horde H-7"     ,
    (Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE , 19 ): "Horde H-8"     ,
    (Overcooked2Dlc.SEASONAL                  , 0  ): "Christmas 1-1" ,
    (Overcooked2Dlc.SEASONAL                  , 1  ): "Christmas 1-2" ,
    (Overcooked2Dlc.SEASONAL                  , 2  ): "Christmas 1-3" ,
    (Overcooked2Dlc.SEASONAL                  , 3  ): "Christmas 1-4" ,
    (Overcooked2Dlc.SEASONAL                  , 4  ): "Christmas 1-5" ,
    (Overcooked2Dlc.SEASONAL                  , 5  ): "Chinese 1-1"   ,
    (Overcooked2Dlc.SEASONAL                  , 6  ): "Chinese 1-2"   ,
    (Overcooked2Dlc.SEASONAL                  , 7  ): "Chinese 1-3"   ,
    (Overcooked2Dlc.SEASONAL                  , 8  ): "Chinese 1-4"   ,
    (Overcooked2Dlc.SEASONAL                  , 9  ): "Chinese 1-5"   ,
    (Overcooked2Dlc.SEASONAL                  , 10 ): "Chinese 1-6"   ,
    (Overcooked2Dlc.SEASONAL                  , 11 ): "Chinese 1-7"   ,
    (Overcooked2Dlc.SEASONAL                  , 12 ): "Winter 1-1"    ,
    (Overcooked2Dlc.SEASONAL                  , 13 ): "Winter H-2"    ,
    (Overcooked2Dlc.SEASONAL                  , 14 ): "Winter 1-3"    ,
    (Overcooked2Dlc.SEASONAL                  , 15 ): "Winter H-4"    ,
    (Overcooked2Dlc.SEASONAL                  , 16 ): "Winter 1-5"    ,
    (Overcooked2Dlc.SEASONAL                  , 17 ): "Spring 1-1"    ,
    (Overcooked2Dlc.SEASONAL                  , 18 ): "Spring 1-2"    ,
    (Overcooked2Dlc.SEASONAL                  , 19 ): "Spring 1-3"    ,
    (Overcooked2Dlc.SEASONAL                  , 20 ): "Spring 1-4"    ,
    (Overcooked2Dlc.SEASONAL                  , 21 ): "Spring 1-5"    ,
    (Overcooked2Dlc.SEASONAL                  , 22 ): "SOBO 1-1"      ,
    (Overcooked2Dlc.SEASONAL                  , 23 ): "SOBO 1-2"      ,
    (Overcooked2Dlc.SEASONAL                  , 24 ): "SOBO 1-3"      ,
    (Overcooked2Dlc.SEASONAL                  , 25 ): "SOBO 1-4"      ,
    (Overcooked2Dlc.SEASONAL                  , 26 ): "SOBO 1-5"      ,
    (Overcooked2Dlc.SEASONAL                  , 27 ): "Moon 1-1"      ,
    (Overcooked2Dlc.SEASONAL                  , 28 ): "Moon 1-2"      ,
    (Overcooked2Dlc.SEASONAL                  , 29 ): "Moon 1-3"      ,
    (Overcooked2Dlc.SEASONAL                  , 30 ): "Moon 1-4"      ,
    (Overcooked2Dlc.SEASONAL                  , 31 ): "Moon 1-5"      ,
}

class OverworldRegion(IntEnum):
    main = 0
    yellow_island = 1
    sky_shelf = 2
    stonehenge_mountain = 3
    tip_of_the_map = 4
    pink_island = 5
    mars_shelf = 6
    dark_green_mountain = 7
    kevin_eight_island = 8
    out_of_bounds = 9

overworld_region_by_level = {
    "1-1": OverworldRegion.main,
    "1-2": OverworldRegion.main,
    "1-3": OverworldRegion.main,
    "1-4": OverworldRegion.main,
    "1-5": OverworldRegion.yellow_island,
    "1-6": OverworldRegion.yellow_island,
    "2-1": OverworldRegion.main,
    "2-2": OverworldRegion.sky_shelf,
    "2-3": OverworldRegion.sky_shelf,
    "2-4": OverworldRegion.main,
    "2-5": OverworldRegion.main,
    "2-6": OverworldRegion.main,
    "3-1": OverworldRegion.stonehenge_mountain,
    "3-2": OverworldRegion.stonehenge_mountain,
    "3-3": OverworldRegion.stonehenge_mountain,
    "3-4": OverworldRegion.stonehenge_mountain,
    "3-5": OverworldRegion.stonehenge_mountain,
    "3-6": OverworldRegion.main,
    "4-1": OverworldRegion.main,
    "4-2": OverworldRegion.main,
    "4-3": OverworldRegion.main,
    "4-4": OverworldRegion.main,
    "4-5": OverworldRegion.main,
    "4-6": OverworldRegion.main,
    "5-1": OverworldRegion.main,
    "5-2": OverworldRegion.sky_shelf,
    "5-3": OverworldRegion.main,
    "5-4": OverworldRegion.tip_of_the_map,
    "5-5": OverworldRegion.tip_of_the_map,
    "5-6": OverworldRegion.tip_of_the_map,
    "6-1": OverworldRegion.pink_island,
    "6-2": OverworldRegion.tip_of_the_map,
    "6-3": OverworldRegion.tip_of_the_map,
    "6-4": OverworldRegion.sky_shelf,
    "6-5": OverworldRegion.mars_shelf,
    "6-6": OverworldRegion.mars_shelf,
    "Kevin-1": OverworldRegion.dark_green_mountain,
    "Kevin-2": OverworldRegion.main,
    "Kevin-3": OverworldRegion.main,
    "Kevin-4": OverworldRegion.main,
    "Kevin-5": OverworldRegion.main,
    "Kevin-6": OverworldRegion.main,
    "Kevin-7": OverworldRegion.tip_of_the_map,
    "Kevin-8": OverworldRegion.kevin_eight_island,
}

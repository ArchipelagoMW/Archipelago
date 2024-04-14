import typing
from BaseClasses import Region, Location
from .Locations import JakAndDaxterLocation, location_table

class JakAndDaxterLevel(int, Enum):
    GEYSER_ROCK = 0
    SANDOVER_VILLAGE = 1
    FORBIDDEN_JUNGLE = 2
    SENTINEL_BEACH = 3
    MISTY_ISLAND = 4
    FIRE_CANYON = 5
    ROCK_VILLAGE = 6
    PRECURSOR_BASIN = 7
    LOST_PRECURSOR_CITY = 8
    BOGGY_SWAMP = 9
    MOUNTAIN_PASS = 10
    VOLCANIC_CRATER = 11
    SPIDER_CAVE = 12
    SNOWY_MOUNTAIN = 13
    LAVA_TUBE = 14
    GOL_AND_MAIAS_CITADEL = 15

class JakAndDaxterSubLevel(int, Enum):
    MAIN = 0
    FORBIDDEN_JUNGLE_PLANT_ROOM = 1
    SENTINEL_BEACH_CANNON_TOWER = 2
    BOGGY_SWAMP_FLUT_FLUT = 3
    MOUNTAIN_PASS_SHORTCUT = 4
    SNOWY_MOUNTAIN_FLUT_FLUT = 5
    SNOWY_MOUNTAIN_LURKER_FORT = 6

class JakAndDaxterRegion(Region):
    game: str = "Jak and Daxter: The Precursor Legacy"

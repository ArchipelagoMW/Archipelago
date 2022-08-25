from enum import Enum
from random import Random


class Overcooked2Dlc(Enum):
    STORY = "Story"
    SURF_N_TURF = "Surf 'n' Turf"
    CAMPFIRE_COOK_OFF = "Campfire Cook Off"
    NIGHT_OF_THE_HANGRY_HORDE = "Night of the Hangry Horde"
    CARNIVAL_OF_CHAOS = "Carnival of Chaos"
    SEASONAL = "Seasonal"
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
    def start_level_id(self) -> int:
        if self == Overcooked2Dlc.STORY:
            return 1
        return 0

    # exclusive
    def end_level_id(self) -> int:
        if self == Overcooked2Dlc.STORY:
            return 1 + (6*6 + 8)
        if self == Overcooked2Dlc.SURF_N_TURF:
            return (3*4 + 1) + 1
        if self == Overcooked2Dlc.CAMPFIRE_COOK_OFF:
            return (3*4 + 3) + 1
        if self == Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE:
            return (3*3 + 3) + 1
        if self == Overcooked2Dlc.CARNIVAL_OF_CHAOS:
            return (3*4 + 3) + 1
        if self == Overcooked2Dlc.SEASONAL:
            return 32 + 1

        assert False

    # Tutorial + Horde Levels
    def excluded_levels(self) -> list[int]:
        if self == Overcooked2Dlc.STORY:
            return [0]
        if self == Overcooked2Dlc.SURF_N_TURF:
            return []
        if self == Overcooked2Dlc.CAMPFIRE_COOK_OFF:
            return []
        if self == Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE:
            return []
        if self == Overcooked2Dlc.CARNIVAL_OF_CHAOS:
            return [12, 13, 14, 15, 16, 17, 18, 19]
        if self == Overcooked2Dlc.SEASONAL:
            return [13, 15]

        assert False


class Overcooked2GameWorld(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    KEVIN = 7

    def as_str(self) -> str:
        if self == Overcooked2GameWorld.KEVIN:
            return "Kevin"

        return str(int(self.value))

    def get_sublevel_count(self) -> int:
        if self == Overcooked2GameWorld.KEVIN:
            return 8

        return 6

    def get_base_id(self) -> int:
        if self == Overcooked2GameWorld.ONE:
            return 1

        prev = Overcooked2GameWorld(self.value - 1)
        return prev.get_base_id() + prev.get_sublevel_count()

    def name(self) -> str:
        if self == Overcooked2GameWorld.KEVIN:
            return "Kevin"

        return "World " + self.as_str()


class Overcooked2Level:
    """
    Abstraction for a playable levels in Overcooked 2. By default constructor
    it can be used as an iterator for all locations in the Story map.
    """
    dlc: str
    sublevel: int

    def __init__(self, world: Overcooked2GameWorld, sublevel: int, dlc="Story"):
        self.world = world
        self.sublevel = sublevel
        self.dlc = Overcooked2Dlc("Story")

    def __init__(self):
        self.world = Overcooked2GameWorld.ONE
        self.sublevel = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.sublevel += 1
        if self.sublevel > self.world.get_sublevel_count():
            if self.world == Overcooked2GameWorld.KEVIN:
                raise StopIteration
            self.world = Overcooked2GameWorld(self.world.value + 1)
            self.sublevel = 1

        return self

    def level_id(self) -> int:
        return self.world.get_base_id() + (self.sublevel - 1)

    def level_name(self) -> str:
        return self.world.as_str() + "-" + str(self.sublevel)

    def location_name_completed(self) -> str:
        return self.level_name() + " Completed"

    def location_name_star_event(self, stars: int) -> str:
        return "%s (%d-Star)" % (self.level_name(), stars)

    def world_name(self) -> str:
        return self.world.name()


class Overcooked2GenericLevel():
    dlc: Overcooked2Dlc
    level_id: int

    def __init__(self, level_id: int, dlc: Overcooked2Dlc = Overcooked2Dlc("Story")):
        self.dlc = dlc
        self.level_id = level_id

    def __str__(self) -> str:
        return f"{self.dlc.value}|{self.level_id}"

    def __repr__(self) -> str:
        return self.__str__()


def level_shuffle_factory(rng: Random) -> dict[int, Overcooked2GenericLevel]:  # return <story_level_id, level>

    # Create a list of all valid levels for selection (excludes tutorial and kevin levels)
    pool = list()
    for dlc in Overcooked2Dlc:
        for level_id in range(dlc.start_level_id(), dlc.end_level_id()):
            if level_id not in dlc.excluded_levels():
                pool.append(
                    Overcooked2GenericLevel(level_id, dlc)
                )

    # Sort the pool to eliminate risk
    pool.sort(key=lambda x: int(x.dlc)*1000 + x.level_id)

    # Shuffle the pool, using the provided RNG
    rng.shuffle(pool)

    # Return the first 44 levels and assign those to each level
    result: dict[int, Overcooked2GenericLevel] = dict()
    story = Overcooked2Dlc.STORY
    for level_id in range(story.start_level_id(), story.end_level_id()):
        result[level_id] = pool.pop(0)

    return result

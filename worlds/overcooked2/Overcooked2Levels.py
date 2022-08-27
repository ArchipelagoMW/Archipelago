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
        id = None
        if self == Overcooked2Dlc.STORY:
            id = 6*6 + 8  # world_count*level_count + kevin count
        if self == Overcooked2Dlc.SURF_N_TURF:
            id = 3*4 + 1
        if self == Overcooked2Dlc.CAMPFIRE_COOK_OFF:
            id = 3*4 + 3
        if self == Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE:
            id = 3*3 + 3 + 9
        if self == Overcooked2Dlc.CARNIVAL_OF_CHAOS:
            id = 3*4 + 3
        if self == Overcooked2Dlc.SEASONAL:
            id = 31

        return self.start_level_id() + id

    # Tutorial + Horde Levels + Endgame
    def excluded_levels(self) -> list[int]:
        if self == Overcooked2Dlc.STORY:
            return [0, 36]

        return []
    
    def horde_levels(self) -> list[int]:
        if self == Overcooked2Dlc.NIGHT_OF_THE_HANGRY_HORDE:
            return [12, 13, 14, 15, 16, 17, 18, 19]
        if self == Overcooked2Dlc.SEASONAL:
            return [13, 15]

        return []


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
    world: Overcooked2GameWorld
    sublevel: int

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


def level_shuffle_factory(rng: Random, shuffle_horde_levels=False) -> dict[int, Overcooked2GenericLevel]:  # return <story_level_id, level>

    # Create a list of all valid levels for selection
    # (excludes tutorial, throne, kevin and sometimes horde levels)
    pool = list()
    for dlc in Overcooked2Dlc:
        for level_id in range(dlc.start_level_id(), dlc.end_level_id()):
            if level_id not in dlc.excluded_levels():
                if shuffle_horde_levels or level_id not in dlc.horde_levels():
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
        if level_id not in story.excluded_levels():
            result[level_id] = pool.pop(0)
        else:
            result[level_id] = Overcooked2GenericLevel(level_id) # This is just 6-6 right now

    return result

dlc_level_id_to_name = {
    (Overcooked2Dlc.STORY, 1 ): "Story 1-1",
    (Overcooked2Dlc.STORY, 2 ): "Story 1-2",
    (Overcooked2Dlc.STORY, 3 ): "Story 1-3",
    (Overcooked2Dlc.STORY, 4 ): "Story 1-4",
    (Overcooked2Dlc.STORY, 5 ): "Story 1-5",
    (Overcooked2Dlc.STORY, 6 ): "Story 1-6",
    (Overcooked2Dlc.STORY, 7 ): "Story 2-1",
    (Overcooked2Dlc.STORY, 8 ): "Story 2-2",
    (Overcooked2Dlc.STORY, 9 ): "Story 2-3",
    (Overcooked2Dlc.STORY, 10): "Story 2-4",
    (Overcooked2Dlc.STORY, 11): "Story 2-5",
    (Overcooked2Dlc.STORY, 12): "Story 2-6",
    (Overcooked2Dlc.STORY, 13): "Story 3-1",
    (Overcooked2Dlc.STORY, 14): "Story 3-2",
    (Overcooked2Dlc.STORY, 15): "Story 3-3",
    (Overcooked2Dlc.STORY, 16): "Story 3-4",
    (Overcooked2Dlc.STORY, 17): "Story 3-5",
    (Overcooked2Dlc.STORY, 18): "Story 3-6",
    (Overcooked2Dlc.STORY, 19): "Story 4-1",
    (Overcooked2Dlc.STORY, 20): "Story 4-2",
    (Overcooked2Dlc.STORY, 21): "Story 4-3",
    (Overcooked2Dlc.STORY, 22): "Story 4-4",
    (Overcooked2Dlc.STORY, 23): "Story 4-5",
    (Overcooked2Dlc.STORY, 24): "Story 4-6",
    (Overcooked2Dlc.STORY, 25): "Story 5-1",
    (Overcooked2Dlc.STORY, 26): "Story 5-2",
    (Overcooked2Dlc.STORY, 27): "Story 5-3",
    (Overcooked2Dlc.STORY, 28): "Story 5-4",
    (Overcooked2Dlc.STORY, 29): "Story 5-5",
    (Overcooked2Dlc.STORY, 30): "Story 5-6",
    (Overcooked2Dlc.STORY, 31): "Story 6-1",
    (Overcooked2Dlc.STORY, 32): "Story 6-2",
    (Overcooked2Dlc.STORY, 33): "Story 6-3",
    (Overcooked2Dlc.STORY, 34): "Story 6-4",
    (Overcooked2Dlc.STORY, 35): "Story 6-5",
    (Overcooked2Dlc.STORY, 36): "Story 6-6",
}

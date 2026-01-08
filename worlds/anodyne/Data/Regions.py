from abc import abstractmethod
from enum import Enum, auto

area_name_trans = {
    "Overworld": "Woods",
    "Bedroom": "Temple of the Seeing One",
    "Red Cave": "Red Grotto",
    "Crowd": "Mountain Cavern",
    "Forest": "Deep Forest",
    "Suburb": "Young Town",
    "Terminal": "Crossing",
    "Happy": "Red",
    "Go": "Garden"
}

all_areas: list[type['RegionEnum']] = []
area_lookup: dict[str, type['RegionEnum']] = {}


class RegionEnum(Enum):
    def __init_subclass__(cls, **kwargs):
        all_areas.append(cls)
        area_lookup[cls.area_name()] = cls

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return "" if name == "DEFAULT" else name.replace('_', ' ')

    @classmethod
    def area_id(cls):
        return all_areas.index(cls)

    @classmethod
    def area_name(cls):
        name = cls.__name__.replace('_', ' ')
        return area_name_trans.setdefault(name, name)

    @classmethod
    @abstractmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        pass

    def __str__(self):
        return self.area_name() + (' ' + self.value).rstrip()


class Apartment(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 592, 833

    floor_1 = auto()
    floor_1_top_left = auto()
    floor_2 = auto()
    floor_2_top_left = auto()
    floor_3 = auto()


class Beach(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 288, 721

    DEFAULT = auto()
    gauntlet = auto()


class Bedroom(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 592, 897

    entrance = auto()
    core = auto()
    shieldy_room = auto()
    after_statue = auto()
    exit = auto()
    drawer = auto()


class Blank(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 80, 400

    windmill = auto()


class Blue(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 352, 513

    DEFAULT = auto()


class Boss_Rush(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 512, 240

    DEFAULT = auto()


class Cell(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 272, 497

    DEFAULT = auto()
    past_gate = auto()


class Circus(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 192, 497

    DEFAULT = auto()
    entrance_lake = auto()
    entry_gauntlets = auto()
    past_entrance_lake = auto()
    circlejump_gauntlets = auto()
    third_key_gauntlet = auto()
    boss_gauntlet = auto()
    north_gauntlet = auto()


class Cliffs(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 512, 561

    DEFAULT = auto()
    post_windmill = auto()


class Crowd(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 592, 561

    floor_1 = auto()
    floor_2 = auto()
    floor_2_gauntlets = auto()
    floor_3 = auto()
    floor_3_center = auto()
    jump_challenge = auto()
    exit = auto()


class Debug(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 256, 240

    DEFAULT = auto()


class Drawer(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 401, 244

    DEFAULT = auto()
    dark = auto()


class Fields(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 400, 721

    DEFAULT = auto()
    Lake = auto()
    Past_Gate = auto()
    Terminal_Entrance = auto()
    North_Secret_Area = auto()
    Goldman = "Goldman's Cave"
    East = auto()


class Forest(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 512, 721

    DEFAULT = auto()


class Go(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 352, 577

    bottom = auto()
    top = auto()


class Happy(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 448, 513

    DEFAULT = auto()
    gauntlet = auto()


class Hotel(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 592, 497

    roof = auto()
    floor_4 = auto()
    floor_4_pad = auto()
    floor_3 = auto()
    floor_2 = auto()
    floor_2_right = auto()
    floor_1 = auto()


class Nexus(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 0, 0

    bottom = auto()
    top = auto()
    ending = auto()


class Overworld(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 512, 897

    DEFAULT = auto()
    west = auto()
    Gauntlet = auto()
    post_windmill = auto()


class Red_Cave(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 192, 562

    top = auto()
    left = auto()
    center = auto()
    right = auto()
    bottom = auto()
    exit = auto()
    Isaac = auto()


class Red_Sea(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 272, 562

    DEFAULT = auto()


class Space(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 512, 497

    DEFAULT = auto()
    Gauntlet = auto()


class Street(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 256, 897

    DEFAULT = auto()


class Suburb(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 512, 833

    DEFAULT = auto()
    card_house = auto()
    past_gate = auto()


class Terminal(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 352, 657

    DEFAULT = auto()
    top = auto()


class Windmill(RegionEnum):
    @classmethod
    def nexus_ut_loc(cls) -> tuple[int, int]:
        return 448, 657

    DEFAULT = auto()
    entrance = auto()


early_nexus_gates = [
    Beach,
    Cliffs,
    Fields,
    Forest,
    Overworld,
    Red_Sea
]

endgame_nexus_gates = [
    Blue,
    Go,
    Happy,
]

post_temple_boss_nexus_gates: list[type[RegionEnum]] = [
    Bedroom,
    Suburb,
    Apartment
]

wrong_big_key_early_locked_nexus_gates = [
    Apartment,
    Bedroom,
    Suburb
]

postgame_regions: list[RegionEnum] = [
    Bedroom.drawer,
    *Drawer,
    *Blank,
    *Debug,
    *Boss_Rush,
    Nexus.top,
    Nexus.ending,
    Space.Gauntlet
]

postgame_without_secret_paths: list[RegionEnum] = [
    Fields.North_Secret_Area
]

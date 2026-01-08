from typing import NamedTuple, Callable
from enum import Flag, auto

from ..Options import AnodyneGameOptions, BigKeyShuffle, VictoryCondition, RedCaveAccess
from .Regions import Bedroom, Crowd, Windmill, Hotel, Circus, Apartment, Terminal, Go, Blue, \
    Happy, Red_Cave, RegionEnum, Nexus


def big_keys_vanilla(options: AnodyneGameOptions):
    return options.big_key_shuffle == BigKeyShuffle.option_vanilla


def windmill_vanilla(options: AnodyneGameOptions):
    return options.split_windmill.value == False


def blue_happy_vanilla(options: AnodyneGameOptions):
    return options.include_blue_happy.value == False


def final_gate_ending(options: AnodyneGameOptions):
    return options.victory_condition == VictoryCondition.option_final_gate


def tentacles_vanilla(options: AnodyneGameOptions):
    return options.red_grotto_access == RedCaveAccess.option_vanilla


# Not all of these are used, but need to be here for flag consistency
class EventFlags(Flag):
    Seer = auto()
    Wall = auto()
    Rogue = auto()
    Manager = auto()
    Watcher = auto()
    Servants = auto()
    Sage = auto()
    Briar = auto()
    Windmill = auto()
    Tentacle_CL = auto()
    Tentacle_CR = auto()
    Tentacle_L = auto()
    Tentacle_R = auto()
    Redcave_R = auto()
    Redcave_L = auto()
    Redcave_N = auto()
    SwapExtended = auto()
    GreenKey = auto()
    RedKey = auto()
    BlueKey = auto()
    Puzzle_Hotel = auto()
    Puzzle_Apartment = auto()
    Puzzle_Circus = auto()
    NStreet = auto()
    NOverworld = auto()
    NRedcave = auto()
    NCrowd = auto()
    NApartment = auto()
    NHotel = auto()
    NCircus = auto()
    NCliff = auto()
    NForest = auto()
    NWindmill = auto()
    NRedsea = auto()
    NBeach = auto()
    NBedroom = auto()
    NFields = auto()
    NGo = auto()
    NTerminal = auto()
    NHappy = auto()
    NSpace = auto()
    NCell = auto()
    NSuburb = auto()
    NBlue = auto()
    Activate_Blue = auto()
    Activate_Happy = auto()
    Victory = auto()  # not real, I'll figure it out if ppl ask


class EventData(NamedTuple):
    region: RegionEnum
    name: str
    reqs: list[str]
    tracker_loc: tuple[int, int]
    flag: EventFlags
    is_active: Callable[[AnodyneGameOptions], bool] = lambda _: True


all_events: list[EventData] = [
    EventData(Bedroom.exit, "Defeat Seer", ["Combat"], (392, 59), EventFlags.Seer),
    EventData(Bedroom.exit, "Grab Green Key", [], (600, 104), EventFlags.GreenKey, big_keys_vanilla),
    EventData(Crowd.floor_1, "Defeat The Wall", ["Combat", "Jump Shoes"], (1519, 984), EventFlags.Wall),
    EventData(Crowd.exit, "Grab Blue Key", [], (1544, 872), EventFlags.BlueKey, big_keys_vanilla),
    EventData(Windmill.DEFAULT, "Windmill activated", [], (216, 376), EventFlags.Windmill, windmill_vanilla),
    EventData(Hotel.floor_1, "Defeat Manager", ["Small Key (Hotel):6", "Combat"], (1356, 1661), EventFlags.Manager),
    EventData(Circus.boss_gauntlet, "Defeat Servants", ["Combat", "Jump Shoes"], (734, 184), EventFlags.Servants),
    EventData(Apartment.floor_3, "Defeat Watcher", ["Combat", "Small Key (Apartment):4"], (1196, 993),
              EventFlags.Watcher),
    EventData(Terminal.top, "Defeat Sage", ["Combat", "Jump Shoes"], (400, 522), EventFlags.Sage),
    EventData(Go.top, "Defeat Briar", ["Combat", "Complete Blue", "Complete Happy"], (400, 216), EventFlags.Briar),
    EventData(Blue.DEFAULT, "Blue Completion", ["Combat", "Jump Shoes"], (5 * 16, 2 * 16), EventFlags.Activate_Blue,
              blue_happy_vanilla),
    EventData(Happy.gauntlet, "Happy Completion", [], (41 * 16, 11 * 16), EventFlags.Activate_Happy,
              blue_happy_vanilla),
    EventData(Nexus.ending, "Open final gate", [], (400, 32), EventFlags.Victory, final_gate_ending),
    EventData(Red_Cave.center, "Center left tentacle hit", ["Combat"], (232, 216), EventFlags.Tentacle_CL,
              tentacles_vanilla),
    EventData(Red_Cave.center, "Center right tentacle hit", ["Combat"], (840, 200), EventFlags.Tentacle_CR,
              tentacles_vanilla),
    EventData(Red_Cave.left, "Left tentacle hit", ["Combat", "Small Key (Red Grotto):6"], (200, 664),
              EventFlags.Tentacle_L, tentacles_vanilla),
    EventData(Red_Cave.right, "Right tentacle hit", ["Combat", "Small Key (Red Grotto):6"], (872, 680),
              EventFlags.Tentacle_R, tentacles_vanilla),
    EventData(Red_Cave.top, "Defeat Rogue", ["Combat"], (1056, 80), EventFlags.Rogue),
    EventData(Red_Cave.exit, "Grab Red Key", [], (1096, 296), EventFlags.RedKey, big_keys_vanilla)
]

all_event_names = {event.name for event in all_events}

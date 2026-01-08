from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import WordipelagoWorld


class WordipelagoLocation(Location):
    game = "Wordipelago"


class WordipelagoLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["WordipelagoWorld"], bool] = lambda world: True


location_data_table: Dict[str, WordipelagoLocationData] = {
    "Used A": WordipelagoLocationData(region="Letters", address=1, can_create=lambda world: world.options.letter_checks >= 1),
    "Used B": WordipelagoLocationData(region="Letters", address=2, can_create=lambda world: world.options.letter_checks >= 2),
    "Used C": WordipelagoLocationData(region="Letters", address=3, can_create=lambda world: world.options.letter_checks >= 2),
    "Used D": WordipelagoLocationData(region="Letters", address=4, can_create=lambda world: world.options.letter_checks >= 2),
    "Used E": WordipelagoLocationData(region="Letters", address=5, can_create=lambda world: world.options.letter_checks >= 1),
    "Used F": WordipelagoLocationData(region="Letters", address=6, can_create=lambda world: world.options.letter_checks >= 2),
    "Used G": WordipelagoLocationData(region="Letters", address=7, can_create=lambda world: world.options.letter_checks >= 2),
    "Used H": WordipelagoLocationData(region="Letters", address=8, can_create=lambda world: world.options.letter_checks >= 2),
    "Used I": WordipelagoLocationData(region="Letters", address=9, can_create=lambda world: world.options.letter_checks >= 1),
    "Used J": WordipelagoLocationData(region="Letters", address=10, can_create=lambda world: world.options.letter_checks >= 3),
    "Used K": WordipelagoLocationData(region="Letters", address=11, can_create=lambda world: world.options.letter_checks >= 3),
    "Used L": WordipelagoLocationData(region="Letters", address=12, can_create=lambda world: world.options.letter_checks >= 2),
    "Used M": WordipelagoLocationData(region="Letters", address=13, can_create=lambda world: world.options.letter_checks >= 2),
    "Used N": WordipelagoLocationData(region="Letters", address=14, can_create=lambda world: world.options.letter_checks >= 2),
    "Used O": WordipelagoLocationData(region="Letters", address=15, can_create=lambda world: world.options.letter_checks >= 1),
    "Used P": WordipelagoLocationData(region="Letters", address=16, can_create=lambda world: world.options.letter_checks >= 2),
    "Used Q": WordipelagoLocationData(region="Letters", address=17, can_create=lambda world: world.options.letter_checks >= 3),
    "Used R": WordipelagoLocationData(region="Letters", address=18, can_create=lambda world: world.options.letter_checks >= 2),
    "Used S": WordipelagoLocationData(region="Letters", address=19, can_create=lambda world: world.options.letter_checks >= 2),
    "Used T": WordipelagoLocationData(region="Letters", address=20, can_create=lambda world: world.options.letter_checks >= 2),
    "Used U": WordipelagoLocationData(region="Letters", address=21, can_create=lambda world: world.options.letter_checks >= 1),
    "Used V": WordipelagoLocationData(region="Letters", address=22, can_create=lambda world: world.options.letter_checks >= 3),
    "Used W": WordipelagoLocationData(region="Letters", address=23, can_create=lambda world: world.options.letter_checks >= 3),
    "Used X": WordipelagoLocationData(region="Letters", address=24, can_create=lambda world: world.options.letter_checks >= 3),
    "Used Y": WordipelagoLocationData(region="Letters", address=25, can_create=lambda world: world.options.letter_checks >= 1),
    "Used Z": WordipelagoLocationData(region="Letters", address=26, can_create=lambda world: world.options.letter_checks >= 3),

    "1 Correct Letter In Word": WordipelagoLocationData(region="Green Checks 1", address=101, can_create=lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),
    "2 Correct Letters In Word": WordipelagoLocationData(region="Green Checks 2", address=102, can_create=lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),
    "3 Correct Letters In Word": WordipelagoLocationData(region="Green Checks 3", address=103, can_create=lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),
    "4 Correct Letters In Word": WordipelagoLocationData(region="Green Checks 4", address=104, can_create=lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),
    "5 Correct Letters In Word": WordipelagoLocationData(region="Green Checks 5", address=105, can_create=lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),

    "----G": WordipelagoLocationData(region="Green Checks 1", address=201, can_create=lambda world: world.options.green_checks >= 2),
    "---G-": WordipelagoLocationData(region="Green Checks 1", address=202, can_create=lambda world: world.options.green_checks >= 2),
    "---GG": WordipelagoLocationData(region="Green Checks 2", address=203, can_create=lambda world: world.options.green_checks >= 2),
    "--G--": WordipelagoLocationData(region="Green Checks 1", address=204, can_create=lambda world: world.options.green_checks >= 2),
    "--G-G": WordipelagoLocationData(region="Green Checks 2", address=205, can_create=lambda world: world.options.green_checks >= 2),
    "--GG-": WordipelagoLocationData(region="Green Checks 2", address=206, can_create=lambda world: world.options.green_checks >= 2),
    "--GGG": WordipelagoLocationData(region="Green Checks 3", address=207, can_create=lambda world: world.options.green_checks >= 2),
    "-G---": WordipelagoLocationData(region="Green Checks 1", address=208, can_create=lambda world: world.options.green_checks >= 2),
    "-G--G": WordipelagoLocationData(region="Green Checks 2", address=209, can_create=lambda world: world.options.green_checks >= 2),
    "-G-G-": WordipelagoLocationData(region="Green Checks 2", address=210, can_create=lambda world: world.options.green_checks >= 2),
    "-G-GG": WordipelagoLocationData(region="Green Checks 3", address=211, can_create=lambda world: world.options.green_checks >= 2),
    "-GG--": WordipelagoLocationData(region="Green Checks 2", address=212, can_create=lambda world: world.options.green_checks >= 2),
    "-GG-G": WordipelagoLocationData(region="Green Checks 3", address=213, can_create=lambda world: world.options.green_checks >= 2),
    "-GGG-": WordipelagoLocationData(region="Green Checks 3", address=214, can_create=lambda world: world.options.green_checks >= 2),
    "-GGGG": WordipelagoLocationData(region="Green Checks 4", address=215, can_create=lambda world: world.options.green_checks >= 2),
    "G----": WordipelagoLocationData(region="Green Checks 1", address=216, can_create=lambda world: world.options.green_checks >= 2),
    "G---G": WordipelagoLocationData(region="Green Checks 2", address=217, can_create=lambda world: world.options.green_checks >= 2),
    "G--G-": WordipelagoLocationData(region="Green Checks 2", address=218, can_create=lambda world: world.options.green_checks >= 2),
    "G--GG": WordipelagoLocationData(region="Green Checks 3", address=219, can_create=lambda world: world.options.green_checks >= 2),
    "G-G--": WordipelagoLocationData(region="Green Checks 2", address=220, can_create=lambda world: world.options.green_checks >= 2),
    "G-G-G": WordipelagoLocationData(region="Green Checks 3", address=221, can_create=lambda world: world.options.green_checks >= 2),
    "G-GG-": WordipelagoLocationData(region="Green Checks 3", address=222, can_create=lambda world: world.options.green_checks >= 2),
    "G-GGG": WordipelagoLocationData(region="Green Checks 4", address=223, can_create=lambda world: world.options.green_checks >= 2),
    "GG---": WordipelagoLocationData(region="Green Checks 2", address=224, can_create=lambda world: world.options.green_checks >= 2),
    "GG--G": WordipelagoLocationData(region="Green Checks 3", address=225, can_create=lambda world: world.options.green_checks >= 2),
    "GG-G-": WordipelagoLocationData(region="Green Checks 3", address=226, can_create=lambda world: world.options.green_checks >= 2),
    "GG-GG": WordipelagoLocationData(region="Green Checks 4", address=227, can_create=lambda world: world.options.green_checks >= 2),
    "GGG--": WordipelagoLocationData(region="Green Checks 3", address=228, can_create=lambda world: world.options.green_checks >= 2),
    "GGG-G": WordipelagoLocationData(region="Green Checks 4", address=229, can_create=lambda world: world.options.green_checks >= 2),
    "GGGG-": WordipelagoLocationData(region="Green Checks 4", address=230, can_create=lambda world: world.options.green_checks >= 2),
    "GGGGG": WordipelagoLocationData(region="Green Checks 5", address=231, can_create=lambda world: world.options.green_checks >= 2),

    "----Y": WordipelagoLocationData(region="Yellow Checks 1", address=301, can_create=lambda world: world.options.yellow_checks == 1),
    "---Y-": WordipelagoLocationData(region="Yellow Checks 1", address=302, can_create=lambda world: world.options.yellow_checks == 1),
    "---YY": WordipelagoLocationData(region="Yellow Checks 2", address=303, can_create=lambda world: world.options.yellow_checks == 1),
    "--Y--": WordipelagoLocationData(region="Yellow Checks 1", address=304, can_create=lambda world: world.options.yellow_checks == 1),
    "--Y-Y": WordipelagoLocationData(region="Yellow Checks 2", address=305, can_create=lambda world: world.options.yellow_checks == 1),
    "--YY-": WordipelagoLocationData(region="Yellow Checks 2", address=306, can_create=lambda world: world.options.yellow_checks == 1),
    "--YYY": WordipelagoLocationData(region="Yellow Checks 3", address=307, can_create=lambda world: world.options.yellow_checks == 1),
    "-Y---": WordipelagoLocationData(region="Yellow Checks 1", address=308, can_create=lambda world: world.options.yellow_checks == 1),
    "-Y--Y": WordipelagoLocationData(region="Yellow Checks 2", address=309, can_create=lambda world: world.options.yellow_checks == 1),
    "-Y-Y-": WordipelagoLocationData(region="Yellow Checks 2", address=310, can_create=lambda world: world.options.yellow_checks == 1),
    "-Y-YY": WordipelagoLocationData(region="Yellow Checks 3", address=311, can_create=lambda world: world.options.yellow_checks == 1),
    "-YY--": WordipelagoLocationData(region="Yellow Checks 2", address=312, can_create=lambda world: world.options.yellow_checks == 1),
    "-YY-Y": WordipelagoLocationData(region="Yellow Checks 3", address=313, can_create=lambda world: world.options.yellow_checks == 1),
    "-YYY-": WordipelagoLocationData(region="Yellow Checks 3", address=314, can_create=lambda world: world.options.yellow_checks == 1),
    "-YYYY": WordipelagoLocationData(region="Yellow Checks 4", address=315, can_create=lambda world: world.options.yellow_checks == 1),
    "Y----": WordipelagoLocationData(region="Yellow Checks 1", address=316, can_create=lambda world: world.options.yellow_checks == 1),
    "Y---Y": WordipelagoLocationData(region="Yellow Checks 2", address=317, can_create=lambda world: world.options.yellow_checks == 1),
    "Y--Y-": WordipelagoLocationData(region="Yellow Checks 2", address=318, can_create=lambda world: world.options.yellow_checks == 1),
    "Y--YY": WordipelagoLocationData(region="Yellow Checks 3", address=319, can_create=lambda world: world.options.yellow_checks == 1),
    "Y-Y--": WordipelagoLocationData(region="Yellow Checks 2", address=320, can_create=lambda world: world.options.yellow_checks == 1),
    "Y-Y-Y": WordipelagoLocationData(region="Yellow Checks 3", address=321, can_create=lambda world: world.options.yellow_checks == 1),
    "Y-YY-": WordipelagoLocationData(region="Yellow Checks 3", address=322, can_create=lambda world: world.options.yellow_checks == 1),
    "Y-YYY": WordipelagoLocationData(region="Yellow Checks 4", address=323, can_create=lambda world: world.options.yellow_checks == 1),
    "YY---": WordipelagoLocationData(region="Yellow Checks 2", address=324, can_create=lambda world: world.options.yellow_checks == 1),
    "YY--Y": WordipelagoLocationData(region="Yellow Checks 3", address=325, can_create=lambda world: world.options.yellow_checks == 1),
    "YY-Y-": WordipelagoLocationData(region="Yellow Checks 3", address=326, can_create=lambda world: world.options.yellow_checks == 1),
    "YY-YY": WordipelagoLocationData(region="Yellow Checks 4", address=327, can_create=lambda world: world.options.yellow_checks == 1),
    "YYY--": WordipelagoLocationData(region="Yellow Checks 3", address=328, can_create=lambda world: world.options.yellow_checks == 1),
    "YYY-Y": WordipelagoLocationData(region="Yellow Checks 4", address=329, can_create=lambda world: world.options.yellow_checks == 1),
    "YYYY-": WordipelagoLocationData(region="Yellow Checks 4", address=330, can_create=lambda world: world.options.yellow_checks == 1),
    "YYYYY": WordipelagoLocationData(region="Yellow Checks 5", address=331, can_create=lambda world: world.options.yellow_checks == 1),
}



def get_location_table():
    location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
    for i in range(50):
        location_table["Word " + str(i + 1)] = 1001 + i
    for i in range(50):
        location_table[str(i + 1) + " Word Streak"] = 2001 + i
    for i in range(200):
        location_table["Point Shop Purchase " + str(i + 1)] = 3001 + i
    return location_table

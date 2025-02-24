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
    "Used A": WordipelagoLocationData(region="Letters", address=1, lambda world: world.options.letter_checks >= 1),
    "Used B": WordipelagoLocationData(region="Letters", address=2, lambda world: world.options.letter_checks >= 2),
    "Used C": WordipelagoLocationData(region="Letters", address=3, lambda world: world.options.letter_checks >= 2),
    "Used D": WordipelagoLocationData(region="Letters", address=4, lambda world: world.options.letter_checks >= 2),
    "Used E": WordipelagoLocationData(region="Letters", address=5, lambda world: world.options.letter_checks >= 1),
    "Used F": WordipelagoLocationData(region="Letters", address=6, lambda world: world.options.letter_checks >= 2),
    "Used G": WordipelagoLocationData(region="Letters", address=7, lambda world: world.options.letter_checks >= 2),
    "Used H": WordipelagoLocationData(region="Letters", address=8, lambda world: world.options.letter_checks >= 2),
    "Used I": WordipelagoLocationData(region="Letters", address=9, lambda world: world.options.letter_checks >= 1),
    "Used J": WordipelagoLocationData(region="Letters", address=10, lambda world: world.options.letter_checks >= 3),
    "Used K": WordipelagoLocationData(region="Letters", address=11, lambda world: world.options.letter_checks >= 3),
    "Used L": WordipelagoLocationData(region="Letters", address=12, lambda world: world.options.letter_checks >= 2),
    "Used M": WordipelagoLocationData(region="Letters", address=13, lambda world: world.options.letter_checks >= 2),
    "Used N": WordipelagoLocationData(region="Letters", address=14, lambda world: world.options.letter_checks >= 2),
    "Used O": WordipelagoLocationData(region="Letters", address=15, lambda world: world.options.letter_checks >= 1),
    "Used P": WordipelagoLocationData(region="Letters", address=16, lambda world: world.options.letter_checks >= 2),
    "Used Q": WordipelagoLocationData(region="Letters", address=17, lambda world: world.options.letter_checks >= 3),
    "Used R": WordipelagoLocationData(region="Letters", address=18, lambda world: world.options.letter_checks >= 2),
    "Used S": WordipelagoLocationData(region="Letters", address=19, lambda world: world.options.letter_checks >= 2),
    "Used T": WordipelagoLocationData(region="Letters", address=20, lambda world: world.options.letter_checks >= 2),
    "Used U": WordipelagoLocationData(region="Letters", address=21, lambda world: world.options.letter_checks >= 1),
    "Used V": WordipelagoLocationData(region="Letters", address=22, lambda world: world.options.letter_checks >= 3),
    "Used W": WordipelagoLocationData(region="Letters", address=23, lambda world: world.options.letter_checks >= 3),
    "Used X": WordipelagoLocationData(region="Letters", address=24, lambda world: world.options.letter_checks >= 3),
    "Used Y": WordipelagoLocationData(region="Letters", address=25, lambda world: world.options.letter_checks >= 1),
    "Used Z": WordipelagoLocationData(region="Letters", address=26, lambda world: world.options.letter_checks >= 3),

    "1 Correct Letter In Word": WordipelagoLocationData(region="WordBest", address=101, lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),
    "2 Correct Letters In Word": WordipelagoLocationData(region="WordBest", address=102, lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),
    "3 Correct Letters In Word": WordipelagoLocationData(region="WordBest", address=103, lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),
    "4 Correct Letters In Word": WordipelagoLocationData(region="WordBest", address=104, lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),
    "5 Correct Letters In Word": WordipelagoLocationData(region="WordBest", address=105, lambda world: world.options.green_checks == 1 or world.options.green_checks == 3),

    "----G": WordipelagoLocationData(region="GreenChecks", address=201, lambda world: world.options.green_checks >= 2),
    "---G-": WordipelagoLocationData(region="GreenChecks", address=202, lambda world: world.options.green_checks >= 2),
    "---GG": WordipelagoLocationData(region="GreenChecks", address=203, lambda world: world.options.green_checks >= 2),
    "--G--": WordipelagoLocationData(region="GreenChecks", address=204, lambda world: world.options.green_checks >= 2),
    "--G-G": WordipelagoLocationData(region="GreenChecks", address=205, lambda world: world.options.green_checks >= 2),
    "--GG-": WordipelagoLocationData(region="GreenChecks", address=206, lambda world: world.options.green_checks >= 2),
    "--GGG": WordipelagoLocationData(region="GreenChecks", address=207, lambda world: world.options.green_checks >= 2),
    "-G---": WordipelagoLocationData(region="GreenChecks", address=208, lambda world: world.options.green_checks >= 2),
    "-G--G": WordipelagoLocationData(region="GreenChecks", address=209, lambda world: world.options.green_checks >= 2),
    "-G-G-": WordipelagoLocationData(region="GreenChecks", address=210, lambda world: world.options.green_checks >= 2),
    "-G-GG": WordipelagoLocationData(region="GreenChecks", address=211, lambda world: world.options.green_checks >= 2),
    "-GG--": WordipelagoLocationData(region="GreenChecks", address=212, lambda world: world.options.green_checks >= 2),
    "-GG-G": WordipelagoLocationData(region="GreenChecks", address=213, lambda world: world.options.green_checks >= 2),
    "-GGG-": WordipelagoLocationData(region="GreenChecks", address=214, lambda world: world.options.green_checks >= 2),
    "-GGGG": WordipelagoLocationData(region="GreenChecks", address=215, lambda world: world.options.green_checks >= 2),
    "G----": WordipelagoLocationData(region="GreenChecks", address=216, lambda world: world.options.green_checks >= 2),
    "G---G": WordipelagoLocationData(region="GreenChecks", address=217, lambda world: world.options.green_checks >= 2),
    "G--G-": WordipelagoLocationData(region="GreenChecks", address=218, lambda world: world.options.green_checks >= 2),
    "G--GG": WordipelagoLocationData(region="GreenChecks", address=219, lambda world: world.options.green_checks >= 2),
    "G-G--": WordipelagoLocationData(region="GreenChecks", address=220, lambda world: world.options.green_checks >= 2),
    "G-G-G": WordipelagoLocationData(region="GreenChecks", address=221, lambda world: world.options.green_checks >= 2),
    "G-GG-": WordipelagoLocationData(region="GreenChecks", address=222, lambda world: world.options.green_checks >= 2),
    "G-GGG": WordipelagoLocationData(region="GreenChecks", address=223, lambda world: world.options.green_checks >= 2),
    "GG---": WordipelagoLocationData(region="GreenChecks", address=224, lambda world: world.options.green_checks >= 2),
    "GG--G": WordipelagoLocationData(region="GreenChecks", address=225, lambda world: world.options.green_checks >= 2),
    "GG-G-": WordipelagoLocationData(region="GreenChecks", address=226, lambda world: world.options.green_checks >= 2),
    "GG-GG": WordipelagoLocationData(region="GreenChecks", address=227, lambda world: world.options.green_checks >= 2),
    "GGG--": WordipelagoLocationData(region="GreenChecks", address=228, lambda world: world.options.green_checks >= 2),
    "GGG-G": WordipelagoLocationData(region="GreenChecks", address=229, lambda world: world.options.green_checks >= 2),
    "GGGG-": WordipelagoLocationData(region="GreenChecks", address=230, lambda world: world.options.green_checks >= 2),
    "GGGGG": WordipelagoLocationData(region="GreenChecks", address=231, lambda world: world.options.green_checks >= 2),

    "----Y": WordipelagoLocationData(region="YellowChecks", address=301, lambda world: world.options.yellow_checks == 1),
    "---Y-": WordipelagoLocationData(region="YellowChecks", address=302, lambda world: world.options.yellow_checks == 1),
    "---YY": WordipelagoLocationData(region="YellowChecks", address=303, lambda world: world.options.yellow_checks == 1),
    "--Y--": WordipelagoLocationData(region="YellowChecks", address=304, lambda world: world.options.yellow_checks == 1),
    "--Y-Y": WordipelagoLocationData(region="YellowChecks", address=305, lambda world: world.options.yellow_checks == 1),
    "--YY-": WordipelagoLocationData(region="YellowChecks", address=306, lambda world: world.options.yellow_checks == 1),
    "--YYY": WordipelagoLocationData(region="YellowChecks", address=307, lambda world: world.options.yellow_checks == 1),
    "-Y---": WordipelagoLocationData(region="YellowChecks", address=308, lambda world: world.options.yellow_checks == 1),
    "-Y--Y": WordipelagoLocationData(region="YellowChecks", address=309, lambda world: world.options.yellow_checks == 1),
    "-Y-Y-": WordipelagoLocationData(region="YellowChecks", address=310, lambda world: world.options.yellow_checks == 1),
    "-Y-YY": WordipelagoLocationData(region="YellowChecks", address=311, lambda world: world.options.yellow_checks == 1),
    "-YY--": WordipelagoLocationData(region="YellowChecks", address=312, lambda world: world.options.yellow_checks == 1),
    "-YY-Y": WordipelagoLocationData(region="YellowChecks", address=313, lambda world: world.options.yellow_checks == 1),
    "-YYY-": WordipelagoLocationData(region="YellowChecks", address=314, lambda world: world.options.yellow_checks == 1),
    "-YYYY": WordipelagoLocationData(region="YellowChecks", address=315, lambda world: world.options.yellow_checks == 1),
    "Y----": WordipelagoLocationData(region="YellowChecks", address=316, lambda world: world.options.yellow_checks == 1),
    "Y---Y": WordipelagoLocationData(region="YellowChecks", address=317, lambda world: world.options.yellow_checks == 1),
    "Y--Y-": WordipelagoLocationData(region="YellowChecks", address=318, lambda world: world.options.yellow_checks == 1),
    "Y--YY": WordipelagoLocationData(region="YellowChecks", address=319, lambda world: world.options.yellow_checks == 1),
    "Y-Y--": WordipelagoLocationData(region="YellowChecks", address=320, lambda world: world.options.yellow_checks == 1),
    "Y-Y-Y": WordipelagoLocationData(region="YellowChecks", address=321, lambda world: world.options.yellow_checks == 1),
    "Y-YY-": WordipelagoLocationData(region="YellowChecks", address=322, lambda world: world.options.yellow_checks == 1),
    "Y-YYY": WordipelagoLocationData(region="YellowChecks", address=323, lambda world: world.options.yellow_checks == 1),
    "YY---": WordipelagoLocationData(region="YellowChecks", address=324, lambda world: world.options.yellow_checks == 1),
    "YY--Y": WordipelagoLocationData(region="YellowChecks", address=325, lambda world: world.options.yellow_checks == 1),
    "YY-Y-": WordipelagoLocationData(region="YellowChecks", address=326, lambda world: world.options.yellow_checks == 1),
    "YY-YY": WordipelagoLocationData(region="YellowChecks", address=327, lambda world: world.options.yellow_checks == 1),
    "YYY--": WordipelagoLocationData(region="YellowChecks", address=328, lambda world: world.options.yellow_checks == 1),
    "YYY-Y": WordipelagoLocationData(region="YellowChecks", address=329, lambda world: world.options.yellow_checks == 1),
    "YYYY-": WordipelagoLocationData(region="YellowChecks", address=330, lambda world: world.options.yellow_checks == 1),
    "YYYYY": WordipelagoLocationData(region="YellowChecks", address=331, lambda world: world.options.yellow_checks == 1),
}

def get_location_table():
    location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
    for i in range(1000):
        location_table["Word " + str(i + 1)] = 1001 + i
    return location_table

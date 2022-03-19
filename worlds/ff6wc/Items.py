from BaseClasses import Item
import typing
from typing import Dict

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


item_table: Dict[str, ItemData] = {
    'TERRA': ItemData(501, True),
    'LOCKE': ItemData(502, True),
    'CYAN': ItemData(503, True),
    'SHADOW': ItemData(504, True),
    'EDGAR': ItemData(505, True),
    'SABIN': ItemData(506, True),
    'CELES': ItemData(507, True),
    'STRAGO': ItemData(508, True),
    'RELM': ItemData(509, True),
    'SETZER': ItemData(510, True),
    'MOG': ItemData(511, True),
    'GAU': ItemData(512, True),
    'GOGO': ItemData(513, True),
    'UMARO': ItemData(514, True),
    'Ramuh': ItemData(601, True),
    'Ifrit': ItemData(602, True),
    'Shiva': ItemData(603, True),
    'Siren': ItemData(604, True),
    'Terrato': ItemData(605, True),
    'Shoat': ItemData(606, True),
    'Maduin': ItemData(607, True),
    'Bismark': ItemData(608, True),
    'Stray': ItemData(609, True),
    'Palidor': ItemData(610, True),
    'Tritoch': ItemData(611, True),
    'Odin': ItemData(612, True),
    'Raiden': ItemData(613, True),
    'Bahamut': ItemData(614, True),
    'Alexandr': ItemData(615, True),
    'Crusader': ItemData(616, True),
    'Ragnarok': ItemData(617, True),
    'Kirin': ItemData(618, True),
    'ZoneSeek': ItemData(619, True),
    'Carbunkl': ItemData(620, True),
    'Phantom': ItemData(621, True),
    'Sraphim': ItemData(622, True),
    'Golem': ItemData(623, True),
    'Unicorn': ItemData(624, True),
    'Fenrir': ItemData(625, True),
    'Starlet': ItemData(626, True),
    'Phoenix': ItemData(627, True),
    'Junk': ItemData(628, False)
}
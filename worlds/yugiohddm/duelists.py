import typing

from enum import Enum
from .utils import Constants


class Duelist(Enum):

    def __init__(self, _id: int, _name: str, bitflag: int, is_yami_yugi: bool = False):
        self.id: int =_id
        self._name: str = _name
        self.bitflag: int = bitflag
        self.is_yami_yugi: bool = is_yami_yugi
        self.wins_address: int = Constants.DUEL_WINS_OFFSET + (self.id - 1) * 2
    
    def __str__(self):
        return self._name
    
    GRANDPA = (7, "Grandpa", 1 << 0)
    DEMITRIUS_THE_BULLY = (6, "Demitrius the Bully", 1 << 1)
    TEA_GARDNER = (5, "Tea Gardner", 1 << 2)
    TRISTAN_TAYLOR = (4, "Tristan Taylor", 1 << 3)
    JOEY_WHEELER = (3, "Joey Wheeler", 1 << 4)
    YUGI_MOTO = (2, "Yugi Moto", 1 << 5)
    YAMI_YUGI = (1, "Yami Yugi", 1 << 6, True)
    # 1 << 7 unused
    MISS_MADUSA = (15, "Miss Madusa", 1 << 8)
    KREIGER = (14, "Kreiger", 1 << 9)
    FORTUNO = (13, "Fortuno", 1 << 10)
    JACKPOT = (12, "Jackpot", 1 << 11)
    FENDER_SHRILL = (11, "Fender Shrill", 1 << 12)
    LINT_GREENDALE = (10, "Lint Greendale", 1 << 13)
    DIRECTOR_LUCIUS = (9, "Director Lucius", 1 << 14)
    AD_ARCHIE = (8, "AD Archie", 1 << 15)
    KANE_MINION_B = (23, "Kane Minion B", 1 << 16)
    KANE_MINION_A = (22, "Kane Minion A", 1 << 17)
    DIESEL_KANE = (21, "Diesel Kane", 1 << 18)
    SETO_KAIBA = (20, "Seto Kaiba", 1 << 19)
    VENOM_C = (19, "Venom C", 1 << 20)
    VENOM_B = (18, "Venom B", 1 << 21)
    VENOM_A = (17, "Venom A", 1 << 22)
    SCORPION_SHOES_OWNER = (16, "Scorpion Shoes Owner", 1 << 23)
    BELUGA = (31, "Beluga", 1 << 24)
    PROFESSOR_JEREMY_HARRISON = (30, "Professor Jeremy Harrison", 1 << 25)
    SHADI = (29, "Shadi", 1 << 26)
    CURATOR_ADRIEL_WAINWRIGHT = (28, "Curator Adriel Wainwright", 1 << 27)
    KANE_MINION_F = (27, "Kane Minion F", 1 << 28)
    KANE_MINION_E = (26, "Kane Minion E", 1 << 29)
    KANE_MINION_D = (25, "Kane Minion D", 1 << 30)
    KANE_MINION_C = (24, "Kane Minion C", 1 << 31)
    CEDRIC = (39, "Cedric", 1 << 32)
    FENG_LONG = (38, "Feng Long", 1 << 33)
    MOKUBA_KAIBA = (37, "Mokuba Kaiba", 1 << 34)
    EGGER_BALDWIN = (36, "Egger Baldwin", 1 << 35)
    THUG_C = (35, "Thug C", 1 << 36)
    THUG_B = (34, "Thug B", 1 << 37)
    THUG_A = (33, "Thug A", 1 << 38)
    THE_GREENDALE_ZOMPIRE = (32, "The Greendale Zompire", 1 << 39)
    STRINGER = (47, "Stringer", 1 << 40)
    GAME_SHOW_PRODUCER = (46, "Game Show Producer", 1 << 41)
    ANTON_PERIWIG = (45, "Anton Periwig", 1 << 42)
    CHOPMAN = (44, "Chopman", 1 << 43)
    KAIBAS_BUTLER = (43, "Kaibas' Butler", 1 << 44)
    SNIPES_CROSSHAIR = (42, "Snipes Crosshair", 1 << 45)
    BICKFORD_GAGE = (41, "Bickford Gage", 1 << 46)
    CHARLIE_GALE = (40, "Charlie Gale", 1 << 47)
    REX_RAPTOR = (55, "Rex Raptor", 1 << 48)
    WEEVIL_UNDERWOOD = (54, "Weevil Underwood", 1 << 49)
    YAMI_BAKURA = (53, "Yami Bakura", 1 << 50)
    MR_TITUS = (52, "Mr. Titus", 1 << 51)
    BAKURA = (51, "Bakura", 1 << 52)
    NIBBLES = (50, "Nibbles", 1 << 53)
    DAMIEN_DRACO = (49, "Damien Draco", 1 << 54)
    TICK_TOCK = (48, "Tick-Tock", 1 << 55)
    PARA = (63, "Para", 1 << 56)
    PANIK = (62, "Panik", 1 << 57)
    THE_PUPPETEER = (61, "The Puppeteer", 1 << 58)
    MAKO_TSUNAMI = (60, "Mako Tsunami", 1 << 59)
    MAI_VALENTINE = (59, "Mai Valentine", 1 << 60)
    MELODY = (58, "Melody", 1 << 61)
    SERENITY_WHEELER = (57, "Serenity Wheeler", 1 << 62)
    MAXIMILLION_PEGASUS = (56, "Maximillion Pegasus", 1 << 63)
    ESPA_ROBA = (71, "Espa Roba", 1 << 64)
    BONZ = (70, "Bonz", 1 << 65)
    SINDIN_THE_CLOWN = (69, "Sindin the Clown", 1 << 66)
    DUKE_DEVLIN = (68, "Duke Devlin", 1 << 67)
    BANDIT_KEITH = (67, "Bandit Keith", 1 << 68)
    KEMO = (66, "Kemo", 1 << 69)
    CROQUET = (65, "Croquet", 1 << 70)
    DOX = (64, "Dox", 1 << 71)
    THE_MERCHANT = (79, "The Merchant", 1 << 72)
    STRINGS = (78, "Strings", 1 << 73)
    ARKANA = (77, "Arkana", 1 << 74)
    MARIK_ISHTAR = (76, "Marik Ishtar", 1 << 75)
    YUGIS_MOTHER = (75, "Yugi's Mother", 1 << 76)
    JOHNNY_STEPS = (74, "Johnny Steps", 1 << 77)
    SEEKER = (73, "Seeker", 1 << 78)
    ISHIZU_ISHTAR = (72, "Ishizu Ishtar", 1 << 79)
    ROGER = (87, "Roger", 1 << 80)
    LLOYD = (86, "Lloyd", 1 << 81)
    NORMAN = (85, "Norman", 1 << 82)
    # 1 << 83 unused?
    ODION = (83, "Odion", 1 << 84)
    UMBRA = (82, "Umbra", 1 << 85)
    LUMIS = (81, "Lumis", 1 << 86)
    PARADOX = (80, "Paradox", 1 << 87)
    # 1 << 88 unused
    # 1 << 89 unused
    DORIS = (93, "Doris", 1 << 90)
    JILL = (92, "Jill", 1 << 91)
    RYAN = (91, "Ryan", 1 << 92)
    PAUL = (90, "Paul", 1 << 93)
    DIANA = (89, "Diana", 1 << 94)
    ANDREA = (88, "Andrea", 1 << 95)

all_duelists: typing.List[Duelist] = [d for d in Duelist]
all_duelists_test: typing.List[typing.Tuple[Duelist, ...]] = [(Duelist.YAMI_YUGI, Duelist.YUGI_MOTO)]
    
def get_duelist_defeat_location_name(duelist: Duelist) -> str:
    return f"{duelist} defeated"

ids_to_duelists: typing.Dict[int, Duelist] = {duelist.id: duelist for duelist in Duelist}

#def map_duelists_to_ids(
#    duelists: typing.Iterable[typing.Tuple[Duelist, ...]]
#) -> typing.Tuple[typing.Tuple[int, ...], ...]:
#    """Converts tuples of Duelist objects to ids to send in the slot data."""
#    return tuple(tuple(duelist.id for duelist in t) for t in duelists)
def map_duelists_to_ids(
    duelists: typing.List[Duelist]
) -> typing.Tuple[int, ...]:
    """Converts tuples of Duelist objects to ids to send in the slot data."""
    return tuple(duelist.id for duelist in duelists)



def map_ids_to_duelists(
    ids: typing.Iterable[typing.Tuple[int, ...]]
) -> typing.Tuple[typing.Tuple[Duelist, ...], ...]:
    """Takes tuples of ids from the slot data and converts them back to Duelist objects."""
    return tuple(tuple(ids_to_duelists[id] for id in t) for t in ids)

name_to_duelist = {duelist.name: duelist for duelist in all_duelists}

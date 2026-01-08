import typing

from enum import Enum


NUMBER_OF_WINS_OFFSET: typing.Final[int] = 0x1D0720
UNLOCK_OFFSET: typing.Final[int] = 0x1D06F4
LATEGAME_DUELIST_UNLOCK_OFFSET: typing.Final[int] = 0x1D06F8


class Duelist(Enum):
    # PSX RAM notes (memory addresses are from Bizhawk's MainRAM domain): DataCrystal is wrong; Free Duel unlock
    # progress is a 5-byte (not 4) bitfield starting at 0x1D06F4. The 5th byte represents duelists Seto 2nd through
    # Nitemare. Duel Master K is the only duelist without a flag and is always unlocked.
    #
    # 1 << 7 is intentionally missing; this value would correspond to the "Build Deck" slot, so it seems the developers
    # skipped it for convenience.
    #
    # In searching for the "Number of Wins" bytes for each duelist, I noticed 0x1D0258 and 0x1D02B8 were also
    # incremented at the end of duels. Perhaps these addresses are for total Free Duels and total wins (even though
    # these value don't seem used anywhere in the game, though I didn't attach any watches to these addresses to find
    # out).
    #
    # Each duelist's number of wins and losses are stored in 2 2-byte integer (losses first, then wins) starting at
    # 0x1D0720 for Simon Muran and continuing left to right, top to bottom, in the Free Duel screen. The number of wins
    # displays properly up to 999, after which only the tens and ones digits are displayed. At very large values (I
    # tried 0xFFFF), nothing is displayed at all for the number.
    SIMON_MURAN = (1, 5, "Simon Muran", 1 << 6)
    TEANA = (2, 5, "Teana", 1 << 5)
    JONO = (3, 5, "Jono", 1 << 4)
    VILLAGER1 = (4, 5, "Villager1", 1 << 3)
    VILLAGER2 = (5, 5, "Villager2", 1 << 2)
    VILLAGER3 = (6, 5, "Villager3", 1 << 1)
    SETO = (7, 10, "Seto", 1 << 0)
    HEISHIN = (8, 20, "Heishin", 1 << 15)
    REX_RAPTOR = (9, 8, "Rex Raptor", 1 << 14)
    WEEVIL_UNDERWOOD = (10, 8, "Weevil Underwood", 1 << 13)
    MAI_VALENTINE = (11, 10, "Mai Valentine", 1 << 12)
    BANDIT_KEITH = (12, 12, "Bandit Keith", 1 << 11)
    SHADI = (13, 12, "Shadi", 1 << 10)
    YAMI_BAKURA = (14, 14, "Yami Bakura", 1 << 9)
    PEGASUS = (15, 16, "Pegasus", 1 << 8)
    ISIS = (16, 16, "Isis", 1 << 23)
    KAIBA = (17, 16, "Kaiba", 1 << 22)
    MAGE_SOLDIER = (18, 12, "Mage Soldier", 1 << 21)
    JONO_2ND = (19, 10, "Jono 2nd", 1 << 20)
    TEANA_2ND = (20, 10, "Teana 2nd", 1 << 19)
    OCEAN_MAGE = (21, 14, "Ocean Mage", 1 << 18)
    HIGH_MAGE_SECMETON = (22, 16, "High Mage Secmeton", 1 << 17)
    FOREST_MAGE = (23, 14, "Forest Mage", 1 << 16)
    # For some reason, when Anubisius's flag is set, Bizhawk's memory-changed counter increments every frame, but the
    # value doesn't change.
    HIGH_MAGE_ANUBISIUS = (24, 16, "High Mage Anubisius", 1 << 31)
    MOUNTAIN_MAGE = (25, 14, "Mountain Mage", 1 << 30)
    HIGH_MAGE_ATENZA = (26, 16, "High Mage Atenza", 1 << 29)
    DESERT_MAGE = (27, 14, "Desert Mage", 1 << 28)
    HIGH_MAGE_MARTIS = (28, 16, "High Mage Martis", 1 << 27)
    MEADOW_MAGE = (29, 14, "Meadow Mage", 1 << 26)
    HIGH_MAGE_KEPURA = (30, 16, "High Mage Kepura", 1 << 25)
    LABYRINTH_MAGE = (31, 16, "Labyrinth Mage", 1 << 24)
    SETO_2ND = (32, 18, "Seto 2nd", 1 << 7, True)
    GUARDIAN_SEBEK = (33, 20, "Guardian Sebek", 1 << 6, True, True)
    GUARDIAN_NEKU = (34, 20, "Guardian Neku", 1 << 5, True, True)
    HEISHIN_2ND = (35, 20, "Heishin 2nd", 1 << 4, True, True)
    SETO_3RD = (36, 20, "Seto 3rd", 1 << 3, True, True)
    DARKNITE = (37, 20, "DarkNite", 1 << 2, True, True)
    NITEMARE = (38, 20, "Nitemare", 1 << 1, True, True)
    DUEL_MASTER_K = (39, 15, "Duel Master K", 0)

    def __init__(self, _id: int, hand_size: int, _name: str, bitflag: int, is_5th_byte: bool = False,
                 is_final_6: bool = False):
        self.id: int = _id
        self.hand_size: int = hand_size
        self._name: str = _name
        self.is_5th_byte: bool = is_5th_byte
        self.bitflag: int = bitflag
        self.is_final_6: bool = is_final_6
        self.wins_address: int = NUMBER_OF_WINS_OFFSET + (self.id - 1) * 4

    def __str__(self):
        return self._name


def get_duelist_defeat_location_name(duelist: Duelist) -> str:
    return f"{duelist} defeated"


ids_to_duelists: typing.Dict[int, Duelist] = {duelist.id: duelist for duelist in Duelist}


def map_duelists_to_ids(
    duelists: typing.Iterable[typing.Tuple[Duelist, ...]]
) -> typing.Tuple[typing.Tuple[int, ...], ...]:
    """Converts tuples of Duelist objects to ids to send in the slot data."""
    return tuple(tuple(duelist.id for duelist in t) for t in duelists)


def map_ids_to_duelists(
    ids: typing.Iterable[typing.Tuple[int, ...]]
) -> typing.Tuple[typing.Tuple[Duelist, ...], ...]:
    """Takes tuples of ids from the slot data and converts them back to Duelist objects."""
    return tuple(tuple(ids_to_duelists[id] for id in t) for t in ids)


mage_pairs: typing.Tuple[typing.Tuple[Duelist, Duelist], ...] = (
    (Duelist.OCEAN_MAGE, Duelist.HIGH_MAGE_SECMETON),
    (Duelist.FOREST_MAGE, Duelist.HIGH_MAGE_ANUBISIUS),
    (Duelist.MOUNTAIN_MAGE, Duelist.HIGH_MAGE_ATENZA),
    (Duelist.DESERT_MAGE, Duelist.HIGH_MAGE_MARTIS),
    (Duelist.MEADOW_MAGE, Duelist.HIGH_MAGE_KEPURA)
)

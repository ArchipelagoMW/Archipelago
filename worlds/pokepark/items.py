from dataclasses import dataclass, field
from typing import Optional, NamedTuple

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


@dataclass()
class PokeparkBaseItemClientData:
    opcode: int = field(init=False)
    parameter1: int
    parameter2: int = 1
    flag_name: bytes = b''
    flag_address: int = 0x80001860


class PokeparkItemData(NamedTuple):
    type: str
    classification: IC
    code: Optional[int]
    quantity: int
    client_data: Optional[PokeparkBaseItemClientData]


@dataclass
class PokeparkFriendshipItemClientData(PokeparkBaseItemClientData):
    def __post_init__(self):
        self.opcode = 0x3c  # friendship opcode


@dataclass
class PokeparkPasswordItemClientData(PokeparkBaseItemClientData):
    def __post_init__(self):
        self.opcode = 0xb7  # friendship opcode


@dataclass
class PokeparkFlagItemClientData(PokeparkBaseItemClientData):
    def __post_init__(self):
        self.opcode = 0x0


@dataclass
class PokeparkUnlockItemClientData(PokeparkBaseItemClientData):
    def __post_init__(self):
        self.opcode = 0x28  # unlock Pokemon opcode


@dataclass
class PokeparkPowerItemClientData(PokeparkBaseItemClientData):
    def __post_init__(self):
        self.opcode = 0xb9  # activate Power opcode


@dataclass
class PokeparkPrismaItemClientData(PokeparkBaseItemClientData):
    def __post_init__(self):
        self.opcode = 0x52  # set Prisma opcode


@dataclass
class PokeparkBerryItemClientData(PokeparkBaseItemClientData):
    def __post_init__(self):
        self.opcode = 0xa  # set Berry opcode


class PokeparkItem(Item):
    game: str = "PokePark"
    type: Optional[str]

    def __init__(self, name: str, player: int, data: PokeparkItemData, classification: Optional[IC] = None) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else PokeparkItem.get_apid(data.code),
            player,
        )

        self.type = data.type
        self.client_data = data.client_data

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item code.

        :param code: The unique code for the item.
        :return: The computed Archipelago ID.
        """
        base_id: int = 10000
        return base_id + code


def generate_flagname(flag: str) -> bytes:
    return flag.encode('ascii') + b'\x00'

ITEM_TABLE: dict[str, PokeparkItemData] = {
    "Chatot Friendship": PokeparkItemData(
        "Item", IC.progression, 0, 1, PokeparkFriendshipItemClientData(
            parameter1=0x4,
        )
    ),
    "Chikorita Friendship": PokeparkItemData(
        "Item", IC.progression, 1, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb6,
        )
    ),
    "Turtwig Friendship": PokeparkItemData(
        "Item", IC.progression, 2, 1, PokeparkFriendshipItemClientData(
            parameter1=0x8,
        )
    ),
    "Torterra Friendship": PokeparkItemData(
        "Item", IC.progression, 3, 1, PokeparkFriendshipItemClientData(
            parameter1=0x2d,
        )
    ),
    "Buneary Friendship": PokeparkItemData(
        "Item", IC.progression, 4, 1, PokeparkFriendshipItemClientData(
            parameter1=0x9,
        )
    ),
    "Munchlax Friendship": PokeparkItemData(
        "Item", IC.progression, 5, 1, PokeparkFriendshipItemClientData(
            parameter1=0x13,
        )
    ),
    "Treecko Friendship": PokeparkItemData(
        "Item", IC.progression, 6, 1, PokeparkFriendshipItemClientData(
            parameter1=0x38,
        )
    ),
    "Mankey Friendship": PokeparkItemData(
        "Item", IC.progression, 7, 1, PokeparkFriendshipItemClientData(
            parameter1=0x21,
        )
    ),
    "Bidoof Friendship": PokeparkItemData(
        "Item", IC.progression, 8, 1, PokeparkFriendshipItemClientData(
            parameter1=0x12,
        )
    ),
    "Bibarel Friendship": PokeparkItemData(
        "Item", IC.progression, 9, 1, PokeparkFriendshipItemClientData(
            parameter1=0x2f,
        )
    ),
    "Oddish Friendship": PokeparkItemData(
        "Item", IC.progression, 10, 1, PokeparkFriendshipItemClientData(
            parameter1=0x22,
        )
    ),
    "Aipom Friendship": PokeparkItemData(
        "Item", IC.progression, 11, 1, PokeparkFriendshipItemClientData(
            parameter1=0xf,
        )
    ),
    "Ambipom Friendship": PokeparkItemData(
        "Item", IC.progression, 12, 1, PokeparkFriendshipItemClientData(
            parameter1=0xe,
        )
    ),
    "Leafeon Friendship": PokeparkItemData(
        "Item", IC.progression, 13, 1, PokeparkFriendshipItemClientData(
            parameter1=0x50,
        )
    ),
    "Spearow Friendship": PokeparkItemData(
        "Item", IC.progression, 14, 1, PokeparkFriendshipItemClientData(
            parameter1=0x8f,
        )
    ),
    "Croagunk Friendship": PokeparkItemData(
        "Item", IC.progression, 15, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb,
        )
    ),
    "Starly Friendship": PokeparkItemData(
        "Item", IC.progression, 16, 1, PokeparkFriendshipItemClientData(
            parameter1=0x2e,
        )
    ),
    "Bonsly Friendship": PokeparkItemData(
        "Item", IC.progression, 17, 1, PokeparkFriendshipItemClientData(
            parameter1=0x10,
        )
    ),
    "Sudowoodo Friendship": PokeparkItemData(
        "Item", IC.progression, 18, 1, PokeparkFriendshipItemClientData(
            parameter1=0x6b,
        )
    ),
    "Pachirisu Friendship": PokeparkItemData(
        "Item", IC.progression, 19, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa,
        )
    ),
    "Lotad Friendship": PokeparkItemData(
        "Item", IC.progression, 20, 1, PokeparkFriendshipItemClientData(
            parameter1=0x19,
        )
    ),
    "Shinx Friendship": PokeparkItemData(
        "Item", IC.progression, 21, 1, PokeparkFriendshipItemClientData(
            parameter1=0xae,
        )
    ),
    "Scyther Friendship": PokeparkItemData(
        "Item", IC.progression, 22, 1, PokeparkFriendshipItemClientData(
            parameter1=0x45,
        )
    ),
    "Magikarp Friendship": PokeparkItemData(
        "Item", IC.progression, 23, 1, PokeparkFriendshipItemClientData(
            parameter1=0x2b,
        )
    ),
    "Caterpie Friendship": PokeparkItemData(
        "Item", IC.progression, 24, 1, PokeparkFriendshipItemClientData(
            parameter1=0x27,
        )
    ),
    "Butterfree Friendship": PokeparkItemData(
        "Item", IC.progression, 25, 1, PokeparkFriendshipItemClientData(
            parameter1=0x8e,
        )
    ),
    "Weedle Friendship": PokeparkItemData(
        "Item", IC.progression, 26, 1, PokeparkFriendshipItemClientData(
            parameter1=0x28,
        )
    ),
    "Shroomish Friendship": PokeparkItemData(
        "Item", IC.progression, 27, 1, PokeparkFriendshipItemClientData(
            parameter1=0x26,
        )
    ),
    "Tropius Friendship": PokeparkItemData(
        "Item", IC.progression, 28, 1, PokeparkFriendshipItemClientData(
            parameter1=0x29,
        )
    ),
    "Bulbasaur Friendship": PokeparkItemData(
        "Item", IC.progression, 29, 1, PokeparkFriendshipItemClientData(
            parameter1=0x39,
        )
    ),
    "Venusaur Friendship": PokeparkItemData(
        "Item", IC.progression, 30, 1, PokeparkFriendshipItemClientData(
            parameter1=0x68,
        )
    ),
    "Piplup Friendship": PokeparkItemData(
        "Item", IC.progression, 31, 1, PokeparkFriendshipItemClientData(
            parameter1=0x6,
        )
    ),
    "Slowpoke Friendship": PokeparkItemData(
        "Item", IC.progression, 32, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa1,
        )
    ),
    "Azurill Friendship": PokeparkItemData(
        "Item", IC.progression, 33, 1, PokeparkFriendshipItemClientData(
            parameter1=0x42,
        )
    ),
    "Corsola Friendship": PokeparkItemData(
        "Item", IC.progression, 34, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb8,
        )
    ),
    "Wynaut Friendship": PokeparkItemData(
        "Item", IC.progression, 35, 1, PokeparkFriendshipItemClientData(
            parameter1=0x1d,
        )
    ),
    "Carvanha Friendship": PokeparkItemData(
        "Item", IC.progression, 36, 1, PokeparkFriendshipItemClientData(
            parameter1=0x7f,
        )
    ),
    "Sharpedo Friendship": PokeparkItemData(
        "Item", IC.progression, 37, 1, PokeparkFriendshipItemClientData(
            parameter1=0x80,
        )
    ),
    "Wailord Friendship": PokeparkItemData(
        "Item", IC.progression, 38, 1, PokeparkFriendshipItemClientData(
            parameter1=0x78,
        )
    ),
    "Totodile Friendship": PokeparkItemData(
        "Item", IC.progression, 39, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb4,
        )
    ),
    "Feraligatr Friendship": PokeparkItemData(
        "Item", IC.progression, 40, 1, PokeparkFriendshipItemClientData(
            parameter1=0x30,
        )
    ),
    "Lapras Friendship": PokeparkItemData(
        "Item", IC.progression, 41, 1, PokeparkFriendshipItemClientData(
            parameter1=0x9e,
        )
    ),
    "Psyduck Friendship": PokeparkItemData(
        "Item", IC.progression, 42, 1, PokeparkFriendshipItemClientData(
            parameter1=0xac,
        )
    ),
    "Golduck Friendship": PokeparkItemData(
        "Item", IC.progression, 43, 1, PokeparkFriendshipItemClientData(
            parameter1=0x33,
        )
    ),
    "Buizel Friendship": PokeparkItemData(
        "Item", IC.progression, 44, 1, PokeparkFriendshipItemClientData(
            parameter1=0xd,
        )
    ),
    "Floatzel Friendship": PokeparkItemData(
        "Item", IC.progression, 45, 1, PokeparkFriendshipItemClientData(
            parameter1=0x7e,
        )
    ),
    "Vaporeon Friendship": PokeparkItemData(
        "Item", IC.progression, 46, 1, PokeparkFriendshipItemClientData(
            parameter1=0x4b,
        )
    ),
    "Mudkip Friendship": PokeparkItemData(
        "Item", IC.progression, 47, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb3,
        )
    ),
    "Taillow Friendship": PokeparkItemData(
        "Item", IC.progression, 48, 1, PokeparkFriendshipItemClientData(
            parameter1=0xad,
        )
    ),
    "Staravia Friendship": PokeparkItemData(
        "Item", IC.progression, 49, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc,
        )
    ),
    "Pidgeotto Friendship": PokeparkItemData(
        "Item", IC.progression, 50, 1, PokeparkFriendshipItemClientData(
            parameter1=0x90,
        )
    ),
    "Krabby Friendship": PokeparkItemData(
        "Item", IC.progression, 51, 1, PokeparkFriendshipItemClientData(
            parameter1=0x5b,
        )
    ),
    "Corphish Friendship": PokeparkItemData(
        "Item", IC.progression, 52, 1, PokeparkFriendshipItemClientData(
            parameter1=0x23,
        )
    ),
    "Blastoise Friendship": PokeparkItemData(
        "Item", IC.progression, 53, 1, PokeparkFriendshipItemClientData(
            parameter1=0x2a,
        )
    ),
    "Wingull Friendship": PokeparkItemData(
        "Item", IC.progression, 54, 1, PokeparkFriendshipItemClientData(
            parameter1=0x59,
        )
    ),
    "Pelipper Friendship": PokeparkItemData(
        "Item", IC.progression, 55, 1, PokeparkFriendshipItemClientData(
            parameter1=0x5a,
        )
    ),
    "Gyarados Friendship": PokeparkItemData(
        "Item", IC.progression, 56, 1, PokeparkFriendshipItemClientData(
            parameter1=0x35,
        )
    ),
    "Glalie Friendship": PokeparkItemData(
        "Item", IC.progression, 57, 1, PokeparkFriendshipItemClientData(
            parameter1=0x82,
        )
    ),
    "Froslass Friendship": PokeparkItemData(
        "Item", IC.progression, 58, 1, PokeparkFriendshipItemClientData(
            parameter1=0x51,
        )
    ),
    "Piloswine Friendship": PokeparkItemData(
        "Item", IC.progression, 59, 1, PokeparkFriendshipItemClientData(
            parameter1=0x56,
        )
    ),
    "Mamoswine Friendship": PokeparkItemData(
        "Item", IC.progression, 60, 1, PokeparkFriendshipItemClientData(
            parameter1=0x83,
        )
    ),
    "Teddiursa Friendship": PokeparkItemData(
        "Item", IC.progression, 61, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa2,
        )
    ),
    "Ursaring Friendship": PokeparkItemData(
        "Item", IC.progression, 62, 1, PokeparkFriendshipItemClientData(
            parameter1=0x86,
        )
    ),
    "Kirlia Friendship": PokeparkItemData(
        "Item", IC.progression, 63, 1, PokeparkFriendshipItemClientData(
            parameter1=0x7a,
        )
    ),
    "Spheal Friendship": PokeparkItemData(
        "Item", IC.progression, 64, 1, PokeparkFriendshipItemClientData(
            parameter1=0x6c,
        )
    ),
    "Quagsire Friendship": PokeparkItemData(
        "Item", IC.progression, 65, 1, PokeparkFriendshipItemClientData(
            parameter1=0x69,
        )
    ),
    "Glaceon Friendship": PokeparkItemData(
        "Item", IC.progression, 66, 1, PokeparkFriendshipItemClientData(
            parameter1=0x4c,
        )
    ),
    "Octillery Friendship": PokeparkItemData(
        "Item", IC.progression, 67, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc7,
        )
    ),
    "Delibird Friendship": PokeparkItemData(
        "Item", IC.progression, 68, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc6,
        )
    ),
    "Primeape Friendship": PokeparkItemData(
        "Item", IC.progression, 69, 1, PokeparkFriendshipItemClientData(
            parameter1=0x54,
        )
    ),
    "Squirtle Friendship": PokeparkItemData(
        "Item", IC.progression, 70, 1, PokeparkFriendshipItemClientData(
            parameter1=0x2c,
        )
    ),
    "Smoochum Friendship": PokeparkItemData(
        "Item", IC.progression, 71, 1, PokeparkFriendshipItemClientData(
            parameter1=0x16,
        )
    ),
    "Sneasel Friendship": PokeparkItemData(
        "Item", IC.progression, 72, 1, PokeparkFriendshipItemClientData(
            parameter1=0x81,
        )
    ),
    "Prinplup Friendship": PokeparkItemData(
        "Item", IC.progression, 73, 1, PokeparkFriendshipItemClientData(
            parameter1=0x6d,
        )
    ),
    "Empoleon Friendship": PokeparkItemData(
        "Item", IC.progression, 74, 1, PokeparkFriendshipItemClientData(
            parameter1=0x3b,
        )
    ),
    "Mr. Mime Friendship": PokeparkItemData(
        "Item", IC.progression, 75, 1, PokeparkFriendshipItemClientData(
            parameter1=0x84,
        )
    ),
    "Mawile Friendship": PokeparkItemData(
        "Item", IC.progression, 76, 1, PokeparkFriendshipItemClientData(
            parameter1=0x53,
        )
    ),
    "Aron Friendship": PokeparkItemData(
        "Item", IC.progression, 77, 1, PokeparkFriendshipItemClientData(
            parameter1=0x1f,
        )
    ),
    "Gible Friendship": PokeparkItemData(
        "Item", IC.progression, 78, 1, PokeparkFriendshipItemClientData(
            parameter1=0x1c,
        )
    ),
    "Marowak Friendship": PokeparkItemData(
        "Item", IC.progression, 79, 1, PokeparkFriendshipItemClientData(
            parameter1=0x70,
        )
    ),
    "Zubat Friendship": PokeparkItemData(
        "Item", IC.progression, 80, 1, PokeparkFriendshipItemClientData(
            parameter1=0x5c,
        )
    ),
    "Golbat Friendship": PokeparkItemData(
        "Item", IC.progression, 81, 1, PokeparkFriendshipItemClientData(
            parameter1=0x95,
        )
    ),
    "Diglett Friendship": PokeparkItemData(
        "Item", IC.progression, 82, 1, PokeparkFriendshipItemClientData(
            parameter1=0x34,
        )
    ),
    "Dugtrio Friendship": PokeparkItemData(
        "Item", IC.progression, 83, 1, PokeparkFriendshipItemClientData(
            parameter1=0x64,
        )
    ),
    "Snorlax Friendship": PokeparkItemData(
        "Item", IC.progression, 84, 1, PokeparkFriendshipItemClientData(
            parameter1=0x99,
        )
    ),
    "Geodude Friendship": PokeparkItemData(
        "Item", IC.progression, 85, 1, PokeparkFriendshipItemClientData(
            parameter1=0x5d,
        )
    ),
    "Machamp Friendship": PokeparkItemData(
        "Item", IC.progression, 86, 1, PokeparkFriendshipItemClientData(
            parameter1=0x71,
        )
    ),
    "Meowth Friendship": PokeparkItemData(
        "Item", IC.progression, 87, 1, PokeparkFriendshipItemClientData(
            parameter1=0x7d,
        )
    ),
    "Scizor Friendship": PokeparkItemData(
        "Item", IC.progression, 88, 1, PokeparkFriendshipItemClientData(
            parameter1=0x47,
        )
    ),
    "Cranidos Friendship": PokeparkItemData(
        "Item", IC.progression, 89, 1, PokeparkFriendshipItemClientData(
            parameter1=0x6e,
        )
    ),
    "Phanpy Friendship": PokeparkItemData(
        "Item", IC.progression, 90, 1, PokeparkFriendshipItemClientData(
            parameter1=0x25,
        )
    ),
    "Raichu Friendship": PokeparkItemData(
        "Item", IC.progression, 91, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa7,
        )
    ),
    "Magnemite Friendship": PokeparkItemData(
        "Item", IC.progression, 92, 1, PokeparkFriendshipItemClientData(
            parameter1=0x18,
        )
    ),
    "Magnezone Friendship": PokeparkItemData(
        "Item", IC.progression, 93, 1, PokeparkFriendshipItemClientData(
            parameter1=0x97,
        )
    ),
    "Hitmonlee Friendship": PokeparkItemData(
        "Item", IC.progression, 94, 1, PokeparkFriendshipItemClientData(
            parameter1=0xaa,
        )
    ),
    "Electivire Friendship": PokeparkItemData(
        "Item", IC.progression, 95, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb2,
        )
    ),
    "Bastiodon Friendship": PokeparkItemData(
        "Item", IC.progression, 96, 1, PokeparkFriendshipItemClientData(
            parameter1=0x85,
        )
    ),
    "Charmander Friendship": PokeparkItemData(
        "Item", IC.progression, 97, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb5,
        )
    ),
    "Hitmontop Friendship": PokeparkItemData(
        "Item", IC.progression, 98, 1, PokeparkFriendshipItemClientData(
            parameter1=0xaf,
        )
    ),
    "Hitmonchan Friendship": PokeparkItemData(
        "Item", IC.progression, 99, 1, PokeparkFriendshipItemClientData(
            parameter1=0xab,
        )
    ),
    "Camerupt Friendship": PokeparkItemData(
        "Item", IC.progression, 100, 1, PokeparkFriendshipItemClientData(
            parameter1=0x6f,
        )
    ),
    "Chimchar Friendship": PokeparkItemData(
        "Item", IC.progression, 101, 1, PokeparkFriendshipItemClientData(
            parameter1=0x7,
        )
    ),
    "Infernape Friendship": PokeparkItemData(
        "Item", IC.progression, 102, 1, PokeparkFriendshipItemClientData(
            parameter1=0x66,
        )
    ),
    "Vulpix Friendship": PokeparkItemData(
        "Item", IC.progression, 103, 1, PokeparkFriendshipItemClientData(
            parameter1=0x87,
        )
    ),
    "Ninetales Friendship": PokeparkItemData(
        "Item", IC.progression, 104, 1, PokeparkFriendshipItemClientData(
            parameter1=0x52,
        )
    ),
    "Farfetch'd Friendship": PokeparkItemData(
        "Item", IC.progression, 105, 1, PokeparkFriendshipItemClientData(
            parameter1=0x55,
        )
    ),
    "Meditite Friendship": PokeparkItemData(
        "Item", IC.progression, 106, 1, PokeparkFriendshipItemClientData(
            parameter1=0x20,
        )
    ),
    "Magby Friendship": PokeparkItemData(
        "Item", IC.progression, 107, 1, PokeparkFriendshipItemClientData(
            parameter1=0x15,
        )
    ),
    "Magmortar Friendship": PokeparkItemData(
        "Item", IC.progression, 108, 1, PokeparkFriendshipItemClientData(
            parameter1=0x76,
        )
    ),
    "Flareon Friendship": PokeparkItemData(
        "Item", IC.progression, 109, 1, PokeparkFriendshipItemClientData(
            parameter1=0x4a,
        )
    ),
    "Magcargo Friendship": PokeparkItemData(
        "Item", IC.progression, 110, 1, PokeparkFriendshipItemClientData(
            parameter1=0x58,
        )
    ),
    "Torkoal Friendship": PokeparkItemData(
        "Item", IC.progression, 111, 1, PokeparkFriendshipItemClientData(
            parameter1=0x57,
        )
    ),
    "Golem Friendship": PokeparkItemData(
        "Item", IC.progression, 112, 1, PokeparkFriendshipItemClientData(
            parameter1=0x74,
        )
    ),
    "Quilava Friendship": PokeparkItemData(
        "Item", IC.progression, 113, 1, PokeparkFriendshipItemClientData(
            parameter1=0x48,
        )
    ),
    "Baltoy Friendship": PokeparkItemData(
        "Item", IC.progression, 114, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa3,
        )
    ),
    "Claydol Friendship": PokeparkItemData(
        "Item", IC.progression, 115, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa4,
        )
    ),
    "Ponyta Friendship": PokeparkItemData(
        "Item", IC.progression, 116, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb0,
        )
    ),
    "Rhyperior Friendship": PokeparkItemData(
        "Item", IC.progression, 117, 1, PokeparkFriendshipItemClientData(
            parameter1=0x75,
        )
    ),
    "Torchic Friendship": PokeparkItemData(
        "Item", IC.progression, 118, 1, PokeparkFriendshipItemClientData(
            parameter1=0x3f,
        )
    ),
    "Blaziken Friendship": PokeparkItemData(
        "Item", IC.progression, 119, 1, PokeparkFriendshipItemClientData(
            parameter1=0x6a,
        )
    ),
    "Murkrow Friendship": PokeparkItemData(
        "Item", IC.progression, 120, 1, PokeparkFriendshipItemClientData(
            parameter1=0x24,
        )
    ),
    "Honchkrow Friendship": PokeparkItemData(
        "Item", IC.progression, 121, 1, PokeparkFriendshipItemClientData(
            parameter1=0x96,
        )
    ),
    "Gliscor Friendship": PokeparkItemData(
        "Item", IC.progression, 122, 1, PokeparkFriendshipItemClientData(
            parameter1=0x93,
        )
    ),
    "Drifloon Friendship": PokeparkItemData(
        "Item", IC.progression, 123, 1, PokeparkFriendshipItemClientData(
            parameter1=0x61,
        )
    ),
    "Kakuna Friendship": PokeparkItemData(
        "Item", IC.progression, 124, 1, PokeparkFriendshipItemClientData(
            parameter1=0x31,
        )
    ),
    "Metapod Friendship": PokeparkItemData(
        "Item", IC.progression, 125, 1, PokeparkFriendshipItemClientData(
            parameter1=0x7b,
        )
    ),
    "Tangrowth Friendship": PokeparkItemData(
        "Item", IC.progression, 126, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb9,
        )
    ),
    "Riolu Friendship": PokeparkItemData(
        "Item", IC.progression, 127, 1, PokeparkFriendshipItemClientData(
            parameter1=0x11,
        )
    ),
    "Sableye Friendship": PokeparkItemData(
        "Item", IC.progression, 128, 1, PokeparkFriendshipItemClientData(
            parameter1=0x79,
        )
    ),
    "Spinarak Friendship": PokeparkItemData(
        "Item", IC.progression, 129, 1, PokeparkFriendshipItemClientData(
            parameter1=0x73,
        )
    ),
    "Breloom Friendship": PokeparkItemData(
        "Item", IC.progression, 130, 1, PokeparkFriendshipItemClientData(
            parameter1=0x65,
        )
    ),
    "Pichu Friendship": PokeparkItemData(
        "Item", IC.progression, 131, 1, PokeparkFriendshipItemClientData(
            parameter1=0x14,
        )
    ),
    "Misdreavus Friendship": PokeparkItemData(
        "Item", IC.progression, 132, 1, PokeparkFriendshipItemClientData(
            parameter1=0x3e,
        )
    ),
    "Mismagius Friendship": PokeparkItemData(
        "Item", IC.progression, 133, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa6,
        )
    ),
    "Elekid Friendship": PokeparkItemData(
        "Item", IC.progression, 134, 1, PokeparkFriendshipItemClientData(
            parameter1=0x17,
        )
    ),
    "Electabuzz Friendship": PokeparkItemData(
        "Item", IC.progression, 135, 1, PokeparkFriendshipItemClientData(
            parameter1=0x2,
        )
    ),
    "Luxray Friendship": PokeparkItemData(
        "Item", IC.progression, 136, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa8,
        )
    ),
    "Stunky Friendship": PokeparkItemData(
        "Item", IC.progression, 137, 1, PokeparkFriendshipItemClientData(
            parameter1=0x1e,
        )
    ),
    "Skuntank Friendship": PokeparkItemData(
        "Item", IC.progression, 138, 1, PokeparkFriendshipItemClientData(
            parameter1=0x43,
        )
    ),
    "Voltorb Friendship": PokeparkItemData(
        "Item", IC.progression, 139, 1, PokeparkFriendshipItemClientData(
            parameter1=0x5f,
        )
    ),
    "Electrode Friendship": PokeparkItemData(
        "Item", IC.progression, 140, 1, PokeparkFriendshipItemClientData(
            parameter1=0x60,
        )
    ),
    "Umbreon Friendship": PokeparkItemData(
        "Item", IC.progression, 141, 1, PokeparkFriendshipItemClientData(
            parameter1=0x4f,
        )
    ),
    "Espeon Friendship": PokeparkItemData(
        "Item", IC.progression, 142, 1, PokeparkFriendshipItemClientData(
            parameter1=0x4e,
        )
    ),
    "Gastly Friendship": PokeparkItemData(
        "Item", IC.progression, 143, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa0,
        )
    ),
    "Haunter Friendship": PokeparkItemData(
        "Item", IC.progression, 144, 1, PokeparkFriendshipItemClientData(
            parameter1=0x44,
        )
    ),
    "Gengar Friendship": PokeparkItemData(
        "Item", IC.progression, 145, 1, PokeparkFriendshipItemClientData(
            parameter1=0x3c,
        )
    ),
    "Duskull Friendship": PokeparkItemData(
        "Item", IC.progression, 146, 1, PokeparkFriendshipItemClientData(
            parameter1=0x1a,
        )
    ),
    "Dusknoir Friendship": PokeparkItemData(
        "Item", IC.progression, 147, 1, PokeparkFriendshipItemClientData(
            parameter1=0xba,
        )
    ),
    "Charizard Friendship": PokeparkItemData(
        "Item", IC.progression, 148, 1, PokeparkFriendshipItemClientData(
            parameter1=0x3a,
        )
    ),
    "Flygon Friendship": PokeparkItemData(
        "Item", IC.progression, 149, 1, PokeparkFriendshipItemClientData(
            parameter1=0x9c,
        )
    ),
    "Porygon-Z Friendship": PokeparkItemData(
        "Item", IC.progression, 150, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc8,
        )
    ),
    "Bronzor Friendship": PokeparkItemData(
        "Item", IC.progression, 151, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa5,
        )
    ),
    "Togekiss Friendship": PokeparkItemData(
        "Item", IC.progression, 152, 1, PokeparkFriendshipItemClientData(
            parameter1=0x94,
        )
    ),
    "Arcanine Friendship": PokeparkItemData(
        "Item", IC.progression, 153, 1, PokeparkFriendshipItemClientData(
            parameter1=0x77,
        )
    ),
    "Lopunny Friendship": PokeparkItemData(
        "Item", IC.progression, 154, 1, PokeparkFriendshipItemClientData(
            parameter1=0x67,
        )
    ),
    "Furret Friendship": PokeparkItemData(
        "Item", IC.progression, 155, 1, PokeparkFriendshipItemClientData(
            parameter1=0x9f,
        )
    ),
    "Staraptor Friendship": PokeparkItemData(
        "Item", IC.progression, 156, 1, PokeparkFriendshipItemClientData(
            parameter1=0x32,
        )
    ),
    "Skorupi Friendship": PokeparkItemData(
        "Item", IC.progression, 157, 1, PokeparkFriendshipItemClientData(
            parameter1=0x1b,
        )
    ),
    "Eevee Friendship": PokeparkItemData(
        "Item", IC.progression, 158, 1, PokeparkFriendshipItemClientData(
            parameter1=0x49,
        )
    ),
    "Hoppip Friendship": PokeparkItemData(
        "Item", IC.progression, 159, 1, PokeparkFriendshipItemClientData(
            parameter1=0x91,
        )
    ),
    "Jumpluff Friendship": PokeparkItemData(
        "Item", IC.progression, 160, 1, PokeparkFriendshipItemClientData(
            parameter1=0x92,
        )
    ),
    "Aerodactyl Friendship": PokeparkItemData(
        "Item", IC.progression, 161, 1, PokeparkFriendshipItemClientData(
            parameter1=0x9b,
        )
    ),
    "Jolteon Friendship": PokeparkItemData(
        "Item", IC.progression, 162, 1, PokeparkFriendshipItemClientData(
            parameter1=0x4d,
        )
    ),
    "Tyranitar Friendship": PokeparkItemData(
        "Item", IC.progression, 163, 1, PokeparkFriendshipItemClientData(
            parameter1=0xa9
        )
    ),
    "Garchomp Friendship": PokeparkItemData(
        "Item", IC.progression, 164, 1, PokeparkFriendshipItemClientData(
            parameter1=0x9a,
        )
    ),
    "Absol Friendship": PokeparkItemData(
        "Item", IC.progression, 165, 1, PokeparkFriendshipItemClientData(
            parameter1=0x46,
        )
    ),
    "Salamence Friendship": PokeparkItemData(
        "Item", IC.progression, 166, 1, PokeparkFriendshipItemClientData(
            parameter1=0x9d,
        )
    ),
    "Bellossom Friendship": PokeparkItemData(
        "Item", IC.progression, 167, 1, PokeparkFriendshipItemClientData(
            parameter1=0x40,
        )
    ),
    "Budew Friendship": PokeparkItemData(
        "Item", IC.progression, 168, 1, PokeparkFriendshipItemClientData(
            parameter1=0x72,
        )
    ),
    "Skiploom Friendship": PokeparkItemData(
        "Item", IC.progression, 169, 1, PokeparkFriendshipItemClientData(
            parameter1=0x41,
        )
    ),
    "Cyndaquil Friendship": PokeparkItemData(
        "Item", IC.progression, 170, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb7,
        )
    ),
    "Mareep Friendship": PokeparkItemData(
        "Item", IC.progression, 171, 1, PokeparkFriendshipItemClientData(
            parameter1=0x3d,
        )
    ),
    "Dragonite Friendship": PokeparkItemData(
        "Item", IC.progression, 172, 1, PokeparkFriendshipItemClientData(
            parameter1=0x98,
        )
    ),
    "Lucario Friendship": PokeparkItemData(
        "Item", IC.progression, 173, 1, PokeparkFriendshipItemClientData(
            parameter1=0x3,
        )
    ),
    "Rayquaza Friendship": PokeparkItemData(
        "Item", IC.progression, 174, 1, PokeparkFriendshipItemClientData(
            parameter1=0x63,
        )
    ),
    "Drifblim Friendship": PokeparkItemData(
        "Item", IC.progression, 175, 1, PokeparkFriendshipItemClientData(
            parameter1=0x62,
        )
    ),
    "Burmy Friendship": PokeparkItemData(
        "Item", IC.progression, 176, 1, PokeparkFriendshipItemClientData(
            parameter1=0x7c,
        )
    ),
    "Mime Jr. Friendship": PokeparkItemData(
        "Item", IC.progression, 177, 1, PokeparkFriendshipItemClientData(
            parameter1=0x1,
        )
    ),
    "Abra Friendship": PokeparkItemData(
        "Item", IC.progression, 178, 1, PokeparkFriendshipItemClientData(
            parameter1=0x5e,
        )
    ),
    "Mew Friendship": PokeparkItemData(
        "Item", IC.progression, 179, 1, PokeparkFriendshipItemClientData(
            parameter1=0x5,
        )
    ),
    "Jirachi Friendship": PokeparkItemData(
        "Item", IC.progression, 180, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc0,
        )
    ),
    "Manaphy Friendship": PokeparkItemData(
        "Item", IC.progression, 181, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc2,
        )
    ),
    "Latias Friendship": PokeparkItemData(
        "Item", IC.progression, 182, 1, PokeparkFriendshipItemClientData(
            parameter1=0xbc,
        )
    ),
    "Suicune Friendship": PokeparkItemData(
        "Item", IC.progression, 183, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc4,
        )
    ),
    "Metagross Friendship": PokeparkItemData(
        "Item", IC.progression, 184, 1, PokeparkFriendshipItemClientData(
            parameter1=0xb1,
        )
    ),
    "Heatran Friendship": PokeparkItemData(
        "Item", IC.progression, 185, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc1,
        )
    ),
    "Groudon Friendship": PokeparkItemData(
        "Item", IC.progression, 186, 1, PokeparkFriendshipItemClientData(
            parameter1=0xbf,
        )
    ),
    "Celebi Friendship": PokeparkItemData(
        "Item", IC.progression, 187, 1, PokeparkFriendshipItemClientData(
            parameter1=0xbb,
        )
    ),
    "Darkrai Friendship": PokeparkItemData(
        "Item", IC.progression, 188, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc3,
        )
    ),
    "Rotom Friendship": PokeparkItemData(
        "Item", IC.progression, 189, 1, PokeparkFriendshipItemClientData(
            parameter1=0x88,
        )
    ),
    "Shaymin Friendship": PokeparkItemData(
        "Item", IC.progression, 190, 1, PokeparkFriendshipItemClientData(
            parameter1=0x36,
        )
    ),
    "Latios Friendship": PokeparkItemData(
        "Item", IC.progression, 191, 1, PokeparkFriendshipItemClientData(
            parameter1=0xbd,
        )
    ),
    "Deoxys Friendship": PokeparkItemData(
        "Item", IC.progression, 192, 1, PokeparkFriendshipItemClientData(
            parameter1=0xc5,
        )
    ),

    "Tropius Unlock": PokeparkItemData(
        "Item", IC.progression, 193, 1, PokeparkUnlockItemClientData(
            parameter1=0x17
        )
    ),
    "Pachirisu Unlock": PokeparkItemData(
        "Item", IC.progression, 194, 1, PokeparkUnlockItemClientData(
            parameter1=0x04
        )
    ),
    "Bonsly Unlock": PokeparkItemData(
        "Item", IC.progression, 195, 1, PokeparkUnlockItemClientData(
            parameter1=0x0f
        )
    ),
    "Sudowoodo Unlock": PokeparkItemData(
        "Item", IC.progression, 196, 1, PokeparkUnlockItemClientData(
            parameter1=0x57
        )
    ),
    "Lotad Unlock": PokeparkItemData(
        "Item", IC.progression, 197, 1, PokeparkUnlockItemClientData(
            parameter1=0x09
        )
    ),
    "Shinx Unlock": PokeparkItemData(
        "Item", IC.progression, 198, 1, PokeparkUnlockItemClientData(
            parameter1=0x10
        )
    ),
    "Scyther Unlock": PokeparkItemData(
        "Item", IC.progression, 199, 1, PokeparkUnlockItemClientData(
            parameter1=0x1b
        )
    ),
    "Caterpie Unlock": PokeparkItemData(
        "Item", IC.progression, 200, 1, PokeparkUnlockItemClientData(
            parameter1=0x0a
        )
    ),
    "Butterfree Unlock": PokeparkItemData(
        "Item", IC.progression, 201, 1, PokeparkUnlockItemClientData(
            parameter1=0x16
        )
    ),
    "Chimchar Unlock": PokeparkItemData(
        "Item", IC.progression, 202, 1, PokeparkUnlockItemClientData(
            parameter1=0x07
        )
    ),
    "Ambipom Unlock": PokeparkItemData(
        "Item", IC.progression, 203, 1, PokeparkUnlockItemClientData(
            parameter1=0x19
        )
    ),
    "Weedle Unlock": PokeparkItemData(
        "Item", IC.progression, 204, 1, PokeparkUnlockItemClientData(
            parameter1=0x0b
        )
    ),
    "Shroomish Unlock": PokeparkItemData(
        "Item", IC.progression, 205, 1, PokeparkUnlockItemClientData(
            parameter1=0x0e
        )
    ),
    "Magikarp Unlock": PokeparkItemData(
        "Item", IC.progression, 206, 1, PokeparkUnlockItemClientData(
            parameter1=0x08
        )
    ),
    "Bidoof Unlock": PokeparkItemData(
        "Item", IC.filler, 207, 1, PokeparkUnlockItemClientData(
            parameter1=0x20
        )
    ),
    "Bidoof 2 Unlock": PokeparkItemData(
        "Item", IC.filler, 208, 1, PokeparkUnlockItemClientData(
            parameter1=0x21
        )
    ),
    "Bidoof 3 Unlock": PokeparkItemData(
        "Item", IC.filler, 209, 1, PokeparkUnlockItemClientData(
            parameter1=0x22
        )
    ),
    "Beach Bidoof Unlock": PokeparkItemData(
        "Item", IC.filler, 210, 1, PokeparkUnlockItemClientData(
            parameter1=0x9c
        )
    ),
    "Bibarel Unlock": PokeparkItemData(
        "Item", IC.progression, 211, 1, PokeparkUnlockItemClientData(
            parameter1=0x18
        )
    ),
    "Starly Unlock": PokeparkItemData(
        "Item", IC.progression, 212, 1, PokeparkUnlockItemClientData(
            parameter1=0x15
        )
    ),
    "Starly 2 Unlock": PokeparkItemData(
        "Item", IC.progression, 213, 1, PokeparkUnlockItemClientData(
            parameter1=0x25
        )
    ),
    "Torterra Unlock": PokeparkItemData(
        "Item", IC.progression, 214, 1, PokeparkUnlockItemClientData(
            parameter1=0x14
        )
    ),
    "Floatzel Unlock": PokeparkItemData(
        "Item", IC.progression, 215, 1, PokeparkUnlockItemClientData(
            parameter1=0x3a
        )
    ),
    "Mudkip Unlock": PokeparkItemData(
        "Item", IC.progression, 216, 1, PokeparkUnlockItemClientData(
            parameter1=0x33
        )
    ),
    "Totodile Unlock": PokeparkItemData(
        "Item", IC.progression, 217, 1, PokeparkUnlockItemClientData(
            parameter1=0x32
        )
    ),
    "Golduck Unlock": PokeparkItemData(
        "Item", IC.progression, 218, 1, PokeparkUnlockItemClientData(
            parameter1=0x39
        )
    ),
    "Krabby Unlock": PokeparkItemData(
        "Item", IC.progression, 219, 1, PokeparkUnlockItemClientData(
            parameter1=0x39
        )
    ),
    "Corphish Unlock": PokeparkItemData(
        "Item", IC.progression, 220, 1, PokeparkUnlockItemClientData(
            parameter1=0x34
        )
    ),
    "Delibird Unlock": PokeparkItemData(
        "Item", IC.progression, 221, 1, PokeparkUnlockItemClientData(
            parameter1=0x4a
        )
    ),
    "Squirtle Unlock": PokeparkItemData(
        "Item", IC.progression, 222, 1, PokeparkUnlockItemClientData(
            parameter1=0x4c
        )
    ),
    "Smoochum Unlock": PokeparkItemData(
        "Item", IC.progression, 223, 1, PokeparkUnlockItemClientData(
            parameter1=0x4b
        )
    ),
    "Sneasel Unlock": PokeparkItemData(
        "Item", IC.progression, 224, 1, PokeparkUnlockItemClientData(
            parameter1=0x48
        )
    ),
    "Mamoswine Unlock": PokeparkItemData(
        "Item", IC.progression, 225, 1, PokeparkUnlockItemClientData(
            parameter1=0x53
        )
    ),
    "Glalie Unlock": PokeparkItemData(
        "Item", IC.progression, 226, 1, PokeparkUnlockItemClientData(
            parameter1=0xb8
        )
    ),
    "Primeape Unlock": PokeparkItemData(
        "Item", IC.progression, 227, 1, PokeparkUnlockItemClientData(
            parameter1=0x4e
        )
    ),
    "Ursaring Unlock": PokeparkItemData(
        "Item", IC.progression, 228, 1, PokeparkUnlockItemClientData(
            parameter1=0x4f
        )
    ),
    "Magnemite Unlock": PokeparkItemData(
        "Item", IC.progression, 229, 1, PokeparkUnlockItemClientData(
            parameter1=0x58
        )
    ),
    "Machamp Unlock": PokeparkItemData(
        "Item", IC.filler, 230, 1, PokeparkUnlockItemClientData(
            parameter1=0x99
        )
    ),
    "Magnemite 2 Unlock": PokeparkItemData(
        "Item", IC.progression, 231, 1, PokeparkUnlockItemClientData(
            parameter1=0xa8
        )
    ),
    "Magnemite 3 Unlock": PokeparkItemData(
        "Item", IC.progression, 232, 1, PokeparkUnlockItemClientData(
            parameter1=0xa9
        )
    ),
    "Diglett Unlock": PokeparkItemData(
        "Item", IC.progression, 233, 1, PokeparkUnlockItemClientData(
            parameter1=0x9a
        )
    ),
    "Magnezone Unlock": PokeparkItemData(
        "Item", IC.progression, 234, 1, PokeparkUnlockItemClientData(
            parameter1=0x67
        )
    ),
    "Phanpy Unlock": PokeparkItemData(
        "Item", IC.progression, 235, 1, PokeparkUnlockItemClientData(
            parameter1=0x59
        )
    ),
    "Raichu Unlock": PokeparkItemData(
        "Item", IC.progression, 236, 1, PokeparkUnlockItemClientData(
            parameter1=0x5f
        )
    ),
    "Infernape Unlock": PokeparkItemData(
        "Item", IC.progression, 237, 1, PokeparkUnlockItemClientData(
            parameter1=0x6b
        )
    ),
    "Ninetales Unlock": PokeparkItemData(
        "Item", IC.progression, 238, 1, PokeparkUnlockItemClientData(
            parameter1=0x75
        )
    ),
    "Ponyta Unlock": PokeparkItemData(
        "Item", IC.progression, 239, 1, PokeparkUnlockItemClientData(
            parameter1=0x1a
        )
    ),
    "Torkoal Unlock": PokeparkItemData(
        "Item", IC.progression, 240, 1, PokeparkUnlockItemClientData(
            parameter1=0x63
        )
    ),
    "Golem Unlock": PokeparkItemData(
        "Item", IC.progression, 241, 1, PokeparkUnlockItemClientData(
            parameter1=0x6c
        )
    ),
    "Baltoy Unlock": PokeparkItemData(
        "Item", IC.progression, 242, 1, PokeparkUnlockItemClientData(
            parameter1=0x9d
        )
    ),
    "Claydol Unlock": PokeparkItemData(
        "Item", IC.progression, 243, 1, PokeparkUnlockItemClientData(
            parameter1=0x65
        )
    ),
    "Hitmonchan Unlock": PokeparkItemData(
        "Item", IC.progression, 244, 1, PokeparkUnlockItemClientData(
            parameter1=0x69
        )
    ),
    "Hitmonlee Unlock": PokeparkItemData(
        "Item", IC.progression, 245, 1, PokeparkUnlockItemClientData(
            parameter1=0x60
        )
    ),
    "Honchkrow Unlock": PokeparkItemData(
        "Item", IC.progression, 246, 1, PokeparkUnlockItemClientData(
            parameter1=0xa0
        )
    ),
    "Metapod Unlock": PokeparkItemData(
        "Item", IC.progression, 247, 1, PokeparkUnlockItemClientData(
            parameter1=0x72
        )
    ),
    "Kakuna Unlock": PokeparkItemData(
        "Item", IC.progression, 248, 1, PokeparkUnlockItemClientData(
            parameter1=0x71
        )
    ),
    "Voltorb Unlock": PokeparkItemData(
        "Item", IC.progression, 249, 1, PokeparkUnlockItemClientData(
            parameter1=0xb7
        )
    ),
    "Elekid Unlock": PokeparkItemData(
        "Item", IC.progression, 250, 1, PokeparkUnlockItemClientData(
            parameter1=0xad
        )
    ),
    "Electabuzz Unlock": PokeparkItemData(
        "Item", IC.progression, 251, 1, PokeparkUnlockItemClientData(
            parameter1=0x66
        )
    ),
    "Luxray Unlock": PokeparkItemData(
        "Item", IC.progression, 252, 1, PokeparkUnlockItemClientData(
            parameter1=0x81
        )
    ),
    "Stunky Unlock": PokeparkItemData(
        "Item", IC.progression, 253, 1, PokeparkUnlockItemClientData(
            parameter1=0xa1
        )
    ),
    "Skuntank Unlock": PokeparkItemData(
        "Item", IC.progression, 254, 1, PokeparkUnlockItemClientData(
            parameter1=0x7f
        )
    ),
    "Breloom Unlock": PokeparkItemData(
        "Item", IC.progression, 255, 1, PokeparkUnlockItemClientData(
            parameter1=0x74
        )
    ),
    "Mismagius Unlock": PokeparkItemData(
        "Item", IC.progression, 256, 1, PokeparkUnlockItemClientData(
            parameter1=0x80
        )
    ),
    "Electrode Unlock": PokeparkItemData(
        "Item", IC.progression, 257, 1, PokeparkUnlockItemClientData(
            parameter1=0xa3
        )
    ),
    "Haunter Unlock": PokeparkItemData(
        "Item", IC.progression, 258, 1, PokeparkUnlockItemClientData(
            parameter1=0x7d
        )
    ),
    "Gastly Unlock": PokeparkItemData(
        "Item", IC.progression, 259, 1, PokeparkUnlockItemClientData(
            parameter1=0xa2
        )
    ),
    "Gastly 2 Unlock": PokeparkItemData(
        "Item", IC.progression, 260, 1, PokeparkUnlockItemClientData(
            parameter1=0xa7
        )
    ),
    "Dusknoir Unlock": PokeparkItemData(
        "Item", IC.progression, 261, 1, PokeparkUnlockItemClientData(
            parameter1=0x84
        )
    ),
    "Espeon Unlock": PokeparkItemData(
        "Item", IC.progression, 262, 1, PokeparkUnlockItemClientData(
            parameter1=0x82
        )
    ),
    "Gengar Unlock": PokeparkItemData(
        "Item", IC.progression, 263, 1, PokeparkUnlockItemClientData(
            parameter1=0x83
        )
    ),
    "Blastoise Unlock": PokeparkItemData(
        "Item", IC.progression, 264, 1, PokeparkUnlockItemClientData(
            parameter1=0x3d
        )
    ),
    "Electivire Unlock": PokeparkItemData(
        "Item", IC.progression, 265, 1, PokeparkUnlockItemClientData(
            parameter1=0x61
        )
    ),
    "Magmortar Unlock": PokeparkItemData(
        "Item", IC.progression, 266, 1, PokeparkUnlockItemClientData(
            parameter1=0x9e
        )
    ),
    "Jolteon Unlock": PokeparkItemData(
        "Item", IC.progression, 267, 1, PokeparkUnlockItemClientData(
            parameter1=0x8d
        )
    ),
    "Aerodactyl Unlock": PokeparkItemData(
        "Item", IC.progression, 268, 1, PokeparkUnlockItemClientData(
            parameter1=0xb4
        )
    ),
    "Tyranitar Unlock": PokeparkItemData(
        "Item", IC.progression, 269, 1, PokeparkUnlockItemClientData(
            parameter1=0x86
        )
    ),
    "Garchomp Unlock": PokeparkItemData(
        "Item", IC.progression, 270, 1, PokeparkUnlockItemClientData(
            parameter1=0x85
        )
    ),
    "Rayquaza Unlock": PokeparkItemData(
        "Item", IC.progression, 271, 1, PokeparkUnlockItemClientData(
            parameter1=0x95
        )
    ),
    "Celebi Unlock": PokeparkItemData(
        "Item", IC.filler, 272, 1, PokeparkUnlockItemClientData(
            parameter1=0xa5
        )
    ),
    "Darkrai Unlock": PokeparkItemData(
        "Item", IC.filler, 273, 1, PokeparkUnlockItemClientData(
            parameter1=0xa4
        )
    ),
    "Groudon Unlock": PokeparkItemData(
        "Item", IC.filler, 274, 1, PokeparkUnlockItemClientData(
            parameter1=0x9f
        )
    ),
    "Jirachi Unlock": PokeparkItemData(
        "Item", IC.filler, 275, 1, PokeparkUnlockItemClientData(
            parameter1=0xa6
        )
    ),
    "Pikachu Balloon": PokeparkItemData(
        "Item", IC.progression, 276, 1, PokeparkPasswordItemClientData(
            parameter1=0x3
        )
    ),
    "Pikachu Surfboard": PokeparkItemData(
        "Item", IC.progression, 277, 1, PokeparkPasswordItemClientData(
            parameter1=0x0
        )
    ),
    "Pikachu Snowboard": PokeparkItemData(
        "Item", IC.progression, 278, 1, PokeparkPasswordItemClientData(
            parameter1=0x2
        )
    ),
    "10 Berries": PokeparkItemData(
        "Item", IC.filler, 279, 1, PokeparkBerryItemClientData(
            parameter1=0xa
        )
    ),
    "20 Berries": PokeparkItemData(
        "Item", IC.filler, 280, 1, PokeparkBerryItemClientData(
            parameter1=0x14
        )
    ),
    "50 Berries": PokeparkItemData(
        "Item", IC.filler, 281, 1, PokeparkBerryItemClientData(
            parameter1=0x32
        )
    ),
    "100 Berries": PokeparkItemData(
        "Item", IC.filler, 282, 1, PokeparkBerryItemClientData(
            parameter1=0x64
        )
    ),
    "Bulbasaur Prisma": PokeparkItemData(
        "Item", IC.progression, 283, 1, PokeparkPrismaItemClientData(
            parameter1=0x0f
        )
    ),
    "Venusaur Prisma": PokeparkItemData(
        "Item", IC.progression, 284, 1, PokeparkPrismaItemClientData(
            parameter1=0x02
        )
    ),
    "Pelipper Prisma": PokeparkItemData(
        "Item", IC.progression, 285, 1, PokeparkPrismaItemClientData(
            parameter1=0x06
        )
    ),
    "Gyarados Prisma": PokeparkItemData(
        "Item", IC.progression, 286, 1, PokeparkPrismaItemClientData(
            parameter1=0x05
        )
    ),
    "Empoleon Prisma": PokeparkItemData(
        "Item", IC.progression, 287, 1, PokeparkPrismaItemClientData(
            parameter1=0x08
        )
    ),
    "Bastiodon Prisma": PokeparkItemData(
        "Item", IC.progression, 288, 1, PokeparkPrismaItemClientData(
            parameter1=0x09
        )
    ),
    "Rhyperior Prisma": PokeparkItemData(
        "Item", IC.progression, 289, 1, PokeparkPrismaItemClientData(
            parameter1=0x0a
        )
    ),
    "Blaziken Prisma": PokeparkItemData(
        "Item", IC.progression, 290, 1, PokeparkPrismaItemClientData(
            parameter1=0x0b
        )
    ),
    "Tangrowth Prisma": PokeparkItemData(
        "Item", IC.progression, 291, 1, PokeparkPrismaItemClientData(
            parameter1=0x03
        )
    ),
    "Dusknoir Prisma": PokeparkItemData(
        "Item", IC.progression, 292, 1, PokeparkPrismaItemClientData(
            parameter1=0x04
        )
    ),
    "Rotom Prisma": PokeparkItemData(
        "Item", IC.progression, 293, 1, PokeparkPrismaItemClientData(
            parameter1=0x0c
        )
    ),
    "Absol Prisma": PokeparkItemData(
        "Item", IC.progression, 294, 1, PokeparkPrismaItemClientData(
            parameter1=0x00
        )
    ),
    "Salamence Prisma": PokeparkItemData(
        "Item", IC.progression, 295, 1, PokeparkPrismaItemClientData(
            parameter1=0x0e
        )
    ),
    "Rayquaza Prisma": PokeparkItemData(
        "Item", IC.progression, 296, 1, PokeparkPrismaItemClientData(
            parameter1=0x01
        )
    ),
    "Progressive Dash": PokeparkItemData(
        "Item", IC.progression, 297, 4, PokeparkPowerItemClientData(
            parameter1=0x01
        )
    ),
    "Progressive Thunderbolt": PokeparkItemData(
        "Item", IC.progression, 298, 4, PokeparkPowerItemClientData(
            parameter1=0x02
        )
    ),
    "Progressive Health": PokeparkItemData(
        "Item", IC.useful, 299, 3, PokeparkPowerItemClientData(
            parameter1=0x03
        )
    ),
    "Progressive Iron Tail": PokeparkItemData(
        "Item", IC.useful, 300, 3, PokeparkPowerItemClientData(
            parameter1=0x04
        )
    ),
    "Double Dash": PokeparkItemData(
        "Item", IC.useful, 301, 1, PokeparkPowerItemClientData(
            parameter1=0x05
        )
    ),
    "Meadow Zone Fast Travel": PokeparkItemData(
        "Item", IC.useful, 302, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0101FuwarideTaxiStop"),
            parameter1=0x80001860
        )
    ),
    "Beach Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 303, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0301FuwarideTaxiStop"),
            parameter1=0x80001860
        )
    ),
    "Ice Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 304, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0302FuwarideTaxiStop"),
            parameter1=0x80001860
        )
    ),
    "Cavern Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 305, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0401FuwarideTaxiStop"),
            parameter1=0x80001860
        )
    ),
    "Magma Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 306, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0402FuwarideTaxiStop"),
            parameter1=0x80001860
        )
    ),
    "Haunted Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 307, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0501FuwarideTaxiStop"),
            parameter1=0x80001860
        )
    ),
    "Granite Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 308, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0601FuwarideTaxiStop"),
            parameter1=0x80001860
        )
    ),
    "Flower Zone Fast Travel": PokeparkItemData(
        "Item", IC.progression, 309, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0602FuwarideTaxiStop"),
            parameter1=0x80001860
        )
    ),

    "Beach Bridge 1 Unlock": PokeparkItemData(
        "Item", IC.progression, 310, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("fMap0301Bridge1Build"),
            parameter1=0x80001860
        )
    ),
    "Beach Bridge 2 Unlock": PokeparkItemData(
        "Item", IC.progression, 311, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("fMap0301Bridge3Build"),
            parameter1=0x80001860
        )
    ),
    "Magma Zone Fire Wall Unlock": PokeparkItemData(
        "Item", IC.progression, 312, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0402FireWallA"),
            parameter1=0x80001860
        )
    ),
    "Haunted Zone Mansion Doors Unlock": PokeparkItemData(
        "Item", IC.progression, 315, 1, PokeparkFlagItemClientData(
            flag_name=generate_flagname("f0502DoorA"),
            parameter1=0x80001860
        )
    ),
    "Victory": PokeparkItemData(
        "Event", IC.progression, None, 1, None
    )
}
LOOKUP_ID_TO_NAME: dict[int, str] = {
    PokeparkItem.get_apid(data.code): item for item, data in ITEM_TABLE.items() if data.code is not None
}

item_name_groups = {

}
_simple_groups = {
    ("Friendship Items", "Friendship"),
    ("Unlock Items", "Unlock"),
    ("Prisma Items", "Prisma"),
    ("Fast Travel Items", "Fast Travel")
}

for basename, substring in _simple_groups:
    if basename not in item_name_groups:
        item_name_groups[basename] = set()
    for itemname in ITEM_TABLE:
        if substring in itemname:
            item_name_groups[basename].add(itemname)

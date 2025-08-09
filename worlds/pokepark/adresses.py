from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional

from worlds.pokepark import FRIENDSHIP_ITEMS, UNLOCK_ITEMS, BERRIES
from worlds.pokepark.LocationIds import MinigameLocationIds, QuestLocationIds
from worlds.pokepark.items import PRISM_ITEM, POWERS


class MemoryRange(Enum):
    BYTE = 1  # 1 Byte
    HALFWORD = 2  # 2 Bytes
    WORD = 4  # 4 Bytes

    @property
    def mask(self):
        if self == MemoryRange.WORD:
            return 0xFFFFFFFF
        elif self == MemoryRange.HALFWORD:
            return 0xFFFF
        else:  # BYTE
            return 0xFF


@dataclass
class MemoryAddress:
    base_address: int
    offset: int = 0
    memory_range: MemoryRange = MemoryRange.WORD
    value: int = 0

    @property
    def final_address(self):
        return self.base_address + self.offset


@dataclass
class UnlockLocation:
    location: MemoryAddress
    zone_id: int
    locationId: int
    is_blocked_until_location: bool = False


@dataclass
class UnlockState:
    item: MemoryAddress
    locations: List[UnlockLocation] = field(default_factory=list)


@dataclass
class PrismaItem:
    item: MemoryAddress
    location: MemoryAddress
    locationId: int
    itemId: int
    stage_id: int


@dataclass
class PokemonLocation:
    location: MemoryAddress
    zone_id: int
    locationId: int
    pokemon_ids: List[int] | None = None
    friendship_items_to_block: List[int] | None = None
    unlock_items_to_block: List[int] | None = None
    is_special_exception: bool = False


@dataclass
class BaseLocation:
    location_name: str
    location_ids: List[int] | None = None
    structure_position: int = 0x0  # position of the specific data structure together used with structure_address_intervall to find wanted data struc address
    memory_range: MemoryRange = MemoryRange.WORD

    # These will be set by subclasses
    bit_mask: int = field(init=False)
    global_manager_data_struc_offset: int = field(init=False)
    in_structure_offset: int = field(init=False)
    expected_value: int = field(init=False)
    in_structure_address_interval: int = field(init=False)

    @property
    def final_offset(self):
        return self.global_manager_data_struc_offset + self.in_structure_offset + (
                self.in_structure_address_interval * self.structure_position)


@dataclass
class FriendshipLocation(BaseLocation):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1F4  # start of friendship data structure
        self.in_structure_offset = 0xc  # best friend offset from friendship address
        self.expected_value = 0x80  # flag is set with value 0x80
        self.in_structure_address_interval = 0x14  # spacing between specific pokemon friendship data
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PrismaLocation(BaseLocation):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1B40  # start of prisma data structure
        self.in_structure_offset = 0x0
        self.expected_value = 0b10  # flag is set with prisma value 0b10
        self.bit_mask = 0b10  # using only second bit
        self.in_structure_address_interval = 0x144  # spacing between prisma


# currently separate classes for flags until more data is available
@dataclass
class WeedleLocation(BaseLocation):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x4b
        self.in_structure_offset = 0x0
        self.expected_value = 0b00001000
        self.bit_mask = 0b00001000
        self.in_structure_address_interval = 0x0


@dataclass
class CaterpieLocation(BaseLocation):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x4b
        self.in_structure_offset = 0x0
        self.expected_value = 0b00000001
        self.bit_mask = 0b00000001
        self.in_structure_address_interval = 0x0


@dataclass
class ShroomishLocation(BaseLocation):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x41
        self.in_structure_offset = 0x0
        self.expected_value = 0b10000000
        self.bit_mask = 0b10000000
        self.in_structure_address_interval = 0x0


@dataclass
class MagikarpLocation(BaseLocation):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x50
        self.in_structure_offset = 0x0
        self.expected_value = 0b10000000
        self.bit_mask = 0b10000000
        self.in_structure_address_interval = 0x0


@dataclass
class BidoofHousingLocation(BaseLocation):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2f
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask


@dataclass
class BulbasaurDashMinigame(BaseLocation):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2E50
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class VenusaurSwingMinigame(BaseLocation):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1ddc
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class BaseItem:
    item_name: str
    opcode: int = field(init=False)
    item_id: int


@dataclass
class FriendshipItem(BaseItem):
    def __post_init__(self):
        self.opcode = 0x3c  # friendship opcode


@dataclass
class UnlockItem(BaseItem):
    def __post_init__(self):
        self.opcode = 0x28  # unlock Pokemon opcode


@dataclass
class PowerItem(BaseItem):
    def __post_init__(self):
        self.opcode = 0xb9  # activate Power opcode


@dataclass
class PrismaItem(BaseItem):
    def __post_init__(self):
        self.opcode = 0x52  # set Prisma opcode


@dataclass
class BerryItem(BaseItem):
    def __post_init__(self):
        self.opcode = 0xa  # set Berry opcode


ITEMS: Dict[int, BaseItem] = {
    FRIENDSHIP_ITEMS["Mime Jr."]: FriendshipItem(
        item_name="Mime Jr. Friendship",
        item_id=0x1,
    ),
    FRIENDSHIP_ITEMS["Electabuzz"]: FriendshipItem(
        item_name="Electabuzz Friendship",
        item_id=0x2,
    ),
    FRIENDSHIP_ITEMS["Lucario"]: FriendshipItem(
        item_name="Lucario Friendship",
        item_id=0x3,
    ),
    FRIENDSHIP_ITEMS["Chatot"]: FriendshipItem(
        item_name="Chatot Friendship",
        item_id=0x4,
    ),
    FRIENDSHIP_ITEMS["Mew"]: FriendshipItem(
        item_name="Mew Friendship",
        item_id=0x5,
    ),
    FRIENDSHIP_ITEMS["Piplup"]: FriendshipItem(
        item_name="Piplup Friendship",
        item_id=0x6,
    ),
    FRIENDSHIP_ITEMS["Chimchar"]: FriendshipItem(
        item_name="Piplup Friendship",
        item_id=0x7,
    ),
    FRIENDSHIP_ITEMS["Turtwig"]: FriendshipItem(
        item_name="Turtwig Friendship",
        item_id=0x8,
    ),
    FRIENDSHIP_ITEMS["Buneary"]: FriendshipItem(
        item_name="Buneary Friendship",
        item_id=0x9,
    ),
    FRIENDSHIP_ITEMS["Pachirisu"]: FriendshipItem(
        item_name="Pachirisu Friendship",
        item_id=0xa,
    ),
    FRIENDSHIP_ITEMS["Croagunk"]: FriendshipItem(
        item_name="Croagunk Friendship",
        item_id=0xb,
    ),
    FRIENDSHIP_ITEMS["Staravia"]: FriendshipItem(
        item_name="Staravia Friendship",
        item_id=0xc,
    ),
    FRIENDSHIP_ITEMS["Buizel"]: FriendshipItem(
        item_name="Buizel Friendship",
        item_id=0xd,
    ),
    FRIENDSHIP_ITEMS["Ambipom"]: FriendshipItem(
        item_name="Ambipom Friendship",
        item_id=0xe,
    ),
    FRIENDSHIP_ITEMS["Aipom"]: FriendshipItem(
        item_name="Aipom Friendship",
        item_id=0xf,
    ),
    FRIENDSHIP_ITEMS["Bonsly"]: FriendshipItem(
        item_name="Bonsly Friendship",
        item_id=0x10,
    ),
    FRIENDSHIP_ITEMS["Riolu"]: FriendshipItem(
        item_name="Riolu Friendship",
        item_id=0x11,
    ),
    FRIENDSHIP_ITEMS["Bidoof"]: FriendshipItem(
        item_name="Bidoof Friendship",
        item_id=0x12,
    ),
    FRIENDSHIP_ITEMS["Munchlax"]: FriendshipItem(
        item_name="Munchlax Friendship",
        item_id=0x13,
    ),
    FRIENDSHIP_ITEMS["Pichu"]: FriendshipItem(
        item_name="Pichu Friendship",
        item_id=0x14,
    ),
    FRIENDSHIP_ITEMS["Magby"]: FriendshipItem(
        item_name="Magby Friendship",
        item_id=0x15,
    ),
    FRIENDSHIP_ITEMS["Smoochum"]: FriendshipItem(
        item_name="Smoochum Friendship",
        item_id=0x16,
    ),
    FRIENDSHIP_ITEMS["Elekid"]: FriendshipItem(
        item_name="Elekid Friendship",
        item_id=0x17,
    ),
    FRIENDSHIP_ITEMS["Magnemite"]: FriendshipItem(
        item_name="Magnemite Friendship",
        item_id=0x18,
    ),
    FRIENDSHIP_ITEMS["Lotad"]: FriendshipItem(
        item_name="Lotad Friendship",
        item_id=0x19,
    ),
    FRIENDSHIP_ITEMS["Duskull"]: FriendshipItem(
        item_name="Duskull Friendship",
        item_id=0x1a,
    ),
    FRIENDSHIP_ITEMS["Skorupi"]: FriendshipItem(
        item_name="Skorupi Friendship",
        item_id=0x1b,
    ),
    FRIENDSHIP_ITEMS["Gible"]: FriendshipItem(
        item_name="Gible Friendship",
        item_id=0x1c,
    ),
    FRIENDSHIP_ITEMS["Wynaut"]: FriendshipItem(
        item_name="Wynaut Friendship",
        item_id=0x1d,
    ),
    FRIENDSHIP_ITEMS["Stunky"]: FriendshipItem(
        item_name="Stunky Friendship",
        item_id=0x1e,
    ),
    FRIENDSHIP_ITEMS["Aron"]: FriendshipItem(
        item_name="Aaron Friendship",
        item_id=0x1f,
    ),
    FRIENDSHIP_ITEMS["Meditite"]: FriendshipItem(
        item_name="Meditite Friendship",
        item_id=0x20,
    ),
    FRIENDSHIP_ITEMS["Mankey"]: FriendshipItem(
        item_name="Mankey Friendship",
        item_id=0x21,
    ),
    FRIENDSHIP_ITEMS["Oddish"]: FriendshipItem(
        item_name="Oddish Friendship",
        item_id=0x22,
    ),
    FRIENDSHIP_ITEMS["Corphish"]: FriendshipItem(
        item_name="Corphish Friendship",
        item_id=0x23,
    ),
    FRIENDSHIP_ITEMS["Murkrow"]: FriendshipItem(
        item_name="Murkrow Friendship",
        item_id=0x24,
    ),
    FRIENDSHIP_ITEMS["Phanpy"]: FriendshipItem(
        item_name="Phanpy Friendship",
        item_id=0x25,
    ),
    FRIENDSHIP_ITEMS["Shroomish"]: FriendshipItem(
        item_name="Shroomish Friendship",
        item_id=0x26,
    ),
    FRIENDSHIP_ITEMS["Caterpie"]: FriendshipItem(
        item_name="Caterpie Friendship",
        item_id=0x27,
    ),
    FRIENDSHIP_ITEMS["Weedle"]: FriendshipItem(
        item_name="Weedle Friendship",
        item_id=0x28,
    ),
    FRIENDSHIP_ITEMS["Tropius"]: FriendshipItem(
        item_name="Tropius Friendship",
        item_id=0x29,
    ),
    FRIENDSHIP_ITEMS["Blastoise"]: FriendshipItem(
        item_name="Blastoise Friendship",
        item_id=0x2a,
    ),
    FRIENDSHIP_ITEMS["Magikarp"]: FriendshipItem(
        item_name="Magikarp Friendship",
        item_id=0x2b,
    ),
    FRIENDSHIP_ITEMS["Squirtle"]: FriendshipItem(
        item_name="Squirtle Friendship",
        item_id=0x2c,
    ),
    FRIENDSHIP_ITEMS["Torterra"]: FriendshipItem(
        item_name="Torterra Friendship",
        item_id=0x2d,
    ),
    FRIENDSHIP_ITEMS["Starly"]: FriendshipItem(
        item_name="Starly Friendship",
        item_id=0x2e,
    ),
    FRIENDSHIP_ITEMS["Bibarel"]: FriendshipItem(
        item_name="Bibarel Friendship",
        item_id=0x2f,
    ),
    FRIENDSHIP_ITEMS["Feraligatr"]: FriendshipItem(
        item_name="Feraligatr Friendship",
        item_id=0x30,
    ),
    FRIENDSHIP_ITEMS["Kakuna"]: FriendshipItem(
        item_name="Kakuna Friendship",
        item_id=0x31,
    ),
    FRIENDSHIP_ITEMS["Staraptor"]: FriendshipItem(
        item_name="Staraptor Friendship",
        item_id=0x32,
    ),
    FRIENDSHIP_ITEMS["Golduck"]: FriendshipItem(
        item_name="Golduck Friendship",
        item_id=0x33,
    ),
    FRIENDSHIP_ITEMS["Diglett"]: FriendshipItem(
        item_name="Diglett Friendship",
        item_id=0x34,
    ),
    FRIENDSHIP_ITEMS["Gyarados"]: FriendshipItem(
        item_name="Gyarados Friendship",
        item_id=0x35,
    ),
    FRIENDSHIP_ITEMS["Shaymin"]: FriendshipItem(
        item_name="Shaymin Friendship",
        item_id=0x36,
    ),
    FRIENDSHIP_ITEMS["Treecko"]: FriendshipItem(
        item_name="Treecko Friendship",
        item_id=0x38,
    ),
    FRIENDSHIP_ITEMS["Bulbasaur"]: FriendshipItem(
        item_name="Bulbasaur Friendship",
        item_id=0x39,
    ),
    FRIENDSHIP_ITEMS["Charizard"]: FriendshipItem(
        item_name="Charizard Friendship",
        item_id=0x3a,
    ),
    FRIENDSHIP_ITEMS["Empoleon"]: FriendshipItem(
        item_name="Empoleon Friendship",
        item_id=0x3b,
    ),
    FRIENDSHIP_ITEMS["Gengar"]: FriendshipItem(
        item_name="Gengar Friendship",
        item_id=0x3c,
    ),
    FRIENDSHIP_ITEMS["Mareep"]: FriendshipItem(
        item_name="Mareep Friendship",
        item_id=0x3d,
    ),
    FRIENDSHIP_ITEMS["Misdreavus"]: FriendshipItem(
        item_name="Misdreavus Friendship",
        item_id=0x3e,
    ),
    FRIENDSHIP_ITEMS["Torchic"]: FriendshipItem(
        item_name="Torchic Friendship",
        item_id=0x3f,
    ),
    FRIENDSHIP_ITEMS["Bellossom"]: FriendshipItem(
        item_name="Bellossom Friendship",
        item_id=0x40,
    ),
    FRIENDSHIP_ITEMS["Skiploom"]: FriendshipItem(
        item_name="Skiploom Friendship",
        item_id=0x41,
    ),
    FRIENDSHIP_ITEMS["Azurill"]: FriendshipItem(
        item_name="Azurill Friendship",
        item_id=0x42,
    ),
    FRIENDSHIP_ITEMS["Skuntank"]: FriendshipItem(
        item_name="Skuntank Friendship",
        item_id=0x43,
    ),
    FRIENDSHIP_ITEMS["Haunter"]: FriendshipItem(
        item_name="Haunter Friendship",
        item_id=0x44,
    ),
    FRIENDSHIP_ITEMS["Scyther"]: FriendshipItem(
        item_name="Scyther Friendship",
        item_id=0x45,
    ),
    FRIENDSHIP_ITEMS["Absol"]: FriendshipItem(
        item_name="Absol Friendship",
        item_id=0x46,
    ),
    FRIENDSHIP_ITEMS["Scizor"]: FriendshipItem(
        item_name="Scizor Friendship",
        item_id=0x47,
    ),
    FRIENDSHIP_ITEMS["Quilava"]: FriendshipItem(
        item_name="Quilava Friendship",
        item_id=0x48,
    ),
    FRIENDSHIP_ITEMS["Eevee"]: FriendshipItem(
        item_name="Eevee Friendship",
        item_id=0x49,
    ),
    FRIENDSHIP_ITEMS["Flareon"]: FriendshipItem(
        item_name="Flareon Friendship",
        item_id=0x4a,
    ),
    FRIENDSHIP_ITEMS["Vaporeon"]: FriendshipItem(
        item_name="Vaporeon Friendship",
        item_id=0x4b,
    ),
    FRIENDSHIP_ITEMS["Glaceon"]: FriendshipItem(
        item_name="Glaceon Friendship",
        item_id=0x4c,
    ),
    FRIENDSHIP_ITEMS["Jolteon"]: FriendshipItem(
        item_name="Jolteon Friendship",
        item_id=0x4d,
    ),
    FRIENDSHIP_ITEMS["Espeon"]: FriendshipItem(
        item_name="Espeon Friendship",
        item_id=0x4e,
    ),
    FRIENDSHIP_ITEMS["Umbreon"]: FriendshipItem(
        item_name="Umbreon Friendship",
        item_id=0x4f,
    ),
    FRIENDSHIP_ITEMS["Leafeon"]: FriendshipItem(
        item_name="Leafeon Friendship",
        item_id=0x50,
    ),
    FRIENDSHIP_ITEMS["Froslass"]: FriendshipItem(
        item_name="Froslass Friendship",
        item_id=0x51,
    ),
    FRIENDSHIP_ITEMS["Ninetales"]: FriendshipItem(
        item_name="Ninetales Friendship",
        item_id=0x52,
    ),
    FRIENDSHIP_ITEMS["Mawile"]: FriendshipItem(
        item_name="Mawile Friendship",
        item_id=0x53,
    ),
    FRIENDSHIP_ITEMS["Primeape"]: FriendshipItem(
        item_name="Primeape Friendship",
        item_id=0x54,
    ),
    FRIENDSHIP_ITEMS["Farfetch'd"]: FriendshipItem(
        item_name="Farfetch'd Friendship",
        item_id=0x55,
    ),
    FRIENDSHIP_ITEMS["Piloswine"]: FriendshipItem(
        item_name="Piloswine Friendship",
        item_id=0x56,
    ),
    FRIENDSHIP_ITEMS["Torkoal"]: FriendshipItem(
        item_name="Torkoal Friendship",
        item_id=0x57,
    ),
    FRIENDSHIP_ITEMS["Magcargo"]: FriendshipItem(
        item_name="Magcargo Friendship",
        item_id=0x58,
    ),
    FRIENDSHIP_ITEMS["Wingull"]: FriendshipItem(
        item_name="Wingull Friendship",
        item_id=0x59,
    ),
    FRIENDSHIP_ITEMS["Pelipper"]: FriendshipItem(
        item_name="Pelipper Friendship",
        item_id=0x5a,
    ),
    FRIENDSHIP_ITEMS["Krabby"]: FriendshipItem(
        item_name="Krabby Friendship",
        item_id=0x5b,
    ),
    FRIENDSHIP_ITEMS["Zubat"]: FriendshipItem(
        item_name="Zubat Friendship",
        item_id=0x5c,
    ),
    FRIENDSHIP_ITEMS["Geodude"]: FriendshipItem(
        item_name="Geodude Friendship",
        item_id=0x5d,
    ),
    FRIENDSHIP_ITEMS["Abra"]: FriendshipItem(
        item_name="Abra Friendship",
        item_id=0x5e,
    ),
    FRIENDSHIP_ITEMS["Voltorb"]: FriendshipItem(
        item_name="Voltorb Friendship",
        item_id=0x5f,
    ),
    FRIENDSHIP_ITEMS["Electrode"]: FriendshipItem(
        item_name="Electrode Friendship",
        item_id=0x60,
    ),
    FRIENDSHIP_ITEMS["Drifloon"]: FriendshipItem(
        item_name="Drifloon Friendship",
        item_id=0x61,
    ),
    FRIENDSHIP_ITEMS["Drifblim"]: FriendshipItem(
        item_name="Drifblim Friendship",
        item_id=0x62,
    ),
    FRIENDSHIP_ITEMS["Rayquaza"]: FriendshipItem(
        item_name="Rayquaza Friendship",
        item_id=0x63,
    ),
    FRIENDSHIP_ITEMS["Dugtrio"]: FriendshipItem(
        item_name="Dugtrio Friendship",
        item_id=0x64,
    ),
    FRIENDSHIP_ITEMS["Breloom"]: FriendshipItem(
        item_name="Breloom Friendship",
        item_id=0x65,
    ),
    FRIENDSHIP_ITEMS["Infernape"]: FriendshipItem(
        item_name="Infernape Friendship",
        item_id=0x66,
    ),
    FRIENDSHIP_ITEMS["Lopunny"]: FriendshipItem(
        item_name="Lopunny Friendship",
        item_id=0x67,
    ),
    FRIENDSHIP_ITEMS["Venusaur"]: FriendshipItem(
        item_name="Venusaur Friendship",
        item_id=0x68,
    ),
    FRIENDSHIP_ITEMS["Quagsire"]: FriendshipItem(
        item_name="Quagsire Friendship",
        item_id=0x69,
    ),
    FRIENDSHIP_ITEMS["Blaziken"]: FriendshipItem(
        item_name="Blaziken Friendship",
        item_id=0x6a,
    ),
    FRIENDSHIP_ITEMS["Sudowoodo"]: FriendshipItem(
        item_name="Sudowoodo Friendship",
        item_id=0x6b,
    ),
    FRIENDSHIP_ITEMS["Spheal"]: FriendshipItem(
        item_name="Spheal Friendship",
        item_id=0x6c,
    ),
    FRIENDSHIP_ITEMS["Prinplup"]: FriendshipItem(
        item_name="Prinplup Friendship",
        item_id=0x6d,
    ),
    FRIENDSHIP_ITEMS["Cranidos"]: FriendshipItem(
        item_name="Cranidos Friendship",
        item_id=0x6e,
    ),
    FRIENDSHIP_ITEMS["Camerupt"]: FriendshipItem(
        item_name="Camerupt Friendship",
        item_id=0x6f,
    ),
    FRIENDSHIP_ITEMS["Marowak"]: FriendshipItem(
        item_name="Marowak Friendship",
        item_id=0x70,
    ),
    FRIENDSHIP_ITEMS["Machamp"]: FriendshipItem(
        item_name="Machamp Friendship",
        item_id=0x71,
    ),
    FRIENDSHIP_ITEMS["Budew"]: FriendshipItem(
        item_name="Budew Friendship",
        item_id=0x72,
    ),
    FRIENDSHIP_ITEMS["Spinarak"]: FriendshipItem(
        item_name="Spinarak Friendship",
        item_id=0x73,
    ),
    FRIENDSHIP_ITEMS["Golem"]: FriendshipItem(
        item_name="Golem Friendship",
        item_id=0x74,
    ),
    FRIENDSHIP_ITEMS["Rhyperior"]: FriendshipItem(
        item_name="Rhyperior Friendship",
        item_id=0x75,
    ),
    FRIENDSHIP_ITEMS["Magmortar"]: FriendshipItem(
        item_name="Magmortar Friendship",
        item_id=0x76,
    ),
    FRIENDSHIP_ITEMS["Arcanine"]: FriendshipItem(
        item_name="Arcanine Friendship",
        item_id=0x77,
    ),
    FRIENDSHIP_ITEMS["Wailord"]: FriendshipItem(
        item_name="Wailord Friendship",
        item_id=0x78,
    ),
    FRIENDSHIP_ITEMS["Sableye"]: FriendshipItem(
        item_name="Sableye Friendship",
        item_id=0x79,
    ),
    FRIENDSHIP_ITEMS["Kirlia"]: FriendshipItem(
        item_name="Kirlia Friendship",
        item_id=0x7a,
    ),
    FRIENDSHIP_ITEMS["Metapod"]: FriendshipItem(
        item_name="Metapod Friendship",
        item_id=0x7b,
    ),
    FRIENDSHIP_ITEMS["Burmy"]: FriendshipItem(
        item_name="Burmy Friendship",
        item_id=0x7c,
    ),
    FRIENDSHIP_ITEMS["Meowth"]: FriendshipItem(
        item_name="Meowth Friendship",
        item_id=0x7d,
    ),
    FRIENDSHIP_ITEMS["Floatzel"]: FriendshipItem(
        item_name="Floatzel Friendship",
        item_id=0x7e,
    ),
    FRIENDSHIP_ITEMS["Carvanha"]: FriendshipItem(
        item_name="Carvanha Friendship",
        item_id=0x7f,
    ),
    FRIENDSHIP_ITEMS["Sharpedo"]: FriendshipItem(
        item_name="Sharpedo Friendship",
        item_id=0x80,
    ),
    FRIENDSHIP_ITEMS["Sneasel"]: FriendshipItem(
        item_name="Sneasel Friendship",
        item_id=0x81,
    ),
    FRIENDSHIP_ITEMS["Glalie"]: FriendshipItem(
        item_name="Glalie Friendship",
        item_id=0x82,
    ),
    FRIENDSHIP_ITEMS["Mamoswine"]: FriendshipItem(
        item_name="Mamoswine Friendship",
        item_id=0x83,
    ),
    FRIENDSHIP_ITEMS["Mr. Mime"]: FriendshipItem(
        item_name="Mr. Mime Friendship",
        item_id=0x84,
    ),
    FRIENDSHIP_ITEMS["Bastiodon"]: FriendshipItem(
        item_name="Bastiodon Friendship",
        item_id=0x85,
    ),
    FRIENDSHIP_ITEMS["Ursaring"]: FriendshipItem(
        item_name="Ursaring Friendship",
        item_id=0x86,
    ),
    FRIENDSHIP_ITEMS["Vulpix"]: FriendshipItem(
        item_name="Vulpix Friendship",
        item_id=0x87,
    ),
    FRIENDSHIP_ITEMS["Rotom"]: FriendshipItem(
        item_name="Rotom Friendship",
        item_id=0x88,
    ),
    FRIENDSHIP_ITEMS["Butterfree"]: FriendshipItem(
        item_name="Butterfree Friendship",
        item_id=0x8e,
    ),
    FRIENDSHIP_ITEMS["Spearow"]: FriendshipItem(
        item_name="Spearow Friendship",
        item_id=0x8f,
    ),
    FRIENDSHIP_ITEMS["Pidgeotto"]: FriendshipItem(
        item_name="Pidgeotto Friendship",
        item_id=0x90,
    ),
    FRIENDSHIP_ITEMS["Hoppip"]: FriendshipItem(
        item_name="Hoppip Friendship",
        item_id=0x91,
    ),
    FRIENDSHIP_ITEMS["Jumpluff"]: FriendshipItem(
        item_name="Jumpluff Friendship",
        item_id=0x92,
    ),
    FRIENDSHIP_ITEMS["Gliscor"]: FriendshipItem(
        item_name="Gliscor Friendship",
        item_id=0x93,
    ),
    FRIENDSHIP_ITEMS["Togekiss"]: FriendshipItem(
        item_name="Togekiss Friendship",
        item_id=0x94,
    ),
    FRIENDSHIP_ITEMS["Golbat"]: FriendshipItem(
        item_name="Golbat Friendship",
        item_id=0x95,
    ),
    FRIENDSHIP_ITEMS["Honchkrow"]: FriendshipItem(
        item_name="Honchkrow Friendship",
        item_id=0x96,
    ),
    FRIENDSHIP_ITEMS["Magnezone"]: FriendshipItem(
        item_name="Magnezone Friendship",
        item_id=0x97,
    ),
    FRIENDSHIP_ITEMS["Dragonite"]: FriendshipItem(
        item_name="Dragonite Friendship",
        item_id=0x98,
    ),
    FRIENDSHIP_ITEMS["Snorlax"]: FriendshipItem(
        item_name="Snorlax Friendship",
        item_id=0x99,
    ),
    FRIENDSHIP_ITEMS["Garchomp"]: FriendshipItem(
        item_name="Garchomp Friendship",
        item_id=0x9a,
    ),
    FRIENDSHIP_ITEMS["Aerodactyl"]: FriendshipItem(
        item_name="Aerodactyl Friendship",
        item_id=0x9b,
    ),
    FRIENDSHIP_ITEMS["Flygon"]: FriendshipItem(
        item_name="Flygon Friendship",
        item_id=0x9c,
    ),
    FRIENDSHIP_ITEMS["Salamence"]: FriendshipItem(
        item_name="Salamence Friendship",
        item_id=0x9d,
    ),
    FRIENDSHIP_ITEMS["Lapras"]: FriendshipItem(
        item_name="Lapras Friendship",
        item_id=0x9e,
    ),
    FRIENDSHIP_ITEMS["Furret"]: FriendshipItem(
        item_name="Furret Friendship",
        item_id=0x9f,
    ),
    FRIENDSHIP_ITEMS["Gastly"]: FriendshipItem(
        item_name="Gastly Friendship",
        item_id=0xa0,
    ),
    FRIENDSHIP_ITEMS["Slowpoke"]: FriendshipItem(
        item_name="Slowpoke Friendship",
        item_id=0xa1,
    ),
    FRIENDSHIP_ITEMS["Teddiursa"]: FriendshipItem(
        item_name="Teddiursa Friendship",
        item_id=0xa2,
    ),
    FRIENDSHIP_ITEMS["Baltoy"]: FriendshipItem(
        item_name="Baltoy Friendship",
        item_id=0xa3,
    ),
    FRIENDSHIP_ITEMS["Claydol"]: FriendshipItem(
        item_name="Claydol Friendship",
        item_id=0xa4,
    ),
    FRIENDSHIP_ITEMS["Bronzor"]: FriendshipItem(
        item_name="Bronzor Friendship",
        item_id=0xa5,
    ),
    FRIENDSHIP_ITEMS["Mismagius"]: FriendshipItem(
        item_name="Mismagius Friendship",
        item_id=0xa6,
    ),
    FRIENDSHIP_ITEMS["Raichu"]: FriendshipItem(
        item_name="Raichu Friendship",
        item_id=0xa7,
    ),
    FRIENDSHIP_ITEMS["Luxray"]: FriendshipItem(
        item_name="Luxray Friendship",
        item_id=0xa8,
    ),
    FRIENDSHIP_ITEMS["Tyranitar"]: FriendshipItem(
        item_name="Tyranitar Friendship",
        item_id=0xa9,
    ),
    FRIENDSHIP_ITEMS["Hitmonlee"]: FriendshipItem(
        item_name="Hitmonlee Friendship",
        item_id=0xaa,
    ),
    FRIENDSHIP_ITEMS["Hitmonchan"]: FriendshipItem(
        item_name="Hitmonchan Friendship",
        item_id=0xab,
    ),
    FRIENDSHIP_ITEMS["Psyduck"]: FriendshipItem(
        item_name="Psyduck Friendship",
        item_id=0xac,
    ),
    FRIENDSHIP_ITEMS["Taillow"]: FriendshipItem(
        item_name="Taillow Friendship",
        item_id=0xad,
    ),
    FRIENDSHIP_ITEMS["Shinx"]: FriendshipItem(
        item_name="Shinx Friendship",
        item_id=0xae,
    ),
    FRIENDSHIP_ITEMS["Hitmontop"]: FriendshipItem(
        item_name="Hitmontop Friendship",
        item_id=0xaf,
    ),
    FRIENDSHIP_ITEMS["Ponyta"]: FriendshipItem(
        item_name="Ponyta Friendship",
        item_id=0xb0,
    ),
    FRIENDSHIP_ITEMS["Metagross"]: FriendshipItem(
        item_name="Metagross Friendship",
        item_id=0xb1,
    ),
    FRIENDSHIP_ITEMS["Electivire"]: FriendshipItem(
        item_name="Electivire Friendship",
        item_id=0xb2,
    ),
    FRIENDSHIP_ITEMS["Mudkip"]: FriendshipItem(
        item_name="Mudkip Friendship",
        item_id=0xb3,
    ),
    FRIENDSHIP_ITEMS["Totodile"]: FriendshipItem(
        item_name="Totodile Friendship",
        item_id=0xb4,
    ),
    FRIENDSHIP_ITEMS["Charmander"]: FriendshipItem(
        item_name="Charmander Friendship",
        item_id=0xb5,
    ),
    FRIENDSHIP_ITEMS["Chikorita"]: FriendshipItem(
        item_name="Chikorita Friendship",
        item_id=0xb6,
    ),
    FRIENDSHIP_ITEMS["Cyndaquil"]: FriendshipItem(
        item_name="Cyndaquil Friendship",
        item_id=0xb7,
    ),
    FRIENDSHIP_ITEMS["Corsola"]: FriendshipItem(
        item_name="Corsola Friendship",
        item_id=0xb8,
    ),
    FRIENDSHIP_ITEMS["Tangrowth"]: FriendshipItem(
        item_name="Tangrowth Friendship",
        item_id=0xb9,
    ),
    FRIENDSHIP_ITEMS["Dusknoir"]: FriendshipItem(
        item_name="Dusknoir Friendship",
        item_id=0xba,
    ),
    FRIENDSHIP_ITEMS["Celebi"]: FriendshipItem(
        item_name="Celebi Friendship",
        item_id=0xbb,
    ),
    FRIENDSHIP_ITEMS["Latias"]: FriendshipItem(
        item_name="Latias Friendship",
        item_id=0xbc,
    ),
    FRIENDSHIP_ITEMS["Latios"]: FriendshipItem(
        item_name="Latios Friendship",
        item_id=0xbd,
    ),
    FRIENDSHIP_ITEMS["Groudon"]: FriendshipItem(
        item_name="Groudon Friendship",
        item_id=0xbf,
    ),
    FRIENDSHIP_ITEMS["Jirachi"]: FriendshipItem(
        item_name="Jirachi Friendship",
        item_id=0xc0,
    ),
    FRIENDSHIP_ITEMS["Heatran"]: FriendshipItem(
        item_name="Heatran Friendship",
        item_id=0xc1,
    ),
    FRIENDSHIP_ITEMS["Manaphy"]: FriendshipItem(
        item_name="Manaphy Friendship",
        item_id=0xc2,
    ),
    FRIENDSHIP_ITEMS["Darkrai"]: FriendshipItem(
        item_name="Darkrai Friendship",
        item_id=0xc3,
    ),
    FRIENDSHIP_ITEMS["Suicune"]: FriendshipItem(
        item_name="Suicune Friendship",
        item_id=0xc4,
    ),
    FRIENDSHIP_ITEMS["Deoxys"]: FriendshipItem(
        item_name="Deoxys Friendship",
        item_id=0xc5,
    ),
    FRIENDSHIP_ITEMS["Delibird"]: FriendshipItem(
        item_name="Delibird Friendship",
        item_id=0xc6,
    ),
    FRIENDSHIP_ITEMS["Octillery"]: FriendshipItem(
        item_name="Octillery Friendship",
        item_id=0xc7,
    ),
    FRIENDSHIP_ITEMS["Porygon-Z"]: FriendshipItem(
        item_name="Porygon-Z Friendship",
        item_id=0xc8,
    ),

    UNLOCK_ITEMS["Pachirisu Unlock"]: UnlockItem(
        item_name="Pachirisu Unlock",
        item_id=0x04
    ),
    UNLOCK_ITEMS["Chimchar Unlock"]: UnlockItem(
        item_name="Chimchar Unlock",
        item_id=0x07
    ),
    UNLOCK_ITEMS["Magikarp Unlock"]: UnlockItem(
        item_name="Magikarp Unlock",
        item_id=0x08
    ),
    UNLOCK_ITEMS["Lotad Unlock"]: UnlockItem(
        item_name="Lotad Unlock",
        item_id=0x09
    ),
    UNLOCK_ITEMS["Caterpie Unlock"]: UnlockItem(
        item_name="Caterpie Unlock",
        item_id=0x0a
    ),
    UNLOCK_ITEMS["Weedle Unlock"]: UnlockItem(
        item_name="Weedle Unlock",
        item_id=0x0b
    ),
    UNLOCK_ITEMS["Shroomish Unlock"]: UnlockItem(
        item_name="Shroomish Unlock",
        item_id=0x0e
    ),
    UNLOCK_ITEMS["Bonsly Unlock"]: UnlockItem(
        item_name="Bonsly Unlock",
        item_id=0x0f
    ),
    UNLOCK_ITEMS["Shinx Unlock"]: UnlockItem(
        item_name="Shinx Unlock",
        item_id=0x10
    ),
    UNLOCK_ITEMS["Torterra Unlock"]: UnlockItem(
        item_name="Torterra Unlock",
        item_id=0x14
    ),
    UNLOCK_ITEMS["Starly Unlock"]: UnlockItem(
        item_name="Starly Unlock",
        item_id=0x15
    ),
    UNLOCK_ITEMS["Butterfree Unlock"]: UnlockItem(
        item_name="Butterfree Unlock",
        item_id=0x16
    ),
    UNLOCK_ITEMS["Tropius Unlock"]: UnlockItem(
        item_name="Tropius Unlock",
        item_id=0x17
    ),
    UNLOCK_ITEMS["Bibarel Unlock"]: UnlockItem(
        item_name="Bibarel Unlock",
        item_id=0x18
    ),
    UNLOCK_ITEMS["Ambipom Unlock"]: UnlockItem(
        item_name="Ambipom Unlock",
        item_id=0x19
    ),
    UNLOCK_ITEMS["Ponyta Unlock"]: UnlockItem(
        item_name="Ponyta Unlock",
        item_id=0x1a
    ),
    UNLOCK_ITEMS["Scyther Unlock"]: UnlockItem(
        item_name="Scyther Unlock",
        item_id=0x1b
    ),
    # UNLOCK_ITEMS["Drifblim Unlock"]: UnlockItem(
    #     item_name="Drifblim Unlock",
    #     item_id=0x1f
    # ),
    UNLOCK_ITEMS["Bidoof Unlock"]: UnlockItem(
        item_name="Bidoof Unlock",
        item_id=0x20
    ),
    UNLOCK_ITEMS["Bidoof Unlock 2"]: UnlockItem(
        item_name="Bidoof Unlock 2",
        item_id=0x21
    ),
    UNLOCK_ITEMS["Bidoof Unlock 3"]: UnlockItem(
        item_name="Bidoof Unlock 3",
        item_id=0x22
    ),
    UNLOCK_ITEMS["Starly Unlock 2"]: UnlockItem(
        item_name="Starly Unlock 2",
        item_id=0x22
    ),
    UNLOCK_ITEMS["Krabby Unlock"]: UnlockItem(
        item_name="Krabby Unlock",
        item_id=0x31
    ),
    UNLOCK_ITEMS["Totodile Unlock"]: UnlockItem(
        item_name="Totodile Unlock",
        item_id=0x32
    ),
    UNLOCK_ITEMS["Mudkip Unlock"]: UnlockItem(
        item_name="Mudkip Unlock",
        item_id=0x33
    ),
    UNLOCK_ITEMS["Corphish Unlock"]: UnlockItem(
        item_name="Corphish Unlock",
        item_id=0x34
    ),
    UNLOCK_ITEMS["Golduck Unlock"]: UnlockItem(
        item_name="Golduck Unlock",
        item_id=0x39
    ),
    UNLOCK_ITEMS["Floatzel Unlock"]: UnlockItem(
        item_name="Floatzel Unlock",
        item_id=0x3a
    ),
    UNLOCK_ITEMS["Blastoise Unlock"]: UnlockItem(
        item_name="Blastoise Unlock",
        item_id=0x3d
    ),
    UNLOCK_ITEMS["Sneasel Unlock"]: UnlockItem(
        item_name="Sneasel Unlock",
        item_id=0x48
    ),
    UNLOCK_ITEMS["Delibird Unlock"]: UnlockItem(
        item_name="Delibird Unlock",
        item_id=0x4a
    ),
    UNLOCK_ITEMS["Smoochum Unlock"]: UnlockItem(
        item_name="Smoochum Unlock",
        item_id=0x4b
    ),
    UNLOCK_ITEMS["Squirtle Unlock"]: UnlockItem(
        item_name="Squirtle Unlock",
        item_id=0x4c
    ),
    UNLOCK_ITEMS["Primeape Unlock"]: UnlockItem(
        item_name="Primeape Unlock",
        item_id=0x4e
    ),
    UNLOCK_ITEMS["Ursaring Unlock"]: UnlockItem(
        item_name="Ursaring Unlock",
        item_id=0x4f
    ),
    UNLOCK_ITEMS["Mamoswine Unlock"]: UnlockItem(
        item_name="Mamoswine Unlock",
        item_id=0x53
    ),
    UNLOCK_ITEMS["Sudowoodo Unlock"]: UnlockItem(
        item_name="Sudowoodo Unlock",
        item_id=0x57
    ),
    UNLOCK_ITEMS["Magnemite Unlock"]: UnlockItem(
        item_name="Magnemite Unlock",
        item_id=0x58
    ),
    UNLOCK_ITEMS["Phanpy Unlock"]: UnlockItem(
        item_name="Phanpy Unlock",
        item_id=0x59
    ),
    UNLOCK_ITEMS["Raichu Unlock"]: UnlockItem(
        item_name="Raichu Unlock",
        item_id=0x5f
    ),
    UNLOCK_ITEMS["Hitmonlee Unlock"]: UnlockItem(
        item_name="Hitmonlee Unlock",
        item_id=0x60
    ),
    UNLOCK_ITEMS["Electivire Unlock"]: UnlockItem(
        item_name="Electivire Unlock",
        item_id=0x61
    ),
    UNLOCK_ITEMS["Torkoal Unlock"]: UnlockItem(
        item_name="Torkoal Unlock",
        item_id=0x63
    ),
    UNLOCK_ITEMS["Claydol Unlock"]: UnlockItem(
        item_name="Claydol Unlock",
        item_id=0x65
    ),
    UNLOCK_ITEMS["Electabuzz Unlock"]: UnlockItem(
        item_name="Electabuzz Unlock",
        item_id=0x66
    ),
    UNLOCK_ITEMS["Magnezone Unlock"]: UnlockItem(
        item_name="Magnezone Unlock",
        item_id=0x67
    ),
    UNLOCK_ITEMS["Hitmonchan Unlock"]: UnlockItem(
        item_name="Hitmonchan Unlock",
        item_id=0x69
    ),
    UNLOCK_ITEMS["Infernape Unlock"]: UnlockItem(
        item_name="Infernape Unlock",
        item_id=0x6b
    ),
    UNLOCK_ITEMS["Golem Unlock"]: UnlockItem(
        item_name="Golem Unlock",
        item_id=0x6c
    ),
    UNLOCK_ITEMS["Golem Unlock"]: UnlockItem(
        item_name="Golem Unlock",
        item_id=0x6c
    ),
    UNLOCK_ITEMS["Kakuna Unlock"]: UnlockItem(
        item_name="Kakuna Unlock",
        item_id=0x71
    ),
    UNLOCK_ITEMS["Metapod Unlock"]: UnlockItem(
        item_name="Metapod Unlock",
        item_id=0x72
    ),
    UNLOCK_ITEMS["Breloom Unlock"]: UnlockItem(
        item_name="Breloom Unlock",
        item_id=0x74
    ),
    UNLOCK_ITEMS["Ninetales Unlock"]: UnlockItem(
        item_name="Ninetales Unlock",
        item_id=0x75
    ),
    UNLOCK_ITEMS["Haunter Unlock"]: UnlockItem(
        item_name="Haunter Unlock",
        item_id=0x7d
    ),
    UNLOCK_ITEMS["Skuntank Unlock"]: UnlockItem(
        item_name="Skuntank Unlock",
        item_id=0x7f
    ),
    UNLOCK_ITEMS["Mismagius Unlock"]: UnlockItem(
        item_name="Mismagius Unlock",
        item_id=0x80
    ),
    UNLOCK_ITEMS["Luxray Unlock"]: UnlockItem(
        item_name="Luxray Unlock",
        item_id=0x81
    ),
    UNLOCK_ITEMS["Espeon Unlock"]: UnlockItem(
        item_name="Espeon Unlock",
        item_id=0x82
    ),
    UNLOCK_ITEMS["Gengar Unlock"]: UnlockItem(
        item_name="Gengar Unlock",
        item_id=0x83
    ),
    UNLOCK_ITEMS["Dusknoir Unlock"]: UnlockItem(
        item_name="Dusknoir Unlock",
        item_id=0x84
    ),
    UNLOCK_ITEMS["Garchomp Unlock"]: UnlockItem(
        item_name="Garchomp Unlock",
        item_id=0x85
    ),
    UNLOCK_ITEMS["Tyranitar Unlock"]: UnlockItem(
        item_name="Tyranitar Unlock",
        item_id=0x86
    ),
    UNLOCK_ITEMS["Jolteon Unlock"]: UnlockItem(
        item_name="Jolteon Unlock",
        item_id=0x8d
    ),
    UNLOCK_ITEMS["Rayquaza Unlock"]: UnlockItem(
        item_name="Rayquaza Unlock",
        item_id=0x95
    ),
    UNLOCK_ITEMS["Machamp Unlock"]: UnlockItem(
        item_name="Machamp Unlock",
        item_id=0x99
    ),
    UNLOCK_ITEMS["Diglett Unlock"]: UnlockItem(
        item_name="Diglett Unlock",
        item_id=0x9a
    ),
    UNLOCK_ITEMS["Baltoy Unlock"]: UnlockItem(
        item_name="Baltoy Unlock",
        item_id=0x9d
    ),
    UNLOCK_ITEMS["Magmortar Unlock"]: UnlockItem(
        item_name="Magmortar Unlock",
        item_id=0x9e
    ),
    UNLOCK_ITEMS["Honchkrow Unlock"]: UnlockItem(
        item_name="Honchkrow Unlock",
        item_id=0xa0
    ),
    UNLOCK_ITEMS["Stunky Unlock"]: UnlockItem(
        item_name="Stunky Unlock",
        item_id=0xa1
    ),
    UNLOCK_ITEMS["Gastly Unlock"]: UnlockItem(
        item_name="Gastly Unlock",
        item_id=0xa2
    ),
    UNLOCK_ITEMS["Electrode Unlock"]: UnlockItem(
        item_name="Electrode Unlock",
        item_id=0xa3
    ),
    UNLOCK_ITEMS["Gastly Unlock 2"]: UnlockItem(
        item_name="Gastly Unlock 2",
        item_id=0xa7
    ),
    UNLOCK_ITEMS["Magnemite Unlock 2"]: UnlockItem(
        item_name="Magnemite Unlock 2",
        item_id=0xa8
    ),
    UNLOCK_ITEMS["Magnemite Unlock 3"]: UnlockItem(
        item_name="Magnemite Unlock 3",
        item_id=0xa9
    ),
    UNLOCK_ITEMS["Elekid Unlock"]: UnlockItem(
        item_name="Elekid Unlock",
        item_id=0xad
    ),
    UNLOCK_ITEMS["Aerodactyl Unlock"]: UnlockItem(
        item_name="Aerodactyl Unlock",
        item_id=0xb4
    ),
    UNLOCK_ITEMS["Voltorb Unlock"]: UnlockItem(
        item_name="Voltorb Unlock",
        item_id=0xb7
    ),
    UNLOCK_ITEMS["Glalie Unlock"]: UnlockItem(
        item_name="Glalie Unlock",
        item_id=0xb8
    ),
    POWERS["Progressive Dash"]: PowerItem(
        item_name="Progressive Dash",
        item_id=0x01
    ),
    POWERS["Progressive Thunderbolt"]: PowerItem(
        item_name="Progressive Thunderbolt",
        item_id=0x02
    ),
    POWERS["Progressive Health"]: PowerItem(
        item_name="Progressive Health",
        item_id=0x03
    ),
    POWERS["Progressive Iron Tail"]: PowerItem(
        item_name="Progressive Iron Tail",
        item_id=0x04
    ),

    PRISM_ITEM["Absol Prisma"]: PrismaItem(
        item_name="Absol Prisma",
        item_id=0x00
    ),
    PRISM_ITEM["Rayquaza Prisma"]: PrismaItem(
        item_name="Rayquaza Prisma",
        item_id=0x01
    ),
    PRISM_ITEM["Venusaur Prisma"]: PrismaItem(
        item_name="Venusaur Prisma",
        item_id=0x02
    ),
    PRISM_ITEM["Tangrowth Prisma"]: PrismaItem(
        item_name="Tangrowth Prisma",
        item_id=0x03
    ),
    PRISM_ITEM["Dusknoir Prisma"]: PrismaItem(
        item_name="Dusknoir Prisma",
        item_id=0x04
    ),
    PRISM_ITEM["Gyarados Prisma"]: PrismaItem(
        item_name="Gyarados Prisma",
        item_id=0x05
    ),
    PRISM_ITEM["Pelipper Prisma"]: PrismaItem(
        item_name="Pelipper Prisma",
        item_id=0x06
    ),
    PRISM_ITEM["Empoleon Prisma"]: PrismaItem(
        item_name="Empoleon Prisma",
        item_id=0x08
    ),
    PRISM_ITEM["Bastiodon Prisma"]: PrismaItem(
        item_name="Bastiodon Prisma",
        item_id=0x09
    ),
    PRISM_ITEM["Rhyperior Prisma"]: PrismaItem(
        item_name="Rhyperior Prisma",
        item_id=0x0a
    ),
    PRISM_ITEM["Blaziken Prisma"]: PrismaItem(
        item_name="Blaziken Prisma",
        item_id=0x0b
    ),
    PRISM_ITEM["Rotom Prisma"]: PrismaItem(
        item_name="Rotom Prisma",
        item_id=0x0c
    ),
    PRISM_ITEM["Salamence Prisma"]: PrismaItem(
        item_name="Salamence Prisma",
        item_id=0x0e
    ),
    PRISM_ITEM["Bulbasaur Prisma"]: PrismaItem(
        item_name="Bulbasaur Prisma",
        item_id=0x0f
    ),
    BERRIES["10 Berries"]: BerryItem(
        item_name="10 Berries",
        item_id=0x0a
    ),
    BERRIES["20 Berries"]: BerryItem(
        item_name="20 Berries",
        item_id=0x14
    ),
    BERRIES["50 Berries"]: BerryItem(
        item_name="50 Berries",
        item_id=0x32
    ),
    BERRIES["100 Berries"]: BerryItem(
        item_name="100 Berries",
        item_id=0x64
    ),
}

LOCATIONS: List[BaseLocation] = [
    FriendshipLocation(
        location_name="Turtwig Overworld",
        structure_position=0,
        location_ids=[FRIENDSHIP_ITEMS["Turtwig"], UNLOCK_ITEMS["Pachirisu Unlock"], UNLOCK_ITEMS["Bonsly Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Torterra Overworld",
        structure_position=1,
        location_ids=[FRIENDSHIP_ITEMS["Torterra"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Treecko Overworld",
        structure_position=2,
        location_ids=[FRIENDSHIP_ITEMS["Treecko"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Pachirisu Overworld",
        structure_position=3,
        location_ids=[FRIENDSHIP_ITEMS["Pachirisu"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Lotad Overworld",
        structure_position=4,
        location_ids=[FRIENDSHIP_ITEMS["Lotad"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Bidoof Overworld",
        structure_position=5,
        location_ids=[FRIENDSHIP_ITEMS["Bidoof"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Bibarel Overworld",
        structure_position=6,
        location_ids=[FRIENDSHIP_ITEMS["Bibarel"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Weedle Overworld",
        structure_position=7,
        location_ids=[FRIENDSHIP_ITEMS["Weedle"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Caterpie Overworld",
        structure_position=8,
        location_ids=[FRIENDSHIP_ITEMS["Caterpie"], UNLOCK_ITEMS["Butterfree Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Butterfree Overworld",
        structure_position=9,
        location_ids=[FRIENDSHIP_ITEMS["Butterfree"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Munchlax Overworld",
        structure_position=10,
        location_ids=[FRIENDSHIP_ITEMS["Munchlax"], UNLOCK_ITEMS["Tropius Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Snorlax Overworld",
        structure_position=11,
        location_ids=[FRIENDSHIP_ITEMS["Snorlax"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Bonsly Overworld",
        structure_position=12,
        location_ids=[FRIENDSHIP_ITEMS["Bonsly"], UNLOCK_ITEMS["Sudowoodo Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Sudowoodo Overworld",
        structure_position=13,
        location_ids=[FRIENDSHIP_ITEMS["Sudowoodo"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Shroomish Overworld",
        structure_position=14,
        location_ids=[FRIENDSHIP_ITEMS["Shroomish"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Breloom Overworld",
        structure_position=15,
        location_ids=[FRIENDSHIP_ITEMS["Breloom"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Mankey Overworld",
        structure_position=16,
        location_ids=[FRIENDSHIP_ITEMS["Mankey"], UNLOCK_ITEMS["Chimchar Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Primeape Overworld",
        structure_position=17,
        location_ids=[FRIENDSHIP_ITEMS["Primeape"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Buneary Overworld",
        structure_position=18,
        location_ids=[FRIENDSHIP_ITEMS["Buneary"], UNLOCK_ITEMS["Lotad Unlock"], UNLOCK_ITEMS["Shinx Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Lopunny Overworld",
        structure_position=19,
        location_ids=[FRIENDSHIP_ITEMS["Lopunny"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Starly Overworld",
        structure_position=20,
        location_ids=[FRIENDSHIP_ITEMS["Starly"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Staravia Overworld",
        structure_position=21,
        location_ids=[FRIENDSHIP_ITEMS["Staravia"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Staraptor Overworld",
        structure_position=22,
        location_ids=[FRIENDSHIP_ITEMS["Staraptor"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Oddish Overworld",
        structure_position=23,
        location_ids=[FRIENDSHIP_ITEMS["Oddish"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Bellossom Overworld",
        structure_position=24,
        location_ids=[FRIENDSHIP_ITEMS["Bellossom"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Spearow Overworld",
        structure_position=25,
        location_ids=[FRIENDSHIP_ITEMS["Spearow"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Tropius Overworld",
        structure_position=26,
        location_ids=[FRIENDSHIP_ITEMS["Tropius"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Shinx Overworld",
        structure_position=27,
        location_ids=[FRIENDSHIP_ITEMS["Shinx"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Luxray Overworld",
        structure_position=28,
        location_ids=[FRIENDSHIP_ITEMS["Luxray"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Ponyta Overworld",
        structure_position=29,
        location_ids=[FRIENDSHIP_ITEMS["Ponyta"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Aipom Overworld",
        structure_position=30,
        location_ids=[FRIENDSHIP_ITEMS["Aipom"], UNLOCK_ITEMS["Ambipom Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Ambipom Overworld",
        structure_position=31,
        location_ids=[FRIENDSHIP_ITEMS["Ambipom"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Scyther Overworld",
        structure_position=32,
        location_ids=[FRIENDSHIP_ITEMS["Scyther"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Scizor Overworld",
        structure_position=33,
        location_ids=[FRIENDSHIP_ITEMS["Scizor"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Croagunk Overworld",
        structure_position=34,
        location_ids=[FRIENDSHIP_ITEMS["Croagunk"], UNLOCK_ITEMS["Scyther Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Bulbasaur Overworld",
        structure_position=35,
        location_ids=[FRIENDSHIP_ITEMS["Bulbasaur"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Venusaur Overworld",
        structure_position=36,
        location_ids=[FRIENDSHIP_ITEMS["Venusaur"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Eevee Overworld",
        structure_position=37,
        location_ids=[FRIENDSHIP_ITEMS["Eevee"], UNLOCK_ITEMS["Jolteon Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Leafeon Overworld",
        structure_position=38,
        location_ids=[FRIENDSHIP_ITEMS["Leafeon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Vaporeon Overworld",
        structure_position=39,
        location_ids=[FRIENDSHIP_ITEMS["Vaporeon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Glaceon Overworld",
        structure_position=40,
        location_ids=[FRIENDSHIP_ITEMS["Glaceon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Flareon Overworld",
        structure_position=41,
        location_ids=[FRIENDSHIP_ITEMS["Flareon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Umbreon Overworld",
        structure_position=42,
        location_ids=[FRIENDSHIP_ITEMS["Umbreon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Espeon Overworld",
        structure_position=43,
        location_ids=[FRIENDSHIP_ITEMS["Espeon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Jolteon Overworld",
        structure_position=44,
        location_ids=[FRIENDSHIP_ITEMS["Jolteon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Azurill Overworld",
        structure_position=45,
        location_ids=[FRIENDSHIP_ITEMS["Azurill"], UNLOCK_ITEMS["Totodile Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Mudkip Overworld",
        structure_position=46,
        location_ids=[FRIENDSHIP_ITEMS["Mudkip"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Krabby Overworld",
        structure_position=47,
        location_ids=[FRIENDSHIP_ITEMS["Krabby"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Corphish Overworld",
        structure_position=48,
        location_ids=[FRIENDSHIP_ITEMS["Corphish"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Corsola Overworld",
        structure_position=49,
        location_ids=[FRIENDSHIP_ITEMS["Corsola"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Slowpoke Overworld",
        structure_position=50,
        location_ids=[FRIENDSHIP_ITEMS["Slowpoke"], UNLOCK_ITEMS["Mudkip Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Buizel Overworld",
        structure_position=51,
        location_ids=[FRIENDSHIP_ITEMS["Buizel"], UNLOCK_ITEMS["Floatzel Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Floatzel Overworld",
        structure_position=52,
        location_ids=[FRIENDSHIP_ITEMS["Floatzel"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Psyduck Overworld",
        structure_position=53,
        location_ids=[FRIENDSHIP_ITEMS["Psyduck"], UNLOCK_ITEMS["Golduck Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Golduck Overworld",
        structure_position=54,
        location_ids=[FRIENDSHIP_ITEMS["Golduck"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Taillow Overworld",
        structure_position=55,
        location_ids=[FRIENDSHIP_ITEMS["Taillow"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Pidgeotto Overworld",
        structure_position=56,
        location_ids=[FRIENDSHIP_ITEMS["Pidgeotto"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Squirtle Overworld",
        structure_position=57,
        location_ids=[FRIENDSHIP_ITEMS["Squirtle"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Blastoise Overworld",
        structure_position=58,
        location_ids=[FRIENDSHIP_ITEMS["Blastoise"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Totodile Overworld",
        structure_position=59,
        location_ids=[FRIENDSHIP_ITEMS["Totodile"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Feraligatr Overworld",
        structure_position=60,
        location_ids=[FRIENDSHIP_ITEMS["Feraligatr"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Lapras Overworld",
        structure_position=61,
        location_ids=[FRIENDSHIP_ITEMS["Lapras"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Wingull Overworld",
        structure_position=62,
        location_ids=[FRIENDSHIP_ITEMS["Wingull"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Pelipper Overworld",
        structure_position=63,
        location_ids=[FRIENDSHIP_ITEMS["Pelipper"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Magikarp Overworld",
        structure_position=64,
        location_ids=[FRIENDSHIP_ITEMS["Magikarp"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Gyarados Overworld",
        structure_position=65,
        location_ids=[FRIENDSHIP_ITEMS["Gyarados"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Teddiursa Overworld",
        structure_position=66,
        location_ids=[FRIENDSHIP_ITEMS["Teddiursa"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Ursaring Overworld",
        structure_position=67,
        location_ids=[FRIENDSHIP_ITEMS["Ursaring"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Spheal Overworld",
        structure_position=68,
        location_ids=[FRIENDSHIP_ITEMS["Spheal"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Smoochum Overworld",
        structure_position=69,
        location_ids=[FRIENDSHIP_ITEMS["Smoochum"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Sneasel Overworld",
        structure_position=70,
        location_ids=[FRIENDSHIP_ITEMS["Sneasel"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Quagsire Overworld",
        structure_position=71,
        location_ids=[FRIENDSHIP_ITEMS["Quagsire"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Delibird Overworld",
        structure_position=72,
        location_ids=[FRIENDSHIP_ITEMS["Delibird"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Octillery Overworld",
        structure_position=73,
        location_ids=[FRIENDSHIP_ITEMS["Octillery"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Glalie Overworld",
        structure_position=74,
        location_ids=[FRIENDSHIP_ITEMS["Glalie"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Froslass Overworld",
        structure_position=75,
        location_ids=[FRIENDSHIP_ITEMS["Froslass"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Piloswine Overworld",
        structure_position=76,
        location_ids=[FRIENDSHIP_ITEMS["Piloswine"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Mamoswine Overworld",
        structure_position=77,
        location_ids=[FRIENDSHIP_ITEMS["Mamoswine"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Piplup Overworld",
        structure_position=78,
        location_ids=[FRIENDSHIP_ITEMS["Piplup"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Prinplup Overworld",
        structure_position=79,
        location_ids=[FRIENDSHIP_ITEMS["Prinplup"]],
        memory_range=MemoryRange.BYTE
    ),

    FriendshipLocation(
        location_name="Empoleon Overworld",
        structure_position=80,
        location_ids=[FRIENDSHIP_ITEMS["Empoleon"]],
        memory_range=MemoryRange.BYTE
    ),

    FriendshipLocation(
        location_name="Geodude Overworld",
        structure_position=81,
        location_ids=[FRIENDSHIP_ITEMS["Geodude"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Gible Overworld",
        structure_position=82,
        location_ids=[FRIENDSHIP_ITEMS["Gible"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Mawile Overworld",
        structure_position=83,
        location_ids=[FRIENDSHIP_ITEMS["Mawile"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Zubat Overworld",
        structure_position=84,
        location_ids=[FRIENDSHIP_ITEMS["Zubat"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Golbat Overworld",
        structure_position=85,
        location_ids=[FRIENDSHIP_ITEMS["Golbat"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Phanpy Overworld",
        structure_position=86,
        location_ids=[FRIENDSHIP_ITEMS["Phanpy"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Cranidos Overworld",
        structure_position=87,
        location_ids=[FRIENDSHIP_ITEMS["Cranidos"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Marowak Overworld",
        structure_position=88,
        location_ids=[FRIENDSHIP_ITEMS["Marowak"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Machamp Overworld",
        structure_position=89,
        location_ids=[FRIENDSHIP_ITEMS["Machamp"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Pichu Overworld",
        structure_position=90,
        location_ids=[FRIENDSHIP_ITEMS["Pichu"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Raichu Overworld",
        structure_position=91,
        location_ids=[FRIENDSHIP_ITEMS["Raichu"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Elekid Overworld",
        structure_position=92,
        location_ids=[FRIENDSHIP_ITEMS["Elekid"], UNLOCK_ITEMS["Electabuzz Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Electabuzz Overworld",
        structure_position=93,
        location_ids=[FRIENDSHIP_ITEMS["Electabuzz"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Electivire Overworld",
        structure_position=94,
        location_ids=[FRIENDSHIP_ITEMS["Electivire"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Mime Jr. Overworld",
        structure_position=95,
        location_ids=[FRIENDSHIP_ITEMS["Mime Jr."]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Mr. Mime Overworld",
        structure_position=96,
        location_ids=[FRIENDSHIP_ITEMS["Mr. Mime"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Bastiodon Overworld",
        structure_position=97,
        location_ids=[FRIENDSHIP_ITEMS["Bastiodon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Torkoal Overworld",
        structure_position=98,
        location_ids=[FRIENDSHIP_ITEMS["Torkoal"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Cyndaquil Overworld",
        structure_position=99,
        location_ids=[FRIENDSHIP_ITEMS["Cyndaquil"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Quilava Overworld",
        structure_position=100,
        location_ids=[FRIENDSHIP_ITEMS["Quilava"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Camerupt Overworld",
        structure_position=101,
        location_ids=[FRIENDSHIP_ITEMS["Camerupt"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Farfetch'd Overworld",
        structure_position=102,
        location_ids=[FRIENDSHIP_ITEMS["Farfetch'd"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Baltoy Overworld",
        structure_position=103,
        location_ids=[FRIENDSHIP_ITEMS["Baltoy"], UNLOCK_ITEMS["Claydol Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Claydol Overworld",
        structure_position=104,
        location_ids=[FRIENDSHIP_ITEMS["Claydol"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Magnemite Overworld",
        structure_position=105,
        location_ids=[FRIENDSHIP_ITEMS["Magnemite"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Magnezone Overworld",
        structure_position=106,
        location_ids=[FRIENDSHIP_ITEMS["Magnezone"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Hitmonlee Overworld",
        structure_position=107,
        location_ids=[FRIENDSHIP_ITEMS["Hitmonlee"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Hitmonchan Overworld",
        structure_position=108,
        location_ids=[FRIENDSHIP_ITEMS["Hitmonchan"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Hitmontop Overworld",
        structure_position=109,
        location_ids=[FRIENDSHIP_ITEMS["Hitmontop"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Magby Overworld",
        structure_position=110,
        location_ids=[FRIENDSHIP_ITEMS["Magby"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Magmortar Overworld",
        structure_position=111,
        location_ids=[FRIENDSHIP_ITEMS["Magmortar"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Chimchar Overworld",
        structure_position=112,  # infernape unlock location only in magmazone using another flag
        location_ids=[FRIENDSHIP_ITEMS["Chimchar"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Infernape Overworld",
        structure_position=113,
        location_ids=[FRIENDSHIP_ITEMS["Infernape"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Rhyperior Overworld",
        structure_position=114,
        location_ids=[FRIENDSHIP_ITEMS["Rhyperior"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Torchic Overworld",
        structure_position=115,
        location_ids=[FRIENDSHIP_ITEMS["Torchic"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Blaziken Overworld",
        structure_position=116,
        location_ids=[FRIENDSHIP_ITEMS["Blaziken"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Meowth Overworld",
        structure_position=117,
        location_ids=[FRIENDSHIP_ITEMS["Meowth"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Gliscor Overworld",
        structure_position=118,
        location_ids=[FRIENDSHIP_ITEMS["Gliscor"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Vulpix Overworld",
        structure_position=119,
        location_ids=[FRIENDSHIP_ITEMS["Vulpix"], UNLOCK_ITEMS["Ninetales Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Ninetales Overworld",
        structure_position=120,
        location_ids=[FRIENDSHIP_ITEMS["Ninetales"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Murkrow Overworld",
        structure_position=121,
        location_ids=[FRIENDSHIP_ITEMS["Murkrow"], UNLOCK_ITEMS["Honchkrow Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Honchkrow Overworld",
        structure_position=122,
        location_ids=[FRIENDSHIP_ITEMS["Honchkrow"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Tangrowth Overworld",
        structure_position=123,
        location_ids=[FRIENDSHIP_ITEMS["Tangrowth"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Abra Overworld",
        structure_position=124,
        location_ids=[FRIENDSHIP_ITEMS["Abra"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Stunky Overworld",
        structure_position=125,
        location_ids=[FRIENDSHIP_ITEMS["Stunky"], UNLOCK_ITEMS["Skuntank Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Skuntank Overworld",
        structure_position=126,
        location_ids=[FRIENDSHIP_ITEMS["Skuntank"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Voltorb Overworld",
        structure_position=127,
        location_ids=[FRIENDSHIP_ITEMS["Voltorb"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Misdreavus Overworld",
        structure_position=128,
        location_ids=[FRIENDSHIP_ITEMS["Misdreavus"]],
        memory_range=MemoryRange.BYTE
    ),

    FriendshipLocation(
        location_name="Mismagius Overworld",
        structure_position=129,
        location_ids=[FRIENDSHIP_ITEMS["Mismagius"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Gastly Overworld",
        structure_position=130,
        location_ids=[FRIENDSHIP_ITEMS["Gastly"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Haunter Overworld",
        structure_position=131,
        location_ids=[FRIENDSHIP_ITEMS["Haunter"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Gengar Overworld",
        structure_position=132,
        location_ids=[FRIENDSHIP_ITEMS["Gengar"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Sableye Overworld",
        structure_position=133,
        location_ids=[FRIENDSHIP_ITEMS["Sableye"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Duskull Overworld",
        structure_position=134,
        location_ids=[FRIENDSHIP_ITEMS["Duskull"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Dusknoir Overworld",
        structure_position=135,
        location_ids=[FRIENDSHIP_ITEMS["Dusknoir"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Chikorita Overworld",
        structure_position=136,
        location_ids=[FRIENDSHIP_ITEMS["Chikorita"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Wynaut Overworld",
        structure_position=137,
        location_ids=[FRIENDSHIP_ITEMS["Wynaut"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Mareep Overworld",
        structure_position=138,
        location_ids=[FRIENDSHIP_ITEMS["Mareep"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Meditite Overworld",
        structure_position=139,
        location_ids=[FRIENDSHIP_ITEMS["Meditite"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Furret Overworld",
        structure_position=140,
        location_ids=[FRIENDSHIP_ITEMS["Furret"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Aerodactyl Overworld",
        structure_position=141,
        location_ids=[FRIENDSHIP_ITEMS["Aerodactyl"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Flygon Overworld",
        structure_position=142,
        location_ids=[FRIENDSHIP_ITEMS["Flygon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Togekiss Overworld",
        structure_position=143,
        location_ids=[FRIENDSHIP_ITEMS["Togekiss"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Arcanine Overworld",
        structure_position=144,
        location_ids=[FRIENDSHIP_ITEMS["Arcanine"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Charmander Overworld",
        structure_position=145,
        location_ids=[FRIENDSHIP_ITEMS["Charmander"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Charizard Overworld",
        structure_position=146,
        location_ids=[FRIENDSHIP_ITEMS["Charizard"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Porygon-Z Overworld",
        structure_position=147,
        location_ids=[FRIENDSHIP_ITEMS["Porygon-Z"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Garchomp Overworld",
        structure_position=148,
        location_ids=[FRIENDSHIP_ITEMS["Garchomp"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Tyranitar Overworld",
        structure_position=149,
        location_ids=[FRIENDSHIP_ITEMS["Tyranitar"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Dragonite Overworld",
        structure_position=150,
        location_ids=[FRIENDSHIP_ITEMS["Dragonite"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Riolu Overworld",
        structure_position=151,
        location_ids=[FRIENDSHIP_ITEMS["Riolu"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Lucario Overworld",
        structure_position=152,
        location_ids=[FRIENDSHIP_ITEMS["Lucario"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Kirlia Overworld",
        structure_position=153,
        location_ids=[FRIENDSHIP_ITEMS["Kirlia"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Absol Overworld",
        structure_position=154,
        location_ids=[FRIENDSHIP_ITEMS["Absol"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Salamence Overworld",
        structure_position=155,
        location_ids=[FRIENDSHIP_ITEMS["Salamence"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Shaymin Overworld",
        structure_position=156,
        location_ids=[FRIENDSHIP_ITEMS["Shaymin"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Manaphy Overworld",
        structure_position=157,
        location_ids=[FRIENDSHIP_ITEMS["Manaphy"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Latias Overworld",
        structure_position=158,
        location_ids=[FRIENDSHIP_ITEMS["Latias"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Suicune Overworld",
        structure_position=159,
        location_ids=[FRIENDSHIP_ITEMS["Suicune"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Metagross Overworld",
        structure_position=160,
        location_ids=[FRIENDSHIP_ITEMS["Metagross"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Heatran Overworld",
        structure_position=161,
        location_ids=[FRIENDSHIP_ITEMS["Heatran"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Groudon Overworld",
        structure_position=162,
        location_ids=[FRIENDSHIP_ITEMS["Groudon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Celebi Overworld",
        structure_position=163,
        location_ids=[FRIENDSHIP_ITEMS["Celebi"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Darkrai Overworld",
        structure_position=164,
        location_ids=[FRIENDSHIP_ITEMS["Darkrai"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Rotom Overworld",
        structure_position=165,
        location_ids=[FRIENDSHIP_ITEMS["Rotom"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Latios Overworld",
        structure_position=166,
        location_ids=[FRIENDSHIP_ITEMS["Latios"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Jirachi Overworld",
        structure_position=167,
        location_ids=[FRIENDSHIP_ITEMS["Jirachi"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Deoxys Overworld",
        structure_position=168,
        location_ids=[FRIENDSHIP_ITEMS["Deoxys"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Mew Overworld",
        structure_position=169,
        location_ids=[FRIENDSHIP_ITEMS["Mew"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Kakuna Overworld",
        structure_position=170,
        location_ids=[FRIENDSHIP_ITEMS["Kakuna"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Aron Overworld",
        structure_position=171,
        location_ids=[FRIENDSHIP_ITEMS["Aron"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Diglett Overworld",
        structure_position=172,
        location_ids=[FRIENDSHIP_ITEMS["Diglett"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Bronzor Overworld",
        structure_position=173,
        location_ids=[FRIENDSHIP_ITEMS["Bronzor"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Dugtrio Overworld",
        structure_position=174,
        location_ids=[FRIENDSHIP_ITEMS["Dugtrio"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Drifloon Overworld",
        structure_position=175,
        location_ids=[FRIENDSHIP_ITEMS["Drifloon"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Drifblim Overworld",
        structure_position=176,
        location_ids=[FRIENDSHIP_ITEMS["Drifblim"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Golem Overworld",
        structure_position=177,
        location_ids=[FRIENDSHIP_ITEMS["Golem"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Hoppip Overworld",
        structure_position=178,
        location_ids=[FRIENDSHIP_ITEMS["Hoppip"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Spinarak Overworld",
        structure_position=179,
        location_ids=[FRIENDSHIP_ITEMS["Spinarak"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Carvanha Overworld",
        structure_position=180,
        location_ids=[FRIENDSHIP_ITEMS["Carvanha"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Magcargo Overworld",
        structure_position=181,
        location_ids=[FRIENDSHIP_ITEMS["Magcargo"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Electrode Overworld",
        structure_position=182,
        location_ids=[FRIENDSHIP_ITEMS["Electrode"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Burmy Overworld",
        structure_position=183,
        location_ids=[FRIENDSHIP_ITEMS["Burmy"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Chatot Overworld",
        structure_position=184,
        location_ids=[FRIENDSHIP_ITEMS["Chatot"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Sharpedo Overworld",
        structure_position=185,
        location_ids=[FRIENDSHIP_ITEMS["Sharpedo"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Skorupi Overworld",
        structure_position=186,
        location_ids=[FRIENDSHIP_ITEMS["Skorupi"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Budew Overworld",
        structure_position=187,
        location_ids=[FRIENDSHIP_ITEMS["Budew"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Metapod Overworld",
        structure_position=188,
        location_ids=[FRIENDSHIP_ITEMS["Metapod"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Jumpluff Overworld",
        structure_position=189,
        location_ids=[FRIENDSHIP_ITEMS["Jumpluff"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Wailord Overworld",
        structure_position=190,
        location_ids=[FRIENDSHIP_ITEMS["Wailord"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Skiploom Overworld",
        structure_position=191,
        location_ids=[FRIENDSHIP_ITEMS["Skiploom"]],
        memory_range=MemoryRange.BYTE
    ),
    FriendshipLocation(
        location_name="Rayquaza Overworld",
        structure_position=192,
        location_ids=[FRIENDSHIP_ITEMS["Rayquaza"]],
        memory_range=MemoryRange.BYTE
    ),
    PrismaLocation(
        location_name="Bulbasaur Prisma",
        structure_position=15,
        location_ids=[PRISM_ITEM["Bulbasaur Prisma"]],
        memory_range=MemoryRange.WORD
    ),
    PrismaLocation(
        location_name="Venusaur Prisma",
        structure_position=2,
        location_ids=[PRISM_ITEM["Venusaur Prisma"]],
        memory_range=MemoryRange.WORD
    ),

    BulbasaurDashMinigame(
        location_name="Pikachu Dash",
        structure_position=0,
        location_ids=[MinigameLocationIds.PIKACHU_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Mew Dash",
        structure_position=1,
        location_ids=[MinigameLocationIds.MEW_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Arcanine Dash",
        structure_position=2,
        location_ids=[MinigameLocationIds.ARCANINE_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Jolteon Dash",
        structure_position=3,
        location_ids=[MinigameLocationIds.JOLTEON_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Leafeon Dash",
        structure_position=4,
        location_ids=[MinigameLocationIds.LEAFEON_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Scyther Dash",
        structure_position=5,
        location_ids=[MinigameLocationIds.SCYTHER_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Ponyta Dash",
        structure_position=6,
        location_ids=[MinigameLocationIds.PONYTA_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Shinx Dash",
        structure_position=7,
        location_ids=[MinigameLocationIds.SHINX_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Eevee Dash",
        structure_position=8,
        location_ids=[MinigameLocationIds.EEVEE_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Pachirisu Dash",
        structure_position=9,
        location_ids=[MinigameLocationIds.PACHIRISU_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Buneary Dash",
        structure_position=10,
        location_ids=[MinigameLocationIds.BUNEARY_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ), BulbasaurDashMinigame(
        location_name="Croagunk Dash",
        structure_position=11,
        location_ids=[MinigameLocationIds.CROAGUNK_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Chimchar Dash",
        structure_position=12,
        location_ids=[MinigameLocationIds.CHIMCHAR_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),

    BulbasaurDashMinigame(
        location_name="Treecko Dash",
        structure_position=13,
        location_ids=[MinigameLocationIds.TREECKO_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Bibarel Dash",
        structure_position=14,
        location_ids=[MinigameLocationIds.BIBAREL_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Turtwig Dash",
        structure_position=15,
        location_ids=[MinigameLocationIds.TURTWIG_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Bulbasaur Dash",
        structure_position=16,
        location_ids=[MinigameLocationIds.BULBASAUR_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Bidoof Dash",
        structure_position=17,
        location_ids=[MinigameLocationIds.BIDOOF_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Oddish Dash",
        structure_position=18,
        location_ids=[MinigameLocationIds.ODDISH_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Shroomish Dash",
        structure_position=19,
        location_ids=[MinigameLocationIds.SHROOMISH_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Munchlax Dash",
        structure_position=20,
        location_ids=[MinigameLocationIds.MUNCHLAX_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Bonsly Dash",
        structure_position=21,
        location_ids=[MinigameLocationIds.BONSLY_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Lotad Dash",
        structure_position=22,
        location_ids=[MinigameLocationIds.LOTAD_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Weedle Dash",
        structure_position=23,
        location_ids=[MinigameLocationIds.WEEDLE_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Caterpie Dash",
        structure_position=24,
        location_ids=[MinigameLocationIds.CATERPIE_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    BulbasaurDashMinigame(
        location_name="Magikarp Dash",
        structure_position=25,
        location_ids=[MinigameLocationIds.MAGIKARP_DASH.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Pikachu Vine Swing",
        structure_position=0,
        location_ids=[MinigameLocationIds.PIKACHU_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Jirachi Vine Swing",
        structure_position=1,
        location_ids=[MinigameLocationIds.JIRACHI_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Blaziken Vine Swing",
        structure_position=2,
        location_ids=[MinigameLocationIds.BLAZIKEN_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Infernape Vine Swing",
        structure_position=3,
        location_ids=[MinigameLocationIds.INFERNAPE_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Lucario Vine Swing",
        structure_position=4,
        location_ids=[MinigameLocationIds.LUCARIO_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Tangrowth Vine Swing",
        structure_position=5,
        location_ids=[MinigameLocationIds.TANGROWTH_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Primeape Vine Swing",
        structure_position=6,
        location_ids=[MinigameLocationIds.PRIMEAPE_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Ambipom Vine Swing",
        structure_position=7,
        location_ids=[MinigameLocationIds.AMBIPOM_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Mankey Vine Swing",
        structure_position=8,
        location_ids=[MinigameLocationIds.MANKEY_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Aipom Vine Swing",
        structure_position=9,
        location_ids=[MinigameLocationIds.AIPOM_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Chimchar Vine Swing",
        structure_position=10,
        location_ids=[MinigameLocationIds.CHIMCHAR_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Treecko Vine Swing",
        structure_position=11,
        location_ids=[MinigameLocationIds.TREECKO_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Croagunk Vine Swing",
        structure_position=12,
        location_ids=[MinigameLocationIds.CROAGUNK_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Pachirisu Vine Swing",
        structure_position=13,
        location_ids=[MinigameLocationIds.PACHIRISU_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Munchlax Vine Swing",
        structure_position=14,
        location_ids=[MinigameLocationIds.MUNCHLAX_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    VenusaurSwingMinigame(
        location_name="Magikarp Vine Swing",
        structure_position=15,
        location_ids=[MinigameLocationIds.MAGIKARP_VINE_SWING.value],
        memory_range=MemoryRange.HALFWORD
    ),
    CaterpieLocation(
        location_name="Caterpie Tree",
        structure_position=0,
        location_ids=[UNLOCK_ITEMS["Caterpie Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    WeedleLocation(
        location_name="Weedle Tree",
        structure_position=0,
        location_ids=[UNLOCK_ITEMS["Weedle Unlock"]],
        memory_range=MemoryRange.BYTE
    ),

    ShroomishLocation(
        location_name="Shroomish Crate",
        structure_position=0,
        location_ids=[UNLOCK_ITEMS["Shroomish Unlock"]],
        memory_range=MemoryRange.BYTE
    ),
    MagikarpLocation(
        location_name="Magikarp electrocuted",
        structure_position=0,
        location_ids=[UNLOCK_ITEMS["Magikarp Unlock"]],
        memory_range=MemoryRange.BYTE
    ),

    BidoofHousingLocation(
        location_name="Bidoof Housing 1",
        structure_position=0,
        _expected_value=0b00000110,
        _bit_mask=0b00000110,
        location_ids=[UNLOCK_ITEMS["Bidoof Unlock"], QuestLocationIds.MEADOW_BIDOOF_HOUSING1.value],
        memory_range=MemoryRange.BYTE
    ),
    BidoofHousingLocation(
        location_name="Bidoof Housing 2",
        structure_position=0,
        _expected_value=0b00001010,
        _bit_mask=0b00001010,
        location_ids=[UNLOCK_ITEMS["Bidoof Unlock 2"], QuestLocationIds.MEADOW_BIDOOF_HOUSING2.value],
        memory_range=MemoryRange.BYTE
    ),
    BidoofHousingLocation(
        location_name="Bidoof Housing 3",
        structure_position=0,
        _expected_value=0b00001110,
        _bit_mask=0b00001110,
        location_ids=[UNLOCK_ITEMS["Bidoof Unlock 3"], QuestLocationIds.MEADOW_BIDOOF_HOUSING3.value],
        memory_range=MemoryRange.BYTE
    ),
    BidoofHousingLocation(
        location_name="Bidoof Housing 4",
        structure_position=0,
        _expected_value=0b00010010,
        _bit_mask=0b00010010,
        location_ids=[UNLOCK_ITEMS["Bibarel Unlock"], QuestLocationIds.MEADOW_BIDOOF_HOUSING4.value],
        memory_range=MemoryRange.BYTE
    )

]

POWER_MAP = {
    0x01: [0x01, 0x04, 0x08, 0x4000],
    0x02: [0x10, 0x20, 0x40, 0x80],
    0x03: [0x100, 0x200, 0x400],
    0x04: [0x800, 0x1000, 0x2000]
}

from dataclasses import dataclass, field
from enum import Flag, auto
from typing import Optional

from BaseClasses import Location, Region
from worlds.pokepark.adresses import MemoryRange


class PokeparkFlag(Flag):
    ALWAYS = auto()  # ALWAYS available
    FRIENDSHIP = auto()  # generic that has no specific POWER COMP
    QUIZ = auto()
    BATTLE = auto()
    CHASE = auto()
    ERRAND = auto()
    HIDEANDSEEK = auto()
    POKEMON_UNLOCK = auto()  # Unlocks like Caterpie Tree
    QUEST = auto()
    ATTRACTION = auto()
    LEGENDARY = auto()  # unsure
    POWER_UP = auto()
    POSTGAME = auto()  # for postgame goals


class MultiZoneFlag(Flag):
    MULTI = auto()
    SINGLE = auto()
    NONE = auto()


@dataclass
class PokeparkBaseClientLocationData:
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

    def __post_init__(self):
        if type(self) == PokeparkBaseClientLocationData:
            self.global_manager_data_struc_offset = 0x0
            self.in_structure_offset = 0x0
            self.expected_value = 0x0
            self.in_structure_address_interval = 0x0
            self.bit_mask = 0xFFFFFFFF


@dataclass
class PokeparkLocationData:
    code: Optional[int]
    flags: PokeparkFlag
    region: str
    stage_id: int
    client_data: PokeparkBaseClientLocationData
    each_zone: MultiZoneFlag = MultiZoneFlag.NONE


@dataclass
class PokeparkFriendshipClientLocationData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1F4  # start of friendship data structure
        self.in_structure_offset = 0xc  # best friend offset from friendship address
        self.expected_value = 0x80  # flag is set with value 0x80
        self.in_structure_address_interval = 0x14  # spacing between specific pokemon friendship data
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkPrismaClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1B40  # start of prisma data structure
        self.in_structure_offset = 0x0
        self.expected_value = 0b10  # flag is set with prisma value 0b10
        self.bit_mask = 0b10  # using only second bit
        self.in_structure_address_interval = 0x144  # spacing between prisma


# currently separate classes for flags until more data is available
@dataclass
class PokeparkThunderboltUpgradeClientLocationData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x3c
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask


@dataclass
class PokeparkIronTailUpgradeClientLocationData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x3e
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask


@dataclass
class PokeparkDoubleDashUpgradeClientLocationData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x4a
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask


@dataclass
class PokeparkDashHealthUpgradeClientLocationData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x3d
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask


@dataclass
class PokeparkWeedleTreeClientData(PokeparkBaseClientLocationData):  # f9901TalkCelebi same byte
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x4b
        self.in_structure_offset = 0x0
        self.expected_value = 0b00001000
        self.bit_mask = 0b00001000
        self.in_structure_address_interval = 0x0


@dataclass
class PokeparkCaterpieTreeClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x4b
        self.in_structure_offset = 0x0
        self.expected_value = 0b00000001
        self.bit_mask = 0b00000001
        self.in_structure_address_interval = 0x0


@dataclass
class PokeparkShroomishCrateClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x41
        self.in_structure_offset = 0x0
        self.expected_value = 0b10000000
        self.bit_mask = 0b10000000
        self.in_structure_address_interval = 0x0


@dataclass
class PokeparkMagikarpRescueClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x50
        self.in_structure_offset = 0x0
        self.expected_value = 0b10000000
        self.bit_mask = 0b10000000
        self.in_structure_address_interval = 0x0


@dataclass
class PokeparkMewChallengeClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x51
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0


@dataclass
class PokeparkBottleIgloQuestClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x31
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0


@dataclass
class PokeparkChristmasTreeQuestClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x43
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0


@dataclass
class PokeparkRhyperiorQuestClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x40
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0



@dataclass
class PokeparkBidoofHousingClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x2f
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask


@dataclass
class PokeparkF0301BippaFlagClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = 0xFFFFFFFF
    _bit_mask: Optional[int] = 0xFFFFFFFF

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x46
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask


@dataclass
class PokeparkBulbasaurAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2E50
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkVenusaurAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1ddc
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkPelipperAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x22ec
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkGyaradosAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x21A8
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkEmpoleonAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2574
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkBastiodonAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x26B8
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkRhyperiorAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x27FC
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkBlazikenAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2940
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkTangrowthAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1F20
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkDusknoirAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2064
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkRotomAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2a84
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkAbsolAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1B54
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkSalamenceAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2D0C
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value


@dataclass
class PokeparkRayquazaAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1C98
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
class PokeparkLocation(Location):
    game: str = "PokePark"

    def __init__(self, player: int, name: str, parent: Region, data: PokeparkLocationData):
        address = None if data.code is None else PokeparkLocation.get_apid(data.code)
        super().__init__(player, name, address=address, parent=parent)

        self.code = data.code
        self.flags = data.flags
        self.region = data.region
        self.stage_id = data.stage_id

        self.address = self.address

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given location code.

        :param code: The unique code for the location.
        :return: The computed Archipelago ID.
        """
        base_id: int = 10000
        return base_id + code


LOCATION_TABLE: dict[str, PokeparkLocationData] = {
    # Treehouse
    "Treehouse - Burmy - Friendship": PokeparkLocationData(
        0, PokeparkFlag.ALWAYS, "Treehouse", 0x0201, PokeparkFriendshipClientLocationData(
            structure_position=183,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Treehouse - Mime Jr. - Friendship": PokeparkLocationData(
        1, PokeparkFlag.ALWAYS, "Treehouse", 0x0201, PokeparkFriendshipClientLocationData(
            structure_position=95,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Treehouse - Abra - Friendship": PokeparkLocationData(
        2, PokeparkFlag.ALWAYS, "Treehouse", 0x0201, PokeparkFriendshipClientLocationData(
            structure_position=124,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Treehouse - Drifblim - Friendship": PokeparkLocationData(
        3, PokeparkFlag.ALWAYS, "Treehouse", 0x0201, PokeparkFriendshipClientLocationData(
            structure_position=176,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Treehouse - Power Up - Thunderbolt Upgrade 1": PokeparkLocationData(
        4, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkThunderboltUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00000001,
            _bit_mask=0b00000001
        )
    ),
    "Treehouse - Power Up - Thunderbolt Upgrade 2": PokeparkLocationData(
        5, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkThunderboltUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Treehouse - Power Up - Thunderbolt Upgrade 3": PokeparkLocationData(
        6, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkThunderboltUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00000011,
            _bit_mask=0b00000011
        )
    ),
    "Treehouse - Power Up - Dash Upgrade 1": PokeparkLocationData(
        7, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkDashHealthUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00010000,
            _bit_mask=0b00010000
        )
    ),
    "Treehouse - Power Up - Dash Upgrade 2": PokeparkLocationData(
        8, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkDashHealthUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00100000,
            _bit_mask=0b00100000
        )
    ),
    "Treehouse - Power Up - Ponyta Unlocked": PokeparkLocationData(
        9, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkDashHealthUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00100000,
            _bit_mask=0b00100000
        )
    ),
    "Treehouse - Power Up - Dash Upgrade 3": PokeparkLocationData(
        10, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkDashHealthUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00110000,
            _bit_mask=0b00110000
        )
    ),
    "Treehouse - Power Up - Double Dash Upgrade": PokeparkLocationData(
        11, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkDoubleDashUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Treehouse - Power Up - Health Upgrade 1": PokeparkLocationData(
        12, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkDashHealthUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00000001,
            _bit_mask=0b00000001
        )
    ),
    "Treehouse - Power Up - Health Upgrade 2": PokeparkLocationData(
        13, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkDashHealthUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),

    "Treehouse - Power Up - Health Upgrade 3": PokeparkLocationData(
        14, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkDashHealthUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00000011,
            _bit_mask=0b00000011
        )
    ),
    "Treehouse - Power Up - Iron Tail Upgrade 1": PokeparkLocationData(
        15, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkIronTailUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00010000,
            _bit_mask=0b00010000
        )
    ),
    "Treehouse - Power Up - Iron Tail Upgrade 2": PokeparkLocationData(
        16, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkIronTailUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00100000,
            _bit_mask=0b00100000
        )
    ),
    "Treehouse - Power Up - Iron Tail Upgrade 3": PokeparkLocationData(
        17, PokeparkFlag.POWER_UP, "Treehouse", 0x0201, PokeparkIronTailUpgradeClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE,
            _expected_value=0b00110000,
            _bit_mask=0b00110000
        )
    ),
    # Meadow Zone Main Area
    "Meadow Zone Main Area - Turtwig Power Competition -- Friendship": PokeparkLocationData(
        18, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Turtwig Power Competition -- Pachirisu Unlocked": PokeparkLocationData(
        19, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Turtwig Power Competition -- Bonsly Unlocked": PokeparkLocationData(
        20, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=0,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bulbasaur -- Friendship": PokeparkLocationData(
        21, PokeparkFlag.FRIENDSHIP, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=35,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Buneary Power Competition -- Friendship": PokeparkLocationData(
        22, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=18,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Buneary Power Competition -- Lotad Unlocked": PokeparkLocationData(
        23, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=18,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Buneary Power Competition -- Shinx Unlocked": PokeparkLocationData(
        24, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=18,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Munchlax Errand -- Friendship": PokeparkLocationData(
        25, PokeparkFlag.ERRAND, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=10,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Munchlax Errand -- Tropius Unlocked": PokeparkLocationData(
        26, PokeparkFlag.ERRAND, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=10,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Tropius Errand -- Friendship": PokeparkLocationData(
        27, PokeparkFlag.ERRAND, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=26,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Pachirisu Power Competition -- Friendship": PokeparkLocationData(
        28, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=3,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Shinx Power Competition -- Friendship": PokeparkLocationData(
        29, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=27,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Mankey Power Competition -- Friendship": PokeparkLocationData(
        30, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=16,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Mankey Power Competition -- Chimchar Unlocked": PokeparkLocationData(
        31, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=16,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Spearow Power Competition -- Friendship": PokeparkLocationData(
        32, PokeparkFlag.FRIENDSHIP, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=25,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Croagunk Power Competition -- Friendship": PokeparkLocationData(
        33, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=34,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Croagunk Power Competition -- Scyther Unlocked": PokeparkLocationData(
        34, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=34,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Lotad Power Competition -- Friendship": PokeparkLocationData(
        35, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=4,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Treecko Power Competition -- Friendship": PokeparkLocationData(
        36, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=2,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Caterpie Tree -- Caterpie Unlocked": PokeparkLocationData(
        37, PokeparkFlag.POKEMON_UNLOCK, "Meadow Zone Main Area", 0x0101, PokeparkCaterpieTreeClientData(
            structure_position=0,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Meadow Zone Main Area - Caterpie Power Competition -- Friendship": PokeparkLocationData(
        38, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=8,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Caterpie Power Competition -- Butterfree Unlocked": PokeparkLocationData(
        39, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=8,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Weedle Tree -- Weedle Unlocked": PokeparkLocationData(
        40, PokeparkFlag.POKEMON_UNLOCK, "Meadow Zone Main Area", 0x0101, PokeparkWeedleTreeClientData(
            structure_position=0,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Meadow Zone Main Area - Weedle Power Competition -- Friendship": PokeparkLocationData(
        41, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=7,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Shroomish Crate -- Shroomish Unlocked": PokeparkLocationData(
        42, PokeparkFlag.POKEMON_UNLOCK, "Meadow Zone Main Area", 0x0101, PokeparkShroomishCrateClientData(
            structure_position=0,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Meadow Zone Main Area - Shroomish Power Competition -- Friendship": PokeparkLocationData(
        43, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=14,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Magikarp Rescue -- Magikarp Unlocked": PokeparkLocationData(
        44, PokeparkFlag.POKEMON_UNLOCK, "Meadow Zone Main Area", 0x0101, PokeparkMagikarpRescueClientData(
            structure_position=0,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Meadow Zone Main Area - Oddish Power Competition -- Friendship": PokeparkLocationData(
        45, PokeparkFlag.HIDEANDSEEK, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=23,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Stage 1": PokeparkLocationData(
        46, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkBidoofHousingClientData(
            structure_position=0,
            _expected_value=0b00000110,
            _bit_mask=0b00000110,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Bidoof 1 Unlocked": PokeparkLocationData(
        47, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkBidoofHousingClientData(
            structure_position=0,
            _expected_value=0b00000110,
            _bit_mask=0b00000110,
            memory_range=MemoryRange.BYTE
        )
    ),

    "Meadow Zone Main Area - Bidoof Housing -- Stage 2": PokeparkLocationData(
        48, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkBidoofHousingClientData(
            structure_position=0,
            _expected_value=0b00001010,
            _bit_mask=0b00001010,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Bidoof 2 Unlocked": PokeparkLocationData(
        49, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkBidoofHousingClientData(
            structure_position=0,
            _expected_value=0b00001010,
            _bit_mask=0b00001010,
            memory_range=MemoryRange.BYTE
        )
    ),

    "Meadow Zone Main Area - Bidoof Housing -- Stage 3": PokeparkLocationData(
        50, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkBidoofHousingClientData(
            structure_position=0,
            _expected_value=0b00001110,
            _bit_mask=0b00001110,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Bidoof 3 Unlocked": PokeparkLocationData(
        51, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkBidoofHousingClientData(
            structure_position=0,
            _expected_value=0b00001110,
            _bit_mask=0b00001110,
            memory_range=MemoryRange.BYTE
        )
    ),

    "Meadow Zone Main Area - Bidoof Housing -- Stage 4": PokeparkLocationData(
        52, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkBidoofHousingClientData(
            structure_position=0,
            _expected_value=0b00010010,
            _bit_mask=0b00010010,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Bibarel Unlocked": PokeparkLocationData(
        53, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkBidoofHousingClientData(
            structure_position=0,
            _expected_value=0b00010010,
            _bit_mask=0b00010010,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing Completed -- Friendship": PokeparkLocationData(
        54, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=5,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing Completed -- Beach Bidoof Unlocked": PokeparkLocationData(
        55, PokeparkFlag.QUEST, "Meadow Zone Main Area", 0x0101, PokeparkF0301BippaFlagClientData(
            structure_position=0,
            _expected_value=0b00000001,
            _bit_mask=0b00000001,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Bibarel Power Competition -- Friendship": PokeparkLocationData(
        56, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=6,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Leafeon Power Competition -- Friendship": PokeparkLocationData(
        57, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=38,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Torterra Power Competition -- Friendship": PokeparkLocationData(
        58, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=1,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Scyther Power Competition -- Friendship": PokeparkLocationData(
        59, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=32,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Meadow Zone Main Area - Starly Power Competition -- Friendship": PokeparkLocationData(
        60, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=20,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Bonsly Power Competition -- Friendship": PokeparkLocationData(
        61, PokeparkFlag.HIDEANDSEEK, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=12,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Bonsly Power Competition -- Sudowoodo Unlocked": PokeparkLocationData(
        62, PokeparkFlag.HIDEANDSEEK, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=12,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),

    "Meadow Zone Main Area - Chimchar Power Competition -- Friendship": PokeparkLocationData(
        63, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=112,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),

    "Meadow Zone Main Area - Sudowoodo Power Competition -- Friendship": PokeparkLocationData(
        64, PokeparkFlag.HIDEANDSEEK, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=13,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),

    "Meadow Zone Main Area - Aipom Power Competition -- Friendship": PokeparkLocationData(
        65, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=30,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),

    "Meadow Zone Main Area - Aipom Power Competition -- Ambipom Unlocked": PokeparkLocationData(
        66, PokeparkFlag.CHASE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=30,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Ambipom Power Competition -- Friendship": PokeparkLocationData(
        67, PokeparkFlag.BATTLE, "Meadow Zone Main Area", 0x0101, PokeparkFriendshipClientLocationData(
            structure_position=31,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    #
    #
    #
    #
    #
    #
    #
    #
    # Bulbasaur's Daring Dash Minigame
    "Bulbasaur's Daring Dash Attraction -- Prisma": PokeparkLocationData(
        68, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101, PokeparkPrismaClientData(
            structure_position=15,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Pikachu": PokeparkLocationData(
        69, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Turtwig": PokeparkLocationData(
        70, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Munchlax": PokeparkLocationData(
        71, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=20,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Chimchar": PokeparkLocationData(
        72, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Treecko": PokeparkLocationData(
        73, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Bibarel": PokeparkLocationData(
        74, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Bulbasaur": PokeparkLocationData(
        75, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=16,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Bidoof": PokeparkLocationData(
        76, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=17,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Oddish": PokeparkLocationData(
        77, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=18,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Shroomish": PokeparkLocationData(
        78, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=19,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Bonsly": PokeparkLocationData(
        79, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=21,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Lotad": PokeparkLocationData(
        80, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=22,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Weedle": PokeparkLocationData(
        81, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=23,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Caterpie": PokeparkLocationData(
        82, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=24,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Magikarp": PokeparkLocationData(
        83, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=25,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Jolteon": PokeparkLocationData(
        84, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Arcanine": PokeparkLocationData(
        85, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Leafeon": PokeparkLocationData(
        86, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Scyther": PokeparkLocationData(
        87, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Ponyta": PokeparkLocationData(
        88, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Shinx": PokeparkLocationData(
        89, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Eevee": PokeparkLocationData(
        90, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Pachirisu": PokeparkLocationData(
        91, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Buneary": PokeparkLocationData(
        92, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Croagunk": PokeparkLocationData(
        93, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Mew": PokeparkLocationData(
        94, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction", 0x0101,
        PokeparkBulbasaurAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),

    "Meadow Zone Venusaur Area - Venusaur -- Friendship": PokeparkLocationData(
        95, PokeparkFlag.ATTRACTION, "Meadow Zone Venusaur Area", 0x0102, PokeparkFriendshipClientLocationData(
            structure_position=36,
            memory_range=MemoryRange.BYTE
        )
    ),

    "Venusaur's Vine Swing Attraction -- Prisma": PokeparkLocationData(
        96, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102, PokeparkPrismaClientData(
            structure_position=2,
            memory_range=MemoryRange.WORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Pikachu": PokeparkLocationData(
        97, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Munchlax": PokeparkLocationData(
        98, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Magikarp": PokeparkLocationData(
        99, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Blaziken": PokeparkLocationData(
        100, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Infernape": PokeparkLocationData(
        101, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Lucario": PokeparkLocationData(
        102, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Primeape": PokeparkLocationData(
        103, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Tangrowth": PokeparkLocationData(
        104, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Ambipom": PokeparkLocationData(
        105, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Croagunk": PokeparkLocationData(
        106, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Mankey": PokeparkLocationData(
        107, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Aipom": PokeparkLocationData(
        108, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Chimchar": PokeparkLocationData(
        109, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Treecko": PokeparkLocationData(
        110, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Pachirisu": PokeparkLocationData(
        111, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Venusaur's Vine Swing Attraction -- Jirachi": PokeparkLocationData(
        112, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102,
        PokeparkVenusaurAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),

    "Venusaur's Vine Swing Attraction -- Jirachi Friendship": PokeparkLocationData(
        113, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0102, PokeparkFriendshipClientLocationData(
            structure_position=167,
            memory_range=MemoryRange.BYTE
        ),
    ),
    # Beach Zone
    #
    #
    "Beach Zone Main Area - Buizel Power Competition -- Friendship": PokeparkLocationData(
        114, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=51,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Buizel Power Competition -- Floatzel Unlocked": PokeparkLocationData(
        115, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=51,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Psyduck Power Competition -- Friendship": PokeparkLocationData(
        116, PokeparkFlag.HIDEANDSEEK, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=53,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Psyduck Power Competition -- Golduck Unlocked": PokeparkLocationData(
        117, PokeparkFlag.HIDEANDSEEK, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=53,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Slowpoke Power Competition -- Friendship": PokeparkLocationData(
        118, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=50,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Slowpoke Power Competition -- Mudkip Unlocked": PokeparkLocationData(
        119, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=50,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Azurill Power Competition -- Friendship": PokeparkLocationData(
        120, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=45,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Azurill Power Competition -- Totodile Unlocked": PokeparkLocationData(
        121, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=45,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Totodile Power Competition -- Friendship": PokeparkLocationData(
        122, PokeparkFlag.BATTLE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=59,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Pidgeotto Power Competition -- Friendship": PokeparkLocationData(
        123, PokeparkFlag.BATTLE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=56,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Corsola Power Competition -- Friendship": PokeparkLocationData(
        124, PokeparkFlag.QUIZ, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=49,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Floatzel Power Competition -- Friendship": PokeparkLocationData(
        125, PokeparkFlag.BATTLE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=52,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Vaporeon Power Competition -- Friendship": PokeparkLocationData(
        126, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=39,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Golduck Power Competition -- Friendship": PokeparkLocationData(
        127, PokeparkFlag.BATTLE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=54,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Wailord Power Competition -- Friendship": PokeparkLocationData(
        128, PokeparkFlag.QUEST, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=190,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Feraligatr Power Competition -- Friendship": PokeparkLocationData(
        129, PokeparkFlag.BATTLE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=60,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Main Area - Blastoise Power Competition -- Friendship": PokeparkLocationData(
        130, PokeparkFlag.BATTLE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=58,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 1": PokeparkLocationData(
        131, PokeparkFlag.QUEST, "Beach Zone Recycle Area", 0x0301, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00010000,
            _bit_mask=0b00010000,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 2": PokeparkLocationData(
        132, PokeparkFlag.QUEST, "Beach Zone Recycle Area", 0x0301, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00100000,
            _bit_mask=0b00100000,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 2 --- Krabby Unlocked": PokeparkLocationData(
        133, PokeparkFlag.QUEST, "Beach Zone Recycle Area", 0x0301, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00100000,
            _bit_mask=0b00100000,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 3": PokeparkLocationData(
        134, PokeparkFlag.QUEST, "Beach Zone Recycle Area", 0x0301, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00110000,
            _bit_mask=0b00110000,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 4": PokeparkLocationData(
        135, PokeparkFlag.QUEST, "Beach Zone Recycle Area", 0x0301, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b01000000,
            _bit_mask=0b01000000,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 4 --- Corphish Unlocked": PokeparkLocationData(
        136, PokeparkFlag.QUEST, "Beach Zone Recycle Area", 0x0301, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b01000000,
            _bit_mask=0b01000000,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 5": PokeparkLocationData(
        137, PokeparkFlag.QUEST, "Beach Zone Recycle Area", 0x0301, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b01010000,
            _bit_mask=0b01010000,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 6": PokeparkLocationData(
        138, PokeparkFlag.QUEST, "Beach Zone Recycle Area", 0x0301, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b01100000,
            _bit_mask=0b01100000,
            memory_range=MemoryRange.BYTE
        ),
    ),

    "Beach Zone Main Area - Krabby Power Competition -- Friendship": PokeparkLocationData(
        139, PokeparkFlag.BATTLE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=47,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Starly Power Competition -- Friendship": PokeparkLocationData(
        140, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=20,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Mudkip Power Competition -- Friendship": PokeparkLocationData(
        141, PokeparkFlag.HIDEANDSEEK, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=46,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Taillow Power Competition -- Friendship": PokeparkLocationData(
        142, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=55,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Staravia Power Competition -- Friendship": PokeparkLocationData(
        143, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=21,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Wingull Power Competition -- Friendship": PokeparkLocationData(
        144, PokeparkFlag.CHASE, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=62,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),

    #
    #
    #
    #
    #
    "Pelipper's Circle Circuit Attraction -- Prisma": PokeparkLocationData(
        145, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301, PokeparkPrismaClientData(
            structure_position=6,
            memory_range=MemoryRange.WORD
        )
    ),

    "Pelipper's Circle Circuit Attraction -- Pikachu": PokeparkLocationData(
        146, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Staraptor": PokeparkLocationData(
        147, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Togekiss": PokeparkLocationData(
        148, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Honchkrow": PokeparkLocationData(
        149, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Gliscor": PokeparkLocationData(
        150, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Pelipper": PokeparkLocationData(
        151, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Staravia": PokeparkLocationData(
        152, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Pidgeotto": PokeparkLocationData(
        153, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Butterfree": PokeparkLocationData(
        154, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Tropius": PokeparkLocationData(
        155, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Murkrow": PokeparkLocationData(
        156, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Taillow": PokeparkLocationData(
        157, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Spearow": PokeparkLocationData(
        158, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Starly": PokeparkLocationData(
        159, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Wingull": PokeparkLocationData(
        160, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Latias": PokeparkLocationData(
        161, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", 0x0301,
        PokeparkPelipperAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Latias Friendship": PokeparkLocationData(
        162, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=158,
            memory_range=MemoryRange.BYTE
        ),
    ),

    #
    #
    #
    # Gyarado's Aqua Dash

    "Gyarado's Aqua Dash Attraction -- Prisma": PokeparkLocationData(
        163, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301, PokeparkPrismaClientData(
            structure_position=5,
            memory_range=MemoryRange.WORD
        )
    ),

    "Gyarado's Aqua Dash Attraction -- Pikachu": PokeparkLocationData(
        164, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Psyduck": PokeparkLocationData(
        165, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Azurill": PokeparkLocationData(
        166, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Slowpoke": PokeparkLocationData(
        167, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Empoleon": PokeparkLocationData(
        168, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Floatzel": PokeparkLocationData(
        169, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Feraligatr": PokeparkLocationData(
        170, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Golduck": PokeparkLocationData(
        171, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Vaporeon": PokeparkLocationData(
        172, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Prinplup": PokeparkLocationData(
        173, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Bibarel": PokeparkLocationData(
        174, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Buizel": PokeparkLocationData(
        175, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Corsola": PokeparkLocationData(
        176, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Piplup": PokeparkLocationData(
        177, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Lotad": PokeparkLocationData(
        178, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Manaphy": PokeparkLocationData(
        179, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301,
        PokeparkGyaradosAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Gyarado's Aqua Dash Attraction -- Manaphy Friendship": PokeparkLocationData(
        180, PokeparkFlag.ATTRACTION, "Gyarado's Aqua Dash Attraction", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=157,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Ice Zone
    #
    #
    #
    #
    #
    #

    "Ice Zone Main Area - Lapras -- Friendship": PokeparkLocationData(
        181, PokeparkFlag.FRIENDSHIP, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=61,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Spheal Power Competition -- Friendship": PokeparkLocationData(
        182, PokeparkFlag.CHASE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=68,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Octillery Power Competition -- Friendship": PokeparkLocationData(
        183, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=73,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Delibird -- Friendship": PokeparkLocationData(
        184, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=72,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Smoochum Power Competition -- Friendship": PokeparkLocationData(
        185, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=69,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Squirtle Power Competition -- Friendship": PokeparkLocationData(
        186, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=57,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Glaceon Power Competition -- Friendship": PokeparkLocationData(
        187, PokeparkFlag.CHASE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=40,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Prinplup Power Competition -- Friendship": PokeparkLocationData(
        188, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=79,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Sneasel Power Competition -- Friendship": PokeparkLocationData(
        189, PokeparkFlag.CHASE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=70,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Piloswine Power Competition -- Friendship": PokeparkLocationData(
        190, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=76,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Glalie -- Friendship": PokeparkLocationData(
        191, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=74,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Primeape Power Competition -- Friendship": PokeparkLocationData(
        192, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=17,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Ursaring Power Competition -- Friendship": PokeparkLocationData(
        193, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=67,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Mamoswine Power Competition -- Friendship": PokeparkLocationData(
        194, PokeparkFlag.BATTLE, "Ice Zone Frozen Lake Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=77,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Kirlia -- Friendship": PokeparkLocationData(
        195, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=153,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Ice Zone Main Area - Igloo Quest -- Stage 1": PokeparkLocationData(
        196, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00000010,
            _bit_mask=0b00000010,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Ice Zone Main Area - Igloo Quest -- Stage 1 -- Primeape Unlocked": PokeparkLocationData(
        197, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00000010,
            _bit_mask=0b00000010,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Ice Zone Main Area - Igloo Quest -- Stage 2": PokeparkLocationData(
        198, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00000100,
            _bit_mask=0b00000100,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Ice Zone Main Area - Igloo Quest -- Stage 2 -- Ursaring Unlocked": PokeparkLocationData(
        199, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00000100,
            _bit_mask=0b00000100,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Ice Zone Main Area - Igloo Quest -- Stage 3": PokeparkLocationData(
        200, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkBottleIgloQuestClientData(
            structure_position=0,
            _expected_value=0b00000110,
            _bit_mask=0b00000110,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Ice Zone Main Area - Christmas Tree Present Quest -- Stage 1": PokeparkLocationData(
        201, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkChristmasTreeQuestClientData(
            structure_position=0,
            _expected_value=0b00010110,
            _bit_mask=0b00010110,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Ice Zone Main Area - Christmas Tree Present Quest -- Stage 2": PokeparkLocationData(
        202, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkChristmasTreeQuestClientData(
            structure_position=0,
            _expected_value=0b00100111,
            _bit_mask=0b00100111,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Ice Zone Main Area - Christmas Tree Present Quest -- Stage 3": PokeparkLocationData(
        203, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkChristmasTreeQuestClientData(
            structure_position=0,
            _expected_value=0b00110111,
            _bit_mask=0b00110111,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Ice Zone Main Area - Christmas Tree Present Quest -- Stage 4": PokeparkLocationData(
        204, PokeparkFlag.QUEST, "Ice Zone Main Area", 0x0302, PokeparkChristmasTreeQuestClientData(
            structure_position=0,
            _expected_value=0b01001111,
            _bit_mask=0b01001111,
            memory_range=MemoryRange.BYTE
        )
    ),

    # lower lift region
    "Ice Zone Lower Lift Area - Quagsire -- Friendship": PokeparkLocationData(
        205, PokeparkFlag.ERRAND, "Ice Zone Lower Lift Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=71,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # each zone pokemon

    "Ice Zone Main Area - Starly Power Competition -- Friendship": PokeparkLocationData(
        206, PokeparkFlag.CHASE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=20,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Krabby Power Competition -- Friendship": PokeparkLocationData(
        207, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=47,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Corphish Power Competition -- Friendship": PokeparkLocationData(
        208, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=48,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Mudkip Power Competition -- Friendship": PokeparkLocationData(
        209, PokeparkFlag.HIDEANDSEEK, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=46,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Taillow Power Competition -- Friendship": PokeparkLocationData(
        210, PokeparkFlag.CHASE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=55,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Staravia Power Competition -- Friendship": PokeparkLocationData(
        211, PokeparkFlag.CHASE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=21,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Teddiursa Power Competition -- Friendship": PokeparkLocationData(
        212, PokeparkFlag.BATTLE, "Ice Zone Main Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=66,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Lower Lift Area - Wingull Power Competition -- Friendship": PokeparkLocationData(
        213, PokeparkFlag.CHASE, "Ice Zone Lower Lift Area", 0x0302, PokeparkFriendshipClientLocationData(
            structure_position=62,
            memory_range=MemoryRange.BYTE
        ), each_zone=MultiZoneFlag.MULTI
    ),

    # Empoleon's Snow Slide
    #
    #
    #
    "Empoleon's Snow Slide Attraction -- Prisma": PokeparkLocationData(
        214, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303, PokeparkPrismaClientData(
            structure_position=8,
            memory_range=MemoryRange.WORD
        )
    ),

    "Empoleon's Snow Slide Attraction -- Pikachu": PokeparkLocationData(
        215, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Teddiursa": PokeparkLocationData(
        216, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Magikarp": PokeparkLocationData(
        217, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Empoleon": PokeparkLocationData(
        218, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Glaceon": PokeparkLocationData(
        219, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Blastoise": PokeparkLocationData(
        220, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Glalie": PokeparkLocationData(
        221, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Lapras": PokeparkLocationData(
        222, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Delibird": PokeparkLocationData(
        223, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Piloswine": PokeparkLocationData(
        224, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Prinplup": PokeparkLocationData(
        225, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Squirtle": PokeparkLocationData(
        226, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Piplup": PokeparkLocationData(
        227, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Quagsire": PokeparkLocationData(
        228, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Spheal": PokeparkLocationData(
        229, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Suicune": PokeparkLocationData(
        230, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303,
        PokeparkEmpoleonAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.WORD
        )
    ),
    "Empoleon's Snow Slide Attraction -- Suicune Friendship": PokeparkLocationData(
        231, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", 0x0303, PokeparkFriendshipClientLocationData(
            structure_position=159,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Cavern Zone
    #
    #
    #
    #
    "Cavern Zone Main Area - Magnemite -- Friendship": PokeparkLocationData(
        232, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=105,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Machamp Power Competition -- Friendship": PokeparkLocationData(
        233, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=89,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Machamp Power Competition -- Machamp Unlocked": PokeparkLocationData(
        234, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=89,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Cranidos Power Competition -- Friendship": PokeparkLocationData(
        235, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=89,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Zubat Power Competition -- Friendship": PokeparkLocationData(
        236, PokeparkFlag.CHASE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=84,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Golbat Power Competition -- Friendship": PokeparkLocationData(
        237, PokeparkFlag.CHASE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=85,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Magnezone Power Competition -- Friendship": PokeparkLocationData(
        238, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=106,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Scizor Power Competition -- Friendship": PokeparkLocationData(
        239, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=33,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Dugtrio Power Competition -- Friendship": PokeparkLocationData(
        240, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=174,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Gible Power Competition -- Friendship": PokeparkLocationData(
        241, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=82,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Phanpy Power Competition -- Friendship": PokeparkLocationData(
        242, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=86,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Hitmonlee Power Competition -- Friendship": PokeparkLocationData(
        243, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=107,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Electivire Power Competition -- Friendship": PokeparkLocationData(
        244, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=94,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Cavern Zone Main Area - Magnemite Crate Entrance -- Magnemite Unlocked": PokeparkLocationData(
        245, PokeparkFlag.POKEMON_UNLOCK, "Cavern Zone Main Area", 0x0401, PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Cavern Zone Main Area - Magnemite Crate Magma Zone Entrance -- Magnemite Unlocked": PokeparkLocationData(
        246, PokeparkFlag.POKEMON_UNLOCK, "Cavern Zone Main Area", 0x0401, PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Cavern Zone Main Area - Magnemite Crate Deep Inside -- Magnemite Unlocked": PokeparkLocationData(
        247, PokeparkFlag.POKEMON_UNLOCK, "Cavern Zone Main Area", 0x0401, PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Cavern Zone Main Area - Diglett Crate -- Magnemite Unlocked": PokeparkLocationData(
        248, PokeparkFlag.POKEMON_UNLOCK, "Cavern Zone Main Area", 0x0401, PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Cavern Zone Main Area - Bonsly Power Competition -- Friendship": PokeparkLocationData(
        249, PokeparkFlag.HIDEANDSEEK, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=12,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Bonsly Power Competition -- Sudowoodo Unlocked": PokeparkLocationData(
        250, PokeparkFlag.HIDEANDSEEK, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=12,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Teddiursa Power Competition -- Friendship": PokeparkLocationData(
        251, PokeparkFlag.QUIZ, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=66,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Chimchar Power Competition -- Friendship": PokeparkLocationData(
        252, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=112,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Sudowoodo Power Competition -- Friendship": PokeparkLocationData(
        253, PokeparkFlag.HIDEANDSEEK, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=13,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Aron Power Competition -- Friendship": PokeparkLocationData(
        254, PokeparkFlag.ERRAND, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=171,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Torchic Power Competition -- Friendship": PokeparkLocationData(
        255, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=115,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Geodude Power Competition -- Friendship": PokeparkLocationData(
        256, PokeparkFlag.HIDEANDSEEK, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=81,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Raichu Power Competition -- Friendship": PokeparkLocationData(
        257, PokeparkFlag.CHASE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=91,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Meowth Power Competition -- Friendship": PokeparkLocationData(
        258, PokeparkFlag.QUIZ, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=117,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Marowak Power Competition -- Friendship": PokeparkLocationData(
        259, PokeparkFlag.BATTLE, "Cavern Zone Main Area", 0x0401, PokeparkFriendshipClientLocationData(
            structure_position=88,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),

    # Bastiodon's Panel Crush
    #
    #
    #
    #
    "Bastiodon's Panel Crush Attraction -- Prisma": PokeparkLocationData(
        260, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401, PokeparkPrismaClientData(
            structure_position=9,
            memory_range=MemoryRange.WORD
        )
    ),

    "Bastiodon's Panel Crush Attraction -- Pikachu": PokeparkLocationData(
        261, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Sableye": PokeparkLocationData(
        262, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Meowth": PokeparkLocationData(
        263, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Torchic": PokeparkLocationData(
        264, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Electivire": PokeparkLocationData(
        265, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Magmortar": PokeparkLocationData(
        266, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Hitmonlee": PokeparkLocationData(
        267, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Ursaring": PokeparkLocationData(
        268, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Mr. Mime": PokeparkLocationData(
        269, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Raichu": PokeparkLocationData(
        270, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Sudowoodo": PokeparkLocationData(
        271, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Charmander": PokeparkLocationData(
        272, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Gible": PokeparkLocationData(
        273, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Chimchar": PokeparkLocationData(
        274, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Magby": PokeparkLocationData(
        275, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Metagross": PokeparkLocationData(
        276, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkBastiodonAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.WORD
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Metagross Friendship": PokeparkLocationData(
        277, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction", 0x0401,
        PokeparkFriendshipClientLocationData(
            structure_position=160,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Magma Zone
    #
    #
    #
    "Magma Zone Main Area - Camerupt Power Competition -- Friendship": PokeparkLocationData(
        278, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=101,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Main Area - Magby Power Competition -- Friendship": PokeparkLocationData(
        279, PokeparkFlag.CHASE, "Magma Zone Main Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=110,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Main Area - Vulpix Power Competition -- Friendship": PokeparkLocationData(
        280, PokeparkFlag.CHASE, "Magma Zone Main Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=119,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Main Area - Vulpix Power Competition -- Ninetales Unlocked": PokeparkLocationData(
        281, PokeparkFlag.CHASE, "Magma Zone Main Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=119,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Ninetales Power Competition -- Friendship": PokeparkLocationData(
        282, PokeparkFlag.CHASE, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=120,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Quilava Power Competition -- Friendship": PokeparkLocationData(
        283, PokeparkFlag.BATTLE, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=100,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Main Area - Flareon Power Competition -- Friendship": PokeparkLocationData(
        284, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=41,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Infernape Power Competition -- Friendship": PokeparkLocationData(
        285, PokeparkFlag.BATTLE, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=113,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Farfetch'd Power Competition -- Friendship": PokeparkLocationData(
        286, PokeparkFlag.BATTLE, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=102,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Ponyta Power Competition -- Friendship": PokeparkLocationData(
        287, PokeparkFlag.CHASE, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=29,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Main Area - Torkoal Power Competition -- Friendship": PokeparkLocationData(
        288, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=98,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Main Area - Golem Power Competition -- Friendship": PokeparkLocationData(
        289, PokeparkFlag.FRIENDSHIP, "Magma Zone Main Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=177,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Hitmonchan Power Competition -- Friendship": PokeparkLocationData(
        290, PokeparkFlag.BATTLE, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=108,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Hitmonchan Power Competition -- Hitmonlee Unlocked": PokeparkLocationData(
        291, PokeparkFlag.BATTLE, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=108,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Main Area - Hitmontop Power Competition -- Friendship": PokeparkLocationData(
        292, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=109,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Magmortar Power Competition -- Friendship": PokeparkLocationData(
        293, PokeparkFlag.BATTLE, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=111,
            memory_range=MemoryRange.BYTE
        ),
    ),

    "Magma Zone Blaziken Area - Blaziken Power Competition -- Friendship": PokeparkLocationData(
        294, PokeparkFlag.FRIENDSHIP, "Magma Zone Blaziken Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=116,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Circle Area - Rhyperior Iron Disc -- Quest": PokeparkLocationData(
        295, PokeparkFlag.QUEST, "Magma Zone Circle Area", 0x0402,
        PokeparkRhyperiorQuestClientData(
            structure_position=0,
            _expected_value=0b10000000,
            _bit_mask=0b10000000,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Magma Zone Main Area - Baltoy Crate -- Baltoy Unlocked": PokeparkLocationData(
        296, PokeparkFlag.POKEMON_UNLOCK, "Magma Zone Main Area", 0x0402,
        PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Magma Zone Main Area - Bonsly Power Competition -- Friendship": PokeparkLocationData(
        297, PokeparkFlag.HIDEANDSEEK, "Magma Zone Main Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=12,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Chimchar Power Competition -- Friendship": PokeparkLocationData(
        298, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=112,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Chimchar Power Competition -- Infernape Unlocked": PokeparkLocationData(
        299, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=112,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Magma Zone Main Area - Aron Power Competition -- Friendship": PokeparkLocationData(
        300, PokeparkFlag.ERRAND, "Magma Zone Main Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=171,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Torchic Power Competition -- Friendship": PokeparkLocationData(
        301, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=115,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Geodude Power Competition -- Friendship": PokeparkLocationData(
        302, PokeparkFlag.HIDEANDSEEK, "Magma Zone Main Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=81,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Baltoy Power Competition -- Friendship": PokeparkLocationData(
        303, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=103,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Baltoy Power Competition -- Claydol Unlocked": PokeparkLocationData(
        304, PokeparkFlag.BATTLE, "Magma Zone Main Area", 0x0403, PokeparkFriendshipClientLocationData(
            structure_position=103,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Circle Area - Meditite Power Competition -- Friendship": PokeparkLocationData(
        305, PokeparkFlag.QUIZ, "Magma Zone Circle Area", 0x0402, PokeparkFriendshipClientLocationData(
            structure_position=139,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    # Rhyperior's Bumper Burn
    #
    #
    #
    #

    "Rhyperior's Bumper Burn Attraction -- Prisma": PokeparkLocationData(
        306, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402, PokeparkPrismaClientData(
            structure_position=10,
            memory_range=MemoryRange.WORD
        )
    ),

    "Rhyperior's Bumper Burn Attraction -- Pikachu": PokeparkLocationData(
        307, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Magnemite": PokeparkLocationData(
        308, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Rhyperior": PokeparkLocationData(
        309, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Tyranitar": PokeparkLocationData(
        310, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Hitmontop": PokeparkLocationData(
        311, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Flareon": PokeparkLocationData(
        312, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Venusaur": PokeparkLocationData(
        313, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Snorlax": PokeparkLocationData(
        314, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Torterra": PokeparkLocationData(
        315, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Magnezone": PokeparkLocationData(
        316, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Claydol": PokeparkLocationData(
        317, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Quilava": PokeparkLocationData(
        318, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Torkoal": PokeparkLocationData(
        319, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Baltoy": PokeparkLocationData(
        320, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Bonsly": PokeparkLocationData(
        321, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Heatran": PokeparkLocationData(
        322, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkRhyperiorAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.WORD
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Heatran Friendship": PokeparkLocationData(
        323, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction", 0x0402,
        PokeparkFriendshipClientLocationData(
            structure_position=161,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Blaziken's Boulder Bash
    #
    #
    #
    #

    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Prisma": PokeparkLocationData(
        324, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403, PokeparkPrismaClientData(
            structure_position=11,
            memory_range=MemoryRange.WORD
        )
    ),

    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Pikachu": PokeparkLocationData(
        325, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Geodude": PokeparkLocationData(
        326, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Phanpy": PokeparkLocationData(
        327, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Blaziken": PokeparkLocationData(
        328, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Garchomp": PokeparkLocationData(
        329, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Scizor": PokeparkLocationData(
        330, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Magmortar": PokeparkLocationData(
        331, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Hitmonchan": PokeparkLocationData(
        332, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Machamp": PokeparkLocationData(
        333, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Marowak": PokeparkLocationData(
        334, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Farfetch'd": PokeparkLocationData(
        335, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Cranidos": PokeparkLocationData(
        336, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Camerupt": PokeparkLocationData(
        337, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Bastiodon": PokeparkLocationData(
        338, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Mawile": PokeparkLocationData(
        339, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Groudon": PokeparkLocationData(
        340, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkBlazikenAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction -- Groudon Friendship": PokeparkLocationData(
        341, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction", 0x0403,
        PokeparkFriendshipClientLocationData(
            structure_position=162,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Haunted Zone
    #
    #
    #
    #
    "Haunted Zone Main Area - Murkrow Power Competition -- Friendship": PokeparkLocationData(
        342, PokeparkFlag.CHASE, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=121,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Main Area - Murkrow Power Competition -- Honchkrow Unlocked": PokeparkLocationData(
        343, PokeparkFlag.CHASE, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=121,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Main Area - Honchkrow Power Competition -- Friendship": PokeparkLocationData(
        344, PokeparkFlag.BATTLE, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=122,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Main Area - Gliscor Power Competition -- Friendship": PokeparkLocationData(
        345, PokeparkFlag.BATTLE, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=118,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Main Area - Metapod Power Competition -- Friendship": PokeparkLocationData(
        346, PokeparkFlag.FRIENDSHIP, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=188,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Main Area - Kakuna Power Competition -- Friendship": PokeparkLocationData(
        347, PokeparkFlag.FRIENDSHIP, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=170,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Main Area - Metapod Left Tree -- Metapod Unlocked": PokeparkLocationData(
        348, PokeparkFlag.POKEMON_UNLOCK, "Haunted Zone Main Area", 0x0501, PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Haunted Zone Main Area - Kakuna Right Tree -- Metapod Unlocked": PokeparkLocationData(
        349, PokeparkFlag.POKEMON_UNLOCK, "Haunted Zone Main Area", 0x0501, PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),

    "Haunted Zone Main Area - Raichu Power Competition -- Friendship": PokeparkLocationData(
        350, PokeparkFlag.CHASE, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=91,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Meowth Power Competition -- Friendship": PokeparkLocationData(
        351, PokeparkFlag.QUIZ, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=117,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Aipom Power Competition -- Friendship": PokeparkLocationData(
        352, PokeparkFlag.CHASE, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=30,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),

    "Haunted Zone Main Area - Aipom Power Competition -- Ambipom Unlocked": PokeparkLocationData(
        353, PokeparkFlag.CHASE, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=30,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Ambipom Power Competition -- Friendship": PokeparkLocationData(
        354, PokeparkFlag.BATTLE, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=31,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Drifloon Power Competition -- Friendship": PokeparkLocationData(
        355, PokeparkFlag.FRIENDSHIP, "Haunted Zone Main Area", 0x0501, PokeparkFriendshipClientLocationData(
            structure_position=175,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),

    # Tangrowth's Swing-Along
    #
    #
    #
    #
    "Tangrowth's Swing-Along Attraction -- Prisma": PokeparkLocationData(
        356, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501, PokeparkPrismaClientData(
            structure_position=3,
            memory_range=MemoryRange.WORD
        )
    ),

    "Tangrowth's Swing-Along Attraction -- Pikachu": PokeparkLocationData(
        357, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Meowth": PokeparkLocationData(
        358, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Pichu": PokeparkLocationData(
        359, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Lucario": PokeparkLocationData(
        360, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Infernape": PokeparkLocationData(
        361, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Blaziken": PokeparkLocationData(
        362, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Riolu": PokeparkLocationData(
        363, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Sneasel": PokeparkLocationData(
        364, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Raichu": PokeparkLocationData(
        365, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Ambipom": PokeparkLocationData(
        366, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Primeape": PokeparkLocationData(
        367, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Aipom": PokeparkLocationData(
        368, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Electabuzz": PokeparkLocationData(
        369, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Chimchar": PokeparkLocationData(
        370, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Croagunk": PokeparkLocationData(
        371, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Celebi": PokeparkLocationData(
        372, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkTangrowthAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),

    "Tangrowth's Swing-Along Attraction -- Celebi Friendship": PokeparkLocationData(
        373, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction", 0x0501,
        PokeparkFriendshipClientLocationData(
            structure_position=163,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Haunted Zone Mansion
    #
    #
    #
    #
    "Haunted Zone Mansion Area - Duskull Power Competition -- Friendship": PokeparkLocationData(
        374, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=134,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Misdreavus Power Competition -- Friendship": PokeparkLocationData(
        375, PokeparkFlag.CHASE, "Haunted Zone Mansion Ballroom Area", 0x0502,
        PokeparkFriendshipClientLocationData(
            structure_position=128,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Pichu Power Competition -- Friendship": PokeparkLocationData(
        376, PokeparkFlag.CHASE, "Haunted Zone Mansion Ballroom Area", 0x0502,
        PokeparkFriendshipClientLocationData(
            structure_position=90,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Umbreon Power Competition -- Friendship": PokeparkLocationData(
        377, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=42,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Umbreon Power Competition -- Espeon Unlocked": PokeparkLocationData(
        378, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=42,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Espeon Power Competition -- Friendship": PokeparkLocationData(
        379, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=43,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Spinarak Power Competition -- Friendship": PokeparkLocationData(
        380, PokeparkFlag.FRIENDSHIP, "Haunted Zone Mansion Antic Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=179,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Riolu Power Competition -- Friendship": PokeparkLocationData(
        381, PokeparkFlag.BATTLE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=151,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Voltorb Power Competition -- Friendship": PokeparkLocationData(
        382, PokeparkFlag.CHASE, "Haunted Zone Mansion Gengar Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=151,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Elekid Power Competition -- Friendship": PokeparkLocationData(
        383, PokeparkFlag.BATTLE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=92,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Elekid Power Competition -- Electabuzz Unlocked": PokeparkLocationData(
        384, PokeparkFlag.BATTLE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=92,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Electabuzz Power Competition -- Friendship": PokeparkLocationData(
        385, PokeparkFlag.BATTLE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=93,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Luxray Power Competition -- Friendship": PokeparkLocationData(
        386, PokeparkFlag.CHASE, "Haunted Zone Mansion Ballroom Area", 0x0502,
        PokeparkFriendshipClientLocationData(
            structure_position=28,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Stunky Power Competition -- Friendship": PokeparkLocationData(
        387, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=125,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Stunky Power Competition -- Skuntank Unlocked": PokeparkLocationData(
        388, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=125,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Skuntank Power Competition -- Friendship": PokeparkLocationData(
        389, PokeparkFlag.BATTLE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=126,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Breloom Power Competition -- Friendship": PokeparkLocationData(
        390, PokeparkFlag.BATTLE, "Haunted Zone Mansion Antic Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=15,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Mismagius Power Competition -- Friendship": PokeparkLocationData(
        391, PokeparkFlag.BATTLE, "Haunted Zone Mansion Ballroom Area", 0x0502,
        PokeparkFriendshipClientLocationData(
            structure_position=129,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Electrode Power Competition -- Friendship": PokeparkLocationData(
        392, PokeparkFlag.CHASE, "Haunted Zone Mansion Ballroom Area", 0x0502,
        PokeparkFriendshipClientLocationData(
            structure_position=182,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Haunter Power Competition -- Friendship": PokeparkLocationData(
        393, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=131,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Gastly Power Competition -- Friendship": PokeparkLocationData(
        394, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=130,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Gengar Power Competition -- Friendship": PokeparkLocationData(
        395, PokeparkFlag.BATTLE, "Haunted Zone Mansion Gengar Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=132,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Haunted Zone Mansion Area - Gengar Painting -- Gengar Unlocked": PokeparkLocationData(
        396, PokeparkFlag.POKEMON_UNLOCK, "Haunted Zone Mansion Gengar Area", 0x0502, PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Haunted Zone Mansion Area - Voltorb Vase -- Voltorb Unlocked": PokeparkLocationData(
        397, PokeparkFlag.POKEMON_UNLOCK, "Haunted Zone Mansion Gengar Area", 0x0502, PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Haunted Zone Mansion Area - Abra Power Competition -- Friendship": PokeparkLocationData(
        398, PokeparkFlag.FRIENDSHIP, "Haunted Zone Mansion Antic Area", 0x0502, PokeparkFriendshipClientLocationData(
            structure_position=124,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    # Dusknoir's Speed Slam
    #
    #
    #
    #
    #
    "Dusknoir's Speed Slam Attraction -- Prisma": PokeparkLocationData(
        399, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502, PokeparkPrismaClientData(
            structure_position=4,
            memory_range=MemoryRange.WORD
        )
    ),

    "Dusknoir's Speed Slam Attraction -- Pikachu": PokeparkLocationData(
        400, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Stunky": PokeparkLocationData(
        401, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Gengar": PokeparkLocationData(
        402, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Mismagius": PokeparkLocationData(
        403, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Scizor": PokeparkLocationData(
        404, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Espeon": PokeparkLocationData(
        405, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Dusknoir": PokeparkLocationData(
        406, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Umbreon": PokeparkLocationData(
        407, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Cranidos": PokeparkLocationData(
        408, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Skuntank": PokeparkLocationData(
        409, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Electrode": PokeparkLocationData(
        410, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Gastly": PokeparkLocationData(
        411, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Duskull": PokeparkLocationData(
        412, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Misdreavus": PokeparkLocationData(
        413, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Krabby": PokeparkLocationData(
        414, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Darkrai": PokeparkLocationData(
        415, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0502,
        PokeparkDusknoirAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Darkrai Friendship": PokeparkLocationData(
        416, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction", 0x0501,
        PokeparkFriendshipClientLocationData(
            structure_position=164,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Rotom's Spooky Shoot-'em-Up
    #
    #
    #
    #
    "Rotom's Spooky Shoot-'em-Up Attraction -- Prisma": PokeparkLocationData(
        417, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503, PokeparkPrismaClientData(
            structure_position=12,
            memory_range=MemoryRange.WORD
        )
    ),

    "Rotom's Spooky Shoot-'em-Up Attraction -- Pikachu": PokeparkLocationData(
        418, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Magnemite": PokeparkLocationData(
        419, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Porygon-Z": PokeparkLocationData(
        420, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Magnezone": PokeparkLocationData(
        421, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Gengar": PokeparkLocationData(
        422, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Magmortar": PokeparkLocationData(
        423, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Electivire": PokeparkLocationData(
        424, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Mismagius": PokeparkLocationData(
        425, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Claydol": PokeparkLocationData(
        426, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Electabuzz": PokeparkLocationData(
        427, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Haunter": PokeparkLocationData(
        428, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Abra": PokeparkLocationData(
        429, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Elekid": PokeparkLocationData(
        430, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Mr. Mime": PokeparkLocationData(
        431, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Baltoy": PokeparkLocationData(
        432, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Rotom": PokeparkLocationData(
        433, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkRotomAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Rotom Friendship": PokeparkLocationData(
        434, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction", 0x0503,
        PokeparkFriendshipClientLocationData(
            structure_position=165,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Granite Zone
    #
    #
    #
    #
    "Granite Zone Main Area - Lopunny Power Competition -- Friendship": PokeparkLocationData(
        435, PokeparkFlag.CHASE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=19,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Eevee Power Competition -- Friendship": PokeparkLocationData(
        436, PokeparkFlag.CHASE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=37,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Eevee Power Competition -- Jolteon Unlocked": PokeparkLocationData(
        437, PokeparkFlag.CHASE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=37,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Charizard Power Competition -- Friendship": PokeparkLocationData(
        438, PokeparkFlag.BATTLE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=146,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Flygon Power Competition -- Friendship": PokeparkLocationData(
        439, PokeparkFlag.CHASE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=142,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Staraptor Power Competition -- Friendship": PokeparkLocationData(
        440, PokeparkFlag.BATTLE, "Granite Zone Salamence Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=22,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Staraptor Power Competition -- Aerodactyl Unlocked": PokeparkLocationData(
        441, PokeparkFlag.BATTLE, "Granite Zone Salamence Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=22,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Aerodactyl Power Competition -- Friendship": PokeparkLocationData(
        442, PokeparkFlag.BATTLE, "Granite Zone Salamence Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=141,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Arcanine Power Competition -- Friendship": PokeparkLocationData(
        443, PokeparkFlag.BATTLE, "Granite Zone Salamence Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=144,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Jolteon Power Competition -- Friendship": PokeparkLocationData(
        444, PokeparkFlag.CHASE, "Granite Zone Salamence Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=44,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Skorupi Power Competition -- Friendship": PokeparkLocationData(
        445, PokeparkFlag.FRIENDSHIP, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=186,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Porygon-Z Power Competition -- Friendship": PokeparkLocationData(
        446, PokeparkFlag.QUIZ, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=147,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Tyranitar Power Competition -- Friendship": PokeparkLocationData(
        447, PokeparkFlag.BATTLE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=149,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Garchomp Power Competition -- Friendship": PokeparkLocationData(
        448, PokeparkFlag.BATTLE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=148,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Granite Zone Main Area - Taillow Power Competition -- Friendship": PokeparkLocationData(
        449, PokeparkFlag.CHASE, "Granite Zone Salamence Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=55,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Drifloon Power Competition -- Friendship": PokeparkLocationData(
        450, PokeparkFlag.FRIENDSHIP, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=175,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Marowak Power Competition -- Friendship": PokeparkLocationData(
        451, PokeparkFlag.BATTLE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=88,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Baltoy Power Competition -- Friendship": PokeparkLocationData(
        452, PokeparkFlag.BATTLE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=103,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Baltoy Power Competition -- Claydol Unlocked": PokeparkLocationData(
        453, PokeparkFlag.BATTLE, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=103,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Furret Power Competition -- Friendship": PokeparkLocationData(
        454, PokeparkFlag.HIDEANDSEEK, "Granite Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=140,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    # Absol Hurdle Dash
    #
    #
    #
    #
    "Absol's Hurdle Bounce Attraction -- Prisma": PokeparkLocationData(
        455, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601, PokeparkPrismaClientData(
            structure_position=0x0,
            memory_range=MemoryRange.WORD
        )
    ),

    "Absol's Hurdle Bounce Attraction -- Pikachu": PokeparkLocationData(
        456, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Chikorita": PokeparkLocationData(
        457, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Absol": PokeparkLocationData(
        458, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Lucario": PokeparkLocationData(
        459, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Ponyta": PokeparkLocationData(
        460, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Ninetales": PokeparkLocationData(
        461, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Lopunny": PokeparkLocationData(
        462, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Espeon": PokeparkLocationData(
        463, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Infernape": PokeparkLocationData(
        464, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Breloom": PokeparkLocationData(
        465, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Riolu": PokeparkLocationData(
        466, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Furret": PokeparkLocationData(
        467, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Mareep": PokeparkLocationData(
        468, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Eevee": PokeparkLocationData(
        469, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Vulpix": PokeparkLocationData(
        470, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Shaymin": PokeparkLocationData(
        471, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction", 0x0601,
        PokeparkAbsolAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Shaymin Friendship": PokeparkLocationData(
        472, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkFriendshipClientLocationData(
            structure_position=156,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Salamence's Sky Race
    #
    #
    #
    #
    "Salamence's Sky Race Attraction -- Prisma": PokeparkLocationData(
        473, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601, PokeparkPrismaClientData(
            structure_position=14,
            memory_range=MemoryRange.WORD
        )
    ),

    "Salamence's Sky Race Attraction -- Pikachu": PokeparkLocationData(
        474, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Salamence": PokeparkLocationData(
        475, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Charizard": PokeparkLocationData(
        476, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Dragonite": PokeparkLocationData(
        477, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Flygon": PokeparkLocationData(
        478, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Aerodactyl": PokeparkLocationData(
        479, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Staraptor": PokeparkLocationData(
        480, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Honchkrow": PokeparkLocationData(
        481, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Gliscor": PokeparkLocationData(
        482, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Pidgeotto": PokeparkLocationData(
        483, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Togekiss": PokeparkLocationData(
        484, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Golbat": PokeparkLocationData(
        485, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Taillow": PokeparkLocationData(
        486, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Murkrow": PokeparkLocationData(
        487, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Zubat": PokeparkLocationData(
        488, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Latios": PokeparkLocationData(
        489, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkSalamenceAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Salamence's Sky Race Attraction -- Latios Friendship": PokeparkLocationData(
        490, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction", 0x0601,
        PokeparkFriendshipClientLocationData(
            structure_position=166,
            memory_range=MemoryRange.BYTE
        ),
    ),

    # Flower Zone
    #
    #
    #
    #
    #
    "Flower Zone Main Area - Skiploom Power Competition -- Friendship": PokeparkLocationData(
        491, PokeparkFlag.FRIENDSHIP, "Flower Zone Main Area", 0x0602, PokeparkFriendshipClientLocationData(
            structure_position=191,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Flower Zone Main Area - Budew Power Competition -- Friendship": PokeparkLocationData(
        492, PokeparkFlag.FRIENDSHIP, "Flower Zone Main Area", 0x0602, PokeparkFriendshipClientLocationData(
            structure_position=187,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Flower Zone Main Area - Cyndaquil Power Competition -- Friendship": PokeparkLocationData(
        493, PokeparkFlag.CHASE, "Flower Zone Main Area", 0x0602, PokeparkFriendshipClientLocationData(
            structure_position=99,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Flower Zone Main Area - Lucario Power Competition -- Friendship": PokeparkLocationData(
        494, PokeparkFlag.CHASE, "Flower Zone Main Area", 0x0602, PokeparkFriendshipClientLocationData(
            structure_position=152,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Flower Zone Main Area - Dragonite Power Competition -- Friendship": PokeparkLocationData(
        495, PokeparkFlag.CHASE, "Flower Zone Main Area", 0x0602, PokeparkFriendshipClientLocationData(
            structure_position=150,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Flower Zone Main Area - Mareep Power Competition -- Friendship": PokeparkLocationData(
        496, PokeparkFlag.CHASE, "Flower Zone Main Area", 0x0602, PokeparkFriendshipClientLocationData(
            structure_position=138,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Flower Zone Main Area - Bellossom Power Competition -- Friendship": PokeparkLocationData(
        497, PokeparkFlag.ERRAND, "Flower Zone Main Area", 0x0602, PokeparkFriendshipClientLocationData(
            structure_position=24,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Flower Zone Main Area - Teddiursa Power Competition -- Friendship": PokeparkLocationData(
        498, PokeparkFlag.BATTLE, "Flower Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=66,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Flower Zone Main Area - Furret Power Competition -- Friendship": PokeparkLocationData(
        499, PokeparkFlag.HIDEANDSEEK, "Flower Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=140,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Flower Zone Main Area - Meditite Power Competition -- Friendship": PokeparkLocationData(
        500, PokeparkFlag.QUIZ, "Flower Zone Main Area", 0x0601, PokeparkFriendshipClientLocationData(
            structure_position=139,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.MULTI
    ),

    # Rayquaza's Balloon Panic
    #
    #
    #
    #
    #
    "Rayquaza's Balloon Panic Attraction -- Prisma": PokeparkLocationData(
        501, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602, PokeparkPrismaClientData(
            structure_position=1,
            memory_range=MemoryRange.WORD
        )
    ),

    "Rayquaza's Balloon Panic Attraction -- Pikachu": PokeparkLocationData(
        502, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=0,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Lucario": PokeparkLocationData(
        503, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=2,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Glaceon": PokeparkLocationData(
        504, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=6,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Luxray": PokeparkLocationData(
        505, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=7,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Mamoswine": PokeparkLocationData(
        506, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=9,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Infernape": PokeparkLocationData(
        507, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=4,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Floatzel": PokeparkLocationData(
        508, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=5,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Rhyperior": PokeparkLocationData(
        509, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=8,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Absol": PokeparkLocationData(
        510, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=3,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Breloom": PokeparkLocationData(
        511, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=10,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Mareep": PokeparkLocationData(
        512, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=11,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Cyndaquil": PokeparkLocationData(
        513, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=14,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Totodile": PokeparkLocationData(
        514, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=13,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Chikorita": PokeparkLocationData(
        515, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=12,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Mime Jr.": PokeparkLocationData(
        516, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=15,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Deoxys": PokeparkLocationData(
        517, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkRayquazaAttractionClientData(
            structure_position=1,
            memory_range=MemoryRange.HALFWORD
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Deoxys Friendship": PokeparkLocationData(
        518, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction", 0x0602,
        PokeparkFriendshipClientLocationData(
            structure_position=168,
            memory_range=MemoryRange.BYTE
        ),
    ),
    # Skygarden
    #
    #
    #
    #
    "Skygarden - Mew Power Competition -- Stage 1": PokeparkLocationData(
        519, PokeparkFlag.ALWAYS, "Skygarden", 0x0701,
        PokeparkMewChallengeClientData(
            structure_position=0,
            _expected_value=0b00010000,
            _bit_mask=0b00010000,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Skygarden - Mew Power Competition -- Stage 2": PokeparkLocationData(
        520, PokeparkFlag.ALWAYS, "Skygarden", 0x0701,
        PokeparkMewChallengeClientData(
            structure_position=0,
            _expected_value=0b00001000,
            _bit_mask=0b00001000,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Skygarden - Mew Power Competition -- Stage 3": PokeparkLocationData(
        521, PokeparkFlag.ALWAYS, "Skygarden", 0x0701,
        PokeparkMewChallengeClientData(
            structure_position=0,
            _expected_value=0b00000100,
            _bit_mask=0b00000100,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Skygarden - Mew Power Competition -- Stage 4": PokeparkLocationData(
        522, PokeparkFlag.ALWAYS, "Skygarden", 0x0701,
        PokeparkMewChallengeClientData(
            structure_position=0,
            _expected_value=0b00000010,
            _bit_mask=0b00000010,
            memory_range=MemoryRange.BYTE
        )
    ),
    "Skygarden - Mew Power Competition -- Friendship": PokeparkLocationData(
        523, PokeparkFlag.ALWAYS, "Skygarden", 0x0701,
        PokeparkFriendshipClientLocationData(
            structure_position=169,
            memory_range=MemoryRange.BYTE
        ),
    ),

    "Skygarden - Prisma Completion -- Stage 1": PokeparkLocationData(
        524, PokeparkFlag.POSTGAME, "Skygarden", 0x0701,
        PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Skygarden - Prisma Completion -- Stage 2": PokeparkLocationData(
        525, PokeparkFlag.POSTGAME, "Skygarden", 0x0701,
        PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),
    "Skygarden - Prisma Completion -- Completed": PokeparkLocationData(
        526, PokeparkFlag.POSTGAME, "Skygarden", 0x0701,
        PokeparkBaseClientLocationData(
            # TODO: add client Data
        )
    ),

    "Beach Zone Middle Isle - Piplup Power Competition -- Friendship": PokeparkLocationData(
        527, PokeparkFlag.BATTLE, "Beach Zone Middle Isle", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=78,
            memory_range=MemoryRange.BYTE
        )
    ),

    "Abra - Friendship": PokeparkLocationData(
        528, PokeparkFlag.ALWAYS, "Abra", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=124,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Spearow Power Competition -- Friendship": PokeparkLocationData(
        529, PokeparkFlag.BATTLE, "Spearow", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=25,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Starly Power Competition -- Friendship": PokeparkLocationData(
        530, PokeparkFlag.CHASE, "Starly", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=20,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Bonsly Power Competition -- Friendship": PokeparkLocationData(
        531, PokeparkFlag.HIDEANDSEEK, "Bonsly", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=12,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Bonsly Power Competition -- Sudowoodo Unlocked": PokeparkLocationData(
        532, PokeparkFlag.HIDEANDSEEK, "Bonsly Unlocks", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=12,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Chimchar Power Competition -- Friendship": PokeparkLocationData(
        533, PokeparkFlag.BATTLE, "Chimchar", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=112,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Sudowoodo Power Competition -- Friendship": PokeparkLocationData(
        534, PokeparkFlag.HIDEANDSEEK, "Sudowoodo", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=13,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Aipom Power Competition -- Friendship": PokeparkLocationData(
        535, PokeparkFlag.CHASE, "Aipom", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=30,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Aipom Power Competition -- Ambipom Unlocked": PokeparkLocationData(
        536, PokeparkFlag.CHASE, "Aipom Unlocks", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=30,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Ambipom Power Competition -- Friendship": PokeparkLocationData(
        537, PokeparkFlag.BATTLE, "Ambipom", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=31,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Krabby Power Competition -- Friendship": PokeparkLocationData(
        538, PokeparkFlag.BATTLE, "Krabby", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=47,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Mudkip Power Competition -- Friendship": PokeparkLocationData(
        539, PokeparkFlag.HIDEANDSEEK, "Mudkip", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=46,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Taillow Power Competition -- Friendship": PokeparkLocationData(
        540, PokeparkFlag.CHASE, "Taillow", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=55,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Staravia Power Competition -- Friendship": PokeparkLocationData(
        541, PokeparkFlag.CHASE, "Staravia", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=21,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Wingull Power Competition -- Friendship": PokeparkLocationData(
        542, PokeparkFlag.CHASE, "Wingull", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=62,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Corphish Power Competition -- Friendship": PokeparkLocationData(
        543, PokeparkFlag.BATTLE, "Corphish", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=48,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Teddiursa Power Competition -- Friendship": PokeparkLocationData(
        544, PokeparkFlag.FRIENDSHIP, "Teddiursa", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=66,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Aron Power Competition -- Friendship": PokeparkLocationData(
        545, PokeparkFlag.ERRAND, "Aron", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=171,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Torchic Power Competition -- Friendship": PokeparkLocationData(
        546, PokeparkFlag.BATTLE, "Torchic", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=115,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Geodude Power Competition -- Friendship": PokeparkLocationData(
        547, PokeparkFlag.HIDEANDSEEK, "Geodude", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=81,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Raichu Power Competition -- Friendship": PokeparkLocationData(
        548, PokeparkFlag.CHASE, "Raichu", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=91,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Meowth Power Competition -- Friendship": PokeparkLocationData(
        549, PokeparkFlag.QUIZ, "Meowth", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=117,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Marowak Power Competition -- Friendship": PokeparkLocationData(
        550, PokeparkFlag.BATTLE, "Marowak", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=88,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Baltoy Power Competition -- Friendship": PokeparkLocationData(
        551, PokeparkFlag.BATTLE, "Baltoy", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=103,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Baltoy Power Competition -- Claydol Unlocked": PokeparkLocationData(
        552, PokeparkFlag.BATTLE, "Baltoy Unlocks", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=103,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Meditite Power Competition -- Friendship": PokeparkLocationData(
        553, PokeparkFlag.QUIZ, "Meditite", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=139,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Drifloon Power Competition -- Friendship": PokeparkLocationData(
        554, PokeparkFlag.FRIENDSHIP, "Drifloon", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=175,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Furret Power Competition -- Friendship": PokeparkLocationData(
        555, PokeparkFlag.HIDEANDSEEK, "Furret", 0x0000, PokeparkFriendshipClientLocationData(
            structure_position=140,
            memory_range=MemoryRange.BYTE
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),

    "Beach Zone Main Area - Pelipper -- Friendship": PokeparkLocationData(
        556, PokeparkFlag.FRIENDSHIP, "Beach Zone Main Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=63,
            memory_range=MemoryRange.BYTE
        ),
    ),
    "Beach Zone Recycle Area - Gyarados -- Friendship": PokeparkLocationData(
        557, PokeparkFlag.FRIENDSHIP, "Beach Zone Recycle Area", 0x0301, PokeparkFriendshipClientLocationData(
            structure_position=65,
            memory_range=MemoryRange.BYTE
        ),
    ),
}

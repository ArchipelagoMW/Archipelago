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
    ATTRACTION = auto()
    ATTRACTION_PRISMA = auto()
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

    # These will be set by subclasses
    memory_range: MemoryRange = field(init=False)
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
        self.memory_range = MemoryRange.WORD


# currently separate classes for flags until more data is available
@dataclass
class PokeparkThunderboltUpgradeClientLocationData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x3c
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkIronTailUpgradeMetapodTreeClientLocationData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x3e
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkDoubleDashUpgradeClientLocationData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x4a
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkDashHealthUpgradeClientLocationData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x3d
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkWeedleTreeClientData(PokeparkBaseClientLocationData):  # f9901TalkCelebi same byte
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None
    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x4b
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkCaterpieTreeClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None
    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x4b
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkShroomishCrateMagnemite3CrateDiglettCrateBaltoyCrateClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None
    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x41
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkKakunaTreeVoltorbVaseClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x38
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE

@dataclass
class PokeparkMagikarpRescueClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None
    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x50
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkPrismaCompletionClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x52
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkMewChallengeGengarPaintingClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x51
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkGolemUnlockFlagClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x48
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkBottleIgloHousingClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x31
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkChristmasTreeClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x43
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkRhyperiorErrandMagnemite2CrateFlagClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x40
        self.in_structure_offset = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.in_structure_address_interval = 0x0
        self.memory_range = MemoryRange.BYTE

@dataclass
class PokeparkBidoofHousingClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x2f
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkF0301BippaFlagClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x46
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.memory_range = MemoryRange.BYTE


@dataclass
class PokeparkMagnemite1CrateFlagClientData(PokeparkBaseClientLocationData):
    _expected_value: Optional[int] = None
    _bit_mask: Optional[int] = None

    def __post_init__(self):
        assert self._expected_value is not None
        assert self._bit_mask is not None
        self.global_manager_data_struc_offset = 0x3b
        self.in_structure_offset = 0x0
        self.in_structure_address_interval = 0x0
        self.expected_value = self._expected_value
        self.bit_mask = self._bit_mask
        self.memory_range = MemoryRange.BYTE

@dataclass
class PokeparkBulbasaurAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2E50
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


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
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkGyaradosAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x21A8
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkEmpoleonAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2574
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkBastiodonAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x26B8
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkRhyperiorAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x27FC
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkBlazikenAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2940
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkTangrowthAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1F20
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkDusknoirAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2064
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkRotomAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2a84
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkAbsolAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1B54
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkSalamenceAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2D0C
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class PokeparkRayquazaAttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x1C98
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class Pokepark07AttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2430
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


@dataclass
class Pokepark13AttractionClientData(PokeparkBaseClientLocationData):
    def __post_init__(self):
        self.global_manager_data_struc_offset = 0x2bc8
        self.in_structure_offset = 0x0
        self.expected_value = 0x0001
        self.in_structure_address_interval = 0xc
        self.bit_mask = 0xFFFFFFFF  # using whole value
        self.memory_range = MemoryRange.HALFWORD


class PokeparkLocation(Location):
    game: str = "PokePark"

    def __init__(self, player: int, name: str, parent: Region, data: PokeparkLocationData):
        address = None if data.code is None else PokeparkLocation.get_apid(data.code)
        super().__init__(player, name, address=address, parent=parent)

        self.code = data.code
        self.flags = data.flags
        self.region = data.region
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


MEW_GOAL_CODE = 546
POSTGAME_PRISMA_GOAL_CODE = 549
LOCATION_TABLE: dict[str, PokeparkLocationData] = {
    # Treehouse
    "Treehouse - Burmy - Friendship": PokeparkLocationData(
        0, PokeparkFlag.ALWAYS, "Treehouse", PokeparkFriendshipClientLocationData(
            structure_position=183
        )
    ),
    "Treehouse - Mime Jr. - Friendship": PokeparkLocationData(
        1, PokeparkFlag.ALWAYS, "Treehouse", PokeparkFriendshipClientLocationData(
            structure_position=95
        )
    ),
    "Treehouse - Abra - Friendship": PokeparkLocationData(
        2, PokeparkFlag.ALWAYS, "Treehouse", PokeparkFriendshipClientLocationData(
            structure_position=124,
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Treehouse - Drifblim - Friendship": PokeparkLocationData(
        3, PokeparkFlag.ALWAYS, "Treehouse", PokeparkFriendshipClientLocationData(
            structure_position=176
        )
    ),
    "Treehouse - Power Up - Thunderbolt Upgrade 1": PokeparkLocationData(
        4, PokeparkFlag.POWER_UP, "Treehouse", PokeparkThunderboltUpgradeClientLocationData(

            _expected_value=0b00000001,
            _bit_mask=0b00000001
        )
    ),
    "Treehouse - Power Up - Thunderbolt Upgrade 2": PokeparkLocationData(
        5, PokeparkFlag.POWER_UP, "Treehouse", PokeparkThunderboltUpgradeClientLocationData(

            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Treehouse - Power Up - Thunderbolt Upgrade 3": PokeparkLocationData(
        6, PokeparkFlag.POWER_UP, "Treehouse", PokeparkThunderboltUpgradeClientLocationData(

            _expected_value=0b00000011,
            _bit_mask=0b00000011
        )
    ),
    "Treehouse - Power Up - Dash Upgrade 1": PokeparkLocationData(
        7, PokeparkFlag.POWER_UP, "Treehouse", PokeparkDashHealthUpgradeClientLocationData(

            _expected_value=0b00010000,
            _bit_mask=0b00010000
        )
    ),
    "Treehouse - Power Up - Dash Upgrade 2": PokeparkLocationData(
        8, PokeparkFlag.POWER_UP, "Treehouse", PokeparkDashHealthUpgradeClientLocationData(

            _expected_value=0b00100000,
            _bit_mask=0b00100000
        )
    ),
    "Treehouse - Power Up - Ponyta Unlocked": PokeparkLocationData(
        9, PokeparkFlag.POWER_UP, "Treehouse", PokeparkDashHealthUpgradeClientLocationData(

            _expected_value=0b00100000,
            _bit_mask=0b00100000
        )
    ),
    "Treehouse - Power Up - Dash Upgrade 3": PokeparkLocationData(
        10, PokeparkFlag.POWER_UP, "Treehouse", PokeparkDashHealthUpgradeClientLocationData(

            _expected_value=0b00110000,
            _bit_mask=0b00110000
        )
    ),
    "Treehouse - Power Up - Double Dash Upgrade": PokeparkLocationData(
        11, PokeparkFlag.POWER_UP, "Treehouse", PokeparkDoubleDashUpgradeClientLocationData(

            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Treehouse - Power Up - Health Upgrade 1": PokeparkLocationData(
        12, PokeparkFlag.POWER_UP, "Treehouse", PokeparkDashHealthUpgradeClientLocationData(

            _expected_value=0b00000001,
            _bit_mask=0b00000001
        )
    ),
    "Treehouse - Power Up - Health Upgrade 2": PokeparkLocationData(
        13, PokeparkFlag.POWER_UP, "Treehouse", PokeparkDashHealthUpgradeClientLocationData(

            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),

    "Treehouse - Power Up - Health Upgrade 3": PokeparkLocationData(
        14, PokeparkFlag.POWER_UP, "Treehouse", PokeparkDashHealthUpgradeClientLocationData(

            _expected_value=0b00000011,
            _bit_mask=0b00000011
        )
    ),
    "Treehouse - Power Up - Iron Tail Upgrade 1": PokeparkLocationData(
        15, PokeparkFlag.POWER_UP, "Treehouse", PokeparkIronTailUpgradeMetapodTreeClientLocationData(

            _expected_value=0b00010000,
            _bit_mask=0b00010000
        )
    ),
    "Treehouse - Power Up - Iron Tail Upgrade 2": PokeparkLocationData(
        16, PokeparkFlag.POWER_UP, "Treehouse", PokeparkIronTailUpgradeMetapodTreeClientLocationData(

            _expected_value=0b00100000,
            _bit_mask=0b00100000
        )
    ),
    "Treehouse - Power Up - Iron Tail Upgrade 3": PokeparkLocationData(
        17, PokeparkFlag.POWER_UP, "Treehouse", PokeparkIronTailUpgradeMetapodTreeClientLocationData(

            _expected_value=0b00110000,
            _bit_mask=0b00110000
        )
    ),
    # Meadow Zone Main Area
    "Meadow Zone Main Area - Turtwig Power Competition -- Friendship": PokeparkLocationData(
        18, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=0
        )
    ),
    "Meadow Zone Main Area - Turtwig Power Competition -- Pachirisu Unlocked": PokeparkLocationData(
        19, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=0
        )
    ),
    "Meadow Zone Main Area - Turtwig Power Competition -- Bonsly Unlocked": PokeparkLocationData(
        20, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=0
        )
    ),
    "Meadow Zone Main Area - Bulbasaur -- Friendship": PokeparkLocationData(
        21, PokeparkFlag.FRIENDSHIP, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=35
        )
    ),
    "Meadow Zone Main Area - Buneary Power Competition -- Friendship": PokeparkLocationData(
        22, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=18
        )
    ),
    "Meadow Zone Main Area - Buneary Power Competition -- Lotad Unlocked": PokeparkLocationData(
        23, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=18
        )
    ),
    "Meadow Zone Main Area - Buneary Power Competition -- Shinx Unlocked": PokeparkLocationData(
        24, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=18
        )
    ),
    "Meadow Zone Main Area - Munchlax Errand -- Friendship": PokeparkLocationData(
        25, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=10
        )
    ),
    "Meadow Zone Main Area - Munchlax Errand -- Tropius Unlocked": PokeparkLocationData(
        26, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=10
        )
    ),
    "Meadow Zone Main Area - Tropius Errand -- Friendship": PokeparkLocationData(
        27, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=26
        )
    ),
    "Meadow Zone Main Area - Pachirisu Power Competition -- Friendship": PokeparkLocationData(
        28, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=3
        )
    ),
    "Meadow Zone Main Area - Shinx Power Competition -- Friendship": PokeparkLocationData(
        29, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=27
        )
    ),
    "Meadow Zone Main Area - Mankey Power Competition -- Friendship": PokeparkLocationData(
        30, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=16
        )
    ),
    "Meadow Zone Main Area - Mankey Power Competition -- Chimchar Unlocked": PokeparkLocationData(
        31, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=16
        )
    ),
    "Meadow Zone Main Area - Spearow Power Competition -- Friendship": PokeparkLocationData(
        32, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=25
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Croagunk Power Competition -- Friendship": PokeparkLocationData(
        33, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=34
        )
    ),
    "Meadow Zone Main Area - Croagunk Power Competition -- Scyther Unlocked": PokeparkLocationData(
        34, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=34
        )
    ),
    "Meadow Zone Main Area - Lotad Power Competition -- Friendship": PokeparkLocationData(
        35, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=4
        )
    ),
    "Meadow Zone Main Area - Treecko Power Competition -- Friendship": PokeparkLocationData(
        36, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=2
        )
    ),
    "Meadow Zone Main Area - Caterpie Tree -- Caterpie Unlocked": PokeparkLocationData(
        37, PokeparkFlag.POKEMON_UNLOCK, "Meadow Zone Main Area", PokeparkCaterpieTreeClientData(
            _expected_value=0b00000001,
            _bit_mask=0b00000001
        ),
    ),
    "Meadow Zone Main Area - Caterpie Power Competition -- Friendship": PokeparkLocationData(
        38, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=8
        )
    ),
    "Meadow Zone Main Area - Caterpie Power Competition -- Butterfree Unlocked": PokeparkLocationData(
        39, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=8
        )
    ),
    "Meadow Zone Main Area - Weedle Tree -- Weedle Unlocked": PokeparkLocationData(
        40, PokeparkFlag.POKEMON_UNLOCK, "Meadow Zone Main Area", PokeparkWeedleTreeClientData(
            _expected_value=0b00001000,
            _bit_mask=0b00001000
        ),
    ),
    "Meadow Zone Main Area - Weedle Power Competition -- Friendship": PokeparkLocationData(
        41, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=7
        )
    ),
    "Meadow Zone Main Area - Shroomish Crate -- Shroomish Unlocked": PokeparkLocationData(
        42, PokeparkFlag.POKEMON_UNLOCK, "Meadow Zone Main Area",
        PokeparkShroomishCrateMagnemite3CrateDiglettCrateBaltoyCrateClientData(

            _expected_value=0b10000000,
            _bit_mask=0b10000000
        ),
    ),
    "Meadow Zone Main Area - Shroomish Power Competition -- Friendship": PokeparkLocationData(
        43, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=14
        )
    ),
    "Meadow Zone Main Area - Magikarp Rescue -- Magikarp Unlocked": PokeparkLocationData(
        44, PokeparkFlag.POKEMON_UNLOCK, "Meadow Zone Main Area", PokeparkMagikarpRescueClientData(
            _expected_value=0b10000000,
            _bit_mask=0b10000000
        ),
    ),
    "Meadow Zone Main Area - Oddish Power Competition -- Friendship": PokeparkLocationData(
        45, PokeparkFlag.HIDEANDSEEK, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=23
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Stage 1": PokeparkLocationData(
        46, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkBidoofHousingClientData(

            _expected_value=0b00000110,
            _bit_mask=0b00000110
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Bidoof 1 Unlocked": PokeparkLocationData(
        47, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkBidoofHousingClientData(

            _expected_value=0b00000110,
            _bit_mask=0b00000110
        )
    ),

    "Meadow Zone Main Area - Bidoof Housing -- Stage 2": PokeparkLocationData(
        48, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkBidoofHousingClientData(

            _expected_value=0b00001010,
            _bit_mask=0b00001010
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Bidoof 2 Unlocked": PokeparkLocationData(
        49, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkBidoofHousingClientData(

            _expected_value=0b00001010,
            _bit_mask=0b00001010
        )
    ),

    "Meadow Zone Main Area - Bidoof Housing -- Stage 3": PokeparkLocationData(
        50, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkBidoofHousingClientData(

            _expected_value=0b00001110,
            _bit_mask=0b00001110
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Bidoof 3 Unlocked": PokeparkLocationData(
        51, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkBidoofHousingClientData(

            _expected_value=0b00001110,
            _bit_mask=0b00001110
        )
    ),

    "Meadow Zone Main Area - Bidoof Housing -- Stage 4": PokeparkLocationData(
        52, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkBidoofHousingClientData(

            _expected_value=0b00010010,
            _bit_mask=0b00010010
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing -- Bibarel Unlocked": PokeparkLocationData(
        53, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkBidoofHousingClientData(

            _expected_value=0b00010010,
            _bit_mask=0b00010010
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing Completed -- Friendship": PokeparkLocationData(
        54, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=5
        )
    ),
    "Meadow Zone Main Area - Bidoof Housing Completed -- Beach Bidoof Unlocked": PokeparkLocationData(
        55, PokeparkFlag.ERRAND, "Meadow Zone Main Area", PokeparkF0301BippaFlagClientData(

            _expected_value=0b00000001,
            _bit_mask=0b00000001
        )
    ),
    "Meadow Zone Main Area - Bibarel Power Competition -- Friendship": PokeparkLocationData(
        56, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=6
        )
    ),
    "Meadow Zone Main Area - Leafeon Power Competition -- Friendship": PokeparkLocationData(
        57, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=38
        )
    ),
    "Meadow Zone Main Area - Torterra Power Competition -- Friendship": PokeparkLocationData(
        58, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=1
        )
    ),
    "Meadow Zone Main Area - Scyther Power Competition -- Friendship": PokeparkLocationData(
        59, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=32
        )
    ),
    "Meadow Zone Main Area - Starly Power Competition -- Friendship": PokeparkLocationData(
        60, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=20
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Bonsly Power Competition -- Friendship": PokeparkLocationData(
        61, PokeparkFlag.HIDEANDSEEK, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=12
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Bonsly Power Competition -- Sudowoodo Unlocked": PokeparkLocationData(
        62, PokeparkFlag.HIDEANDSEEK, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=12
        ), each_zone=MultiZoneFlag.MULTI
    ),

    "Meadow Zone Main Area - Chimchar Power Competition -- Friendship": PokeparkLocationData(
        63, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=112
        ), each_zone=MultiZoneFlag.MULTI
    ),

    "Meadow Zone Main Area - Sudowoodo Power Competition -- Friendship": PokeparkLocationData(
        64, PokeparkFlag.HIDEANDSEEK, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=13
        ), each_zone=MultiZoneFlag.MULTI
    ),

    "Meadow Zone Main Area - Aipom Power Competition -- Friendship": PokeparkLocationData(
        65, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=30
        ), each_zone=MultiZoneFlag.MULTI
    ),

    "Meadow Zone Main Area - Aipom Power Competition -- Ambipom Unlocked": PokeparkLocationData(
        66, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=30
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Ambipom Power Competition -- Friendship": PokeparkLocationData(
        67, PokeparkFlag.BATTLE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=31
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Meadow Zone Main Area - Magikarp Power Competition -- Friendship": PokeparkLocationData(
        68, PokeparkFlag.CHASE, "Meadow Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=64
        )
    ),

    # Bulbasaur's Daring Dash Minigame

    "Bulbasaur's Daring Dash Attraction -- Prisma": PokeparkLocationData(
        69, PokeparkFlag.ATTRACTION_PRISMA, "Bulbasaur's Daring Dash Attraction", PokeparkPrismaClientData(
            structure_position=15
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Pikachu": PokeparkLocationData(
        70, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=0
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Turtwig": PokeparkLocationData(
        71, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=15
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Munchlax": PokeparkLocationData(
        72, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=20
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Chimchar": PokeparkLocationData(
        73, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=12
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Treecko": PokeparkLocationData(
        74, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=13
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Bibarel": PokeparkLocationData(
        75, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=14
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Bulbasaur": PokeparkLocationData(
        76, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=16
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Bidoof": PokeparkLocationData(
        77, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=17
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Oddish": PokeparkLocationData(
        78, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=18
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Shroomish": PokeparkLocationData(
        79, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=19
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Bonsly": PokeparkLocationData(
        80, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=21
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Lotad": PokeparkLocationData(
        81, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=22
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Weedle": PokeparkLocationData(
        82, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=23
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Caterpie": PokeparkLocationData(
        83, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=24
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Magikarp": PokeparkLocationData(
        84, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=25
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Jolteon": PokeparkLocationData(
        85, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=3
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Arcanine": PokeparkLocationData(
        86, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=2
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Leafeon": PokeparkLocationData(
        87, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=4
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Scyther": PokeparkLocationData(
        88, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=5
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Ponyta": PokeparkLocationData(
        89, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=6
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Shinx": PokeparkLocationData(
        90, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=7
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Eevee": PokeparkLocationData(
        91, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=8
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Pachirisu": PokeparkLocationData(
        92, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=9
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Buneary": PokeparkLocationData(
        93, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=10
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Croagunk": PokeparkLocationData(
        94, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=11
        )
    ),
    "Bulbasaur's Daring Dash Attraction -- Mew": PokeparkLocationData(
        95, PokeparkFlag.ATTRACTION, "Bulbasaur's Daring Dash Attraction",
        PokeparkBulbasaurAttractionClientData(
            structure_position=1
        )
    ),

    "Meadow Zone Venusaur Area - Venusaur -- Friendship": PokeparkLocationData(
        96, PokeparkFlag.FRIENDSHIP, "Meadow Zone Venusaur Area", PokeparkFriendshipClientLocationData(
            structure_position=36
        )
    ),

    "Venusaur's Vine Swing Attraction -- Prisma": PokeparkLocationData(
        97, PokeparkFlag.ATTRACTION_PRISMA, "Venusaur's Vine Swing Attraction", PokeparkPrismaClientData(
            structure_position=2
        )
    ),
    "Venusaur's Vine Swing Attraction -- Pikachu": PokeparkLocationData(
        98, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=0
        )
    ),
    "Venusaur's Vine Swing Attraction -- Munchlax": PokeparkLocationData(
        99, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=14
        )
    ),
    "Venusaur's Vine Swing Attraction -- Magikarp": PokeparkLocationData(
        100, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=15
        )
    ),
    "Venusaur's Vine Swing Attraction -- Blaziken": PokeparkLocationData(
        101, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=2
        )
    ),
    "Venusaur's Vine Swing Attraction -- Infernape": PokeparkLocationData(
        102, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=3
        )
    ),
    "Venusaur's Vine Swing Attraction -- Lucario": PokeparkLocationData(
        103, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=4
        )
    ),
    "Venusaur's Vine Swing Attraction -- Primeape": PokeparkLocationData(
        104, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=6
        )
    ),
    "Venusaur's Vine Swing Attraction -- Tangrowth": PokeparkLocationData(
        105, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=5
        )
    ),
    "Venusaur's Vine Swing Attraction -- Ambipom": PokeparkLocationData(
        106, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=7
        )
    ),
    "Venusaur's Vine Swing Attraction -- Croagunk": PokeparkLocationData(
        107, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=12
        )
    ),
    "Venusaur's Vine Swing Attraction -- Mankey": PokeparkLocationData(
        108, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=8
        )
    ),
    "Venusaur's Vine Swing Attraction -- Aipom": PokeparkLocationData(
        109, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=9
        )
    ),
    "Venusaur's Vine Swing Attraction -- Chimchar": PokeparkLocationData(
        110, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=10
        )
    ),
    "Venusaur's Vine Swing Attraction -- Treecko": PokeparkLocationData(
        111, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=11
        )
    ),
    "Venusaur's Vine Swing Attraction -- Pachirisu": PokeparkLocationData(
        112, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=13
        )
    ),
    "Venusaur's Vine Swing Attraction -- Jirachi": PokeparkLocationData(
        113, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction",
        PokeparkVenusaurAttractionClientData(
            structure_position=1
        )
    ),

    "Venusaur's Vine Swing Attraction -- Jirachi Friendship": PokeparkLocationData(
        114, PokeparkFlag.ATTRACTION, "Venusaur's Vine Swing Attraction", PokeparkFriendshipClientLocationData(
            structure_position=167
        ),
    ),
    # Beach Zone
    "Beach Zone Main Area - Buizel Power Competition -- Friendship": PokeparkLocationData(
        115, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=51
        ),
    ),
    "Beach Zone Main Area - Buizel Power Competition -- Floatzel Unlocked": PokeparkLocationData(
        116, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=51
        ),
    ),
    "Beach Zone Main Area - Psyduck Power Competition -- Friendship": PokeparkLocationData(
        117, PokeparkFlag.HIDEANDSEEK, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=53
        ),
    ),
    "Beach Zone Main Area - Psyduck Power Competition -- Golduck Unlocked": PokeparkLocationData(
        118, PokeparkFlag.HIDEANDSEEK, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=53
        ),
    ),
    "Beach Zone Main Area - Slowpoke Power Competition -- Friendship": PokeparkLocationData(
        119, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=50
        ),
    ),
    "Beach Zone Main Area - Slowpoke Power Competition -- Mudkip Unlocked": PokeparkLocationData(
        120, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=50
        ),
    ),
    "Beach Zone Main Area - Azurill Power Competition -- Friendship": PokeparkLocationData(
        121, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=45
        ),
    ),
    "Beach Zone Main Area - Azurill Power Competition -- Totodile Unlocked": PokeparkLocationData(
        122, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=45
        ),
    ),
    "Beach Zone Main Area - Totodile Power Competition -- Friendship": PokeparkLocationData(
        123, PokeparkFlag.BATTLE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=59
        ),
    ),
    "Beach Zone Main Area - Pidgeotto Power Competition -- Friendship": PokeparkLocationData(
        124, PokeparkFlag.BATTLE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=56
        ),
    ),
    "Beach Zone Main Area - Corsola Power Competition -- Friendship": PokeparkLocationData(
        125, PokeparkFlag.QUIZ, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=49
        ),
    ),
    "Beach Zone Main Area - Floatzel Power Competition -- Friendship": PokeparkLocationData(
        126, PokeparkFlag.BATTLE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=52
        ),
    ),
    "Beach Zone Main Area - Vaporeon Power Competition -- Friendship": PokeparkLocationData(
        127, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=39
        ),
    ),
    "Beach Zone Main Area - Golduck Power Competition -- Friendship": PokeparkLocationData(
        128, PokeparkFlag.BATTLE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=54
        ),
    ),
    "Beach Zone Main Area - Wailord Power Competition -- Friendship": PokeparkLocationData(
        129, PokeparkFlag.ERRAND, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=190
        ),
    ),
    "Beach Zone Main Area - Feraligatr Power Competition -- Friendship": PokeparkLocationData(
        130, PokeparkFlag.BATTLE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=60
        ),
    ),
    "Beach Zone Main Area - Blastoise Power Competition -- Friendship": PokeparkLocationData(
        131, PokeparkFlag.BATTLE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=58
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 1": PokeparkLocationData(
        132, PokeparkFlag.ERRAND, "Beach Zone Recycle Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00010000,
            _bit_mask=0b00010000
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 2": PokeparkLocationData(
        133, PokeparkFlag.ERRAND, "Beach Zone Recycle Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00100000,
            _bit_mask=0b00100000
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 2 --- Krabby Unlocked": PokeparkLocationData(
        134, PokeparkFlag.ERRAND, "Beach Zone Recycle Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00100000,
            _bit_mask=0b00100000
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 3": PokeparkLocationData(
        135, PokeparkFlag.ERRAND, "Beach Zone Recycle Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00110000,
            _bit_mask=0b00110000
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 4": PokeparkLocationData(
        136, PokeparkFlag.ERRAND, "Beach Zone Recycle Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b01000000,
            _bit_mask=0b01000000
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 4 --- Corphish Unlocked": PokeparkLocationData(
        137, PokeparkFlag.ERRAND, "Beach Zone Recycle Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b01000000,
            _bit_mask=0b01000000
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 5": PokeparkLocationData(
        138, PokeparkFlag.ERRAND, "Beach Zone Recycle Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b01010000,
            _bit_mask=0b01010000
        ),
    ),
    "Beach Zone Recycle Area - Bottle Recycling -- Stage 6": PokeparkLocationData(
        139, PokeparkFlag.ERRAND, "Beach Zone Recycle Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b01100000,
            _bit_mask=0b01100000
        ),
    ),

    "Beach Zone Main Area - Krabby Power Competition -- Friendship": PokeparkLocationData(
        140, PokeparkFlag.BATTLE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=47
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Starly Power Competition -- Friendship": PokeparkLocationData(
        141, PokeparkFlag.CHASE, "Beach Zone Main Area", Pokepark07AttractionClientData(
            structure_position=0
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Mudkip Power Competition -- Friendship": PokeparkLocationData(
        142, PokeparkFlag.HIDEANDSEEK, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=46
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Taillow Power Competition -- Friendship": PokeparkLocationData(
        143, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=55
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Staravia Power Competition -- Friendship": PokeparkLocationData(
        144, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=21
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Wingull Power Competition -- Friendship": PokeparkLocationData(
        145, PokeparkFlag.CHASE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=62
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Middle Isle - Piplup Power Competition -- Friendship": PokeparkLocationData(
        146, PokeparkFlag.BATTLE, "Beach Zone Middle Isle", PokeparkFriendshipClientLocationData(
            structure_position=78
        )
    ),
    "Beach Zone Main Area - Corphish Power Competition -- Friendship": PokeparkLocationData(
        147, PokeparkFlag.BATTLE, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=48
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Spearow Power Competition -- Friendship": PokeparkLocationData(
        148, PokeparkFlag.BATTLE, "Beach Zone Main Area", Pokepark13AttractionClientData(
            structure_position=5
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Beach Zone Main Area - Pelipper -- Friendship": PokeparkLocationData(
        149, PokeparkFlag.FRIENDSHIP, "Beach Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=63
        ),
    ),
    "Beach Zone Recycle Area - Gyarados -- Friendship": PokeparkLocationData(
        150, PokeparkFlag.FRIENDSHIP, "Beach Zone Recycle Area", PokeparkFriendshipClientLocationData(
            structure_position=65
        ),
    ),
    "Pelipper's Circle Circuit Attraction -- Prisma": PokeparkLocationData(
        151, PokeparkFlag.ATTRACTION_PRISMA, "Pelipper's Circle Circuit Attraction", PokeparkPrismaClientData(
            structure_position=6
        )
    ),

    "Pelipper's Circle Circuit Attraction -- Pikachu": PokeparkLocationData(
        152, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=15
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Staraptor": PokeparkLocationData(
        153, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=1
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Togekiss": PokeparkLocationData(
        154, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=2
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Honchkrow": PokeparkLocationData(
        155, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=3
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Gliscor": PokeparkLocationData(
        156, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=6
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Pelipper": PokeparkLocationData(
        157, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=9
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Staravia": PokeparkLocationData(
        158, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=4
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Pidgeotto": PokeparkLocationData(
        159, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=5
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Butterfree": PokeparkLocationData(
        160, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=14
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Tropius": PokeparkLocationData(
        161, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=13
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Murkrow": PokeparkLocationData(
        162, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=11
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Taillow": PokeparkLocationData(
        163, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=7
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Spearow": PokeparkLocationData(
        164, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=8
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Starly": PokeparkLocationData(
        165, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=10
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Wingull": PokeparkLocationData(
        166, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=12
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Latias": PokeparkLocationData(
        167, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction",
        PokeparkPelipperAttractionClientData(
            structure_position=0
        )
    ),
    "Pelipper's Circle Circuit Attraction -- Latias Friendship": PokeparkLocationData(
        168, PokeparkFlag.ATTRACTION, "Pelipper's Circle Circuit Attraction", PokeparkFriendshipClientLocationData(
            structure_position=158
        ),
    ),

    # Gyarados' Aqua Dash

    "Gyarados' Aqua Dash Attraction -- Prisma": PokeparkLocationData(
        169, PokeparkFlag.ATTRACTION_PRISMA, "Gyarados' Aqua Dash Attraction", PokeparkPrismaClientData(
            structure_position=5
        )
    ),

    "Gyarados' Aqua Dash Attraction -- Pikachu": PokeparkLocationData(
        170, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=12
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Psyduck": PokeparkLocationData(
        171, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=13
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Azurill": PokeparkLocationData(
        172, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=14
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Slowpoke": PokeparkLocationData(
        173, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=15
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Empoleon": PokeparkLocationData(
        174, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=1
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Floatzel": PokeparkLocationData(
        175, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=2
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Feraligatr": PokeparkLocationData(
        176, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=3
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Golduck": PokeparkLocationData(
        177, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=4
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Vaporeon": PokeparkLocationData(
        178, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=5
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Prinplup": PokeparkLocationData(
        179, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=6
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Bibarel": PokeparkLocationData(
        180, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=7
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Buizel": PokeparkLocationData(
        181, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=9
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Corsola": PokeparkLocationData(
        182, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=8
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Piplup": PokeparkLocationData(
        183, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=10
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Lotad": PokeparkLocationData(
        184, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=11
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Manaphy": PokeparkLocationData(
        185, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction",
        PokeparkGyaradosAttractionClientData(
            structure_position=0
        )
    ),
    "Gyarados' Aqua Dash Attraction -- Manaphy Friendship": PokeparkLocationData(
        186, PokeparkFlag.ATTRACTION, "Gyarados' Aqua Dash Attraction", PokeparkFriendshipClientLocationData(
            structure_position=157
        ),
    ),

    # Ice Zone

    "Ice Zone Main Area - Lapras -- Friendship": PokeparkLocationData(
        187, PokeparkFlag.FRIENDSHIP, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=61
        ),
    ),
    "Ice Zone Main Area - Spheal Power Competition -- Friendship": PokeparkLocationData(
        188, PokeparkFlag.CHASE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=68
        ),
    ),
    "Ice Zone Main Area - Octillery Power Competition -- Friendship": PokeparkLocationData(
        189, PokeparkFlag.BATTLE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=73
        ),
    ),
    "Ice Zone Main Area - Delibird -- Friendship": PokeparkLocationData(
        190, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=72
        ),
    ),
    "Ice Zone Main Area - Smoochum Power Competition -- Friendship": PokeparkLocationData(
        191, PokeparkFlag.BATTLE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=69
        ),
    ),
    "Ice Zone Main Area - Squirtle Power Competition -- Friendship": PokeparkLocationData(
        192, PokeparkFlag.BATTLE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=57
        ),
    ),
    "Ice Zone Main Area - Glaceon Power Competition -- Friendship": PokeparkLocationData(
        193, PokeparkFlag.CHASE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=40
        ),
    ),
    "Ice Zone Main Area - Prinplup Power Competition -- Friendship": PokeparkLocationData(
        194, PokeparkFlag.BATTLE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=79
        ),
    ),
    "Ice Zone Main Area - Sneasel Power Competition -- Friendship": PokeparkLocationData(
        195, PokeparkFlag.CHASE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=70
        ),
    ),
    "Ice Zone Main Area - Piloswine Power Competition -- Friendship": PokeparkLocationData(
        196, PokeparkFlag.BATTLE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=76
        ),
    ),
    "Ice Zone Main Area - Glalie -- Friendship": PokeparkLocationData(
        197, PokeparkFlag.BATTLE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=74
        ),
    ),
    "Ice Zone Main Area - Primeape Power Competition -- Friendship": PokeparkLocationData(
        198, PokeparkFlag.BATTLE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=17
        ),
    ),
    "Ice Zone Main Area - Ursaring Power Competition -- Friendship": PokeparkLocationData(
        199, PokeparkFlag.BATTLE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=67
        ),
    ),
    "Ice Zone Main Area - Mamoswine Power Competition -- Friendship": PokeparkLocationData(
        200, PokeparkFlag.BATTLE, "Ice Zone Frozen Lake Area", PokeparkFriendshipClientLocationData(
            structure_position=77
        ),
    ),
    "Ice Zone Main Area - Kirlia -- Friendship": PokeparkLocationData(
        201, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=153
        ),
    ),
    "Ice Zone Main Area - Igloo Housing -- Stage 1": PokeparkLocationData(
        202, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Ice Zone Main Area - Igloo Housing -- Stage 1 -- Primeape Unlocked": PokeparkLocationData(
        203, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Ice Zone Main Area - Igloo Housing -- Stage 2": PokeparkLocationData(
        204, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00000100,
            _bit_mask=0b00000100
        )
    ),
    "Ice Zone Main Area - Igloo Housing -- Stage 2 -- Ursaring Unlocked": PokeparkLocationData(
        205, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00000100,
            _bit_mask=0b00000100
        )
    ),
    "Ice Zone Main Area - Igloo Housing -- Stage 3": PokeparkLocationData(
        206, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkBottleIgloHousingClientData(

            _expected_value=0b00000110,
            _bit_mask=0b00000110
        )
    ),
    "Ice Zone Main Area - Christmas Tree Present -- Stage 1": PokeparkLocationData(
        207, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkChristmasTreeClientData(

            _expected_value=0b00010110,
            _bit_mask=0b00010110
        )
    ),
    "Ice Zone Main Area - Christmas Tree Present -- Stage 2": PokeparkLocationData(
        208, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkChristmasTreeClientData(

            _expected_value=0b00100111,
            _bit_mask=0b00100111
        )
    ),
    "Ice Zone Main Area - Christmas Tree Present -- Stage 3": PokeparkLocationData(
        209, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkChristmasTreeClientData(

            _expected_value=0b00110111,
            _bit_mask=0b00110111
        )
    ),
    "Ice Zone Main Area - Christmas Tree Present -- Stage 4": PokeparkLocationData(
        210, PokeparkFlag.ERRAND, "Ice Zone Main Area", PokeparkChristmasTreeClientData(

            _expected_value=0b01001111,
            _bit_mask=0b01001111
        )
    ),
    "Ice Zone Frozen Lake Area - Frozen Mamoswine -- Ice Rescue": PokeparkLocationData(
        211, PokeparkFlag.POKEMON_UNLOCK, "Ice Zone Frozen Lake Area",
        PokeparkMewChallengeGengarPaintingClientData(

            _expected_value=0b00100000,
            _bit_mask=0b00100000
        )
    ),

    # lower lift region
    "Ice Zone Lower Lift Area - Quagsire -- Friendship": PokeparkLocationData(
        212, PokeparkFlag.ERRAND, "Ice Zone Lower Lift Area", PokeparkFriendshipClientLocationData(
            structure_position=71
        ),
    ),

    "Ice Zone Main Area - Starly Power Competition -- Friendship": PokeparkLocationData(
        213, PokeparkFlag.CHASE, "Ice Zone Main Area", Pokepark07AttractionClientData(
            structure_position=1
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Krabby Power Competition -- Friendship": PokeparkLocationData(
        214, PokeparkFlag.BATTLE, "Ice Zone Main Area", Pokepark07AttractionClientData(
            structure_position=2
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Corphish Power Competition -- Friendship": PokeparkLocationData(
        215, PokeparkFlag.BATTLE, "Ice Zone Lower Lift Area", Pokepark07AttractionClientData(
            structure_position=3
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Mudkip Power Competition -- Friendship": PokeparkLocationData(
        216, PokeparkFlag.HIDEANDSEEK, "Ice Zone Main Area", Pokepark07AttractionClientData(
            structure_position=4
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Taillow Power Competition -- Friendship": PokeparkLocationData(
        217, PokeparkFlag.CHASE, "Ice Zone Main Area", Pokepark07AttractionClientData(
            structure_position=5
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Staravia Power Competition -- Friendship": PokeparkLocationData(
        218, PokeparkFlag.CHASE, "Ice Zone Main Area", Pokepark07AttractionClientData(
            structure_position=6
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Main Area - Teddiursa Power Competition -- Friendship": PokeparkLocationData(
        219, PokeparkFlag.CHASE, "Ice Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=66
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Lower Lift Area - Wingull Power Competition -- Friendship": PokeparkLocationData(
        220, PokeparkFlag.CHASE, "Ice Zone Lower Lift Area", Pokepark07AttractionClientData(
            structure_position=7
        ), each_zone=MultiZoneFlag.MULTI
    ),
    "Ice Zone Lower Lift Area - Froslass Power Competition -- Friendship": PokeparkLocationData(
        221, PokeparkFlag.BATTLE, "Ice Zone Lower Lift Area", PokeparkFriendshipClientLocationData(
            structure_position=75
        )
    ),

    "Ice Zone Empoleon Area - Empoleon -- Friendship": PokeparkLocationData(
        222, PokeparkFlag.FRIENDSHIP, "Ice Zone Empoleon Area", PokeparkFriendshipClientLocationData(
            structure_position=80
        )
    ),
    # Empoleon's Snow Slide

    "Empoleon's Snow Slide Attraction -- Prisma": PokeparkLocationData(
        223, PokeparkFlag.ATTRACTION_PRISMA, "Empoleon's Snow Slide Attraction", PokeparkPrismaClientData(
            structure_position=8
        )
    ),

    "Empoleon's Snow Slide Attraction -- Pikachu": PokeparkLocationData(
        224, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=13
        )
    ),
    "Empoleon's Snow Slide Attraction -- Teddiursa": PokeparkLocationData(
        225, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=14
        )
    ),
    "Empoleon's Snow Slide Attraction -- Magikarp": PokeparkLocationData(
        226, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=15
        )
    ),
    "Empoleon's Snow Slide Attraction -- Empoleon": PokeparkLocationData(
        227, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=1
        )
    ),
    "Empoleon's Snow Slide Attraction -- Glaceon": PokeparkLocationData(
        228, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=2
        )
    ),
    "Empoleon's Snow Slide Attraction -- Blastoise": PokeparkLocationData(
        229, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=3
        )
    ),
    "Empoleon's Snow Slide Attraction -- Glalie": PokeparkLocationData(
        230, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=4
        )
    ),
    "Empoleon's Snow Slide Attraction -- Lapras": PokeparkLocationData(
        231, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=5
        )
    ),
    "Empoleon's Snow Slide Attraction -- Delibird": PokeparkLocationData(
        232, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=7
        )
    ),
    "Empoleon's Snow Slide Attraction -- Piloswine": PokeparkLocationData(
        233, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=12
        )
    ),
    "Empoleon's Snow Slide Attraction -- Prinplup": PokeparkLocationData(
        234, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=6
        )
    ),
    "Empoleon's Snow Slide Attraction -- Squirtle": PokeparkLocationData(
        235, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=9
        )
    ),
    "Empoleon's Snow Slide Attraction -- Piplup": PokeparkLocationData(
        236, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=10
        )
    ),
    "Empoleon's Snow Slide Attraction -- Quagsire": PokeparkLocationData(
        237, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=8
        )
    ),
    "Empoleon's Snow Slide Attraction -- Spheal": PokeparkLocationData(
        238, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=11
        )
    ),
    "Empoleon's Snow Slide Attraction -- Suicune": PokeparkLocationData(
        239, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction",
        PokeparkEmpoleonAttractionClientData(
            structure_position=0
        )
    ),
    "Empoleon's Snow Slide Attraction -- Suicune Friendship": PokeparkLocationData(
        240, PokeparkFlag.ATTRACTION, "Empoleon's Snow Slide Attraction", PokeparkFriendshipClientLocationData(
            structure_position=159
        ),
    ),

    # Cavern Zone

    "Cavern Zone Main Area - Magnemite -- Friendship": PokeparkLocationData(
        241, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=105
        ),
    ),
    "Cavern Zone Main Area - Machamp Power Competition -- Friendship": PokeparkLocationData(
        242, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=89
        ),
    ),
    "Cavern Zone Main Area - Machamp Power Competition -- Machamp Unlocked": PokeparkLocationData(
        243, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=89
        ),
    ),
    "Cavern Zone Main Area - Cranidos Power Competition -- Friendship": PokeparkLocationData(
        244, PokeparkFlag.BATTLE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=87
        ),
    ),
    "Cavern Zone Main Area - Zubat Power Competition -- Friendship": PokeparkLocationData(
        245, PokeparkFlag.CHASE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=84
        ),
    ),
    "Cavern Zone Main Area - Golbat Power Competition -- Friendship": PokeparkLocationData(
        246, PokeparkFlag.CHASE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=85
        ),
    ),
    "Cavern Zone Main Area - Magnezone Power Competition -- Friendship": PokeparkLocationData(
        247, PokeparkFlag.BATTLE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=106
        ),
    ),
    "Cavern Zone Main Area - Scizor Power Competition -- Friendship": PokeparkLocationData(
        248, PokeparkFlag.BATTLE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=33
        ),
    ),
    "Cavern Zone Main Area - Dugtrio Power Competition -- Friendship": PokeparkLocationData(
        249, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=174
        ),
    ),
    "Cavern Zone Main Area - Gible Power Competition -- Friendship": PokeparkLocationData(
        250, PokeparkFlag.BATTLE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=82
        ),
    ),
    "Cavern Zone Main Area - Phanpy Power Competition -- Friendship": PokeparkLocationData(
        251, PokeparkFlag.ERRAND, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=86
        ),
    ),
    "Cavern Zone Main Area - Hitmonlee Power Competition -- Friendship": PokeparkLocationData(
        252, PokeparkFlag.BATTLE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=107
        ),
    ),
    "Cavern Zone Main Area - Electivire Power Competition -- Friendship": PokeparkLocationData(
        253, PokeparkFlag.BATTLE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=94
        ),
    ),
    "Cavern Zone Main Area - Magnemite Crate Entrance -- Magnemite Unlocked": PokeparkLocationData(
        254, PokeparkFlag.POKEMON_UNLOCK, "Cavern Zone Main Area", PokeparkMagnemite1CrateFlagClientData(
            _expected_value=0b00001000,
            _bit_mask=0b00001000
        )
    ),
    "Cavern Zone Main Area - Magnemite Crate Magma Zone Entrance -- Magnemite Unlocked": PokeparkLocationData(
        255, PokeparkFlag.POKEMON_UNLOCK, "Cavern Zone Main Area",
        PokeparkRhyperiorErrandMagnemite2CrateFlagClientData(
            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Cavern Zone Main Area - Magnemite Crate Deep Inside -- Magnemite Unlocked": PokeparkLocationData(
        256, PokeparkFlag.POKEMON_UNLOCK, "Cavern Zone Main Area",
        PokeparkShroomishCrateMagnemite3CrateDiglettCrateBaltoyCrateClientData(

            _expected_value=0b00100000,
            _bit_mask=0b00100000
        )
    ),
    "Cavern Zone Main Area - Diglett Crate -- Diglett Unlocked": PokeparkLocationData(
        257, PokeparkFlag.POKEMON_UNLOCK, "Cavern Zone Main Area",
        PokeparkShroomishCrateMagnemite3CrateDiglettCrateBaltoyCrateClientData(

            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Cavern Zone Main Area - Bonsly Power Competition -- Friendship": PokeparkLocationData(
        258, PokeparkFlag.HIDEANDSEEK, "Cavern Zone Main Area", Pokepark07AttractionClientData(
            structure_position=8
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Bonsly Power Competition -- Sudowoodo Unlocked": PokeparkLocationData(
        259, PokeparkFlag.HIDEANDSEEK, "Cavern Zone Main Area", Pokepark07AttractionClientData(
            structure_position=8
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Teddiursa Power Competition -- Friendship": PokeparkLocationData(
        260, PokeparkFlag.QUIZ, "Cavern Zone Main Area", Pokepark07AttractionClientData(
            structure_position=9
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Chimchar Power Competition -- Friendship": PokeparkLocationData(
        261, PokeparkFlag.BATTLE, "Cavern Zone Main Area", Pokepark07AttractionClientData(
            structure_position=10
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Sudowoodo Power Competition -- Friendship": PokeparkLocationData(
        262, PokeparkFlag.HIDEANDSEEK, "Cavern Zone Main Area", Pokepark07AttractionClientData(
            structure_position=11
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Aron Power Competition -- Friendship": PokeparkLocationData(
        263, PokeparkFlag.ERRAND, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=171
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Torchic Power Competition -- Friendship": PokeparkLocationData(
        264, PokeparkFlag.BATTLE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=115
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Geodude Power Competition -- Friendship": PokeparkLocationData(
        265, PokeparkFlag.HIDEANDSEEK, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=81
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Raichu Power Competition -- Friendship": PokeparkLocationData(
        266, PokeparkFlag.CHASE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=91
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Meowth Power Competition -- Friendship": PokeparkLocationData(
        267, PokeparkFlag.QUIZ, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=117
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Marowak Power Competition -- Friendship": PokeparkLocationData(
        268, PokeparkFlag.BATTLE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=88
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Cavern Zone Main Area - Diglett Power Competition -- Friendship": PokeparkLocationData(
        269, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=172
        ),
    ),
    "Cavern Zone Main Area - Mawile Power Competition -- Friendship": PokeparkLocationData(
        270, PokeparkFlag.CHASE, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=83
        )
    ),
    "Cavern Zone Main Area - Bastiodon -- Friendship": PokeparkLocationData(
        271, PokeparkFlag.FRIENDSHIP, "Cavern Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=97
        )
    ),
    # Bastiodon's Panel Crush

    "Bastiodon's Panel Crush Attraction -- Prisma": PokeparkLocationData(
        272, PokeparkFlag.ATTRACTION_PRISMA, "Bastiodon's Panel Crush Attraction", PokeparkPrismaClientData(
            structure_position=9
        )
    ),

    "Bastiodon's Panel Crush Attraction -- Pikachu": PokeparkLocationData(
        273, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=12
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Sableye": PokeparkLocationData(
        274, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=6
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Meowth": PokeparkLocationData(
        275, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=14
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Torchic": PokeparkLocationData(
        276, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=13
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Electivire": PokeparkLocationData(
        277, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=2
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Magmortar": PokeparkLocationData(
        278, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=3
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Hitmonlee": PokeparkLocationData(
        279, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=1
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Ursaring": PokeparkLocationData(
        280, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=5
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Mr. Mime": PokeparkLocationData(
        281, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=7
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Raichu": PokeparkLocationData(
        282, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=4
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Sudowoodo": PokeparkLocationData(
        283, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=8
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Charmander": PokeparkLocationData(
        284, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=9
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Gible": PokeparkLocationData(
        285, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=10
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Chimchar": PokeparkLocationData(
        286, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=11
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Magby": PokeparkLocationData(
        287, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=15
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Metagross": PokeparkLocationData(
        288, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkBastiodonAttractionClientData(
            structure_position=0
        )
    ),
    "Bastiodon's Panel Crush Attraction -- Metagross Friendship": PokeparkLocationData(
        289, PokeparkFlag.ATTRACTION, "Bastiodon's Panel Crush Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=160
        ),
    ),

    # Magma Zone

    "Magma Zone Main Area - Camerupt Power Competition -- Friendship": PokeparkLocationData(
        290, PokeparkFlag.BATTLE, "Magma Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=101
        ),
    ),
    "Magma Zone Main Area - Magby Power Competition -- Friendship": PokeparkLocationData(
        291, PokeparkFlag.CHASE, "Magma Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=110
        ),
    ),
    "Magma Zone Main Area - Vulpix Power Competition -- Friendship": PokeparkLocationData(
        292, PokeparkFlag.CHASE, "Magma Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=119
        ),
    ),
    "Magma Zone Main Area - Vulpix Power Competition -- Ninetales Unlocked": PokeparkLocationData(
        293, PokeparkFlag.CHASE, "Magma Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=119
        ),
    ),
    "Magma Zone Circle Area - Ninetales Power Competition -- Friendship": PokeparkLocationData(
        294, PokeparkFlag.CHASE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=120
        ),
    ),
    "Magma Zone Circle Area - Quilava Power Competition -- Friendship": PokeparkLocationData(
        295, PokeparkFlag.BATTLE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=100
        ),
    ),
    "Magma Zone Circle Area - Flareon Power Competition -- Friendship": PokeparkLocationData(
        296, PokeparkFlag.BATTLE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=41
        ),
    ),
    "Magma Zone Circle Area - Infernape Power Competition -- Friendship": PokeparkLocationData(
        297, PokeparkFlag.BATTLE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=113
        ),
    ),
    "Magma Zone Circle Area - Farfetch'd Power Competition -- Friendship": PokeparkLocationData(
        298, PokeparkFlag.BATTLE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=102
        ),
    ),
    "Magma Zone Circle Area - Ponyta Power Competition -- Friendship": PokeparkLocationData(
        299, PokeparkFlag.CHASE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=29
        ),
    ),
    "Magma Zone Main Area - Torkoal Power Competition -- Friendship": PokeparkLocationData(
        300, PokeparkFlag.BATTLE, "Magma Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=98
        ),
    ),
    "Magma Zone Main Area - Golem Power Competition -- Friendship": PokeparkLocationData(
        301, PokeparkFlag.FRIENDSHIP, "Magma Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=177
        ),
    ),
    "Magma Zone Circle Area - Hitmonchan Power Competition -- Friendship": PokeparkLocationData(
        302, PokeparkFlag.BATTLE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=108
        ),
    ),
    "Magma Zone Circle Area - Hitmonchan Power Competition -- Hitmonlee Unlocked": PokeparkLocationData(
        303, PokeparkFlag.BATTLE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=108
        ),
    ),
    "Magma Zone Main Area - Hitmontop Power Competition -- Friendship": PokeparkLocationData(
        304, PokeparkFlag.ERRAND, "Magma Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=109
        ),
    ),
    "Magma Zone Circle Area - Magmortar Power Competition -- Friendship": PokeparkLocationData(
        305, PokeparkFlag.BATTLE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=111
        ),
    ),

    "Magma Zone Blaziken Area - Blaziken -- Friendship": PokeparkLocationData(
        306, PokeparkFlag.FRIENDSHIP, "Magma Zone Blaziken Area", PokeparkFriendshipClientLocationData(
            structure_position=116
        ),
    ),
    "Magma Zone Circle Area - Rhyperior Iron Disc -- Errand": PokeparkLocationData(
        307, PokeparkFlag.ERRAND, "Magma Zone Circle Area",
        PokeparkRhyperiorErrandMagnemite2CrateFlagClientData(

            _expected_value=0b10000000,
            _bit_mask=0b10000000
        )
    ),
    "Magma Zone Circle Area - Rhyperior -- Friendship": PokeparkLocationData(
        308, PokeparkFlag.ERRAND, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=114
        ),
    ),
    "Magma Zone Main Area - Baltoy Crate -- Baltoy Unlocked": PokeparkLocationData(
        309, PokeparkFlag.POKEMON_UNLOCK, "Magma Zone Main Area",
        PokeparkShroomishCrateMagnemite3CrateDiglettCrateBaltoyCrateClientData(

            _expected_value=0b00000001,
            _bit_mask=0b00000001
        )
    ),
    "Magma Zone Main Area - Bonsly Power Competition -- Friendship": PokeparkLocationData(
        310, PokeparkFlag.HIDEANDSEEK, "Magma Zone Main Area", Pokepark07AttractionClientData(
            structure_position=12
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Chimchar Power Competition -- Friendship": PokeparkLocationData(
        311, PokeparkFlag.BATTLE, "Magma Zone Main Area", Pokepark07AttractionClientData(
            structure_position=13
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Chimchar Power Competition -- Infernape Unlocked": PokeparkLocationData(
        312, PokeparkFlag.BATTLE, "Magma Zone Main Area", Pokepark07AttractionClientData(
            structure_position=13
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Aron Power Competition -- Friendship": PokeparkLocationData(
        313, PokeparkFlag.ERRAND, "Magma Zone Main Area", Pokepark07AttractionClientData(
            structure_position=14
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Torchic Power Competition -- Friendship": PokeparkLocationData(
        314, PokeparkFlag.BATTLE, "Magma Zone Main Area", Pokepark07AttractionClientData(
            structure_position=15
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Geodude Power Competition -- Friendship": PokeparkLocationData(
        315, PokeparkFlag.HIDEANDSEEK, "Magma Zone Main Area", Pokepark07AttractionClientData(
            structure_position=16
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Baltoy Power Competition -- Friendship": PokeparkLocationData(
        316, PokeparkFlag.BATTLE, "Magma Zone Main Area", Pokepark07AttractionClientData(
            structure_position=17
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Baltoy Power Competition -- Claydol Unlocked": PokeparkLocationData(
        317, PokeparkFlag.BATTLE, "Magma Zone Main Area", Pokepark07AttractionClientData(
            structure_position=17
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Circle Area - Meditite Power Competition -- Friendship": PokeparkLocationData(
        318, PokeparkFlag.QUIZ, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=139
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Magma Zone Main Area - Drill -- Torkoal Unlocked": PokeparkLocationData(
        319, PokeparkFlag.POKEMON_UNLOCK, "Magma Zone Main Area",
        PokeparkShroomishCrateMagnemite3CrateDiglettCrateBaltoyCrateClientData(

            _expected_value=0b00010000,
            _bit_mask=0b00010000
        )
    ),
    "Magma Zone Main Area - Furnace -- Golem Unlocked": PokeparkLocationData(
        320, PokeparkFlag.POKEMON_UNLOCK, "Magma Zone Main Area",
        PokeparkGolemUnlockFlagClientData(

            _expected_value=0b00010000,
            _bit_mask=0b00010000
        )
    ),
    "Magma Zone Circle Area - Charmander Power Competition -- Friendship": PokeparkLocationData(
        321, PokeparkFlag.BATTLE, "Magma Zone Circle Area", PokeparkFriendshipClientLocationData(
            structure_position=145
        ),
    ),
    "Magma Zone Main Area - Claydol Power Competition -- Friendship": PokeparkLocationData(
        322, PokeparkFlag.BATTLE, "Magma Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=104
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    # Rhyperior's Bumper Burn

    "Rhyperior's Bumper Burn Attraction -- Prisma": PokeparkLocationData(
        323, PokeparkFlag.ATTRACTION_PRISMA, "Rhyperior's Bumper Burn Attraction", PokeparkPrismaClientData(
            structure_position=10
        )
    ),

    "Rhyperior's Bumper Burn Attraction -- Pikachu": PokeparkLocationData(
        324, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=14
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Magnemite": PokeparkLocationData(
        325, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=15
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Rhyperior": PokeparkLocationData(
        326, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=1
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Tyranitar": PokeparkLocationData(
        327, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=2
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Hitmontop": PokeparkLocationData(
        328, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=3
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Flareon": PokeparkLocationData(
        329, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=4
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Venusaur": PokeparkLocationData(
        330, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=5
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Snorlax": PokeparkLocationData(
        331, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=6
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Torterra": PokeparkLocationData(
        332, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=7
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Magnezone": PokeparkLocationData(
        333, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=8
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Claydol": PokeparkLocationData(
        334, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=9
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Quilava": PokeparkLocationData(
        335, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=10
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Torkoal": PokeparkLocationData(
        336, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=11
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Baltoy": PokeparkLocationData(
        337, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=12
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Bonsly": PokeparkLocationData(
        338, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=13
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Heatran": PokeparkLocationData(
        339, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkRhyperiorAttractionClientData(
            structure_position=0
        )
    ),
    "Rhyperior's Bumper Burn Attraction -- Heatran Friendship": PokeparkLocationData(
        340, PokeparkFlag.ATTRACTION, "Rhyperior's Bumper Burn Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=161
        ),
    ),

    # Blaziken's Boulder Bash

    "Blaziken's Boulder Bash Attraction -- Prisma": PokeparkLocationData(
        341, PokeparkFlag.ATTRACTION_PRISMA, "Blaziken's Boulder Bash Attraction", PokeparkPrismaClientData(
            structure_position=11
        )
    ),

    "Blaziken's Boulder Bash Attraction -- Pikachu": PokeparkLocationData(
        342, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=13
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Geodude": PokeparkLocationData(
        343, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=14
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Phanpy": PokeparkLocationData(
        344, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=15
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Blaziken": PokeparkLocationData(
        345, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=1
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Garchomp": PokeparkLocationData(
        346, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=2
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Scizor": PokeparkLocationData(
        347, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=3
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Magmortar": PokeparkLocationData(
        348, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=4
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Hitmonchan": PokeparkLocationData(
        349, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=5
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Machamp": PokeparkLocationData(
        350, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=6
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Marowak": PokeparkLocationData(
        351, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=8
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Farfetch'd": PokeparkLocationData(
        352, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=12
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Cranidos": PokeparkLocationData(
        353, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=9
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Camerupt": PokeparkLocationData(
        354, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=10
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Bastiodon": PokeparkLocationData(
        355, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=7
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Mawile": PokeparkLocationData(
        356, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=11
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Groudon": PokeparkLocationData(
        357, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkBlazikenAttractionClientData(
            structure_position=0
        )
    ),
    "Blaziken's Boulder Bash Attraction -- Groudon Friendship": PokeparkLocationData(
        358, PokeparkFlag.ATTRACTION, "Blaziken's Boulder Bash Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=162
        ),
    ),

    # Haunted Zone

    "Haunted Zone Main Area - Murkrow Power Competition -- Friendship": PokeparkLocationData(
        359, PokeparkFlag.CHASE, "Haunted Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=121
        ),
    ),
    "Haunted Zone Main Area - Murkrow Power Competition -- Honchkrow Unlocked": PokeparkLocationData(
        360, PokeparkFlag.CHASE, "Haunted Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=121
        ),
    ),
    "Haunted Zone Main Area - Honchkrow Power Competition -- Friendship": PokeparkLocationData(
        361, PokeparkFlag.BATTLE, "Haunted Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=122
        ),
    ),
    "Haunted Zone Main Area - Gliscor Power Competition -- Friendship": PokeparkLocationData(
        362, PokeparkFlag.BATTLE, "Haunted Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=118
        ),
    ),
    "Haunted Zone Main Area - Metapod Power Competition -- Friendship": PokeparkLocationData(
        363, PokeparkFlag.FRIENDSHIP, "Haunted Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=188
        ),
    ),
    "Haunted Zone Main Area - Kakuna Power Competition -- Friendship": PokeparkLocationData(
        364, PokeparkFlag.FRIENDSHIP, "Haunted Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=170
        ),
    ),
    "Haunted Zone Main Area - Metapod Left Tree -- Metapod Unlocked": PokeparkLocationData(
        365, PokeparkFlag.POKEMON_UNLOCK, "Haunted Zone Main Area",
        PokeparkIronTailUpgradeMetapodTreeClientLocationData(

            _expected_value=0b00000001,
            _bit_mask=0b00000001,
        )
    ),
    "Haunted Zone Main Area - Kakuna Right Tree -- Metapod Unlocked": PokeparkLocationData(
        366, PokeparkFlag.POKEMON_UNLOCK, "Haunted Zone Main Area", PokeparkKakunaTreeVoltorbVaseClientData(

            _expected_value=0b01000000,
            _bit_mask=0b01000000
        )
    ),

    "Haunted Zone Main Area - Raichu Power Competition -- Friendship": PokeparkLocationData(
        367, PokeparkFlag.CHASE, "Haunted Zone Main Area", Pokepark07AttractionClientData(
            structure_position=18
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Meowth Power Competition -- Friendship": PokeparkLocationData(
        368, PokeparkFlag.QUIZ, "Haunted Zone Main Area", Pokepark07AttractionClientData(
            structure_position=19
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Aipom Power Competition -- Friendship": PokeparkLocationData(
        369, PokeparkFlag.CHASE, "Haunted Zone Main Area", Pokepark07AttractionClientData(
            structure_position=20
        ),
        each_zone=MultiZoneFlag.MULTI
    ),

    "Haunted Zone Main Area - Aipom Power Competition -- Ambipom Unlocked": PokeparkLocationData(
        370, PokeparkFlag.CHASE, "Haunted Zone Main Area", Pokepark07AttractionClientData(
            structure_position=20
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Ambipom Power Competition -- Friendship": PokeparkLocationData(
        371, PokeparkFlag.BATTLE, "Haunted Zone Main Area", Pokepark07AttractionClientData(
            structure_position=21
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Drifloon Power Competition -- Friendship": PokeparkLocationData(
        372, PokeparkFlag.FRIENDSHIP, "Drifloon", PokeparkFriendshipClientLocationData(
            structure_position=175
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Haunted Zone Main Area - Tangrowth -- Friendship": PokeparkLocationData(
        373, PokeparkFlag.FRIENDSHIP, "Haunted Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=123
        ),
    ),

    # Tangrowth's Swing-Along

    "Tangrowth's Swing-Along Attraction -- Prisma": PokeparkLocationData(
        374, PokeparkFlag.ATTRACTION_PRISMA, "Tangrowth's Swing-Along Attraction", PokeparkPrismaClientData(
            structure_position=3
        )
    ),

    "Tangrowth's Swing-Along Attraction -- Pikachu": PokeparkLocationData(
        375, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=0
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Meowth": PokeparkLocationData(
        376, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=14
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Pichu": PokeparkLocationData(
        377, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=15
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Lucario": PokeparkLocationData(
        378, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=2
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Infernape": PokeparkLocationData(
        379, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=3
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Blaziken": PokeparkLocationData(
        380, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=4
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Riolu": PokeparkLocationData(
        381, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=5
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Sneasel": PokeparkLocationData(
        382, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=6
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Raichu": PokeparkLocationData(
        383, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=8
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Ambipom": PokeparkLocationData(
        384, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=9
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Primeape": PokeparkLocationData(
        385, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=10
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Aipom": PokeparkLocationData(
        386, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=11
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Electabuzz": PokeparkLocationData(
        387, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=7
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Chimchar": PokeparkLocationData(
        388, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=12
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Croagunk": PokeparkLocationData(
        389, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=13
        )
    ),
    "Tangrowth's Swing-Along Attraction -- Celebi": PokeparkLocationData(
        390, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkTangrowthAttractionClientData(
            structure_position=1
        )
    ),

    "Tangrowth's Swing-Along Attraction -- Celebi Friendship": PokeparkLocationData(
        391, PokeparkFlag.ATTRACTION, "Tangrowth's Swing-Along Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=163
        ),
    ),

    # Haunted Zone Mansion

    "Haunted Zone Mansion Area - Duskull Power Competition -- Friendship": PokeparkLocationData(
        392, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=134
        ),
    ),
    "Haunted Zone Mansion Area - Misdreavus Power Competition -- Friendship": PokeparkLocationData(
        393, PokeparkFlag.CHASE, "Haunted Zone Mansion Ballroom Area",
        PokeparkFriendshipClientLocationData(
            structure_position=128
        ),
    ),
    "Haunted Zone Mansion Area - Pichu Power Competition -- Friendship": PokeparkLocationData(
        394, PokeparkFlag.CHASE, "Haunted Zone Mansion Ballroom Area",
        PokeparkFriendshipClientLocationData(
            structure_position=90
        ),
    ),
    "Haunted Zone Mansion Area - Umbreon Power Competition -- Friendship": PokeparkLocationData(
        395, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=42
        ),
    ),
    "Haunted Zone Mansion Area - Umbreon Power Competition -- Espeon Unlocked": PokeparkLocationData(
        396, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=42
        ),
    ),
    "Haunted Zone Mansion Area - Espeon Power Competition -- Friendship": PokeparkLocationData(
        397, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=43
        ),
    ),
    "Haunted Zone Mansion Area - Spinarak Power Competition -- Friendship": PokeparkLocationData(
        398, PokeparkFlag.FRIENDSHIP, "Haunted Zone Mansion Antic Area", PokeparkFriendshipClientLocationData(
            structure_position=179
        ),
    ),
    "Haunted Zone Main Area - Riolu Power Competition -- Friendship": PokeparkLocationData(
        399, PokeparkFlag.BATTLE, "Riolu", PokeparkFriendshipClientLocationData(
            structure_position=151
        ),
    ),
    "Haunted Zone Mansion Area - Voltorb Power Competition -- Friendship": PokeparkLocationData(
        400, PokeparkFlag.BATTLE, "Haunted Zone Mansion Gengar Area", PokeparkFriendshipClientLocationData(
            structure_position=127
        ),
    ),
    "Haunted Zone Mansion Area - Elekid Power Competition -- Friendship": PokeparkLocationData(
        401, PokeparkFlag.HIDEANDSEEK, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=92
        ),
    ),
    "Haunted Zone Mansion Area - Elekid Power Competition -- Electabuzz Unlocked": PokeparkLocationData(
        402, PokeparkFlag.HIDEANDSEEK, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=92
        ),
    ),
    "Haunted Zone Mansion Area - Electabuzz Power Competition -- Friendship": PokeparkLocationData(
        403, PokeparkFlag.BATTLE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=93
        ),
    ),
    "Haunted Zone Mansion Area - Luxray Power Competition -- Friendship": PokeparkLocationData(
        404, PokeparkFlag.CHASE, "Haunted Zone Mansion Ballroom Area",
        PokeparkFriendshipClientLocationData(
            structure_position=28
        ),
    ),
    "Haunted Zone Mansion Area - Stunky Power Competition -- Friendship": PokeparkLocationData(
        405, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=125
        ),
    ),
    "Haunted Zone Mansion Area - Stunky Power Competition -- Skuntank Unlocked": PokeparkLocationData(
        406, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=125
        ),
    ),
    "Haunted Zone Mansion Area - Skuntank Power Competition -- Friendship": PokeparkLocationData(
        407, PokeparkFlag.BATTLE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=126
        ),
    ),
    "Haunted Zone Mansion Area - Breloom Power Competition -- Friendship": PokeparkLocationData(
        408, PokeparkFlag.BATTLE, "Haunted Zone Mansion Antic Area", PokeparkFriendshipClientLocationData(
            structure_position=15
        ),
    ),
    "Haunted Zone Mansion Area - Mismagius Power Competition -- Friendship": PokeparkLocationData(
        409, PokeparkFlag.BATTLE, "Haunted Zone Mansion Ballroom Area",
        PokeparkFriendshipClientLocationData(
            structure_position=129
        ),
    ),
    "Haunted Zone Mansion Area - Electrode Power Competition -- Friendship": PokeparkLocationData(
        410, PokeparkFlag.CHASE, "Haunted Zone Mansion Ballroom Area",
        PokeparkFriendshipClientLocationData(
            structure_position=182
        ),
    ),
    "Haunted Zone Mansion Area - Haunter Power Competition -- Friendship": PokeparkLocationData(
        411, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=131
        ),
    ),
    "Haunted Zone Mansion Area - Gastly Power Competition -- Friendship": PokeparkLocationData(
        412, PokeparkFlag.CHASE, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=130
        ),
    ),
    "Haunted Zone Mansion Area - Gengar Power Competition -- Friendship": PokeparkLocationData(
        413, PokeparkFlag.BATTLE, "Haunted Zone Mansion Gengar Area", PokeparkFriendshipClientLocationData(
            structure_position=132
        ),
    ),
    "Haunted Zone Mansion Area - Gengar Painting -- Gengar Unlocked": PokeparkLocationData(
        414, PokeparkFlag.POKEMON_UNLOCK, "Haunted Zone Mansion Gengar Area",
        PokeparkMewChallengeGengarPaintingClientData(

            _expected_value=0b00000001,
            _bit_mask=0b00000001
        )
    ),
    "Haunted Zone Mansion Area - Voltorb Vase -- Voltorb Unlocked": PokeparkLocationData(
        415, PokeparkFlag.POKEMON_UNLOCK, "Haunted Zone Mansion Gengar Area",
        PokeparkKakunaTreeVoltorbVaseClientData(

            _expected_value=0b00001000,
            _bit_mask=0b00001000
        )
    ),
    "Haunted Zone Mansion Area - Abra Power Competition -- Friendship": PokeparkLocationData(
        416, PokeparkFlag.FRIENDSHIP, "Haunted Zone Mansion Antic Area", Pokepark07AttractionClientData(
            structure_position=22
        ),
        each_zone=MultiZoneFlag.MULTI
    ),

    "Haunted Zone Mansion Area - Dusknoir -- Friendship": PokeparkLocationData(
        417, PokeparkFlag.FRIENDSHIP, "Haunted Zone Mansion Area", PokeparkFriendshipClientLocationData(
            structure_position=135
        ),
    ),

    # Dusknoir's Speed Slam

    "Dusknoir's Speed Slam Attraction -- Prisma": PokeparkLocationData(
        418, PokeparkFlag.ATTRACTION_PRISMA, "Dusknoir's Speed Slam Attraction", PokeparkPrismaClientData(
            structure_position=4
        )
    ),

    "Dusknoir's Speed Slam Attraction -- Pikachu": PokeparkLocationData(
        419, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=0
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Stunky": PokeparkLocationData(
        420, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=14
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Gengar": PokeparkLocationData(
        421, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=2
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Mismagius": PokeparkLocationData(
        422, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=4
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Scizor": PokeparkLocationData(
        423, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=5
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Espeon": PokeparkLocationData(
        424, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=3
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Dusknoir": PokeparkLocationData(
        425, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=6
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Umbreon": PokeparkLocationData(
        426, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=7
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Cranidos": PokeparkLocationData(
        427, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=10
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Skuntank": PokeparkLocationData(
        428, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=11
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Electrode": PokeparkLocationData(
        429, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=9
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Gastly": PokeparkLocationData(
        430, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=13
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Duskull": PokeparkLocationData(
        431, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=15
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Misdreavus": PokeparkLocationData(
        432, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=12
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Krabby": PokeparkLocationData(
        433, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=8
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Darkrai": PokeparkLocationData(
        434, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkDusknoirAttractionClientData(
            structure_position=1
        )
    ),
    "Dusknoir's Speed Slam Attraction -- Darkrai Friendship": PokeparkLocationData(
        435, PokeparkFlag.ATTRACTION, "Dusknoir's Speed Slam Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=164
        ),
    ),

    # Rotom's Spooky Shoot-'em-Up

    "Rotom's Spooky Shoot-'em-Up Attraction -- Prisma": PokeparkLocationData(
        436, PokeparkFlag.ATTRACTION_PRISMA, "Rotom's Spooky Shoot-'em-Up Attraction", PokeparkPrismaClientData(
            structure_position=12
        )
    ),

    "Rotom's Spooky Shoot-'em-Up Attraction -- Pikachu": PokeparkLocationData(
        437, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=14
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Magnemite": PokeparkLocationData(
        438, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=15
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Porygon-Z": PokeparkLocationData(
        439, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=1
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Magnezone": PokeparkLocationData(
        440, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=2
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Gengar": PokeparkLocationData(
        441, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=3
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Magmortar": PokeparkLocationData(
        442, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=4
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Electivire": PokeparkLocationData(
        443, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=5
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Mismagius": PokeparkLocationData(
        444, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=6
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Claydol": PokeparkLocationData(
        445, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=7
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Electabuzz": PokeparkLocationData(
        446, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=9
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Haunter": PokeparkLocationData(
        447, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=10
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Abra": PokeparkLocationData(
        448, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=11
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Elekid": PokeparkLocationData(
        449, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=12
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Mr. Mime": PokeparkLocationData(
        450, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=8
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Baltoy": PokeparkLocationData(
        451, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=13
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Rotom": PokeparkLocationData(
        452, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkRotomAttractionClientData(
            structure_position=0
        )
    ),
    "Rotom's Spooky Shoot-'em-Up Attraction -- Rotom Friendship": PokeparkLocationData(
        453, PokeparkFlag.ATTRACTION, "Rotom's Spooky Shoot-'em-Up Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=165
        ),
    ),

    # Granite Zone

    "Granite Zone Main Area - Lopunny Power Competition -- Friendship": PokeparkLocationData(
        454, PokeparkFlag.CHASE, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=19
        ),
    ),
    "Granite Zone Main Area - Eevee Power Competition -- Friendship": PokeparkLocationData(
        455, PokeparkFlag.CHASE, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=37
        ),
    ),
    "Granite Zone Main Area - Eevee Power Competition -- Jolteon Unlocked": PokeparkLocationData(
        456, PokeparkFlag.CHASE, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=37
        ),
    ),
    "Granite Zone Main Area - Charizard Power Competition -- Friendship": PokeparkLocationData(
        457, PokeparkFlag.BATTLE, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=146
        ),
    ),
    "Granite Zone Main Area - Flygon Power Competition -- Friendship": PokeparkLocationData(
        458, PokeparkFlag.CHASE, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=142
        ),
    ),
    "Granite Zone Main Area - Staraptor Power Competition -- Friendship": PokeparkLocationData(
        459, PokeparkFlag.BATTLE, "Granite Zone Salamence Area", PokeparkFriendshipClientLocationData(
            structure_position=22
        ),
    ),
    "Granite Zone Main Area - Staraptor Power Competition -- Aerodactyl Unlocked": PokeparkLocationData(
        460, PokeparkFlag.BATTLE, "Granite Zone Salamence Area", PokeparkFriendshipClientLocationData(
            structure_position=22
        ),
    ),
    "Granite Zone Main Area - Aerodactyl Power Competition -- Friendship": PokeparkLocationData(
        461, PokeparkFlag.BATTLE, "Granite Zone Salamence Area", PokeparkFriendshipClientLocationData(
            structure_position=141
        ),
    ),
    "Granite Zone Main Area - Arcanine Power Competition -- Friendship": PokeparkLocationData(
        462, PokeparkFlag.CHASE, "Granite Zone Salamence Area", PokeparkFriendshipClientLocationData(
            structure_position=144
        ),
    ),
    "Granite Zone Main Area - Jolteon Power Competition -- Friendship": PokeparkLocationData(
        463, PokeparkFlag.CHASE, "Granite Zone Salamence Area", PokeparkFriendshipClientLocationData(
            structure_position=44
        ),
    ),
    "Granite Zone Main Area - Skorupi Power Competition -- Friendship": PokeparkLocationData(
        464, PokeparkFlag.FRIENDSHIP, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=186
        ),
    ),
    "Granite Zone Main Area - Porygon-Z Power Competition -- Friendship": PokeparkLocationData(
        465, PokeparkFlag.QUIZ, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=147
        ),
    ),
    "Granite Zone Main Area - Tyranitar Power Competition -- Friendship": PokeparkLocationData(
        466, PokeparkFlag.BATTLE, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=149
        ),
    ),
    "Granite Zone Main Area - Garchomp Power Competition -- Friendship": PokeparkLocationData(
        467, PokeparkFlag.BATTLE, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=148
        ),
    ),
    "Granite Zone Main Area - Taillow Power Competition -- Friendship": PokeparkLocationData(
        468, PokeparkFlag.CHASE, "Granite Zone Salamence Area", Pokepark07AttractionClientData(
            structure_position=24
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Drifloon Power Competition -- Friendship": PokeparkLocationData(
        469, PokeparkFlag.FRIENDSHIP, "Granite Zone Main Area", Pokepark07AttractionClientData(
            structure_position=23
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Marowak Power Competition -- Friendship": PokeparkLocationData(
        470, PokeparkFlag.BATTLE, "Granite Zone Main Area", Pokepark07AttractionClientData(
            structure_position=25
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Baltoy Power Competition -- Friendship": PokeparkLocationData(
        471, PokeparkFlag.BATTLE, "Granite Zone Main Area", Pokepark13AttractionClientData(
            structure_position=0
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Baltoy Power Competition -- Claydol Unlocked": PokeparkLocationData(
        472, PokeparkFlag.BATTLE, "Granite Zone Main Area", Pokepark13AttractionClientData(
            structure_position=0
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Furret Power Competition -- Friendship": PokeparkLocationData(
        473, PokeparkFlag.HIDEANDSEEK, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=140
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Claydol Power Competition -- Friendship": PokeparkLocationData(
        474, PokeparkFlag.BATTLE, "Granite Zone Main Area", Pokepark13AttractionClientData(
            structure_position=4
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Granite Zone Main Area - Absol -- Friendship": PokeparkLocationData(
        475, PokeparkFlag.FRIENDSHIP, "Granite Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=154
        ),
    ),
    "Granite Zone Salamence Area - Salamence -- Friendship": PokeparkLocationData(
        476, PokeparkFlag.FRIENDSHIP, "Granite Zone Salamence Area", PokeparkFriendshipClientLocationData(
            structure_position=155
        ),
    ),
    # Absol Hurdle Dash

    "Absol's Hurdle Bounce Attraction -- Prisma": PokeparkLocationData(
        477, PokeparkFlag.ATTRACTION_PRISMA, "Absol's Hurdle Bounce Attraction", PokeparkPrismaClientData(
            structure_position=0
        )
    ),

    "Absol's Hurdle Bounce Attraction -- Pikachu": PokeparkLocationData(
        478, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=0
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Chikorita": PokeparkLocationData(
        479, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=15
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Absol": PokeparkLocationData(
        480, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=6
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Lucario": PokeparkLocationData(
        481, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=3
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Ponyta": PokeparkLocationData(
        482, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=7
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Ninetales": PokeparkLocationData(
        483, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=8
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Lopunny": PokeparkLocationData(
        484, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=2
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Espeon": PokeparkLocationData(
        485, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=5
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Infernape": PokeparkLocationData(
        486, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=4
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Breloom": PokeparkLocationData(
        487, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=9
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Riolu": PokeparkLocationData(
        488, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=10
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Furret": PokeparkLocationData(
        489, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=11
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Mareep": PokeparkLocationData(
        490, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=12
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Eevee": PokeparkLocationData(
        491, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=13
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Vulpix": PokeparkLocationData(
        492, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=14
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Shaymin": PokeparkLocationData(
        493, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkAbsolAttractionClientData(
            structure_position=1
        )
    ),
    "Absol's Hurdle Bounce Attraction -- Shaymin Friendship": PokeparkLocationData(
        494, PokeparkFlag.ATTRACTION, "Absol's Hurdle Bounce Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=156
        ),
    ),

    # Salamence's Sky Race

    "Salamence's Sky Race Attraction -- Prisma": PokeparkLocationData(
        495, PokeparkFlag.ATTRACTION_PRISMA, "Salamence's Sky Race Attraction", PokeparkPrismaClientData(
            structure_position=14
        )
    ),

    "Salamence's Sky Race Attraction -- Pikachu": PokeparkLocationData(
        496, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=15
        )
    ),
    "Salamence's Sky Race Attraction -- Salamence": PokeparkLocationData(
        497, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=1
        )
    ),
    "Salamence's Sky Race Attraction -- Charizard": PokeparkLocationData(
        498, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=2
        )
    ),
    "Salamence's Sky Race Attraction -- Dragonite": PokeparkLocationData(
        499, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=3
        )
    ),
    "Salamence's Sky Race Attraction -- Flygon": PokeparkLocationData(
        500, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=4
        )
    ),
    "Salamence's Sky Race Attraction -- Aerodactyl": PokeparkLocationData(
        501, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=5
        )
    ),
    "Salamence's Sky Race Attraction -- Staraptor": PokeparkLocationData(
        502, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=7
        )
    ),
    "Salamence's Sky Race Attraction -- Honchkrow": PokeparkLocationData(
        503, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=8
        )
    ),
    "Salamence's Sky Race Attraction -- Gliscor": PokeparkLocationData(
        504, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=9
        )
    ),
    "Salamence's Sky Race Attraction -- Pidgeotto": PokeparkLocationData(
        505, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=10
        )
    ),
    "Salamence's Sky Race Attraction -- Togekiss": PokeparkLocationData(
        506, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=6
        )
    ),
    "Salamence's Sky Race Attraction -- Golbat": PokeparkLocationData(
        507, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=13
        )
    ),
    "Salamence's Sky Race Attraction -- Taillow": PokeparkLocationData(
        508, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=11
        )
    ),
    "Salamence's Sky Race Attraction -- Murkrow": PokeparkLocationData(
        509, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=12
        )
    ),
    "Salamence's Sky Race Attraction -- Zubat": PokeparkLocationData(
        510, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=14
        )
    ),
    "Salamence's Sky Race Attraction -- Latios": PokeparkLocationData(
        511, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkSalamenceAttractionClientData(
            structure_position=0
        )
    ),
    "Salamence's Sky Race Attraction -- Latios Friendship": PokeparkLocationData(
        512, PokeparkFlag.ATTRACTION, "Salamence's Sky Race Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=166
        ),
    ),

    # Flower Zone

    "Flower Zone Main Area - Skiploom Power Competition -- Friendship": PokeparkLocationData(
        513, PokeparkFlag.FRIENDSHIP, "Flower Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=191
        ),
    ),
    "Flower Zone Main Area - Budew Power Competition -- Friendship": PokeparkLocationData(
        514, PokeparkFlag.FRIENDSHIP, "Flower Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=187
        ),
    ),
    "Flower Zone Main Area - Cyndaquil Power Competition -- Friendship": PokeparkLocationData(
        515, PokeparkFlag.CHASE, "Flower Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=99
        ),
    ),
    "Flower Zone Main Area - Lucario Power Competition -- Friendship": PokeparkLocationData(
        516, PokeparkFlag.CHASE, "Flower Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=152
        ),
    ),
    "Flower Zone Main Area - Dragonite Power Competition -- Friendship": PokeparkLocationData(
        517, PokeparkFlag.CHASE, "Flower Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=150
        ),
    ),
    "Flower Zone Main Area - Mareep Power Competition -- Friendship": PokeparkLocationData(
        518, PokeparkFlag.CHASE, "Flower Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=138
        ),
    ),
    "Flower Zone Main Area - Bellossom Power Competition -- Friendship": PokeparkLocationData(
        519, PokeparkFlag.ERRAND, "Flower Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=24
        ),
    ),
    "Flower Zone Main Area - Teddiursa Power Competition -- Friendship": PokeparkLocationData(
        520, PokeparkFlag.CHASE, "Flower Zone Main Area", Pokepark13AttractionClientData(
            structure_position=1
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Flower Zone Main Area - Furret Power Competition -- Friendship": PokeparkLocationData(
        521, PokeparkFlag.HIDEANDSEEK, "Flower Zone Main Area", Pokepark13AttractionClientData(
            structure_position=2
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Flower Zone Main Area - Meditite Power Competition -- Friendship": PokeparkLocationData(
        522, PokeparkFlag.QUIZ, "Flower Zone Main Area", Pokepark13AttractionClientData(
            structure_position=3
        ),
        each_zone=MultiZoneFlag.MULTI
    ),
    "Flower Zone Main Area - Rayquaza -- Friendship": PokeparkLocationData(
        523, PokeparkFlag.FRIENDSHIP, "Flower Zone Main Area", PokeparkFriendshipClientLocationData(
            structure_position=192
        ),
    ),
    # Rayquaza's Balloon Panic

    "Rayquaza's Balloon Panic Attraction -- Prisma": PokeparkLocationData(
        524, PokeparkFlag.ATTRACTION_PRISMA, "Rayquaza's Balloon Panic Attraction", PokeparkPrismaClientData(
            structure_position=1
        )
    ),

    "Rayquaza's Balloon Panic Attraction -- Pikachu": PokeparkLocationData(
        525, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=0
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Lucario": PokeparkLocationData(
        526, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=2
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Glaceon": PokeparkLocationData(
        527, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=6
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Luxray": PokeparkLocationData(
        528, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=7
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Mamoswine": PokeparkLocationData(
        529, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=9
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Infernape": PokeparkLocationData(
        530, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=4
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Floatzel": PokeparkLocationData(
        531, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=5
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Rhyperior": PokeparkLocationData(
        532, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=8
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Absol": PokeparkLocationData(
        533, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=3
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Breloom": PokeparkLocationData(
        534, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=10
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Mareep": PokeparkLocationData(
        535, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=11
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Cyndaquil": PokeparkLocationData(
        536, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=14
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Totodile": PokeparkLocationData(
        537, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=13
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Chikorita": PokeparkLocationData(
        538, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=12
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Mime Jr.": PokeparkLocationData(
        539, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=15
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Deoxys": PokeparkLocationData(
        540, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkRayquazaAttractionClientData(
            structure_position=1
        )
    ),
    "Rayquaza's Balloon Panic Attraction -- Deoxys Friendship": PokeparkLocationData(
        541, PokeparkFlag.ATTRACTION, "Rayquaza's Balloon Panic Attraction",
        PokeparkFriendshipClientLocationData(
            structure_position=168
        ),
    ),
    # Skygarden

    "Skygarden - Mew Power Competition -- Stage 1": PokeparkLocationData(
        542, PokeparkFlag.ALWAYS, "Skygarden",
        PokeparkMewChallengeGengarPaintingClientData(

            _expected_value=0b00010000,
            _bit_mask=0b00010000
        )
    ),
    "Skygarden - Mew Power Competition -- Stage 2": PokeparkLocationData(
        543, PokeparkFlag.ALWAYS, "Skygarden",
        PokeparkMewChallengeGengarPaintingClientData(

            _expected_value=0b00001000,
            _bit_mask=0b00001000
        )
    ),
    "Skygarden - Mew Power Competition -- Stage 3": PokeparkLocationData(
        544, PokeparkFlag.ALWAYS, "Skygarden",
        PokeparkMewChallengeGengarPaintingClientData(

            _expected_value=0b00000100,
            _bit_mask=0b00000100
        )
    ),
    "Skygarden - Mew Power Competition -- Stage 4": PokeparkLocationData(
        545, PokeparkFlag.ALWAYS, "Skygarden",
        PokeparkMewChallengeGengarPaintingClientData(

            _expected_value=0b00000010,
            _bit_mask=0b00000010
        )
    ),
    "Skygarden - Mew Power Competition -- Friendship": PokeparkLocationData(
        546, PokeparkFlag.ALWAYS, "Skygarden",
        PokeparkFriendshipClientLocationData(
            structure_position=169
        ),
    ),

    "Skygarden - Prisma Completion -- Stage 1": PokeparkLocationData(
        547, PokeparkFlag.POSTGAME, "Skygarden",
        PokeparkPrismaCompletionClientData(

            _expected_value=0b00000100,
            _bit_mask=0b00000100
        )
    ),
    "Skygarden - Prisma Completion -- Stage 2": PokeparkLocationData(
        548, PokeparkFlag.POSTGAME, "Skygarden",
        PokeparkPrismaCompletionClientData(

            _expected_value=0b00000110,
            _bit_mask=0b00000110
        )
    ),
    "Skygarden - Prisma Completion -- Completed": PokeparkLocationData(
        549, PokeparkFlag.POSTGAME, "Skygarden",
        PokeparkPrismaCompletionClientData(

            _expected_value=0b00001000,
            _bit_mask=0b00001000
        )
    ),

    "Abra - Friendship": PokeparkLocationData(
        550, PokeparkFlag.ALWAYS, "Abra", PokeparkFriendshipClientLocationData(
            structure_position=124
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Spearow Power Competition -- Friendship": PokeparkLocationData(
        551, PokeparkFlag.BATTLE, "Spearow", PokeparkFriendshipClientLocationData(
            structure_position=25
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Starly Power Competition -- Friendship": PokeparkLocationData(
        552, PokeparkFlag.CHASE, "Starly", PokeparkFriendshipClientLocationData(
            structure_position=20
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Bonsly Power Competition -- Friendship": PokeparkLocationData(
        553, PokeparkFlag.HIDEANDSEEK, "Bonsly", PokeparkFriendshipClientLocationData(
            structure_position=12
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Bonsly Power Competition -- Sudowoodo Unlocked": PokeparkLocationData(
        554, PokeparkFlag.HIDEANDSEEK, "Bonsly Unlocks", PokeparkFriendshipClientLocationData(
            structure_position=12
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Chimchar Power Competition -- Friendship": PokeparkLocationData(
        555, PokeparkFlag.BATTLE, "Chimchar", PokeparkFriendshipClientLocationData(
            structure_position=112
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Sudowoodo Power Competition -- Friendship": PokeparkLocationData(
        556, PokeparkFlag.HIDEANDSEEK, "Sudowoodo", PokeparkFriendshipClientLocationData(
            structure_position=13
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Aipom Power Competition -- Friendship": PokeparkLocationData(
        557, PokeparkFlag.CHASE, "Aipom", PokeparkFriendshipClientLocationData(
            structure_position=30
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Aipom Power Competition -- Ambipom Unlocked": PokeparkLocationData(
        558, PokeparkFlag.CHASE, "Aipom Unlocks", PokeparkFriendshipClientLocationData(
            structure_position=30
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Ambipom Power Competition -- Friendship": PokeparkLocationData(
        559, PokeparkFlag.BATTLE, "Ambipom", PokeparkFriendshipClientLocationData(
            structure_position=31
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Krabby Power Competition -- Friendship": PokeparkLocationData(
        560, PokeparkFlag.BATTLE, "Krabby", PokeparkFriendshipClientLocationData(
            structure_position=47
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Mudkip Power Competition -- Friendship": PokeparkLocationData(
        561, PokeparkFlag.HIDEANDSEEK, "Mudkip", PokeparkFriendshipClientLocationData(
            structure_position=46
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Taillow Power Competition -- Friendship": PokeparkLocationData(
        562, PokeparkFlag.CHASE, "Taillow", PokeparkFriendshipClientLocationData(
            structure_position=55
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Staravia Power Competition -- Friendship": PokeparkLocationData(
        563, PokeparkFlag.CHASE, "Staravia", PokeparkFriendshipClientLocationData(
            structure_position=21
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Wingull Power Competition -- Friendship": PokeparkLocationData(
        564, PokeparkFlag.CHASE, "Wingull", PokeparkFriendshipClientLocationData(
            structure_position=62
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Corphish Power Competition -- Friendship": PokeparkLocationData(
        565, PokeparkFlag.BATTLE, "Corphish", PokeparkFriendshipClientLocationData(
            structure_position=48
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Teddiursa Power Competition -- Friendship": PokeparkLocationData(
        566, PokeparkFlag.FRIENDSHIP, "Teddiursa", PokeparkFriendshipClientLocationData(
            structure_position=66
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Aron Power Competition -- Friendship": PokeparkLocationData(
        567, PokeparkFlag.ERRAND, "Aron", PokeparkFriendshipClientLocationData(
            structure_position=171
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Torchic Power Competition -- Friendship": PokeparkLocationData(
        568, PokeparkFlag.BATTLE, "Torchic", PokeparkFriendshipClientLocationData(
            structure_position=115
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Geodude Power Competition -- Friendship": PokeparkLocationData(
        569, PokeparkFlag.HIDEANDSEEK, "Geodude", PokeparkFriendshipClientLocationData(
            structure_position=81
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Raichu Power Competition -- Friendship": PokeparkLocationData(
        570, PokeparkFlag.CHASE, "Raichu", PokeparkFriendshipClientLocationData(
            structure_position=91
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Meowth Power Competition -- Friendship": PokeparkLocationData(
        571, PokeparkFlag.QUIZ, "Meowth", PokeparkFriendshipClientLocationData(
            structure_position=117
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Marowak Power Competition -- Friendship": PokeparkLocationData(
        572, PokeparkFlag.BATTLE, "Marowak", PokeparkFriendshipClientLocationData(
            structure_position=88
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Baltoy Power Competition -- Friendship": PokeparkLocationData(
        573, PokeparkFlag.BATTLE, "Baltoy", PokeparkFriendshipClientLocationData(
            structure_position=103
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Baltoy Power Competition -- Claydol Unlocked": PokeparkLocationData(
        574, PokeparkFlag.BATTLE, "Baltoy Unlocks", PokeparkFriendshipClientLocationData(
            structure_position=103
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Meditite Power Competition -- Friendship": PokeparkLocationData(
        575, PokeparkFlag.QUIZ, "Meditite", PokeparkFriendshipClientLocationData(
            structure_position=139
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Drifloon Power Competition -- Friendship": PokeparkLocationData(
        576, PokeparkFlag.FRIENDSHIP, "Drifloon", PokeparkFriendshipClientLocationData(
            structure_position=175
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Furret Power Competition -- Friendship": PokeparkLocationData(
        577, PokeparkFlag.HIDEANDSEEK, "Furret", PokeparkFriendshipClientLocationData(
            structure_position=140
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),
    "Claydol Power Competition -- Friendship": PokeparkLocationData(
        578, PokeparkFlag.BATTLE, "Claydol", PokeparkFriendshipClientLocationData(
            structure_position=104
        ),
        each_zone=MultiZoneFlag.SINGLE
    ),

}

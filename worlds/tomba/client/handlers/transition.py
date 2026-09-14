from CommonClient import logger

from . import AbstractHandler
from ..emulators.emulator import Emulator
from ...sections import Section, Sections
from ...bitutils import TypeSize, read_int, write_int, is_address

AREAS_ARRAY_ADDRESS = 0x07C54C


class Entrance:
    SIZE = 0x08

    address: int
    raw: bytearray
    animation_parameters: int
    animation: int
    section: Section
    spawn: int

    def __init__(self, address: int, raw: bytearray):
        self.address = address
        self.load(raw)

    def load(self, raw: bytearray):
        self.raw = raw
        self.animation_parameters = read_int(raw, 0, TypeSize.WORD, byteorder="big")
        self.animation = raw[4]
        self.section = Sections.get(Section(raw[5], raw[6]))
        self.spawn = raw[7]

    async def save(self, psx: Emulator):
        data = bytearray(Entrance.SIZE)

        data = write_int(data, 0x00, TypeSize.WORD, self.animation_parameters, byteorder="big")
        data[4] = self.animation
        data[5] = self.section.area_id
        data[6] = self.section.section_id
        data[7] = self.spawn

        await psx.write_memory(self.address, data)

    def __str__(self) -> str:
        return (
            f"Entrance 0x{self.address:08X} to {self.section} "
            + f"at spawn 0x{self.spawn:02X} with {self.animation:02X} method "
            + f"(anim params: {self.animation_parameters:08X})"
        )

    @staticmethod
    async def compute_entrances_array(psx: Emulator, section: Section) -> int:
        """Give the address of a given entrance
        Throws AttributeError if the entrance can not be found"""
        sections_array = await psx.read_int(AREAS_ARRAY_ADDRESS + section.area_id * TypeSize.WORD)
        if not is_address(sections_array):
            raise AttributeError(f"sections array is not loaded: {sections_array:08X}")

        entrances_array = await psx.read_int(sections_array + section.section_id * TypeSize.WORD)
        if not is_address(entrances_array):
            raise AttributeError(f"entrances array is not loaded: {entrances_array:08X}")

        return entrances_array


class TransitionHandler(AbstractHandler):
    """Handles transitions manipulations"""

    async def update_transitions(self, section: Section):
        """Re-writes all transitions to align on the randomized entrances"""
        pairings: dict[str, dict[int, tuple[int, int, int]]] = self.ctx.slot_data.get("entrance_pairings", [])

        if not pairings:
            # Alter the transition out of Mermaid Singing Beach
            target_section = Sections.MASAKARI_JUNGLE
            target_spawn = 0x01
            if self.ctx.slot_data.get("fast_motocross_retry", False):
                target_section = Sections.GARAGE
                target_spawn = 0x00

            pairings[Sections.THE_MERMAIDS_SINGING_BEACH.network_key()] = {}
            pairings[Sections.THE_MERMAIDS_SINGING_BEACH.network_key()][0x01] = (
                target_section.area_id,
                target_section.section_id,
                target_spawn,
            )

        entrances_array = await Entrance.compute_entrances_array(self.tomba.playstation, section)

        for entrance_id, target in pairings.get(section.get_unpurified().network_key(), {}).items():
            target_area = target[0]
            target_section = target[1]
            target_spawn = target[2]

            entrance_address = entrances_array + Entrance.SIZE * int(entrance_id)
            data = bytearray(3)
            data[0] = target_area
            data[1] = target_section
            data[2] = target_spawn

            await self.tomba.playstation.write_memory(entrance_address + 5, data)

            logger.debug(
                f"Update transition 0x{entrance_address:08X} "
                f"0x{int(entrance_id):02X} "
                f"to 0x{target_area:02X}-0x{target_section:02X} "
                f"at 0x{target_spawn:02X}"
            )

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from worlds.pokepark import FRIENDSHIP_ITEMS, UNLOCK_ITEMS, BERRIES
from worlds.pokepark.LocationIds import MinigameLocationIds, OverworldPokemonLocationIds, QuestLocationIds, \
    UnlockLocationIds
from worlds.pokepark.items import PRISM_ITEM, REGION_UNLOCK

pokemon_id_address = 0x8036dc20
stage_id_address = 0x8036AEF0  # word
is_in_menu_address = 0x80482F04
meadow_zone_stage_id = 0x13002E8
meadow_zone_loadscreen_stage_id = 0x12FFDFC
meadow_zone_venusaur_stage_id = 0x7D9C7C
beach_zone_stage_id = 0x1591C24
beach_zone_loadscreen_stage_id = 0x15916FC
ice_zone_stage_id = 0x129D6A0
ice_zone_loadscreen_stage_id = 0x129D0FC
treehouse_stage_id = 0x13282F8
cavern_zone_stage_id = 0x111C338
cavern_zone_loadscreen_stage_id = 0x111BD9C
magma_zone_stage_id = 0x167A9FC
magma_zone_loadscreen_stage_id = 0x167A27C
haunted_zone_stage_id = 0xE4D558
haunted_zone_loadscreen_stage_id = 0xE4D35C
haunted_zone_mansion_stage_id = 0x12BFC90
haunted_zone_mansion_loadscreen_stage_id = 0x12BF6DC
main_menu_stage_id = 0x6FC360
main_menu2_stage_id = 0x93BEA0
main_menu3_stage_id = 0x2A080
intro_stage_id = 0x940220
bulbasaur_minigame_stage_id = 0x98F584
venusaur_minigame_stage_id = 0xA81938
pelipper_minigame_stage_id = 0xD92358
gyarados_minigame_stage_id = 0xC61408
empoleon_minigame_stage_id = 0xBE6D00
bastidon_minigame_stage_id = 0xD02DA8
rhyperior_minigame_stage_id = 0xB78444
blaziken_minigame_stage_id = 0xA85D38
tangrowth_minigame_stage_id = 0xA8DC18
dusknoir_minigame_stage_id = 0xBA0DEC
rotom_minigame_stage_id = 0xB3E09C

LOADSCREEN_TO_ZONE = {
    meadow_zone_loadscreen_stage_id: meadow_zone_stage_id,
    beach_zone_loadscreen_stage_id: beach_zone_stage_id,
    ice_zone_loadscreen_stage_id: ice_zone_stage_id,
    cavern_zone_loadscreen_stage_id: cavern_zone_stage_id,
    magma_zone_loadscreen_stage_id: magma_zone_stage_id,
    haunted_zone_loadscreen_stage_id: haunted_zone_stage_id,
    haunted_zone_mansion_loadscreen_stage_id: haunted_zone_mansion_stage_id

}


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
    pokemon_ids: List[int]
    locationId: int
    friendship_items_to_block: List[int] | None = None,
    unlock_items_to_block: List[int] | None = None
    is_special_exception: bool = False


@dataclass
class PokemonStateInfo:
    item: MemoryAddress
    locations: List[PokemonLocation] = field(default_factory=list)


@dataclass
class MinigameLocation:
    locationId: int
    location: MemoryAddress
    stage_id: int


@dataclass
class QuestLocation:
    locationId: int
    location: MemoryAddress
    check_mask: int


@dataclass
class ZoneGateUnlocks:
    item_ids: List[int]
    stage_id: int
    gate: MemoryAddress


@dataclass
class ZoneState:
    """Represents a specific zone unlock state"""
    item_id: int
    world_state_value: int
    addresses: List[MemoryAddress]
    fast_travel_flag: int


@dataclass
class ZoneSystem:
    """Complete zone system including world states and gates"""
    world_state_address: int
    fast_travel_address: int
    states: List[ZoneState]
    treehouse_gates: List[ZoneGateUnlocks]
    connected_zone_gates: List[ZoneGateUnlocks]


ZONESYSTEM = ZoneSystem(world_state_address=0x8037500D,
                        fast_travel_address=0x8037502F,
                        states=[
                            ZoneState(
                                item_id=REGION_UNLOCK["Meadow Zone Unlock"],
                                world_state_value=0x7c0,
                                addresses=[
                                    MemoryAddress(  # unlock venusaur gate
                                        base_address=0x8037500F,
                                        value=0b01100000,
                                        memory_range=MemoryRange.BYTE),
                                    MemoryAddress(  # setup Bulbasaur
                                        base_address=0x80375020,
                                        value=0b00000010,
                                        memory_range=MemoryRange.BYTE),
                                    MemoryAddress(  # setup Bulbasaur
                                        base_address=0x80375010,
                                        value=0b10000000,
                                        memory_range=MemoryRange.BYTE)
                                ],
                                fast_travel_flag=0x80),
                            ZoneState(
                                item_id=REGION_UNLOCK["Beach Zone Unlock"],
                                world_state_value=0x870,
                                addresses=[
                                    MemoryAddress(  # unlock bidoof in beach zone
                                        base_address=0x80376af0,
                                        value=0b00001000,
                                        memory_range=MemoryRange.BYTE),
                                    MemoryAddress(  # bidoof quest state on completed
                                        base_address=0x80375026,
                                        value=0b00000011,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(  # activate all bridges in beach zone
                                        base_address=0x80375010,
                                        value=0b00111011,
                                        memory_range=MemoryRange.BYTE
                                    )
                                ],
                                fast_travel_flag=0x40),
                            ZoneState(
                                item_id=REGION_UNLOCK["Ice Zone Unlock"],
                                world_state_value=0xC1E,
                                addresses=[
                                    MemoryAddress(
                                        base_address=0x80375021,  # lift
                                        value=0b00001000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x80375013,  # gate and lake
                                        value=0b00001100,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x80375031,  # skip first christmas tree quest step
                                        value=0b00100000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                ],
                                fast_travel_flag=0x20),
                            ZoneState(
                                item_id=REGION_UNLOCK["Cavern Zone & Magma Zone Unlock"],
                                world_state_value=0x13f7,
                                addresses=[
                                    # Cavern zone

                                    # magma zone
                                    MemoryAddress(
                                        base_address=0x8037502B,  # clear fire main room
                                        value=0b10000000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x8037502A,  # clear fire below
                                        value=0b00000001,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x8037500C,  # lohgock bridge (map)
                                        value=0b00010000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x80375014,  # lohgock bridge
                                        value=0b00001000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x80375014,  # lohgock door
                                        value=0b00000100,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x80375028,  # skip farfetch dialog
                                        value=0b00010000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x80375031,  # skip lever dialog
                                        value=0b10000000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                ],
                                fast_travel_flag=0x18),  # +0x10 Cavern zone +0x08 magma zone
                            ZoneState(
                                item_id=REGION_UNLOCK["Haunted Zone Unlock"],
                                world_state_value=0x1c3f,
                                addresses=[

                                    MemoryAddress(
                                        base_address=0x8037501E,  # open door on bridge
                                        value=0b00000100,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x8037501F,  # open green gem door
                                        value=0b00100000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x8037501F,  # open blue gem door
                                        value=0b00010000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x8037501F,  # open red gem door
                                        value=0b00001000,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x8037501F,  # open black gem door
                                        value=0b00000100,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                    MemoryAddress(
                                        base_address=0x8037501F,  # open bookshelf to rotom
                                        value=0b00000010,
                                        memory_range=MemoryRange.BYTE
                                    ),
                                ],
                                fast_travel_flag=0x04),
                        ],
                        treehouse_gates=[
                            ZoneGateUnlocks(
                                stage_id=0x13282F8,
                                item_ids=[REGION_UNLOCK["Beach Zone Unlock"]],
                                gate=MemoryAddress(
                                    base_address=0x80D53068,
                                    memory_range=MemoryRange.WORD,
                                    value=0x01
                                )
                            ),
                            ZoneGateUnlocks(
                                stage_id=0x13282F8,
                                item_ids=[REGION_UNLOCK["Meadow Zone Unlock"]],
                                gate=MemoryAddress(
                                    base_address=0x80D52128,
                                    memory_range=MemoryRange.WORD,
                                    value=0x01
                                )
                            ),
                            ZoneGateUnlocks(
                                stage_id=0x13282F8,
                                item_ids=[REGION_UNLOCK["Cavern Zone & Magma Zone Unlock"]],
                                gate=MemoryAddress(
                                    base_address=0x80D53FA8,
                                    memory_range=MemoryRange.WORD,
                                    value=0x01
                                )
                            ),
                            ZoneGateUnlocks(
                                stage_id=0x13282F8,
                                item_ids=[REGION_UNLOCK["Haunted Zone Unlock"]],
                                gate=MemoryAddress(
                                    base_address=0x80D54EE8,
                                    memory_range=MemoryRange.WORD,
                                    value=0x01
                                )
                            )
                        ],
                        connected_zone_gates=[ZoneGateUnlocks(
                            stage_id=0x13282F8,  # not used here
                            item_ids=[REGION_UNLOCK["Beach Zone Unlock"], REGION_UNLOCK["Ice Zone Unlock"]],
                            gate=MemoryAddress(  # removes stone to lapras
                                base_address=0x80375012,
                                memory_range=MemoryRange.BYTE,
                                value=0b00010000)
                        )])

QUEST_LOCATIONS = [
    # Meadow Zone
    #
    QuestLocation(
        locationId=QuestLocationIds.MEADOW_BIDOOF_HOUSING1.value,
        location=MemoryAddress(
            base_address=0x8037500F,
            memory_range=MemoryRange.BYTE,
            value=0b00000110),
        check_mask=0b00000110
    ),
    QuestLocation(
        locationId=QuestLocationIds.MEADOW_BIDOOF_HOUSING2.value,
        location=MemoryAddress(
            base_address=0x8037500F,
            memory_range=MemoryRange.BYTE,
            value=0b00001010),
        check_mask=0b00001010
    ),
    QuestLocation(
        locationId=QuestLocationIds.MEADOW_BIDOOF_HOUSING3.value,
        location=MemoryAddress(
            base_address=0x8037500F,
            memory_range=MemoryRange.BYTE,
            value=0b00001110),
        check_mask=0b00001110
    ),
    QuestLocation(
        locationId=QuestLocationIds.MEADOW_BIDOOF_HOUSING4.value,
        location=MemoryAddress(
            base_address=0x8037500F,
            memory_range=MemoryRange.BYTE,
            value=0b00010010),
        check_mask=0b00010010
    ),

    # Beach Zone
    #
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE1.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00010000),
        check_mask=0b00010000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE2.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00100000),
        check_mask=0b00100000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE3.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00110000),
        check_mask=0b00110000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE4.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b01000000),
        check_mask=0b01000000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE5.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b01010000),
        check_mask=0b01010000
    ),
    QuestLocation(
        locationId=QuestLocationIds.BEACH_BOTTLE6.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b01100000),
        check_mask=0b01100000
    ),

    QuestLocation(
        locationId=QuestLocationIds.IGLOO_QUEST1.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00000010),
        check_mask=0b00000010
    ),
    QuestLocation(
        locationId=QuestLocationIds.IGLOO_QUEST2.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00000100),
        check_mask=0b00000100
    ),
    QuestLocation(
        locationId=QuestLocationIds.IGLOO_QUEST3.value,
        location=MemoryAddress(
            base_address=0x80375011,
            memory_range=MemoryRange.BYTE,
            value=0b00000110),
        check_mask=0b00000110
    ),
    QuestLocation(
        locationId=QuestLocationIds.CHRISTMAS_TREE1.value,
        location=MemoryAddress(
            base_address=0x80375023,
            memory_range=MemoryRange.BYTE,
            value=0b00010110),
        check_mask=0b00010110
    ),
    QuestLocation(
        locationId=QuestLocationIds.CHRISTMAS_TREE2.value,
        location=MemoryAddress(
            base_address=0x80375023,
            memory_range=MemoryRange.BYTE,
            value=0b00100111),
        check_mask=0b00100111
    ),
    QuestLocation(
        locationId=QuestLocationIds.CHRISTMAS_TREE3.value,
        location=MemoryAddress(
            base_address=0x80375023,
            memory_range=MemoryRange.BYTE,
            value=0b00110111),
        check_mask=0b00110111
    ),
    QuestLocation(
        locationId=QuestLocationIds.CHRISTMAS_TREE4.value,
        location=MemoryAddress(
            base_address=0x80375023,
            memory_range=MemoryRange.BYTE,
            value=0b01001111),
        check_mask=0b01001111
    ),

    # Power up Quest Check
    QuestLocation(
        locationId=QuestLocationIds.THUNDERBOLT_POWERUP1.value,
        location=MemoryAddress(
            base_address=0x8037501C,
            memory_range=MemoryRange.BYTE,
            value=0b00000001),
        check_mask=0b00000001
    ),
    QuestLocation(
        locationId=QuestLocationIds.THUNDERBOLT_POWERUP2.value,
        location=MemoryAddress(
            base_address=0x8037501C,
            memory_range=MemoryRange.BYTE,
            value=0b00000010),
        check_mask=0b00000010
    ),
    QuestLocation(
        locationId=QuestLocationIds.THUNDERBOLT_POWERUP3.value,
        location=MemoryAddress(
            base_address=0x8037501C,
            memory_range=MemoryRange.BYTE,
            value=0b00000011),
        check_mask=0b00000011
    ),
    QuestLocation(
        locationId=QuestLocationIds.DASH_POWERUP1.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00010000),
        check_mask=0b00010000
    ),
    QuestLocation(
        locationId=QuestLocationIds.DASH_POWERUP2.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00100000),
        check_mask=0b00100000
    ),
    QuestLocation(
        locationId=QuestLocationIds.DASH_POWERUP3.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00110000),
        check_mask=0b00110000
    ),
    QuestLocation(
        locationId=QuestLocationIds.HEALTH_POWERUP1.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00000001),
        check_mask=0b00000001
    ),
    QuestLocation(
        locationId=QuestLocationIds.HEALTH_POWERUP2.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00000010),
        check_mask=0b00000010
    ),
    QuestLocation(
        locationId=QuestLocationIds.HEALTH_POWERUP3.value,
        location=MemoryAddress(
            base_address=0x8037501d,
            memory_range=MemoryRange.BYTE,
            value=0b00000011),
        check_mask=0b00000011
    ),

    QuestLocation(
        locationId=QuestLocationIds.IRON_TAIL_POWERUP1.value,
        location=MemoryAddress(
            base_address=0x8037501E,
            memory_range=MemoryRange.BYTE,
            value=0b00010000),
        check_mask=0b00010000
    ),
    QuestLocation(
        locationId=QuestLocationIds.IRON_TAIL_POWERUP2.value,
        location=MemoryAddress(
            base_address=0x8037501E,
            memory_range=MemoryRange.BYTE,
            value=0b00100000),
        check_mask=0b00100000
    ),
    QuestLocation(
        locationId=QuestLocationIds.IRON_TAIL_POWERUP3.value,
        location=MemoryAddress(
            base_address=0x8037501E,
            memory_range=MemoryRange.BYTE,
            value=0b00110000),
        check_mask=0b00110000
    ),

    # Magma Zone
    QuestLocation(
        locationId=QuestLocationIds.MEDITITE_QUIZ.value,
        location=MemoryAddress(
            base_address=0x80375028,
            memory_range=MemoryRange.BYTE,
            value=0b00100000),
        check_mask=0b00100000
    ),
    QuestLocation(
        locationId=QuestLocationIds.RHYPERIOR_DISC.value,
        location=MemoryAddress(
            base_address=0x80375020,
            memory_range=MemoryRange.BYTE,
            value=0b10000000),
        check_mask=0b10000000
    ),

    # Haunted Zone
    QuestLocation(
        locationId=UNLOCK_ITEMS["Gengar Unlock"],
        location=MemoryAddress(
            base_address=0x80375031,
            memory_range=MemoryRange.BYTE,
            value=0b00000001),
        check_mask=0b00000001
    ),
]

MINIGAME_LOCATIONS = [
    # Meadow Zone - Bulbasaur's Daring Dash Minigame
    #
    MinigameLocation(
        MinigameLocationIds.PIKACHU_DASH.value,
        MemoryAddress(
            base_address=0x80377E30,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TURTWIG_DASH.value,
        MemoryAddress(
            base_address=0x80377EE4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MUNCHLAX_DASH.value,
        MemoryAddress(
            base_address=0x80377F20,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CHIMCHAR_DASH.value,
        MemoryAddress(
            base_address=0x80377EC0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TREECKO_DASH.value,
        MemoryAddress(
            base_address=0x80377ECC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BIBAREL_DASH.value,
        MemoryAddress(
            base_address=0x80377ED8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BULBASAUR_DASH.value,
        MemoryAddress(
            base_address=0x80377EF0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BIDOOF_DASH.value,
        MemoryAddress(
            base_address=0x80377EFC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.ODDISH_DASH.value,
        MemoryAddress(
            base_address=0x80377F08,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SHROOMISH_DASH.value,
        MemoryAddress(
            base_address=0x80377F14,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BONSLY_DASH.value,
        MemoryAddress(
            base_address=0x80377F2C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.LOTAD_DASH.value,
        MemoryAddress(
            base_address=0x80377F38,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.WEEDLE_DASH.value,
        MemoryAddress(
            base_address=0x80377F44,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CATERPIE_DASH.value,
        MemoryAddress(
            base_address=0x80377F50,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGIKARP_DASH.value,
        MemoryAddress(
            base_address=0x80377F5C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.JOLTEON_DASH.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bulbasaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.ARCANINE_DASH.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.LEAFEON_DASH.value,
        MemoryAddress(
            base_address=0x80377E60,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SCYTHER_DASH.value,
        MemoryAddress(
            base_address=0x80377e6c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PONYTA_DASH.value,
        MemoryAddress(
            base_address=0x80377e78,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SHINX_DASH.value,
        MemoryAddress(
            base_address=0x80377E84,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.EEVEE_DASH.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PACHIRISU_DASH.value,
        MemoryAddress(
            base_address=0x80377E9C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BUNEARY_DASH.value,
        MemoryAddress(
            base_address=0x80377EA8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CROAGUNK_DASH.value,
        MemoryAddress(
            base_address=0x80377EB4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bulbasaur_minigame_stage_id),

    # Meadow Zone - Venusaur's Vine Swing Minigame
    #
    MinigameLocation(
        MinigameLocationIds.PIKACHU_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376DBC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MUNCHLAX_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e64,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGIKARP_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e70,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.BLAZIKEN_VINE_SWING.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.INFERNAPE_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376de0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.LUCARIO_VINE_SWING.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PRIMEAPE_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376E04,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TANGROWTH_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376df8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.AMBIPOM_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e10,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CROAGUNK_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e4c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MANKEY_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e1c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.AIPOM_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e28,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CHIMCHAR_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e34,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TREECKO_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e40,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PACHIRISU_VINE_SWING.value,
        MemoryAddress(
            base_address=0x80376e58,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=venusaur_minigame_stage_id),

    # Beach Zone Pelipper's Circle Circuit
    #
    MinigameLocation(
        MinigameLocationIds.PIKACHU_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377380,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.STARAPTOR_CIRCLE.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=pelipper_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.TOGEKISS_CIRCLE.value,
    #     MemoryAddress(
    #         base_address=,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.HONCHKROW_CIRCLE.value,
        MemoryAddress(
            base_address=0x803772f0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GLISCOR_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377314,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PELIPPER_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377338,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.STARAVIA_CIRCLE.value,
        MemoryAddress(
            base_address=0x803772FC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PIDGEOTTO_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377308,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BUTTERFREE_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377374,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TROPIUS_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377368,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MURKROW_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377350,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TAILLOW_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377320,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SPEAROW_CIRCLE.value,
        MemoryAddress(
            base_address=0x8037732C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.STARLY_CIRCLE.value,
        MemoryAddress(
            base_address=0x80377344,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.WINGULL_CIRCLE.value,
        MemoryAddress(
            base_address=0x8037735c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=pelipper_minigame_stage_id),

    # Beach Zone Gyarados' Aqua Dash
    #
    MinigameLocation(
        MinigameLocationIds.PIKACHU_AQUA.value,
        MemoryAddress(
            base_address=0x80377218,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PSYDUCK_AQUA.value,
        MemoryAddress(
            base_address=0x80377224,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.AZURILL_AQUA.value,
        MemoryAddress(
            base_address=0x80377230,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SLOWPOKE_AQUA.value,
        MemoryAddress(
            base_address=0x8037723c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.EMPOLEON_AQUA.value,
        MemoryAddress(
            base_address=0x80377194,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.FLOATZEL_AQUA.value,
        MemoryAddress(
            base_address=0x803771a0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.FERALIGATR_AQUA.value,
        MemoryAddress(
            base_address=0x803771ac,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GOLDUCK_AQUA.value,
        MemoryAddress(
            base_address=0x803771b8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.VAPOREON_AQUA.value,
        MemoryAddress(
            base_address=0x803771c4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PRINPLUP_AQUA.value,
        MemoryAddress(
            base_address=0x803771d0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BIBAREL_AQUA.value,
        MemoryAddress(
            base_address=0x803771dc,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BUIZEL_AQUA.value,
        MemoryAddress(
            base_address=0x803771f4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CORSOLA_AQUA.value,
        MemoryAddress(
            base_address=0x803771e8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PIPLUP_AQUA.value,
        MemoryAddress(
            base_address=0x80377200,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.LOTAD_AQUA.value,
        MemoryAddress(
            base_address=0x8037720c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=gyarados_minigame_stage_id),

    # Ice Zone - Empoleon's Snow Slide
    MinigameLocation(
        MinigameLocationIds.PIKACHU_SLIDE.value,
        MemoryAddress(
            base_address=0x803775F0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TEDDIURSA_SLIDE.value,
        MemoryAddress(
            base_address=0x803775FC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PIPLUP_SLIDE.value,
        MemoryAddress(
            base_address=0x803775CC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.LAPRAS_SLIDE.value,
        MemoryAddress(
            base_address=0x80377590,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SPHEAL_SLIDE.value,
        MemoryAddress(
            base_address=0x803775D8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGIKARP_SLIDE.value,
        MemoryAddress(
            base_address=0x80377608,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GLACEON_SLIDE.value,
        MemoryAddress(
            base_address=0x8037756C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GLALIE_SLIDE.value,
        MemoryAddress(
            base_address=0x80377584,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.DELIBIRD_SLIDE.value,
        MemoryAddress(
            base_address=0x803775A8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PILOSWINE_SLIDE.value,
        MemoryAddress(
            base_address=0x803775E4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PRINPLUP_SLIDE.value,
        MemoryAddress(
            base_address=0x8037759C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SQUIRTLE_SLIDE.value,
        MemoryAddress(
            base_address=0x803775C0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.QUAGSIRE_SLIDE.value,
        MemoryAddress(
            base_address=0x803775B4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.EMPOLEON_SLIDE.value,
        MemoryAddress(
            base_address=0x80377560,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=empoleon_minigame_stage_id),

    # Cavern Zone - Bastiodon's Panel Crush
    MinigameLocation(
        MinigameLocationIds.PIKACHU_PANEL.value,
        MemoryAddress(
            base_address=0x80377728,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SABLEYE_PANEL.value,
        MemoryAddress(
            base_address=0x803776e0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MEOWTH_PANEL.value,
        MemoryAddress(
            base_address=0x80377740,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TORCHIC_PANEL.value,
        MemoryAddress(
            base_address=0x80377734,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.ELECTIVIRE_PANEL.value,
    #     MemoryAddress(
    #         base_address=0x,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bastidon_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.MAGMORTAR_PANEL.value,
    #     MemoryAddress(
    #         base_address=0x,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.HITMONLEE_PANEL.value,
        MemoryAddress(
            base_address=0x803776a4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.URSARING_PANEL.value,
        MemoryAddress(
            base_address=0x803776d4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MRMIME_PANEL.value,
        MemoryAddress(
            base_address=0x803776ec,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.RAICHU_PANEL.value,
        MemoryAddress(
            base_address=0x803776c8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SUDOWOODO_PANEL.value,
        MemoryAddress(
            base_address=0x803776f8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CHARMANDER_PANEL.value,
        MemoryAddress(
            base_address=0x80377704,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GIBLE_PANEL.value,
        MemoryAddress(
            base_address=0x80377710,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CHIMCHAR_PANEL.value,
        MemoryAddress(
            base_address=0x8037771c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGBY_PANEL.value,
        MemoryAddress(
            base_address=0x8037774c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=bastidon_minigame_stage_id),

    # Magma Zone - Rhyperior's Bumper Burn
    MinigameLocation(
        MinigameLocationIds.PIKACHU_BUMPER.value,
        MemoryAddress(
            base_address=0x80377884,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGNEMITE_BUMPER.value,
        MemoryAddress(
            base_address=0x803777e8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.RHYPERIOR_BUMPER.value,
        MemoryAddress(
            base_address=0x803777e8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.TYRANITAR_BUMPER.value,
    #     MemoryAddress(
    #         base_address=0x,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.HITMONTOP_BUMPER.value,
        MemoryAddress(
            base_address=0x80377800,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.FLAREON_BUMPER.value,
        MemoryAddress(
            base_address=0x8037780c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.VENUSAUR_BUMPER.value,
        MemoryAddress(
            base_address=0x80377818,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.SNORLAX_BUMPER.value,
    #     MemoryAddress(
    #         base_address=0x,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TORTERRA_BUMPER.value,
        MemoryAddress(
            base_address=0x80377830,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGNEZONE_BUMPER.value,
        MemoryAddress(
            base_address=0x8037783c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CLAYDOL_BUMPER.value,
        MemoryAddress(
            base_address=0x80377848,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.QUILAVA_BUMPER.value,
        MemoryAddress(
            base_address=0x80377854,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.TORKOAL_BUMPER.value,
        MemoryAddress(
            base_address=0x80377860,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BALTOY_BUMPER.value,
        MemoryAddress(
            base_address=0x8037786c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BONSLY_BUMPER.value,
        MemoryAddress(
            base_address=0x80377878,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rhyperior_minigame_stage_id),

    # Magma Zone - Blaziken's Boulder Bash

    MinigameLocation(
        MinigameLocationIds.PIKACHU_BOULDER.value,
        MemoryAddress(
            base_address=0x803779BC,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GEODUDE_BOULDER.value,
        MemoryAddress(
            base_address=0x803779c8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PHANPY_BOULDER.value,
        MemoryAddress(
            base_address=0x803779d4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.BLAZIKEN_BOULDER.value,
    #     MemoryAddress(
    #         base_address=0x,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=blaziken_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.GARCHOMP_BOULDER.value,
    #     MemoryAddress(
    #         base_address=0x,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SCIZOR_BOULDER.value,
        MemoryAddress(
            base_address=0x80377944,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.MAGMORTAR_BOULDER.value,
    #     MemoryAddress(
    #         base_address=0x80377944,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.HITMONCHAN_BOULDER.value,
        MemoryAddress(
            base_address=0x8037795c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MACHAMP_BOULDER.value,
        MemoryAddress(
            base_address=0x80377968,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAROWAK_BOULDER.value,
        MemoryAddress(
            base_address=0x80377980,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.FARFETCHD_BOULDER.value,
        MemoryAddress(
            base_address=0x803779b0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CRANIDOS_BOULDER.value,
        MemoryAddress(
            base_address=0x8037798c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CAMERUPT_BOULDER.value,
        MemoryAddress(
            base_address=0x80377998,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BASTIODON_BOULDER.value,
        MemoryAddress(
            base_address=0x80377974,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAWILE_BOULDER.value,
        MemoryAddress(
            base_address=0x803779a4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=blaziken_minigame_stage_id),

    # Tangrowth's Swing-Along
    MinigameLocation(
        MinigameLocationIds.PIKACHU_SWING.value,
        MemoryAddress(
            base_address=0x80376F00,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MEOWTH_SWING.value,
        MemoryAddress(
            base_address=0x80376FA8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PICHU_SWING.value,
        MemoryAddress(
            base_address=0x80376fb4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.LUCARIO_SWING.value,
    #     MemoryAddress(
    #         base_address=0x80376fb4,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.INFERNAPE_SWING.value,
        MemoryAddress(
            base_address=0x80376f24,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.BLAZIKEN_SWING.value,
    #     MemoryAddress(
    #         base_address=0x80376f24,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.RIOLU_SWING.value,
        MemoryAddress(
            base_address=0x80376f3c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SNEASEL_SWING.value,
        MemoryAddress(
            base_address=0x80376f48,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.RAICHU_SWING.value,
        MemoryAddress(
            base_address=0x80376f60,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.AMBIPOM_SWING.value,
        MemoryAddress(
            base_address=0x80376f6c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.PRIMEAPE_SWING.value,
        MemoryAddress(
            base_address=0x80376f78,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.AIPOM_SWING.value,
        MemoryAddress(
            base_address=0x80376f84,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.ELECTABUZZ_SWING.value,
        MemoryAddress(
            base_address=0x80376f54,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CHIMCHAR_SWING.value,
        MemoryAddress(
            base_address=0x80376f88,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CROAGUNK_SWING.value,
        MemoryAddress(
            base_address=0x80376f94,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=tangrowth_minigame_stage_id),

    # Dusknoir's Speed Slam
    MinigameLocation(
        MinigameLocationIds.PIKACHU_SLAM.value,
        MemoryAddress(
            base_address=0x80377044,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),

    MinigameLocation(
        MinigameLocationIds.STUNKY_SLAM.value,
        MemoryAddress(
            base_address=0x803770ec,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),

    MinigameLocation(
        MinigameLocationIds.GENGAR_SLAM.value,
        MemoryAddress(
            base_address=0x8037705c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MISMAGIUS_SLAM.value,
        MemoryAddress(
            base_address=0x80377074,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SCIZOR_SLAM.value,
        MemoryAddress(
            base_address=0x80377080,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.ESPEON_SLAM.value,
        MemoryAddress(
            base_address=0x80377068,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.DUSKNOIR_SLAM.value,
        MemoryAddress(
            base_address=0x8037708c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.UMBREON_SLAM.value,
        MemoryAddress(
            base_address=0x80377098,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CRANIDOS_SLAM.value,
        MemoryAddress(
            base_address=0x803770bc,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.SKUNTANK_SLAM.value,
        MemoryAddress(
            base_address=0x803770c8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.ELECTRODE_SLAM.value,
        MemoryAddress(
            base_address=0x803770b0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GASTLY_SLAM.value,
        MemoryAddress(
            base_address=0x803770e0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.DUSKULL_SLAM.value,
        MemoryAddress(
            base_address=0x803770f8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MISDREAVUS_SLAM.value,
        MemoryAddress(
            base_address=0x803770d4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.KRABBY_SLAM.value,
        MemoryAddress(
            base_address=0x803770a4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=dusknoir_minigame_stage_id),

    # Rotom's Spooky Shoot-'em-Up
    MinigameLocation(
        MinigameLocationIds.PIKACHU_SHOOT.value,
        MemoryAddress(
            base_address=0x80377B0C,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGNEMITE_SHOOT.value,
        MemoryAddress(
            base_address=0x80377b18,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.PORYGONZ_SHOOT.value,
    #     MemoryAddress(
    #         base_address=0x,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MAGNEZONE_SHOOT.value,
        MemoryAddress(
            base_address=0x80377a7c,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.GENGAR_SHOOT.value,
        MemoryAddress(
            base_address=0x80377a88,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.MAGMORTAR_SHOOT.value,
    #     MemoryAddress(
    #         base_address=0x80377a88,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=rotom_minigame_stage_id),
    # MinigameLocation(
    #     MinigameLocationIds.ELECTIVIRE_SHOOT.value,
    #     MemoryAddress(
    #         base_address=0x80377a88,
    #         memory_range=MemoryRange.HALFWORD,
    #         value=0x0001),
    #     stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MISMAGIUS_SHOOT.value,
        MemoryAddress(
            base_address=0x80377aac,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.CLAYDOL_SHOOT.value,
        MemoryAddress(
            base_address=0x80377ab8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.ELECTABUZZ_SHOOT.value,
        MemoryAddress(
            base_address=0x80377ad0,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.HAUNTER_SHOOT.value,
        MemoryAddress(
            base_address=0x80377adc,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.ABRA_SHOOT.value,
        MemoryAddress(
            base_address=0x80377ae8,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.ELEKID_SHOOT.value,
        MemoryAddress(
            base_address=0x80377af4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.MRMIME_SHOOT.value,
        MemoryAddress(
            base_address=0x80377ac4,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
    MinigameLocation(
        MinigameLocationIds.BALTOY_SHOOT.value,
        MemoryAddress(
            base_address=0x80377b00,
            memory_range=MemoryRange.HALFWORD,
            value=0x0001),
        stage_id=rotom_minigame_stage_id),
]

blocked_friendship_itemIds = []
blocked_friendship_unlock_itemIds = []
POKEMON_STATES = {
    # Meadow Zone Pokemon
    #
    FRIENDSHIP_ITEMS["Chikorita"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375C74, memory_range=MemoryRange.BYTE, value=0x80),
    ),

    FRIENDSHIP_ITEMS["Pachirisu"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375210, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375210, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000031, 0x00000004],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Pachirisu"]],
                locationId=FRIENDSHIP_ITEMS["Pachirisu"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Bulbasaur"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375490, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375490, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bulbasaur"]],
                locationId=FRIENDSHIP_ITEMS["Bulbasaur"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Munchlax"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037529C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037529C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000002f, 0x00000005],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Munchlax"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Tropius Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Munchlax"],
                is_special_exception=True
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Tropius"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753DC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803753DC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000017],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Tropius"]],
                locationId=FRIENDSHIP_ITEMS["Tropius"],
                is_special_exception=True
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Turtwig"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751D4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803751D4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000002d, 0x00000002],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Turtwig"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Bonsly Unlock"], UNLOCK_ITEMS["Pachirisu Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Turtwig"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Bonsly"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752C4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752C4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bonsly"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Sudowoodo Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Bonsly"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752C4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000005],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bonsly"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Sudowoodo Unlock"]],
                locationId=OverworldPokemonLocationIds.BONSLY_CAVERN.value
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752C4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000003],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bonsly"]],
                locationId=OverworldPokemonLocationIds.BONSLY_MAGMA.value
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Sudowoodo"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752D8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752D8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Sudowoodo"]],
                locationId=FRIENDSHIP_ITEMS["Sudowoodo"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752D8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000001a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Sudowoodo"]],
                locationId=OverworldPokemonLocationIds.SUDOWOODO_CAVERN.value
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Buneary"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037533C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037533C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000003],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Buneary"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Lotad Unlock"], UNLOCK_ITEMS["Shinx Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Buneary"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Shinx"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753F0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803753F0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000010, 0x0000002c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Shinx"]],
                locationId=FRIENDSHIP_ITEMS["Shinx"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Mankey"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375314, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Spearow"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753C8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803753C8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000027, 0x00000013],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Spearow"]],
                locationId=FRIENDSHIP_ITEMS["Spearow"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Croagunk"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037547C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037547C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Croagunk"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Scyther Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Croagunk"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Chatot"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80376034, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Lotad"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375224, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375224, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000021, 0x00000009, 0x00000028, 0x00000029],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Lotad"]],
                locationId=FRIENDSHIP_ITEMS["Lotad"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Treecko"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751FC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803751FC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000006],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Treecko"]],
                locationId=FRIENDSHIP_ITEMS["Treecko"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Caterpie"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375274, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375274, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Caterpie"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Butterfree Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Caterpie"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Butterfree"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375288, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375288, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000002e, 0x00000016],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Butterfree"]],
                locationId=FRIENDSHIP_ITEMS["Butterfree"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Chimchar"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375A94, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375A94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000007],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Chimchar"]],
                locationId=FRIENDSHIP_ITEMS["Chimchar"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375A94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000004],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Chimchar"]],
                locationId=OverworldPokemonLocationIds.CHIMCHAR_CAVERN.value
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375A94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x0000000a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Chimchar"]],
                locationId=OverworldPokemonLocationIds.CHIMCHAR_MAGMA.value
            ),
        ]
    ),
    FRIENDSHIP_ITEMS["Aipom"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037542C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037542C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000025, 0x00000012],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Aipom"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Ambipom Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Aipom"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037542C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x00000003],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Aipom"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Ambipom Unlock"]],
                locationId=OverworldPokemonLocationIds.AIPOM_HAUNTED.value
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Ambipom"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375440, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375440, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000019],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Ambipom"]],
                locationId=FRIENDSHIP_ITEMS["Ambipom"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375440, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x00000004],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Ambipom"]],
                locationId=OverworldPokemonLocationIds.AMBIPOM_HAUNTED.value
            ),
        ]
    ),
    FRIENDSHIP_ITEMS["Weedle"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375260, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375260, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Weedle"]],
                locationId=FRIENDSHIP_ITEMS["Weedle"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Shroomish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752EC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803752EC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Shroomish"]],
                locationId=FRIENDSHIP_ITEMS["Shroomish"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Magikarp"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756D4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756D4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000008],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Magikarp"]],
                locationId=FRIENDSHIP_ITEMS["Magikarp"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Oddish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753A0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803753A0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Oddish"]],
                locationId=FRIENDSHIP_ITEMS["Oddish"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Leafeon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754CC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803754CC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001C],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Leafeon"]],
                locationId=FRIENDSHIP_ITEMS["Leafeon"],
                is_special_exception=True
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Bidoof"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375238, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375238, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000000c],
                unlock_items_to_block=[UNLOCK_ITEMS["Bidoof Unlock"],
                                       UNLOCK_ITEMS["Bidoof Unlock 2"],
                                       UNLOCK_ITEMS["Bidoof Unlock 3"],
                                       UNLOCK_ITEMS["Bidoof Unlock 3"]],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bidoof"]],
                locationId=FRIENDSHIP_ITEMS["Bidoof"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Starly"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375364, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(  # Meadow Zone
                location=MemoryAddress(base_address=0x80375364, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000023, 0x00000024, 0x0000002a, 0x00000015, 0x00000026],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Starly"]],
                locationId=FRIENDSHIP_ITEMS["Starly"]
            ),
            PokemonLocation(  # Beach Zone
                location=MemoryAddress(base_address=0x80375364, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000026, 0x00000008],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Starly"]],
                locationId=OverworldPokemonLocationIds.STARLY_BEACH.value
            ),
            PokemonLocation(  # Ice Zone
                location=MemoryAddress(base_address=0x80375364, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000001f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Starly"]],
                locationId=OverworldPokemonLocationIds.STARLY_ICE.value
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Torterra"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751E8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803751E8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Torterra"]],
                locationId=FRIENDSHIP_ITEMS["Torterra"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Bibarel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037524C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037524C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x00000018],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Bibarel"]],
                locationId=FRIENDSHIP_ITEMS["Bibarel"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Scyther"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375454, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375454, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Scyther"]],
                locationId=FRIENDSHIP_ITEMS["Scyther"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Venusaur"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754a4, memory_range=MemoryRange.BYTE, value=0x80)
    ),

    # Beach Zone Pokemon
    #
    #
    FRIENDSHIP_ITEMS["Buizel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755d0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755d0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000002],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Buizel"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Floatzel Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Buizel"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Psyduck"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755F8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755F8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000003],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Psyduck"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Golduck Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Psyduck"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Slowpoke"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755BC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755BC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000004],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Slowpoke"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Mudkip Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Slowpoke"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Azurill"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375558, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375558, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000005],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Azurill"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Totodile Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Azurill"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Totodile"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375670, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375670, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000000c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Totodile"]],
                locationId=FRIENDSHIP_ITEMS["Totodile"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Mudkip"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037556C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037556C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000000d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Mudkip"]],
                locationId=FRIENDSHIP_ITEMS["Mudkip"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Pidgeotto"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375634, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375634, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000018],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Pidgeotto"]],
                locationId=FRIENDSHIP_ITEMS["Pidgeotto"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Taillow"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375620, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(  # Beach Zone
                location=MemoryAddress(base_address=0x80375620, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000029, 0x00000024],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Taillow"]],
                locationId=FRIENDSHIP_ITEMS["Taillow"]
            ),
            PokemonLocation(  # Ice Zone
                location=MemoryAddress(base_address=0x80375620, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Taillow"]],
                locationId=OverworldPokemonLocationIds.TAILLOW_ICE.value
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Wingull"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756ac, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756ac, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000000a, 0x0000002b, 0x00000024],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Wingull"]],
                locationId=FRIENDSHIP_ITEMS["Wingull"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756ac, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000002f, 0x0000002e, 0x00000010],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Wingull"]],
                locationId=OverworldPokemonLocationIds.WINGULL_ICE.value
            )
        ]
    ),

    FRIENDSHIP_ITEMS["Staravia"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375378, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(  # Beach Zone
                location=MemoryAddress(base_address=0x80375378, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000017],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Staravia"]],
                locationId=FRIENDSHIP_ITEMS["Staravia"]
            ),
            PokemonLocation(  # Ice Zone
                location=MemoryAddress(base_address=0x80375378, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Staravia"]],
                locationId=OverworldPokemonLocationIds.STARAVIA_ICE.value
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Corsola"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755A8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755A8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000022, 0x00000021, 0x00000006],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Corsola"]],
                locationId=FRIENDSHIP_ITEMS["Corsola"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Floatzel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755E4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803755E4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000016],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Floatzel"]],
                locationId=FRIENDSHIP_ITEMS["Floatzel"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Vaporeon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754E0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803754E0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Vaporeon"]],
                locationId=FRIENDSHIP_ITEMS["Vaporeon"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Golduck"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037560C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037560C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000015],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Golduck"]],
                locationId=FRIENDSHIP_ITEMS["Golduck"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Pelipper"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756C0, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Sharpedo"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80376048, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Wynaut"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375C88, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Carvanha"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375FE4, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Krabby"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375580, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(  # Beach Zone
                location=MemoryAddress(base_address=0x80375580, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000002c, 0x0000002d, 0x0000000b, 0x00000020],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Krabby"]],
                locationId=FRIENDSHIP_ITEMS["Krabby"],
            ),
            PokemonLocation(  # Ice Zone
                location=MemoryAddress(base_address=0x80375580, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000002d, 0x00000004, 0x0000002c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Krabby"]],
                locationId=OverworldPokemonLocationIds.KRABBY_ICE.value
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Wailord"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803760ac, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803760ac, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x00000013],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Wailord"]],
                locationId=FRIENDSHIP_ITEMS["Wailord"],
                is_special_exception=True
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Corphish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375594, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375594, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000002f, 0x0000002e, 0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Corphish"]],
                locationId=FRIENDSHIP_ITEMS["Corphish"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375594, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000005, 0x00000022, 0x00000023],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Corphish"]],
                locationId=OverworldPokemonLocationIds.CORPHISH_ICE.value
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Gyarados"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756E8, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Feraligatr"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375684, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375684, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000001b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Feraligatr"]],
                locationId=FRIENDSHIP_ITEMS["Feraligatr"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Piplup"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757EC, memory_range=MemoryRange.BYTE, value=0x80)),

    # Treehouse
    FRIENDSHIP_ITEMS["Burmy"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80376020, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80376020, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=treehouse_stage_id,
                pokemon_ids=[0x00000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Burmy"]],
                locationId=FRIENDSHIP_ITEMS["Burmy"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Mime Jr."]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375940, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375940, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=treehouse_stage_id,
                pokemon_ids=[0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Mime Jr."]],
                locationId=FRIENDSHIP_ITEMS["Mime Jr."]
            )
        ]
    ),

    # multiple versions since friendship is possible in multiple region, but for now its juts one location
    FRIENDSHIP_ITEMS["Drifblim"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375f94, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(  # Treehouse
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=treehouse_stage_id,
                pokemon_ids=[0x0000001d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            ),
            PokemonLocation(  # Meadow Zone
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=meadow_zone_stage_id,
                pokemon_ids=[0x0000001f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            ),
            PokemonLocation(  # Beach Zone
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000001f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            ),
            PokemonLocation(  # Ice Zone
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000001c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            ),
            PokemonLocation(  # Cavern Zone
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000018],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            ),
            PokemonLocation(  # Magma Zone
                location=MemoryAddress(base_address=0x80375f94, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000019],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifblim"]],
                locationId=FRIENDSHIP_ITEMS["Drifblim"]
            )
        ]
    ),

    # also multiple version of lapras since it has Beach Zone and Ice Zone locations, for now one location
    FRIENDSHIP_ITEMS["Lapras"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375698, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(  # Beach Zone
                location=MemoryAddress(base_address=0x80375698, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=beach_zone_stage_id,
                pokemon_ids=[0x0000001c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Lapras"]],
                locationId=FRIENDSHIP_ITEMS["Lapras"]
            ),
            PokemonLocation(  # Ice Zone
                location=MemoryAddress(base_address=0x80375698, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000017],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Lapras"]],
                locationId=FRIENDSHIP_ITEMS["Lapras"]
            )
        ]
    ),

    FRIENDSHIP_ITEMS["Spheal"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375724, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375724, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000001d, 0x00000026, 0x0000001e, 0x00000029, 0x00000028, 0x00000006, 0x00000027],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Spheal"]],
                locationId=FRIENDSHIP_ITEMS["Spheal"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Octillery"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375788, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375788, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000024, 0x00000014, 0x00000025],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Octillery"]],
                locationId=FRIENDSHIP_ITEMS["Octillery"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Teddiursa"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756FC, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756FC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000021, 0x00000007],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Teddiursa"]],
                locationId=FRIENDSHIP_ITEMS["Teddiursa"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x803756FC, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000019],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Teddiursa"]],
                locationId=OverworldPokemonLocationIds.TEDDIURSA_CAVERN.value
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Delibird"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375774, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375774, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000008],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Delibird"]],
                locationId=FRIENDSHIP_ITEMS["Delibird"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Smoochum"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375738, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375738, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000b, 0x00000030, 0x00000031],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Smoochum"]],
                locationId=FRIENDSHIP_ITEMS["Smoochum"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Squirtle"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375648, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375648, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Squirtle"]],
                locationId=FRIENDSHIP_ITEMS["Squirtle"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Glaceon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754F4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803754F4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000016],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Glaceon"]],
                locationId=FRIENDSHIP_ITEMS["Glaceon"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Prinplup"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375800, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375800, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000001b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Prinplup"]],
                locationId=FRIENDSHIP_ITEMS["Prinplup"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Sneasel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037574C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037574C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000020, 0x00000001],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Sneasel"]],
                locationId=FRIENDSHIP_ITEMS["Sneasel"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Piloswine"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757C4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803757C4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000000a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Piloswine"]],
                locationId=FRIENDSHIP_ITEMS["Piloswine"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Glalie"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037579C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037579C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000015],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Glalie"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Ursaring Unlock"], UNLOCK_ITEMS["Primeape Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Glalie"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Froslass"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757B0, memory_range=MemoryRange.BYTE, value=0x80)
    ),
    FRIENDSHIP_ITEMS["Primeape"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375328, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375328, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000012],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Primeape"]],
                locationId=FRIENDSHIP_ITEMS["Primeape"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Ursaring"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375710, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375710, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000013],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Ursaring"]],
                locationId=FRIENDSHIP_ITEMS["Ursaring"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Mamoswine"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757D8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803757D8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000019],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Mamoswine"]],
                locationId=FRIENDSHIP_ITEMS["Mamoswine"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Kirlia"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375DC8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375DC8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x00000009],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Kirlia"]],
                locationId=FRIENDSHIP_ITEMS["Kirlia"]
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Quagsire"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375760, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375760, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=ice_zone_stage_id,
                pokemon_ids=[0x0000002a, 0x00000011, 0x0000002b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Quagsire"]],
                locationId=FRIENDSHIP_ITEMS["Quagsire"],
                is_special_exception=True
            )
        ]
    ),
    FRIENDSHIP_ITEMS["Empoleon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375814, memory_range=MemoryRange.BYTE, value=0x80)
    ),

    # Cavern Zone
    #
    FRIENDSHIP_ITEMS["Magnemite"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375a08, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375a08, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000006],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Magnemite"]],
                locationId=FRIENDSHIP_ITEMS["Magnemite"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375a08, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000028],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Magnemite"]],
                locationId=OverworldPokemonLocationIds.MAGNEMITE_CAVERN_2.value
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375a08, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000029],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Magnemite"]],
                locationId=OverworldPokemonLocationIds.MAGNEMITE_CAVERN_3.value
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Magnezone"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375a1c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375a1c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000001d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Magnezone"]],
                locationId=FRIENDSHIP_ITEMS["Magnezone"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Geodude"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375828, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375828, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000007],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Geodude"]],
                locationId=FRIENDSHIP_ITEMS["Geodude"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375828, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000008],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Geodude"]],
                locationId=OverworldPokemonLocationIds.GEODUDE_MAGMA.value
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Torchic"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375ad0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375ad0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000002],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Torchic"]],
                locationId=FRIENDSHIP_ITEMS["Torchic"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375ad0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000009],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Torchic"]],
                locationId=OverworldPokemonLocationIds.TORCHIC_MAGMA.value
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Machamp"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803758c8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803758c8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000000d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Machamp"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Machamp Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Machamp"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x803758c8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000002f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Machamp"]],
                locationId=OverworldPokemonLocationIds.MACHAMP_CAVERN_BATTLE.value
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Meowth"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375af8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375af8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000001b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Meowth"]],
                locationId=FRIENDSHIP_ITEMS["Meowth"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375af8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x00000002],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Meowth"]],
                locationId=OverworldPokemonLocationIds.MEOWTH_HAUNTED.value
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Zubat"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375864, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375864, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000020, 0x00000021, 0x00000022, 0x00000023, 0x00000024, 0x00000025, 0x00000026,
                             0x00000027, 0x0000001f, 0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Zubat"]],
                locationId=FRIENDSHIP_ITEMS["Zubat"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Cranidos"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803758a0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803758a0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000002d, 0x0000000b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Cranidos"]],
                locationId=FRIENDSHIP_ITEMS["Cranidos"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Golbat"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375878, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375878, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000002a, 0x0000002b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Golbat"]],
                locationId=FRIENDSHIP_ITEMS["Golbat"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Scizor"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375468, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375468, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000001c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Scizor"]],
                locationId=FRIENDSHIP_ITEMS["Scizor"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Mawile"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375850, memory_range=MemoryRange.BYTE, value=0x80),
        # locations=[ # story based
        #     PokemonLocation(
        #         location=MemoryAddress(base_address=0x80375850, offset=0x0001, value=0x80,
        #                                memory_range=MemoryRange.BYTE),
        #         zone_id=Cavern_zone_stage_id,
        #         pokemon_ids=[0x00000008],
        #         friendship_items_to_block=[FRIENDSHIP_ITEMS["Mawile"]],
        #         locationId=FRIENDSHIP_ITEMS["Mawile"]
        #     )
        # ],
    ),
    FRIENDSHIP_ITEMS["Marowak"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803758b4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803758b4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000000c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Marowak"]],
                locationId=FRIENDSHIP_ITEMS["Marowak"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Mr. Mime"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375954, memory_range=MemoryRange.BYTE, value=0x80)
    ),
    FRIENDSHIP_ITEMS["Aron"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375f30, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375f30, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000000a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Aron"]],
                locationId=FRIENDSHIP_ITEMS["Aron"],
                is_special_exception=True
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375f30, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x0000000b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Aron"]],
                locationId=OverworldPokemonLocationIds.ARON_MAGMA.value,
                is_special_exception=True
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Dugtrio"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375f6c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375f6c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Dugtrio"]],
                locationId=FRIENDSHIP_ITEMS["Dugtrio"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Diglett"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375f44, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Gible"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037583c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037583c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000001, 0x00000030],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Gible"]],
                locationId=FRIENDSHIP_ITEMS["Gible"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Phanpy"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037588c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037588c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x000002e, 0x00000009],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Phanpy"]],
                is_special_exception=True,
                locationId=FRIENDSHIP_ITEMS["Phanpy"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Raichu"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803758f0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803758f0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x0000010],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Raichu"]],
                locationId=FRIENDSHIP_ITEMS["Raichu"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x803758f0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x0000009],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Raichu"]],
                locationId=OverworldPokemonLocationIds.RAICHU_HAUNTED.value
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Hitmonlee"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375A30, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375A30, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=cavern_zone_stage_id,
                pokemon_ids=[0x00000011],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Hitmonlee"]],
                locationId=FRIENDSHIP_ITEMS["Hitmonlee"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Bastiodon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375968, memory_range=MemoryRange.BYTE, value=0x80),
        # locations=[
        #     PokemonLocation(
        #         location=MemoryAddress(base_address=0x80375968, offset=0x0001, value=0x80,
        #                                memory_range=MemoryRange.BYTE),
        #         zone_id=Cavern_zone_stage_id,
        #         pokemon_ids=[0x],
        #         friendship_items_to_block=[FRIENDSHIP_ITEMS["Bastiodon"]],
        #         locationId=FRIENDSHIP_ITEMS["Bastiodon"]
        #     )
        # ],
    ),
    #
    # Magma Zone
    FRIENDSHIP_ITEMS["Camerupt"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803759B8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803759B8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x0000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Camerupt"]],
                locationId=FRIENDSHIP_ITEMS["Camerupt"]
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Magby"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375a6c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375a6c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x0000001, 0x0000001f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Magby"]],
                locationId=FRIENDSHIP_ITEMS["Magby"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375a6c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000020, 0x00000021],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Magby"]],
                locationId=OverworldPokemonLocationIds.MAGBY_MAGMA_BATTLE.value
            )
        ],
    ),
    FRIENDSHIP_ITEMS["Vulpix"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375b20, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375b20, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x0000029, 0x0000000c, 0x0000002a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Vulpix"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Ninetales Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Vulpix"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Ninetales"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375b34, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375b34, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Ninetales"]],
                locationId=FRIENDSHIP_ITEMS["Ninetales"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Quilava"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803759a4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803759a4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000006],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Quilava"]],
                locationId=FRIENDSHIP_ITEMS["Quilava"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Flareon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375508, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375508, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x0000000f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Flareon"]],
                locationId=FRIENDSHIP_ITEMS["Flareon"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Meditite"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375CB0, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Infernape"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375aa8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375aa8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000012],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Infernape"]],
                locationId=FRIENDSHIP_ITEMS["Infernape"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Farfetch'd"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803759cc, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803759cc, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000015],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Farfetch'd"]],
                locationId=FRIENDSHIP_ITEMS["Farfetch'd"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Magcargo"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375FF8, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Charmander"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375D28, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Ponyta"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375418, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375418, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x0000001a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Ponyta"]],
                locationId=FRIENDSHIP_ITEMS["Ponyta"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Torkoal"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037597c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037597c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000023, 0x00000028, 0x00000025, 0x00000022, 0x00000027, 0x00000024, 0x00000026,
                             0x00000005],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Torkoal"]],
                locationId=FRIENDSHIP_ITEMS["Torkoal"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Golem"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375fa8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375fa8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000013],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Golem"]],
                locationId=FRIENDSHIP_ITEMS["Golem"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Rhyperior"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375ABC, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Baltoy"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803759e0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803759e0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000004],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Baltoy"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Claydol Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Baltoy"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Claydol"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803759f4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803759f4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000007],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Claydol"]],
                locationId=FRIENDSHIP_ITEMS["Claydol"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Hitmonchan"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375a44, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375a44, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000010],
                unlock_items_to_block=[UNLOCK_ITEMS["Hitmonlee Unlock"]],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Hitmonchan"]],
                locationId=FRIENDSHIP_ITEMS["Hitmonchan"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Hitmontop"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375a58, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375a58, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=magma_zone_stage_id,
                pokemon_ids=[0x00000016],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Hitmontop"]],
                locationId=FRIENDSHIP_ITEMS["Hitmontop"]
            ),
        ],
    ),

    # Haunted Zone
    FRIENDSHIP_ITEMS["Drifloon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375f80, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375f80, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x0000000a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifloon"]],
                locationId=FRIENDSHIP_ITEMS["Drifloon"]
            ),
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375f80, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000029, 0x0000000f, 0x00000028],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Drifloon"]],
                locationId=FRIENDSHIP_ITEMS["Drifloon"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Murkrow"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375b48, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375b48, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x0000000c],
                unlock_items_to_block=[UNLOCK_ITEMS["Honchkrow Unlock"]],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Murkrow"]],
                locationId=FRIENDSHIP_ITEMS["Murkrow"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Honchkrow"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375b5c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375b5c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x00000015],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Honchkrow"]],
                locationId=FRIENDSHIP_ITEMS["Honchkrow"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Gliscor"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375b0c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375b0c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x0000000b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Gliscor"]],
                locationId=FRIENDSHIP_ITEMS["Gliscor"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Metapod"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80376084, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80376084, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x0000000e],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Metapod"]],
                locationId=FRIENDSHIP_ITEMS["Metapod"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Kakuna"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375F1C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375F1C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_stage_id,
                pokemon_ids=[0x0000000d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Kakuna"]],
                locationId=FRIENDSHIP_ITEMS["Kakuna"]
            ),
        ],
    ),

    # Haunted Zone Mansion
    FRIENDSHIP_ITEMS["Duskull"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375c4c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375c4c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000001],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Duskull"]],
                locationId=FRIENDSHIP_ITEMS["Duskull"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Sableye"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375C38, memory_range=MemoryRange.BYTE, value=0x80)
    ),
    FRIENDSHIP_ITEMS["Misdreavus"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375bd4, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375bd4, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000004],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Misdreavus"]],
                locationId=FRIENDSHIP_ITEMS["Misdreavus"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Pichu"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803758dc, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x803758dc, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x0000000a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Pichu"]],
                locationId=FRIENDSHIP_ITEMS["Pichu"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Umbreon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037551c, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037551c, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x0000000e],
                unlock_items_to_block=[UNLOCK_ITEMS["Espeon Unlock"]],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Umbreon"]],
                locationId=FRIENDSHIP_ITEMS["Umbreon"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Espeon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375530, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375530, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000013],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Espeon"]],
                locationId=FRIENDSHIP_ITEMS["Espeon"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Spinarak"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375fd0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375fd0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x0000000c],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Spinarak"]],
                locationId=FRIENDSHIP_ITEMS["Spinarak"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Abra"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375b84, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375b84, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000008],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Abra"]],
                locationId=FRIENDSHIP_ITEMS["Abra"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Riolu"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375da0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375da0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000019],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Riolu"]],
                locationId=FRIENDSHIP_ITEMS["Riolu"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Voltorb"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375bc0, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375bc0, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000003],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Voltorb"]],
                locationId=FRIENDSHIP_ITEMS["Voltorb"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Elekid"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375904, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375904, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000007],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Elekid"]],
                unlock_items_to_block=[UNLOCK_ITEMS["Electabuzz Unlock"]],
                locationId=FRIENDSHIP_ITEMS["Elekid"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Electabuzz"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375918, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375918, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x0000001b],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Electabuzz"]],
                locationId=FRIENDSHIP_ITEMS["Electabuzz"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Luxray"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375404, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375404, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000012],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Luxray"]],
                locationId=FRIENDSHIP_ITEMS["Luxray"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Stunky"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375b98, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375b98, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000002],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Stunky"]],
                locationId=FRIENDSHIP_ITEMS["Stunky"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Skuntank"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375bac, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375bac, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000010],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Skuntank"]],
                locationId=FRIENDSHIP_ITEMS["Skuntank"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Breloom"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375300, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375300, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x0000001a],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Breloom"]],
                locationId=FRIENDSHIP_ITEMS["Breloom"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Mismagius"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375be8, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375be8, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000011],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Mismagius"]],
                locationId=FRIENDSHIP_ITEMS["Mismagius"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Haunter"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375c10, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375c10, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000026, 0x00000027],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Haunter"]],
                locationId=FRIENDSHIP_ITEMS["Haunter"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Gastly"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375bfc, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375bfc, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000005, 0x0000001e, 0x00000020, 0x00000021, 0x00000022, 0x00000023,
                             0x00000024, 0x00000025, 0x0000001c, 0x0000001d, 0x0000001f],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Gastly"]],
                locationId=FRIENDSHIP_ITEMS["Gastly"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Dusknoir"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375C60, memory_range=MemoryRange.BYTE, value=0x80)
    ),
    FRIENDSHIP_ITEMS["Tangrowth"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375B70, memory_range=MemoryRange.BYTE, value=0x80)
    ),
    FRIENDSHIP_ITEMS["Electrode"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037600C, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x8037600C, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x0000000d],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Electrode"]],
                locationId=FRIENDSHIP_ITEMS["Electrode"]
            ),
        ],
    ),
    FRIENDSHIP_ITEMS["Gengar"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375c24, memory_range=MemoryRange.BYTE, value=0x80),
        locations=[
            PokemonLocation(
                location=MemoryAddress(base_address=0x80375c24, offset=0x0001, value=0x80,
                                       memory_range=MemoryRange.BYTE),
                zone_id=haunted_zone_mansion_stage_id,
                pokemon_ids=[0x00000014],
                friendship_items_to_block=[FRIENDSHIP_ITEMS["Gengar"]],
                locationId=FRIENDSHIP_ITEMS["Gengar"]
            ),
        ],
    ),
}

prisma_blocked_itemIds = []

PRISMAS = {
    PRISM_ITEM["Bulbasaur Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377E1C, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377e1c, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Bulbasaur Prisma"],
        itemId=PRISM_ITEM["Bulbasaur Prisma"],
        stage_id=bulbasaur_minigame_stage_id
    ),
    PRISM_ITEM["Venusaur Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80376DA8, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80376DA8, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Venusaur Prisma"],
        itemId=PRISM_ITEM["Venusaur Prisma"],
        stage_id=venusaur_minigame_stage_id
    ),
    PRISM_ITEM["Pelipper Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x803772B8, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x803772B8, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Pelipper Prisma"],
        itemId=PRISM_ITEM["Pelipper Prisma"],
        stage_id=pelipper_minigame_stage_id
    ),
    PRISM_ITEM["Gyarados Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377174, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377174, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Gyarados Prisma"],
        itemId=PRISM_ITEM["Gyarados Prisma"],
        stage_id=gyarados_minigame_stage_id
    ),
    PRISM_ITEM["Empoleon Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377540, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377540, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Empoleon Prisma"],
        itemId=PRISM_ITEM["Empoleon Prisma"],
        stage_id=empoleon_minigame_stage_id
    ),
    PRISM_ITEM["Bastiodon Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377684, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377684, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Bastiodon Prisma"],
        itemId=PRISM_ITEM["Bastiodon Prisma"],
        stage_id=bastidon_minigame_stage_id
    ),
    PRISM_ITEM["Rhyperior Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x803777C8, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x803777C8, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Rhyperior Prisma"],
        itemId=PRISM_ITEM["Rhyperior Prisma"],
        stage_id=rhyperior_minigame_stage_id
    ),
    PRISM_ITEM["Blaziken Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x8037790C, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x8037790C, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Blaziken Prisma"],
        itemId=PRISM_ITEM["Blaziken Prisma"],
        stage_id=blaziken_minigame_stage_id
    ),
    PRISM_ITEM["Tangrowth Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80376EEC, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80376EEC, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Tangrowth Prisma"],
        itemId=PRISM_ITEM["Tangrowth Prisma"],
        stage_id=tangrowth_minigame_stage_id
    ),
    PRISM_ITEM["Dusknoir Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377030, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377030, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Dusknoir Prisma"],
        itemId=PRISM_ITEM["Dusknoir Prisma"],
        stage_id=dusknoir_minigame_stage_id
    ),
    PRISM_ITEM["Rotom Prisma"]: PrismaItem(
        item=MemoryAddress(base_address=0x80377A50, memory_range=MemoryRange.WORD, value=0x00000003),
        location=MemoryAddress(base_address=0x80377A50, memory_range=MemoryRange.BYTE, value=0x03,
                               offset=0x7fff + 0x0003),
        locationId=PRISM_ITEM["Rotom Prisma"],
        itemId=PRISM_ITEM["Rotom Prisma"],
        stage_id=rotom_minigame_stage_id
    ),
}

BLOCKED_UNLOCKS = []

UNLOCKS: dict[int, UnlockState] = {
    # Misc
    UNLOCK_ITEMS["Drifblim Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376AD0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x40000000
        )
    ),

    # Meadow Zone Unlocks
    #
    UNLOCK_ITEMS["Tropius Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00400000
        ),
        locations=[UnlockLocation(
            locationId=UNLOCK_ITEMS["Tropius Unlock"],
            zone_id=meadow_zone_stage_id,
            location=MemoryAddress(
                base_address=0x80376ad0,
                offset=0x7FFF + 0x0001,
                memory_range=MemoryRange.BYTE,
                value=0x40
            ),
        )],
    ),

    UNLOCK_ITEMS["Pachirisu Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000008
        ),
        locations=[
            UnlockLocation(
                locationId=UNLOCK_ITEMS["Pachirisu Unlock"],
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0003,
                    memory_range=MemoryRange.BYTE,
                    value=0x08
                ),
                zone_id=meadow_zone_stage_id
            ),
            UnlockLocation(
                locationId=UNLOCK_ITEMS["Pachirisu Unlock"],
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0002,
                    memory_range=MemoryRange.BYTE,
                    value=0x40
                ),
                zone_id=meadow_zone_stage_id
            )
        ],

    ),
    UNLOCK_ITEMS["Bonsly Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376Ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00004000
        )
    ),
    UNLOCK_ITEMS["Sudowoodo Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00400000
        ),
        locations=[UnlockLocation(
            locationId=UNLOCK_ITEMS["Sudowoodo Unlock"],
            location=MemoryAddress(
                base_address=0x80376ad8,
                offset=0x7FFF + 0x0001,
                memory_range=MemoryRange.BYTE,
                value=0x40
            ),
            zone_id=meadow_zone_stage_id
        ),
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad8,
                    offset=0x7FFF + 0x0001,
                    memory_range=MemoryRange.BYTE,
                    value=0x40
                ),
                locationId=UnlockLocationIds.SUDOWOODO_CAVERN.value,
                zone_id=cavern_zone_stage_id
            )],
    ),
    UNLOCK_ITEMS["Lotad Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000100
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0002,
                    memory_range=MemoryRange.BYTE,
                    value=0x80
                ),
                locationId=UNLOCK_ITEMS["Lotad Unlock"],
                zone_id=meadow_zone_stage_id
            )
        ],

    ),
    UNLOCK_ITEMS["Shinx Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376Ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00008000
        ),
    ),
    UNLOCK_ITEMS["Scyther Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x04000000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0000,
                    memory_range=MemoryRange.BYTE,
                    value=0x04
                ),
                locationId=UNLOCK_ITEMS["Scyther Unlock"],
                zone_id=meadow_zone_stage_id
            )
        ],
    ),
    UNLOCK_ITEMS["Caterpie Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000200
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0002,
                    memory_range=MemoryRange.BYTE,
                    value=0x02
                ),
                locationId=UNLOCK_ITEMS["Caterpie Unlock"],
                is_blocked_until_location=True,
                zone_id=meadow_zone_stage_id
            )
        ],
    ),
    UNLOCK_ITEMS["Butterfree Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00200000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0001,
                    memory_range=MemoryRange.BYTE,
                    value=0x20
                ),
                locationId=UNLOCK_ITEMS["Butterfree Unlock"],
                zone_id=meadow_zone_stage_id
            )
        ],
    ),
    UNLOCK_ITEMS["Chimchar Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000040
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0003,
                    memory_range=MemoryRange.BYTE,
                    value=0x40
                ),
                locationId=UNLOCK_ITEMS["Chimchar Unlock"],
                zone_id=meadow_zone_stage_id
            )
        ],

    ),
    UNLOCK_ITEMS["Ambipom Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x01000000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad0,
                offset=0x7FFF + 0x0000,
                memory_range=MemoryRange.BYTE,
                value=0x01
            ),
            locationId=UNLOCK_ITEMS["Ambipom Unlock"],
            zone_id=meadow_zone_stage_id
        ),
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0000,
                    memory_range=MemoryRange.BYTE,
                    value=0x01
                ),
                locationId=UnlockLocationIds.AMBIPOM_HAUNTED.value,
                zone_id=haunted_zone_stage_id
            ),

        ],
    ),

    UNLOCK_ITEMS["Weedle Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000400
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad0,
                offset=0x7FFF + 0x0002,
                memory_range=MemoryRange.BYTE,
                value=0x04
            ),
            locationId=UNLOCK_ITEMS["Weedle Unlock"],
            is_blocked_until_location=True,
            zone_id=meadow_zone_stage_id
        )],
    ),
    UNLOCK_ITEMS["Shroomish Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00002000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad0,
                offset=0x7FFF + 0x0002,
                memory_range=MemoryRange.BYTE,
                value=0x20
            ),
            locationId=UNLOCK_ITEMS["Shroomish Unlock"],
            is_blocked_until_location=True,
            zone_id=meadow_zone_stage_id
        )],

    ),
    UNLOCK_ITEMS["Magikarp Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000080
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad0,
                    offset=0x7FFF + 0x0003,
                    memory_range=MemoryRange.BYTE,
                    value=0x80
                ),
                locationId=UNLOCK_ITEMS["Magikarp Unlock"],
                is_blocked_until_location=True,
                zone_id=meadow_zone_stage_id
            )
        ],
    ),
    UNLOCK_ITEMS["Bidoof Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x80000000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad0,
                offset=0x7FFF + 0x0000,
                memory_range=MemoryRange.BYTE,
                value=0x80
            ),
            locationId=UNLOCK_ITEMS["Bidoof Unlock"],
            zone_id=meadow_zone_stage_id
        )],
    ),
    UNLOCK_ITEMS["Bidoof Unlock 2"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000001
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad4,
                offset=0x7FFF + 0x0003,
                memory_range=MemoryRange.BYTE,
                value=0x01
            ),
            locationId=UNLOCK_ITEMS["Bidoof Unlock 2"],
            zone_id=meadow_zone_stage_id
        )],

    ),
    UNLOCK_ITEMS["Bidoof Unlock 3"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000002
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad4,
                offset=0x7FFF + 0x0003,
                memory_range=MemoryRange.BYTE,
                value=0x02
            ),
            locationId=UNLOCK_ITEMS["Bidoof Unlock 3"],
            zone_id=meadow_zone_stage_id
        )],

    ),
    UNLOCK_ITEMS["Bibarel Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00800000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad0,
                offset=0x7FFF + 0x0001,
                memory_range=MemoryRange.BYTE,
                value=0x80
            ),
            locationId=UNLOCK_ITEMS["Bibarel Unlock"],
            zone_id=meadow_zone_stage_id
        )],
    ),
    UNLOCK_ITEMS["Starly Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00100000
        )
    ),
    UNLOCK_ITEMS["Starly Unlock 2"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000010
        )
    ),
    UNLOCK_ITEMS["Torterra Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00080000
        ),
    ),

    # Beach Zone Unlock
    #
    UNLOCK_ITEMS["Floatzel Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x02000000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad4,
                offset=0x7FFF + 0x0000,
                memory_range=MemoryRange.BYTE,
                value=0x02
            ),
            locationId=UNLOCK_ITEMS["Floatzel Unlock"],
            zone_id=beach_zone_stage_id
        )],
    ),
    UNLOCK_ITEMS["Golduck Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x01000000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad4,
                offset=0x7FFF + 0x0000,
                memory_range=MemoryRange.BYTE,
                value=0x01
            ),
            locationId=UNLOCK_ITEMS["Golduck Unlock"],
            zone_id=beach_zone_stage_id
        )],

    ),
    UNLOCK_ITEMS["Mudkip Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00040000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad4,
                offset=0x7FFF + 0x0001,
                memory_range=MemoryRange.BYTE,
                value=0x04
            ),
            locationId=UNLOCK_ITEMS["Mudkip Unlock"],
            zone_id=beach_zone_stage_id
        )],
    ),
    UNLOCK_ITEMS["Totodile Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00020000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad4,
                offset=0x7FFF + 0x0001,
                memory_range=MemoryRange.BYTE,
                value=0x02
            ),
            locationId=UNLOCK_ITEMS["Totodile Unlock"],
            zone_id=beach_zone_stage_id
        )],

    ),
    UNLOCK_ITEMS["Krabby Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00010000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad4,
                    offset=0x7FFF + 0x0001,
                    memory_range=MemoryRange.BYTE,
                    value=0x01
                ),
                locationId=UNLOCK_ITEMS["Krabby Unlock"],
                is_blocked_until_location=True,
                zone_id=beach_zone_stage_id
            )
        ],

    ),
    UNLOCK_ITEMS["Corphish Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00080000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ad4,
                offset=0x7FFF + 0x0001,
                memory_range=MemoryRange.BYTE,
                value=0x08
            ),
            locationId=UNLOCK_ITEMS["Corphish Unlock"],
            is_blocked_until_location=True,
            zone_id=beach_zone_stage_id
        )],
    ),

    # Misc
    #
    UNLOCK_ITEMS["Pikachu Balloon"]: UnlockState(
        item=MemoryAddress(
            base_address=0x8037AEC3,
            memory_range=MemoryRange.BYTE,
            value=0x08
        )
    ),
    UNLOCK_ITEMS["Pikachu Surfboard"]: UnlockState(
        item=MemoryAddress(
            base_address=0x8037AEC3,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )
    ),
    UNLOCK_ITEMS["Pikachu Snowboard"]: UnlockState(
        item=MemoryAddress(
            base_address=0x8037AEC3,
            memory_range=MemoryRange.BYTE,
            value=0x04
        )
    ),

    UNLOCK_ITEMS["Delibird Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000200
        )
    ),
    UNLOCK_ITEMS["Squirtle Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000800
        )
    ),
    UNLOCK_ITEMS["Smoochum Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000400
        )
    ),
    UNLOCK_ITEMS["Sneasel Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000080
        )
    ),
    UNLOCK_ITEMS["Mamoswine Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00040000
        )
    ),
    UNLOCK_ITEMS["Glalie Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00800000
        )
    ),
    UNLOCK_ITEMS["Primeape Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00002000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad8,
                    offset=0x7FFF + 0x0002,
                    memory_range=MemoryRange.BYTE,
                    value=0x20
                ),
                locationId=UNLOCK_ITEMS["Primeape Unlock"],
                zone_id=ice_zone_stage_id
            )
        ],

    ),
    UNLOCK_ITEMS["Ursaring Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00004000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad8,
                    offset=0x7FFF + 0x0002,
                    memory_range=MemoryRange.BYTE,
                    value=0x40
                ),
                locationId=UNLOCK_ITEMS["Ursaring Unlock"],
                zone_id=ice_zone_stage_id
            )
        ],

    ),

    # Cavern Zone
    #
    #
    UNLOCK_ITEMS["Magnemite Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00800000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad8,
                    offset=0x7FFF + 0x0001,
                    memory_range=MemoryRange.BYTE,
                    value=0x80
                ),
                locationId=UNLOCK_ITEMS["Magnemite Unlock"],
                is_blocked_until_location=True,
                zone_id=cavern_zone_stage_id
            ),

        ]

    ),
    UNLOCK_ITEMS["Magnemite Unlock 2"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000080
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ae4,
                    offset=0x7FFF + 0x0003,
                    memory_range=MemoryRange.BYTE,
                    value=0x80
                ),
                locationId=UNLOCK_ITEMS["Magnemite Unlock 2"],
                is_blocked_until_location=True,
                zone_id=cavern_zone_stage_id
            ),

        ]

    ),
    UNLOCK_ITEMS["Magnemite Unlock 3"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000100
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ae4,
                    offset=0x7FFF + 0x0002,
                    memory_range=MemoryRange.BYTE,
                    value=0x01
                ),
                locationId=UNLOCK_ITEMS["Magnemite Unlock 3"],
                is_blocked_until_location=True,
                zone_id=cavern_zone_stage_id
            ),

        ]

    ),
    UNLOCK_ITEMS["Magnezone Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000040
        )

    ),
    UNLOCK_ITEMS["Diglett Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x02000000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ae0,
                    offset=0x7FFF,
                    memory_range=MemoryRange.BYTE,
                    value=0x02
                ),
                locationId=UNLOCK_ITEMS["Diglett Unlock"],
                is_blocked_until_location=True,
                zone_id=cavern_zone_stage_id
            ),

        ]

    ),
    UNLOCK_ITEMS["Machamp Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x01000000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376ae0,
                offset=0x7FFF + 0x0000,
                memory_range=MemoryRange.BYTE,
                value=0x10
            ),
            locationId=UNLOCK_ITEMS["Machamp Unlock"],
            zone_id=cavern_zone_stage_id
        )]

    ),
    UNLOCK_ITEMS["Phanpy Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x01000000
        )

    ),
    UNLOCK_ITEMS["Raichu Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x40000000
        )

    ),

    # Magma Zone
    #
    #
    UNLOCK_ITEMS["Infernape Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000400
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376adc,
                offset=0x7FFF + 0x0002,
                memory_range=MemoryRange.BYTE,
                value=0x04
            ),
            locationId=UNLOCK_ITEMS["Infernape Unlock"],
            zone_id=magma_zone_stage_id
        )]

    ),
    UNLOCK_ITEMS["Ninetales Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00100000
        ),
        locations=[UnlockLocation(
            location=MemoryAddress(
                base_address=0x80376adc,
                offset=0x7FFF + 0x0001,
                memory_range=MemoryRange.BYTE,
                value=0x10
            ),
            locationId=UNLOCK_ITEMS["Ninetales Unlock"],
            zone_id=magma_zone_stage_id
        )]

    ),
    UNLOCK_ITEMS["Ponyta Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x02000000
        ),

    ),
    UNLOCK_ITEMS["Torkoal Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000004
        ),

    ),
    UNLOCK_ITEMS["Golem Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000800
        ),

    ),
    UNLOCK_ITEMS["Baltoy Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x10000000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ae0,
                    offset=0x7FFF,
                    memory_range=MemoryRange.BYTE,
                    value=0x10
                ),
                locationId=UNLOCK_ITEMS["Baltoy Unlock"],
                is_blocked_until_location=True,
                zone_id=magma_zone_stage_id
            ),

        ]

    ),
    UNLOCK_ITEMS["Claydol Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000010
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376adc,
                    offset=0x7FFF + 0x0003,
                    memory_range=MemoryRange.BYTE,
                    value=0x10
                ),
                locationId=UNLOCK_ITEMS["Claydol Unlock"],
                zone_id=magma_zone_stage_id
            ),

        ]

    ),
    UNLOCK_ITEMS["Hitmonchan Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000100
        ),

    ),
    UNLOCK_ITEMS["Hitmonlee Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x80000000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ad8,
                    offset=0x7FFF + 0x0000,
                    memory_range=MemoryRange.BYTE,
                    value=0x80
                ),
                locationId=UNLOCK_ITEMS["Hitmonlee Unlock"],
                zone_id=magma_zone_stage_id
            ),

        ]

    ),

    # Haunted Zone
    UNLOCK_ITEMS["Honchkrow Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x80000000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ae0,
                    offset=0x7FFF + 0x0000,
                    memory_range=MemoryRange.BYTE,
                    value=0x80
                ),
                locationId=UNLOCK_ITEMS["Honchkrow Unlock"],
                zone_id=haunted_zone_stage_id
            ),

        ]

    ),
    UNLOCK_ITEMS["Metapod Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00020000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376adc,
                    offset=0x7FFF + 0x0001,
                    memory_range=MemoryRange.BYTE,
                    value=0x02
                ),
                locationId=UNLOCK_ITEMS["Metapod Unlock"],
                is_blocked_until_location=True,
                zone_id=haunted_zone_stage_id
            )
        ],
    ),
    UNLOCK_ITEMS["Kakuna Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00010000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376adc,
                    offset=0x7FFF + 0x0001,
                    memory_range=MemoryRange.BYTE,
                    value=0x01
                ),
                locationId=UNLOCK_ITEMS["Kakuna Unlock"],
                is_blocked_until_location=True,
                zone_id=haunted_zone_stage_id
            )
        ],
    ),

    # Haunted Zone Mansion
    UNLOCK_ITEMS["Voltorb Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00400000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ae4,
                    offset=0x7FFF + 0x0001,
                    memory_range=MemoryRange.BYTE,
                    value=0x40
                ),
                locationId=UNLOCK_ITEMS["Voltorb Unlock"],
                is_blocked_until_location=True,
                zone_id=haunted_zone_mansion_stage_id
            )
        ],
    ),
    UNLOCK_ITEMS["Elekid Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00001000
        )
    ),
    UNLOCK_ITEMS["Electabuzz Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000020
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376adc,
                    offset=0x7FFF + 0x0003,
                    memory_range=MemoryRange.BYTE,
                    value=0x20
                ),
                locationId=UNLOCK_ITEMS["Electabuzz Unlock"],
                zone_id=haunted_zone_mansion_stage_id
            )
        ],
    ),
    UNLOCK_ITEMS["Luxray Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000001
        )
    ),
    UNLOCK_ITEMS["Stunky Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000001
        )
    ),
    UNLOCK_ITEMS["Skuntank Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x40000000
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376adc,
                    offset=0x7FFF + 0x0000,
                    memory_range=MemoryRange.BYTE,
                    value=0x40
                ),
                locationId=UNLOCK_ITEMS["Skuntank Unlock"],
                zone_id=haunted_zone_mansion_stage_id
            )
        ],
    ),
    UNLOCK_ITEMS["Breloom Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00080000
        )
    ),
    UNLOCK_ITEMS["Mismagius Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x80000000
        )
    ),
    UNLOCK_ITEMS["Electrode Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000004
        )
    ),
    UNLOCK_ITEMS["Haunter Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376adc,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x10000000
        )
    ),
    UNLOCK_ITEMS["Gastly Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000002
        )
    ),
    UNLOCK_ITEMS["Gastly Unlock 2"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000040
        )
    ),
    UNLOCK_ITEMS["Gengar Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000004
        )
    ),
    UNLOCK_ITEMS["Dusknoir Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000008
        )
    ),
    UNLOCK_ITEMS["Espeon Unlock"]: UnlockState(
        item=MemoryAddress(
            base_address=0x80376ae0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000002
        ),
        locations=[
            UnlockLocation(
                location=MemoryAddress(
                    base_address=0x80376ae0,
                    offset=0x7FFF + 0x0003,
                    memory_range=MemoryRange.BYTE,
                    value=0x02
                ),
                locationId=UNLOCK_ITEMS["Espeon Unlock"],
                zone_id=haunted_zone_mansion_stage_id
            )
        ],
    ),
}

POWER_INCREMENTS = {
    "thunderbolt": {
        "increments": [0x10, 0x20, 0x40, 0x80],  # +20, +40, +80
    },
    "dash": {
        "increments": [0x01, 0x04, 0x08, 0x4000],  # +4, +8, +4000
    },
    "health": {
        "increments": [0x100, 0x200, 0x400]
    },
    "iron_tail": {
        "increments": [0x800, 0x1000, 0x2000]
    }
}

POWER_SHARED_ADDR = 0x8037AEEE

berry_item_checks = {
    BERRIES["10 Berries"]: [(0x8037AEDE, 0xa)],
    BERRIES["20 Berries"]: [(0x8037AEDE, 0x14)],
    BERRIES["50 Berries"]: [(0x8037AEDE, 0x32)],
    BERRIES["100 Berries"]: [(0x8037AEDE, 0x64)],
}

logic_adresses = [
    # clean up pokemon id
    (0x8004faa0, 0x3d808037),
    (0x8004faa4, 0x38600000),
    (0x8004faa8, 0x906CDC20),
    (0x8004faac, 0x4e800020),

    # Friendship trigger logic
    (0x80126508, 0x98030001),
    # unlock trigger logic
    (0x8018397c, 0x90047fff),
    (0x80183970, 0x38600000),
    # disable berries in friendship
    # (0x80180a3c, 0x60000000),
    # disable check is friend check for locations
    # (0x801812f8,0x60000000)
    # (0x801146f8,0x38600000),
    # (0x801812e0,0x38600000)

    # find out pokemon id
    (0x80026664, 0x3ca08037),
    (0x80026668, 0x9085dc20),
    (0x8002666c, 0x4e800020),

    # prism trigger logic
    (0x801261e0, 0x90037fff),

    # deactivate power level up
    (0x801268f4, 0x60000000)
]

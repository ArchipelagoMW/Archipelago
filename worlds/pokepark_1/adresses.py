from dataclasses import dataclass
from enum import Enum
from typing import List

from worlds.pokepark_1 import FRIENDSHIP_ITEMS, UNLOCK_ITEMS, BERRIES
from worlds.pokepark_1.items import PRISM_ITEM, POWERS, REGION_UNLOCK

driffzeppeli_address = 0x80376AE0
driffzeppeli_value = 0x40000000
pokemon_id_address = 0x8036dc20
stage_id_address = 0x8036AEF0  # word
is_in_menu_address = 0x80482F04
meadow_zone_stage_id = 0x13002E8
beach_zone_stage_id = 0x1591C24
main_menu_stage_id = 0x6FC360
main_menu2_stage_id = 0x93BEA0
main_menu3_stage_id = 0x2A080
intro_stage_id = 0x940220
treehouse_stage_id = 0x13282F8
bulbasaur_minigame_stage_id = 0x98F584
venusaur_minigame_stage_id = 0xA81938
pelipper_minigame_stage_id = 0xD92358
gyarados_minigame_stage_id = 0xC61408


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
class UnlockItem:
    item: MemoryAddress  #
    itemId: int | None = None
    location: List[MemoryAddress] | None = None
    locationId: int | None = None


@dataclass
class PrismaItem:
    item: MemoryAddress
    location: MemoryAddress
    locationId: int
    itemId: int
    stage_id: int


@dataclass
class PokemonStateInfo:
    item: MemoryAddress
    locationId: int | None = None
    zone_id: int | None = None
    pokemon_ids: List[int] | None = None
    location: MemoryAddress | None = None
    friendship_items_to_block: List[int] | None = None
    unlock_items_to_block: List[int] | None = None
    is_special_exception: bool = False


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
        location=MemoryAddress(base_address=0x80375210, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000031, 0x00000004],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Pachirisu"]],
        locationId=FRIENDSHIP_ITEMS["Pachirisu"]),
    FRIENDSHIP_ITEMS["Bulbasaur"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375490, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375490, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000001e],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Bulbasaur"]],
        locationId=FRIENDSHIP_ITEMS["Bulbasaur"]),
    FRIENDSHIP_ITEMS["Munchlax"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037529C, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x8037529C, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000002f, 0x00000005],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Munchlax"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Tropius Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Munchlax"],
        is_special_exception=True),
    FRIENDSHIP_ITEMS["Tropius"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753DC, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803753DC, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000017],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Tropius"]],
        locationId=FRIENDSHIP_ITEMS["Tropius"],
        is_special_exception=True),
    FRIENDSHIP_ITEMS["Turtwig"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751D4, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803751D4, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000002d, 0x00000002],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Turtwig"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Bonsly Unlock"], UNLOCK_ITEMS["Pachirisu Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Turtwig"]),
    FRIENDSHIP_ITEMS["Bonsly"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752C4, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803752C4, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000000f],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Bonsly"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Sudowoodo Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Bonsly"]),
    FRIENDSHIP_ITEMS["Sudowoodo"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752D8, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803752D8, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000001a],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Sudowoodo"]],
        locationId=FRIENDSHIP_ITEMS["Sudowoodo"]),
    FRIENDSHIP_ITEMS["Buneary"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037533C, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x8037533C, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000003],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Buneary"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Lotad Unlock"], UNLOCK_ITEMS["Shinx Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Buneary"]),
    FRIENDSHIP_ITEMS["Shinx"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753F0, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803753F0, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000010, 0x0000002c],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Shinx"]],
        locationId=FRIENDSHIP_ITEMS["Shinx"]),
    FRIENDSHIP_ITEMS["Mankey"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375314, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Spearow"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753C8, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803753C8, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000027, 0x00000013],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Spearow"]],
        locationId=FRIENDSHIP_ITEMS["Spearow"]),
    FRIENDSHIP_ITEMS["Croagunk"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037547C, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x8037547C, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000001d],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Croagunk"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Scyther Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Croagunk"]),
    FRIENDSHIP_ITEMS["Chatot"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80376034, memory_range=MemoryRange.BYTE, value=0x80),
    ),
    FRIENDSHIP_ITEMS["Lotad"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375224, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375224, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000021, 0x00000009, 0x00000028, 0x00000029],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Lotad"]],
        locationId=FRIENDSHIP_ITEMS["Lotad"]),
    FRIENDSHIP_ITEMS["Treecko"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751FC, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803751FC, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000006],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Treecko"]],
        locationId=FRIENDSHIP_ITEMS["Treecko"]),
    FRIENDSHIP_ITEMS["Caterpie"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375274, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375274, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000000a],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Caterpie"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Butterfree Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Caterpie"]),
    FRIENDSHIP_ITEMS["Butterfree"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375288, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375288, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000002e, 0x00000016],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Butterfree"]],
        locationId=FRIENDSHIP_ITEMS["Butterfree"]),
    FRIENDSHIP_ITEMS["Chimchar"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375A94, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375A94, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000007],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Chimchar"]],
        locationId=FRIENDSHIP_ITEMS["Chimchar"]),
    FRIENDSHIP_ITEMS["Aipom"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037542C, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x8037542C, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000025, 0x00000012],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Aipom"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Ambipom Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Aipom"]),
    FRIENDSHIP_ITEMS["Ambipom"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375440, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375440, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000019],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Ambipom"]],
        locationId=FRIENDSHIP_ITEMS["Ambipom"]),
    FRIENDSHIP_ITEMS["Weedle"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375260, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375260, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000000b],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Weedle"]],
        locationId=FRIENDSHIP_ITEMS["Weedle"]),
    FRIENDSHIP_ITEMS["Shroomish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803752EC, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803752EC, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000000e],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Shroomish"]],
        locationId=FRIENDSHIP_ITEMS["Shroomish"]),
    FRIENDSHIP_ITEMS["Magikarp"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756D4, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803756D4, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000008],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Magikarp"]],
        locationId=FRIENDSHIP_ITEMS["Magikarp"]),
    FRIENDSHIP_ITEMS["Oddish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803753A0, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803753A0, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000000d],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Oddish"]],
        locationId=FRIENDSHIP_ITEMS["Oddish"]),
    FRIENDSHIP_ITEMS["Leafeon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754CC, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803754CC, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000001C],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Leafeon"]],
        locationId=FRIENDSHIP_ITEMS["Leafeon"],
        is_special_exception=True),
    FRIENDSHIP_ITEMS["Bidoof"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375238, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375238, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000000c],
        unlock_items_to_block=[UNLOCK_ITEMS.get("Bidoof1 Unlock"), UNLOCK_ITEMS.get("Bidoof2 Unlock"),
                               UNLOCK_ITEMS.get("Bidoof3 Unlock"), UNLOCK_ITEMS.get("Bibarel Unlock")],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Bidoof"]],
        locationId=FRIENDSHIP_ITEMS["Bidoof"]),
    FRIENDSHIP_ITEMS["Starly"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375364, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375364, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000023, 0x00000024, 0x0000002a, 0x00000015, 0x00000026],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Starly"]],
        locationId=FRIENDSHIP_ITEMS["Starly"]),
    FRIENDSHIP_ITEMS["Torterra"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803751E8, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803751E8, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000014],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Torterra"]],
        locationId=FRIENDSHIP_ITEMS["Torterra"]),
    FRIENDSHIP_ITEMS["Bibarel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037524C, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x8037524C, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x00000018],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Bibarel"]],
        locationId=FRIENDSHIP_ITEMS["Bibarel"]),
    FRIENDSHIP_ITEMS["Scyther"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375454, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375454, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=meadow_zone_stage_id,
        pokemon_ids=[0x0000001b],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Scyther"]],
        locationId=FRIENDSHIP_ITEMS["Scyther"]),

    # Beach Zone Pokemon
    #
    #
    FRIENDSHIP_ITEMS["Buizel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755d0, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803755d0, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000002],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Buizel"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Floatzel Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Buizel"]),
    FRIENDSHIP_ITEMS["Psyduck"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755F8, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803755F8, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000003],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Psyduck"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Golduck Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Psyduck"]),
    FRIENDSHIP_ITEMS["Slowpoke"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755BC, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803755BC, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000004],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Slowpoke"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Mudkip Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Slowpoke"]),
    FRIENDSHIP_ITEMS["Azurill"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375558, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375558, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000005],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Azurill"]],
        unlock_items_to_block=[UNLOCK_ITEMS["Totodile Unlock"]],
        locationId=FRIENDSHIP_ITEMS["Azurill"]),
    FRIENDSHIP_ITEMS["Totodile"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375670, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375670, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x0000000c],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Totodile"]],
        locationId=FRIENDSHIP_ITEMS["Totodile"]),
    FRIENDSHIP_ITEMS["Mudkip"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037556C, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x8037556C, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x0000000d],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Mudkip"]],
        locationId=FRIENDSHIP_ITEMS["Mudkip"]),
    FRIENDSHIP_ITEMS["Pidgeotto"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375634, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375634, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000018],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Pidgeotto"]],
        locationId=FRIENDSHIP_ITEMS["Pidgeotto"]),
    FRIENDSHIP_ITEMS["Taillow"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375620, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375620, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000029,0x00000024],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Taillow"]],
        locationId=FRIENDSHIP_ITEMS["Taillow"]),
    FRIENDSHIP_ITEMS["Wingull"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756ac, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803756ac, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x0000000a, 0x0000002b,0x00000024],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Wingull"]],
        locationId=FRIENDSHIP_ITEMS["Wingull"]),
    FRIENDSHIP_ITEMS["Starly"] + 1000: PokemonStateInfo( #offset since this entry is not an item
        item=MemoryAddress(base_address=0x80375364, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375364, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000026, 0x00000008],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Starly"]],
        locationId=FRIENDSHIP_ITEMS["Starly"] + 1000),
    FRIENDSHIP_ITEMS["Staravia"]: PokemonStateInfo(  # offset since this entry is not an item
        item=MemoryAddress(base_address=0x80375378, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375378, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000017],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Staravia"]],
        locationId=FRIENDSHIP_ITEMS["Staravia"]),
    FRIENDSHIP_ITEMS["Corsola"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755A8, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803755A8, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000022,0x00000021,0x00000006],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Corsola"]],
        locationId=FRIENDSHIP_ITEMS["Corsola"]),
    FRIENDSHIP_ITEMS["Floatzel"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803755E4, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803755E4, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000016],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Floatzel"]],
        locationId=FRIENDSHIP_ITEMS["Floatzel"]),
    FRIENDSHIP_ITEMS["Vaporeon"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803754E0, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803754E0, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000014],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Vaporeon"]],
        locationId=FRIENDSHIP_ITEMS["Vaporeon"]),
    FRIENDSHIP_ITEMS["Golduck"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x8037560C, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x8037560C, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000015],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Golduck"]],
        locationId=FRIENDSHIP_ITEMS["Golduck"]),
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
        location=MemoryAddress(base_address=0x80375580, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x0000002c,0x0000002d,0x0000000b,0x00000020],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Krabby"]],
        locationId=FRIENDSHIP_ITEMS["Krabby"]),
    FRIENDSHIP_ITEMS["Wailord"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803760ac, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x803760ac, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x00000013],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Wailord"]],
        locationId=FRIENDSHIP_ITEMS["Wailord"],
    is_special_exception=True),
    FRIENDSHIP_ITEMS["Corphish"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375594, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375594, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x0000002f, 0x0000002e, 0x0000000e],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Corphish"]],
        locationId=FRIENDSHIP_ITEMS["Corphish"]),
    FRIENDSHIP_ITEMS["Gyarados"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803756E8, memory_range=MemoryRange.BYTE, value=0x80)),
    FRIENDSHIP_ITEMS["Feraligatr"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x80375684, memory_range=MemoryRange.BYTE, value=0x80),
        location=MemoryAddress(base_address=0x80375684, offset=0x0001, value=0x80, memory_range=MemoryRange.BYTE),
        zone_id=beach_zone_stage_id,
        pokemon_ids=[0x0000001b],
        friendship_items_to_block=[FRIENDSHIP_ITEMS["Feraligatr"]],
        locationId=FRIENDSHIP_ITEMS["Feraligatr"]),
    FRIENDSHIP_ITEMS["Piplup"]: PokemonStateInfo(
        item=MemoryAddress(base_address=0x803757EC, memory_range=MemoryRange.BYTE, value=0x80)),
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
}

blocked_unlock_itemIds = [UNLOCK_ITEMS["Caterpie Unlock"], UNLOCK_ITEMS["Weedle Unlock"],
                          UNLOCK_ITEMS["Shroomish Unlock"],
                          UNLOCK_ITEMS["Magikarp Unlock"]]
UNLOCKS = {
    # Meadow Zone Unlocks
    #
    UNLOCK_ITEMS["Tropius Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00400000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x40
        )],
        locationId=UNLOCK_ITEMS["Tropius Unlock"]
    ),

    UNLOCK_ITEMS["Pachirisu Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000008
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x08
        ),
            MemoryAddress(
                base_address=0x80376ad0,
                offset=0x7FFF + 0x0002,
                memory_range=MemoryRange.BYTE,
                value=0x40
            ),
        ],
        locationId=UNLOCK_ITEMS["Pachirisu Unlock"]
    ),
    UNLOCK_ITEMS["Bonsly Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376Ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00004000
        )
    ),
    UNLOCK_ITEMS["Sudowoodo Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad8,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00400000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad8,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x40
        )],
        locationId=UNLOCK_ITEMS["Sudowoodo Unlock"]
    ),
    UNLOCK_ITEMS["Lotad Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000100
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x80
        )],
        locationId=UNLOCK_ITEMS["Lotad Unlock"]
    ),
    UNLOCK_ITEMS["Shinx Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376Ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00008000
        ),
    ),
    UNLOCK_ITEMS["Scyther Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x04000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x04
        )],
        locationId=UNLOCK_ITEMS["Scyther Unlock"]
    ),
    UNLOCK_ITEMS["Caterpie Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000200
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x02
        )],
        locationId=UNLOCK_ITEMS["Caterpie Unlock"]
    ),
    UNLOCK_ITEMS["Butterfree Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00200000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x20
        )],
        locationId=UNLOCK_ITEMS["Butterfree Unlock"]
    ),
    UNLOCK_ITEMS["Chimchar Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000040
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x40
        )],
        locationId=UNLOCK_ITEMS["Chimchar Unlock"]
    ),
    UNLOCK_ITEMS["Ambipom Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x01000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )],
        locationId=UNLOCK_ITEMS["Ambipom Unlock"]
    ),
    UNLOCK_ITEMS["Weedle Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000400
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x04
        )],
        locationId=UNLOCK_ITEMS["Weedle Unlock"]
    ),
    UNLOCK_ITEMS["Shroomish Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00002000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0002,
            memory_range=MemoryRange.BYTE,
            value=0x20
        )],
        locationId=UNLOCK_ITEMS["Shroomish Unlock"]
    ),
    UNLOCK_ITEMS["Magikarp Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000080
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x80
        )],
        locationId=UNLOCK_ITEMS["Magikarp Unlock"]
    ),
    UNLOCK_ITEMS["Bidoof1 Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x80000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad0,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x80
        )],
        locationId=UNLOCK_ITEMS["Bidoof1 Unlock"]
    ),
    UNLOCK_ITEMS["Bidoof2 Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000001
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )],
        locationId=UNLOCK_ITEMS["Bidoof2 Unlock"]
    ),
    UNLOCK_ITEMS["Bidoof3 Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000002
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0003,
            memory_range=MemoryRange.BYTE,
            value=0x02
        )],
        locationId=UNLOCK_ITEMS["Bidoof3 Unlock"]
    ),
    UNLOCK_ITEMS["Bibarel Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00800000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x80
        )],
        locationId=UNLOCK_ITEMS["Bibarel Unlock"]
    ),
    UNLOCK_ITEMS["Starly Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00100000
        )
    ),
    UNLOCK_ITEMS["Starly Unlock 2"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00000010
        )
    ),
    UNLOCK_ITEMS["Torterra Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad0,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00080000
        ),

    ),

    # Beach Zone Unlock
    #
    UNLOCK_ITEMS["Floatzel Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x02000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x02
        )],
        locationId=UNLOCK_ITEMS["Floatzel Unlock"]
    ),
    UNLOCK_ITEMS["Golduck Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x01000000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0000,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )],
        locationId=UNLOCK_ITEMS["Golduck Unlock"]
    ),
    UNLOCK_ITEMS["Mudkip Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00040000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x04
        )],
        locationId=UNLOCK_ITEMS["Mudkip Unlock"]
    ),
    UNLOCK_ITEMS["Totodile Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00020000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x02
        )],
        locationId=UNLOCK_ITEMS["Totodile Unlock"]
    ),
    UNLOCK_ITEMS["Krabby Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00010000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )],
        locationId=UNLOCK_ITEMS["Krabby Unlock"]
    ),
    UNLOCK_ITEMS["Corphish Unlock"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x80376ad4,
            offset=0x10,
            memory_range=MemoryRange.WORD,
            value=0x00080000
        ),
        location=[MemoryAddress(
            base_address=0x80376ad4,
            offset=0x7FFF + 0x0001,
            memory_range=MemoryRange.BYTE,
            value=0x08
        )],
        locationId=UNLOCK_ITEMS["Corphish Unlock"]
    ),

    # Misc
    #
    UNLOCK_ITEMS["Pikachu Balloon"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x8037AEC3,
            memory_range=MemoryRange.BYTE,
            value=0x08
        )
    ),
    UNLOCK_ITEMS["Pikachu Surfboard"]: UnlockItem(
        item=MemoryAddress(
            base_address=0x8037AEC3,
            memory_range=MemoryRange.BYTE,
            value=0x01
        )
    )
}



quests_location_checks = [

    # quests
    # Meadow Zone
    (0x8037500F, 0x66, BERRIES.get("10 Berries") + 1),
    (0x8037500F, 0x6A, BERRIES.get("10 Berries") + 2),
    (0x8037500F, 0x6E, BERRIES.get("10 Berries") + 3),
    (0x8037500F, 0x72, BERRIES.get("10 Berries") + 4),

    # Beach Zone
    (0x80375011, 0x10, BERRIES.get("10 Berries") + 5),
    (0x80375011, 0x20, BERRIES.get("10 Berries") + 6),
    (0x80375011, 0x30, BERRIES.get("10 Berries") + 7),
    (0x80375011, 0x40, BERRIES.get("10 Berries") + 8),
    (0x80375011, 0x50, BERRIES.get("10 Berries") + 9),
    (0x80375011, 0x60, BERRIES.get("10 Berries") + 10),
]

# halfword
minigame_location_checks = [
    # Meadow Zone - Bulbasaur's Daring Dash Minigame
    #
    # Pikachu
    (0x80377E30, 0x0001, BERRIES.get("100 Berries") + 1),
    # Turtwig
    (0x80377EE4, 0x0001, BERRIES.get("100 Berries") + 2),
    # Munchlax
    (0x80377F20, 0x0001, BERRIES.get("100 Berries") + 3),
    # Chimchar
    (0x80377EC0, 0x0001, BERRIES.get("100 Berries") + 4),
    # Treecko
    (0x80377ECC, 0x0001, BERRIES.get("100 Berries") + 5),
    # Bibarel
    (0x80377ED8, 0x0001, BERRIES.get("100 Berries") + 6),
    # Bulbasaur
    (0x80377EF0, 0x0001, BERRIES.get("100 Berries") + 7),
    # Bidoof
    (0x80377EFC, 0x0001, BERRIES.get("100 Berries") + 8),
    # Oddish
    (0x80377F08, 0x0001, BERRIES.get("100 Berries") + 9),
    # Shroomish
    (0x80377F14, 0x0001, BERRIES.get("100 Berries") + 10),
    # Bonsly
    (0x80377F2C, 0x0001, BERRIES.get("100 Berries") + 11),
    # Lotad
    (0x80377F38, 0x0001, BERRIES.get("100 Berries") + 12),
    # Weedle
    (0x80377F44, 0x0001, BERRIES.get("100 Berries") + 13),
    # Caterpie
    (0x80377F50, 0x0001, BERRIES.get("100 Berries") + 14),
    # Magikarp
    (0x80377F5C, 0x0001, BERRIES.get("100 Berries") + 15),
    # Jolteon
    # (0x0, 0x0001, BERRIES.get("100 Berries") + 16),
    # Arcanine
    # (0x0, 0x0001, BERRIES.get("100 Berries") + 17),
    # Leafeon
    (0x80377E60, 0x0001, BERRIES.get("100 Berries") + 18),
    # Scyther
    (0x80377e6c, 0x0001, BERRIES.get("100 Berries") + 19),
    # Ponyta
    # (0x0, 0x0001, BERRIES.get("100 Berries") + 20),
    # Shinx
    (0x80377E84, 0x0001, BERRIES.get("100 Berries") + 21),
    # Eevee
    # (0x0, 0x0001, BERRIES.get("100 Berries") + 22),
    # Pachirisu
    (0x80377E9C, 0x0001, BERRIES.get("100 Berries") + 23),
    # Buneary
    (0x80377EA8, 0x0001, BERRIES.get("100 Berries") + 24),
    # Croagunk
    (0x80377EB4, 0x0001, BERRIES.get("100 Berries") + 25),

    # Pikachu
    (0x80376DBC, 0x0001, BERRIES.get("100 Berries") + 26),
    # Munchlax
    (0x80376e64, 0x0001, BERRIES.get("100 Berries") + 27),
    # Magikarp
    (0x80376e70, 0x0001, BERRIES.get("100 Berries") + 28),
    # Blaziken
    # (0x, 0x0001, BERRIES.get("100 Berries") + 29),
    # Infernape
    # (0x, 0x0001, BERRIES.get("100 Berries") + 30),
    # Lucario
    # (0x, 0x0001, BERRIES.get("100 Berries") + 31),
    # Primeape
    # (0x, 0x0001, BERRIES.get("100 Berries") + 32),
    # Tangrowth
    # (0x, 0x0001, BERRIES.get("100 Berries") + 33),
    # Ambipom
    (0x80376e10, 0x0001, BERRIES.get("100 Berries") + 34),
    # Croagunk
    (0x80376e4c, 0x0001, BERRIES.get("100 Berries") + 35),
    # Mankey
    (0x80376e1c, 0x0001, BERRIES.get("100 Berries") + 36),
    # Aipom
    (0x80376e28, 0x0001, BERRIES.get("100 Berries") + 37),
    # Chimchar
    (0x80376e34, 0x0001, BERRIES.get("100 Berries") + 38),
    # Treecko
    (0x80376e40, 0x0001, BERRIES.get("100 Berries") + 39),
    # Pachirisu
    (0x80376e58, 0x0001, BERRIES.get("100 Berries") + 40),

    # Beach Zone Pelipper's Circle Circuit
    # Pikachu
    (0x80377380, 0x0001, BERRIES.get("100 Berries") + 41),
    # Staraptor
    # (0x, 0x0001, BERRIES.get("100 Berries") + 42),
    # Togekiss
    # (0x, 0x0001, BERRIES.get("100 Berries") + 43),
    # Honchkrow
    # (0x, 0x0001, BERRIES.get("100 Berries") + 44),
    # Gliscor
    # (0x, 0x0001, BERRIES.get("100 Berries") + 45),
    # Pelipper
    (0x80377338, 0x0001, BERRIES.get("100 Berries") + 46),
    # Staravia
    (0x803772FC, 0x0001, BERRIES.get("100 Berries") + 47),
    # Pidgeotto
    (0x80377308, 0x0001, BERRIES.get("100 Berries") + 48),
    # Butterfree
    (0x80377374, 0x0001, BERRIES.get("100 Berries") + 49),
    # Tropius
    (0x80377368, 0x0001, BERRIES.get("100 Berries") + 50),
    # Murkrow
    # (0x, 0x0001, BERRIES.get("100 Berries") + 51),
    # Taillow
    (0x80377320, 0x0001, BERRIES.get("100 Berries") + 52),
    # Spearow
    (0x8037732C, 0x0001, BERRIES.get("100 Berries") + 53),
    # Starly
    (0x80377344, 0x0001, BERRIES.get("100 Berries") + 54),
    # Wingull
    (0x8037735c, 0x0001, BERRIES.get("100 Berries") + 55),

    # Beach Zone Gyarados' Aqua Dash
    # Pikachu
    (0x80377218, 0x0001, BERRIES.get("100 Berries") + 56),
    # Psyduck
    (0x80377224, 0x0001, BERRIES.get("100 Berries") + 57),
    # Azurill
    (0x80377230, 0x0001, BERRIES.get("100 Berries") + 58),
    # Slowpoke
    (0x8037723c, 0x0001, BERRIES.get("100 Berries") + 59),
    # Empoleon
    # (0x, 0x0001, BERRIES.get("100 Berries") + 60),
    # Floatzel
    (0x803771a0, 0x0001, BERRIES.get("100 Berries") + 61),
    # Feraligatr
    (0x803771ac, 0x0001, BERRIES.get("100 Berries") + 62),
    # Golduck
    (0x803771b8, 0x0001, BERRIES.get("100 Berries") + 63),
    # Vaporeon
    (0x803771c4, 0x0001, BERRIES.get("100 Berries") + 64),
    # Prinplup
    # (0x, 0x0001, BERRIES.get("100 Berries") + 65),
    # Bibarel
    (0x803771dc, 0x0001, BERRIES.get("100 Berries") + 66),
    # Buizel
    (0x803771f4, 0x0001, BERRIES.get("100 Berries") + 67),
    # Corsola
    (0x803771e8, 0x0001, BERRIES.get("100 Berries") + 68),
    # Piplup
    (0x80377200, 0x0001, BERRIES.get("100 Berries") + 69),
    # Lotad
    (0x8037720c, 0x0001, BERRIES.get("100 Berries") + 70),

]

power_item_location_checks = [
    (0x8037501c, 0x01, POWERS["Progressive Thunderbolt"] + 1, 0x0F),
    (0x8037501c, 0x02, POWERS["Progressive Thunderbolt"] + 2, 0x0F),
    (0x8037501c, 0x03, POWERS["Progressive Thunderbolt"] + 3, 0x0F),
    (0x8037501d, 0x10, POWERS["Progressive Dash"] + 1, 0xF0),
    (0x8037501d, 0x20, POWERS["Progressive Dash"] + 2, 0xF0),
    (0x8037501d, 0x30, POWERS["Progressive Dash"] + 3, 0xF0),
    (0x8037501d, 0x01, POWERS["Progressive Health"] + 1, 0x0F),
    (0x8037501d, 0x02, POWERS["Progressive Health"] + 2, 0x0F),
    (0x8037501d, 0x03, POWERS["Progressive Health"] + 3, 0x0F)
]
POWER_INCREMENTS = {
    "thunderbolt": {
        "base": 0x11,
        "increments": [0x20, 0x40, 0x80],  # +20, +40, +80
    },
    "dash": {
        "base": 0x11,
        "increments": [0x04, 0x08, 0x4000],  # +4, +8, +4000
    },
    "health": {
        "base": 0x11,
        "increments": [0x100, 0x200, 0x400]
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

    # deactivate thunderbolt level up
    (0x801268f4, 0x60000000)
]

green_zone_trigger_address = stage_id_address
green_zone_trigger_value = intro_stage_id
green_zone_states_word = [
    (0x8037500C, 0x44C60),  # set state before beach zone
    (0x80377E1C, 0x2),  # init prisma for minigame bulbasaur
    (0x80376DA8, 0x2),  # init prisma for minigame Venusaur
    (0x8037502E, 0x5840)  # skip munchlax tutorial
]
green_zone_states_byte = [
    (0x8037AEEF, 0x11),  # init thunderbolt and dash
    (0x8037AEC9, 0x37),  # init status menu
    (0x80376AF7, 0x10),  # activate Celebi
    (0x80375021, 0x20)  # skipping driffzepeli quest
]
green_zone_keep_state = [
    (0x8037501B, 0x08)  # blocking photo quest so beach zone is not unlocked
]

beach_zone_trigger_address = 0x8037500D
beach_zone_trigger_value = 0x7d0
beach_zone_states_word = [
    (0x803772B8, 0x2),  # init prisma Pelipper
    (0x80377174, 0x2)  # init prisma Gyarados
]
beach_zone_states_hword = [
    (0x8037500D, 0x870)  # world state
]
beach_zone_states_byte = [
    (0x80376af0, 0x08),  # unlock bidoof in beach zone
    (0x80375026, 0x03),  # bidoof only first bridge unlocked setup
    (0x80375010, 0x3b),  # building all bridges
]  # next stage unlock 0x80375012, 0x14

region_unlock_item_checks = {
    REGION_UNLOCK["Beach Zone Unlock"]: [(0x8037500D, 0x7d0)]
}

# bidifas event going 66 6a ... but depends on base value | maybe masking | checking bits

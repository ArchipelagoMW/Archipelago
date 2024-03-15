from typing import Dict, NamedTuple, Optional, Tuple, Union

from BaseClasses import ItemClassification

from ..enums import ZorkGrandInquisitorItems, ZorkGrandInquisitorTags


class ZorkGrandInquisitorItemData(NamedTuple):
    statemap_keys: Optional[Tuple[int, ...]]
    archipelago_id: Optional[int]
    classification: ItemClassification
    tags: Tuple[ZorkGrandInquisitorTags, ...]
    maximum_quantity: Optional[int] = 1


ITEM_OFFSET = 9758067000

item_data: Dict[ZorkGrandInquisitorItems, ZorkGrandInquisitorItemData] = {
    # Inventory Items
    ZorkGrandInquisitorItems.BROGS_BICKERING_TORCH: ZorkGrandInquisitorItemData(
        statemap_keys=(67,),  # Extinguished = 103
        archipelago_id=ITEM_OFFSET + 0,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH: ZorkGrandInquisitorItemData(
        statemap_keys=(68,),  # Extinguished = 104
        archipelago_id=ITEM_OFFSET + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.BROGS_GRUE_EGG: ZorkGrandInquisitorItemData(
        statemap_keys=(70,),  # Boiled = 71
        archipelago_id=ITEM_OFFSET + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.BROGS_PLANK: ZorkGrandInquisitorItemData(
        statemap_keys=(69,),
        archipelago_id=ITEM_OFFSET + 3,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.FLATHEADIA_FUDGE: ZorkGrandInquisitorItemData(
        statemap_keys=(54,),
        archipelago_id=ITEM_OFFSET + 4,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP: ZorkGrandInquisitorItemData(
        statemap_keys=(86,),
        archipelago_id=ITEM_OFFSET + 5,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH: ZorkGrandInquisitorItemData(
        statemap_keys=(84,),
        archipelago_id=ITEM_OFFSET + 6,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT: ZorkGrandInquisitorItemData(
        statemap_keys=(9,),
        archipelago_id=ITEM_OFFSET + 7,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN: ZorkGrandInquisitorItemData(
        statemap_keys=(16,),
        archipelago_id=ITEM_OFFSET + 8,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.HAMMER: ZorkGrandInquisitorItemData(
        statemap_keys=(23,),
        archipelago_id=ITEM_OFFSET + 9,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.HUNGUS_LARD: ZorkGrandInquisitorItemData(
        statemap_keys=(55,),
        archipelago_id=ITEM_OFFSET + 10,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.JAR_OF_HOTBUGS: ZorkGrandInquisitorItemData(
        statemap_keys=(56,),
        archipelago_id=ITEM_OFFSET + 11,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LANTERN: ZorkGrandInquisitorItemData(
        statemap_keys=(4,),
        archipelago_id=ITEM_OFFSET + 12,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER: ZorkGrandInquisitorItemData(
        statemap_keys=(88,),
        archipelago_id=ITEM_OFFSET + 13,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1: ZorkGrandInquisitorItemData(
        statemap_keys=(116,),  # With fly = 120
        archipelago_id=ITEM_OFFSET + 14,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2: ZorkGrandInquisitorItemData(
        statemap_keys=(117,),  # With fly = 121
        archipelago_id=ITEM_OFFSET + 15,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3: ZorkGrandInquisitorItemData(
        statemap_keys=(118,),  # With fly = 122
        archipelago_id=ITEM_OFFSET + 16,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4: ZorkGrandInquisitorItemData(
        statemap_keys=(119,),  # With fly = 123
        archipelago_id=ITEM_OFFSET + 17,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.MAP: ZorkGrandInquisitorItemData(
        statemap_keys=(6,),
        archipelago_id=ITEM_OFFSET + 18,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.MEAD_LIGHT: ZorkGrandInquisitorItemData(
        statemap_keys=(2,),
        archipelago_id=ITEM_OFFSET + 19,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.MOSS_OF_MAREILON: ZorkGrandInquisitorItemData(
        statemap_keys=(57,),
        archipelago_id=ITEM_OFFSET + 20,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.MUG: ZorkGrandInquisitorItemData(
        statemap_keys=(35,),
        archipelago_id=ITEM_OFFSET + 21,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.OLD_SCRATCH_CARD: ZorkGrandInquisitorItemData(
        statemap_keys=(17,),
        archipelago_id=ITEM_OFFSET + 22,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.PERMA_SUCK_MACHINE: ZorkGrandInquisitorItemData(
        statemap_keys=(36,),
        archipelago_id=ITEM_OFFSET + 23,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.PLASTIC_SIX_PACK_HOLDER: ZorkGrandInquisitorItemData(
        statemap_keys=(3,),
        archipelago_id=ITEM_OFFSET + 24,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS: ZorkGrandInquisitorItemData(
        statemap_keys=(5827,),
        archipelago_id=ITEM_OFFSET + 25,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.PROZORK_TABLET: ZorkGrandInquisitorItemData(
        statemap_keys=(65,),
        archipelago_id=ITEM_OFFSET + 26,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.QUELBEE_HONEYCOMB: ZorkGrandInquisitorItemData(
        statemap_keys=(53,),
        archipelago_id=ITEM_OFFSET + 27,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.ROPE: ZorkGrandInquisitorItemData(
        statemap_keys=(83,),
        archipelago_id=ITEM_OFFSET + 28,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS: ZorkGrandInquisitorItemData(
        statemap_keys=(101,),  # SNA = 41
        archipelago_id=ITEM_OFFSET + 29,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV: ZorkGrandInquisitorItemData(
        statemap_keys=(102,),  # VIG = 48
        archipelago_id=ITEM_OFFSET + 30,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SHOVEL: ZorkGrandInquisitorItemData(
        statemap_keys=(49,),
        archipelago_id=ITEM_OFFSET + 31,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SNAPDRAGON: ZorkGrandInquisitorItemData(
        statemap_keys=(50,),
        archipelago_id=ITEM_OFFSET + 32,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.STUDENT_ID: ZorkGrandInquisitorItemData(
        statemap_keys=(39,),
        archipelago_id=ITEM_OFFSET + 33,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SUBWAY_TOKEN: ZorkGrandInquisitorItemData(
        statemap_keys=(20,),
        archipelago_id=ITEM_OFFSET + 34,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.SWORD: ZorkGrandInquisitorItemData(
        statemap_keys=(21,),
        archipelago_id=ITEM_OFFSET + 35,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.ZIMDOR_SCROLL: ZorkGrandInquisitorItemData(
        statemap_keys=(25,),
        archipelago_id=ITEM_OFFSET + 36,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    ZorkGrandInquisitorItems.ZORK_ROCKS: ZorkGrandInquisitorItemData(
        statemap_keys=(37,),
        archipelago_id=ITEM_OFFSET + 37,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.INVENTORY_ITEM,),
    ),
    # Hotspots
    ZorkGrandInquisitorItems.HOTSPOT_666_MAILBOX: ZorkGrandInquisitorItemData(
        statemap_keys=(9116,),
        archipelago_id=ITEM_OFFSET + 100 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS: ZorkGrandInquisitorItemData(
        statemap_keys=(15434, 15436, 15438, 15440),
        archipelago_id=ITEM_OFFSET + 100 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX: ZorkGrandInquisitorItemData(
        statemap_keys=(12096,),
        archipelago_id=ITEM_OFFSET + 100 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_BLINDS: ZorkGrandInquisitorItemData(
        statemap_keys=(4799,),
        archipelago_id=ITEM_OFFSET + 100 + 3,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS: ZorkGrandInquisitorItemData(
        statemap_keys=(12691, 12692, 12693, 12694, 12695, 12696, 12697, 12698, 12699, 12700, 12701),
        archipelago_id=ITEM_OFFSET + 100 + 4,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT: ZorkGrandInquisitorItemData(
        statemap_keys=(12702,),
        archipelago_id=ITEM_OFFSET + 100 + 5,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT: ZorkGrandInquisitorItemData(
        statemap_keys=(12909,),
        archipelago_id=ITEM_OFFSET + 100 + 6,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT: ZorkGrandInquisitorItemData(
        statemap_keys=(12900,),
        archipelago_id=ITEM_OFFSET + 100 + 7,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR: ZorkGrandInquisitorItemData(
        statemap_keys=(5010,),
        archipelago_id=ITEM_OFFSET + 100 + 8,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT: ZorkGrandInquisitorItemData(
        statemap_keys=(9539,),
        archipelago_id=ITEM_OFFSET + 100 + 9,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER: ZorkGrandInquisitorItemData(
        statemap_keys=(19712,),
        archipelago_id=ITEM_OFFSET + 100 + 10,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT: ZorkGrandInquisitorItemData(
        statemap_keys=(2586,),
        archipelago_id=ITEM_OFFSET + 100 + 11,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER: ZorkGrandInquisitorItemData(
        statemap_keys=(11878,),
        archipelago_id=ITEM_OFFSET + 100 + 12,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND: ZorkGrandInquisitorItemData(
        statemap_keys=(11751,),
        archipelago_id=ITEM_OFFSET + 100 + 13,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH: ZorkGrandInquisitorItemData(
        statemap_keys=(15147, 15153),
        archipelago_id=ITEM_OFFSET + 100 + 14,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW: ZorkGrandInquisitorItemData(
        statemap_keys=(1705,),
        archipelago_id=ITEM_OFFSET + 100 + 15,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS: ZorkGrandInquisitorItemData(
        statemap_keys=(1425, 1426),
        archipelago_id=ITEM_OFFSET + 100 + 16,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE: ZorkGrandInquisitorItemData(
        statemap_keys=(13106,),
        archipelago_id=ITEM_OFFSET + 100 + 17,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS: ZorkGrandInquisitorItemData(
        statemap_keys=(13219, 13220, 13221, 13222),
        archipelago_id=ITEM_OFFSET + 100 + 18,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS: ZorkGrandInquisitorItemData(
        statemap_keys=(14327, 14332, 14337, 14342),
        archipelago_id=ITEM_OFFSET + 100 + 19,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT: ZorkGrandInquisitorItemData(
        statemap_keys=(12528,),
        archipelago_id=ITEM_OFFSET + 100 + 20,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS: ZorkGrandInquisitorItemData(
        statemap_keys=(12523, 12524, 12525),
        archipelago_id=ITEM_OFFSET + 100 + 21,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE: ZorkGrandInquisitorItemData(
        statemap_keys=(13002,),
        archipelago_id=ITEM_OFFSET + 100 + 22,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL: ZorkGrandInquisitorItemData(
        statemap_keys=(10726,),
        archipelago_id=ITEM_OFFSET + 100 + 23,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR: ZorkGrandInquisitorItemData(
        statemap_keys=(12280,),
        archipelago_id=ITEM_OFFSET + 100 + 24,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_GRASS: ZorkGrandInquisitorItemData(
        statemap_keys=(
            17694,
            17695,
            17696,
            17697,
            18200,
            17703,
            17704,
            17705,
            17710,
            17711,
            17712,
            17713,
            17714,
            17715,
            17716,
            17722,
            17723,
            17724,
            17725,
            17726,
            17727
        ),
        archipelago_id=ITEM_OFFSET + 100 + 25,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS: ZorkGrandInquisitorItemData(
        statemap_keys=(8448, 8449, 8450, 8451, 8452, 8453, 8454, 8455, 8456, 8457, 8458, 8459),
        archipelago_id=ITEM_OFFSET + 100 + 26,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER: ZorkGrandInquisitorItemData(
        statemap_keys=(8446,),
        archipelago_id=ITEM_OFFSET + 100 + 27,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HARRY: ZorkGrandInquisitorItemData(
        statemap_keys=(4260,),
        archipelago_id=ITEM_OFFSET + 100 + 28,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY: ZorkGrandInquisitorItemData(
        statemap_keys=(18026,),
        archipelago_id=ITEM_OFFSET + 100 + 29,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH: ZorkGrandInquisitorItemData(
        statemap_keys=(17623,),
        archipelago_id=ITEM_OFFSET + 100 + 30,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR: ZorkGrandInquisitorItemData(
        statemap_keys=(13140,),
        archipelago_id=ITEM_OFFSET + 100 + 31,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR: ZorkGrandInquisitorItemData(
        statemap_keys=(10441,),
        archipelago_id=ITEM_OFFSET + 100 + 32,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_LOUDSPEAKER_VOLUME_BUTTONS: ZorkGrandInquisitorItemData(
        statemap_keys=(19632, 19627),
        archipelago_id=ITEM_OFFSET + 100 + 33,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR: ZorkGrandInquisitorItemData(
        statemap_keys=(3025,),
        archipelago_id=ITEM_OFFSET + 100 + 34,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG: ZorkGrandInquisitorItemData(
        statemap_keys=(3036,),
        archipelago_id=ITEM_OFFSET + 100 + 35,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MIRROR: ZorkGrandInquisitorItemData(
        statemap_keys=(5031,),
        archipelago_id=ITEM_OFFSET + 100 + 36,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MONASTERY_VENT: ZorkGrandInquisitorItemData(
        statemap_keys=(13597,),
        archipelago_id=ITEM_OFFSET + 100 + 37,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE: ZorkGrandInquisitorItemData(
        statemap_keys=(13390,),
        archipelago_id=ITEM_OFFSET + 100 + 38,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR: ZorkGrandInquisitorItemData(
        statemap_keys=(2455, 2447),
        archipelago_id=ITEM_OFFSET + 100 + 39,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS: ZorkGrandInquisitorItemData(
        statemap_keys=(12389, 12390),
        archipelago_id=ITEM_OFFSET + 100 + 40,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE: ZorkGrandInquisitorItemData(
        statemap_keys=(4302,),
        archipelago_id=ITEM_OFFSET + 100 + 41,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE: ZorkGrandInquisitorItemData(
        statemap_keys=(16383, 16384),
        archipelago_id=ITEM_OFFSET + 100 + 42,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE: ZorkGrandInquisitorItemData(
        statemap_keys=(2769,),
        archipelago_id=ITEM_OFFSET + 100 + 43,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON: ZorkGrandInquisitorItemData(
        statemap_keys=(4149,),
        archipelago_id=ITEM_OFFSET + 100 + 44,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS: ZorkGrandInquisitorItemData(
        statemap_keys=(12584, 12585, 12586, 12587),
        archipelago_id=ITEM_OFFSET + 100 + 45,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT: ZorkGrandInquisitorItemData(
        statemap_keys=(12574,),
        archipelago_id=ITEM_OFFSET + 100 + 46,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT: ZorkGrandInquisitorItemData(
        statemap_keys=(13412,),
        archipelago_id=ITEM_OFFSET + 100 + 47,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER: ZorkGrandInquisitorItemData(
        statemap_keys=(12170,),
        archipelago_id=ITEM_OFFSET + 100 + 48,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM: ZorkGrandInquisitorItemData(
        statemap_keys=(16382,),
        archipelago_id=ITEM_OFFSET + 100 + 49,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM: ZorkGrandInquisitorItemData(
        statemap_keys=(4209,),
        archipelago_id=ITEM_OFFSET + 100 + 50,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE: ZorkGrandInquisitorItemData(
        statemap_keys=(11973,),
        archipelago_id=ITEM_OFFSET + 100 + 51,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT: ZorkGrandInquisitorItemData(
        statemap_keys=(13168,),
        archipelago_id=ITEM_OFFSET + 100 + 52,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY: ZorkGrandInquisitorItemData(
        statemap_keys=(15396,),
        archipelago_id=ITEM_OFFSET + 100 + 53,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH: ZorkGrandInquisitorItemData(
        statemap_keys=(9706,),
        archipelago_id=ITEM_OFFSET + 100 + 54,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS: ZorkGrandInquisitorItemData(
        statemap_keys=(9728, 9729, 9730),
        archipelago_id=ITEM_OFFSET + 100 + 55,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    ZorkGrandInquisitorItems.HOTSPOT_WELL: ZorkGrandInquisitorItemData(
        statemap_keys=(10314,),
        archipelago_id=ITEM_OFFSET + 100 + 56,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.HOTSPOT,),
    ),
    # Spells
    ZorkGrandInquisitorItems.SPELL_GLORF: ZorkGrandInquisitorItemData(
        statemap_keys=(202,),
        archipelago_id=ITEM_OFFSET + 200 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_GOLGATEM: ZorkGrandInquisitorItemData(
        statemap_keys=(192,),
        archipelago_id=ITEM_OFFSET + 200 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_IGRAM: ZorkGrandInquisitorItemData(
        statemap_keys=(199,),
        archipelago_id=ITEM_OFFSET + 200 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_KENDALL: ZorkGrandInquisitorItemData(
        statemap_keys=(196,),
        archipelago_id=ITEM_OFFSET + 200 + 3,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_NARWILE: ZorkGrandInquisitorItemData(
        statemap_keys=(197,),
        archipelago_id=ITEM_OFFSET + 200 + 4,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_REZROV: ZorkGrandInquisitorItemData(
        statemap_keys=(195,),
        archipelago_id=ITEM_OFFSET + 200 + 5,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_THROCK: ZorkGrandInquisitorItemData(
        statemap_keys=(200,),
        archipelago_id=ITEM_OFFSET + 200 + 6,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    ZorkGrandInquisitorItems.SPELL_VOXAM: ZorkGrandInquisitorItemData(
        statemap_keys=(191,),
        archipelago_id=ITEM_OFFSET + 200 + 7,
        classification=ItemClassification.useful,
        tags=(ZorkGrandInquisitorTags.SPELL,),
    ),
    # Subway Destinations
    ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM: ZorkGrandInquisitorItemData(
        statemap_keys=(13757, 13297, 13486, 13625),
        archipelago_id=ITEM_OFFSET + 300 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SUBWAY_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES: ZorkGrandInquisitorItemData(
        statemap_keys=(13758, 13309, 13498, 13637),
        archipelago_id=ITEM_OFFSET + 300 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SUBWAY_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY: ZorkGrandInquisitorItemData(
        statemap_keys=(13759, 13316, 13505, 13644),
        archipelago_id=ITEM_OFFSET + 300 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.SUBWAY_DESTINATION,),
    ),
    # Teleporter Destinations
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR: ZorkGrandInquisitorItemData(
        statemap_keys=(2203,),
        archipelago_id=ITEM_OFFSET + 400 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH: ZorkGrandInquisitorItemData(
        statemap_keys=(7132,),
        archipelago_id=ITEM_OFFSET + 400 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES: ZorkGrandInquisitorItemData(
        statemap_keys=(7119,),
        archipelago_id=ITEM_OFFSET + 400 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY: ZorkGrandInquisitorItemData(
        statemap_keys=(7148,),
        archipelago_id=ITEM_OFFSET + 400 + 3,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB: ZorkGrandInquisitorItemData(
        statemap_keys=(16545,),
        archipelago_id=ITEM_OFFSET + 400 + 4,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TELEPORTER_DESTINATION,),
    ),
    # Totemizer Destinations
    ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION: ZorkGrandInquisitorItemData(
        statemap_keys=(9660,),
        archipelago_id=ITEM_OFFSET + 500 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TOTEMIZER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY: ZorkGrandInquisitorItemData(
        statemap_keys=(9666,),
        archipelago_id=ITEM_OFFSET + 500 + 1,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.TOTEMIZER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL: ZorkGrandInquisitorItemData(
        statemap_keys=(9668,),
        archipelago_id=ITEM_OFFSET + 500 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TOTEMIZER_DESTINATION,),
    ),
    ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ: ZorkGrandInquisitorItemData(
        statemap_keys=(9662,),
        archipelago_id=ITEM_OFFSET + 500 + 3,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.TOTEMIZER_DESTINATION,),
    ),
    # Totems
    ZorkGrandInquisitorItems.TOTEM_BROG: ZorkGrandInquisitorItemData(
        statemap_keys=(4853,),
        archipelago_id=ITEM_OFFSET + 600 + 0,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TOTEM,),
    ),
    ZorkGrandInquisitorItems.TOTEM_GRIFF: ZorkGrandInquisitorItemData(
        statemap_keys=(4315,),
        archipelago_id=ITEM_OFFSET + 600 + 1,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TOTEM,),
    ),
    ZorkGrandInquisitorItems.TOTEM_LUCY: ZorkGrandInquisitorItemData(
        statemap_keys=(5223,),
        archipelago_id=ITEM_OFFSET + 600 + 2,
        classification=ItemClassification.progression,
        tags=(ZorkGrandInquisitorTags.TOTEM,),
    ),
    # Filler
    ZorkGrandInquisitorItems.FILLER_INQUISITION_PROPAGANDA_FLYER: ZorkGrandInquisitorItemData(
        statemap_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 0,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    ZorkGrandInquisitorItems.FILLER_UNREADABLE_SPELL_SCROLL: ZorkGrandInquisitorItemData(
        statemap_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 1,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    ZorkGrandInquisitorItems.FILLER_MAGIC_CONTRABAND: ZorkGrandInquisitorItemData(
        statemap_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 2,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    ZorkGrandInquisitorItems.FILLER_FROBOZZ_ELECTRIC_GADGET: ZorkGrandInquisitorItemData(
        statemap_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 3,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
    ZorkGrandInquisitorItems.FILLER_NONSENSICAL_INQUISITION_PAPERWORK: ZorkGrandInquisitorItemData(
        statemap_keys=None,
        archipelago_id=ITEM_OFFSET + 700 + 4,
        classification=ItemClassification.filler,
        tags=(ZorkGrandInquisitorTags.FILLER,),
        maximum_quantity=None,
    ),
}

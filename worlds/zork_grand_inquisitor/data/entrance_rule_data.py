from typing import Dict, Tuple, Union

from ..enums import ZorkGrandInquisitorEvents, ZorkGrandInquisitorItems, ZorkGrandInquisitorRegions


entrance_rule_data: Dict[
    Tuple[
        ZorkGrandInquisitorRegions,
        ZorkGrandInquisitorRegions,
    ],
    Union[
        Tuple[
            Tuple[
                Union[
                    ZorkGrandInquisitorEvents,
                    ZorkGrandInquisitorItems,
                    ZorkGrandInquisitorRegions,
                ],
                ...,
            ],
            ...,
        ],
        None,
    ],
] = {
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.DM_LAIR): (
        (
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE,
        ),
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
        ),
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.GUE_TECH): (
        (
            ZorkGrandInquisitorItems.SPELL_REZROV,
            ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR,
        ),
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH,
        ),
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
        ),
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.PORT_FOOZLE): None,
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB,
        ),
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS): (
        (
            ZorkGrandInquisitorItems.SUBWAY_TOKEN,
            ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT,
        ),
    ),
    (ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
        ),
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.CROSSROADS): None,
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR): (
        (
            ZorkGrandInquisitorEvents.DOOR_SMOKED_CIGAR,
            ZorkGrandInquisitorEvents.DOOR_DRANK_MEAD,
        ),
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH,
        ),
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
        ),
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB,
        ),
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
        ),
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR, ZorkGrandInquisitorRegions.DM_LAIR): None,
    (ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR, ZorkGrandInquisitorRegions.WALKING_CASTLE): (
        (
            ZorkGrandInquisitorItems.HOTSPOT_BLINDS,
            ZorkGrandInquisitorEvents.KNOWS_OBIDIL,
        ),
    ),
    (ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR, ZorkGrandInquisitorRegions.WHITE_HOUSE): (
        (
            ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD,
        ),
    ),
    (ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO, ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON): (
        (
            ZorkGrandInquisitorItems.TOTEM_GRIFF,
            ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW,
        ),
    ),
    (ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO, ZorkGrandInquisitorRegions.HADES_BEYOND_GATES): None,
    (ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON, ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO): None,
    (ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON, ZorkGrandInquisitorRegions.ENDGAME): (
        (
            ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN,
            ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS,
            ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH,
            ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4,
            ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY,
            ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS,
            ZorkGrandInquisitorRegions.WHITE_HOUSE,
            ZorkGrandInquisitorItems.TOTEM_BROG,  # Needed here since White House is not broken down in 2 regions
            ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_GRUE_EGG,
            ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT,
            ZorkGrandInquisitorItems.BROGS_PLANK,
            ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE,
        ),
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH, ZorkGrandInquisitorRegions.CROSSROADS): None,
    (ZorkGrandInquisitorRegions.GUE_TECH, ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY): (
        (
            ZorkGrandInquisitorItems.SPELL_IGRAM,
            ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS,
        ),
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH, ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE): (
        (ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR,),
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY, ZorkGrandInquisitorRegions.GUE_TECH): None,
    (ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): (
        (
            ZorkGrandInquisitorItems.STUDENT_ID,
            ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE,
        ),
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.CROSSROADS): (
        (ZorkGrandInquisitorItems.MAP,),
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.DM_LAIR): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
        ),
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.GUE_TECH): None,
    (ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
        ),
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB,
        ),
    ),
    (ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
        ),
    ),
    (ZorkGrandInquisitorRegions.HADES, ZorkGrandInquisitorRegions.HADES_BEYOND_GATES): (
        (
            ZorkGrandInquisitorEvents.KNOWS_SNAVIG,
            ZorkGrandInquisitorItems.TOTEM_BROG,  # Visually hiding this totem is tied to owning it; no choice
        ),
    ),
    (ZorkGrandInquisitorRegions.HADES, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,),
    ),
    (ZorkGrandInquisitorRegions.HADES_BEYOND_GATES, ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO): (
        (
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD,
        ),
    ),
    (ZorkGrandInquisitorRegions.HADES_BEYOND_GATES, ZorkGrandInquisitorRegions.HADES): None,
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.CROSSROADS): (
        (ZorkGrandInquisitorItems.MAP,),
    ),
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.DM_LAIR): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
        ),
    ),
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH,
        ),
    ),
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.HADES): (
        (
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
        ),
    ),
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB,
        ),
    ),
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS): None,
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM): (
        (ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM,),
    ),
    (ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        (ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,),
    ),
    (ZorkGrandInquisitorRegions.MENU, ZorkGrandInquisitorRegions.PORT_FOOZLE): None,
    (ZorkGrandInquisitorRegions.MONASTERY, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
        ),
    ),
    (ZorkGrandInquisitorRegions.MONASTERY, ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT): (
        (
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
        ),
    ),
    (ZorkGrandInquisitorRegions.MONASTERY, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): None,
    (ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT, ZorkGrandInquisitorRegions.MONASTERY): None,
    (ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT, ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST): (
        (
            ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER,
            ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT,
            ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorEvents.KNOWS_YASTARD,
        ),
    ),
    (ZorkGrandInquisitorRegions.PORT_FOOZLE, ZorkGrandInquisitorRegions.CROSSROADS): (
        (
            ZorkGrandInquisitorEvents.LANTERN_DALBOZ_ACCESSIBLE,
            ZorkGrandInquisitorItems.ROPE,
            ZorkGrandInquisitorItems.HOTSPOT_WELL,
        ),
    ),
    (ZorkGrandInquisitorRegions.PORT_FOOZLE, ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP): (
        (
            ZorkGrandInquisitorEvents.CIGAR_ACCESSIBLE,
            ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL,
        ),
    ),
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP, ZorkGrandInquisitorRegions.PORT_FOOZLE): None,
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST, ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT): None,
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST, ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN): (
        (
            ZorkGrandInquisitorItems.TOTEM_LUCY,
            ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR,
        ),
    ),
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN, ZorkGrandInquisitorRegions.ENDGAME): (
        (
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4,
            ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY,
            ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS,
            ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
            ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN,
            ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS,
            ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH,
            ZorkGrandInquisitorRegions.WHITE_HOUSE,
            ZorkGrandInquisitorItems.TOTEM_BROG,  # Needed here since White House is not broken down in 2 regions
            ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_GRUE_EGG,
            ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT,
            ZorkGrandInquisitorItems.BROGS_PLANK,
            ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE,
        ),
    ),
    (ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN, ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST): None,
    (ZorkGrandInquisitorRegions.SPELL_LAB, ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE): None,
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.CROSSROADS): (
        (ZorkGrandInquisitorItems.MAP,),
    ),
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.DM_LAIR): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
        ),
    ),
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH,
        ),
    ),
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY): None,
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
        ),
    ),
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.SPELL_LAB): (
        (
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE,
            ZorkGrandInquisitorEvents.DAM_DESTROYED,
            ZorkGrandInquisitorItems.SPELL_GOLGATEM,
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM,
        ),
    ),
    (ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
        ),
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS, ZorkGrandInquisitorRegions.CROSSROADS): None,
    (ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (
            ZorkGrandInquisitorItems.SPELL_KENDALL,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES,
        ),
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS, ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM): (
        (
            ZorkGrandInquisitorItems.SPELL_KENDALL,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM,
        ),
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        (
            ZorkGrandInquisitorItems.SPELL_KENDALL,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,
        ),
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES,),
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM, ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS): None,
    (ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM, ZorkGrandInquisitorRegions.SUBWAY_MONASTERY): (
        (ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,),
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.HADES_SHORE): (
        (ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES,),
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.MONASTERY): (
        (
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorEvents.ROPE_GLORFABLE,
            ZorkGrandInquisitorItems.HOTSPOT_MONASTERY_VENT,
        ),
    ),
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS): None,
    (ZorkGrandInquisitorRegions.SUBWAY_MONASTERY, ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM): (
        (ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM,),
    ),
    (ZorkGrandInquisitorRegions.WALKING_CASTLE, ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR): None,
    (ZorkGrandInquisitorRegions.WHITE_HOUSE, ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR): None,
    (ZorkGrandInquisitorRegions.WHITE_HOUSE, ZorkGrandInquisitorRegions.ENDGAME): (
        (
            ZorkGrandInquisitorItems.TOTEM_BROG,  # Needed here since White House is not broken down in 2 regions
            ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_GRUE_EGG,
            ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT,
            ZorkGrandInquisitorItems.BROGS_PLANK,
            ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE,
            ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
            ZorkGrandInquisitorItems.GRIFFS_AIR_PUMP,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_RAFT,
            ZorkGrandInquisitorItems.GRIFFS_INFLATABLE_SEA_CAPTAIN,
            ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS,
            ZorkGrandInquisitorItems.GRIFFS_DRAGON_TOOTH,
            ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_1,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_2,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_3,
            ZorkGrandInquisitorItems.LUCYS_PLAYING_CARD_4,
            ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY,
            ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS,
        ),
    ),
}

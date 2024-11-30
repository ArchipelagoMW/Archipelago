from typing import Dict, NamedTuple, Optional, Tuple

from ..enums import ZorkGrandInquisitorRegions


class ZorkGrandInquisitorRegionData(NamedTuple):
    exits: Optional[Tuple[ZorkGrandInquisitorRegions, ...]]


region_data: Dict[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegionData] = {
    ZorkGrandInquisitorRegions.CROSSROADS: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.DM_LAIR,
            ZorkGrandInquisitorRegions.GUE_TECH,
            ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
            ZorkGrandInquisitorRegions.HADES_SHORE,
            ZorkGrandInquisitorRegions.PORT_FOOZLE,
            ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
            ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
            ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        )
    ),
    ZorkGrandInquisitorRegions.DM_LAIR: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.CROSSROADS,
            ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
            ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
            ZorkGrandInquisitorRegions.HADES_SHORE,
            ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
            ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        )
    ),
    ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.DM_LAIR,
            ZorkGrandInquisitorRegions.WALKING_CASTLE,
            ZorkGrandInquisitorRegions.WHITE_HOUSE,
        )
    ),
    ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
            ZorkGrandInquisitorRegions.HADES_BEYOND_GATES,
        )
    ),
    ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
            ZorkGrandInquisitorRegions.ENDGAME,
        )
    ),
    ZorkGrandInquisitorRegions.ENDGAME: ZorkGrandInquisitorRegionData(exits=None),
    ZorkGrandInquisitorRegions.GUE_TECH: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.CROSSROADS,
            ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
            ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
        )
    ),
    ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.GUE_TECH,
            ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        )
    ),
    ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.CROSSROADS,
            ZorkGrandInquisitorRegions.DM_LAIR,
            ZorkGrandInquisitorRegions.GUE_TECH,
            ZorkGrandInquisitorRegions.HADES_SHORE,
            ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
            ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        )
    ),
    ZorkGrandInquisitorRegions.HADES: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.HADES_BEYOND_GATES,
            ZorkGrandInquisitorRegions.HADES_SHORE,
        )
    ),
    ZorkGrandInquisitorRegions.HADES_BEYOND_GATES: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
            ZorkGrandInquisitorRegions.HADES,
        )
    ),
    ZorkGrandInquisitorRegions.HADES_SHORE: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.CROSSROADS,
            ZorkGrandInquisitorRegions.DM_LAIR,
            ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
            ZorkGrandInquisitorRegions.HADES,
            ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
            ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
            ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
            ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        )
    ),
    ZorkGrandInquisitorRegions.MENU: ZorkGrandInquisitorRegionData(
        exits=(ZorkGrandInquisitorRegions.PORT_FOOZLE,)
    ),
    ZorkGrandInquisitorRegions.MONASTERY: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.HADES_SHORE,
            ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
            ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        )
    ),
    ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.MONASTERY,
            ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
        )
    ),
    ZorkGrandInquisitorRegions.PORT_FOOZLE: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.CROSSROADS,
            ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP,
        )
    ),
    ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP: ZorkGrandInquisitorRegionData(
        exits=(ZorkGrandInquisitorRegions.PORT_FOOZLE,)
    ),
    ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
            ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        )
    ),
    ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.ENDGAME,
            ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
        )
    ),
    ZorkGrandInquisitorRegions.SPELL_LAB: ZorkGrandInquisitorRegionData(
        exits=(ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,)
    ),
    ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.CROSSROADS,
            ZorkGrandInquisitorRegions.DM_LAIR,
            ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
            ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
            ZorkGrandInquisitorRegions.HADES_SHORE,
            ZorkGrandInquisitorRegions.SPELL_LAB,
            ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        )
    ),
    ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.CROSSROADS,
            ZorkGrandInquisitorRegions.HADES_SHORE,
            ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
            ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        )
    ),
    ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.HADES_SHORE,
            ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
            ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        )
    ),
    ZorkGrandInquisitorRegions.SUBWAY_MONASTERY: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.HADES_SHORE,
            ZorkGrandInquisitorRegions.MONASTERY,
            ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
            ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        )
    ),
    ZorkGrandInquisitorRegions.WALKING_CASTLE: ZorkGrandInquisitorRegionData(
        exits=(ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,)
    ),
    ZorkGrandInquisitorRegions.WHITE_HOUSE: ZorkGrandInquisitorRegionData(
        exits=(
            ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
            ZorkGrandInquisitorRegions.ENDGAME,
        )
    ),
}

from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    TOT_ENTRANCE_GOSSIP_STONE_SONG_FAIRY = "ToT Entrance Gossip Stone Fairy"
    CHAMBER_OF_SAGES = "Chamber of Sages"


def set_region_rules(world: "SohWorld") -> None:
    # ToT Entrance
    # Events
    add_events(Regions.TOT_ENTRANCE, world, [
        (EventLocations.TOT_ENTRANCE_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: call_gossip_fairy_except_suns(bundle))
    ])
    # Locations
    add_locations(Regions.TOT_ENTRANCE, world, [
        (Locations.MARKET_TOT_LEFT_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle) or (can_use(Items.SUNS_SONG, bundle) and is_adult(bundle))),
        (Locations.MARKET_TOT_LEFT_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.MARKET_TOT_LEFT_CENTER_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle) or (can_use(Items.SUNS_SONG, bundle) and is_adult(bundle))),
        (Locations.MARKET_TOT_LEFT_CENTER_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.MARKET_TOT_RIGHT_CENTER_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle) or (can_use(Items.SUNS_SONG, bundle) and is_adult(bundle))),
        (Locations.MARKET_TOT_RIGHT_CENTER_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.MARKET_TOT_RIGHT_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy_except_suns(bundle) or (can_use(Items.SUNS_SONG, bundle) and is_adult(bundle))),
        (Locations.MARKET_TOT_RIGHT_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle))
    ])
    # Connections
    connect_regions(Regions.TOT_ENTRANCE, world, [
        (Regions.MARKET, lambda bundle: True),
        (Regions.TEMPLE_OF_TIME, lambda bundle: True)
    ])

    # Temple of Time
    # Locations
    add_locations(Regions.TEMPLE_OF_TIME, world, [
        (Locations.MARKET_TOT_LIGHT_ARROW_CUTSCENE,
         lambda bundle: is_adult(bundle) and can_trigger_lacs(bundle))
    ])
    # Connections
    connect_regions(Regions.TEMPLE_OF_TIME, world, [
        (Regions.TOT_ENTRANCE, lambda bundle: True),
        (Regions.BEYOND_DOOR_OF_TIME,
         lambda bundle: world.options.door_of_time == "open" or
         (can_use(Items.SONG_OF_TIME, bundle) and
          (world.options.door_of_time == "song_only" or
           (stone_count(bundle) == 3 and has_item(Items.OCARINA_OF_TIME, bundle))))),
    ])

    # Beyond Door of Time
    # Events
    add_events(Regions.BEYOND_DOOR_OF_TIME, world, [
        (EventLocations.CHAMBER_OF_SAGES,
         Events.TIME_TRAVEL, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.BEYOND_DOOR_OF_TIME, world, [
        (Locations.GIFT_FROM_RAURU, lambda bundle: is_adult(bundle)),
        (Locations.SHEIK_AT_TEMPLE, lambda bundle: has_item(
            Items.FOREST_MEDALLION, bundle) and is_adult(bundle))
    ])
    # Connections
    connect_regions(Regions.BEYOND_DOOR_OF_TIME, world, [
        (Regions.TEMPLE_OF_TIME, lambda bundle: True),
        (Regions.MASTER_SWORD_PEDESTAL, lambda bundle: is_adult(bundle))
    ])

    # Get Master Sword
    # Locations
    add_locations(Regions.MASTER_SWORD_PEDESTAL, world, [
        (Locations.MARKET_TOT_MASTER_SWORD, lambda bundle: True),
    ])

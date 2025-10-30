from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    DESERT_COLOSSUS_FAIRY_POND_COLOSSUS = "Desert Colossus Fairy Pond Colossus"
    DESERT_COLOSSUS_FAIRY_POND_OASIS = "Desert Colossus Fairy Pond Oasis"
    DESERT_COLOSSUS_BUG_ROCK = "Desert Colossus Bug Rock"
    DESERT_COLOSSUS_BEAN_PATCH = "Desert Colossus Bean Patch"
    DESERT_COLOSSUS_DAY_NIGHT_CYCLE_CHILD = "Desert Colossus Day Night Cycle Child"
    DESERT_COLOSSUS_DAY_NIGHT_CYCLE_ADULT = "Desert Colossus Day Night Cycle Adult"


class LocalEvents(StrEnum):
    DESERT_COLOSSUS_BEAN_PLANTED = "Desert Colossus Bean Planted"


def set_region_rules(world: "SohWorld") -> None:
    # Desert Colossus
    # Events
    add_events(Regions.DESERT_COLOSSUS, world, [
        (EventLocations.DESERT_COLOSSUS_FAIRY_POND_COLOSSUS, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (EventLocations.DESERT_COLOSSUS_BUG_ROCK,
         Events.CAN_ACCESS_BUGS, lambda bundle: True),
        (EventLocations.DESERT_COLOSSUS_BEAN_PATCH, LocalEvents.DESERT_COLOSSUS_BEAN_PLANTED,
         lambda bundle: is_child(bundle) and can_use(Items.MAGIC_BEAN, bundle)),
        (EventLocations.DESERT_COLOSSUS_DAY_NIGHT_CYCLE_CHILD,
         Events.CHILD_CAN_PASS_TIME, lambda bundle: is_child(bundle)),
        (EventLocations.DESERT_COLOSSUS_DAY_NIGHT_CYCLE_ADULT,
         Events.ADULT_CAN_PASS_TIME, lambda bundle: is_adult(bundle)),
    ])
    # Locations
    add_locations(Regions.DESERT_COLOSSUS, world, [
        (Locations.COLOSSUS_FREESTANDING_POH, lambda bundle: is_adult(bundle)
         and has_item(LocalEvents.DESERT_COLOSSUS_BEAN_PLANTED, bundle)),
        (Locations.COLOSSUS_GS_BEAN_PATCH,
         lambda bundle: can_spawn_soil_skull(bundle) and can_attack(bundle)),
        (Locations.COLOSSUS_GS_TREE, lambda bundle: is_adult(bundle)
         and hookshot_or_boomerang(bundle) and can_get_nighttime_gs(bundle)),
        (Locations.COLOSSUS_GS_HILL, lambda bundle: is_adult(bundle) and ((has_item(LocalEvents.DESERT_COLOSSUS_BEAN_PLANTED, bundle) and can_attack(bundle))
         or can_use(Items.LONGSHOT, bundle) or (can_do_trick(Tricks.COLOSSUS_GS, bundle) and can_use(Items.HOOKSHOT, bundle))) and can_get_nighttime_gs(bundle)),
        (Locations.COLOSSUS_BEAN_SPROUT_FAIRY1, lambda bundle: is_child(bundle) and can_use(
            Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.COLOSSUS_BEAN_SPROUT_FAIRY2, lambda bundle: is_child(bundle) and can_use(
            Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.COLOSSUS_BEAN_SPROUT_FAIRY3, lambda bundle: is_child(bundle) and can_use(
            Items.MAGIC_BEAN, bundle) and can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.COLOSSUS_GOSSIP_STONE_FAIRY,
         lambda bundle: call_gossip_fairy(bundle)),
        (Locations.COLOSSUS_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle))

    ])
    # Connections
    connect_regions(Regions.DESERT_COLOSSUS, world, [
        (Regions.DESERT_COLOSSUS_OASIS, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle) and (
            has_item(Items.BRONZE_SCALE, bundle) or can_use(Items.IRON_BOOTS, bundle))),
        (Regions.COLOSSUS_GREAT_FAIRY_FOUNTAIN,
         lambda bundle: has_explosives(bundle)),
        (Regions.SPIRIT_TEMPLE_ENTRYWAY, lambda bundle: True),
        (Regions.WASTELAND_NEAR_COLOSSUS, lambda bundle: True),
        (Regions.COLOSSUS_GROTTO, lambda bundle: can_use(
            Items.SILVER_GAUNTLETS, bundle))
    ])

    # Desert Colossus Oasis
    # Events
    add_events(Regions.DESERT_COLOSSUS_OASIS, world, [
        (EventLocations.DESERT_COLOSSUS_FAIRY_POND_OASIS,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.DESERT_COLOSSUS_OASIS, world, [
        (Locations.COLOSSUS_OASIS_FAIRY1, lambda bundle: True),
        (Locations.COLOSSUS_OASIS_FAIRY2, lambda bundle: True),
        (Locations.COLOSSUS_OASIS_FAIRY3, lambda bundle: True),
        (Locations.COLOSSUS_OASIS_FAIRY4, lambda bundle: True),
        (Locations.COLOSSUS_OASIS_FAIRY5, lambda bundle: True),
        (Locations.COLOSSUS_OASIS_FAIRY6, lambda bundle: True),
        (Locations.COLOSSUS_OASIS_FAIRY7, lambda bundle: True),
        (Locations.COLOSSUS_OASIS_FAIRY8, lambda bundle: True)

    ])
    # Connections
    connect_regions(Regions.DESERT_COLOSSUS_OASIS, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: True)
    ])

    # Desert Colossus Outside Temple
    # Locations
    add_locations(Regions.DESERT_COLOSSUS_OUTSIDE_TEMPLE, world, [
        (Locations.SHEIK_AT_COLOSSUS, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.DESERT_COLOSSUS_OUTSIDE_TEMPLE, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: True)
    ])

    # Desert Colossus Great Fairy Fountain
    # Locations
    add_locations(Regions.COLOSSUS_GREAT_FAIRY_FOUNTAIN, world, [
        (Locations.COLOSSUS_GREAT_FAIRY_REWARD,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Connections
    connect_regions(Regions.COLOSSUS_GREAT_FAIRY_FOUNTAIN, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: True)
    ])

    # Desert Colossus Great Fairy Fountain
    # Locations
    add_locations(Regions.COLOSSUS_GROTTO, world, [
        (Locations.COLOSSUS_DEKU_SCRUB_GROTTO_REAR,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.COLOSSUS_DEKU_SCRUB_GROTTO_FRONT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.COLOSSUS_DEKU_SCRUB_GROTTO_BEEHIVE,
         lambda bundle: can_break_upper_beehives(bundle)),
    ])
    # Connections
    connect_regions(Regions.COLOSSUS_GROTTO, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: True)
    ])

from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    LLR_TALON_RACE = "LLR Talon Race"
    LLR_TIME_TRIAL = "LLR Time Trial"


def set_region_rules(world: "SohWorld") -> None:
    # Lon Lon Ranch
    # Events
    add_events(Regions.LON_LON_RANCH, world, [
        (EventLocations.LLR_TALON_RACE, Events.FREED_EPONA, lambda bundle: (has_item(Items.CHILD_WALLET, bundle)
         or world.options.skip_epona_race.value == 1) and can_play_song(Items.EPONAS_SONG, bundle) and is_adult(bundle) and at_day(bundle)),
        (EventLocations.LLR_TIME_TRIAL, Events.GOTTEN_LINKS_COW, lambda bundle: has_item(Items.CHILD_WALLET,
         bundle) and can_play_song(Items.EPONAS_SONG, bundle) and is_adult(bundle) and at_day(bundle)),
    ])
    # Locations
    add_locations(Regions.LON_LON_RANCH, world, [
        (Locations.SONG_FROM_MALON, lambda bundle: is_child(bundle) and has_item(
            Items.ZELDAS_LETTER, bundle) and has_item(Items.FAIRY_OCARINA, bundle) and at_day(bundle)),
        (Locations.LLR_GS_TREE, lambda bundle: is_child(
            bundle) and can_bonk_trees(bundle)),
        (Locations.LLR_GS_RAIN_SHED, lambda bundle: is_child(
            bundle) and can_get_nighttime_gs(bundle)),
        (Locations.LLR_GS_HOUSE_WINDOW, lambda bundle: is_child(bundle)
         and hookshot_or_boomerang(bundle) and can_get_nighttime_gs(bundle)),
        (Locations.LLR_GS_BACK_WALL, lambda bundle: is_child(bundle)
         and hookshot_or_boomerang(bundle) and can_get_nighttime_gs(bundle)),
        (Locations.LLR_FRONT_POT1, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.LLR_FRONT_POT2, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.LLR_FRONT_POT3, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.LLR_FRONT_POT4, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.LLR_RAIN_SHED_POT1, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.LLR_RAIN_SHED_POT2, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.LLR_RAIN_SHED_POT3, lambda bundle: is_child(
            bundle) and can_break_pots(bundle)),
        (Locations.LLR_NEAR_TREE_CRATE, lambda bundle: is_child(
            bundle) and can_break_crates(bundle)),
        (Locations.LLR_TREE, lambda bundle: is_child(
            bundle) and can_bonk_trees(bundle)),
    ])
    # Connections
    connect_regions(Regions.LON_LON_RANCH, world, [
        (Regions.HYRULE_FIELD, lambda bundle: True),
        (Regions.LLR_TALONS_HOUSE, lambda bundle: can_open_overworld_door(
            Items.TALONS_HOUSE_KEY, bundle)),
        (Regions.LLR_STABLES, lambda bundle: can_open_overworld_door(
            Items.STABLES_KEY, bundle)),
        (Regions.LLR_TOWER, lambda bundle: can_open_overworld_door(
            Items.BACK_TOWER_KEY, bundle)),
        (Regions.LLR_GROTTO, lambda bundle: is_child(bundle)),
    ])

    # LLR Talons House
    # Locations
    add_locations(Regions.LLR_TALONS_HOUSE, world, [
        (Locations.LLR_TALONS_CHICKENS, lambda bundle: has_item(Items.CHILD_WALLET, bundle)
         and is_child(bundle) and at_day(bundle) and has_item(Items.ZELDAS_LETTER, bundle)),
        (Locations.LLR_TALONS_HOUSE_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.LLR_TALONS_HOUSE_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.LLR_TALONS_HOUSE_POT3, lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.LLR_TALONS_HOUSE, world, [
        (Regions.LON_LON_RANCH, lambda bundle: True)
    ])

    # LLR Stables
    # Locations
    add_locations(Regions.LLR_STABLES, world, [
        (Locations.LLR_STABLES_LEFT_COW,
         lambda bundle: can_play_song(Items.EPONAS_SONG, bundle)),
        (Locations.LLR_STABLES_RIGHT_COW,
         lambda bundle: can_play_song(Items.EPONAS_SONG, bundle)),
    ])
    # Connections
    connect_regions(Regions.LLR_STABLES, world, [
        (Regions.LON_LON_RANCH, lambda bundle: True)
    ])

    # LLR Tower
    # Locations
    add_locations(Regions.LLR_TOWER, world, [
        (Locations.LLR_FREESTANDING_POH, lambda bundle: is_child(bundle)),
        (Locations.LLR_TOWER_LEFT_COW,
         lambda bundle: can_play_song(Items.EPONAS_SONG, bundle)),
        (Locations.LLR_TOWER_RIGHT_COW,
         lambda bundle: can_play_song(Items.EPONAS_SONG, bundle)),
    ])
    # Connections
    connect_regions(Regions.LLR_TOWER, world, [
        (Regions.LON_LON_RANCH, lambda bundle: True)
    ])

    # LLR Grotto
    # Locations
    add_locations(Regions.LLR_GROTTO, world, [
        (Locations.LLR_DEKU_SCRUB_GROTTO_LEFT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.LLR_DEKU_SCRUB_GROTTO_RIGHT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.LLR_DEKU_SCRUB_GROTTO_CENTER,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.LLR_DEKU_SCRUB_GROTTO_BEEHIVE,
         lambda bundle: can_break_upper_beehives(bundle)),
    ])
    # Connections
    connect_regions(Regions.LLR_GROTTO, world, [
        (Regions.LON_LON_RANCH, lambda bundle: True)
    ])

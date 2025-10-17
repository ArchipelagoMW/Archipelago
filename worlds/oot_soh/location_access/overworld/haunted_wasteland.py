from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    WASTELAND_FAIRY_POT = "Wasteland Fairy Pot"
    WASTELAND_NUT_POT = "Wasteland Nut Pot"
    WASTELAND_CARPET_SALESMAN_STORE = "Wasteland Carpet Salesman Store"


def set_region_rules(world: "SohWorld") -> None:
    # Haunted Wasteland Near Fortress
    # Locations
    add_locations(Regions.WASTELAND_NEAR_FORTRESS, world, [
        (Locations.WASTELAND_BEFORE_QUICKSAND_CRATE,
         lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.WASTELAND_NEAR_FORTRESS, world, [
        (Regions.GF_OUTSIDE_GATE, lambda bundle: True),
        (Regions.HAUNTED_WASTELAND, lambda bundle: can_use_any(
            [Items.HOVER_BOOTS, Items.LONGSHOT], bundle) or can_do_trick(Tricks.HW_CROSSING, bundle))
    ])

    # Haunted Wasteland
    # Events
    add_events(Regions.HAUNTED_WASTELAND, world, [
        (EventLocations.WASTELAND_FAIRY_POT,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True),
        (EventLocations.WASTELAND_NUT_POT, Events.CAN_FARM_NUTS, lambda bundle: True)
    ])
    if world.options.shuffle_merchants.value == 0 or world.options.shuffle_merchants.value == 1:
        add_events(Regions.HAUNTED_WASTELAND, world, [
            (EventLocations.WASTELAND_CARPET_SALESMAN_STORE, Events.CARPET_MERCHANT, lambda bundle: has_item(
                Items.ADULT_WALLET, bundle) and (can_jump_slash(bundle) or can_use(Items.HOVER_BOOTS, bundle)))
        ])
    # Locations
    add_locations(Regions.HAUNTED_WASTELAND, world, [
        (Locations.WASTELAND_CHEST, lambda bundle: has_fire_source(bundle)),
        (Locations.WASTELAND_CARPET_SALESMAN, lambda bundle: has_item(Items.ADULT_WALLET,
         bundle) and (can_jump_slash(bundle) or can_use(Items.HOVER_BOOTS, bundle))),
        (Locations.WASTELAND_GS, lambda bundle: hookshot_or_boomerang(bundle) or (
            is_adult(bundle) and can_ground_jump(bundle) and can_jump_slash(bundle))),
        (Locations.WASTELAND_NEAR_GS_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.WASTELAND_NEAR_GS_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.WASTELAND_NEAR_GS_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.WASTELAND_NEAR_GS_POT4, lambda bundle: can_break_pots(bundle)),
        (Locations.WASTELAND_AFTER_QUICKSAND_CRATE1,
         lambda bundle: can_break_crates(bundle)),
        (Locations.WASTELAND_AFTER_QUICKSAND_CRATE2,
         lambda bundle: can_break_crates(bundle)),
        (Locations.WASTELAND_AFTER_QUICKSAND_CRATE3,
         lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.HAUNTED_WASTELAND, world, [
        (Regions.WASTELAND_NEAR_COLOSSUS, lambda bundle: can_do_trick(
            Tricks.LENS_HW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)),
        (Regions.WASTELAND_NEAR_FORTRESS, lambda bundle: can_use_any(
            [Items.HOVER_BOOTS, Items.LONGSHOT], bundle) or can_do_trick(Tricks.HW_CROSSING, bundle))
    ])

    # Haunted Wasteland Near Colossus
    # Locations
    add_locations(Regions.WASTELAND_NEAR_COLOSSUS, world, [
        (Locations.WASTELAND_NEAR_COLOSSUS_CRATE,
         lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.WASTELAND_NEAR_COLOSSUS, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: True),
        (Regions.HAUNTED_WASTELAND, lambda bundle: can_do_trick(
            Tricks.HW_REVERSE, bundle))
    ])

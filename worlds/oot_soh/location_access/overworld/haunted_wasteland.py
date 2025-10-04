from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld

class EventLocations(str, Enum):
    HAUNTED_WATELAND_FAIRY_POT = "Haunted Wasteland Fairy Pot"
    HAUNTED_WATELAND_NUT_POT = "Haunted Wasteland Nut Pot"
    HAUNTED_WATELAND_CARPET_MERCHANT = "Haunted Wasteland Carpet Merchant"


class LocalEvents(str, Enum):
    CAN_BUY_FROM_CARPET_MERCHANT = "Can Buy From Carpet Merchant"

def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
    ## Haunted Wasteland Near Fortress
    # Locations
    add_locations(Regions.WASTELAND_NEAR_FORTRESS, world, [
        (Locations.WASTELAND_BEFORE_QUICKSAND_CRATE, lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.WASTELAND_NEAR_FORTRESS, world, [
        (Regions.GF_OUTSIDE_GATE, lambda bundle: True),
        (Regions.HAUNTED_WASTELAND, lambda bundle: can_use_any([Items.HOVER_BOOTS, Items.LONGSHOT], bundle) or can_do_trick(Tricks.HW_CROSSING, bundle))
    ])

    ## Haunted Wasteland
    # Events
    add_events(Regions.HAUNTED_WASTELAND, world, [
        (EventLocations.HAUNTED_WATELAND_FAIRY_POT, Events.CAN_ACCESS_FAIRIES, lambda bundle: True),
        (EventLocations.HAUNTED_WATELAND_NUT_POT, Events.CAN_FARM_NUTS, lambda bundle: True),
        (EventLocations.HAUNTED_WATELAND_CARPET_MERCHANT, LocalEvents.CAN_BUY_FROM_CARPET_MERCHANT, lambda bundle: has_item(Items.ADULT_WALLET, bundle) and True and (can_jump_slash(bundle) or can_use(Items.HOVER_BOOTS, bundle))) # TODO replace true with CanBuyAnother() equivilent
    ])
    # Locations
    add_locations(Regions.HAUNTED_WASTELAND, world, [
        (Locations.WASTELAND_CHEST, lambda bundle: can_break_crates(bundle)),
        (Locations.WASTELAND_CARPET_SALESMAN, lambda bundle: can_break_crates(bundle)),
        (Locations.WASTELAND_GS, lambda bundle: can_break_crates(bundle)),
        (Locations.WASTELAND_NEAR_GS_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.WASTELAND_NEAR_GS_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.WASTELAND_NEAR_GS_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.WASTELAND_NEAR_GS_POT4, lambda bundle: can_break_pots(bundle)),
        (Locations.WASTELAND_AFTER_QUICKSAND_CRATE1, lambda bundle: can_break_crates(bundle)),
        (Locations.WASTELAND_AFTER_QUICKSAND_CRATE2, lambda bundle: can_break_crates(bundle)),
        (Locations.WASTELAND_AFTER_QUICKSAND_CRATE3, lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.HAUNTED_WASTELAND, world, [
        (Regions.WASTELAND_NEAR_COLOSSUS, lambda bundle: can_do_trick(Tricks.LENS_HW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)),
        (Regions.WASTELAND_NEAR_FORTRESS, lambda bundle: can_use_any([Items.HOVER_BOOTS, Items.LONGSHOT], bundle) or can_do_trick(Tricks.HW_CROSSING, bundle))
    ])

    ## Haunted Wasteland
    # Locations
    add_locations(Regions.HAUNTED_WASTELAND, world, [
        (Locations.WASTELAND_NEAR_COLOSSUS_CRATE, lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.HAUNTED_WASTELAND, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: True),
        (Regions.HAUNTED_WASTELAND, lambda bundle: can_do_trick(Tricks.HW_REVERSE, bundle) or False)
    ])
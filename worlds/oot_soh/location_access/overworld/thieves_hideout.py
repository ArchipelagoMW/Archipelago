from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventsLocations(StrEnum):
    TH_1_TORCH_CARPENTER_CELL = "TH 1 Torch Carpenter Cell"
    TH_DOUBLE_CELL_CARPENTER_CELL = "TH Double Cell Carpenter Cell"
    TH_DEAD_END_CARPENTER_CELL = "TH Dead End Carpenter Cell"
    TH_STEEP_SLOPE_CARPENTER_CELL = "TH Steep Slope Carpenter Cell"
    TH_RESCUED_ALL_CARPENTERS = "TH Rescued All Carpenters"


class LocalEvents(StrEnum):
    TH_1_TORCH_CELL_CARPENTER_FREED = "TH 1 Torch Cell Carpenter Freed"
    TH_DOUBLE_CELL_CARPENTER_FREED = "TH Double Cell Carpenter Freed"
    TH_DEAD_END_CELL_CARPENTER_FREED = "TH Dead End Cell Carpenter Freed"
    TH_STEEP_SLOPE_CELL_CARPENTER_FREED = "TH Steep Slope Cell Carpenter Freed"


def set_region_rules(world: "SohWorld") -> None:
    # Thieves' Hideout 1 Torch Cell
    # Events
    add_events(Regions.THIEVES_HIDEOUT_1_TORCH_CELL, world, [
        (EventsLocations.TH_1_TORCH_CARPENTER_CELL, LocalEvents.TH_1_TORCH_CELL_CARPENTER_FREED,
         lambda bundle: can_kill_enemy(bundle, Enemies.GERUDO_WARRIOR))
    ])
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_1_TORCH_CELL, world, [
        (Locations.TH_1_TORCH_CARPENTER, lambda bundle: can_kill_enemy(
            bundle, Enemies.GERUDO_WARRIOR)),
        (Locations.TH_1_TORCH_CELL_RIGHT_POT,
         lambda bundle: can_break_pots(bundle)),
        (Locations.TH_1_TORCH_CELL_MIDDLE_POT,
         lambda bundle: can_break_pots(bundle)),
        (Locations.TH_1_TORCH_CELL_LEFT_POT, lambda bundle: can_break_pots(bundle)),
        (Locations.TH_1_TORCH_CELL_CRATE, lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_1_TORCH_CELL, world, [
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True),
        (Regions.GF_NEAR_GROTTO, lambda bundle: True),
        (Regions.THIEVES_HIDEOUT_RESCUE_CARPENTERS,
         lambda bundle: True)
    ])

    # Thieves Hideout Double Cell
    # Events
    add_events(Regions.THIEVES_HIDEOUT_DOUBLE_CELL, world, [
        (EventsLocations.TH_DOUBLE_CELL_CARPENTER_CELL, LocalEvents.TH_DOUBLE_CELL_CARPENTER_FREED,
         lambda bundle: can_kill_enemy(bundle, Enemies.GERUDO_WARRIOR)),
    ])
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_DOUBLE_CELL, world, [
        (Locations.TH_DOUBLE_CELL_CARPENTER,
         lambda bundle: can_kill_enemy(bundle, Enemies.GERUDO_WARRIOR)),
        (Locations.TH_DOUBLE_CELL_RIGHT_POT, lambda bundle: can_break_pots(bundle)),
        (Locations.TH_DOUBLE_CELL_MIDDLE_POT,
         lambda bundle: can_break_pots(bundle)),
        (Locations.TH_DOUBLE_CELL_LEFT_POT, lambda bundle: can_break_pots(bundle)),
        (Locations.TH_RIGHTMOST_JAILED_POT, lambda bundle: can_break_pots(bundle)),
        (Locations.TH_RIGHT_MIDDLE_JAILED_POT,
         lambda bundle: can_break_pots(bundle)),
        (Locations.TH_LEFT_MIDDLE_JAILED_POT,
         lambda bundle: can_break_pots(bundle)),
        (Locations.TH_LEFTMOST_JAILED_POT, lambda bundle: can_break_pots(bundle)),
        (Locations.TH_DOUBLE_CELL_LEFT_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.TH_DOUBLE_CELL_RIGHT_CRATE,
         lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_DOUBLE_CELL, world, [
        (Regions.GERUDO_FORTRESS_OUTSKIRTS, lambda bundle: True),
        (Regions.GF_NEAR_GROTTO, lambda bundle: True),
        (Regions.THIEVES_HIDEOUT_RESCUE_CARPENTERS,
         lambda bundle: True)
    ])

    # Thieves Hideout Dead End Cell
    # Events
    add_events(Regions.THIEVES_HIDEOUT_DEAD_END_CELL, world, [
        (EventsLocations.TH_DEAD_END_CARPENTER_CELL, LocalEvents.TH_DEAD_END_CELL_CARPENTER_FREED,
         lambda bundle: can_kill_enemy(bundle, Enemies.GERUDO_WARRIOR))
    ])
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_DEAD_END_CELL, world, [
        (Locations.TH_DEAD_END_CARPENTER, lambda bundle: can_kill_enemy(
            bundle, Enemies.GERUDO_WARRIOR)),
        (Locations.TH_DEAD_END_CELL_CRATE, lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_DEAD_END_CELL, world, [
        (Regions.GF_BELOW_GS, lambda bundle: True),
        (Regions.THIEVES_HIDEOUT_RESCUE_CARPENTERS,
         lambda bundle: True)
    ])

    # Thieves Hideout Steep Slope Cell
    # Events
    add_events(Regions.THIEVES_HIDEOUT_STEEP_SLOPE_CELL, world, [
        (EventsLocations.TH_STEEP_SLOPE_CARPENTER_CELL, LocalEvents.TH_STEEP_SLOPE_CELL_CARPENTER_FREED,
         lambda bundle: can_kill_enemy(bundle, Enemies.GERUDO_WARRIOR))
    ])
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_STEEP_SLOPE_CELL, world, [
        (Locations.TH_STEEP_SLOPE_CARPENTER,
         lambda bundle: can_kill_enemy(bundle, Enemies.GERUDO_WARRIOR)),
        (Locations.TH_STEEP_SLOPE_RIGHT_POT, lambda bundle: can_break_pots(bundle)),
        (Locations.TH_STEEP_SLOPE_LEFT_POT, lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_STEEP_SLOPE_CELL, world, [
        (Regions.GF_ABOVE_GTG, lambda bundle: True),
        (Regions.GF_TOP_OF_LOWER_VINES, lambda bundle: True),
        (Regions.THIEVES_HIDEOUT_RESCUE_CARPENTERS,
         lambda bundle: True)
    ])

    # Thieves Hideout Rescue Carpenters
    # This is a deviation from ship logic due to the union of locations
    # Events
    add_events(Regions.THIEVES_HIDEOUT_RESCUE_CARPENTERS, world, [
        (EventsLocations.TH_RESCUED_ALL_CARPENTERS, Events.RESCUED_ALL_CARPENTERS,
         lambda bundle: (((small_keys(Items.GERUDO_FORTRESS_SMALL_KEY, 4,
                                      bundle) and world.options.fortress_carpenters.value == 0)
                          or (small_keys(Items.GERUDO_FORTRESS_SMALL_KEY, 1,
                                         bundle) and world.options.fortress_carpenters.value == 1))
                         and has_item(LocalEvents.TH_DOUBLE_CELL_CARPENTER_FREED, bundle)
                         and has_item(LocalEvents.TH_STEEP_SLOPE_CELL_CARPENTER_FREED, bundle)
                         and has_item(LocalEvents.TH_DEAD_END_CELL_CARPENTER_FREED, bundle)
                         and has_item(LocalEvents.TH_1_TORCH_CELL_CARPENTER_FREED, bundle))
         or world.options.fortress_carpenters.value == 2)
    ])
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_RESCUE_CARPENTERS, world, [
        (Locations.GF_GERUDO_MEMBERSHIP_CARD,
         lambda bundle: has_item(Events.RESCUED_ALL_CARPENTERS, bundle))
    ])

    # Thieves Hideout Kitchen Corridor
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_KITCHEN_CORRIDOR, world, [
        (Locations.TH_NEAR_KITCHEN_LEFTMOST_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.TH_NEAR_KITCHEN_MIDDLE_LEFT_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.TH_NEAR_KITCHEN_MIDDLE_RIGHT_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.TH_NEAR_KITCHEN_RIGHTMOST_CRATE,
         lambda bundle: can_break_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_KITCHEN_CORRIDOR, world, [
        (Regions.GF_NEAR_GROTTO, lambda bundle: True),
        (Regions.GF_ABOVE_GTG, lambda bundle: True),
        (Regions.THIEVES_HIDEOUT_KITCHEN_BOTTOM,
         lambda bundle: can_pass_enemy(bundle, Enemies.GERUDO_GUARD))
    ])

    # Thieves Hideout Kitchen Bottom
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_KITCHEN_BOTTOM, world, [
        (Locations.TH_KITCHEN_CRATE,
         lambda bundle: can_break_crates(bundle) and can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Locations.TH_KITCHEN_SUN_FAIRY,
         lambda bundle: can_pass_enemy(bundle, Enemies.GERUDO_GUARD) and can_use(Items.SUNS_SONG, bundle))
    ])
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_KITCHEN_BOTTOM, world, [
        (Regions.THIEVES_HIDEOUT_KITCHEN_CORRIDOR,
         lambda bundle: can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Regions.THIEVES_HIDEOUT_KITCHEN_TOP,
         lambda bundle: can_pass_enemy(bundle, Enemies.GERUDO_GUARD)),
        (Regions.THIEVES_HIDEOUT_KITCHEN_POTS,
         lambda bundle: can_break_pots(bundle) and can_pass_enemy(bundle, Enemies.GERUDO_GUARD))
    ])

    # Thieves Hideout Kitchen Top
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_KITCHEN_TOP, world, [
        (Regions.THIEVES_HIDEOUT_KITCHEN_BOTTOM, lambda bundle: True),
        (Regions.THIEVES_HIDEOUT_KITCHEN_POTS,
         lambda bundle: can_use(Items.BOOMERANG, bundle)),
        (Regions.GF_NEAR_GS,
         lambda bundle: can_pass_enemy(bundle, Enemies.GERUDO_GUARD) or can_use(Items.HOVER_BOOTS, bundle)),
        (Regions.GF_TOP_OF_LOWER_VINES,
         lambda bundle: can_pass_enemy(bundle, Enemies.GERUDO_GUARD) or can_use(Items.HOVER_BOOTS, bundle))
    ])

    # Thieves Hideout Kitchen Pots
    # This is a deviation from ship logic due to the union of locations
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_KITCHEN_POTS, world, [
        (Locations.TH_KITCHEN_POT1, lambda bundle: True),
        (Locations.TH_KITCHEN_POT2, lambda bundle: True),
    ])

    # Thieves Hideout Break Room
    # Locations
    add_locations(Regions.THIEVES_HIDEOUT_BREAK_ROOM, world, [
        (Locations.TH_BREAK_ROOM_FRONT_POT,
         lambda bundle: (can_pass_enemy(
             bundle, Enemies.BREAK_ROOM_GUARD) and can_break_pots(bundle))
         or (can_pass_enemy(bundle, Enemies.GERUDO_GUARD) and can_use(Items.BOOMERANG, bundle))),
        (Locations.TH_BREAK_ROOM_BACK_POT,
         lambda bundle: (can_pass_enemy(
             bundle, Enemies.BREAK_ROOM_GUARD) and can_break_pots(bundle))
         or (can_pass_enemy(bundle, Enemies.GERUDO_GUARD) and can_use(Items.BOOMERANG, bundle))),
        (Locations.TH_BREAK_HALLWAY_OUTER_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.TH_BREAK_HALLWAY_INNER_CRATE,
         lambda bundle: can_break_crates(bundle)),
        (Locations.TH_BREAK_ROOM_RIGHT_CRATE,
         lambda bundle: (can_pass_enemy(
             bundle, Enemies.BREAK_ROOM_GUARD) and can_break_crates(bundle))
         or (can_pass_enemy(bundle, Enemies.GERUDO_GUARD) and has_explosives(bundle)
             and can_use(Items.BOOMERANG, bundle))),
        (Locations.TH_BREAK_ROOM_LEFT_CRATE,
         lambda bundle: (can_pass_enemy(
             bundle, Enemies.BREAK_ROOM_GUARD) and can_break_crates(bundle))
         or (can_pass_enemy(bundle, Enemies.GERUDO_GUARD) and has_explosives(bundle)
             and can_use(Items.BOOMERANG, bundle))),

    ])
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_BREAK_ROOM, world, [
        (Regions.GF_BELOW_CHEST, lambda bundle: can_pass_enemy(
            bundle, Enemies.GERUDO_GUARD)),
        (Regions.THIEVES_HIDEOUT_BREAK_ROOM_CORRIDOR,
         lambda bundle: can_use(Items.HOOKSHOT, bundle))
    ])

    # Thieves Hideout Break Room Corridor
    # Connections
    connect_regions(Regions.THIEVES_HIDEOUT_BREAK_ROOM_CORRIDOR, world, [
        (Regions.THIEVES_HIDEOUT_BREAK_ROOM,
         lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.GF_ABOVE_JAIL, lambda bundle: True)
    ])

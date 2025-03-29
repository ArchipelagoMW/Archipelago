from .RegionBase import JakAndDaxterRegion
from ..Options import EnableOrbsanity
from .. import JakAndDaxterWorld
from ..Rules import can_free_scout_flies, can_fight, can_reach_orbs_level


def build_regions(level_name: str, world: JakAndDaxterWorld) -> list[JakAndDaxterRegion]:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 25)

    # You can get this scout fly by running from the blue eco vent across the temple bridge,
    # falling onto the river, collecting the 3 blue clusters, using the jump pad, and running straight to the box.
    main_area.add_fly_locations([393223])

    lurker_machine = JakAndDaxterRegion("Lurker Machine", player, multiworld, level_name, 5)
    lurker_machine.add_cell_locations([3], access_rule=lambda state: can_fight(state, player))

    # This cell and this scout fly can both be gotten with the blue eco clusters near the jump pad.
    lurker_machine.add_cell_locations([9])
    lurker_machine.add_fly_locations([131079])

    river = JakAndDaxterRegion("River", player, multiworld, level_name, 42)

    # All of these can be gotten with blue eco, hitting the dark eco boxes, or by running.
    river.add_cell_locations([5, 8])
    river.add_fly_locations([7, 196615])
    river.add_special_locations([5])
    river.add_cache_locations([10369])

    temple_exit = JakAndDaxterRegion("Temple Exit", player, multiworld, level_name, 12)

    # This fly is too far from accessible blue eco sources.
    temple_exit.add_fly_locations([262151], access_rule=lambda state: can_free_scout_flies(state, player))

    temple_exterior = JakAndDaxterRegion("Temple Exterior", player, multiworld, level_name, 10)

    # All of these can be gotten with blue eco and running.
    temple_exterior.add_cell_locations([4])
    temple_exterior.add_fly_locations([327687, 65543])
    temple_exterior.add_special_locations([4])

    temple_int_pre_blue = JakAndDaxterRegion("Temple Interior (Pre Blue Eco)", player, multiworld, level_name, 17)
    temple_int_pre_blue.add_cell_locations([2])
    temple_int_pre_blue.add_special_locations([2])

    temple_int_post_blue = JakAndDaxterRegion("Temple Interior (Post Blue Eco)", player, multiworld, level_name, 39)
    temple_int_post_blue.add_cell_locations([6], access_rule=lambda state: can_fight(state, player))

    main_area.connect(lurker_machine)               # Run and jump (tree stump platforms).
    main_area.connect(river)                        # Jump down.
    main_area.connect(temple_exit)                  # Run and jump (bridges).

    lurker_machine.connect(main_area)               # Jump down.
    lurker_machine.connect(river)                   # Jump down.
    lurker_machine.connect(temple_exterior)         # Jump down (ledge).

    river.connect(main_area)                        # Jump up (ledges near fisherman).
    river.connect(lurker_machine)                   # Jump pad (aim toward machine).
    river.connect(temple_exit)                      # Run and jump (trampolines).
    river.connect(temple_exterior)                  # Jump pad (aim toward temple door).

    temple_exit.connect(main_area)                  # Run and jump (bridges).
    temple_exit.connect(river)                      # Jump down.
    temple_exit.connect(temple_exterior)            # Run and jump (bridges, dodge spikes).

    # Requires Jungle Elevator.
    temple_exterior.connect(temple_int_pre_blue, rule=lambda state: state.has("Jungle Elevator", player))

    # Requires Blue Eco Switch.
    temple_int_pre_blue.connect(temple_int_post_blue, rule=lambda state: state.has("Blue Eco Switch", player))

    # Requires defeating the plant boss (combat).
    temple_int_post_blue.connect(temple_exit, rule=lambda state: can_fight(state, player))

    multiworld.regions.append(main_area)
    multiworld.regions.append(lurker_machine)
    multiworld.regions.append(river)
    multiworld.regions.append(temple_exit)
    multiworld.regions.append(temple_exterior)
    multiworld.regions.append(temple_int_pre_blue)
    multiworld.regions.append(temple_int_post_blue)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 150 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(3,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, bundle=bundle_index:
                                   can_reach_orbs_level(state, player, world, level, bundle))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area, temple_int_post_blue]

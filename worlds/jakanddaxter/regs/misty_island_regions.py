from .region_base import JakAndDaxterRegion
from ..options import EnableOrbsanity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import JakAndDaxterWorld
from ..rules import can_free_scout_flies, can_fight, can_reach_orbs_level


def build_regions(level_name: str, world: "JakAndDaxterWorld") -> JakAndDaxterRegion:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 9)

    muse_course = JakAndDaxterRegion("Muse Course", player, multiworld, level_name, 21)
    muse_course.add_cell_locations([23])
    muse_course.add_fly_locations([327708], access_rule=lambda state: can_free_scout_flies(state, player))

    zoomer = JakAndDaxterRegion("Zoomer", player, multiworld, level_name, 32)
    zoomer.add_cell_locations([27, 29])
    zoomer.add_fly_locations([393244])

    ship = JakAndDaxterRegion("Ship", player, multiworld, level_name, 10)
    ship.add_cell_locations([24])
    ship.add_fly_locations([131100], access_rule=lambda state: can_free_scout_flies(state, player))

    far_side = JakAndDaxterRegion("Far Side", player, multiworld, level_name, 16)

    # In order to even reach this fly, you must use the seesaw or crouch jump.
    far_side_cliff = JakAndDaxterRegion("Far Side Cliff", player, multiworld, level_name, 5)
    far_side_cliff.add_fly_locations([28], access_rule=lambda state: can_free_scout_flies(state, player))

    # To carry the blue eco fast enough to open this cache, you need to break the bone bridges along the way.
    far_side_cache = JakAndDaxterRegion("Far Side Orb Cache", player, multiworld, level_name, 15)
    far_side_cache.add_cache_locations([11072], access_rule=lambda state: can_fight(state, player))

    barrel_course = JakAndDaxterRegion("Barrel Course", player, multiworld, level_name, 10)
    barrel_course.add_fly_locations([196636], access_rule=lambda state: can_free_scout_flies(state, player))

    # 14 orbs for the boxes you can only break with the cannon.
    cannon = JakAndDaxterRegion("Cannon", player, multiworld, level_name, 14)
    cannon.add_cell_locations([26], access_rule=lambda state: can_fight(state, player))

    upper_approach = JakAndDaxterRegion("Upper Arena Approach", player, multiworld, level_name, 6)
    upper_approach.add_fly_locations([65564, 262172], access_rule=lambda state:
                                     can_free_scout_flies(state, player))

    lower_approach = JakAndDaxterRegion("Lower Arena Approach", player, multiworld, level_name, 7)
    lower_approach.add_cell_locations([30])

    arena = JakAndDaxterRegion("Arena", player, multiworld, level_name, 5)
    arena.add_cell_locations([25], access_rule=lambda state: can_fight(state, player))

    main_area.connect(muse_course)             # TODO - What do you need to chase the muse the whole way around?
    main_area.connect(zoomer)                  # Run and jump down.
    main_area.connect(ship)                    # Run and jump.
    main_area.connect(lower_approach)          # Run and jump.

    # Need to break the bone bridge to access.
    main_area.connect(upper_approach, rule=lambda state: can_fight(state, player))

    muse_course.connect(main_area)             # Run and jump down.

    # The zoomer pad is low enough that it requires Crouch Jump specifically.
    zoomer.connect(main_area, rule=lambda state: state.has_all(("Crouch", "Crouch Jump"), player))

    ship.connect(main_area)                    # Run and jump down.
    ship.connect(far_side)                     # Run and jump down.
    ship.connect(barrel_course)                # Run and jump (dodge barrels).

    far_side.connect(ship)                     # Run and jump.
    far_side.connect(arena)                    # Run and jump.

    # Only if you can use the seesaw or Crouch Jump from the seesaw's edge.
    far_side.connect(far_side_cliff, rule=lambda state:
                     state.has("Jump Dive", player)
                     or state.has_all(("Crouch", "Crouch Jump"), player))

    # Only if you can break the bone bridges to carry blue eco over the mud pit.
    far_side.connect(far_side_cache, rule=lambda state: can_fight(state, player))

    far_side_cliff.connect(far_side)           # Run and jump down.

    barrel_course.connect(cannon)              # Run and jump (dodge barrels).

    cannon.connect(barrel_course)              # Run and jump (dodge barrels).
    cannon.connect(arena)                      # Run and jump down.
    cannon.connect(upper_approach)             # Run and jump down.

    upper_approach.connect(lower_approach)     # Jump down.
    upper_approach.connect(arena)              # Jump down.

    # One cliff is accessible, but only via Crouch Jump.
    lower_approach.connect(upper_approach, rule=lambda state: state.has_all(("Crouch", "Crouch Jump"), player))

    # Requires breaking bone bridges.
    lower_approach.connect(arena, rule=lambda state: can_fight(state, player))

    arena.connect(lower_approach)              # Run.
    arena.connect(far_side)                    # Run.

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(muse_course)
    world.level_to_regions[level_name].append(zoomer)
    world.level_to_regions[level_name].append(ship)
    world.level_to_regions[level_name].append(far_side)
    world.level_to_regions[level_name].append(far_side_cliff)
    world.level_to_regions[level_name].append(far_side_cache)
    world.level_to_regions[level_name].append(barrel_course)
    world.level_to_regions[level_name].append(cannon)
    world.level_to_regions[level_name].append(upper_approach)
    world.level_to_regions[level_name].append(lower_approach)
    world.level_to_regions[level_name].append(arena)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 150 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(4,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return main_area

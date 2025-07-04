from BaseClasses import CollectionState
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

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 128)
    main_area.add_cell_locations([18, 21, 22])

    # These scout fly boxes can be broken by running with freely accessible blue eco.
    # The 3 clusters by the Flut Flut egg can go surprisingly far.
    main_area.add_fly_locations([327700, 20, 65556, 262164])

    # This scout fly box can be broken with the locked blue eco vent, or by normal combat tricks.
    main_area.add_fly_locations([393236], access_rule=lambda state:
                                state.has("Blue Eco Switch", player)
                                or can_free_scout_flies(state, player))

    # No need for the blue eco vent for either of the orb caches.
    main_area.add_cache_locations([12634, 12635])

    pelican = JakAndDaxterRegion("Pelican", player, multiworld, level_name, 0)
    pelican.add_cell_locations([16], access_rule=lambda state: can_fight(state, player))

    # Only these specific attacks can push the flut flut egg off the cliff.
    flut_flut_egg = JakAndDaxterRegion("Flut Flut Egg", player, multiworld, level_name, 0)
    flut_flut_egg.add_cell_locations([17], access_rule=lambda state:
                                     state.has_any(("Punch", "Kick", "Jump Kick"), player))
    flut_flut_egg.add_special_locations([17], access_rule=lambda state:
                                        state.has_any(("Punch", "Kick", "Jump Kick"), player))

    eco_harvesters = JakAndDaxterRegion("Eco Harvesters", player, multiworld, level_name, 0)
    eco_harvesters.add_cell_locations([15], access_rule=lambda state: can_fight(state, player))

    green_ridge = JakAndDaxterRegion("Ridge Near Green Vents", player, multiworld, level_name, 5)
    green_ridge.add_fly_locations([131092], access_rule=lambda state: can_free_scout_flies(state, player))

    blue_ridge = JakAndDaxterRegion("Ridge Near Blue Vent", player, multiworld, level_name, 5)
    blue_ridge.add_fly_locations([196628], access_rule=lambda state:
                                 state.has("Blue Eco Switch", player)
                                 or can_free_scout_flies(state, player))

    cannon_tower = JakAndDaxterRegion("Cannon Tower", player, multiworld, level_name, 12)
    cannon_tower.add_cell_locations([19], access_rule=lambda state: can_fight(state, player))

    main_area.connect(pelican)           # Swim and jump.
    main_area.connect(flut_flut_egg)     # Run and jump.
    main_area.connect(eco_harvesters)    # Run.

    # We need a helper function for the uppercut logs.
    def can_uppercut_and_jump_logs(state: CollectionState, p: int) -> bool:
        return (state.has_any(("Double Jump", "Jump Kick"), p)
                and (state.has_all(("Crouch", "Crouch Uppercut"), p)
                     or state.has_all(("Punch", "Punch Uppercut"), p)))

    # If you have double jump or crouch jump, you don't need the logs to reach this place.
    main_area.connect(green_ridge, rule=lambda state:
                      state.has("Double Jump", player)
                      or state.has_all(("Crouch", "Crouch Jump"), player)
                      or can_uppercut_and_jump_logs(state, player))

    # If you have the blue eco jump pad, you don't need the logs to reach this place.
    main_area.connect(blue_ridge, rule=lambda state:
                      state.has("Blue Eco Switch", player)
                      or can_uppercut_and_jump_logs(state, player))

    main_area.connect(cannon_tower, rule=lambda state: state.has("Blue Eco Switch", player))

    # All these can go back to main_area immediately.
    pelican.connect(main_area)
    flut_flut_egg.connect(main_area)
    eco_harvesters.connect(main_area)
    green_ridge.connect(main_area)
    blue_ridge.connect(main_area)
    cannon_tower.connect(main_area)

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(pelican)
    world.level_to_regions[level_name].append(flut_flut_egg)
    world.level_to_regions[level_name].append(eco_harvesters)
    world.level_to_regions[level_name].append(green_ridge)
    world.level_to_regions[level_name].append(blue_ridge)
    world.level_to_regions[level_name].append(cannon_tower)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 150 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(2,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return main_area

from typing import List

from .RegionBase import JakAndDaxterRegion
from .. import EnableOrbsanity, JakAndDaxterWorld
from ..Rules import can_free_scout_flies, can_fight, can_reach_orbs_level


def build_regions(level_name: str, world: JakAndDaxterWorld) -> List[JakAndDaxterRegion]:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 128)
    main_area.add_cell_locations([18, 21, 22])

    # These 3 scout fly boxes can be broken by running with freely accessible blue eco.
    main_area.add_fly_locations([327700, 20, 65556])

    # These 2 scout fly boxes can be broken with the locked blue eco vent, or by normal combat tricks.
    main_area.add_fly_locations([262164, 393236], access_rule=lambda state:
                                state.has("Blue Eco Switch", player)
                                or can_free_scout_flies(state, player))

    # No need for the blue eco vent for the orb caches.
    main_area.add_cache_locations([12634, 12635])

    pelican = JakAndDaxterRegion("Pelican", player, multiworld, level_name, 0)
    pelican.add_cell_locations([16], access_rule=lambda state: can_fight(state, player))

    # Only these specific attacks can push the flut flut egg off the cliff.
    flut_flut_egg = JakAndDaxterRegion("Flut Flut Egg", player, multiworld, level_name, 0)
    flut_flut_egg.add_cell_locations([17], access_rule=lambda state:
                                     state.has_any({"Punch", "Kick", "Jump Kick"}, player))
    flut_flut_egg.add_special_locations([17], access_rule=lambda state:
                                        state.has_any({"Punch", "Kick", "Jump Kick"}, player))

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

    # You don't need any kind of uppercut to reach this place, just a high jump from a convenient nearby ledge.
    main_area.connect(green_ridge, rule=lambda state:
                      state.has("Double Jump", player)
                      or state.has_all({"Crouch", "Crouch Jump"}, player))

    # Can either uppercut the log and jump from it, or use the blue eco jump pad.
    main_area.connect(blue_ridge, rule=lambda state:
                      state.has("Blue Eco Switch", player)
                      or (state.has("Double Jump", player)
                          and (state.has_all({"Crouch", "Crouch Uppercut"}, player)
                               or state.has_all({"Punch", "Punch Uppercut"}, player))))

    main_area.connect(cannon_tower, rule=lambda state: state.has("Blue Eco Switch", player))

    # All these can go back to main_area immediately.
    pelican.connect(main_area)
    flut_flut_egg.connect(main_area)
    eco_harvesters.connect(main_area)
    green_ridge.connect(main_area)
    blue_ridge.connect(main_area)
    cannon_tower.connect(main_area)

    multiworld.regions.append(main_area)
    multiworld.regions.append(pelican)
    multiworld.regions.append(flut_flut_egg)
    multiworld.regions.append(eco_harvesters)
    multiworld.regions.append(green_ridge)
    multiworld.regions.append(blue_ridge)
    multiworld.regions.append(cannon_tower)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 150 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(2,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, bundle=bundle_index:
                                   can_reach_orbs_level(state, player, world, level, bundle))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area]

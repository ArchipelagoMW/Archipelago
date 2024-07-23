from typing import List
from BaseClasses import CollectionState, MultiWorld
from .RegionBase import JakAndDaxterRegion
from .. import JakAndDaxterOptions, EnableOrbsanity
from ..Rules import can_free_scout_flies, can_fight, can_reach_orbs


# God help me... here we go.
def build_regions(level_name: str, multiworld: MultiWorld, options: JakAndDaxterOptions, player: int) -> List[JakAndDaxterRegion]:

    # This level is full of short-medium gaps that cannot be crossed by single jump alone.
    # These helper functions list out the moves that can cross all these gaps (painting with a broad brush but...)
    def can_jump_farther(state: CollectionState, p: int) -> bool:
        return (state.has("Double Jump", p)
                or state.has("Jump Kick", p)
                or (state.has("Punch", p) and state.has("Punch Uppercut", p)))

    def can_triple_jump(state: CollectionState, p: int) -> bool:
        return state.has("Double Jump", p) and state.has("Jump Kick", p)

    def can_jump_stairs(state: CollectionState, p: int) -> bool:
        return (state.has("Double Jump", p)
                or (state.has("Crouch", p) and state.has("Crouch Jump", p))
                or (state.has("Crouch", p) and state.has("Crouch Uppercut", p))
                or state.has("Jump Dive", p))

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 0)
    main_area.add_fly_locations([91], access_rule=lambda state: can_free_scout_flies(state, player))

    robot_scaffolding = JakAndDaxterRegion("Scaffolding Around Robot", player, multiworld, level_name, 8)
    robot_scaffolding.add_fly_locations([196699], access_rule=lambda state:
                                        can_free_scout_flies(state, player))

    jump_pad_room = JakAndDaxterRegion("Jump Pad Chamber", player, multiworld, level_name, 88)
    jump_pad_room.add_cell_locations([73], access_rule=lambda state: can_fight(state, player))
    jump_pad_room.add_special_locations([73], access_rule=lambda state: can_fight(state, player))
    jump_pad_room.add_fly_locations([131163])  # Blue eco vent is right next to it.
    jump_pad_room.add_fly_locations([65627], access_rule=lambda state:
                                    can_free_scout_flies(state, player)
                                    and can_jump_farther(state, player))

    blast_furnace = JakAndDaxterRegion("Blast Furnace", player, multiworld, level_name, 39)
    blast_furnace.add_cell_locations([71], access_rule=lambda state: can_fight(state, player))
    blast_furnace.add_special_locations([71], access_rule=lambda state: can_fight(state, player))
    blast_furnace.add_fly_locations([393307])  # Blue eco vent nearby.

    bunny_room = JakAndDaxterRegion("Bunny Chamber", player, multiworld, level_name, 45)
    bunny_room.add_cell_locations([72], access_rule=lambda state: can_fight(state, player))
    bunny_room.add_special_locations([72], access_rule=lambda state: can_fight(state, player))
    bunny_room.add_fly_locations([262235], access_rule=lambda state:
                                 can_free_scout_flies(state, player))

    rotating_tower = JakAndDaxterRegion("Rotating Tower", player, multiworld, level_name, 20)
    rotating_tower.add_cell_locations([70], access_rule=lambda state: can_fight(state, player))
    rotating_tower.add_special_locations([70], access_rule=lambda state: can_fight(state, player))
    rotating_tower.add_fly_locations([327771], access_rule=lambda state:
                                     can_free_scout_flies(state, player))

    final_boss = JakAndDaxterRegion("Final Boss", player, multiworld, level_name, 0)

    final_door = JakAndDaxterRegion("Final Door", player, multiworld, level_name, 0)

    # Jump Dive required for a lot of buttons, prepare yourself.
    main_area.connect(robot_scaffolding, rule=lambda state:
                      state.has("Jump Dive", player)
                      or (state.has("Roll", player) and state.has("Roll Jump", player)))
    main_area.connect(jump_pad_room)

    robot_scaffolding.connect(main_area, rule=lambda state: state.has("Jump Dive", player))
    robot_scaffolding.connect(blast_furnace, rule=lambda state:
                              state.has("Jump Dive", player)
                              and can_jump_farther(state, player)
                              and ((state.has("Roll", player) and state.has("Roll Jump", player))
                                   or can_triple_jump(state, player)))
    robot_scaffolding.connect(bunny_room, rule=lambda state:
                              state.has("Jump Dive", player)
                              and can_jump_farther(state, player)
                              and ((state.has("Roll", player) and state.has("Roll Jump", player))
                                   or can_triple_jump(state, player)))

    jump_pad_room.connect(main_area)
    jump_pad_room.connect(robot_scaffolding, rule=lambda state:
                          state.has("Jump Dive", player)
                          and ((state.has("Roll", player) and state.has("Roll Jump", player))
                               or can_triple_jump(state, player)))

    blast_furnace.connect(robot_scaffolding)  # Blue eco elevator takes you right back.

    bunny_room.connect(robot_scaffolding, rule=lambda state:
                       state.has("Jump Dive", player)
                       and ((state.has("Roll", player) and state.has("Roll Jump", player))
                            or can_jump_farther(state, player)))

    # Final climb.
    robot_scaffolding.connect(rotating_tower, rule=lambda state:
                              state.has("Freed The Blue Sage", player)
                              and state.has("Freed The Red Sage", player)
                              and state.has("Freed The Yellow Sage", player)
                              and can_jump_stairs(state, player))

    rotating_tower.connect(main_area)  # Take stairs back down.

    # Final elevator. Need to break boxes at summit to get blue eco for platform.
    rotating_tower.connect(final_boss, rule=lambda state:
                           state.has("Freed The Green Sage", player)
                           and can_fight(state, player))

    final_boss.connect(rotating_tower)  # Take elevator back down.

    # Final door. Need 100 power cells.
    final_boss.connect(final_door, rule=lambda state: state.has("Power Cell", player, 100))

    multiworld.regions.append(main_area)
    multiworld.regions.append(robot_scaffolding)
    multiworld.regions.append(jump_pad_room)
    multiworld.regions.append(blast_furnace)
    multiworld.regions.append(bunny_room)
    multiworld.regions.append(rotating_tower)
    multiworld.regions.append(final_boss)
    multiworld.regions.append(final_door)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_size = options.level_orbsanity_bundle_size.value
        bundle_count = int(200 / bundle_size)
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(15,
                                   bundle_index,
                                   bundle_size,
                                   access_rule=lambda state, bundle=bundle_index:
                                   can_reach_orbs(state, player, multiworld, options, level_name)
                                   >= (bundle_size * (bundle + 1)))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area, final_boss, final_door]

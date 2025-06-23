from BaseClasses import CollectionState
from .region_base import JakAndDaxterRegion
from ..options import EnableOrbsanity, CompletionCondition
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import JakAndDaxterWorld
from ..rules import can_free_scout_flies, can_fight, can_reach_orbs_level


# God help me... here we go.
def build_regions(level_name: str, world: "JakAndDaxterWorld") -> tuple[JakAndDaxterRegion | None, ...]:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    # This level is full of short-medium gaps that cannot be crossed by single jump alone.
    # These helper functions list out the moves that can cross all these gaps (painting with a broad brush but...)
    def can_jump_farther(state: CollectionState, p: int) -> bool:
        return (state.has_any(("Double Jump", "Jump Kick"), p)
                or state.has_all(("Punch", "Punch Uppercut"), p))

    def can_triple_jump(state: CollectionState, p: int) -> bool:
        return state.has_all(("Double Jump", "Jump Kick"), p)

    def can_jump_stairs(state: CollectionState, p: int) -> bool:
        return (state.has("Double Jump", p)
                or state.has("Jump Dive", p)
                or state.has_all(("Crouch", "Crouch Jump"), p)
                or state.has_all(("Crouch", "Crouch Uppercut"), p))

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 0)
    main_area.add_fly_locations([91], access_rule=lambda state: can_free_scout_flies(state, player))

    robot_scaffolding = JakAndDaxterRegion("Scaffolding Around Robot", player, multiworld, level_name, 8)
    robot_scaffolding.add_fly_locations([196699], access_rule=lambda state: can_free_scout_flies(state, player))

    jump_pad_room = JakAndDaxterRegion("Jump Pad Chamber", player, multiworld, level_name, 88)
    jump_pad_room.add_cell_locations([73], access_rule=lambda state: can_fight(state, player))
    jump_pad_room.add_special_locations([73], access_rule=lambda state: can_fight(state, player))
    jump_pad_room.add_fly_locations([131163])  # Blue eco vent is right next to it.
    jump_pad_room.add_fly_locations([65627], access_rule=lambda state:
                                    can_free_scout_flies(state, player) and can_jump_farther(state, player))
    jump_pad_room.add_cache_locations([24039, 24040])  # First, blue eco vent, second, blue eco cluster near sage.

    blast_furnace = JakAndDaxterRegion("Blast Furnace", player, multiworld, level_name, 39)
    blast_furnace.add_cell_locations([71], access_rule=lambda state: can_fight(state, player))
    blast_furnace.add_special_locations([71], access_rule=lambda state: can_fight(state, player))
    blast_furnace.add_fly_locations([393307])  # Blue eco vent nearby.
    blast_furnace.add_cache_locations([24038])  # Blue eco cluster near sage.

    bunny_room = JakAndDaxterRegion("Bunny Chamber", player, multiworld, level_name, 45)
    bunny_room.add_cell_locations([72], access_rule=lambda state: can_fight(state, player))
    bunny_room.add_special_locations([72], access_rule=lambda state: can_fight(state, player))
    bunny_room.add_fly_locations([262235], access_rule=lambda state: can_free_scout_flies(state, player))

    rotating_tower = JakAndDaxterRegion("Rotating Tower", player, multiworld, level_name, 20)
    rotating_tower.add_cell_locations([70], access_rule=lambda state: can_fight(state, player))
    rotating_tower.add_special_locations([70], access_rule=lambda state: can_fight(state, player))
    rotating_tower.add_fly_locations([327771], access_rule=lambda state: can_free_scout_flies(state, player))

    final_boss = JakAndDaxterRegion("Final Boss", player, multiworld, level_name, 0)

    # Jump Dive required for a lot of buttons, prepare yourself.
    main_area.connect(robot_scaffolding, rule=lambda state:
                      state.has("Jump Dive", player) or state.has_all(("Roll", "Roll Jump"), player))
    main_area.connect(jump_pad_room)

    robot_scaffolding.connect(main_area, rule=lambda state: state.has("Jump Dive", player))
    robot_scaffolding.connect(blast_furnace, rule=lambda state:
                              state.has("Jump Dive", player)
                              and can_jump_farther(state, player)
                              and (can_triple_jump(state, player) or state.has_all(("Roll", "Roll Jump"), player)))
    robot_scaffolding.connect(bunny_room, rule=lambda state:
                              state.has("Jump Dive", player)
                              and can_jump_farther(state, player)
                              and (can_triple_jump(state, player) or state.has_all(("Roll", "Roll Jump"), player)))

    jump_pad_room.connect(main_area)
    jump_pad_room.connect(robot_scaffolding, rule=lambda state:
                          state.has("Jump Dive", player)
                          and (can_triple_jump(state, player) or state.has_all(("Roll", "Roll Jump"), player)))

    blast_furnace.connect(robot_scaffolding)  # Blue eco elevator takes you right back.

    bunny_room.connect(robot_scaffolding, rule=lambda state:
                       state.has("Jump Dive", player)
                       and (can_jump_farther(state, player) or state.has_all(("Roll", "Roll Jump"), player)))

    # Final climb.
    robot_scaffolding.connect(rotating_tower, rule=lambda state:
                              can_jump_stairs(state, player)
                              and state.has_all(("Freed The Blue Sage",
                                                 "Freed The Red Sage",
                                                 "Freed The Yellow Sage"), player))

    rotating_tower.connect(main_area)  # Take stairs back down.

    # Final elevator. Need to break boxes at summit to get blue eco for platform.
    rotating_tower.connect(final_boss, rule=lambda state:
                           can_fight(state, player)
                           and state.has("Freed The Green Sage", player))

    final_boss.connect(rotating_tower)  # Take elevator back down.

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(robot_scaffolding)
    world.level_to_regions[level_name].append(jump_pad_room)
    world.level_to_regions[level_name].append(blast_furnace)
    world.level_to_regions[level_name].append(bunny_room)
    world.level_to_regions[level_name].append(rotating_tower)
    world.level_to_regions[level_name].append(final_boss)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 200 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(15,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    # Final door. Need 100 power cells.
    if options.jak_completion_condition == CompletionCondition.option_open_100_cell_door:
        final_door = JakAndDaxterRegion("Final Door", player, multiworld, level_name, 0)
        final_boss.connect(final_door, rule=lambda state: state.has("Power Cell", player, 100))

        world.level_to_regions[level_name].append(final_door)

        return main_area, final_boss, final_door
    else:
        return main_area, final_boss, None

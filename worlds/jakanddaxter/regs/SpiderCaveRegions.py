from .RegionBase import JakAndDaxterRegion
from ..Options import EnableOrbsanity
from .. import JakAndDaxterWorld
from ..Rules import can_free_scout_flies, can_fight, can_reach_orbs_level


def build_regions(level_name: str, world: JakAndDaxterWorld) -> list[JakAndDaxterRegion]:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    # A large amount of this area can be covered by single jump, floating platforms, web trampolines, and goggles.
    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 63)
    main_area.add_cell_locations([78, 84])
    main_area.add_fly_locations([327765, 393301, 196693, 131157])

    # This is a virtual region describing what you need to DO to get the Dark Crystal power cell,
    # rather than describing where each of the crystals ARE, because you can destroy them in any order,
    # and you need to destroy ALL of them to get the cell.
    dark_crystals = JakAndDaxterRegion("Dark Crystals", player, multiworld, level_name, 0)

    # can_fight = The underwater crystal in dark cave.
    # Roll Jump = The underwater crystal across a long dark eco pool.
    # The rest of the crystals can be destroyed with yellow eco in main_area.
    dark_crystals.add_cell_locations([79], access_rule=lambda state:
                                     can_fight(state, player)
                                     and state.has_all({"Roll", "Roll Jump"}, player))

    dark_cave = JakAndDaxterRegion("Dark Cave", player, multiworld, level_name, 5)
    dark_cave.add_cell_locations([80])
    dark_cave.add_fly_locations([262229], access_rule=lambda state: can_free_scout_flies(state, player))

    robot_cave = JakAndDaxterRegion("Robot Cave", player, multiworld, level_name, 0)

    # Need double jump for orbs.
    scaffolding_level_zero = JakAndDaxterRegion("Robot Scaffolding Level 0", player, multiworld, level_name, 12)

    scaffolding_level_one = JakAndDaxterRegion("Robot Scaffolding Level 1", player, multiworld, level_name, 53)
    scaffolding_level_one.add_fly_locations([85])  # Shootable.

    scaffolding_level_two = JakAndDaxterRegion("Robot Scaffolding Level 2", player, multiworld, level_name, 4)

    # Using the blue eco from the pole course, you can single jump to the scout fly up here.
    scaffolding_level_three = JakAndDaxterRegion("Robot Scaffolding Level 3", player, multiworld, level_name, 29)
    scaffolding_level_three.add_cell_locations([81])
    scaffolding_level_three.add_fly_locations([65621])

    pole_course = JakAndDaxterRegion("Pole Course", player, multiworld, level_name, 18)
    pole_course.add_cell_locations([82])

    # You only need combat to fight through the spiders, but to collect the orb crates,
    # you will need the yellow eco vent unlocked.
    spider_tunnel = JakAndDaxterRegion("Spider Tunnel", player, multiworld, level_name, 4)
    spider_tunnel.add_cell_locations([83])

    spider_tunnel_crates = JakAndDaxterRegion("Spider Tunnel Orb Crates", player, multiworld, level_name, 12)

    main_area.connect(dark_crystals)
    main_area.connect(robot_cave)
    main_area.connect(dark_cave, rule=lambda state:
                      can_fight(state, player)
                      and (state.has("Double Jump", player)
                           or state.has_all({"Crouch", "Crouch Jump"}, player)))

    robot_cave.connect(main_area)
    robot_cave.connect(pole_course)                 # Nothing special required.
    robot_cave.connect(scaffolding_level_one)       # Ramps lead to level 1.
    robot_cave.connect(spider_tunnel)               # Web trampolines (bounce twice on each to gain momentum).

    pole_course.connect(robot_cave)                 # Blue eco platform down.

    scaffolding_level_one.connect(robot_cave)       # All scaffolding (level 1+) connects back by jumping down.

    # Elevator, but the orbs need double jump or jump kick.
    scaffolding_level_one.connect(scaffolding_level_zero, rule=lambda state:
                                  state.has_any({"Double Jump", "Jump Kick"}, player))

    # Narrow enough that enemies are unavoidable.
    scaffolding_level_one.connect(scaffolding_level_two, rule=lambda state: can_fight(state, player))

    scaffolding_level_zero.connect(scaffolding_level_one)           # Elevator.

    scaffolding_level_two.connect(robot_cave)                       # Jump down.
    scaffolding_level_two.connect(scaffolding_level_one)            # Elevator.

    # Elevator, but narrow enough that enemies are unavoidable.
    scaffolding_level_two.connect(scaffolding_level_three, rule=lambda state: can_fight(state, player))

    scaffolding_level_three.connect(robot_cave)                     # Jump down.
    scaffolding_level_three.connect(scaffolding_level_two)          # Elevator.

    spider_tunnel.connect(robot_cave)                               # Back to web trampolines.
    spider_tunnel.connect(main_area)                                # Escape with jump pad.

    # Requires yellow eco switch.
    spider_tunnel.connect(spider_tunnel_crates, rule=lambda state: state.has("Yellow Eco Switch", player))

    multiworld.regions.append(main_area)
    multiworld.regions.append(dark_crystals)
    multiworld.regions.append(dark_cave)
    multiworld.regions.append(robot_cave)
    multiworld.regions.append(scaffolding_level_zero)
    multiworld.regions.append(scaffolding_level_one)
    multiworld.regions.append(scaffolding_level_two)
    multiworld.regions.append(scaffolding_level_three)
    multiworld.regions.append(pole_course)
    multiworld.regions.append(spider_tunnel)
    multiworld.regions.append(spider_tunnel_crates)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 200 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(13,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, bundle=bundle_index:
                                   can_reach_orbs_level(state, player, world, level, bundle))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area]

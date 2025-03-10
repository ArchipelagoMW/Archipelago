from .RegionBase import JakAndDaxterRegion
from ..Options import EnableOrbsanity
from .. import JakAndDaxterWorld
from ..Rules import can_reach_orbs_level
from ..locs import ScoutLocations as Scouts
from worlds.generic.Rules import add_rule


def build_regions(level_name: str, world: JakAndDaxterWorld) -> list[JakAndDaxterRegion]:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    # This is basically just Klaww.
    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 0)
    main_area.add_cell_locations([86])

    # Some folks prefer firing Yellow Eco from the hip, so optionally put this rule before Klaww. Klaww is the only
    # location in main_area, so he's at index 0.
    if world.options.require_punch_for_klaww:
        add_rule(main_area.locations[0], lambda state: state.has("Punch", player))

    race = JakAndDaxterRegion("Race", player, multiworld, level_name, 50)
    race.add_cell_locations([87])

    # All scout flies can be broken with the zoomer.
    race.add_fly_locations(Scouts.locMP_scoutTable.keys())

    shortcut = JakAndDaxterRegion("Shortcut", player, multiworld, level_name, 0)
    shortcut.add_cell_locations([110])

    # Of course, in order to make it to the race region, you must defeat Klaww. He's not optional.
    # So we need to set up this inter-region rule as well (or make it free if the setting is off).
    if world.options.require_punch_for_klaww:
        main_area.connect(race, rule=lambda state: state.has("Punch", player))
    else:
        main_area.connect(race)

    # You actually can go backwards from the race back to Klaww's area.
    race.connect(main_area)
    race.connect(shortcut, rule=lambda state: state.has("Yellow Eco Switch", player))

    shortcut.connect(race)

    multiworld.regions.append(main_area)
    multiworld.regions.append(race)
    multiworld.regions.append(shortcut)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 50 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(10,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, bundle=bundle_index:
                                   can_reach_orbs_level(state, player, world, level, bundle))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    # Return race required for inter-level connections.
    return [main_area, race]

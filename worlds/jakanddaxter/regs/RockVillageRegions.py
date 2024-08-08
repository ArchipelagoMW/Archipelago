from typing import List
from BaseClasses import CollectionState, MultiWorld
from .RegionBase import JakAndDaxterRegion
from .. import JakAndDaxterOptions, EnableOrbsanity
from ..Rules import can_free_scout_flies, can_trade, can_reach_orbs


def build_regions(level_name: str, multiworld: MultiWorld, options: JakAndDaxterOptions, player: int) -> List[JakAndDaxterRegion]:

    # This includes most of the area surrounding LPC as well, for orb_count purposes. You can swim and single jump.
    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 23)
    main_area.add_cell_locations([31], access_rule=lambda state:
                                 can_trade(state, player, multiworld, options, 1530))
    main_area.add_cell_locations([32], access_rule=lambda state:
                                 can_trade(state, player, multiworld, options, 1530))
    main_area.add_cell_locations([33], access_rule=lambda state:
                                 can_trade(state, player, multiworld, options, 1530))
    main_area.add_cell_locations([34], access_rule=lambda state:
                                 can_trade(state, player, multiworld, options, 1530))
    main_area.add_cell_locations([35], access_rule=lambda state:
                                 can_trade(state, player, multiworld, options, 1530, 34))

    # These 2 scout fly boxes can be broken by running with nearby blue eco.
    main_area.add_fly_locations([196684, 262220])
    main_area.add_fly_locations([76, 131148, 65612, 327756], access_rule=lambda state:
                                can_free_scout_flies(state, player))

    # Warrior Pontoon check. You just talk to him and get his introduction.
    main_area.add_special_locations([33])

    orb_cache = JakAndDaxterRegion("Orb Cache", player, multiworld, level_name, 20)

    # You need roll jump to be able to reach this before the blue eco runs out.
    orb_cache.add_cache_locations([10945], access_rule=lambda state: state.has_all({"Roll", "Roll Jump"}, player))

    # Fly here can be gotten with Yellow Eco from Boggy, goggles, and no extra movement options (see fly ID 43).
    pontoon_bridge = JakAndDaxterRegion("Pontoon Bridge", player, multiworld, level_name, 7)
    pontoon_bridge.add_fly_locations([393292])

    klaww_cliff = JakAndDaxterRegion("Klaww's Cliff", player, multiworld, level_name, 0)

    main_area.connect(orb_cache, rule=lambda state: state.has_all({"Roll", "Roll Jump"}, player))
    main_area.connect(pontoon_bridge, rule=lambda state: state.has("Warrior's Pontoons", player))

    orb_cache.connect(main_area)

    pontoon_bridge.connect(main_area, rule=lambda state: state.has("Warrior's Pontoons", player))
    pontoon_bridge.connect(klaww_cliff, rule=lambda state:
                           state.has("Double Jump", player)
                           or state.has_all({"Crouch", "Crouch Jump"}, player)
                           or state.has_all({"Crouch", "Crouch Uppercut", "Jump Kick"}, player))

    klaww_cliff.connect(pontoon_bridge)  # Just jump back down.

    multiworld.regions.append(main_area)
    multiworld.regions.append(orb_cache)
    multiworld.regions.append(pontoon_bridge)
    multiworld.regions.append(klaww_cliff)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_size = options.level_orbsanity_bundle_size.value
        bundle_count = int(50 / bundle_size)
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(6,
                                   bundle_index,
                                   bundle_size,
                                   access_rule=lambda state, bundle=bundle_index:
                                   can_reach_orbs(state, player, multiworld, options, level_name)
                                   >= (bundle_size * (bundle + 1)))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    # Return klaww_cliff required for inter-level connections.
    return [main_area, pontoon_bridge, klaww_cliff]

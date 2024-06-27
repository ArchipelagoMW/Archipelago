from typing import List
from BaseClasses import CollectionState, MultiWorld
from .RegionBase import JakAndDaxterRegion
from ..Rules import can_free_scout_flies, can_trade


def build_regions(level_name: str, player: int, multiworld: MultiWorld) -> List[JakAndDaxterRegion]:

    # This includes most of the area surrounding LPC as well, for orb_count purposes. You can swim and single jump.
    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 23)
    main_area.add_cell_locations([31], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530))
    main_area.add_cell_locations([32], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530))
    main_area.add_cell_locations([33], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530))
    main_area.add_cell_locations([34], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530))
    main_area.add_cell_locations([35], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530, 34))

    # These 2 scout fly boxes can be broken by running with nearby blue eco.
    main_area.add_fly_locations([196684, 262220])
    main_area.add_fly_locations([76, 131148, 65612, 327756], access_rule=lambda state:
                                can_free_scout_flies(state, player))

    # Warrior Pontoon check. You just talk to him and get his introduction.
    main_area.add_special_locations([33])

    orb_cache = JakAndDaxterRegion("Orb Cache", player, multiworld, level_name, 20)

    # You need roll jump to be able to reach this before the blue eco runs out.
    orb_cache.add_cache_locations([10945], access_rule=lambda state:
                                  (state.has("Roll", player) and state.has("Roll Jump", player)))

    pontoon_bridge = JakAndDaxterRegion("Pontoon Bridge", player, multiworld, level_name, 7)
    pontoon_bridge.add_fly_locations([393292], access_rule=lambda state: can_free_scout_flies(state, player))

    klaww_cliff = JakAndDaxterRegion("Klaww's Cliff", player, multiworld, level_name, 0)

    main_area.connect(orb_cache, rule=lambda state: (state.has("Roll", player) and state.has("Roll Jump", player)))
    main_area.connect(pontoon_bridge, rule=lambda state: state.has("Warrior's Pontoons", player))

    orb_cache.connect(main_area)

    pontoon_bridge.connect(main_area, rule=lambda state: state.has("Warrior's Pontoons", player))
    pontoon_bridge.connect(klaww_cliff, rule=lambda state:
                           state.has("Double Jump", player)
                           or (state.has("Crouch", player)
                               and state.has("Crouch Jump", player))
                           or (state.has("Crouch", player)
                               and state.has("Crouch Uppercut", player)
                               and state.has("Jump Kick", player)))

    klaww_cliff.connect(pontoon_bridge)  # Just jump back down.

    multiworld.regions.append(main_area)
    multiworld.regions.append(orb_cache)
    multiworld.regions.append(pontoon_bridge)
    multiworld.regions.append(klaww_cliff)

    # Return klaww_cliff required for inter-level connections.
    return [main_area, pontoon_bridge, klaww_cliff]

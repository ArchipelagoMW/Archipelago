from worlds.generic.Rules import add_rule
from .Logic import MetroidPrimeLogic as logic
from BaseClasses import MultiWorld


def set_rules(multiworld: MultiWorld, player, locations):
    access_rules = {
        # chozo ruins locations
        'Chozo Ruins: Main Plaza - Half-Pipe': lambda state: logic.prime_can_boost(state, multiworld, player),
        'Chozo Ruins: Main Plaza - Grapple Ledge': lambda state: (
                logic.prime_has_missiles(state, multiworld, player) and
                logic.prime_can_bomb(state, multiworld, player) and
                logic.prime_can_heat(state, multiworld, player) and
                state.has_all({'Boost Ball', 'Grapple Beam', 'Wave Beam'}, player)),
        'Chozo Ruins: Main Plaza - Tree': lambda state: logic.prime_can_super(state, multiworld, player),
        'Chozo Ruins: Main Plaza - Locked Door': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                                state.has('Morph Ball', player)),
        'Chozo Ruins: Ruined Fountain': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                       logic.prime_can_bomb(state, multiworld, player) and
                                                       logic.prime_can_spider(state, multiworld, player)),
        'Chozo Ruins: Ruined Shrine - Plated Beetle': lambda state: (
                    logic.prime_has_missiles(state, multiworld, player) and
                    state.has_any({'Morph Ball', 'Space Jump Boots'}, player)),
        'Chozo Ruins: Ruined Shrine - Half-Pipe': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                                 logic.prime_can_boost(state, multiworld, player)),
        'Chozo Ruins: Ruined Shrine - Lower Tunnel': lambda state: (
                    logic.prime_has_missiles(state, multiworld, player) and
                    (logic.prime_can_bomb(state, multiworld, player) or
                     logic.prime_can_pb(state, multiworld, player))),
        'Chozo Ruins: Vault': lambda state: (logic.prime_has_missiles(state, multiworld, player)
                                             and logic.prime_can_bomb(state, multiworld, player)),
        'Chozo Ruins: Training Chamber': lambda state: (logic.prime_magma_pool(state, multiworld, player) and
                                                        logic.prime_can_bomb(state, multiworld, player) and
                                                        state.has_all({'Boost Ball', 'Spider Ball', 'Wave Beam'},
                                                                      player)),
        'Chozo Ruins: Ruined Nursery': lambda state: logic.prime_can_bomb(state, multiworld, player),
        'Chozo Ruins: Training Chamber Access': lambda state: (logic.prime_magma_pool(state, multiworld, player) and
                                                               logic.prime_can_bomb(state, multiworld, player) and
                                                               state.has('Wave Beam', player)),
        'Chozo Ruins: Magma Pool': lambda state: (logic.prime_magma_pool(state, multiworld, player) and
                                                  logic.prime_can_pb(state, multiworld, player)),
        'Chozo Ruins: Tower of Light': lambda state: (logic.prime_tower_of_light(state, multiworld, player) and
                                                      (logic.prime_has_missile_count(state, multiworld, player) >= 40)),
        'Chozo Ruins: Tower Chamber': lambda state: (logic.prime_tower_of_light(state, multiworld, player)
                                                     and state.has('Gravity Suit', player)),
        'Chozo Ruins: Ruined Gallery - Missile Wall': lambda state: logic.prime_has_missiles(state, multiworld, player),
        'Chozo Ruins: Ruined Gallery - Tunnel': lambda state: logic.prime_can_bomb(state, multiworld, player),
        'Chozo Ruins: Transport Access North': lambda state: logic.prime_has_missiles(state, multiworld, player),
        'Chozo Ruins: Gathering Hall': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                      state.has('Space Jump Boots', player) and
                                                      (logic.prime_can_bomb(state, multiworld, player) or
                                                       logic.prime_can_pb(state, multiworld, player))),
        'Chozo Ruins: Sunchamber - Flaaghra': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                             logic.prime_can_bomb(state, multiworld, player) and
                                                             state.count('Energy Tank', player) >= 1),
        'Chozo Ruins: Sunchamber - Ghosts': lambda state: (logic.prime_can_super(state, multiworld, player) and
                                                           logic.prime_can_bomb(state, multiworld, player) and
                                                           logic.prime_can_spider(state, multiworld, player)),
        'Chozo Ruins: Watery Hall Access': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                          state.has('Morph Ball', player)),
        'Chozo Ruins: Watery Hall - Scan Puzzle': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                                 state.has('Morph Ball', player)),
        'Chozo Ruins: Watery Hall - Underwater': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                                logic.prime_can_bomb(state, multiworld, player) and
                                                                state.has_all({'Space Jump Boots', 'Gravity Suit'},
                                                                              player)),
        'Chozo Ruins: Dynamo - Lower': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                      (logic.prime_can_bomb(state, multiworld, player) or
                                                       logic.prime_can_pb(state, multiworld, player))),
        'Chozo Ruins: Dynamo - Spider Track': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                             (logic.prime_can_bomb(state, multiworld, player) or
                                                              logic.prime_can_pb(state, multiworld, player)) and
                                                             logic.prime_can_spider(state, multiworld, player)),
        'Chozo Ruins: Burn Dome - Missile': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                           logic.prime_has_missiles(state, multiworld, player)),
        'Chozo Ruins: Burn Dome - Incinerator Drone': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                                     logic.prime_has_missiles(state, multiworld,
                                                                                              player)),
        'Chozo Ruins: Furnace - Spider Tracks': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                               logic.prime_can_bomb(state, multiworld, player) and
                                                               logic.prime_can_pb(state, multiworld, player) and
                                                               state.has_all({'Spider Ball', 'Boost Ball'}, player)),
        'Chozo Ruins: Furnace - Inside Furnace': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                                logic.prime_has_missiles(state, multiworld, player)),
        'Chozo Ruins: Hall of the Elders': lambda state: (logic.prime_late_chozo(state, multiworld, player) and
                                                          logic.prime_can_bomb(state, multiworld, player) and
                                                          state.has_all({'Space Jump Boots', 'Spider Ball', 'Ice Beam'},
                                                                        player)),
        'Chozo Ruins: Crossway': lambda state: (logic.prime_late_chozo(state, multiworld, player) and
                                                logic.prime_can_super(state, multiworld, player) and
                                                logic.prime_can_bomb(state, multiworld, player) and
                                                state.has_all({'Boost Ball', 'Spider Ball'}, player)),
        'Chozo Ruins: Elder Chamber': lambda state: (logic.prime_late_chozo(state, multiworld, player) and
                                                     logic.prime_can_bomb(state, multiworld, player) and
                                                     state.has_all({'Space Jump Boots', 'Ice Beam', 'Plasma Beam'},
                                                                   player)),
        'Chozo Ruins: Antechamber': lambda state: (logic.prime_reflecting_pool(state, multiworld, player) and
                                                   logic.prime_has_missiles(state, multiworld, player) and
                                                   state.has('Ice Beam', player)),

        # phendrana drifts locations
        'Phendrana Drifts: Phendrana Shorelines - Behind Ice': lambda state: (
                    logic.prime_front_phen(state, multiworld, player) and
                    state.has('Plasma Beam', player)),
        'Phendrana Drifts: Phendrana Shorelines - Spider Track': lambda state: (
                    logic.prime_front_phen(state, multiworld, player) and
                    logic.prime_can_super(state, multiworld, player) and
                    logic.prime_can_spider(state, multiworld, player) and
                    state.has('Space Jump Boots', player)),
        'Phendrana Drifts: Chozo Ice Temple': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                             state.has_all({'Plasma Beam', 'Space Jump Boots'},
                                                                           player)),
        'Phendrana Drifts: Ice Ruins West': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                           state.has_all({'Plasma Beam', 'Space Jump Boots'}, player)),
        'Phendrana Drifts: Ice Ruins East - Behind Ice': lambda state: (
                    logic.prime_front_phen(state, multiworld, player) and
                    state.has('Plasma Beam', player)),
        'Phendrana Drifts: Ice Ruins East - Spider Track': lambda state: (
                    logic.prime_front_phen(state, multiworld, player) and
                    logic.prime_can_spider(state, multiworld, player)),
        'Phendrana Drifts: Chapel of the Elders': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                                 logic.prime_can_bomb(state, multiworld, player) and
                                                                 state.has_all({'Space Jump Boots', 'Wave Beam'},
                                                                               player)),
        'Phendrana Drifts: Ruined Courtyard': lambda state: (logic.prime_middle_phen(state, multiworld, player) and
                                                             state.has_all({'Space Jump Boots', 'Wave Beam'},
                                                                           player) and
                                                             ((logic.prime_can_bomb(state, multiworld, player) and
                                                               logic.prime_can_boost(state, multiworld, player)) or
                                                              logic.prime_can_spider(state, multiworld, player))),
        'Phendrana Drifts: Phendrana Canyon': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                             (logic.prime_can_boost(state, multiworld, player) or
                                                              state.has('Space Jump Boots', player))),
        'Phendrana Drifts: Quarantine Cave': lambda state: (logic.prime_quarantine_cave(state, multiworld, player) and
                                                            logic.prime_can_spider(state, multiworld, player) and
                                                            state.has('Thermal Visor', player) and
                                                            state.count('Energy Tank', player) >= 3),
        'Phendrana Drifts: Research Lab Hydra': lambda state: (logic.prime_labs(state, multiworld, player) and
                                                               logic.prime_can_super(state, multiworld, player)),
        'Phendrana Drifts: Quarantine Monitor': lambda state: (
                    logic.prime_quarantine_cave(state, multiworld, player) and
                    logic.prime_can_spider(state, multiworld, player) and
                    state.has_all({'Thermal Visor', 'Grapple Beam'}, player)),
        'Phendrana Drifts: Observatory': lambda state: (logic.prime_labs(state, multiworld, player) and
                                                        logic.prime_can_bomb(state, multiworld, player) and
                                                        logic.prime_can_boost(state, multiworld, player)),
        'Phendrana Drifts: Transport Access': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                                             state.has('Plasma Beam', player)),
        'Phendrana Drifts: Control Tower': lambda state: (logic.prime_labs(state, multiworld, player) and
                                                          logic.prime_can_bomb(state, multiworld, player) and
                                                          state.has('Plasma Beam', player)),
        'Phendrana Drifts: Research Core': lambda state: logic.prime_labs(state, multiworld, player),
        'Phendrana Drifts: Frost Cave': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                                       state.has('Grapple Beam', player)),
        'Phendrana Drifts: Research Lab Aether - Tank': lambda state: logic.prime_labs(state, multiworld, player),
        'Phendrana Drifts: Research Lab Aether - Morph Track': lambda state: logic.prime_labs(state, multiworld,
                                                                                              player),
        'Phendrana Drifts: Gravity Chamber - Underwater': lambda state: (
                    logic.prime_far_phen(state, multiworld, player) and
                    state.has('Gravity Suit', player)),
        'Phendrana Drifts: Gravity Chamber - Grapple Ledge': lambda state: (
                    logic.prime_far_phen(state, multiworld, player) and
                    state.has_all({'Gravity Suit', 'Plasma Beam',
                                   'Grapple Beam'}, player)),
        'Phendrana Drifts: Storage Cave': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                                         logic.prime_can_pb(state, multiworld, player) and
                                                         state.has_all({'Plasma Beam', 'Grapple Beam'}, player)),
        'Phendrana Drifts: Security Cave': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                                          logic.prime_can_pb(state, multiworld, player) and
                                                          state.has_all({'Plasma Beam', 'Grapple Beam'}, player)),

        # tallon overworld locations
        'Tallon Overworld: Landing Site': lambda state: state.has('Morph Ball', player),
        'Tallon Overworld: Alcove': lambda state: ((logic.prime_can_bomb(state, multiworld, player) and
                                                    logic.prime_can_boost(state, multiworld, player)) or
                                                   state.has('Space Jump Boots', player)),
        'Tallon Overworld: Frigate Crash Site': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                               state.has_all(
                                                                   {'Space Jump Boots', 'Morph Ball', 'Gravity Suit'},
                                                                   player)),
        'Tallon Overworld: Overgrown Cavern': lambda state: (logic.prime_reflecting_pool(state, multiworld, player) and
                                                             state.has_all({'Ice Beam', 'Morph Ball'}, player)),

        'Tallon Overworld: Root Cave': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                      state.has_all({'Grapple Beam', 'Space Jump Boots', 'X-Ray Visor'},
                                                                    player)),
        'Tallon Overworld: Artifact Temple': lambda state: logic.prime_has_missiles(state, multiworld, player),
        'Tallon Overworld: Transport Tunnel B': lambda state: logic.prime_has_missiles(state, multiworld, player),
        'Tallon Overworld: Arbor Chamber': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                          state.has_all(
                                                              {'Grapple Beam', 'Space Jump Boots', 'X-Ray Visor',
                                                               'Plasma Beam'}, player)),
        'Tallon Overworld: Cargo Freight Lift to Deck Gamma': lambda state: logic.prime_frigate(state, multiworld,
                                                                                                player),
        'Tallon Overworld: Biohazard Containment': lambda state: (logic.prime_frigate(state, multiworld, player) and
                                                                  logic.prime_can_super(state, multiworld, player)),
        'Tallon Overworld: Hydro Access Tunnel': lambda state: (logic.prime_frigate(state, multiworld, player) and
                                                                logic.prime_can_bomb(state, multiworld, player)),
        'Tallon Overworld: Great Tree Chamber': lambda state: (
                state.has_all({'X-Ray Visor', 'Ice Beam', 'Space Jump Boots'}, player) and
                (logic.prime_reflecting_pool(state, multiworld, player) or
                 (logic.prime_frigate(state, multiworld, player) and
                  logic.prime_can_bomb(state, multiworld, player) and
                  logic.prime_can_boost(state, multiworld, player)))),
        'Tallon Overworld: Life Grove Tunnel': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                              logic.prime_can_boost(state, multiworld, player) and
                                                              logic.prime_can_spider(state, multiworld, player) and
                                                              logic.prime_can_pb(state, multiworld, player) and
                                                              state.has_all({'Ice Beam', 'Space Jump Boots'},
                                                                            player) and
                                                              (logic.prime_frigate(state, multiworld, player) or
                                                               logic.prime_reflecting_pool(state, multiworld, player))),
        'Tallon Overworld: Life Grove - Start': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                               logic.prime_can_boost(state, multiworld, player) and
                                                               logic.prime_can_spider(state, multiworld, player) and
                                                               logic.prime_can_pb(state, multiworld, player) and
                                                               state.has_all({'Ice Beam', 'Space Jump Boots'},
                                                                             player) and
                                                               (logic.prime_frigate(state, multiworld, player) or
                                                                logic.prime_reflecting_pool(state, multiworld,
                                                                                            player))),
        'Tallon Overworld: Life Grove - Underwater Spinner': lambda state: (
                    logic.prime_can_bomb(state, multiworld, player) and
                    logic.prime_can_boost(state, multiworld, player) and
                    logic.prime_can_spider(state, multiworld, player) and
                    logic.prime_can_pb(state, multiworld, player) and
                    state.has_all({'Ice Beam', 'Space Jump Boots'}, player) and
                    (logic.prime_frigate(state, multiworld, player) or
                     logic.prime_reflecting_pool(state, multiworld, player))),

        # phazon mines locations
        'Phazon Mines: Main Quarry': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                    logic.prime_can_bomb(state, multiworld, player) and
                                                    logic.prime_can_spider(state, multiworld, player) and
                                                    state.has('Thermal Visor', player)),
        'Phazon Mines: Security Access A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                          logic.prime_can_pb(state, multiworld, player)),
        'Phazon Mines: Storage Depot B': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                        logic.prime_can_bomb(state, multiworld, player) and
                                                        logic.prime_can_pb(state, multiworld, player) and
                                                        logic.prime_can_spider(state, multiworld, player) and
                                                        state.has('Grapple Beam', player)),
        'Phazon Mines: Storage Depot A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                        logic.prime_can_pb(state, multiworld, player) and
                                                        state.has('Plasma Beam', player)),
        'Phazon Mines: Elite Research - Phazon Elite': lambda state: (
                    logic.prime_upper_mines(state, multiworld, player) and
                    logic.prime_can_pb(state, multiworld, player)),
        'Phazon Mines: Elite Research - Laser': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                               logic.prime_can_bomb(state, multiworld, player) and
                                                               logic.prime_can_boost(state, multiworld, player)),
        'Phazon Mines: Elite Control Access': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                             logic.prime_can_bomb(state, multiworld, player) and
                                                             logic.prime_can_pb(state, multiworld, player) and
                                                             logic.prime_can_spider(state, multiworld, player) and
                                                             state.has('Grapple Beam', player)),
        'Phazon Mines: Ventilation Shaft': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                          logic.prime_can_bomb(state, multiworld, player) and
                                                          logic.prime_can_pb(state, multiworld, player) and
                                                          logic.prime_can_spider(state, multiworld, player) and
                                                          logic.prime_can_boost(state, multiworld, player) and
                                                          state.has('Grapple Beam', player)),
        'Phazon Mines: Phazon Processing Center': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                                 logic.prime_can_bomb(state, multiworld, player) and
                                                                 logic.prime_can_pb(state, multiworld, player) and
                                                                 logic.prime_can_spider(state, multiworld, player) and
                                                                 state.has('Grapple Beam', player)),
        'Phazon Mines: Processing Center Access': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                                 state.has('X-Ray Visor', player)),
        'Phazon Mines: Elite Quarters': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                       state.has('X-Ray Visor', player) and
                                                       state.count('Energy Tank', player) >= 7),
        'Phazon Mines: Central Dynamo': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                       logic.prime_can_bomb(state, multiworld, player) and
                                                       logic.prime_can_pb(state, multiworld, player) and
                                                       logic.prime_can_spider(state, multiworld, player) and
                                                       state.has_all({'Grapple Beam', 'X-Ray Visor'}, player)),
        'Phazon Mines: Metroid Quarantine B': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                             logic.prime_can_super(state, multiworld, player)),
        'Phazon Mines: Metroid Quarantine A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                             logic.prime_can_bomb(state, multiworld, player) and
                                                             logic.prime_can_pb(state, multiworld, player) and
                                                             logic.prime_can_spider(state, multiworld, player) and
                                                             logic.prime_can_boost(state, multiworld, player) and
                                                             state.has_all({'Grapple Beam', 'X-Ray Visor'}, player)),
        'Phazon Mines: Fungal Hall B': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                      state.has_any({'Thermal Visor', 'X-Ray Visor'}, player)),
        'Phazon Mines: Phazon Mining Tunnel': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                             state.has('Phazon Suit', player)),
        'Phazon Mines: Fungal Hall Access': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                           logic.prime_can_bomb(state, multiworld, player) and
                                                           logic.prime_can_pb(state, multiworld, player) and
                                                           logic.prime_can_boost(state, multiworld, player) and
                                                           state.has_all({'Grapple Beam', 'X-Ray Visor', 'Plasma Beam'},
                                                                         player)),

        # magmoor caverns locations
        'Magmoor Caverns: Lava Lake': lambda state: (logic.prime_can_heat(state, multiworld, player) and
                                                     logic.prime_has_missiles(state, multiworld, player) and
                                                     state.has_all({'Morph Ball', 'Space Jump Boots'}, player)),
        'Magmoor Caverns: Triclops Pit': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                                        logic.prime_has_missiles(state, multiworld, player) and
                                                        state.has('Space Jump Boots', player)),
        'Magmoor Caverns: Storage Cavern': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                                          state.has('Morph Ball', player)),
        'Magmoor Caverns: Transport Tunnel A': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                                              logic.prime_can_bomb(state, multiworld, player)),
        'Magmoor Caverns: Warrior Shrine': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                                          logic.prime_can_bomb(state, multiworld, player) and
                                                          logic.prime_can_boost(state, multiworld, player) and
                                                          state.has('Space Jump Boots', player)),
        'Magmoor Caverns: Shore Tunnel': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                                        logic.prime_can_pb(state, multiworld, player) and
                                                        state.has('Space Jump Boots', player)),
        'Magmoor Caverns: Fiery Shores - Morph Track': lambda state: (
                    logic.prime_can_heat(state, multiworld, player) and
                    logic.prime_has_missiles(state, multiworld, player) and
                    logic.prime_can_bomb(state, multiworld, player)),
        'Magmoor Caverns: Fiery Shores - Warrior Shrine Tunnel': lambda state: (
                    logic.prime_early_magmoor(state, multiworld, player)
                    and logic.prime_can_bomb(state, multiworld, player)
                    and logic.prime_can_boost(state, multiworld, player)
                    and logic.prime_can_pb(state, multiworld, player)
                    and state.has('Space Jump Boots', player)),
        'Magmoor Caverns: Plasma Processing': lambda state: (logic.prime_late_magmoor(state, multiworld, player) and
                                                             logic.prime_can_bomb(state, multiworld, player) and
                                                             logic.prime_can_boost(state, multiworld, player) and
                                                             logic.prime_can_spider(state, multiworld, player) and
                                                             state.has_all({'Ice Beam', 'Plasma Beam', 'Grapple Beam'},
                                                                           player)),
        'Magmoor Caverns: Magmoor Workstation': lambda state: (logic.prime_late_magmoor(state, multiworld, player) and
                                                               state.has_all(
                                                                   {'Morph Ball', 'Wave Beam', 'Thermal Visor'},
                                                                   player))
    }

    for i in locations:
        location = multiworld.get_location(i, player)
        try:
            add_rule(location, access_rules[i])
        except KeyError:
            continue

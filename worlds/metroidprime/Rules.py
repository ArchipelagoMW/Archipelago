from worlds.generic.Rules import add_rule
from .Logic import MetroidPrimeLogic as logic


def set_rules(multiworld, player):
    access_rules = {
        # chozo ruins locations
        'CR Main Plaza - Half-Pipe': lambda state: logic.prime_can_boost(state, multiworld, player),
        'CR Main Plaza - Grapple Ledge': lambda state: (
                logic.prime_has_missiles(state, multiworld, player) and
                logic.prime_can_bomb(state, multiworld, player) and
                logic.prime_can_heat(state, multiworld, player) and
                state.has({'Boost Ball', 'Grapple Beam', 'Wave Beam'}, player)),
        'CR Main Plaza - Tree': lambda state: logic.prime_can_super(state, multiworld, player),
        'CR Main Plaza - Locked Door': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                      state.has({'Morph Ball'}, player)),
        'CR Ruined Fountain': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                             logic.prime_can_bomb(state, multiworld, player) and
                                             logic.prime_can_spider(state, multiworld, player)),
        'CR Ruined Shrine - Plated Beetle': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                           state.has_any({'Morph Ball', 'Space Jump Boots'}, player)),
        'CR Ruined Shrine - Half-Pipe': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                       logic.prime_can_boost(state, multiworld, player)),
        'CR Ruined Shrine - Lower Tunnel': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                          (logic.prime_can_bomb(state, multiworld, player) or
                                                           logic.prime_can_pb(state, multiworld, player))),
        'CR Vault': lambda state: (logic.prime_has_missiles(state, multiworld, player)
                                   and logic.prime_can_bomb(state, multiworld, player)),
        'CR Training Chamber': lambda state: (logic.prime_magma_pool(state, multiworld, player) and
                                              logic.prime_can_bomb(state, multiworld, player) and
                                              state.has({'Boost Ball', 'Spider Ball', 'Wave Beam'}, player)),
        'CR Ruined Nursery': lambda state: logic.prime_can_bomb(state, multiworld, player),
        'CR Training Chamber Access': lambda state: (logic.prime_magma_pool(state, multiworld, player) and
                                                     logic.prime_can_bomb(state, multiworld, player) and
                                                     state.has({'Wave Beam'}, player)),
        'CR Magma Pool': lambda state: (logic.prime_magma_pool(state, multiworld, player) and
                                        logic.prime_can_pb(state, multiworld, player)),
        'CR Tower of Light': lambda state: (logic.prime_tower_of_light(state, multiworld, player) and
                                            (logic.prime_has_missile_count(state, multiworld, player) >= 40)),
        'CR Tower Chamber': lambda state: (logic.prime_tower_of_light(state, multiworld, player)
                                           and state.has({'Gravity Suit'}, player)),
        'CR Ruined Gallery - Missile Wall': lambda state: logic.prime_has_missiles(state, multiworld, player),
        'CR Ruined Gallery - Tunnel': lambda state: logic.prime_can_bomb(state, multiworld, player),
        'CR Transport Access North': lambda state: logic.prime_has_missiles(state, multiworld, player),
        'CR Gathering Hall': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                            state.has({'Space Jump Boots'}, player) and
                                            (logic.prime_can_bomb(state, multiworld, player) or
                                             logic.prime_can_pb(state, multiworld, player))),
        'CR Sunchamber - Flaaghra': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                   logic.prime_can_bomb(state, multiworld, player) and
                                                   logic.prime_etank_count(state, multiworld, player) >= 1),
        'CR Sunchamber - Ghosts': lambda state: (logic.prime_can_super(state, multiworld, player) and
                                                 logic.prime_can_bomb(state, multiworld, player) and
                                                 logic.prime_can_spider(state, multiworld, player)),
        'CR Watery Hall Access': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                state.has({'Morph Ball'}, player)),
        'CR Watery Hall - Scan Puzzle': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                       state.has({'Morph Ball'}, player)),
        'CR Watery Hall - Underwater': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                      logic.prime_can_bomb(state, multiworld, player) and
                                                      state.has({'Space Jump Boots', 'Gravity Suit'}, player)),
        'CR Dynamo - Lower': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                            (logic.prime_can_bomb(state, multiworld, player) or
                                             logic.prime_can_pb(state, multiworld, player))),
        'CR Dynamo - Spider Track': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                   (logic.prime_can_bomb(state, multiworld, player) or
                                                    logic.prime_can_pb(state, multiworld, player)) and
                                                   logic.prime_can_spider(state, multiworld, player)),
        'CR Burn Dome - Missile': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                 logic.prime_has_missiles(state, multiworld, player)),
        'CR Burn Dome - Incinerator Drone': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                           logic.prime_has_missiles(state, multiworld, player)),
        'CR Furnace - Spider Tracks': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                     logic.prime_can_bomb(state, multiworld, player) and
                                                     logic.prime_can_pb(state, multiworld, player) and
                                                     state.has({'Spider Ball', 'Boost Ball'}, player)),
        'CR Furnace - Inside Furnace': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                      logic.prime_has_missiles(state, multiworld, player)),
        'CR Hall of the Elders': lambda state: (logic.prime_late_chozo(state, multiworld, player) and
                                                logic.prime_can_bomb(state, multiworld, player) and
                                                state.has({'Space Jump Boots', 'Spider Ball', 'Ice Beam'}, player)),
        'CR Crossway': lambda state: (logic.prime_late_chozo(state, multiworld, player) and
                                      logic.prime_can_super(state, multiworld, player) and
                                      logic.prime_can_bomb(state, multiworld, player) and
                                      state.has({'Boost Ball', 'Spider Ball'}, player)),
        'CR Elder Chamber': lambda state: (logic.prime_late_chozo(state, multiworld, player) and
                                           logic.prime_can_bomb(state, multiworld, player) and
                                           state.has({'Space Jump Boots', 'Ice Beam', 'Plasma Beam'}, player)),
        'CR Antechamber': lambda state: (logic.prime_reflecting_pool(state, multiworld, player) and
                                         logic.prime_has_missiles(state, multiworld, player) and
                                         state.has({'Ice Beam'}, player)),

        # phendrana drifts locations
        'PD Phendrana Shorelines - Behind Ice': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                               state.has({'Plasma Beam'}, player)),
        'PD Phendrana Shorelines - Spider Track': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                                 logic.prime_can_super(state, multiworld, player) and
                                                                 logic.prime_can_spider(state, multiworld, player) and
                                                                 state.has({'Space Jump Boots'}, player)),
        'PD Chozo Ice Temple': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                              state.has({'Plasma Beam', 'Space Jump Boots'}, player)),
        'PD Ice Ruins West': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                            state.has({'Plasma Beam', 'Space Jump Boots'}, player)),
        'PD Ice Ruins East - Behind Ice': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                         state.has({'Plasma Beam'}, player)),
        'PD Ice Ruins East - Spider Track': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                           logic.prime_can_spider(state, multiworld, player)),
        'PD Chapel of the Elders': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                                  logic.prime_can_bomb(state, multiworld, player) and
                                                  state.has({'Space Jump Boots', 'Wave Beam'}, player)),
        'PD Ruined Courtyard': lambda state: (logic.prime_middle_phen(state, multiworld, player) and
                                              state.has({'Space Jump Boots', 'Wave Beam'}, player) and
                                              ((logic.prime_can_bomb(state, multiworld, player) and
                                               logic.prime_can_boost(state, multiworld, player)) or
                                               logic.prime_can_spider(state, multiworld, player))),
        'PD Phendrana Canyon': lambda state: (logic.prime_front_phen(state, multiworld, player) and
                                              (logic.prime_can_boost(state, multiworld, player) or
                                               state.has({'Space Jump Boots'}, player))),
        'PD Quarantine Cave': lambda state: (logic.prime_quarantine_cave(state, multiworld, player) and
                                             logic.prime_can_spider(state, multiworld, player) and
                                             state.has({'Thermal Visor'}, player) and
                                             logic.prime_etank_count(state, multiworld, player) >= 3),
        'PD Research Lab Hydra': lambda state: (logic.prime_labs(state, multiworld, player) and
                                                logic.prime_can_super(state, multiworld, player)),
        'PD Quarantine Monitor': lambda state: (logic.prime_quarantine_cave(state, multiworld, player) and
                                                logic.prime_can_spider(state, multiworld, player) and
                                                state.has({'Thermal Visor', 'Grapple Beam'}, player)),
        'PD Observatory': lambda state: (logic.prime_labs(state, multiworld, player) and
                                         logic.prime_can_bomb(state, multiworld, player) and
                                         logic.prime_can_boost(state, multiworld, player)),
        'PD Transport Access': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                              state.has({'Plasma Beam'}, player)),
        'PD Control Tower': lambda state: (logic.prime_labs(state, multiworld, player) and
                                           logic.prime_can_bomb(state, multiworld, player) and
                                           state.has({'Plasma Beam'}, player)),
        'PD Research Core': lambda state: logic.prime_labs(state, multiworld, player),
        'PD Frost Cave': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                        state.has({'Grapple Beam'}, player)),
        'PD Research Lab Aether - Tank': lambda state: logic.prime_labs(state, multiworld, player),
        'PD Research Lab Aether - Morph Track': lambda state: logic.prime_labs(state, multiworld, player),
        'PD Gravity Chamber - Underwater': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                                          state.has({'Gravity Suit'}, player)),
        'PD Gravity Chamber - Grapple Ledge': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                                             state.has({'Gravity Suit', 'Plasma Beam',
                                                                        'Grapple Beam'}, player)),
        'PD Storage Cave': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                          logic.prime_can_pb(state, multiworld, player) and
                                          state.has({'Plasma Beam', 'Grapple Beam'}, player)),
        'PD Security Cave': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                           logic.prime_can_pb(state, multiworld, player) and
                                           state.has({'Plasma Beam', 'Grapple Beam'}, player)),

        # tallon overworld locations
        'TO Landing Site': lambda state: state.has({'Morph Ball'}, player),
        'TO Alcove': lambda state: ((logic.prime_can_bomb(state, multiworld, player) and
                                     logic.prime_can_boost(state, multiworld, player)) or
                                    state.has({'Space Jump Boots'}, player)),
        'TO Frigate Crash Site': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                                state.has({'Space Jump Boots', 'Morph Ball', 'Gravity Suit'}, player)),
        'TO Overgrown Cavern': lambda state: (logic.prime_reflecting_pool(state, multiworld, player) and
                                              state.has({'Ice Beam', 'Morph Ball'}, player)),

        'TO Root Cave': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                       state.has({'Grapple Beam', 'Space Jump Boots', 'X-Ray Visor'}, player)),
        'TO Artifact Temple': lambda state: logic.prime_has_missiles(state, multiworld, player),
        'TO Transport Tunnel B': lambda state: logic.prime_has_missiles(state, multiworld, player),
        'TO Arbor Chamber': lambda state: (logic.prime_has_missiles(state, multiworld, player) and
                                           state.has({'Grapple Beam', 'Space Jump Boots', 'X-Ray Visor',
                                                      'Plasma Beam'}, player)),
        'TO Cargo Freight Lift to Deck Gamma': lambda state: logic.prime_frigate(state, multiworld, player),
        'TO Biohazard Containment': lambda state: (logic.prime_frigate(state, multiworld, player) and
                                                   logic.prime_can_super(state, multiworld, player)),
        'TO Hydro Access Tunnel': lambda state: (logic.prime_frigate(state, multiworld, player) and
                                                 logic.prime_can_bomb(state, multiworld, player)),
        'TO Great Tree Chamber': lambda state: (state.has({'X-Ray Visor', 'Ice Beam', 'Space Jump Boots'}, player) and
                                                (logic.prime_reflecting_pool(state, multiworld, player) or
                                                 (logic.prime_frigate(state, multiworld, player) and
                                                  logic.prime_can_bomb(state, multiworld, player) and
                                                  logic.prime_can_boost(state, multiworld, player)))),
        'TO Life Grove Tunnel': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                               logic.prime_can_boost(state, multiworld, player) and
                                               logic.prime_can_spider(state, multiworld, player) and
                                               logic.prime_can_pb(state, multiworld, player) and
                                               state.has({'Ice Beam', 'Space Jump Boots'}, player) and
                                               (logic.prime_frigate(state, multiworld, player) or
                                                logic.prime_reflecting_pool(state, multiworld, player))),
        'TO Life Grove - Start': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                logic.prime_can_boost(state, multiworld, player) and
                                                logic.prime_can_spider(state, multiworld, player) and
                                                logic.prime_can_pb(state, multiworld, player) and
                                                state.has({'Ice Beam', 'Space Jump Boots'}, player) and
                                                (logic.prime_frigate(state, multiworld, player) or
                                                 logic.prime_reflecting_pool(state, multiworld, player))),
        'TO Life Grove - Underwater Spinner': lambda state: (logic.prime_can_bomb(state, multiworld, player) and
                                                             logic.prime_can_boost(state, multiworld, player) and
                                                             logic.prime_can_spider(state, multiworld, player) and
                                                             logic.prime_can_pb(state, multiworld, player) and
                                                             state.has({'Ice Beam', 'Space Jump Boots'}, player) and
                                                             (logic.prime_frigate(state, multiworld, player) or
                                                              logic.prime_reflecting_pool(state, multiworld, player))),

        # phazon mines locations
        'PM Main Quarry': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                         logic.prime_can_bomb(state, multiworld, player) and
                                         logic.prime_can_spider(state, multiworld, player) and
                                         state.has({'Thermal Visor'}, player)),
        'PM Security Access A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                               logic.prime_can_pb(state, multiworld, player)),
        'PM Storage Depot B': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                             logic.prime_can_bomb(state, multiworld, player) and
                                             logic.prime_can_pb(state, multiworld, player) and
                                             logic.prime_can_spider(state, multiworld, player) and
                                             state.has({'Grapple Beam'}, player)),
        'PM Storage Depot A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                             logic.prime_can_pb(state, multiworld, player) and
                                             state.has({'Plasma Beam'}, player)),
        'PM Elite Research - Phazon Elite': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                           logic.prime_can_pb(state, multiworld, player)),
        'PM Elite Research - Laser': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                    logic.prime_can_bomb(state, multiworld, player) and
                                                    logic.prime_can_boost(state, multiworld, player)),
        'PM Elite Control Access': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                  logic.prime_can_bomb(state, multiworld, player) and
                                                  logic.prime_can_pb(state, multiworld, player) and
                                                  logic.prime_can_spider(state, multiworld, player) and
                                                  state.has({'Grapple Beam'}, player)),
        'PM Ventilation Shaft': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                               logic.prime_can_bomb(state, multiworld, player) and
                                               logic.prime_can_pb(state, multiworld, player) and
                                               logic.prime_can_spider(state, multiworld, player) and
                                               logic.prime_can_boost(state, multiworld, player) and
                                               state.has({'Grapple Beam'}, player)),
        'PM Phazon Processing Center': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                      logic.prime_can_bomb(state, multiworld, player) and
                                                      logic.prime_can_pb(state, multiworld, player) and
                                                      logic.prime_can_spider(state, multiworld, player) and
                                                      state.has({'Grapple Beam'}, player)),
        'PM Processing Center Access': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                      state.has({'X-Ray Visor'}, player)),
        'PM Elite Quarters': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                            state.has({'X-Ray Visor'}, player) and
                                            logic.prime_etank_count(state, multiworld, player) >= 7),
        'PM Central Dynamo': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                            logic.prime_can_bomb(state, multiworld, player) and
                                            logic.prime_can_pb(state, multiworld, player) and
                                            logic.prime_can_spider(state, multiworld, player) and
                                            state.has({'Grapple Beam', 'X-Ray Visor'}, player)),
        'PM Metroid Quarantine B': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                  logic.prime_can_super(state, multiworld, player)),
        'PM Metroid Quarantine A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                  logic.prime_can_bomb(state, multiworld, player) and
                                                  logic.prime_can_pb(state, multiworld, player) and
                                                  logic.prime_can_spider(state, multiworld, player) and
                                                  logic.prime_can_boost(state, multiworld, player) and
                                                  state.has({'Grapple Beam', 'X-Ray Visor'}, player)),
        'PM Fungal Hall B': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                           state.has_any({'Thermal Visor', 'X-Ray Visor'}, player)),
        'PM Phazon Mining Tunnel': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                  state.has({'Phazon Suit'}, player)),
        'PM Fungal Hall Access': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                logic.prime_can_bomb(state, multiworld, player) and
                                                logic.prime_can_pb(state, multiworld, player) and
                                                logic.prime_can_boost(state, multiworld, player) and
                                                state.has({'Grapple Beam', 'X-Ray Visor', 'Plasma Beam'}, player)),

        # magmoor caverns locations
        'MC Lava Lake': lambda state: (logic.prime_can_heat(state, multiworld, player) and
                                       logic.prime_has_missiles(state, multiworld, player) and
                                       state.has({'Morph Ball', 'Space Jump Boots'}, player)),
        'MC Triclops Pit': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                          logic.prime_has_missiles(state, multiworld, player) and
                                          state.has({'Space Jump Boots'}, player)),
        'MC Storage Cavern': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                            state.has({'Morph Ball'}, player)),
        'MC Transport Tunnel A': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                                logic.prime_can_bomb(state, multiworld, player)),
        'MC Warrior Shrine': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                            logic.prime_can_bomb(state, multiworld, player) and
                                            logic.prime_can_boost(state, multiworld, player) and
                                            state.has({'Space Jump Boots'}, player)),
        'MC Shore Tunnel': lambda state: (logic.prime_early_magmoor(state, multiworld, player) and
                                          logic.prime_can_pb(state, multiworld, player) and
                                          state.has({'Space Jump Boots'}, player)),
        'MC Fiery Shores - Morph Track': lambda state: (logic.prime_can_heat(state, multiworld, player) and
                                                        logic.prime_has_missiles(state, multiworld, player) and
                                                        logic.prime_can_bomb(state, multiworld, player)),
        'MC Fiery Shores - Warrior Shrine Tunnel': lambda state: (logic.prime_early_magmoor(state, multiworld, player)
                                                                  and logic.prime_can_bomb(state, multiworld, player)
                                                                  and logic.prime_can_boost(state, multiworld, player)
                                                                  and logic.prime_can_pb(state, multiworld, player)
                                                                  and state.has({'Space Jump Boots'}, player)),
        'MC Plasma Processing': lambda state: (logic.prime_late_magmoor(state, multiworld, player) and
                                               logic.prime_can_bomb(state, multiworld, player) and
                                               logic.prime_can_boost(state, multiworld, player) and
                                               logic.prime_can_spider(state, multiworld, player) and
                                               state.has({'Ice Beam', 'Plasma Beam', 'Grapple Beam'}, player)),
        'MC Magmoor Workstation': lambda state: (logic.prime_late_magmoor(state, multiworld, player) and
                                                 state.has({'Morph Ball', 'Wave Beam', 'Thermal Visor'}, player))
    }

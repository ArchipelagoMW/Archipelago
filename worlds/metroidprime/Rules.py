from worlds.generic.Rules import add_rule
from Logic import MetroidPrimeLogic as logic


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
                                                   logic.prime_can_bomb(state, multiworld, player)),
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
                                             state.has({'Thermal Visor'}, player)),
        'PD Research Lab Hydra': lambda state: (logic.prime_labs(state, multiworld, player) and
                                                logic.prime_can_super(state, multiworld, player)),
        'PD Quarantine Monitor': lambda state: (logic.prime_quarantine_cave(state, multiworld, player) and
                                                logic.prime_can_spider(state, multiworld, player) and
                                                state.has({'Thermal Visor', 'Grapple Beam'}, player)),
        'PD Observatory': lambda state: (logic.prime_labs(state, multiworld, player) and
                                         logic.prime_can_bomb(state, multiworld, player) and
                                         logic.prime_can_boost(state, multiworld. player)),
        'PD Transport Access': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                              state.has({'Plasma Beam'}, player)),
        'PD Control Tower': lambda state: (logic.prime_labs(state, multiworld, player) and
                                           logic.prime_can_bomb(state, multiworld, player) and
                                           state.has({'Plasma Beam'}, player)),
        'PD Research Core': lambda state: logic.prime_labs(state, multiworld, player),
        'PD Frost Cave': lambda state: (logic.prime_far_phen(state, multiworld, player) and
                                        state.has({'Grapple Beam'}, player)),
        'PD Research Lab Aether - Tank': lambda state: logic.prime_labs(state, multiworld, player),
        'PD Research Lab Aether - Morph Track': lambda state: logic.prime_labs(state, multiworld. player),
        'PD Gravity Chamber - Underwater': lambda state: (logic.prime_far_phen(state, multiworld. player) and
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
    }

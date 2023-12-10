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
    }

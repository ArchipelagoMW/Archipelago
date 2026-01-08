from BaseClasses import CollectionState
from ..BlastShieldRando import BlastShieldType
from ..DoorRando import DoorLockType
from ..LogicCombat import can_combat_flaahgra, can_combat_ghosts
from ..Items import SuitUpgrade
from ..data.AreaNames import MetroidPrimeArea
from .RoomData import AreaData, PickupData, RoomData
from .DoorData import DoorData
from ..Logic import (
    can_bomb,
    can_boost,
    can_grapple,
    can_heat,
    can_ice_beam,
    can_missile,
    can_morph_ball,
    can_move_underwater,
    can_plasma_beam,
    can_power_beam,
    can_power_bomb,
    can_scan,
    can_space_jump,
    can_spider,
    can_super_missile,
    can_wave_beam,
    has_energy_tanks,
    has_power_bomb_count,
)
from ..data.Tricks import Tricks
from .RoomNames import RoomName
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


def can_exit_ruined_shrine(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    item1 = world.get_location(
        "Chozo Ruins: Ruined Shrine - Plated Beetle"
    ).item
    if can_morph_ball(world, state) or can_space_jump(world, state):
        return True
    if (
        item1 is not None
        and item1.name in ["Morph Ball", "Space Jump Boots"]
        and item1.player == world.player
    ):
        return True
    return False


def can_climb_sun_tower(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    return (
        can_spider(world, state)
        and can_super_missile(world, state)
        and can_bomb(world, state)
    )


def can_flaahgra(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    bomb_req = can_bomb(world, state) or (
        can_power_bomb(world, state) and has_power_bomb_count(world, state, 4)
    )
    if world.starting_room_data.name == RoomName.Sunchamber_Lobby.value:
        return bomb_req
    return (
        state.can_reach_region(RoomName.Sunchamber.value, world.player)
        and can_combat_flaahgra(world, state)
        and can_missile(world, state)
        and can_scan(world, state)
        and bomb_req
    )


def can_climb_tower_of_light(
    world: "MetroidPrimeWorld", state: CollectionState
) -> bool:
    return (
        can_missile(world, state)
        and state.has(SuitUpgrade.Missile_Expansion.value, world.player, 8)
        and can_space_jump(world, state)
    )


class ChozoRuinsAreaData(AreaData):
    def __init__(self):
        super().__init__(MetroidPrimeArea.Chozo_Ruins.value)
        self.rooms = {
            #  Force blue to prevent softlocks
            RoomName.Antechamber: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Reflecting_Pool,
                        lock=DoorLockType.Blue,
                        defaultLock=DoorLockType.Ice,
                        exclude_from_rando=True,
                    )
                },
                pickups=[
                    PickupData("Chozo Ruins: Antechamber"),
                ],
            ),
            RoomName.Arboretum_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Arboretum),
                    1: DoorData(RoomName.Ruined_Fountain),
                }
            ),
            RoomName.Arboretum: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Sunchamber_Lobby,
                        rule_func=lambda world, state: (
                            can_bomb(world, state)
                            or (
                                bool(world.options.flaahgra_power_bombs.value)
                                and can_power_bomb(world, state)
                                and can_space_jump(world, state)
                            )
                        )
                        and can_scan(world, state),
                        blast_shield=BlastShieldType.Missile,
                        tricks=[Tricks.arboretum_scan_gate_skip],
                    ),
                    1: DoorData(
                        RoomName.Arboretum_Access, blast_shield=BlastShieldType.Missile
                    ),
                    2: DoorData(
                        RoomName.Gathering_Hall_Access,
                        blast_shield=BlastShieldType.Missile,
                    ),
                }
            ),
            RoomName.Burn_Dome_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Burn_Dome, rule_func=can_bomb),
                    1: DoorData(
                        RoomName.Energy_Core,
                        rule_func=can_bomb,
                        defaultLock=DoorLockType.None_,
                        exclude_from_rando=True,
                    ),
                }
            ),
            RoomName.Burn_Dome: RoomData(
                doors={
                    0: DoorData(RoomName.Burn_Dome_Access),
                },
                pickups=[
                    PickupData("Chozo Ruins: Burn Dome - Missile", rule_func=can_bomb),
                    PickupData("Chozo Ruins: Burn Dome - Incinerator Drone"),
                ],
            ),
            RoomName.Crossway_Access_South: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Crossway,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_morph_ball,
                    ),
                    1: DoorData(
                        RoomName.Hall_of_the_Elders,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_morph_ball,
                    ),
                }
            ),
            RoomName.Crossway_Access_West: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Crossway,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_morph_ball,
                    ),
                    1: DoorData(
                        RoomName.Furnace,
                        rule_func=can_morph_ball,
                        exclude_from_rando=True,
                    ),
                },
                pickups=[],
            ),
            RoomName.Crossway: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Crossway_Access_South, defaultLock=DoorLockType.Ice
                    ),
                    1: DoorData(RoomName.Crossway_Access_West),
                    2: DoorData(
                        RoomName.Elder_Hall_Access,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=lambda world, state: can_boost(world, state),
                        tricks=[Tricks.crossway_hpbj],
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Crossway",
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_boost(world, state)
                        and can_spider(world, state)
                        and can_super_missile(world, state)
                        and can_scan(world, state),
                        tricks=[Tricks.crossway_item_fewer_reqs],
                    ),
                ],
            ),
            RoomName.Dynamo_Access: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Watery_Hall,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=can_bomb,
                    ),
                    1: DoorData(
                        RoomName.Dynamo, destination_area=MetroidPrimeArea.Chozo_Ruins
                    ),
                },
            ),
            RoomName.Dynamo: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Dynamo_Access,
                        destination_area=MetroidPrimeArea.Chozo_Ruins,
                    ),
                },
                pickups=[
                    PickupData("Chozo Ruins: Dynamo - Lower", rule_func=can_missile),
                    PickupData(
                        "Chozo Ruins: Dynamo - Spider Track",
                        rule_func=lambda world, state: can_spider(world, state),
                    ),
                ],
            ),
            RoomName.East_Atrium: RoomData(
                doors={
                    0: DoorData(RoomName.Gathering_Hall),
                    1: DoorData(RoomName.Energy_Core_Access),
                }
            ),
            RoomName.East_Furnace_Access: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Hall_of_the_Elders, defaultLock=DoorLockType.Ice
                    ),
                    1: DoorData(RoomName.Furnace, defaultLock=DoorLockType.Ice),
                }
            ),
            RoomName.Elder_Chamber: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Hall_of_the_Elders, defaultLock=DoorLockType.Ice
                    ),
                },
                pickups=[PickupData("Chozo Ruins: Elder Chamber")],
            ),
            RoomName.Elder_Hall_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Hall_of_the_Elders),
                    1: DoorData(
                        RoomName.Crossway, blast_shield=BlastShieldType.Missile
                    ),
                }
            ),
            RoomName.Energy_Core_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Energy_Core),
                    1: DoorData(RoomName.East_Atrium),
                }
            ),
            RoomName.Energy_Core: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Burn_Dome_Access,
                        defaultLock=DoorLockType.None_,
                        rule_func=can_bomb,
                        exclude_from_rando=True,
                    ),  # Bombs are required to get out of here
                    1: DoorData(RoomName.West_Furnace_Access, rule_func=can_bomb),
                    2: DoorData(RoomName.Energy_Core_Access),
                }
            ),
            RoomName.Eyon_Tunnel: RoomData(
                doors={
                    0: DoorData(RoomName.Ruined_Nursery),
                    1: DoorData(RoomName.Nursery_Access),
                }
            ),
            RoomName.Furnace: RoomData(
                doors={
                    0: DoorData(
                        RoomName.East_Furnace_Access,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_space_jump,
                    ),
                    1: DoorData(RoomName.West_Furnace_Access, rule_func=can_bomb),
                    2: DoorData(
                        RoomName.Crossway_Access_West,
                        exclude_from_rando=True,
                        rule_func=can_morph_ball,
                        defaultLock=DoorLockType.None_,
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Furnace - Spider Tracks",
                        rule_func=lambda world, state: can_power_bomb(world, state)
                        and can_boost(world, state)
                        and can_spider(world, state),
                        tricks=[
                            Tricks.furnace_spider_track_hbj,
                            Tricks.furnace_spider_track_sj_bombs,
                        ],
                    ),
                    PickupData(
                        "Chozo Ruins: Furnace - Inside Furnace", exclude_from_logic=True
                    ),
                ],
            ),
            RoomName.Gathering_Hall_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Gathering_Hall),
                    1: DoorData(
                        RoomName.Arboretum, blast_shield=BlastShieldType.Missile
                    ),
                }
            ),
            RoomName.Gathering_Hall: RoomData(
                doors={
                    0: DoorData(RoomName.Watery_Hall_Access),
                    1: DoorData(
                        RoomName.Gathering_Hall_Access,
                        blast_shield=BlastShieldType.Missile,
                    ),
                    2: DoorData(
                        RoomName.Save_Station_2, blast_shield=BlastShieldType.Missile
                    ),
                    3: DoorData(
                        RoomName.East_Atrium,
                        rule_func=lambda world, state: can_morph_ball(world, state)
                        or can_space_jump(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Gathering Hall",
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and (can_bomb(world, state) or can_power_bomb(world, state)),
                        tricks=[Tricks.gathering_hall_without_space_jump],
                    )
                ],
            ),
            RoomName.Hall_of_the_Elders: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Reflecting_Pool_Access,
                        rule_func=lambda world, state: can_combat_ghosts(world, state)
                        and can_bomb(world, state)
                        and can_spider(world, state)
                        and can_wave_beam(world, state)
                        and can_space_jump(world, state),
                        tricks=[
                            Tricks.hall_of_elders_reflecting_pool_no_spider,
                            Tricks.hall_of_elders_reflecting_pool_no_wave_beam,
                        ],
                    ),
                    1: DoorData(
                        RoomName.Elder_Hall_Access,
                        rule_func=lambda world, state: can_combat_ghosts(world, state)
                        and can_boost(world, state)
                        and can_missile(world, state)
                        and can_space_jump(world, state),
                    ),
                    2: DoorData(
                        RoomName.East_Furnace_Access,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_combat_ghosts(world, state)
                        and can_power_beam(world, state),
                    ),
                    3: DoorData(
                        RoomName.Crossway_Access_South,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_combat_ghosts(world, state)
                        and can_power_beam(world, state),
                    ),
                    4: DoorData(
                        RoomName.Elder_Chamber,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_combat_ghosts(world, state)
                        and can_bomb(world, state)
                        and can_plasma_beam(world, state)
                        and can_space_jump(world, state)
                        and can_spider(world, state),
                        tricks=[Tricks.hall_of_elders_elder_chamber_no_spider],
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Hall of the Elders",
                        rule_func=lambda world, state: can_combat_ghosts(world, state)
                        and can_power_beam(world, state)
                        and can_bomb(world, state)
                        and can_spider(world, state)
                        and can_ice_beam(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.hall_of_elders_item_no_spider],
                    ),
                ],
            ),
            RoomName.Hive_Totem: RoomData(
                doors={
                    0: DoorData(RoomName.Totem_Access),
                    1: DoorData(
                        RoomName.Transport_Access_North,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=lambda world, state: can_power_beam(world, state)
                        or bool(world.options.remove_hive_mecha.value),
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Hive Totem",
                        rule_func=lambda world, state: can_power_beam(world, state)
                        or bool(world.options.remove_hive_mecha.value),
                    ),
                ],
            ),
            RoomName.Magma_Pool: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Training_Chamber_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_grapple(world, state)
                        and can_heat(world, state),
                        tricks=[
                            Tricks.magma_pool_scan_dash,
                            Tricks.magma_pool_debris_jump,
                        ],
                    ),
                    1: DoorData(
                        RoomName.Meditation_Fountain,
                        rule_func=lambda world, state: has_energy_tanks(world, state, 1)
                        and (
                            state.has(SuitUpgrade.Varia_Suit.value, world.player)
                            or state.has(SuitUpgrade.Gravity_Suit.value, world.player)
                            or state.has(SuitUpgrade.Phazon_Suit.value, world.player)
                        ),
                    ),  # Damage reduction lets player cross
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Magma Pool",
                        rule_func=lambda world, state: can_grapple(world, state)
                        and can_heat(world, state)
                        and can_power_bomb(world, state),
                        tricks=[
                            Tricks.magma_pool_item_infinite_speed,
                            Tricks.magma_pool_item_scan_dash,
                            Tricks.magma_pool_item_debris_jump,
                        ],
                    ),
                ],
            ),
            RoomName.Main_Plaza: RoomData(
                doors={
                    0: DoorData(RoomName.Ruined_Fountain_Access),
                    1: DoorData(RoomName.Ruins_Entrance),
                    2: DoorData(
                        RoomName.Ruined_Shrine_Access,
                        blast_shield=BlastShieldType.Missile,
                    ),
                    3: DoorData(RoomName.Nursery_Access),
                    4: DoorData(
                        RoomName.Plaza_Access,
                        rule_func=lambda world, state: False,
                        tricks=[Tricks.vault_via_plaza],
                    ),
                    5: DoorData(
                        RoomName.Piston_Tunnel, rule_func=lambda world, state: False
                    ),  # Piston tunnel to training chamber is blocked by a chozo head that needs to be destroyed from the other side
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Main Plaza - Half-Pipe",
                        rule_func=can_boost,
                        tricks=[
                            Tricks.plaza_half_pipe_no_boost,
                            Tricks.plaza_half_pipe_morph_only,
                        ],
                    ),
                    PickupData(
                        "Chozo Ruins: Main Plaza - Grapple Ledge",
                        rule_func=lambda world, state: state.can_reach_region(
                            RoomName.Piston_Tunnel.value, world.player
                        )
                        and can_grapple(world, state),
                        tricks=[Tricks.plaza_grapple_ledge_r_jump],
                    ),
                    PickupData(
                        "Chozo Ruins: Main Plaza - Tree",
                        rule_func=can_super_missile,
                        tricks=[],
                    ),
                    PickupData(
                        "Chozo Ruins: Main Plaza - Locked Door",
                        rule_func=lambda world, state: state.can_reach_region(
                            RoomName.Plaza_Access.value, world.player
                        )
                        and can_morph_ball(world, state),
                        tricks=[Tricks.vault_via_plaza],
                    ),
                ],
            ),  # If we do room rando, the logic for this will need to be adjusted
            RoomName.Map_Station: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(RoomName.Ruined_Gallery),
                },
            ),
            RoomName.Meditation_Fountain: RoomData(
                doors={
                    0: DoorData(RoomName.Magma_Pool),
                    1: DoorData(RoomName.Ruined_Fountain),
                }
            ),
            RoomName.North_Atrium: RoomData(
                doors={
                    0: DoorData(RoomName.Ruined_Nursery),
                    1: DoorData(RoomName.Ruined_Gallery),
                }
            ),
            RoomName.Nursery_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Eyon_Tunnel),
                    1: DoorData(RoomName.Main_Plaza),
                }
            ),
            RoomName.Piston_Tunnel: RoomData(
                doors={
                    0: DoorData(RoomName.Main_Plaza, rule_func=can_morph_ball),
                    1: DoorData(RoomName.Training_Chamber, rule_func=can_morph_ball),
                }
            ),
            RoomName.Plaza_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Main_Plaza),
                    1: DoorData(RoomName.Vault),
                }
            ),
            RoomName.Reflecting_Pool_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Reflecting_Pool),
                    1: DoorData(RoomName.Hall_of_the_Elders),
                }
            ),
            RoomName.Reflecting_Pool: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Save_Station_3,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=lambda world, state: can_boost(world, state)
                        and can_bomb(world, state),
                        tricks=[
                            Tricks.reflecting_pool_space_jump_climb,
                            Tricks.reflecting_pool_nsj_climb,
                        ],
                    ),
                    1: DoorData(
                        RoomName.Transport_Access_South,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_boost(world, state)
                        and can_bomb(world, state),
                        tricks=[
                            Tricks.reflecting_pool_space_jump_climb,
                            Tricks.reflecting_pool_nsj_climb,
                        ],
                    ),
                    2: DoorData(RoomName.Reflecting_Pool_Access),
                    3: DoorData(
                        RoomName.Antechamber,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=lambda world, state: can_boost(world, state)
                        and can_bomb(world, state),
                        tricks=[
                            Tricks.reflecting_pool_space_jump_climb,
                            Tricks.reflecting_pool_nsj_climb,
                        ],
                    ),
                }
            ),
            RoomName.Ruined_Fountain_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Main_Plaza, rule_func=can_morph_ball),
                    1: DoorData(RoomName.Ruined_Fountain, rule_func=can_morph_ball),
                }
            ),
            RoomName.Ruined_Fountain: RoomData(
                doors={
                    0: DoorData(RoomName.Arboretum_Access),
                    1: DoorData(RoomName.Ruined_Fountain_Access),
                    2: DoorData(RoomName.Meditation_Fountain),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Ruined Fountain",
                        rule_func=lambda world, state: world.get_location(
                            "Chozo Ruins: Sunchamber - Flaahgra"
                        ).can_reach(state)
                        and can_spider(world, state),
                    )
                ],
            ),  # This location can accidentally be locked out if flaahgra is skipped
            RoomName.Ruined_Gallery: RoomData(
                doors={
                    0: DoorData(RoomName.North_Atrium),
                    1: DoorData(RoomName.Totem_Access),
                    2: DoorData(
                        RoomName.Map_Station,
                        destination_area=MetroidPrimeArea.Chozo_Ruins,
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Ruined Gallery - Missile Wall",
                        rule_func=can_missile,
                    ),
                    PickupData(
                        "Chozo Ruins: Ruined Gallery - Tunnel", rule_func=can_bomb
                    ),
                ],
            ),
            RoomName.Ruined_Nursery: RoomData(
                doors={
                    0: DoorData(RoomName.Save_Station_1),
                    1: DoorData(RoomName.North_Atrium),
                    2: DoorData(RoomName.Eyon_Tunnel),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Ruined Nursery",
                        rule_func=can_bomb,
                        tricks=[Tricks.ruined_nursery_no_bombs],
                    ),
                ],
            ),
            RoomName.Ruined_Shrine_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Ruined_Shrine),
                    1: DoorData(
                        RoomName.Main_Plaza, blast_shield=BlastShieldType.Missile
                    ),
                }
            ),
            RoomName.Ruined_Shrine: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Tower_of_Light_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_spider(world, state)
                        and can_boost(world, state),
                        tricks=[
                            Tricks.ruined_shrine_upper_door_no_spider_ball,
                            Tricks.ruined_shrine_upper_door_scan_dash,
                        ],
                    ),
                    1: DoorData(
                        RoomName.Ruined_Shrine_Access,
                        rule_func=lambda world, state: can_morph_ball(world, state)
                        or can_space_jump(world, state),
                        tricks=[Tricks.ruined_shrine_scan_dash_escape],
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Ruined Shrine - Plated Beetle",
                        rule_func=can_exit_ruined_shrine,
                        tricks=[Tricks.ruined_shrine_scan_dash_escape],
                    ),
                    PickupData(
                        "Chozo Ruins: Ruined Shrine - Half-Pipe", rule_func=can_boost
                    ),
                    PickupData(
                        "Chozo Ruins: Ruined Shrine - Lower Tunnel",
                        rule_func=lambda world, state: can_bomb(world, state)
                        or can_power_bomb(world, state),
                    ),
                ],
            ),
            RoomName.Ruins_Entrance: RoomData(
                doors={
                    0: DoorData(RoomName.Main_Plaza),
                    1: DoorData(RoomName.Transport_to_Tallon_Overworld_North),
                }
            ),
            RoomName.Save_Station_1: RoomData(
                doors={
                    0: DoorData(RoomName.Ruined_Nursery),
                },
                pickups=[],
            ),
            RoomName.Save_Station_2: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Gathering_Hall, blast_shield=BlastShieldType.Missile
                    ),
                }
            ),
            RoomName.Save_Station_3: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Reflecting_Pool,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=can_bomb,
                    ),
                    1: DoorData(
                        RoomName.Transport_to_Tallon_Overworld_East, rule_func=can_bomb
                    ),
                }
            ),
            RoomName.Sun_Tower: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Sun_Tower_Access,
                        rule_func=can_climb_sun_tower,
                        exclude_from_rando=True,
                    ),
                    1: DoorData(RoomName.Transport_to_Magmoor_Caverns_North),
                }
            ),
            RoomName.Sun_Tower_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Sunchamber, exclude_from_rando=True),
                    1: DoorData(RoomName.Sun_Tower, exclude_from_rando=True),
                }
            ),
            RoomName.Sunchamber_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Sunchamber),
                    1: DoorData(RoomName.Sunchamber_Lobby),
                },
            ),
            RoomName.Sunchamber_Lobby: RoomData(
                doors={
                    0: DoorData(RoomName.Sunchamber_Access),
                    1: DoorData(
                        RoomName.Arboretum, rule_func=lambda world, state: False
                    ),
                }
            ),
            RoomName.Sunchamber: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Sun_Tower_Access,
                        rule_func=can_flaahgra,
                        exclude_from_rando=True,
                    )
                    # 1: DoorData(RoomName.Sunchamber_Lobby, rule_func=can_climb_sun_tower) # gets locked until after you beat the ghosts
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Sunchamber - Flaahgra", rule_func=can_flaahgra
                    ),
                    PickupData(
                        "Chozo Ruins: Sunchamber - Ghosts",
                        rule_func=lambda world, state: can_flaahgra(world, state)
                        and can_combat_ghosts(world, state)
                        and can_climb_sun_tower(world, state),
                    ),
                ],
            ),
            RoomName.Totem_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Ruined_Gallery),
                    1: DoorData(RoomName.Hive_Totem),
                }
            ),
            RoomName.Tower_Chamber: RoomData(
                doors={
                    0: DoorData(RoomName.Tower_of_Light, defaultLock=DoorLockType.Wave),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Tower Chamber",
                        rule_func=lambda world, state: True,
                    ),
                ],
            ),
            RoomName.Tower_of_Light_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Tower_of_Light, defaultLock=DoorLockType.Wave),
                    1: DoorData(RoomName.Ruined_Shrine),
                }
            ),
            RoomName.Tower_of_Light: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Tower_of_Light_Access, defaultLock=DoorLockType.Wave
                    ),
                    1: DoorData(
                        RoomName.Tower_Chamber,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_move_underwater(world, state)
                        and can_space_jump(world, state),
                        tricks=[
                            Tricks.tower_chamber_no_gravity,
                            Tricks.tower_chamber_no_space_jump,
                        ],
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Tower of Light",
                        rule_func=can_climb_tower_of_light,
                        tricks=[
                            Tricks.tower_of_light_climb_without_missiles,
                            Tricks.tower_of_light_climb_nsj,
                        ],
                    )
                ],
            ),
            RoomName.Training_Chamber_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Magma_Pool, defaultLock=DoorLockType.Wave),
                    1: DoorData(
                        RoomName.Training_Chamber, defaultLock=DoorLockType.Wave
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Training Chamber Access", rule_func=can_morph_ball
                    )
                ],
            ),
            RoomName.Training_Chamber: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Training_Chamber_Access, defaultLock=DoorLockType.Wave
                    ),
                    1: DoorData(
                        RoomName.Piston_Tunnel,
                        rule_func=lambda world, state: can_boost(world, state)
                        and can_bomb(world, state)
                        and can_combat_ghosts(world, state)
                        and can_power_beam(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Training Chamber",
                        rule_func=lambda world, state: can_boost(world, state)
                        and can_spider(world, state)
                        and can_bomb(world, state)
                        and can_power_beam(world, state)
                        and can_combat_ghosts(world, state),
                    )
                ],
            ),
            RoomName.Transport_Access_North: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Hive_Totem,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=can_bomb,
                    ),
                    1: DoorData(
                        RoomName.Transport_to_Magmoor_Caverns_North,
                        rule_func=can_morph_ball,
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Transport Access North",
                        lambda world, state: can_bomb(world, state)
                        or (
                            state.can_reach(
                                RoomName.Hive_Totem.value, None, world.player
                            )
                            and can_missile(world, state)
                        ),
                    )
                ],
            ),
            RoomName.Transport_Access_South: RoomData(
                doors={
                    0: DoorData(RoomName.Reflecting_Pool, defaultLock=DoorLockType.Ice),
                    1: DoorData(
                        RoomName.Transport_to_Tallon_Overworld_South,
                        destination_area=MetroidPrimeArea.Chozo_Ruins,
                    ),
                }
            ),
            RoomName.Transport_to_Magmoor_Caverns_North: RoomData(
                doors={
                    0: DoorData(RoomName.Sun_Tower),
                    1: DoorData(RoomName.Vault_Access),
                    2: DoorData(RoomName.Transport_Access_North),
                }
            ),
            RoomName.Transport_to_Tallon_Overworld_East: RoomData(
                doors={
                    0: DoorData(RoomName.Save_Station_3),
                }
            ),
            RoomName.Transport_to_Tallon_Overworld_North: RoomData(
                doors={0: DoorData(RoomName.Ruins_Entrance)}
            ),
            RoomName.Transport_to_Tallon_Overworld_South: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(RoomName.Transport_Access_South),
                },
            ),
            RoomName.Vault_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Vault, rule_func=can_morph_ball),
                    1: DoorData(
                        RoomName.Transport_to_Magmoor_Caverns_North,
                        rule_func=can_morph_ball,
                    ),
                }
            ),
            RoomName.Vault: RoomData(
                doors={
                    0: DoorData(RoomName.Vault_Access),
                    1: DoorData(RoomName.Plaza_Access),
                },
                pickups=[
                    PickupData("Chozo Ruins: Vault", rule_func=can_bomb),
                ],
            ),
            RoomName.Watery_Hall_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Gathering_Hall),
                    1: DoorData(
                        RoomName.Watery_Hall, blast_shield=BlastShieldType.Missile
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Watery Hall Access", rule_func=can_missile
                    ),
                ],
            ),
            RoomName.Watery_Hall: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Dynamo_Access,
                        destination_area=MetroidPrimeArea.Chozo_Ruins,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=lambda world, state: can_scan(world, state)
                        and (can_power_bomb(world, state) or can_bomb(world, state)),
                    ),
                    1: DoorData(
                        RoomName.Watery_Hall_Access,
                        blast_shield=BlastShieldType.Missile,
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Watery Hall - Scan Puzzle", rule_func=can_scan
                    ),
                    PickupData(
                        "Chozo Ruins: Watery Hall - Underwater",
                        rule_func=lambda world, state: can_move_underwater(world, state)
                        and can_space_jump(world, state)
                        and can_flaahgra(world, state),
                        tricks=[
                            Tricks.watery_hall_no_gravity,
                            Tricks.watery_hall_no_gravity_no_space_jump,
                        ],
                    ),
                ],
            ),
            RoomName.West_Furnace_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Energy_Core),
                    1: DoorData(
                        RoomName.Furnace,
                        rule_func=lambda world, state: can_spider(world, state)
                        and can_bomb(world, state),
                        tricks=[Tricks.furnace_no_spider_ball],
                        exclude_from_rando=True,
                    ),
                },
                pickups=[
                    PickupData(
                        "Chozo Ruins: Furnace - Inside Furnace",
                        rule_func=can_bomb,
                        exclude_from_config=True,
                    )
                ],
            ),  # This is not actually in west furnace, but it can only be accessed from west furnace, logic-wise
        }
        self._init_room_names_and_areas()

from BaseClasses import CollectionState
from ..BlastShieldRando import BlastShieldType
from ..DoorRando import DoorLockType
from ..LogicCombat import can_combat_labs, can_combat_thardus
from .Tricks import Tricks
from .AreaNames import MetroidPrimeArea
from .RoomData import AreaData, PickupData, RoomData
from .DoorData import DoorData
from ..Logic import (
    can_bomb,
    can_boost,
    can_charge_beam,
    can_defeat_sheegoth,
    can_grapple,
    can_melt_ice,
    can_missile,
    can_morph_ball,
    can_move_underwater,
    can_plasma_beam,
    can_power_bomb,
    can_scan,
    can_space_jump,
    can_spider,
    can_super_missile,
    can_thermal,
    can_wave_beam,
    can_xray,
)
from .RoomNames import RoomName
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


def _can_reach_top_of_ruined_courtyard(
    world: "MetroidPrimeWorld", state: CollectionState
):
    return (
        (can_boost(world, state) and can_bomb(world, state) and can_scan(world, state))
        or can_spider(world, state)
    ) and can_space_jump(world, state)


def _can_climb_observatory_via_puzzle(
    world: "MetroidPrimeWorld", state: CollectionState
):
    return (
        can_boost(world, state)
        and can_bomb(world, state)
        and can_space_jump(world, state)
        and can_scan(world, state)
    )


class PhendranaDriftsAreaData(AreaData):
    def __init__(self):
        super().__init__(MetroidPrimeArea.Phendrana_Drifts.value)
        self.rooms = {
            RoomName.Aether_Lab_Entryway: RoomData(
                doors={
                    0: DoorData(RoomName.East_Tower, defaultLock=DoorLockType.Wave),
                    1: DoorData(
                        RoomName.Research_Lab_Aether, defaultLock=DoorLockType.Wave
                    ),
                }
            ),
            RoomName.Canyon_Entryway: RoomData(
                doors={
                    0: DoorData(RoomName.Phendrana_Canyon),
                    1: DoorData(
                        RoomName.Ice_Ruins_West, blast_shield=BlastShieldType.Missile
                    ),
                }
            ),
            RoomName.Chamber_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Hunter_Cave, defaultLock=DoorLockType.Wave),
                    1: DoorData(
                        RoomName.Gravity_Chamber, defaultLock=DoorLockType.Wave
                    ),
                }
            ),
            RoomName.Chapel_of_the_Elders: RoomData(
                doors={
                    # Force blue to prevent soft lock
                    0: DoorData(
                        RoomName.Chapel_Tunnel,
                        lock=DoorLockType.Blue,
                        defaultLock=DoorLockType.Wave,
                        exclude_from_rando=True,
                        rule_func=lambda world, state: can_defeat_sheegoth(world, state)
                        and can_space_jump(world, state)
                        and can_wave_beam(world, state),
                        tricks=[Tricks.chapel_of_elders_escape_no_sj],
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Chapel of the Elders",
                        rule_func=lambda world, state: can_space_jump(world, state),
                        tricks=[Tricks.chapel_of_elders_escape_no_sj],
                    ),
                ],
            ),
            RoomName.Chapel_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Chapel_of_the_Elders,
                        rule_func=lambda world, state: can_bomb(world, state),
                    ),
                    1: DoorData(
                        RoomName.Chozo_Ice_Temple,
                        rule_func=lambda world, state: can_bomb(world, state),
                    ),
                }
            ),
            RoomName.Chozo_Ice_Temple: RoomData(
                doors={
                    0: DoorData(RoomName.Temple_Entryway),
                    1: DoorData(
                        RoomName.Chapel_Tunnel,
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_space_jump(world, state)
                        and can_missile(world, state),
                        tricks=[Tricks.ice_temple_to_chapel_no_sj],
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Chozo Ice Temple",
                        rule_func=lambda world, state: can_morph_ball(world, state)
                        and can_space_jump(world, state)
                        and can_melt_ice(world, state),
                    ),
                ],
            ),
            RoomName.Control_Tower: RoomData(
                doors={
                    0: DoorData(
                        RoomName.East_Tower,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_combat_labs,
                    ),
                    1: DoorData(
                        RoomName.West_Tower,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_combat_labs,
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Control Tower",
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_space_jump(world, state)
                        and can_missile(world, state)
                        and can_melt_ice(world, state)
                        and can_bomb(world, state),
                        tricks=[Tricks.control_tower_item_no_plasma],
                    ),
                ],
            ),
            RoomName.Courtyard_Entryway: RoomData(
                doors={
                    0: DoorData(RoomName.Ruined_Courtyard),
                    1: DoorData(RoomName.Ice_Ruins_West),
                }
            ),
            RoomName.East_Tower: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Aether_Lab_Entryway,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_scan,
                    ),
                    1: DoorData(RoomName.Control_Tower, defaultLock=DoorLockType.Wave),
                }
            ),
            RoomName.Frost_Cave_Access: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Frozen_Pike,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_bomb,
                    ),
                    1: DoorData(
                        RoomName.Frost_Cave,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_bomb,
                    ),
                }
            ),
            RoomName.Frost_Cave: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Save_Station_C,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_missile(world, state),
                    ),
                    1: DoorData(
                        RoomName.Frost_Cave_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_space_jump,
                    ),
                    2: DoorData(
                        RoomName.Upper_Edge_Tunnel,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_missile(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Frost Cave",
                        rule_func=lambda world, state: can_grapple(world, state)
                        and can_missile(world, state)
                        and can_move_underwater(world, state),
                        tricks=[Tricks.frost_cave_no_grapple],
                    ),
                ],
            ),
            RoomName.Frozen_Pike: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Pike_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_space_jump,
                    ),
                    1: DoorData(
                        RoomName.Transport_Access,
                        defaultLock=DoorLockType.Wave,
                        destination_area=MetroidPrimeArea.Phendrana_Drifts,
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.frozen_pike_no_bombs],
                    ),
                    2: DoorData(
                        RoomName.Frost_Cave_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_space_jump,
                    ),
                    3: DoorData(
                        RoomName.Hunter_Cave_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_move_underwater(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.frozen_pike_no_gravity_suit],
                    ),
                }
            ),
            RoomName.Gravity_Chamber: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Lake_Tunnel,
                        destination_area=MetroidPrimeArea.Phendrana_Drifts,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_move_underwater(world, state)
                        and can_space_jump(world, state),
                    ),  # Must have gravity
                    1: DoorData(
                        RoomName.Chamber_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_move_underwater(world, state)
                        and can_space_jump(world, state),
                    ),  # Must have gravity
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Gravity Chamber - Underwater",
                        rule_func=lambda world, state: can_move_underwater(world, state)
                        and can_space_jump(world, state),
                    ),  # Must have gravity
                    PickupData(
                        "Phendrana Drifts: Gravity Chamber - Grapple Ledge",
                        rule_func=lambda world, state: can_move_underwater(world, state)
                        and can_space_jump(world, state)
                        and can_melt_ice(world, state)
                        and can_grapple(world, state),
                        tricks=[Tricks.gravity_chamber_no_grapple_plasma],
                    ),
                ],
            ),  # Must have gravity
            RoomName.Hunter_Cave_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Frozen_Pike, defaultLock=DoorLockType.Wave),
                    1: DoorData(RoomName.Hunter_Cave, defaultLock=DoorLockType.Wave),
                }
            ),
            RoomName.Hunter_Cave: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Hunter_Cave_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_missile(world, state)
                        and can_grapple(world, state)
                        and can_space_jump(world, state),
                    ),
                    1: DoorData(
                        RoomName.Lower_Edge_Tunnel,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_space_jump,
                    ),
                    2: DoorData(
                        RoomName.Chamber_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_grapple(world, state),
                    ),
                    3: DoorData(
                        RoomName.Lake_Tunnel,
                        destination_area=MetroidPrimeArea.Phendrana_Drifts,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_missile(world, state),
                    ),
                }
            ),
            RoomName.Hydra_Lab_Entryway: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Research_Lab_Hydra, defaultLock=DoorLockType.Wave
                    ),
                    1: DoorData(
                        RoomName.Research_Entrance, defaultLock=DoorLockType.Wave
                    ),
                }
            ),
            RoomName.Ice_Ruins_Access: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Ice_Ruins_East,
                        rule_func=lambda world, state: can_missile(world, state)
                        or can_charge_beam(world, state),
                    ),
                    1: DoorData(
                        RoomName.Phendrana_Shorelines,
                        rule_func=lambda world, state: can_missile(world, state)
                        or can_charge_beam(world, state),
                    ),
                }
            ),
            RoomName.Ice_Ruins_East: RoomData(
                doors={
                    0: DoorData(RoomName.Ice_Ruins_Access),
                    1: DoorData(RoomName.Plaza_Walkway),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Ice Ruins East - Behind Ice",
                        rule_func=can_melt_ice,
                    ),
                    PickupData(
                        "Phendrana Drifts: Ice Ruins East - Spider Track",
                        rule_func=can_spider,
                    ),
                ],
            ),
            RoomName.Ice_Ruins_West: RoomData(
                doors={
                    0: DoorData(RoomName.Ruins_Entryway),
                    1: DoorData(
                        RoomName.Courtyard_Entryway,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_space_jump(world, state),
                    ),
                    2: DoorData(
                        RoomName.Canyon_Entryway, blast_shield=BlastShieldType.Missile
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Ice Ruins West",
                        rule_func=lambda world, state: can_melt_ice(world, state)
                        and can_space_jump(world, state)
                        and can_missile(world, state),
                    ),
                ],
            ),
            RoomName.Lake_Tunnel: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(RoomName.Hunter_Cave, defaultLock=DoorLockType.Wave),
                    1: DoorData(
                        RoomName.Gravity_Chamber, defaultLock=DoorLockType.Wave
                    ),
                },
            ),
            RoomName.Lower_Edge_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Phendranas_Edge,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_morph_ball,
                    ),
                    1: DoorData(
                        RoomName.Hunter_Cave,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_morph_ball,
                    ),
                }
            ),
            RoomName.Map_Station: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(RoomName.Research_Entrance),
                },
            ),
            RoomName.North_Quarantine_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Quarantine_Cave,
                        rule_func=can_morph_ball,
                        defaultLock=DoorLockType.Wave,
                    ),
                    1: DoorData(
                        RoomName.Quarantine_Access,
                        rule_func=can_morph_ball,
                        defaultLock=DoorLockType.Wave,
                    ),
                }
            ),
            RoomName.Observatory_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Observatory, defaultLock=DoorLockType.Wave),
                    1: DoorData(
                        RoomName.Research_Lab_Hydra, defaultLock=DoorLockType.Wave
                    ),
                }
            ),
            RoomName.Observatory: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Observatory_Access, defaultLock=DoorLockType.Wave
                    ),
                    1: DoorData(
                        RoomName.West_Tower_Entrance,
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and _can_climb_observatory_via_puzzle(world, state),
                        tricks=[Tricks.observatory_puzzle_skip],
                        defaultLock=DoorLockType.Wave,
                    ),
                    2: DoorData(
                        RoomName.Save_Station_D,
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and _can_climb_observatory_via_puzzle(world, state),
                        tricks=[Tricks.observatory_puzzle_skip],
                        blast_shield=BlastShieldType.Missile,
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Observatory",
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and _can_climb_observatory_via_puzzle(world, state),
                        tricks=[Tricks.observatory_puzzle_skip],
                    ),
                ],
            ),
            RoomName.Phendrana_Canyon: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Canyon_Entryway,
                        rule_func=lambda world, state: (
                            can_boost(world, state) and can_scan(world, state)
                        )
                        or can_space_jump(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Phendrana Canyon",
                        tricks=[Tricks.phendrana_canyon_escape_no_items],
                    ),
                ],
            ),
            RoomName.Phendrana_Shorelines: RoomData(
                doors={
                    0: DoorData(RoomName.Shoreline_Entrance),
                    1: DoorData(
                        RoomName.Temple_Entryway,
                        rule_func=can_space_jump,
                        tricks=[Tricks.ice_temple_no_sj],
                    ),
                    2: DoorData(RoomName.Save_Station_B),
                    3: DoorData(RoomName.Ruins_Entryway, rule_func=can_space_jump),
                    4: DoorData(RoomName.Plaza_Walkway, rule_func=can_space_jump),
                    5: DoorData(
                        RoomName.Ice_Ruins_Access,
                        rule_func=lambda world, state: can_missile(world, state)
                        and can_scan(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Phendrana Shorelines - Behind Ice",
                        rule_func=can_melt_ice,
                    ),
                    PickupData(
                        "Phendrana Drifts: Phendrana Shorelines - Spider Track",
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_spider(world, state)
                        and can_super_missile(world, state)
                        and can_scan(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.shorelines_spider_track_no_sj],
                    ),
                ],
            ),
            RoomName.Phendranas_Edge: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Lower_Edge_Tunnel, defaultLock=DoorLockType.Wave
                    ),
                    1: DoorData(
                        RoomName.Upper_Edge_Tunnel, defaultLock=DoorLockType.Wave
                    ),
                    2: DoorData(
                        RoomName.Storage_Cave,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_grapple(world, state)
                        and (can_thermal(world, state) or can_xray(world, state))
                        and can_power_bomb(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.phendranas_edge_storage_cavern_no_grapple],
                    ),
                    3: DoorData(
                        RoomName.Security_Cave,
                        defaultLock=DoorLockType.None_,
                        exclude_from_rando=True,
                        rule_func=lambda world, state: can_grapple(world, state)
                        and can_morph_ball(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.phendranas_edge_security_cavern_no_grapple],
                    ),
                }
            ),
            RoomName.Pike_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Frozen_Pike, defaultLock=DoorLockType.Wave),
                    1: DoorData(RoomName.Research_Core, defaultLock=DoorLockType.Ice),
                }
            ),
            RoomName.Plaza_Walkway: RoomData(
                doors={
                    0: DoorData(RoomName.Phendrana_Shorelines, sub_region_door_index=3),
                    1: DoorData(RoomName.Ice_Ruins_East),
                }
            ),
            RoomName.Quarantine_Access: RoomData(
                doors={
                    0: DoorData(RoomName.North_Quarantine_Tunnel),
                    1: DoorData(RoomName.Ruined_Courtyard),
                }
            ),
            RoomName.Quarantine_Cave: RoomData(
                doors={
                    0: DoorData(
                        RoomName.North_Quarantine_Tunnel,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_combat_thardus(world, state)
                        and can_spider(world, state)
                        and can_thermal(world, state),
                        tricks=[Tricks.quarantine_to_north_courtyard_slope_jump],
                    ),
                    1: DoorData(
                        RoomName.South_Quarantine_Tunnel,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_combat_thardus(world, state)
                        and can_thermal(world, state)
                        and (
                            (can_bomb(world, state) and can_spider(world, state))
                            or (
                                can_space_jump(world, state)
                                and can_grapple(world, state)
                            )
                        ),
                    ),
                    2: DoorData(
                        RoomName.Quarantine_Monitor,
                        defaultLock=DoorLockType.None_,
                        exclude_from_rando=True,
                        rule_func=lambda world, state: can_combat_thardus(world, state)
                        and can_spider(world, state)
                        and can_grapple(world, state),
                        tricks=[Tricks.monitor_cave_no_grapple],
                    ),  # Not an annotated door
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Quarantine Cave",
                        rule_func=lambda world, state: can_combat_thardus(world, state)
                        and can_thermal(world, state),
                    ),
                ],
            ),
            RoomName.Quarantine_Monitor: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Quarantine_Cave,
                        rule_func=can_morph_ball,
                        defaultLock=DoorLockType.None_,
                        exclude_from_rando=True,
                    ),  # Not an annotated door
                },
                pickups=[
                    PickupData("Phendrana Drifts: Quarantine Monitor"),
                ],
            ),
            RoomName.Research_Core_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Research_Core, defaultLock=DoorLockType.Wave),
                    1: DoorData(
                        RoomName.Research_Lab_Aether, defaultLock=DoorLockType.Wave
                    ),  # Vertical door, going up
                }
            ),
            RoomName.Research_Core: RoomData(
                doors={
                    0: DoorData(RoomName.Pike_Access, defaultLock=DoorLockType.Ice),
                    1: DoorData(
                        RoomName.Research_Core_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_thermal(world, state)
                        and can_wave_beam(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Research Core",
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_thermal(world, state)
                        and can_scan(world, state)
                        and can_wave_beam(world, state),
                    ),
                ],
            ),
            RoomName.Research_Entrance: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Specimen_Storage, defaultLock=DoorLockType.Wave
                    ),
                    1: DoorData(
                        RoomName.Map_Station,
                        destination_area=MetroidPrimeArea.Phendrana_Drifts,
                    ),
                    2: DoorData(
                        RoomName.Hydra_Lab_Entryway, defaultLock=DoorLockType.Wave
                    ),
                }
            ),
            RoomName.Research_Lab_Aether: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Aether_Lab_Entryway,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_space_jump(world, state),
                    ),
                    1: DoorData(
                        RoomName.Research_Core_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_missile(world, state)
                        or can_power_bomb(world, state),
                    ),  # Vertical door, going down
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Research Lab Aether - Tank",
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_missile(world, state),
                    ),
                    PickupData(
                        "Phendrana Drifts: Research Lab Aether - Morph Track",
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_bomb(world, state)
                        and can_space_jump(world, state),
                    ),
                ],
            ),
            RoomName.Research_Lab_Hydra: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Hydra_Lab_Entryway,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_scan(world, state),
                    ),  # scan door is two way w/ random prime
                    1: DoorData(
                        RoomName.Observatory_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_combat_labs(world, state)
                        and can_scan(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Research Lab Hydra",
                        rule_func=lambda world, state: can_super_missile(world, state)
                        and can_scan(world, state),
                    ),
                ],
            ),
            RoomName.Ruined_Courtyard: RoomData(
                doors={
                    0: DoorData(RoomName.Courtyard_Entryway),
                    1: DoorData(
                        RoomName.Save_Station_A,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=lambda world, state: _can_reach_top_of_ruined_courtyard(
                            world, state
                        ),
                        tricks=[Tricks.phendrana_courtyard_no_boost_spider],
                    ),
                    2: DoorData(
                        RoomName.Specimen_Storage,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: _can_reach_top_of_ruined_courtyard(
                            world, state
                        ),
                        tricks=[Tricks.phendrana_courtyard_no_boost_spider],
                    ),
                    3: DoorData(
                        RoomName.Quarantine_Access,
                        rule_func=lambda world, state: _can_reach_top_of_ruined_courtyard(
                            world, state
                        )
                        and can_wave_beam(world, state)
                        and can_thermal(world, state)
                        and can_super_missile(world, state),
                        tricks=[Tricks.phendrana_courtyard_no_boost_spider],
                    ),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Ruined Courtyard",
                        rule_func=lambda world, state: _can_reach_top_of_ruined_courtyard(
                            world, state
                        ),
                        tricks=[Tricks.phendrana_courtyard_item_no_boost_spider],
                    ),
                ],
            ),
            RoomName.Ruins_Entryway: RoomData(
                doors={
                    0: DoorData(RoomName.Ice_Ruins_West),
                    1: DoorData(RoomName.Phendrana_Shorelines, sub_region_door_index=4),
                }
            ),
            RoomName.Save_Station_A: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Ruined_Courtyard, blast_shield=BlastShieldType.Missile
                    ),
                }
            ),
            RoomName.Save_Station_B: RoomData(
                doors={
                    0: DoorData(RoomName.Phendrana_Shorelines),
                }
            ),
            RoomName.Save_Station_C: RoomData(
                doors={
                    0: DoorData(RoomName.Frost_Cave, defaultLock=DoorLockType.Wave),
                }
            ),
            RoomName.Save_Station_D: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Observatory, blast_shield=BlastShieldType.Missile
                    ),
                }
            ),
            RoomName.Security_Cave: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Phendranas_Edge,
                        rule_func=can_morph_ball,
                        defaultLock=DoorLockType.None_,
                        exclude_from_rando=True,
                    ),
                },
                pickups=[
                    PickupData("Phendrana Drifts: Security Cave"),
                ],
            ),
            RoomName.Shoreline_Entrance: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Transport_to_Magmoor_Caverns_West,
                        rule_func=lambda world, state: can_charge_beam(world, state)
                        or can_missile(world, state),
                    ),
                    1: DoorData(
                        RoomName.Phendrana_Shorelines,
                        rule_func=lambda world, state: can_charge_beam(world, state)
                        or can_missile(world, state),
                    ),
                }
            ),
            RoomName.South_Quarantine_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Quarantine_Cave, defaultLock=DoorLockType.Wave
                    ),
                    1: DoorData(
                        RoomName.Transport_to_Magmoor_Caverns_South,
                        defaultLock=DoorLockType.Wave,
                        destination_area=MetroidPrimeArea.Phendrana_Drifts,
                    ),
                }
            ),
            RoomName.Specimen_Storage: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Research_Entrance, defaultLock=DoorLockType.Wave
                    ),
                    1: DoorData(
                        RoomName.Ruined_Courtyard, defaultLock=DoorLockType.Wave
                    ),
                }
            ),
            RoomName.Storage_Cave: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Phendranas_Edge, defaultLock=DoorLockType.Plasma
                    ),
                },
                pickups=[
                    PickupData("Phendrana Drifts: Storage Cave"),
                ],
            ),
            RoomName.Temple_Entryway: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Chozo_Ice_Temple,
                        rule_func=lambda world, state: can_missile(world, state)
                        or can_charge_beam(world, state)
                        or can_plasma_beam(world, state),
                    ),
                    1: DoorData(
                        RoomName.Phendrana_Shorelines,
                        rule_func=lambda world, state: can_missile(world, state)
                        or can_charge_beam(world, state)
                        or can_plasma_beam(world, state),
                    ),
                }
            ),
            RoomName.Transport_Access: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Transport_to_Magmoor_Caverns_South,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phendrana_Drifts,
                    ),
                    1: DoorData(RoomName.Frozen_Pike, defaultLock=DoorLockType.Wave),
                },
                pickups=[
                    PickupData(
                        "Phendrana Drifts: Transport Access", rule_func=can_melt_ice
                    ),
                ],
            ),
            RoomName.Transport_to_Magmoor_Caverns_South: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Transport_Access,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phendrana_Drifts,
                        rule_func=can_spider,
                    ),
                    1: DoorData(
                        RoomName.South_Quarantine_Tunnel, defaultLock=DoorLockType.Wave
                    ),
                },
            ),
            RoomName.Transport_to_Magmoor_Caverns_West: RoomData(
                doors={
                    0: DoorData(RoomName.Shoreline_Entrance),
                }
            ),
            RoomName.Upper_Edge_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Phendranas_Edge,
                        rule_func=can_morph_ball,
                        defaultLock=DoorLockType.Wave,
                    ),
                    1: DoorData(
                        RoomName.Frost_Cave,
                        rule_func=can_morph_ball,
                        defaultLock=DoorLockType.Wave,
                    ),
                }
            ),
            RoomName.West_Tower_Entrance: RoomData(
                doors={
                    0: DoorData(
                        RoomName.West_Tower, blast_shield=BlastShieldType.Missile
                    ),
                    1: DoorData(RoomName.Observatory, defaultLock=DoorLockType.Wave),
                }
            ),
            RoomName.West_Tower: RoomData(
                doors={
                    0: DoorData(
                        RoomName.West_Tower_Entrance,
                        blast_shield=BlastShieldType.Missile,
                    ),
                    1: DoorData(
                        RoomName.Control_Tower,
                        rule_func=can_scan,
                        defaultLock=DoorLockType.Wave,
                    ),
                }
            ),
        }
        self._init_room_names_and_areas()

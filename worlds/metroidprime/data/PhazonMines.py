from ..Items import SuitUpgrade
from ..DoorRando import DoorLockType
from ..LogicCombat import (
    can_combat_beam_pirates,
    can_combat_mines,
    can_combat_omega_pirate,
)
from .Tricks import Tricks
from .RoomNames import RoomName
from .AreaNames import MetroidPrimeArea
from .RoomData import AreaData, PickupData, RoomData
from .DoorData import DoorData
from ..Logic import (
    can_backwards_lower_mines,
    can_bomb,
    can_boost,
    can_grapple,
    can_melt_ice,
    can_morph_ball,
    can_phazon,
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


class PhazonMinesAreaData(AreaData):
    def __init__(self):
        super().__init__(MetroidPrimeArea.Phazon_Mines.value)
        self.rooms = {
            RoomName.Central_Dynamo: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Dynamo_Access,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_space_jump(world, state)
                        and can_power_bomb(world, state),
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                    ),
                    1: DoorData(
                        RoomName.Quarantine_Access_A,
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_power_bomb(world, state),
                        defaultLock=DoorLockType.Ice,
                    ),
                    2: DoorData(
                        RoomName.Save_Station_Mines_B,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_bomb,
                    ),  # Door only unlocks after defeating drone and then completing the maze
                },
                pickups=[
                    PickupData("Phazon Mines: Central Dynamo", rule_func=can_bomb),
                ],
            ),
            RoomName.Dynamo_Access: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Central_Dynamo,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                    ),
                    1: DoorData(
                        RoomName.Omega_Research, defaultLock=DoorLockType.Ice
                    ),  # Vertical going up
                },
            ),
            RoomName.Elevator_A: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Elevator_Access_A, defaultLock=DoorLockType.Ice
                    ),
                    1: DoorData(
                        RoomName.Elite_Control_Access,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_scan,
                    ),  # Not annotated
                }
            ),
            RoomName.Elevator_Access_A: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Ore_Processing,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_spider,
                        tricks=[Tricks.mines_climb_shafts_no_spider],
                    ),
                    1: DoorData(
                        RoomName.Elevator_A,
                        defaultLock=DoorLockType.Ice,
                    ),
                }
            ),
            RoomName.Elevator_Access_B: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Metroid_Quarantine_A, defaultLock=DoorLockType.Ice
                    ),
                    1: DoorData(RoomName.Elevator_B, defaultLock=DoorLockType.Plasma),
                }
            ),
            RoomName.Elevator_B: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Elevator_Access_B, defaultLock=DoorLockType.Plasma
                    ),
                    1: DoorData(
                        RoomName.Fungal_Hall_Access, defaultLock=DoorLockType.Plasma
                    ),
                }
            ),
            RoomName.Elite_Control_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Elevator_A, defaultLock=DoorLockType.Ice),
                    1: DoorData(RoomName.Elite_Control, defaultLock=DoorLockType.Wave),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Elite Control Access", rule_func=can_morph_ball
                    ),
                ],
            ),
            RoomName.Elite_Control: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Maintenance_Tunnel,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_scan,
                    ),
                    1: DoorData(
                        RoomName.Elite_Control_Access,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_scan,
                    ),
                    2: DoorData(
                        RoomName.Ventilation_Shaft,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_scan,
                    ),  # Vertical door going up
                }
            ),
            RoomName.Elite_Quarters_Access: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Metroid_Quarantine_B,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=can_backwards_lower_mines,
                    ),
                    1: DoorData(
                        RoomName.Elite_Quarters,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=can_melt_ice,
                    ),
                }
            ),
            RoomName.Elite_Quarters: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Elite_Quarters_Access,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_combat_omega_pirate(
                            world, state
                        ),
                    ),
                    1: DoorData(
                        RoomName.Processing_Center_Access,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_combat_omega_pirate(
                            world, state
                        )
                        and can_scan(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Elite Quarters",
                        rule_func=lambda world, state: can_combat_omega_pirate(
                            world, state
                        ),
                    ),
                ],
            ),
            RoomName.Elite_Research: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Research_Access,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_boost(world, state)
                        and can_space_jump(world, state)
                        and can_scan(world, state)
                        and can_combat_beam_pirates(
                            world, state, SuitUpgrade.Power_Beam
                        ),
                        tricks=[Tricks.elite_research_spinner_no_boost],
                    ),
                    1: DoorData(
                        RoomName.Security_Access_B, defaultLock=DoorLockType.Ice
                    ),  # Vertical door, going down
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Elite Research - Phazon Elite",
                        rule_func=lambda world, state: can_power_bomb(world, state)
                        and can_combat_beam_pirates(
                            world, state, SuitUpgrade.Power_Beam
                        ),
                    ),
                    PickupData(
                        "Phazon Mines: Elite Research - Laser",
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_boost(world, state)
                        and can_space_jump(world, state)
                        and can_scan(world, state)
                        and can_combat_beam_pirates(
                            world, state, SuitUpgrade.Power_Beam
                        ),
                        tricks=[Tricks.elite_research_spinner_no_boost],
                    ),
                ],
            ),
            RoomName.Fungal_Hall_A: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Phazon_Mining_Tunnel,
                        rule_func=lambda world, state: can_grapple(world, state)
                        and can_space_jump(world, state),
                        defaultLock=DoorLockType.Ice,
                        tricks=[Tricks.fungal_hall_a_no_grapple],
                    ),
                    1: DoorData(
                        RoomName.Fungal_Hall_Access,
                        rule_func=can_space_jump,
                        defaultLock=DoorLockType.Ice,
                    ),
                }
            ),
            RoomName.Fungal_Hall_Access: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Fungal_Hall_A,
                        rule_func=lambda world, state: can_space_jump(world, state),
                    ),
                    1: DoorData(
                        RoomName.Elevator_B,
                        rule_func=lambda world, state: can_space_jump(world, state),
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Fungal Hall Access",
                        rule_func=lambda world, state: can_morph_ball(world, state)
                        and can_phazon(world, state),
                        tricks=[Tricks.fungal_hall_access_no_phazon_suit],
                    ),
                ],
            ),
            RoomName.Fungal_Hall_B: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Missile_Station_Mines,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_grapple(world, state),
                        tricks=[Tricks.fungal_hall_b_no_grapple],
                    ),
                    1: DoorData(
                        RoomName.Quarantine_Access_B,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_grapple(world, state),
                        tricks=[Tricks.fungal_hall_b_no_grapple],
                    ),
                    2: DoorData(
                        RoomName.Phazon_Mining_Tunnel,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=can_space_jump,
                        tricks=[Tricks.fungal_hall_b_no_grapple],
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Fungal Hall B",
                        rule_func=lambda world, state: can_bomb(world, state)
                        or can_power_bomb(world, state),
                    ),
                ],
            ),
            RoomName.Main_Quarry: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Waste_Disposal,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_grapple(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.main_quarry_to_waste_disposal_no_grapple],
                    ),
                    1: DoorData(
                        RoomName.Quarry_Access,
                        defaultLock=DoorLockType.Wave,
                    ),
                    2: DoorData(
                        RoomName.Save_Station_Mines_A,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_spider,
                    ),
                    3: DoorData(
                        RoomName.Security_Access_A,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_scan,
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Main Quarry",
                        rule_func=lambda world, state: can_morph_ball(world, state)
                        and can_spider(world, state)
                        and can_bomb(world, state)
                        and can_thermal(world, state)
                        and can_wave_beam(world, state)
                        and can_scan(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.main_quarry_item_no_spider],
                    ),
                ],
            ),
            RoomName.Maintenance_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Elite_Control,
                        rule_func=can_power_bomb,
                        defaultLock=DoorLockType.Ice,
                    ),
                    1: DoorData(
                        RoomName.Phazon_Processing_Center,
                        rule_func=can_power_bomb,
                        defaultLock=DoorLockType.Ice,
                    ),
                }
            ),
            RoomName.Map_Station_Mines: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Omega_Research,
                        rule_func=can_power_bomb,
                        defaultLock=DoorLockType.Ice,
                    ),
                }
            ),
            RoomName.Metroid_Quarantine_A: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Quarantine_Access_A,
                        defaultLock=DoorLockType.Wave,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_backwards_lower_mines(world, state)
                        and can_space_jump(world, state),
                    ),
                    1: DoorData(
                        RoomName.Elevator_Access_B,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_scan(world, state)
                        and can_spider(world, state)
                        and can_bomb(world, state)
                        and can_space_jump(world, state)
                        and can_xray(world, state),
                        tricks=[Tricks.metroid_quarantine_a_no_spider],
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Metroid Quarantine A",
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and (
                            can_scan(world, state)
                            or can_backwards_lower_mines(world, state)
                        )
                        and can_power_bomb(world, state)
                        and can_space_jump(world, state)
                        and can_xray(world, state),
                        tricks=[],
                    ),
                ],
            ),
            RoomName.Metroid_Quarantine_B: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Quarantine_Access_B,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_combat_beam_pirates(
                            world, state, SuitUpgrade.Plasma_Beam
                        )
                        and can_space_jump(world, state),
                    ),
                    1: DoorData(
                        RoomName.Elite_Quarters_Access,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_combat_beam_pirates(
                            world, state, SuitUpgrade.Plasma_Beam
                        )
                        and can_spider(world, state)
                        and can_grapple(world, state)
                        and can_space_jump(world, state)
                        and can_scan(world, state),
                        tricks=[Tricks.metroid_quarantine_b_no_spider_grapple],
                    ),
                    2: DoorData(
                        RoomName.Save_Station_Mines_C,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_combat_beam_pirates(
                            world, state, SuitUpgrade.Plasma_Beam
                        )
                        and can_spider(world, state)
                        and can_grapple(world, state)
                        and can_space_jump(world, state)
                        and can_scan(world, state),
                        tricks=[Tricks.metroid_quarantine_b_no_spider_grapple],
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Metroid Quarantine B",
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_combat_beam_pirates(
                            world, state, SuitUpgrade.Plasma_Beam
                        )
                        and state.can_reach(
                            RoomName.Elite_Quarters_Access.value, None, world.player
                        )
                        and can_super_missile(world, state),
                        tricks=[],
                    ),
                ],
            ),
            RoomName.Mine_Security_Station: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Security_Access_A,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_wave_beam,
                    ),
                    1: DoorData(
                        RoomName.Security_Access_B,
                        defaultLock=DoorLockType.Wave,
                        rule_func=can_wave_beam,
                    ),
                    2: DoorData(
                        RoomName.Storage_Depot_A,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_power_bomb(world, state)
                        and can_plasma_beam(world, state)
                        and can_scan(world, state),
                    ),
                }
            ),
            RoomName.Missile_Station_Mines: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Fungal_Hall_B, defaultLock=DoorLockType.Plasma
                    ),
                }
            ),
            RoomName.Omega_Research: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Map_Station_Mines,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_power_bomb(world, state),
                    ),
                    1: DoorData(
                        RoomName.Ventilation_Shaft,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_power_bomb(world, state),
                    ),
                    2: DoorData(
                        RoomName.Dynamo_Access,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                        rule_func=lambda world, state: can_combat_mines(world, state)
                        and can_power_bomb(world, state),
                    ),  # Vertical door going down
                }
            ),
            RoomName.Ore_Processing: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Research_Access,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: True,
                    ),
                    1: DoorData(
                        RoomName.Storage_Depot_B,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: (
                            can_combat_beam_pirates(
                                world, state, SuitUpgrade.Power_Beam
                            )
                            and can_spider(world, state)
                            and can_bomb(world, state)
                            and can_power_bomb(world, state)
                        )
                        or (
                            state.can_reach(
                                RoomName.Waste_Disposal.value, None, world.player
                            )
                            and can_grapple(world, state)
                        ),
                        tricks=[Tricks.ore_processing_to_storage_depot_b_no_spider],
                        indirect_condition_rooms=[RoomName.Waste_Disposal],
                    ),
                    2: DoorData(
                        RoomName.Waste_Disposal,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_combat_beam_pirates(
                            world, state, SuitUpgrade.Power_Beam
                        )
                        and can_spider(world, state)
                        and can_grapple(world, state)
                        and can_bomb(world, state)
                        and can_power_bomb(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.ore_processing_climb_no_grapple_spider],
                    ),
                    3: DoorData(
                        RoomName.Elevator_Access_A,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_combat_beam_pirates(
                            world, state, SuitUpgrade.Power_Beam
                        )
                        and can_spider(world, state)
                        and can_grapple(world, state)
                        and can_bomb(world, state)
                        and can_power_bomb(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.ore_processing_climb_no_grapple_spider],
                    ),
                }
            ),
            RoomName.Phazon_Mining_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Fungal_Hall_B,
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_power_bomb(world, state),
                        defaultLock=DoorLockType.Plasma,
                    ),
                    1: DoorData(
                        RoomName.Fungal_Hall_A,
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_power_bomb(world, state),
                        defaultLock=DoorLockType.Plasma,
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Phazon Mining Tunnel",
                        rule_func=lambda world, state: can_phazon(world, state)
                        and can_bomb(world, state),
                        tricks=[],
                    ),
                ],
            ),
            RoomName.Phazon_Processing_Center: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Transport_Access,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_spider(world, state)
                        and can_bomb(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.climb_phazon_processing_center_no_spider],
                    ),
                    1: DoorData(
                        RoomName.Maintenance_Tunnel,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_spider(world, state)
                        and can_bomb(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.climb_phazon_processing_center_no_spider],
                    ),
                    2: DoorData(
                        RoomName.Processing_Center_Access,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=can_phazon,
                        tricks=[Tricks.phazon_processing_center_no_phazon_suit],
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Phazon Processing Center",
                        rule_func=lambda world, state: can_spider(world, state)
                        and can_bomb(world, state)
                        and can_space_jump(world, state)
                        and can_power_bomb(world, state),
                        tricks=[Tricks.phazon_processing_center_item_no_spider],
                    ),
                ],
            ),
            RoomName.Processing_Center_Access: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Phazon_Processing_Center,
                        rule_func=lambda world, state: can_scan(world, state)
                        or can_backwards_lower_mines(world, state),
                        defaultLock=DoorLockType.Plasma,
                    ),
                    1: DoorData(
                        RoomName.Elite_Quarters,
                        rule_func=lambda world, state: can_backwards_lower_mines(
                            world, state
                        ),
                        defaultLock=DoorLockType.Plasma,
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Processing Center Access",
                        rule_func=lambda world, state: can_backwards_lower_mines(
                            world, state
                        )
                        or state.can_reach(
                            RoomName.Elite_Quarters.value, None, world.player
                        ),
                        tricks=[],
                    ),
                ],
            ),
            RoomName.Quarantine_Access_A: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Central_Dynamo,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                    ),
                    1: DoorData(
                        RoomName.Metroid_Quarantine_A, defaultLock=DoorLockType.Wave
                    ),
                }
            ),
            RoomName.Quarantine_Access_B: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Metroid_Quarantine_B, defaultLock=DoorLockType.Plasma
                    ),
                    1: DoorData(
                        RoomName.Fungal_Hall_B, defaultLock=DoorLockType.Plasma
                    ),
                }
            ),
            RoomName.Quarry_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Wave),
                    1: DoorData(
                        RoomName.Transport_to_Tallon_Overworld_South,
                        defaultLock=DoorLockType.Wave,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                    ),
                }
            ),
            RoomName.Research_Access: RoomData(
                doors={
                    0: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice),
                    1: DoorData(
                        RoomName.Elite_Research,
                        defaultLock=DoorLockType.Ice,
                        # Can't go backwards through the wall without tricks, checks if player can reach the room from the other side
                        rule_func=lambda world, state: False,
                        tricks=[
                            Tricks.elite_research_backwards_wall_boost_no_spider,
                            Tricks.elite_research_backwards_wall_boost,
                        ],
                    ),
                }
            ),
            RoomName.Save_Station_Mines_A: RoomData(
                doors={
                    0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Wave),
                }
            ),
            RoomName.Save_Station_Mines_B: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Central_Dynamo,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                    ),
                }
            ),
            RoomName.Save_Station_Mines_C: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Metroid_Quarantine_B, defaultLock=DoorLockType.Plasma
                    ),
                }
            ),
            RoomName.Security_Access_A: RoomData(
                doors={
                    0: DoorData(RoomName.Main_Quarry, defaultLock=DoorLockType.Ice),
                    1: DoorData(
                        RoomName.Mine_Security_Station, defaultLock=DoorLockType.Ice
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Security Access A",
                        rule_func=can_power_bomb,
                        tricks=[],
                    ),
                ],
            ),
            RoomName.Security_Access_B: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Mine_Security_Station, defaultLock=DoorLockType.Wave
                    ),  # Vertical door going down
                    1: DoorData(
                        RoomName.Elite_Research, defaultLock=DoorLockType.Ice
                    ),  # Vertical door going up
                }
            ),
            RoomName.Storage_Depot_A: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Mine_Security_Station, defaultLock=DoorLockType.Plasma
                    ),
                },
                pickups=[
                    PickupData("Phazon Mines: Storage Depot A"),
                ],
            ),
            RoomName.Storage_Depot_B: RoomData(
                doors={
                    0: DoorData(RoomName.Ore_Processing, defaultLock=DoorLockType.Ice),
                },
                pickups=[
                    PickupData("Phazon Mines: Storage Depot B"),
                ],
            ),
            RoomName.Transport_Access: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Phazon_Processing_Center, defaultLock=DoorLockType.Ice
                    ),
                    1: DoorData(
                        RoomName.Transport_to_Magmoor_Caverns_South,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                    ),
                },
            ),
            RoomName.Transport_to_Magmoor_Caverns_South: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Transport_Access,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Phazon_Mines,
                    ),
                },
            ),
            RoomName.Transport_to_Tallon_Overworld_South: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Quarry_Access,
                        defaultLock=DoorLockType.Wave,
                    ),
                },
            ),
            RoomName.Ventilation_Shaft: RoomData(
                doors={
                    0: DoorData(RoomName.Omega_Research, defaultLock=DoorLockType.Ice),
                    1: DoorData(
                        RoomName.Elite_Control,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_boost,
                        tricks=[Tricks.ventilation_shaft_hpbj],
                    ),
                },
                pickups=[
                    PickupData(
                        "Phazon Mines: Ventilation Shaft",
                        rule_func=lambda world, state: can_scan(world, state)
                        and can_power_bomb(world, state)
                        and can_space_jump(world, state),
                    ),
                ],
            ),
            RoomName.Waste_Disposal: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Main_Quarry,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_bomb,
                    ),
                    1: DoorData(
                        RoomName.Ore_Processing,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_bomb,
                    ),
                }
            ),
        }
        self._init_room_names_and_areas()

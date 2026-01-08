from BaseClasses import CollectionState
from ..BlastShieldRando import BlastShieldType
from ..DoorRando import DoorLockType
from ..Logic import (
    can_bomb,
    can_boost,
    can_charge_beam,
    can_grapple,
    can_missile,
    can_morph_ball,
    can_move_underwater,
    can_power_beam,
    can_power_bomb,
    can_space_jump,
    can_spider,
    can_super_missile,
    can_xray,
    can_wave_beam,
    can_thermal,
)
from ..LogicCombat import can_combat_ghosts
from .Tricks import Tricks
from .AreaNames import MetroidPrimeArea
from .RoomData import AreaData, PickupData, RoomData
from .DoorData import DoorData
from .RoomNames import RoomName
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


def can_crashed_frigate_front(
    world: "MetroidPrimeWorld", state: CollectionState
) -> bool:
    return (
        can_morph_ball(world, state)
        and can_wave_beam(world, state)
        and can_thermal(world, state)
        and (can_move_underwater(world, state) or can_space_jump(world, state))
    )


def can_crashed_frigate(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
    return (
        can_crashed_frigate_front(world, state)
        and can_bomb(world, state)
        and can_space_jump(world, state)
        and can_move_underwater(world, state)
    )


def can_crashed_frigate_backwards(
    world: "MetroidPrimeWorld", state: CollectionState
) -> bool:
    return (
        can_space_jump(world, state)
        and can_move_underwater(world, state)
        and can_bomb(world, state)
    )


class TallonOverworldAreaData(AreaData):
    def __init__(self):
        super().__init__(MetroidPrimeArea.Tallon_Overworld.value)
        self.rooms = {
            RoomName.Alcove: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Landing_Site,
                        rule_func=can_space_jump,
                        tricks=[Tricks.alcove_escape],
                    ),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Alcove",
                        rule_func=can_space_jump,
                        tricks=[Tricks.alcove_escape],
                    ),
                ],
            ),
            RoomName.Arbor_Chamber: RoomData(
                doors={
                    0: DoorData(RoomName.Root_Cave),
                },
                pickups=[
                    PickupData("Tallon Overworld: Arbor Chamber"),
                ],
            ),
            RoomName.Artifact_Temple: RoomData(
                doors={
                    0: DoorData(RoomName.Temple_Lobby),
                },
                pickups=[
                    PickupData("Tallon Overworld: Artifact Temple"),
                ],
            ),
            RoomName.Biohazard_Containment: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Cargo_Freight_Lift_to_Deck_Gamma,
                        rule_func=can_crashed_frigate_backwards,
                        tricks=[Tricks.frigate_backwards_no_gravity],
                    ),
                    1: DoorData(
                        RoomName.Hydro_Access_Tunnel,
                        rule_func=can_crashed_frigate,
                        tricks=[Tricks.frigate_no_gravity],
                    ),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Biohazard Containment",
                        rule_func=can_super_missile,
                    ),
                ],
            ),
            # RoomName.Biotech_Research_Area_1: RoomData(
            # ),
            RoomName.Canyon_Cavern: RoomData(
                doors={
                    1: DoorData(RoomName.Landing_Site),
                    0: DoorData(RoomName.Tallon_Canyon),
                },
            ),
            RoomName.Cargo_Freight_Lift_to_Deck_Gamma: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Frigate_Access_Tunnel,
                        exclude_from_rando=True,
                        rule_func=can_crashed_frigate_backwards,
                        tricks=[Tricks.frigate_backwards_no_gravity],
                    ),
                    1: DoorData(
                        RoomName.Biohazard_Containment,
                        rule_func=can_crashed_frigate,
                        tricks=[Tricks.frigate_no_gravity],
                    ),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Cargo Freight Lift to Deck Gamma",
                        rule_func=lambda world, state: (
                            can_missile(world, state) or can_charge_beam(world, state)
                        )
                        and (
                            can_crashed_frigate_front(world, state)
                            or can_crashed_frigate_backwards(world, state)
                        ),
                    ),
                ],
            ),
            # RoomName.Connection_Elevator_to_Deck_Beta: RoomData(
            # ),
            # RoomName.Deck_Beta_Conduit_Hall: RoomData(
            # ),
            # RoomName.Deck_Beta_Security_Hall: RoomData(
            # ),
            # RoomName.Deck_Beta_Transit_Hall: RoomData(
            # ),
            RoomName.Frigate_Access_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Cargo_Freight_Lift_to_Deck_Gamma,
                        rule_func=can_crashed_frigate_front,
                        tricks=[Tricks.frigate_no_gravity],
                        exclude_from_rando=True,
                    ),
                    1: DoorData(
                        RoomName.Frigate_Crash_Site, defaultLock=DoorLockType.Ice
                    ),
                }
            ),
            RoomName.Frigate_Crash_Site: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Waterfall_Cavern,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=can_missile,
                    ),
                    1: DoorData(
                        RoomName.Frigate_Access_Tunnel, defaultLock=DoorLockType.Ice
                    ),
                    2: DoorData(
                        RoomName.Overgrown_Cavern,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: False,  # Can't reach unless a trick is used
                        tricks=[Tricks.frigate_crash_site_climb_to_overgrown_cavern],
                    ),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Frigate Crash Site",
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_move_underwater(world, state),
                        tricks=[
                            Tricks.frigate_crash_site_scan_dash,
                            Tricks.frigate_crash_site_slope_jump,
                        ],
                    ),
                ],
            ),
            RoomName.Great_Tree_Chamber: RoomData(
                doors={
                    0: DoorData(RoomName.Great_Tree_Hall),
                },
                pickups=[
                    PickupData("Tallon Overworld: Great Tree Chamber"),
                ],
            ),
            RoomName.Great_Tree_Hall: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Hydro_Access_Tunnel,
                        rule_func=lambda world, state: False,
                        tricks=[Tricks.great_tree_hall_skip_bars],
                        exclude_from_rando=True,
                    ),  # Can't reach from other doors unless you use a trick until after you go through frigate
                    1: DoorData(
                        RoomName.Great_Tree_Chamber,
                        rule_func=lambda world, state: can_xray(world, state)
                        and can_space_jump(world, state),
                        tricks=[
                            Tricks.great_tree_chamber_no_xray,
                            Tricks.great_tree_chamber_nsj_no_xray,
                        ],
                    ),
                    2: DoorData(
                        RoomName.Transport_Tunnel_D,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                    ),  # Can't reach from other doors unless you use a trick until after you go through frigate
                    3: DoorData(
                        RoomName.Life_Grove_Tunnel,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_spider,
                        tricks=[Tricks.great_tree_hall_no_spider_ball],
                    ),
                    4: DoorData(
                        RoomName.Transport_Tunnel_E,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                        rule_func=lambda world, state: False,
                        tricks=[Tricks.great_tree_hall_skip_bars],
                    ),  # Can't reach from other doors unless you use a trick until after you go through frigate
                },
            ),
            RoomName.Gully: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Tallon_Canyon,
                        defaultLock=DoorLockType.Blue,
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_space_jump(world, state),
                    ),
                    1: DoorData(RoomName.Landing_Site, sub_region_door_index=3),
                },
            ),
            RoomName.Hydro_Access_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Great_Tree_Hall,
                        rule_func=lambda world, state: can_crashed_frigate(world, state)
                        and can_boost(world, state),
                        tricks=[Tricks.hydro_access_tunnel_no_gravity],
                        sub_region_door_index=4,
                        sub_region_access_override=can_crashed_frigate,
                    ),  # Boost is needed to open way in great tree hall
                    1: DoorData(
                        RoomName.Biohazard_Containment,
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_move_underwater(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.hydro_access_tunnel_no_gravity],
                    ),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Hydro Access Tunnel",
                        rule_func=lambda world, state: can_bomb(world, state)
                        and can_move_underwater(world, state),
                        tricks=[Tricks.hydro_access_tunnel_no_gravity],
                    ),
                ],
            ),
            RoomName.Landing_Site: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Gully,
                        rule_func=lambda world, state: can_space_jump(world, state),
                        tricks=[Tricks.landing_site_scan_dash],
                    ),
                    1: DoorData(RoomName.Canyon_Cavern),
                    2: DoorData(RoomName.Temple_Hall),
                    3: DoorData(
                        RoomName.Alcove,
                        rule_func=can_space_jump,
                        tricks=[Tricks.landing_site_scan_dash],
                    ),
                    4: DoorData(RoomName.Waterfall_Cavern),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Landing Site", rule_func=can_morph_ball
                    ),
                ],
            ),
            RoomName.Life_Grove_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Great_Tree_Hall,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_power_bomb(world, state)
                        and can_boost(world, state)
                        and can_bomb(world, state),
                    ),
                    1: DoorData(
                        RoomName.Life_Grove,
                        defaultLock=DoorLockType.None_,
                        rule_func=lambda world, state: can_power_beam(world, state)
                        and can_combat_ghosts(world, state)
                        and can_power_bomb(world, state)
                        and can_boost(world, state)
                        and can_bomb(world, state),
                        exclude_from_rando=True,
                    ),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Life Grove Tunnel",
                        rule_func=lambda world, state: can_power_bomb(world, state)
                        and can_bomb(world, state)
                        and can_boost(world, state),
                    ),
                ],
            ),
            RoomName.Life_Grove: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Life_Grove_Tunnel,
                        defaultLock=DoorLockType.None_,
                        rule_func=lambda world, state: can_power_bomb(world, state)
                        and can_space_jump(world, state)
                        and can_morph_ball(world, state)
                        and can_power_beam(world, state),
                        tricks=[],
                        exclude_from_rando=True,
                    )
                },
                pickups=[
                    PickupData("Tallon Overworld: Life Grove - Start"),
                    PickupData(
                        "Tallon Overworld: Life Grove - Underwater Spinner",
                        rule_func=lambda world, state: can_boost(world, state)
                        and can_bomb(world, state),
                    ),
                ],
            ),
            # These have door types not in room data and no pickups
            # RoomName.Main_Ventilation_Shaft_Section_A: RoomData(
            # ),
            # RoomName.Main_Ventilation_Shaft_Section_B: RoomData(
            # ),
            # RoomName.Main_Ventilation_Shaft_Section_C: RoomData(
            # ),
            # RoomName.Reactor_Core: RoomData(
            # ),
            RoomName.Overgrown_Cavern: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Frigate_Crash_Site,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_morph_ball,
                    ),
                    1: DoorData(
                        RoomName.Transport_Tunnel_C,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                        defaultLock=DoorLockType.Ice,
                        rule_func=can_morph_ball,
                    ),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Overgrown Cavern", rule_func=can_morph_ball
                    ),
                ],
            ),
            # RoomName.Reactor_Access: RoomData(
            # ),
            RoomName.Root_Cave: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Transport_Tunnel_B,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                    ),
                    1: DoorData(
                        RoomName.Root_Tunnel, blast_shield=BlastShieldType.Missile
                    ),
                    2: DoorData(
                        RoomName.Arbor_Chamber,
                        defaultLock=DoorLockType.Plasma,
                        rule_func=lambda world, state: can_grapple(world, state)
                        and can_xray(world, state)
                        and can_space_jump(world, state),
                        tricks=[Tricks.root_cave_arbor_chamber_no_grapple_xray],
                    ),
                },
                pickups=[
                    PickupData(
                        "Tallon Overworld: Root Cave",
                        rule_func=lambda world, state: can_space_jump(world, state)
                        and can_grapple(world, state)
                        and can_xray(world, state),
                        tricks=[Tricks.root_cave_arbor_chamber_no_grapple_xray],
                    ),
                ],
            ),
            RoomName.Root_Tunnel: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Root_Cave, blast_shield=BlastShieldType.Missile
                    ),
                    1: DoorData(RoomName.Tallon_Canyon),
                },
            ),
            # RoomName.Savestation: RoomData(
            # ),
            RoomName.Tallon_Canyon: RoomData(
                doors={
                    0: DoorData(RoomName.Canyon_Cavern),
                    1: DoorData(
                        RoomName.Transport_Tunnel_A,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                    ),
                    2: DoorData(
                        RoomName.Gully,
                        defaultLock=DoorLockType.Blue,
                        rule_func=lambda world, state: can_boost(world, state)
                        and can_bomb(world, state),
                    ),
                    3: DoorData(RoomName.Root_Tunnel),
                }
            ),
            RoomName.Temple_Hall: RoomData(
                doors={
                    1: DoorData(RoomName.Landing_Site),
                    2: DoorData(RoomName.Temple_Security_Station),
                },
            ),
            RoomName.Temple_Lobby: RoomData(
                doors={
                    0: DoorData(RoomName.Artifact_Temple),
                    1: DoorData(
                        RoomName.Temple_Security_Station,
                        blast_shield=BlastShieldType.Missile,
                    ),
                },
            ),
            RoomName.Temple_Security_Station: RoomData(
                doors={
                    0: DoorData(RoomName.Temple_Hall),
                    1: DoorData(
                        RoomName.Temple_Lobby, blast_shield=BlastShieldType.Missile
                    ),
                },
            ),
            RoomName.Transport_to_Chozo_Ruins_East: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Transport_Tunnel_C,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                        defaultLock=DoorLockType.Ice,
                    ),
                },
            ),
            RoomName.Transport_to_Chozo_Ruins_South: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Transport_Tunnel_D,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                    ),
                },
            ),
            RoomName.Transport_to_Chozo_Ruins_West: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Transport_Tunnel_A,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                    ),
                },
            ),
            RoomName.Transport_to_Magmoor_Caverns_East: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Transport_Tunnel_B,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                    )
                },
            ),
            RoomName.Transport_to_Phazon_Mines_East: RoomData(
                doors={
                    0: DoorData(
                        RoomName.Transport_Tunnel_E,
                        defaultLock=DoorLockType.Ice,
                        destination_area=MetroidPrimeArea.Tallon_Overworld,
                    ),
                },
            ),
            RoomName.Transport_Tunnel_A: RoomData(
                doors={
                    0: DoorData(RoomName.Transport_to_Chozo_Ruins_West),
                    1: DoorData(RoomName.Tallon_Canyon),
                },
                include_area_in_name=True,
            ),
            RoomName.Transport_Tunnel_B: RoomData(
                doors={
                    0: DoorData(RoomName.Transport_to_Magmoor_Caverns_East),
                    1: DoorData(RoomName.Root_Cave),
                },
                include_area_in_name=True,
                pickups=[
                    PickupData("Tallon Overworld: Transport Tunnel B"),
                ],
            ),
            RoomName.Transport_Tunnel_C: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Overgrown_Cavern, defaultLock=DoorLockType.Ice
                    ),
                    1: DoorData(
                        RoomName.Transport_to_Chozo_Ruins_East,
                        defaultLock=DoorLockType.Ice,
                    ),
                },
            ),
            RoomName.Transport_Tunnel_D: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(RoomName.Great_Tree_Hall, defaultLock=DoorLockType.Ice),
                    1: DoorData(
                        RoomName.Transport_to_Chozo_Ruins_South,
                        defaultLock=DoorLockType.Ice,
                    ),
                },
            ),
            RoomName.Transport_Tunnel_E: RoomData(
                include_area_in_name=True,
                doors={
                    0: DoorData(
                        RoomName.Transport_to_Phazon_Mines_East,
                        defaultLock=DoorLockType.Ice,
                    ),
                    1: DoorData(
                        RoomName.Great_Tree_Hall,
                        defaultLock=DoorLockType.Ice,
                        rule_func=lambda world, state: can_boost(world, state)
                        and can_space_jump(world, state),
                        sub_region_door_index=0,
                        sub_region_access_override=lambda world, state: True,
                    ),
                },
            ),
            RoomName.Waterfall_Cavern: RoomData(
                doors={
                    0: DoorData(RoomName.Landing_Site, rule_func=can_morph_ball),
                    1: DoorData(
                        RoomName.Frigate_Crash_Site,
                        blast_shield=BlastShieldType.Missile,
                        rule_func=can_morph_ball,
                    ),
                },
            ),
        }
        self._init_room_names_and_areas()

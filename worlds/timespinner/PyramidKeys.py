from typing import Tuple
from BaseClasses import MultiWorld
from .Options import is_option_enabled

def get_pyramid_keys_unlock(world: MultiWorld, player: int) -> str:
    present_teleportation_gates: Tuple[str, ...] = (
        "GateKittyBoss",
        "GateLeftLibrary",
        "GateMilitairyGate",
        "GateSealedCaves",
        "GateSealedSirensCave",
        "GateLakeDesolation"
    )

    past_teleportation_gates: Tuple[str, ...] = (
        "GateLakeSirineRight",
        "GateAccessToPast",
        "GateCastleRamparts",
        "GateCastleKeep",
        "GateRoyalTowers",
        "GateMaw",
        "GateCavesOfBanishment"
    )

    if is_option_enabled(world, player, "Inverted"):
        gates = present_teleportation_gates
    else:
        gates = (*past_teleportation_gates, *present_teleportation_gates)

    if not world:
        return gates[0]

    return world.random.choice(gates)
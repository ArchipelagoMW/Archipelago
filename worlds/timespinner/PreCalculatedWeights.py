from typing import Tuple, Dict, Union
from BaseClasses import MultiWorld
from .Options import is_option_enabled, get_option_value


class PreCalculatedWeights:
    pyramid_keys_unlock: str
    flood_basement: bool
    flood_basement_high: bool
    flood_xarion: bool
    flood_maw: bool
    flood_pyramid_shaft: bool
    flood_pyramid_back: bool
    flood_moat: bool
    flood_courtyard: bool
    flood_lake_desolation: bool
    dry_lake_serene: bool

    def __init__(self, world: MultiWorld, player: int):
        weights_overrrides: Dict[str, Dict[str, int]] = self.get_flood_weights_overrides(world, player)

        self.flood_basement, self.flood_basement_high = \
            self.roll_flood_setting_with_available_save(world, player, weights_overrrides, "CastleBasement")
        self.flood_xarion = self.roll_flood_setting(world, player, weights_overrrides, "Xarion")
        self.flood_maw = self.roll_flood_setting(world, player, weights_overrrides, "Maw")
        self.flood_pyramid_shaft = self.roll_flood_setting(world, player, weights_overrrides, "AncientPyramidShaft")
        self.flood_pyramid_back = self.roll_flood_setting(world, player, weights_overrrides, "Sandman")
        self.flood_moat = self.roll_flood_setting(world, player, weights_overrrides, "CastleMoat")
        self.flood_courtyard = self.roll_flood_setting(world, player, weights_overrrides, "CastleCourtyard")
        self.flood_lake_desolation = self.roll_flood_setting(world, player, weights_overrrides, "LakeDesolation")
        self.dry_lake_serene = self.roll_flood_setting(world, player, weights_overrrides, "LakeSerene")

        self.pyramid_keys_unlock = self.get_pyramid_keys_unlock(world, player, self.flood_maw)


    def get_pyramid_keys_unlock(self, world: MultiWorld, player: int, is_maw_flooded: bool) -> str:
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
            "GateCavesOfBanishment"
        )

        past_water_locked_teleportation_gates: Tuple[str, ...] = (
            "GateMaw",
        )

        if is_option_enabled(world, player, "Inverted"):
            gates = present_teleportation_gates
        else:
            if is_maw_flooded:
                gates = (*past_teleportation_gates, *present_teleportation_gates)
            else:
                gates = (*past_teleportation_gates, *present_teleportation_gates, *past_water_locked_teleportation_gates)

        if not world:
            return gates[0]

        return world.random.choice(gates)


    def get_flood_weights_overrides(self, world: MultiWorld, player: int) -> Dict[str, int]:
        weights_overrrides_option: Union[int, Dict[str, Dict[str, int]]] = \
            get_option_value(world, player, "RisingTidesOverrides")

        if (weights_overrrides_option == 0):
            return {}
        else:
            return weights_overrrides_option 


    def roll_flood_setting(self, world: MultiWorld, player: int, weights: Dict[str, Dict[str, int]], key: str) -> bool:
        if not world or not is_option_enabled(world, player, "RisingTides"):
            return False

        if not key in weights:
            weights[key] = { "Dry": 67, "Flooded": 33 }

        result: str = world.random.choices(list(weights[key].keys()), weights=list(map(int, weights[key].values())))[0]

        return result == "Flooded"


    def roll_flood_setting_with_available_save(self, world: MultiWorld, player: int, \
                                               weights: Dict[str, Dict[str, int]], key: str) -> Tuple[bool, bool]:

        if not world or not is_option_enabled(world, player, "RisingTides"):
            return (False, False)

        if not key in weights:
            weights[key] = { "Dry": 66, "Flooded": 17, "FloodedWithSavePointAvailable": 17 }

        result: str = world.random.choices(list(weights[key].keys()), weights=list(map(int, weights[key].values()), 1))[0]

        if (result == "Dry"):
            return (False, False)
        elif (result == "Flooded"):
            return (True, False)
        elif (result == "FloodedWithSavePointAvailable"):
            return (True, True)

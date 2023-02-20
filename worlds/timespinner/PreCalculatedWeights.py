from typing import Tuple, Dict, Union
from BaseClasses import MultiWorld
from .Options import is_option_enabled, get_option_value


class PreCalculatedWeights:
    pyramid_keys_unlock: str
    present_key_unlock: str
    past_key_unlock: str
    time_key_unlock: str

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

        self.pyramid_keys_unlock, self.present_key_unlock, self.past_key_unlock, self.time_key_unlock = \
            self.get_pyramid_keys_unlock(world, player, self.flood_maw)


    def get_pyramid_keys_unlock(self, world: MultiWorld, player: int, is_maw_flooded: bool) -> Tuple[str, str, str, str]:
        present_teleportation_gates: Tuple[str, ...] = (
            "GateKittyBoss",
            "GateLeftLibrary",
            "GateMilitaryGate",
            "GateSealedCaves",
            "GateSealedSirensCave",
            "GateLakeDesolation"
        )

        past_teleportation_gates: Tuple[str, ...] = (
            "GateLakeSereneRight",
            "GateAccessToPast",
            "GateCastleRamparts",
            "GateCastleKeep",
            "GateRoyalTowers",
            "GateCavesOfBanishment"
        )

        ancient_pyramid_teleportation_gates: Tuple[str, ...] = (
            "GateGyre",
            "GateLeftPyramid",
            "GateRightPyramid"
        )

        if not world:
            return (
                present_teleportation_gates[0], 
                present_teleportation_gates[0], 
                past_teleportation_gates[0], 
                ancient_pyramid_teleportation_gates[0]
            )

        if not is_maw_flooded:
            past_teleportation_gates += ("GateMaw", )

        if is_option_enabled(world, player, "Inverted"):
            all_gates: Tuple[str, ...] = present_teleportation_gates
        else:
            all_gates: Tuple[str, ...] = past_teleportation_gates + present_teleportation_gates

        return (
            world.random.choice(all_gates),
            world.random.choice(present_teleportation_gates),
            world.random.choice(past_teleportation_gates),
            world.random.choice(ancient_pyramid_teleportation_gates)
        )

    @staticmethod
    def get_flood_weights_overrides( world: MultiWorld, player: int) -> Dict[str, int]:
        weights_overrides_option: Union[int, Dict[str, Dict[str, int]]] = \
            get_option_value(world, player, "RisingTidesOverrides")

        if weights_overrides_option == 0:
            return {}
        else:
            return weights_overrides_option 

    @staticmethod
    def roll_flood_setting(world: MultiWorld, player: int, weights: Dict[str, Dict[str, int]], key: str) -> bool:
        if not world or not is_option_enabled(world, player, "RisingTides"):
            return False

        weights = weights[key] if key in weights else { "Dry": 67, "Flooded": 33 }

        result: str = world.random.choices(list(weights.keys()), weights=list(map(int, weights.values())))[0]

        return result == "Flooded"

    @staticmethod
    def roll_flood_setting_with_available_save(world: MultiWorld, player: int,
                                               weights: Dict[str, Dict[str, int]], key: str) -> Tuple[bool, bool]:

        if not world or not is_option_enabled(world, player, "RisingTides"):
            return False, False

        weights = weights[key] if key in weights else {"Dry": 66, "Flooded": 17, "FloodedWithSavePointAvailable": 17}

        result: str = world.random.choices(list(weights.keys()), weights=list(map(int, weights.values())))[0]
        
        if result == "Dry":
            return False, False
        elif result == "Flooded":
            return True, False
        elif result == "FloodedWithSavePointAvailable":
            return True, True

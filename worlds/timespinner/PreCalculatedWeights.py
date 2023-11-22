from typing import Tuple, Dict, Union, List
from BaseClasses import MultiWorld
from .Options import timespinner_options, is_option_enabled, get_option_value

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
    flood_lake_serene: bool
    flood_lake_serene_bridge: bool
    flood_lab: bool

    def __init__(self, world: MultiWorld, player: int):
        if world and is_option_enabled(world, player, "RisingTides"):
            weights_overrrides: Dict[str, Union[str, Dict[str, int]]] = self.get_flood_weights_overrides(world, player)

            self.flood_basement, self.flood_basement_high = \
                self.roll_flood_setting(world, player, weights_overrrides, "CastleBasement")
            self.flood_xarion, _ = self.roll_flood_setting(world, player, weights_overrrides, "Xarion")
            self.flood_maw, _ = self.roll_flood_setting(world, player, weights_overrrides, "Maw")
            self.flood_pyramid_shaft, _ = self.roll_flood_setting(world, player, weights_overrrides, "AncientPyramidShaft")
            self.flood_pyramid_back, _ = self.roll_flood_setting(world, player, weights_overrrides, "Sandman")
            self.flood_moat, _ = self.roll_flood_setting(world, player, weights_overrrides, "CastleMoat")
            self.flood_courtyard, _ = self.roll_flood_setting(world, player, weights_overrrides, "CastleCourtyard")
            self.flood_lake_desolation, _ = self.roll_flood_setting(world, player, weights_overrrides, "LakeDesolation")
            self.flood_lake_serene, _ = self.roll_flood_setting(world, player, weights_overrrides, "LakeSerene")
            self.flood_lake_serene_bridge, _ = self.roll_flood_setting(world, player, weights_overrrides, "LakeSereneBridge")
            self.flood_lab, _ = self.roll_flood_setting(world, player, weights_overrrides, "Lab")
        else:
            self.flood_basement = False
            self.flood_basement_high = False
            self.flood_xarion = False
            self.flood_maw = False
            self.flood_pyramid_shaft = False
            self.flood_pyramid_back = False
            self.flood_moat = False
            self.flood_courtyard = False
            self.flood_lake_desolation = False
            self.flood_lake_serene = True 
            self.flood_lake_serene_bridge = False
            self.flood_lab = False

        self.pyramid_keys_unlock, self.present_key_unlock, self.past_key_unlock, self.time_key_unlock = \
            self.get_pyramid_keys_unlocks(world, player, self.flood_maw, self.flood_xarion)

    @staticmethod
    def get_pyramid_keys_unlocks(world: MultiWorld, player: int, is_maw_flooded: bool, is_xarion_flooded: bool) -> Tuple[str, str, str, str]:
        present_teleportation_gates: List[str] = [
            "GateKittyBoss",
            "GateLeftLibrary",
            "GateMilitaryGate",
            "GateSealedCaves",
            "GateSealedSirensCave",
            "GateLakeDesolation"
        ]

        past_teleportation_gates: List[str] = [
            "GateLakeSereneRight",
            "GateAccessToPast",
            "GateCastleRamparts",
            "GateCastleKeep",
            "GateRoyalTowers",
            "GateCavesOfBanishment"
        ]

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
            past_teleportation_gates.append("GateMaw")

        if not is_xarion_flooded:
            present_teleportation_gates.append("GateXarion")

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
    def get_flood_weights_overrides(world: MultiWorld, player: int) -> Dict[str, Union[str, Dict[str, int]]]:
        weights_overrides_option: Union[int, Dict[str, Union[str, Dict[str, int]]]] = \
            get_option_value(world, player, "RisingTidesOverrides")

        default_weights: Dict[str, Dict[str, int]] = timespinner_options["RisingTidesOverrides"].default

        if not weights_overrides_option:
            weights_overrides_option = default_weights
        else:
            for key, weights in default_weights.items():
                if not key in weights_overrides_option:
                    weights_overrides_option[key] = weights

        return weights_overrides_option 

    @staticmethod
    def roll_flood_setting(world: MultiWorld, player: int,
            all_weights: Dict[str, Union[Dict[str, int], str]], key: str) -> Tuple[bool, bool]:

        weights: Union[Dict[str, int], str] = all_weights[key]

        if isinstance(weights, dict):
            result: str = world.random.choices(list(weights.keys()), weights=list(map(int, weights.values())))[0]
        else:
            result: str = weights
        
        if result == "Dry":
            return False, False
        elif result == "Flooded":
            return True, True
        elif result == "FloodedWithSavePointAvailable":
            return True, False

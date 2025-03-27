from typing import Tuple, Dict, Union, List
from random import Random
from .Options import TimespinnerOptions

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

    def __init__(self, options: TimespinnerOptions, random: Random):
        if options.rising_tides:
            weights_overrrides: Dict[str, Union[str, Dict[str, int]]] = self.get_flood_weights_overrides(options)

            self.flood_basement, self.flood_basement_high = \
                self.roll_flood_setting(random, weights_overrrides, "CastleBasement")
            self.flood_xarion, _ = self.roll_flood_setting(random, weights_overrrides, "Xarion")
            self.flood_maw, _ = self.roll_flood_setting(random, weights_overrrides, "Maw")
            self.flood_pyramid_shaft, _ = self.roll_flood_setting(random, weights_overrrides, "AncientPyramidShaft")
            self.flood_pyramid_back, _ = self.roll_flood_setting(random, weights_overrrides, "Sandman")
            self.flood_moat, _ = self.roll_flood_setting(random, weights_overrrides, "CastleMoat")
            self.flood_courtyard, _ = self.roll_flood_setting(random, weights_overrrides, "CastleCourtyard")
            self.flood_lake_desolation, _ = self.roll_flood_setting(random, weights_overrrides, "LakeDesolation")
            self.flood_lake_serene, _ = self.roll_flood_setting(random, weights_overrrides, "LakeSerene")
            self.flood_lake_serene_bridge, _ = self.roll_flood_setting(random, weights_overrrides, "LakeSereneBridge")
            self.flood_lab, _ = self.roll_flood_setting(random, weights_overrrides, "Lab")
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
            self.get_pyramid_keys_unlocks(options, random, self.flood_maw, self.flood_xarion, self.flood_lab)

    @staticmethod
    def get_pyramid_keys_unlocks(options: TimespinnerOptions, random: Random,
                                 is_maw_flooded: bool, is_xarion_flooded: bool,
                                 is_lab_flooded: bool) -> Tuple[str, str, str, str]:
        
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

        if not is_maw_flooded:
            past_teleportation_gates.append("GateMaw")

        if options.risky_warps: 
            past_teleportation_gates.append("GateLakeSereneLeft")
            present_teleportation_gates.append("GateDadsTower")
            if not is_xarion_flooded:
                present_teleportation_gates.append("GateXarion")
            if not is_lab_flooded:
                present_teleportation_gates.append("GateLabEntrance")

        if options.inverted or (options.pyramid_start and not options.back_to_the_future):
            all_gates: Tuple[str, ...] = present_teleportation_gates
        else:
            all_gates: Tuple[str, ...] = past_teleportation_gates + present_teleportation_gates

        return (
            random.choice(all_gates),
            random.choice(present_teleportation_gates),
            random.choice(past_teleportation_gates),
            random.choice(ancient_pyramid_teleportation_gates)
        )

    @staticmethod
    def get_flood_weights_overrides(options: TimespinnerOptions) -> Dict[str, Union[str, Dict[str, int]]]:
        weights_overrides_option: Union[int, Dict[str, Union[str, Dict[str, int]]]] = \
            options.rising_tides_overrides.value

        default_weights: Dict[str, Dict[str, int]] = options.rising_tides_overrides.default

        if not weights_overrides_option:
            weights_overrides_option = default_weights
        else:
            for key, weights in default_weights.items():
                if not key in weights_overrides_option:
                    weights_overrides_option[key] = weights

        return weights_overrides_option 

    @staticmethod
    def roll_flood_setting(random: Random, all_weights: Dict[str, Union[Dict[str, int], str]],
                           key: str) -> Tuple[bool, bool]:

        weights: Union[Dict[str, int], str] = all_weights[key]

        if isinstance(weights, dict):
            result: str = random.choices(list(weights.keys()), weights=list(map(int, weights.values())))[0]
        else:
            result: str = weights
        
        if result == "Dry":
            return False, False
        elif result == "Flooded":
            return True, True
        elif result == "FloodedWithSavePointAvailable":
            return True, False

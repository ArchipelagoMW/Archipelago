from typing import Any, Dict

import Options as APOptions
from . import LuigiOptions as LMOptions

all_random_settings = {
    "progression_balancing":                          "random",
    "accessibility":                                  "random",
    LMOptions.Goal.display_name:                      "random",
    LMOptions.RankRequirement.display_name:           "random",
    LMOptions.LuigiWalkSpeed.display_name:            "random",
    LMOptions.LuigiFearAnim.display_name:             "random",
    LMOptions.BetterVacuum.display_name:              "random",
    LMOptions.StartWithBooRadar.display_name:         "random",
    LMOptions.StartHiddenMansion.display_name:        "random",
    LMOptions.PickupAnim.display_name:                "random",
    LMOptions.RandomMusic.display_name:               "random",
    LMOptions.DoorRando.display_name:                 "random",
    LMOptions.PortraitHints.display_name:             "random",
    LMOptions.HintDistribution.display_name:          "random",
    LMOptions.Toadsanity.display_name:                "random",
    LMOptions.Plants.display_name:                    "random",
    LMOptions.Furnisanity.display_name:               "random",
    LMOptions.Boosanity.display_name:                 "random",
    LMOptions.Portrification.display_name:            "random",
    LMOptions.Lightsanity.display_name:               "random",
    LMOptions.Walksanity.display_name:                "random",
    LMOptions.SpeedySpirits.display_name:             "random",
    LMOptions.BooGates.display_name:                  "random",
    LMOptions.KingBooHealth.display_name:             "random",
    LMOptions.MarioItems.display_name:                "random",
    LMOptions.WashroomBooCount.display_name:          "random",
    LMOptions.BalconyBooCount.display_name:           "random",
    LMOptions.FinalBooCount.display_name:             "random",
    LMOptions.BundleWeight.display_name:              "random",
    LMOptions.CoinWeight.display_name:                "random",
    LMOptions.BillWeight.display_name:                "random",
    LMOptions.BarsWeight.display_name:                "random",
    LMOptions.GemsWeight.display_name:                "random",
    LMOptions.PoisonTrapWeight.display_name:          "random",
    LMOptions.BombWeight.display_name:                "random",
    LMOptions.IceTrapWeight.display_name:             "random",
    LMOptions.BananaTrapWeight.display_name:          "random",
    LMOptions.Enemizer.display_name:                  "random",
    LMOptions.Deathlink.display_name:                 "random"
}

allsanity_settings = {
    LMOptions.Toadsanity.display_name:                "true",
    LMOptions.Plants.display_name:                    "true",
    LMOptions.Furnisanity.display_name:               "true",
    LMOptions.Boosanity.display_name:                 "true",
    LMOptions.Portrification.display_name:            "true",
    LMOptions.Lightsanity.display_name:               "true",
    LMOptions.Walksanity.display_name:                "true",
    LMOptions.SpeedySpirits.display_name:             "true",
}

money_settings = {
    LMOptions.BundleWeight.display_name:              100,
    LMOptions.CoinWeight.display_name:                100,
    LMOptions.BillWeight.display_name:                100,
    LMOptions.BarsWeight.display_name:                100,
    LMOptions.GemsWeight.display_name:                100,
    LMOptions.PoisonTrapWeight.display_name:          0,
    LMOptions.BombWeight.display_name:                0,
    LMOptions.IceTrapWeight.display_name:             0,
    LMOptions.BananaTrapWeight.display_name:          0,
}

trap_settings = {
    LMOptions.BundleWeight.display_name:              0,
    LMOptions.CoinWeight.display_name:                0,
    LMOptions.BillWeight.display_name:                0,
    LMOptions.BarsWeight.display_name:                0,
    LMOptions.GemsWeight.display_name:                0,
    LMOptions.PoisonTrapWeight.display_name:          100,
    LMOptions.BombWeight.display_name:                100,
    LMOptions.IceTrapWeight.display_name:             100,
    LMOptions.BananaTrapWeight.display_name:          100,
}

lm_options_presets: Dict[str, Dict[str, Any]] = {
    "All random": all_random_settings,
    "I Love Money": money_settings,
    "Raining Traps": trap_settings,
    "Allsanity": allsanity_settings,
}
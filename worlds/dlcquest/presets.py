from typing import Any, Dict

from .Options import DoubleJumpGlitch, CoinSanity, CoinSanityRange, PermanentCoins, TimeIsMoney, EndingChoice, Campaign, ItemShuffle

all_random_settings = {
    DoubleJumpGlitch.internal_name:         "random",
    CoinSanity.internal_name:               "random",
    CoinSanityRange.internal_name:          "random",
    PermanentCoins.internal_name:           "random",
    TimeIsMoney.internal_name:              "random",
    EndingChoice.internal_name:             "random",
    Campaign.internal_name:                 "random",
    ItemShuffle.internal_name:              "random",
    "death_link":                           "random",
}

main_campaign_settings = {
    DoubleJumpGlitch.internal_name:         DoubleJumpGlitch.option_none,
    CoinSanity.internal_name:               CoinSanity.option_coin,
    CoinSanityRange.internal_name:          30,
    PermanentCoins.internal_name:           PermanentCoins.option_false,
    TimeIsMoney.internal_name:              TimeIsMoney.option_required,
    EndingChoice.internal_name:             EndingChoice.option_true,
    Campaign.internal_name:                 Campaign.option_basic,
    ItemShuffle.internal_name:              ItemShuffle.option_shuffled,
}

lfod_campaign_settings = {
    DoubleJumpGlitch.internal_name:         DoubleJumpGlitch.option_none,
    CoinSanity.internal_name:               CoinSanity.option_coin,
    CoinSanityRange.internal_name:          30,
    PermanentCoins.internal_name:           PermanentCoins.option_false,
    TimeIsMoney.internal_name:              TimeIsMoney.option_required,
    EndingChoice.internal_name:             EndingChoice.option_true,
    Campaign.internal_name:                 Campaign.option_live_freemium_or_die,
    ItemShuffle.internal_name:              ItemShuffle.option_shuffled,
}

easy_settings = {
    DoubleJumpGlitch.internal_name:         DoubleJumpGlitch.option_none,
    CoinSanity.internal_name:               CoinSanity.option_none,
    CoinSanityRange.internal_name:          40,
    PermanentCoins.internal_name:           PermanentCoins.option_true,
    TimeIsMoney.internal_name:              TimeIsMoney.option_required,
    EndingChoice.internal_name:             EndingChoice.option_true,
    Campaign.internal_name:                 Campaign.option_both,
    ItemShuffle.internal_name:              ItemShuffle.option_shuffled,
}

hard_settings = {
    DoubleJumpGlitch.internal_name:         DoubleJumpGlitch.option_simple,
    CoinSanity.internal_name:               CoinSanity.option_coin,
    CoinSanityRange.internal_name:          30,
    PermanentCoins.internal_name:           PermanentCoins.option_false,
    TimeIsMoney.internal_name:              TimeIsMoney.option_optional,
    EndingChoice.internal_name:             EndingChoice.option_true,
    Campaign.internal_name:                 Campaign.option_both,
    ItemShuffle.internal_name:              ItemShuffle.option_shuffled,
}


dlcq_options_presets: Dict[str, Dict[str, Any]] = {
    "All random": all_random_settings,
    "Main campaign": main_campaign_settings,
    "LFOD campaign": lfod_campaign_settings,
    "Both easy": easy_settings,
    "Both hard": hard_settings,
}

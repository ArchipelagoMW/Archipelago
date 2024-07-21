from Options import DeathLink, ProgressionBalancing, Accessibility, OptionGroup
from .Options import (Campaign, ItemShuffle, TimeIsMoney, EndingChoice, PermanentCoins, DoubleJumpGlitch, CoinSanity,
                      CoinSanityRange, DeathLink)

dlcq_option_groups = [
    OptionGroup("General", [
        Campaign,
        ItemShuffle,
        CoinSanity,
    ]),
    OptionGroup("Tedious and Grind", [
        TimeIsMoney,
        DoubleJumpGlitch,
    ]),
    OptionGroup("Extra Customization", [
        EndingChoice,
        PermanentCoins,
        CoinSanityRange,
    ]),
    OptionGroup("Advanced Options", [
        DeathLink,
        ProgressionBalancing,
        Accessibility,
    ]),
]

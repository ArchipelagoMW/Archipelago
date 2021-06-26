import typing

from Options import Option, DefaultOnToggle, Toggle

hollow_knight_randomize_options: typing.Dict[str, type(Option)] = {
    "RandomizeDreamers": DefaultOnToggle,
    "RandomizeSkills": DefaultOnToggle,
    "RandomizeCharms": DefaultOnToggle,
    "RandomizeKeys": DefaultOnToggle,
    "RandomizeGeoChests": Toggle,
    "RandomizeMaskShards": DefaultOnToggle,
    "RandomizeVesselFragments": DefaultOnToggle,
    "RandomizeCharmNotches": Toggle,
    "RandomizePaleOre": DefaultOnToggle,
    "RandomizeRancidEggs": Toggle,
    "RandomizeRelics": DefaultOnToggle,
    "RandomizeMaps": Toggle,
    "RandomizeStags": Toggle,
    "RandomizeGrubs": Toggle,
    "RandomizeWhisperingRoots": Toggle,
    "RandomizeRocks": Toggle,
    "RandomizeSoulTotems": Toggle,
    "RandomizePalaceTotems": Toggle,
    "RandomizeLoreTablets": Toggle,
    "RandomizeLifebloodCocoons": Toggle,
    "RandomizeFlames": Toggle
}
hollow_knight_skip_options: typing.Dict[str, type(Option)] = {
    "MILDSKIPS": Toggle,
    "SPICYSKIPS": Toggle,
    "FIREBALLSKIPS": Toggle,
    "ACIDSKIPS": Toggle,
    "SPIKETUNNELS": Toggle,
    "DARKROOMS": Toggle,
    "CURSED": Toggle,
    "SHADESKIPS": Toggle,
}
hollow_knight_options: typing.Dict[str, type(Option)] = {**hollow_knight_randomize_options,
                                                         **hollow_knight_skip_options}
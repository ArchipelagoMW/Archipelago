from Options import Toggle, Choice


class RandomizeHiddenItems(Toggle):
    """Enabled: Hidden Items are shuffled into the pool
        Disabled: Hidden Items are vanilla"""
    display_name = "Randomize Hidden Items"
    default = 0


class RandomizeStarters(Toggle):
    """Enabled: Starter Pokemon species are random
        Disabled: Starter Pokemon species are vanilla"""
    display_name = "Randomize Starters"
    default = 1


class RandomizeWilds(Toggle):
    """Enabled: Wild Pokemon species are random
        Disabled: Wild Pokemon species are vanilla"""
    display_name = "Randomize Wilds"
    default = 1


class RandomizeLearnsets(Choice):
    """start_with_four_moves: Random movesets with 4 starting moves
    randomize: Random movesets
    vanilla: Vanilla movesets"""
    display_name = "Randomize Learnsets"
    default = 2
    option_start_with_four_moves = 2
    option_randomize = 1
    option_vanilla = 0


class FullTmHmCompatibility(Toggle):
    """Enabled: All Pokemon are compatible with all TMs and HMs 
        Disabled: TM and HM compatibility is vanilla"""
    display_name = "Full TM/HM Compatibility"
    default = 1


class BlindTrainers(Toggle):
    """"""
    display_name = "Blind Trainers"
    default = 1


pokemon_crystal_options = {
    "randomize_hidden_items": RandomizeHiddenItems,
    "randomize_starters": RandomizeStarters,
    "randomize_wilds": RandomizeWilds,
    "randomize_learnsets": RandomizeLearnsets,
    "full_tmhm_compatibility": FullTmHmCompatibility,
    "blind_trainers": BlindTrainers
}

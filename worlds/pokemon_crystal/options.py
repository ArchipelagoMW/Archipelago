from Options import Toggle


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


class FullTmHmCompatibility(Toggle):
    """Enabled: All Pokemon are compatible with all TMs and HMs 
        Disabled: TM and HM compatibility is vanilla"""
    display_name = "Full TM/HM Compatibility"
    default = 1


pokemon_crystal_options = {
    "randomize_hidden_items": RandomizeHiddenItems,
    "randomize_starters": RandomizeStarters,
    "randomize_wilds": RandomizeWilds,
    "full_tmhm_compatibility": FullTmHmCompatibility
}

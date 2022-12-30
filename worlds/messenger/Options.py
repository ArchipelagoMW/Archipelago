from Options import Toggle, DefaultOnToggle


class Logic(DefaultOnToggle):
    """Whether the seed should be guaranteed completable."""
    display_name = "Use Logic"


class PowerSeals(Toggle):
    """Whether power seal locations should be randomized."""
    display_name = "Shuffle Seals"


messenger_options = {
    "enable_logic": Logic,
    "shuffle_seals": PowerSeals,
}

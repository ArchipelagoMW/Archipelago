from Options import Toggle


class PowerSeals(Toggle):
    """Whether power seal locations should be randomized."""
    display_name = "Shuffle Seals"


messenger_options = {
    "shuffle_seals": PowerSeals,
}

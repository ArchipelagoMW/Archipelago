from Options import Toggle, DefaultOnToggle, DeathLink, Range


class Logic(DefaultOnToggle):
    """Whether the seed should be guaranteed completable."""
    display_name = "Use Logic"


class PowerSeals(Toggle):
    """Whether power seal locations should be randomized."""
    display_name = "Shuffle Seals"


class NotesNeeded(Range):
    """How many notes are needed to access the Music Box."""
    display_name = "Notes Needed"
    range_start = 1
    range_end = 6
    default = range_end


messenger_options = {
    "enable_logic": Logic,
    "shuffle_seals": PowerSeals,
    "notes_needed": NotesNeeded,
    "death_link": DeathLink,
}

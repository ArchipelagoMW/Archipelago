from Options import DefaultOnToggle, DeathLink, Range, Accessibility, Choice


class MessengerAccessibility(Accessibility):
    default = 0
    # defaulting to locations accessibility since items makes certain items self-locking


class Logic(DefaultOnToggle):
    """Whether the seed should be guaranteed completable."""
    display_name = "Use Logic"


class PowerSeals(DefaultOnToggle):
    """Whether power seal locations should be randomized."""
    display_name = "Shuffle Seals"


class Goal(Choice):
    """Requirement to finish the game. Shop Chest will force seals to be shuffled."""
    option_phantom = 0
    option_shop_chest = 1


class NotesNeeded(Range):
    """How many notes are needed to access the Music Box."""
    display_name = "Notes Needed"
    range_start = 1
    range_end = 6
    default = range_end


class AmountSeals(Range):
    """Number of power seals that exist in the item pool when shop chest is the goal."""
    range_start = 1
    range_end = 45
    default = range_end


class RequiredSeals(Range):
    """Percentage of total seals required to open the sh op chest."""
    range_start = 10
    range_end = 100
    default = range_end


messenger_options = {
    "accessibility": MessengerAccessibility,
    "enable_logic": Logic,
    "shuffle_seals": PowerSeals,
    "goal": Goal,
    "notes_needed": NotesNeeded,
    "total_seals": AmountSeals,
    "percent_seals_required": RequiredSeals,
    "death_link": DeathLink,
}

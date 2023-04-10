from Options import DefaultOnToggle, DeathLink, Range, Accessibility, Choice, Toggle


class MessengerAccessibility(Accessibility):
    default = Accessibility.option_locations
    # defaulting to locations accessibility since items makes certain items self-locking
    __doc__ = Accessibility.__doc__.replace(f"default {Accessibility.default}", f"default {default}")


class Logic(Choice):
    """
    The level of logic to use when determining what locations in your world are accessible.
    Normal can require damage boosts, but otherwise approachable for someone who has beaten the game.
    Hard has some easier speedrunning tricks in logic. May need to leash.
    Challenging contains more medium and hard difficulty speedrunning tricks.
    OoB places everything with the minimum amount of rules possible. Expect to do OoB. Not guaranteed completable.
    """
    display_name = "Logic Level"
    option_normal = 0
    option_hard = 1
    option_challenging = 2
    option_oob = 3


class PowerSeals(DefaultOnToggle):
    """Whether power seal locations should be randomized."""
    display_name = "Shuffle Seals"


class MegaShards(Toggle):
    """Whether mega shards should be item locations."""
    display_name = "Shuffle Mega Time Shards"


class Goal(Choice):
    """Requirement to finish the game. Power Seal Hunt will force power seal locations to be shuffled."""
    display_name = "Goal"
    option_open_music_box = 0
    option_power_seal_hunt = 1


class MusicBox(DefaultOnToggle):
    """Whether the music box gauntlet needs to be done."""
    display_name = "Music Box Gauntlet"


class NotesNeeded(Range):
    """How many notes are needed to access the Music Box."""
    display_name = "Notes Needed"
    range_start = 1
    range_end = 6
    default = range_end


class AmountSeals(Range):
    """Number of power seals that exist in the item pool when power seal hunt is the goal."""
    display_name = "Total Power Seals"
    range_start = 1
    range_end = 85
    default = 45


class RequiredSeals(Range):
    """Percentage of total seals required to open the shop chest."""
    display_name = "Percent Seals Required"
    range_start = 10
    range_end = 100
    default = range_end


messenger_options = {
    "accessibility": MessengerAccessibility,
    "logic_level": Logic,
    "shuffle_seals": PowerSeals,
    "shuffle_shards": MegaShards,
    "goal": Goal,
    "music_box": MusicBox,
    "notes_needed": NotesNeeded,
    "total_seals": AmountSeals,
    "percent_seals_required": RequiredSeals,
    "death_link": DeathLink,
}

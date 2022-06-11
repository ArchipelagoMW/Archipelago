import typing
from Options import Option, DefaultOnToggle, Range, Toggle, DeathLink, Choice

class ExpandedPool(DefaultOnToggle):
    """Puts room clear drops and Take Any caves into the pool of items and locations."""
    display_name = "Expanded Item Pool"

class TriforceLocations(Choice):
    """Where Triforce fragments can be located. Note that Triforce pieces
    obtained in a dungeon will heal and warp you out, while overworld Triforce pieces obtained will appear to have
    no immediate effect. This is normal."""
    display_name = "Triforce Locations"
    option_vanilla = 0
    option_dungeons = 1
    option_anywhere = 2

class StartingPosition(Choice):
    """How easy is the start of the game. <em>Safe</em> means a weapon is guaranteed in Wooden Sword Cave.
    <em>Unsafe</em> means that progression is guaranteed between Wooden Sword Cave, Letter Cave, and Armos Knight
    as well as any locations they unlock. <em>Dangerous</em> can require seeking out money and gambling caves in order
    to purchase initial progression."""
    display_name = "Starting Position"
    option_safe = 0
    option_unsafe = 1
    option_dangerous = 2

tloz_options: typing.Dict[str, type(Option)] = {
    "ExpandedPool": ExpandedPool,
    "TriforceLocations": TriforceLocations,
    "StartingPosition": StartingPosition
}

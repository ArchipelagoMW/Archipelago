from Options import Toggle, Range, Choice, Option
import typing


class DeathLink(Toggle):
    """Activate DeathLink"""
    display_name = "DeathLink"


class Trap(Toggle):
    """Put some traps in the item pool"""
    display_name = "Trap"


class RandomizeCodes(Toggle):
    """Randomize All codes in the game(Clock, safe, etc.)"""
    display_name = "Randomize Codes"


class RandomizeDeck(Toggle):
    """Randomize every card of the deck at the start of every encounter"""
    display_name = "Randomize deck"


inscryption_options: typing.Dict[str, type(Option)] = {
    "deathlink": DeathLink,
    "trap": Trap,
    "randomize_codes": RandomizeCodes,
    "randomize_deck": RandomizeDeck,
}

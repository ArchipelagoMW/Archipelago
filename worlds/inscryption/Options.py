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


class OptionalDeathCard(Choice):
    """Add a Moment after death where you can decide to create a death card or not.
    Disable: Disable the feature.
    Always on: The feature is always on.
    DeathLink Only: The feature only happens during a DeathLink death."""
    auto_display_name = True
    display_name = "Optional Death Card"
    option_disable = 0
    option_always_on = 1
    option_deathlink_only = 2

    def get_event_name(self) -> str:
        return {
            self.option_disable: "Disable",
            self.option_always_on: "Always on",
            self.option_deathlink_only: "DeathLink Only",
        }[self.value]


inscryption_options: typing.Dict[str, type(Option)] = {
    "deathlink": DeathLink,
    "trap": Trap,
    "randomize_codes": RandomizeCodes,
    "randomize_deck": RandomizeDeck,
    "optional_death_card": OptionalDeathCard,
}

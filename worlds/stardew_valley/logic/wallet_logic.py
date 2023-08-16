from .museum_logic import MuseumLogic
from .. import options
from ..data.museum_data import dwarf_scrolls, all_museum_items
from ..stardew_rule import StardewRule, And
from .received_logic import ReceivedLogic
from ..strings.wallet_item_names import Wallet


class WalletLogic:
    player: int
    received = ReceivedLogic
    museum: MuseumLogic

    def __init__(self, player: int, received: ReceivedLogic, museum: MuseumLogic):
        self.player = player
        self.received = received
        self.museum = museum

    def can_speak_dwarf(self) -> StardewRule:
        if self.museum.museum_option == options.Museumsanity.option_none:
            return And([self.museum.can_donate_museum_item(item) for item in dwarf_scrolls])
        return self.received("Dwarvish Translation Guide")

    def has_rusty_key(self) -> StardewRule:
        if self.museum.museum_option == options.Museumsanity.option_none:
            required_donations = 80  # It's 60, but without a metal detector I'd rather overshoot so players don't get screwed by RNG
            return self.museum.can_donate_many([item.name for item in all_museum_items], required_donations)
        return self.received(Wallet.rusty_key)

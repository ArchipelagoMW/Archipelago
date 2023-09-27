from .museum_logic import MuseumLogic
from ..stardew_rule import StardewRule
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
        return self.received("Dwarvish Translation Guide")

    def has_rusty_key(self) -> StardewRule:
        return self.received(Wallet.rusty_key)

from functools import cached_property

from .museum_logic import MuseumLogic
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import StardewRule
from ..strings.wallet_item_names import Wallet


class WalletLogic:
    player: int
    received = ReceivedLogicMixin
    museum: MuseumLogic

    def __init__(self, player: int, received: ReceivedLogicMixin, museum: MuseumLogic):
        self.player = player
        self.received = received
        self.museum = museum

    @cached_property
    def can_speak_dwarf(self) -> StardewRule:
        return self.received(Wallet.dwarvish_translation_guide)

    @cached_property
    def has_rusty_key(self) -> StardewRule:
        return self.received(Wallet.rusty_key)

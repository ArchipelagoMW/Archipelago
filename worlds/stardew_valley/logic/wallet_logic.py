from .base_logic import BaseLogic, BaseLogicMixin
from .received_logic import ReceivedLogicMixin
from ..stardew_rule import StardewRule
from ..strings.wallet_item_names import Wallet


class WalletLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet = WalletLogic(*args, **kwargs)


class WalletLogic(BaseLogic):

    def can_speak_dwarf(self) -> StardewRule:
        return self.logic.received(Wallet.dwarvish_translation_guide)

    def has_rusty_key(self) -> StardewRule:
        return self.logic.received(Wallet.rusty_key)

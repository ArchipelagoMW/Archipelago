import logging
import typing
from typing import Dict, List, Optional, NamedTuple
from SNIClient import SNIContext
from NetUtils import NetworkItem

class ItemSend(NamedTuple):
    receiving: int
    item: NetworkItem

class SoulBlazerContext(SNIContext):
    """Extend SNIContext to provide more data"""

    def __init__(self, snes_address: str, server_address: str, password: str) -> None:
        super().__init__(snes_address, server_address, password)
        self.gem_data: Dict[str, int]
        self.exp_data: Dict[str, int]
        self.item_send_queue: List[ItemSend]

    def on_package(self, cmd: str, args: Dict[str, typing.Any]) -> None:
        super().on_package(cmd, args)
        if cmd == "Connected":
            slot_data = args.get("slot_data", None)
            if slot_data:
                self.gem_data = slot_data.get("gem_data", {})
                self.exp_data = slot_data.get("item_data", {})

    def on_print_json(self, args: Dict):
        super().on_print_json(args)

        # We want ItemSends from us to another player so we can print them in game
        if args.get("type", "") == "ItemSend" and args["receiving"] != self.slot and args["item"].player == self.slot:
            self.item_send_queue.append(ItemSend(args["receiving"], args["item"]))
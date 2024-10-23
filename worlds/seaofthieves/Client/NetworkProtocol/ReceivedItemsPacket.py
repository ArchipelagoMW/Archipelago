from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, \
    add_json_text, JSONTypes
import typing


class ReceivedItemsPacket:

    def __init__(self, dict: dict):
        self.index: typing.Optional[int] = dict.get('index')
        self.items: typing.List[NetworkItem] | None = dict.get('items')

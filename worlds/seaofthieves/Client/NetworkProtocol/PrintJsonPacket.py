from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, \
    add_json_text, JSONTypes
import typing


class PrintJsonPacket:

    def __init__(self, dict):
        self.countdown: int = dict.get('countdown')
        self.tags: typing.List[str] | None = dict.get('tags')
        self.message: typing.Optional[str] = dict.get('message')
        self.slot: typing.Optional[int] = dict.get('slot')
        self.team: typing.Optional[int] = dict.get('team')
        self.found: typing.Optional[bool] = dict.get('found')
        self.receiving: typing.Optional[int] = dict.get('receiving')
        self.type: typing.Optional[str] = dict.get('type')
        self.data: typing.List[JSONMessagePart] | None = dict.get('data')
        self.item: NetworkItem | None = dict.get('item')

    def print(self):
        if self.message is not None:
            print(self.message)

from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, \
    add_json_text, JSONTypes
import typing


class SetReplyPacket:

    def __init__(self, dict):
        self.key: str = dict.get('key')
        self.value: any = dict.get('value')
        self.original_value: any = dict.get('original_value')

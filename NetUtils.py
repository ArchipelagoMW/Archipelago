from __future__ import annotations
import asyncio
import logging
import typing
import enum
from json import JSONEncoder, JSONDecoder

import websockets

from Utils import Version

class JSONMessagePart(typing.TypedDict, total=False):
    text: str
    # optional
    type: str
    color: str
    # mainly for items, optional
    found: bool



class CLientStatus(enum.IntEnum):
    CLIENT_UNKNOWN = 0
    CLIENT_CONNECTED = 5
    CLIENT_READY = 10
    CLIENT_PLAYING = 20
    CLIENT_GOAL = 30


class NetworkPlayer(typing.NamedTuple):
    team: int
    slot: int
    alias: str
    name: str


class NetworkItem(typing.NamedTuple):
    item: int
    location: int
    player: int


def _scan_for_TypedTuples(obj: typing.Any) -> typing.Any:
    if isinstance(obj, tuple) and hasattr(obj, "_fields"):  # NamedTuple is not actually a parent class
        data = obj._asdict()
        data["class"] = obj.__class__.__name__
        return data
    if isinstance(obj, (tuple, list)):
        return tuple(_scan_for_TypedTuples(o) for o in obj)
    if isinstance(obj, dict):
        return {key: _scan_for_TypedTuples(value) for key, value in obj.items()}
    return obj


_encode = JSONEncoder(
    ensure_ascii=False,
    check_circular=False,
).encode


def encode(obj):
    return _encode(_scan_for_TypedTuples(obj))

def get_any_version(data: dict) -> Version:
    data = {key.lower(): value for key, value in data.items()}  # .NET version classes have capitalized keys
    return Version(int(data["major"]), int(data["minor"]), int(data["build"]))

whitelist = {"NetworkPlayer": NetworkPlayer,
             "NetworkItem": NetworkItem,
             }

custom_hooks = {
    "Version": get_any_version
}

def _object_hook(o: typing.Any) -> typing.Any:
    if isinstance(o, dict):
        hook = custom_hooks.get(o.get("class", None), None)
        if hook:
            return hook(o)
        cls = whitelist.get(o.get("class", None), None)
        if cls:
            for key in tuple(o):
                if key not in cls._fields:
                    del(o[key])
            return cls(**o)

    return o


decode = JSONDecoder(object_hook=_object_hook).decode


class Node:
    endpoints: typing.List
    dumper = staticmethod(encode)
    loader = staticmethod(decode)

    def __init__(self):
        self.endpoints = []
        super(Node, self).__init__()

    def broadcast_all(self, msgs):
        msgs = self.dumper(msgs)
        for endpoint in self.endpoints:
            asyncio.create_task(self.send_encoded_msgs(endpoint, msgs))

    async def send_msgs(self, endpoint: Endpoint, msgs: typing.Iterable[dict]):
        if not endpoint.socket or not endpoint.socket.open or endpoint.socket.closed:
            return
        msg = self.dumper(msgs)
        try:
            await endpoint.socket.send(msg)
        except websockets.ConnectionClosed:
            logging.exception(f"Exception during send_msgs, could not send {msg}")
            await self.disconnect(endpoint)

    async def send_encoded_msgs(self, endpoint: Endpoint, msg: str):
        if not endpoint.socket or not endpoint.socket.open or endpoint.socket.closed:
            return
        try:
            await endpoint.socket.send(msg)
        except websockets.ConnectionClosed:
            logging.exception("Exception during send_msgs")
            await self.disconnect(endpoint)

    async def disconnect(self, endpoint):
        if endpoint in self.endpoints:
            self.endpoints.remove(endpoint)


class Endpoint:
    socket: websockets.WebSocketServerProtocol

    def __init__(self, socket):
        self.socket = socket

    async def disconnect(self):
        raise NotImplementedError


class HandlerMeta(type):
    def __new__(mcs, name, bases, attrs):
        handlers = attrs["handlers"] = {}
        trigger: str = "_handle_"
        for base in bases:
            handlers.update(base.commands)
        handlers.update({handler_name[len(trigger):]: method for handler_name, method in attrs.items() if
                         handler_name.startswith(trigger)})

        orig_init = attrs.get('__init__', None)

        def __init__(self, *args, **kwargs):
            # turn functions into bound methods
            self.handlers = {name: method.__get__(self, type(self)) for name, method in
                             handlers.items()}
            if orig_init:
                orig_init(self, *args, **kwargs)

        attrs['__init__'] = __init__
        return super(HandlerMeta, mcs).__new__(mcs, name, bases, attrs)

class JSONTypes(str, enum.Enum):
    color = "color"
    text = "text"
    player_id = "player_id"
    player_name = "player_name"
    item_name = "item_name"
    item_id = "item_id"
    location_name = "location_name"
    location_id = "location_id"
    entrance_name = "entrance_name"

class JSONtoTextParser(metaclass=HandlerMeta):
    def __init__(self, ctx):
        self.ctx = ctx

    def __call__(self, input_object: typing.List[JSONMessagePart]) -> str:
        return "".join(self.handle_node(section) for section in input_object)

    def handle_node(self, node: JSONMessagePart):
        type = node.get("type", None)
        handler = self.handlers.get(type, self.handlers["text"])
        return handler(node)

    def _handle_color(self, node: JSONMessagePart):
        codes = node["color"].split(";")
        buffer = "".join(color_code(code) for code in codes)
        return buffer + self._handle_text(node) + color_code("reset")

    def _handle_text(self, node: JSONMessagePart):
        return node.get("text", "")

    def _handle_player_id(self, node: JSONMessagePart):
        player = int(node["text"])
        node["color"] = 'magenta' if player == self.ctx.slot else 'yellow'
        node["text"] = self.ctx.player_names[player]
        return self._handle_color(node)

    # for other teams, spectators etc.? Only useful if player isn't in the clientside mapping
    def _handle_player_name(self, node: JSONMessagePart):
        node["color"] = 'yellow'
        return self._handle_color(node)

    def _handle_item_name(self, node: JSONMessagePart):
        # todo: use a better info source
        from worlds.alttp.Items import progression_items
        node["color"] = 'green' if node.get("found", False) else 'cyan'
        if node["text"] in progression_items:
            node["color"] += ";white_bg"
        return self._handle_color(node)

    def _handle_item_id(self, node: JSONMessagePart):
        item_id = int(node["text"])
        node["text"] = self.ctx.item_name_getter(item_id)
        return self._handle_item_name(node)

    def _handle_location_name(self, node: JSONMessagePart):
        node["color"] = 'blue_bg;white'
        return self._handle_color(node)

    def _handle_location_id(self, node: JSONMessagePart):
        item_id = int(node["text"])
        node["text"] = self.ctx.location_name_getter(item_id)
        return self._handle_item_name(node)

    def _handle_entrance_name(self, node: JSONMessagePart):
        node["color"] = 'white_bg;black'
        return self._handle_color(node)


color_codes = {'reset': 0, 'bold': 1, 'underline': 4, 'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
               'magenta': 35, 'cyan': 36, 'white': 37, 'black_bg': 40, 'red_bg': 41, 'green_bg': 42, 'yellow_bg': 43,
               'blue_bg': 44, 'purple_bg': 45, 'cyan_bg': 46, 'white_bg': 47}


def color_code(*args):
    return '\033[' + ';'.join([str(color_codes[arg]) for arg in args]) + 'm'


def color(text, *args):
    return color_code(*args) + text + color_code('reset')


def add_json_text(parts: list, text: typing.Any, **kwargs) -> None:
    parts.append({"text": str(text), **kwargs})


class Hint(typing.NamedTuple):
    receiving_player: int
    finding_player: int
    location: int
    item: int
    found: bool
    entrance: str = ""

    def re_check(self, ctx, team) -> Hint:
        if self.found:
            return self
        found = self.location in ctx.location_checks[team, self.finding_player]
        if found:
            return Hint(self.receiving_player, self.finding_player, self.location, self.item, found, self.entrance)
        return self

    def __hash__(self):
        return hash((self.receiving_player, self.finding_player, self.location, self.item, self.entrance))

    def as_network_message(self) -> dict:
        parts = []
        add_json_text(parts, "[Hint]: ")
        add_json_text(parts, self.receiving_player, type="player_id")
        add_json_text(parts, "'s ")
        add_json_text(parts, self.item, type="item_id", found=self.found)
        add_json_text(parts, " is at ")
        add_json_text(parts, self.location, type="location_id")
        add_json_text(parts, " in ")
        add_json_text(parts, self.finding_player, type ="player_id")
        if self.entrance:
            add_json_text(parts, "'s World at ")
            add_json_text(parts, self.entrance, type="entrance_name")
        else:
            add_json_text(parts, "'s World")
        if self.found:
            add_json_text(parts, ". (found)")
        else:
            add_json_text(parts, ".")

        return {"cmd": "PrintJSON", "data": parts, "type": "hint"}
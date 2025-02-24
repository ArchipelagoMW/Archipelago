from __future__ import annotations

import typing
import enum
import warnings
from json import JSONEncoder, JSONDecoder

import websockets

from Utils import ByValue, Version


class HintStatus(ByValue, enum.IntEnum):
    HINT_FOUND = 0
    HINT_UNSPECIFIED = 1
    HINT_NO_PRIORITY = 10
    HINT_AVOID = 20
    HINT_PRIORITY = 30


class JSONMessagePart(typing.TypedDict, total=False):
    text: str
    # optional
    type: str
    color: str
    # owning player for location/item
    player: int
    # if type == item indicates item flags
    flags: int
    # if type == hint_status
    hint_status: HintStatus


class ClientStatus(ByValue, enum.IntEnum):
    CLIENT_UNKNOWN = 0
    CLIENT_CONNECTED = 5
    CLIENT_READY = 10
    CLIENT_PLAYING = 20
    CLIENT_GOAL = 30


class SlotType(ByValue, enum.IntFlag):
    spectator = 0b00
    player = 0b01
    group = 0b10

    @property
    def always_goal(self) -> bool:
        """Mark this slot as having reached its goal instantly."""
        return self.value != 0b01


class Permission(ByValue, enum.IntFlag):
    disabled = 0b000  # 0, completely disables access
    enabled = 0b001  # 1, allows manual use
    goal = 0b010  # 2, allows manual use after goal completion
    auto = 0b110  # 6, forces use after goal completion, only works for release
    auto_enabled = 0b111  # 7, forces use after goal completion, allows manual use any time

    @staticmethod
    def from_text(text: str):
        data = 0
        if "auto" in text:
            data |= 0b110
        elif "goal" in text:
            data |= 0b010
        if "enabled" in text:
            data |= 0b001
        return Permission(data)


class NetworkPlayer(typing.NamedTuple):
    """Represents a particular player on a particular team."""
    team: int
    slot: int
    alias: str
    name: str


class NetworkSlot(typing.NamedTuple):
    """Represents a particular slot across teams."""
    name: str
    game: str
    type: SlotType
    group_members: typing.Union[typing.List[int], typing.Tuple] = ()  # only populated if type == group


class NetworkItem(typing.NamedTuple):
    item: int
    location: int
    player: int
    """ Sending player, except in LocationInfo (from LocationScouts), where it is the receiving player. """
    flags: int = 0


def _scan_for_TypedTuples(obj: typing.Any) -> typing.Any:
    if isinstance(obj, tuple) and hasattr(obj, "_fields"):  # NamedTuple is not actually a parent class
        data = obj._asdict()
        data["class"] = obj.__class__.__name__
        return data
    if isinstance(obj, (tuple, list, set, frozenset)):
        return tuple(_scan_for_TypedTuples(o) for o in obj)
    if isinstance(obj, dict):
        return {key: _scan_for_TypedTuples(value) for key, value in obj.items()}
    return obj


_encode = JSONEncoder(
    ensure_ascii=False,
    check_circular=False,
    separators=(',', ':'),
).encode


def encode(obj: typing.Any) -> str:
    return _encode(_scan_for_TypedTuples(obj))


def get_any_version(data: dict) -> Version:
    data = {key.lower(): value for key, value in data.items()}  # .NET version classes have capitalized keys
    return Version(int(data["major"]), int(data["minor"]), int(data["build"]))


allowlist = {
    "NetworkPlayer": NetworkPlayer,
    "NetworkItem": NetworkItem,
    "NetworkSlot": NetworkSlot
}

custom_hooks = {
    "Version": get_any_version
}


def _object_hook(o: typing.Any) -> typing.Any:
    if isinstance(o, dict):
        hook = custom_hooks.get(o.get("class", None), None)
        if hook:
            return hook(o)
        cls = allowlist.get(o.get("class", None), None)
        if cls:
            for key in tuple(o):
                if key not in cls._fields:
                    del (o[key])
            return cls(**o)

    return o


decode = JSONDecoder(object_hook=_object_hook).decode


class Endpoint:
    socket: websockets.WebSocketServerProtocol

    def __init__(self, socket):
        self.socket = socket


class HandlerMeta(type):
    def __new__(mcs, name, bases, attrs):
        handlers = attrs["handlers"] = {}
        trigger: str = "_handle_"
        for base in bases:
            handlers.update(base.handlers)
        handlers.update({handler_name[len(trigger):]: method for handler_name, method in attrs.items() if
                         handler_name.startswith(trigger)})

        orig_init = attrs.get('__init__', None)
        if not orig_init:
            for base in bases:
                orig_init = getattr(base, '__init__', None)
                if orig_init:
                    break

        def __init__(self, *args, **kwargs):
            if orig_init:
                orig_init(self, *args, **kwargs)
            # turn functions into bound methods
            self.handlers = {name: method.__get__(self, type(self)) for name, method in
                             handlers.items()}

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
    hint_status = "hint_status"


class JSONtoTextParser(metaclass=HandlerMeta):
    color_codes = {
        # not exact color names, close enough but decent looking
        "black": "000000",
        "red": "EE0000",
        "green": "00FF7F",
        "yellow": "FAFAD2",
        "blue": "6495ED",
        "magenta": "EE00EE",
        "cyan": "00EEEE",
        "slateblue": "6D8BE8",
        "plum": "AF99EF",
        "salmon": "FA8072",
        "white": "FFFFFF",
        "orange": "FF7700",
    }

    def __init__(self, ctx):
        self.ctx = ctx

    def __call__(self, input_object: typing.List[JSONMessagePart]) -> str:
        return "".join(self.handle_node(section) for section in input_object)

    def handle_node(self, node: JSONMessagePart):
        node_type = node.get("type", None)
        handler = self.handlers.get(node_type, self.handlers["text"])
        return handler(node)

    def _handle_color(self, node: JSONMessagePart):
        codes = node["color"].split(";")
        buffer = "".join(color_code(code) for code in codes if code in color_codes)
        return buffer + self._handle_text(node) + color_code("reset")

    def _handle_text(self, node: JSONMessagePart):
        return node.get("text", "")

    def _handle_player_id(self, node: JSONMessagePart):
        player = int(node["text"])
        node["color"] = 'magenta' if self.ctx.slot_concerns_self(player) else 'yellow'
        node["text"] = self.ctx.player_names[player]
        return self._handle_color(node)

    # for other teams, spectators etc.? Only useful if player isn't in the clientside mapping
    def _handle_player_name(self, node: JSONMessagePart):
        node["color"] = 'yellow'
        return self._handle_color(node)

    def _handle_item_name(self, node: JSONMessagePart):
        flags = node.get("flags", 0)
        if flags == 0:
            node["color"] = 'cyan'
        elif flags & 0b001:  # advancement
            node["color"] = 'plum'
        elif flags & 0b010:  # useful
            node["color"] = 'slateblue'
        elif flags & 0b100:  # trap
            node["color"] = 'salmon'
        else:
            node["color"] = 'cyan'
        return self._handle_color(node)

    def _handle_item_id(self, node: JSONMessagePart):
        item_id = int(node["text"])
        node["text"] = self.ctx.item_names.lookup_in_slot(item_id, node["player"])
        return self._handle_item_name(node)

    def _handle_location_name(self, node: JSONMessagePart):
        node["color"] = 'green'
        return self._handle_color(node)

    def _handle_location_id(self, node: JSONMessagePart):
        location_id = int(node["text"])
        node["text"] = self.ctx.location_names.lookup_in_slot(location_id, node["player"])
        return self._handle_location_name(node)

    def _handle_entrance_name(self, node: JSONMessagePart):
        node["color"] = 'blue'
        return self._handle_color(node)

    def _handle_hint_status(self, node: JSONMessagePart):
        node["color"] = status_colors.get(node["hint_status"], "red")
        return self._handle_color(node)


class RawJSONtoTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)


color_codes = {'reset': 0, 'bold': 1, 'underline': 4, 'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
               'magenta': 35, 'cyan': 36, 'white': 37, 'black_bg': 40, 'red_bg': 41, 'green_bg': 42, 'yellow_bg': 43,
               'blue_bg': 44, 'magenta_bg': 45, 'cyan_bg': 46, 'white_bg': 47,
               'plum': 35, 'slateblue': 34, 'salmon': 31,}  # convert ui colors to terminal colors


def color_code(*args):
    return '\033[' + ';'.join([str(color_codes[arg]) for arg in args]) + 'm'


def color(text, *args):
    return color_code(*args) + text + color_code('reset')


def add_json_text(parts: list, text: typing.Any, **kwargs) -> None:
    parts.append({"text": str(text), **kwargs})


def add_json_item(parts: list, item_id: int, player: int = 0, item_flags: int = 0, **kwargs) -> None:
    parts.append({"text": str(item_id), "player": player, "flags": item_flags, "type": JSONTypes.item_id, **kwargs})


def add_json_location(parts: list, location_id: int, player: int = 0, **kwargs) -> None:
    parts.append({"text": str(location_id), "player": player, "type": JSONTypes.location_id, **kwargs})


status_names: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: "(found)",
    HintStatus.HINT_UNSPECIFIED: "(unspecified)",
    HintStatus.HINT_NO_PRIORITY: "(no priority)",
    HintStatus.HINT_AVOID: "(avoid)",
    HintStatus.HINT_PRIORITY: "(priority)",
}
status_colors: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: "green",
    HintStatus.HINT_UNSPECIFIED: "white",
    HintStatus.HINT_NO_PRIORITY: "slateblue",
    HintStatus.HINT_AVOID: "salmon",
    HintStatus.HINT_PRIORITY: "plum",
}


def add_json_hint_status(parts: list, hint_status: HintStatus, text: typing.Optional[str] = None, **kwargs):
    parts.append({"text": text if text != None else status_names.get(hint_status, "(unknown)"),
                  "hint_status": hint_status, "type": JSONTypes.hint_status, **kwargs})


class Hint(typing.NamedTuple):
    receiving_player: int
    finding_player: int
    location: int
    item: int
    found: bool
    entrance: str = ""
    item_flags: int = 0
    status: HintStatus = HintStatus.HINT_UNSPECIFIED

    def re_check(self, ctx, team) -> Hint:
        if self.found and self.status == HintStatus.HINT_FOUND:
            return self
        found = self.location in ctx.location_checks[team, self.finding_player]
        if found:
            return self._replace(found=found, status=HintStatus.HINT_FOUND)
        return self
    
    def re_prioritize(self, ctx, status: HintStatus) -> Hint:
        if self.found and status != HintStatus.HINT_FOUND:
            status = HintStatus.HINT_FOUND
        if status != self.status:
            return self._replace(status=status)
        return self

    def __hash__(self):
        return hash((self.receiving_player, self.finding_player, self.location, self.item, self.entrance))

    def as_network_message(self) -> dict:
        parts = []
        add_json_text(parts, "[Hint]: ")
        add_json_text(parts, self.receiving_player, type="player_id")
        add_json_text(parts, "'s ")
        add_json_item(parts, self.item, self.receiving_player, self.item_flags)
        add_json_text(parts, " is at ")
        add_json_location(parts, self.location, self.finding_player)
        add_json_text(parts, " in ")
        add_json_text(parts, self.finding_player, type="player_id")
        if self.entrance:
            add_json_text(parts, "'s World at ")
            add_json_text(parts, self.entrance, type="entrance_name")
        else:
            add_json_text(parts, "'s World")
        add_json_text(parts, ". ")
        add_json_hint_status(parts, self.status)

        return {"cmd": "PrintJSON", "data": parts, "type": "Hint",
                "receiving": self.receiving_player,
                "item": NetworkItem(self.item, self.location, self.finding_player, self.item_flags),
                "found": self.found}

    @property
    def local(self):
        return self.receiving_player == self.finding_player


class _LocationStore(dict, typing.MutableMapping[int, typing.Dict[int, typing.Tuple[int, int, int]]]):
    def __init__(self, values: typing.MutableMapping[int, typing.Dict[int, typing.Tuple[int, int, int]]]):
        super().__init__(values)

        if not self:
            raise ValueError(f"Rejecting game with 0 players")

        if len(self) != max(self):
            raise ValueError("Player IDs not continuous")

        if len(self.get(0, {})):
            raise ValueError("Invalid player id 0 for location")

    def find_item(self, slots: typing.Set[int], seeked_item_id: int
                  ) -> typing.Generator[typing.Tuple[int, int, int, int, int], None, None]:
        for finding_player, check_data in self.items():
            for location_id, (item_id, receiving_player, item_flags) in check_data.items():
                if receiving_player in slots and item_id == seeked_item_id:
                    yield finding_player, location_id, item_id, receiving_player, item_flags

    def get_for_player(self, slot: int) -> typing.Dict[int, typing.Set[int]]:
        import collections
        all_locations: typing.Dict[int, typing.Set[int]] = collections.defaultdict(set)
        for source_slot, location_data in self.items():
            for location_id, values in location_data.items():
                if values[1] == slot:
                    all_locations[source_slot].add(location_id)
        return all_locations

    def get_checked(self, state: typing.Dict[typing.Tuple[int, int], typing.Set[int]], team: int, slot: int
                    ) -> typing.List[int]:
        checked = state[team, slot]
        if not checked:
            # This optimizes the case where everyone connects to a fresh game at the same time.
            if slot not in self:
                raise KeyError(slot)
            return []
        return [location_id for
                location_id in self[slot] if
                location_id in checked]

    def get_missing(self, state: typing.Dict[typing.Tuple[int, int], typing.Set[int]], team: int, slot: int
                    ) -> typing.List[int]:
        checked = state[team, slot]
        if not checked:
            # This optimizes the case where everyone connects to a fresh game at the same time.
            return list(self[slot])
        return [location_id for
                location_id in self[slot] if
                location_id not in checked]

    def get_remaining(self, state: typing.Dict[typing.Tuple[int, int], typing.Set[int]], team: int, slot: int
                      ) -> typing.List[typing.Tuple[int, int]]:
        checked = state[team, slot]
        player_locations = self[slot]
        return sorted([(player_locations[location_id][1], player_locations[location_id][0]) for
                        location_id in player_locations if
                        location_id not in checked])


if typing.TYPE_CHECKING:  # type-check with pure python implementation until we have a typing stub
    LocationStore = _LocationStore
else:
    try:
        from _speedups import LocationStore
        import _speedups
        import os.path
        if os.path.isfile("_speedups.pyx") and os.path.getctime(_speedups.__file__) < os.path.getctime("_speedups.pyx"):
            warnings.warn(f"{_speedups.__file__} outdated! "
                          f"Please rebuild with `cythonize -b -i _speedups.pyx` or delete it!")
    except ImportError:
        try:
            import pyximport
            pyximport.install()
        except ImportError:
            pyximport = None
        try:
            from _speedups import LocationStore
        except ImportError:
            warnings.warn("_speedups not available. Falling back to pure python LocationStore. "
                          "Install a matching C++ compiler for your platform to compile _speedups.")
            LocationStore = _LocationStore

from __future__ import annotations

import enum
import shlex
import typing
import warnings
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import inspect
from colorsys import hls_to_rgb, rgb_to_hls
from itertools import chain, repeat
from json import JSONEncoder, JSONDecoder

if typing.TYPE_CHECKING:
    from websockets import WebSocketServerProtocol as ServerConnection
    from CommonClient import CommonContext

from Utils import ByValue, Version


class HintStatus(ByValue, enum.IntEnum):
    HINT_UNSPECIFIED = 0
    HINT_NO_PRIORITY = 10
    HINT_AVOID = 20
    HINT_PRIORITY = 30
    HINT_FOUND = 40


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
    group_members: Sequence[int] = ()  # only populated if type == group


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


_base_types = str | int | bool | float | None | tuple["_base_types", ...] | dict["_base_types", "base_types"]


def convert_to_base_types(obj: typing.Any) -> _base_types:
    if isinstance(obj, (tuple, list, set, frozenset)):
        return tuple(convert_to_base_types(o) for o in obj)
    elif isinstance(obj, dict):
        return {convert_to_base_types(key): convert_to_base_types(value) for key, value in obj.items()}
    elif obj is None or type(obj) in (str, int, float, bool):
        return obj
    # unwrap simple types to their base, such as StrEnum
    elif isinstance(obj, str):
        return str(obj)
    elif isinstance(obj, int):
        return int(obj)
    elif isinstance(obj, float):
        return float(obj)
    else:
        raise Exception(f"Cannot handle {type(obj)}")


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


_decode = JSONDecoder(object_hook=_object_hook).decode


try:
    from _speedups import check_json_depth as _check_depth
except ImportError:
    def _check_depth(s: str, limit: int = 16) -> None:
        depth = 1
        in_quotes = False
        escape = False
        for c in s:
            if c == "\\" and not escape:
                escape = True
                continue
            if c == '"' and not escape:
                in_quotes = not in_quotes
                continue
            if not in_quotes:
                if c in "[{":
                    depth += 1
                    if depth > limit:
                        raise ValueError("JSON document too complex")
                elif c in "}]":
                    depth -= 1
            escape = False

        if depth != 1:  # free check
            raise ValueError("JSON document malformed")


def decode(s: str) -> typing.Any:
    _check_depth(s)  # raises ValueError
    return _decode(s)


class Endpoint:
    __slots__ = ("socket",)

    socket: "ServerConnection"

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


color_rgb = {
    # not exact color names, close enough but decent looking
    "black": "000000",
    "red": "EE0000",
    "green": "00FF7F",
    "yellow": "FAFA40",
    "blue": "6495ED",
    "magenta": "EE00EE",
    "cyan": "00EEEE",
    "slateblue": "6D8BE8",
    "plum": "AF99EF",
    "salmon": "FA8072",
    "white": "FFFFFF",
    "orange": "FF7700",
}

class JSONtoTextParser(metaclass=HandlerMeta):
    color_codes = color_rgb

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
        for i, code in enumerate(codes):
            if code.endswith("_dark"):
                codes[i] = "gray"

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


def get_dark_color(color: str, color_codes: dict[str, str]) -> str | None:
    color_code = color_codes.get(color)
    if color_code:
        r, g, b = [int(part, 16) / 255 for part in (color_code[:2], color_code[2:4], color_code[4:])]
        h, l, s = rgb_to_hls(r, g, b)
        color_code = "".join(f"{int(255 * part):02X}" for part in hls_to_rgb(h, l / 1.8, s / 2.5))

    return color_code


class RawJSONtoTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)


color_codes: dict[str, str] = {
    "reset": "0", "bold": "1", "underline": "4", "black": "30", "red": "31", "green": "32", "yellow": "33",
    "blue": "34", "magenta": "35", "cyan": "36", "white": "37", "black_bg": "40", "red_bg": "41", "green_bg": "42",
    "yellow_bg": "43", "blue_bg": "44", "magenta_bg": "45", "cyan_bg": "46", "white_bg": "47",
    # convert ui colors to terminal colors
    "plum": "38;5;147", "slateblue": "38;5;68", "orange": "38;5;208", "salmon": "38;5;210",
    "gray": "38;5;241",  # for grayed out text
}


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


def add_json_color(parts: list, text: typing.Any, color: str | None, **kwargs) -> None:
    if color:
        parts.append({"text": str(text), "type": "color", "color": color, **kwargs})
    else:
        add_json_text(parts, text, **kwargs)


class CommandType(enum.IntEnum):
    server_console = 0
    client_connected = 1
    client_always = 2


@dataclass(frozen=True)
class CommandData:
    command: str
    arg_types: Sequence[str | None]  # Specifies type for colors, or special value of "$int" for an integer
    raw: bool
    command_type: CommandType
    vararg_type: str | None = "error"  # Type for after all arg_types are exhausted
    starting_server_version: Version = Version(0, 6, 0)
    required_tags: frozenset[str] = frozenset({"AP"})

COMMAND_FORMS: tuple[CommandData, ...] = (
    CommandData("!help", (), False, CommandType.client_connected),
    CommandData("!license", (), False, CommandType.client_connected),
    CommandData("!options", (), False, CommandType.client_connected),
    CommandData("!admin", (), True, CommandType.client_connected),  # Special cased for forms and for following command
    CommandData("!players", (), False, CommandType.client_connected),
    CommandData("!status", (None,), False, CommandType.client_connected),
    CommandData("!release", (), False, CommandType.client_connected),
    CommandData("!collect", (), False, CommandType.client_connected),
    CommandData("!countdown", ("$int",), False, CommandType.client_connected),
    CommandData("!remaining", (), False, CommandType.client_connected),
    CommandData("!missing", (None,), True, CommandType.client_connected),
    CommandData("!checked", (None,), True, CommandType.client_connected),
    CommandData("!alias", (None,), True, CommandType.client_connected),
    CommandData("!getitem", ("item",), True, CommandType.client_connected),
    CommandData("!hint", ("item",), True, CommandType.client_connected),
    CommandData("!hint_location", ("location",), True, CommandType.client_connected),

    CommandData("/help", (), False, CommandType.server_console),
    CommandData("/license", (), False, CommandType.server_console),
    CommandData("/options", (), False, CommandType.server_console),
    CommandData("/save", (), False, CommandType.server_console),
    CommandData("/players", (), False, CommandType.server_console),
    CommandData("/status", (None,), False, CommandType.server_console),
    CommandData("/exit", (), False, CommandType.server_console),
    CommandData("/alias", (), True, CommandType.server_console),  # Special cased for taking a single arg then splitting
    CommandData("/collect", ("player",), True, CommandType.server_console),
    CommandData("/countdown", ("$int",), False, CommandType.server_console),
    CommandData("/release", ("player",), True, CommandType.server_console),
    CommandData("/allow_release", ("player",), True, CommandType.server_console),
    CommandData("/forbid_release", ("player",), True, CommandType.server_console),
    CommandData("/send_multiple", ("$int", "player"), False, CommandType.server_console, vararg_type="item"),
    CommandData("/send", ("player",), False, CommandType.server_console, vararg_type="item"),
    CommandData("/send_location", ("player",), False, CommandType.server_console, vararg_type="location"),
    CommandData("/send_multiple", ("$int", "player"), True, CommandType.server_console, vararg_type="item"),
    CommandData("/hint", ("player",), False, CommandType.server_console, vararg_type="item"),
    CommandData("/hint_location", ("player",), False, CommandType.server_console, vararg_type="location"),
    # Has special handling of available options
    CommandData("/option", ("command", None), False, CommandType.server_console),
    CommandData("/datastore", (), False, CommandType.server_console),

    CommandData("/help", (), False, CommandType.client_always),
    CommandData("/license", (), False, CommandType.client_always),
    CommandData("/exit", (), False, CommandType.client_always),
    CommandData("/connect", (None,), False, CommandType.client_always),
    CommandData("/disconnect", (), False, CommandType.client_always),
    CommandData("/received", (), False, CommandType.client_always),
    CommandData("/missing", (None,), False, CommandType.client_always),
    CommandData("/items", (), False, CommandType.client_always),
    CommandData("/locations", (), False, CommandType.client_always),
    CommandData("/item_groups", ("item",), True, CommandType.client_always),
    CommandData("/location_groups", ("location",), True, CommandType.client_always),
    CommandData("/ready", (), False, CommandType.client_always),

    # Customserver-specific command
    CommandData("!video", (None, None), False, CommandType.client_connected, required_tags=frozenset({"WebHost"})),
)
"""
List of recognized commands and metadata for highlighting.
Commands with mutliple version variants should be stored from newest to oldest.
"""


@dataclass(frozen=True)
class OptionData:
    option: str
    val_type: str | None | tuple[str, ...]  # Either a single value like arg_type or a tuple listing possible values
    starting_server_version: Version = Version(0, 6, 0)

SERVER_OPTIONS = (
    OptionData("hint_cost", "$int"),
    OptionData("location_check_points", "$int"),
    OptionData("server_password", None),
    OptionData("password", None),
    OptionData("release_mode", ("disabled", "enabled", "auto", "auto_enabled", "goal")),
    OptionData("remaining_mode", ("disabled", "enabled", "goal")),
    OptionData("collect_mode", ("disabled", "enabled", "auto", "auto_enabled", "goal")),
    # countdown_mode first added in https://github.com/ArchipelagoMW/Archipelago/pull/5465
    OptionData("countdown_mode", ("disabled", "enabled", "auto"), starting_server_version=Version(0, 6, 4)),
    OptionData("item_cheat", None),
    OptionData("compatibility", "$int"),
)


def _extract_matching_runs(text: str, args: list[str]) -> list[list[str]]:
    # Annoyingly, shlex does not seem to provide a way to give information about the removed whitespace or escape chars,
    # so run a comparison to the original text to extract them
    subpart_list = [[] for _ in range(len(args))]
    plain_index = 0
    split_index = 0
    tok_start = 0  # text[tok_start:plain_index] represents the current token being matched
    cur_arg = 0
    while plain_index < len(text):
        if split_index >= len(args[cur_arg]):
            # Hit end of arg, push token. Empty args can give a whitespace only token here
            subpart_list[cur_arg].append((text[tok_start:plain_index], args[cur_arg] != ""))

            # Check for any non-matching chars up until next whitespace
            tok_start = plain_index
            while not text[plain_index] in " \t\r\n":  # Default shlex whitespace
                plain_index += 1
                if plain_index == len(text):
                    break
            if plain_index > tok_start:
                subpart_list[cur_arg].append((text[tok_start:plain_index], False))

            tok_start = plain_index
            cur_arg += 1
            split_index = 0
            # Now done after processing
            if plain_index == len(text) or cur_arg == len(args):
                break

        if split_index >= len(args[cur_arg]) or text[plain_index] != args[cur_arg][split_index]:
            # Hit a non-matching part that should be grayed out, push current token and parse rest of non-matching part
            if plain_index > tok_start:
                subpart_list[cur_arg].append((text[tok_start:plain_index], True))

            tok_start = plain_index
            while split_index < len(args[cur_arg]) and text[plain_index] != args[cur_arg][split_index]:
                plain_index += 1
            if plain_index > tok_start:
                subpart_list[cur_arg].append((text[tok_start:plain_index], False))
            tok_start = plain_index

        split_index += 1
        plain_index += 1
    # Check for if there's a final token to be pushed
    if plain_index > tok_start:
        subpart_list[-1].append((text[tok_start:plain_index], True))

    return subpart_list


_basic_arg_colors = {
    "item": "cyan", "location": "green", "player": "yellow",
    "command": "orange", "unrecognized": "red", "error": "underline;red"
}

def get_arg_type_color(arg_type: str | None, arg_val: str = "") -> str | None:
    if arg_type == "$int":
        try:
            int(arg_val)
            return None
        except ValueError:
            return get_arg_type_color("error")

    if arg_type:
        return _basic_arg_colors.get(arg_type)


def colorize_input(text: str, ctx: CommonContext | None = None,
                   server_version: Version | None = None) -> list[JSONMessagePart]:
    if not server_version and ctx:
        server_version = ctx.server_version

    try:
        args = shlex.split(text)
    except ValueError:
        args = text.split()

    if not args:
        return []

    parts = []
    if ctx and ctx.input_requests > 0:
        add_json_text(parts, text)
        return parts

    def command_form_matches(form: CommandData):
        if form.command != args[0]:
            return False
        # Check if command type is usable here
        if ctx:
            if form.command_type == CommandType.server_console:
                return False
            if form.command_type == CommandType.client_connected:
                if not ctx.server_tags:
                    return False
                assert server_version
                # Check server compatibility
                if form.starting_server_version > server_version:
                    return False
                if not form.required_tags.issubset(ctx.server_tags):
                    return False

        else:
            if form.command_type != CommandType.server_console:
                return False

        return True

    data = next((form for form in COMMAND_FORMS if command_form_matches(form)), None)

    # Try searching CommandProcessor for additional defined commands there
    if not data and ctx:
        for name, func in ctx.command_processor.commands.items():
            command = ctx.command_processor.marker + name
            raw = getattr(func, "raw_text", False)
            if command == args[0]:
                try:
                    sig = inspect.signature(func)

                    pos_types = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                    pos_args = len([param for param in sig.parameters.values() if param.kind in pos_types]) - 1
                    vararg = any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in sig.parameters.values())

                    data = CommandData(
                        command, (None,) * pos_args, raw, CommandType.client_always,
                        vararg_type="error" if not vararg else None
                    )
                except ValueError:
                    data = CommandData(command, (), raw, CommandType.client_always, vararg_type=None)

    if not data:
        add_json_text(parts, text)
        return parts

    if data.raw:
        first_split = text.split(maxsplit=1)
        if len(first_split) > 1:
            add_json_color(parts, text[:-len(first_split[1])], get_arg_type_color("command"))

            if ctx and args[0] == "!admin":
                if first_split[1].strip().startswith("login "):
                    add_json_color(parts, "login ", get_arg_type_color("command"))
                    add_json_text(parts, first_split[1][6:])
                elif first_split[1] == "logout":
                    add_json_color(parts, "logout", get_arg_type_color("command"))
                else:
                    # Strip context so it's treated as from server, but use the server's reported version
                    parts.extend(colorize_input(first_split[1], server_version=server_version))
            elif args[0] == "/alias":
                player_name, sp, alias = first_split[1].partition(" ")
                add_json_color(parts, player_name, get_arg_type_color("player"))
                add_json_text(parts, sp + alias)
            else:
                arg_type = data.arg_types[0] if data.arg_types else data.vararg_type
                arg_color = get_arg_type_color(arg_type, first_split[1])
                add_json_color(parts, first_split[1], arg_color)
        else:
            add_json_color(parts, text, get_arg_type_color("command"))
        return parts

    subpart_list = _extract_matching_runs(text, args)

    arg_types = ["command"] + list(data.arg_types)
    if not ctx and args[0] == "/option" and len(args) > 1:
        matching_option = next((data for data in SERVER_OPTIONS if data.option == args[1]
                                and (not server_version or data.starting_server_version <= server_version)), None)
        if matching_option:
            if len(args) > 2:
                if isinstance(matching_option.val_type, tuple):
                    arg_types[2] = "unrecognized" if args[2] not in matching_option.val_type else None
                else:
                    arg_types[2] = matching_option.val_type
        else:
            arg_types[1] = "unrecognized"

    for subparts, arg_type in zip(subpart_list, chain(arg_types, repeat(data.vararg_type))):
        arg_color = get_arg_type_color(arg_type, "".join(subpart for subpart, _ in subparts))

        for (subpart, highlight) in subparts:
            add_json_color(parts, subpart, arg_color if highlight else f"{arg_color}_dark")

    return parts


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


class MinimumVersions(typing.TypedDict):
    server: tuple[int, int, int]
    clients: dict[int, tuple[int, int, int]]


class GamesPackage(typing.TypedDict, total=False):
    item_name_groups: dict[str, list[str]]
    item_name_to_id: dict[str, int]
    location_name_groups: dict[str, list[str]]
    location_name_to_id: dict[str, int]
    checksum: str


class DataPackage(typing.TypedDict):
    games: dict[str, GamesPackage]


class MultiData(typing.TypedDict):
    slot_data: dict[int, Mapping[str, typing.Any]]
    slot_info: dict[int, NetworkSlot]
    connect_names: dict[str, tuple[int, int]]
    locations: dict[int, dict[int, tuple[int, int, int]]]
    checks_in_area: dict[int, dict[str, int | list[int]]]
    server_options: dict[str, object]
    er_hint_data: dict[int, dict[int, str]]
    precollected_items: dict[int, list[int]]
    precollected_hints: dict[int, set[Hint]]
    version: tuple[int, int, int]
    tags: list[str]
    minimum_versions: MinimumVersions
    seed_name: str
    spheres: list[dict[int, set[int]]]
    datapackage: dict[str, GamesPackage]
    race_mode: int


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
            import logging
            logger = logging.getLogger()
            old_level = logger.level
            from _speedups import LocationStore
            logger.setLevel(old_level)
        except ImportError:
            warnings.warn("_speedups not available. Falling back to pure python LocationStore. "
                          "Install a matching C++ compiler for your platform to compile _speedups.")
            LocationStore = _LocationStore

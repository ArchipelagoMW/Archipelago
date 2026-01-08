r"""JSON with Comments for Python

    >>> import jsonc
    >>> jsonc.loads("{// comment \n}")
    {}
    >>> jsonc.loads("{/* comment */}")
    {}
    >>> jsonc.loads('{"spam": "ham // egg" /* comment */}')
    {'spam': 'ham // egg'}
    >>> jsonc.loads('{"spam": /* comment */"ham /* egg */"}')
    {'spam': 'ham /* egg */'}
"""

from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from io import StringIO
from tokenize import COMMENT, NL, STRING, TokenInfo, generate_tokens, untokenize
from typing import TYPE_CHECKING, Any, TextIO
from warnings import warn

__version__ = "1.2.2"
import json
import re
from json import JSONDecoder, JSONEncoder  # for compatibility

if TYPE_CHECKING:
    CommentsDict = dict[str, "Comments"] | dict[int, "Comments"]
    Comments = str | CommentsDict | tuple[str, CommentsDict]


_REMOVE_C_COMMENT = r"""
    ( # String Literal
        \"(?:\\.|[^\\\"])*?\"
    )
    |
    ( # Comment
        \/\*.*?\*\/
        |
        \/\/[^\r\n]*?(?:[\r\n])
    )
    """


_REMOVE_TRAILING_COMMA = r"""
    ( # String Literal
        \"(?:\\.|[^\\\"])*?\"
    )
    | # Right Brace without Trailing Comma & Spaces
    ,\s*([\]}])
"""


_ADD_TRAILING_COMMA = r"""
    ( # String Literal
        \"(?:\\.|[^\\\"])*?\"
    )
    | # Don't match opening braces to avoid {,}
    ((?<=\")|[^,\[{\s])
    (?=\s*([\]}]))
"""


def _remove_c_comment(text: str) -> str:
    if text[-1] != "\n":
        text = text + "\n"
    return re.sub(
        _REMOVE_C_COMMENT, lambda x: x.group(1), text, flags=re.DOTALL | re.VERBOSE
    )


def _remove_trailing_comma(text: str) -> str:
    return re.sub(
        _REMOVE_TRAILING_COMMA,
        lambda x: x.group(1) or x.group(2),
        text,
        flags=re.DOTALL | re.VERBOSE,
    )


def _add_trailing_comma(text: str) -> str:
    return re.sub(
        _ADD_TRAILING_COMMA,
        lambda x: x.group(1) or x.group(2) + ",",
        text,
        flags=re.DOTALL | re.VERBOSE,
    )


def _make_comment(text: str, indent=0) -> str:
    return "\n".join(
        " " * indent + "// " + line if line else "" for line in text.splitlines()
    )


def _get_comments(
    comments: CommentsDict | None, key: str | int
) -> tuple[str | None, CommentsDict | None]:
    if comments is not None:
        comments = comments.pop(key, None)
        if isinstance(comments, tuple):
            comm, comments = comments
        elif isinstance(comments, str):
            comm = comments
            comments = None
        else:
            comm = None
        return comm, comments
    return None, None


def _warn_unused(
    comments: CommentsDict | None,
    stack: list[tuple[CommentsDict | None, int | None, str | int]],
):
    if not comments:
        return
    full_key = ".".join(str(key) for _, _, key in stack[1:])
    if full_key:
        full_key += "."
    for k in comments:
        warn("Unused comment with key: " + full_key + str(k))


def load(
    fp: TextIO,
    *,
    cls: type[json.JSONDecoder] | None = None,
    object_hook: Callable[[dict[Any, Any]], Any] | None = None,
    parse_float: Callable[[str], Any] | None = None,
    parse_int: Callable[[str], Any] | None = None,
    parse_constant: Callable[[str], Any] | None = None,
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None,
    **kw: dict[str, Any],
) -> Any:
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document) to a Python object.

    Reference: ``json.load``
    """
    return json.loads(
        _remove_trailing_comma(_remove_c_comment(fp.read())),
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
        **kw,
    )


def loads(
    s: str,
    *,
    cls: type[json.JSONDecoder] | None = None,
    object_hook: Callable[[dict[Any, Any]], Any] | None = None,
    parse_float: Callable[[str], Any] | None = None,
    parse_int: Callable[[str], Any] | None = None,
    parse_constant: Callable[[str], Any] | None = None,
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None,
    **kw: dict[str, Any],
) -> Any:
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.

    Reference: ``json.loads``
    """
    return json.loads(
        _remove_trailing_comma(_remove_c_comment(s)),
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
        **kw,
    )


def add_comments(data: str, comments: Comments) -> str:
    header, comments = _get_comments({0: deepcopy(comments)}, 0)
    if header:
        header = _make_comment(header) + "\n"
    else:
        header = ""
    result = []
    stack = []
    line_shift = 0
    array_index: int | None = None
    key: str | int | None = None
    for token in generate_tokens(StringIO(data).readline):
        if (
            token.type == STRING or (array_index is not None and token.string != "]")
        ) and result[-1].type == NL:
            key = array_index if array_index is not None else json.loads(token.string)
            stack.append((comments, array_index, key))
            comm, comments = _get_comments(comments, key)
            if comm:
                comm = _make_comment(comm, token.start[1])
                comm_coord = (token.start[0] + line_shift, 0)
                result.append(
                    TokenInfo(
                        COMMENT,
                        comm,
                        comm_coord,
                        comm_coord,
                        "",
                    )
                )
                result.append(
                    TokenInfo(
                        NL,
                        "\n",
                        comm_coord,
                        comm_coord,
                        "",
                    )
                )
                line_shift += 1

        if token.string == ",":
            _warn_unused(comments, stack)
            comments, array_index, key = stack.pop()
            if array_index is not None:
                array_index += 1
        elif token.string == "[":
            stack.append((comments, array_index, key))
            array_index = 0
        elif token.string == "{":
            stack.append((comments, array_index, key))
            array_index = None
        elif token.string in {"]", "}"}:
            _warn_unused(comments, stack)
            comments, array_index, key = stack.pop()
            if result[-1].type == NL and result[-2].string != ",":
                _warn_unused(comments, stack)
                comments, array_index, key = stack.pop()

        token = TokenInfo(
            token.type,
            token.string,
            (token.start[0] + line_shift, token.start[1]),
            (token.end[0] + line_shift, token.end[1]),
            token.line,
        )
        result.append(token)

    assert not stack, "Error when adding comments to JSON"
    return header + untokenize(result)


def dumps(
    obj: Any,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls: type[JSONEncoder] | None = None,
    indent: int | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], Any] | None = None,
    sort_keys=False,
    trailing_comma=False,
    comments: Comments | None = None,
    **kw,
) -> str:
    """Serialize ``obj`` to a JSON formatted ``str``.

    Reference: ``json.dumps``
    """

    data = json.dumps(
        obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kw,
    )

    if trailing_comma:
        data = _add_trailing_comma(data)

    if comments is None:
        return data
    if indent is None:
        warn("Can't add comments to non-indented JSON")
        return data

    return add_comments(data, comments)


def dump(
    obj: Any,
    fp: TextIO,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls: type[JSONEncoder] | None = None,
    indent: int | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], Any] | None = None,
    sort_keys=False,
    trailing_comma=False,
    comments: Comments | None = None,
    **kw,
):
    """Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    Reference: ``json.dump``
    """

    fp.write(
        dumps(
            obj,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            trailing_comma=trailing_comma,
            comments=comments,
            **kw,
        )
    )

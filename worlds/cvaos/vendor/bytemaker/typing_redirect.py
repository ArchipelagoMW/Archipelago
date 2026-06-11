"""
typing_redirect.py

This module allows for Python version-agnostic typing and collections.abc imports.
    It uses Python standard library batteries where possible.
    For older versions, this module will export from typing_extensions.
"""

import sys
from importlib.util import find_spec
from typing import Any

if sys.version_info < (3, 9):
    from typing import (
        Callable,
        Iterable,
        Mapping,
        MutableMapping,
        MutableSequence,
        Sequence,
    )
else:
    from collections.abc import (
        Callable,
        Iterable,
        Mapping,
        MutableMapping,
        MutableSequence,
        Sequence,
    )

if sys.version_info < (3, 10):
    UnionType = Any
    if find_spec("typing_extensions"):
        from typing_extensions import Concatenate, ParamSpec
    else:
        ParamSpec = Any
        Concatenate = Any
else:
    from types import UnionType
    from typing import ParamSpec
    from typing import Concatenate

from collections.abc import Hashable
from typing import (
    ClassVar,
    Dict,
    Final,
    ForwardRef,
    Generic,
    ItemsView,
    Iterator,
    List,
    Literal,
    Optional,
    Protocol,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    overload,
    runtime_checkable,
)

if sys.version_info < (3, 12):
    if find_spec("typing_extensions"):
        from typing_extensions import Buffer
    else:
        Buffer = TypeVar("Buffer")  # Fall back to TypeVar
else:
    from collections.abc import Buffer

if sys.version_info < (3, 13):
    if find_spec("typing_extensions"):
        from typing_extensions import TypeIs  # type: ignore[reportAssignmentType]
    else:
        T = TypeVar("T")

        class TypeIs(Generic[T]):
            def __class_getitem__(cls, item):
                return cls

else:
    from typing import TypeIs


__all__ = [
    "Any",
    "Buffer",
    "Callable",
    "ClassVar",
    "Concatenate",
    "Dict",
    "Final",
    "ForwardRef",
    "Hashable",
    "ItemsView",
    "Iterable",
    "Iterator",
    "List",
    "Literal",
    "Mapping",
    "MutableMapping",
    "MutableSequence",
    "Optional",
    "ParamSpec",
    "Protocol",
    "Set",
    "Sequence",
    "Tuple",
    "Type",
    "TypeIs",
    "TypeVar",
    "Union",
    "UnionType",
    "get_args",
    "get_origin",
    "get_type_hints",
    "overload",
    "runtime_checkable",
]

if sys.version_info >= (3, 11):
    from typing import Self  # noqa: F401

    __all__.append("Self")

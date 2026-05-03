from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Literal, TypeAlias, TypeVar

T = TypeVar("T")
E = TypeVar("E")


@dataclass(slots=True)
class Ok(Generic[T]):
    """Represents a successful result payload."""

    value: T
    ok: Literal[True] = True


@dataclass(slots=True)
class Err(Generic[E]):
    """Represents a failed result payload."""

    error: E
    ok: Literal[False] = False


Result: TypeAlias = Ok[T] | Err[E]

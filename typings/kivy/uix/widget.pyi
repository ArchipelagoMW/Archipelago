""" FillType_* is not a real kivy type - just something to fill unknown typing. """

from typing import Any, Optional, Protocol
from ..graphics.texture import FillType_Drawable, FillType_Vec


class FillType_BindCallback(Protocol):
    def __call__(self, *args: Any) -> None: ...


class FillType_Canvas:
    def add(self, drawable: FillType_Drawable) -> None: ...

    def clear(self) -> None: ...

    def __enter__(self) -> None: ...

    def __exit__(self, *args: Any) -> None: ...


class Widget:
    canvas: FillType_Canvas
    width: int
    pos: FillType_Vec

    def bind(self,
             *,
             pos: Optional[FillType_BindCallback] = ...,
             size: Optional[FillType_BindCallback] = ...) -> None: ...

    def refresh(self) -> None: ...

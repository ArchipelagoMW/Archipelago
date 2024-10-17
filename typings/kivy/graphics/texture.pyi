""" FillType_* is not a real kivy type - just something to fill unknown typing. """

from typing import Sequence

FillType_Vec = Sequence[int]


class FillType_Drawable:
    def __init__(self, *, pos: FillType_Vec = ..., size: FillType_Vec = ...) -> None: ...


class Texture:
    size: FillType_Vec

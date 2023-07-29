""" FillType_* is not a real kivy type - just something to fill unknown typing. """

from typing import Sequence

FillType_Vec = Sequence[int]


class FillType_Drawable:
    def __init__(self, *, pos: FillType_Vec = ..., size: FillType_Vec = ...) -> None: ...


class FillType_Texture(FillType_Drawable):
    pass


class FillType_Shape(FillType_Drawable):
    texture: FillType_Texture

    def __init__(self,
                 *,
                 texture: FillType_Texture = ...,
                 pos: FillType_Vec = ...,
                 size: FillType_Vec = ...) -> None: ...


class Ellipse(FillType_Shape):
    pass


class Color:
    def __init__(self, r: float, g: float, b: float, a: float) -> None: ...


class Rectangle(FillType_Shape):
    def __init__(self,
                 *,
                 source: str = ...,
                 texture: FillType_Texture = ...,
                 pos: FillType_Vec = ...,
                 size: FillType_Vec = ...) -> None: ...

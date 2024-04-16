from .texture import FillType_Drawable, FillType_Vec, Texture


class FillType_Shape(FillType_Drawable):
    texture: Texture

    def __init__(self,
                 *,
                 texture: Texture = ...,
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
                 texture: Texture = ...,
                 pos: FillType_Vec = ...,
                 size: FillType_Vec = ...) -> None: ...

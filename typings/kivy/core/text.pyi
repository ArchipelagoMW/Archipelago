from typing import Tuple
from ..graphics import FillType_Shape
from ..uix.widget import Widget


class Label(FillType_Shape, Widget):
    def __init__(self, *, text: str, font_size: int, color: Tuple[float, float, float, float]) -> None: ...

from typing import Literal
from .layout import Layout


class BoxLayout(Layout):
    orientation: Literal['horizontal', 'vertical']

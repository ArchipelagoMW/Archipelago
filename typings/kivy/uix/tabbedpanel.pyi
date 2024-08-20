from .layout import Layout
from .widget import Widget


class TabbedPanel(Layout):
    pass


class TabbedPanelItem(Widget):
    content: Widget

    def __init__(self, *, text: str = ...) -> None: ...

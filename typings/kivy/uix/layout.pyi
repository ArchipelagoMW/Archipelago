from typing import Any
from .widget import Widget


class Layout(Widget):
    def add_widget(self, widget: Widget) -> None: ...

    def do_layout(self, *largs: Any, **kwargs: Any) -> None: ...

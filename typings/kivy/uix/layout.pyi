from typing import Any, Sequence

from .widget import Widget


class Layout(Widget):
    @property
    def children(self) -> Sequence[Widget]: ...

    def add_widget(self, widget: Widget) -> None: ...

    def remove_widget(self, widget: Widget) -> None: ...

    def do_layout(self, *largs: Any, **kwargs: Any) -> None: ...

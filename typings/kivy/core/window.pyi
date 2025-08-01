from typing import Callable, ClassVar

from kivy.event import EventDispatcher


class WindowBase(EventDispatcher):
    width: ClassVar[int]  # readonly AliasProperty
    height: ClassVar[int]  # readonly AliasProperty

    @staticmethod
    def bind(**kwargs: Callable[..., None]) -> None: ...


class Window(WindowBase):
    ...

from typing import Callable


class DOMNode:
    def bind(self, event: str, callback: Callable[["DOMEvent"], None]) -> None: ...
    def __getitem__(self, id_: str) -> "DOMNode": ...
    def click(self) -> None: ...
    def submit(self) -> None: ...


class DOMEvent:
    pass  # actual definition depends on specific event because things are just passed down to js


document: DOMNode
window: DOMNode  # this is not actually true, but there is no proper type for this (yet)

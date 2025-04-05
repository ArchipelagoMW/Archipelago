from typing import Any, Callable


class And:
    def __init__(self, __type: type, __func: Callable[[Any], bool]) -> None: ...


class Or:
    def __init__(self, *args: object) -> None: ...


class Schema:
    def __init__(self, __x: object) -> None: ...


class Optional(Schema):
    ...

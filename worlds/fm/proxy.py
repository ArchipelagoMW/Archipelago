import typing


class ValueProxy:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value


class OptionsProxy:
    serialized_options: typing.Dict[str, int]

    def __init__(self, serialized_options: typing.Dict[str, int]) -> None:
        self.serialized_options = serialized_options

    def __getattr__(self, item: str) -> ValueProxy:
        return ValueProxy(self.serialized_options[item])

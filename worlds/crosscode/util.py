"""
Everyone's favorite part of every python library: miscellaneous utility functions anc classes.
"""

import typing

K = typing.TypeVar("K")
V = typing.TypeVar("V")

class KeyDefaultDict(dict[K, V]):
    """
    Like defaultdict, but bases the default value on the key.
    """
    default_factory: typing.Callable[[K], V] | None
    """
    Function that takes a key and returns that key's default value.
    """

    def __init__(
       self,
       default_factory: typing.Callable[[K], V],
       *args: typing.Iterable[typing.Any],
       **kwargs: dict[str, typing.Any]
    ):
        """
        Creates a keydefaultdict with the specified factory function. Remaining arguments are sent to the dict 
        """
        self.default_factory = default_factory
        super().__init__(*args, **kwargs)

    def __missing__(self, key: K):
        """
        Runs when a dict value is missing.
        """
        if self.default_factory is None:
            raise KeyError( key )
        ret = self[key] = self.default_factory(key)
        return ret

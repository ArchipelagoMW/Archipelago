import functools
from typing import Union, Callable

from .logic_cache import CachedRules


class CachedLogic:
    player: int
    cached_rules: CachedRules

    def __init__(self, player: int, cached_rules: CachedRules):
        self.player = player
        self.cached_rules = cached_rules

    def get_cache_key(self, method: Union[str, Callable], *parameters) -> str:
        if isinstance(method, Callable):
            method = method.__name__
        if parameters is None:
            return f"{type(self).__name__} {method}"
        return f"{type(self).__name__} {method} {' '.join(map(str, parameters))}"


def cache_rule(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        key = self.get_cache_key(func, *args)
        return self.cached_rules.try_get_rule(key, lambda: func(self, *args, **kwargs))
    return wrapper


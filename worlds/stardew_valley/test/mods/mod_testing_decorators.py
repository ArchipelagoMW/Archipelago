import unittest
from collections.abc import Collection
from functools import wraps, partial
from typing import Type

from ... import options


def must_test_all_mods(cls: Type[unittest.TestCase] | None = None, /, *, excluded_mods: Collection[str] = None):
    if cls is None:
        return partial(must_test_all_mods, excluded_mods=excluded_mods)

    if excluded_mods is None:
        setattr(cls, "tested_mods", set())
    else:
        setattr(cls, "tested_mods", set(excluded_mods))

    orignal_tear_down_class = cls.tearDownClass

    @wraps(cls.tearDownClass)
    def wrapper():
        tested_mods: set[str] = getattr(cls, "tested_mods")

        diff = set(options.Mods.valid_keys) - tested_mods
        if diff:
            raise AssertionError(f"Mods {diff} were not tested")

        return orignal_tear_down_class()

    cls.tearDownClass = wrapper

    return cls


def mod_testing(func=None, /, *, mod: str):
    if func is None:
        return partial(mod_testing, mod=mod)

    @wraps(func)
    def wrapper(self: unittest.TestCase, *args, **kwargs):
        getattr(self, "tested_mods").add(mod)
        return func(self, *args, **kwargs)

    return wrapper

import unittest
from collections.abc import Callable, Iterable
from functools import wraps, partial
from typing import Type

from ... import options


def must_test_all_mods(cls: Type[unittest.TestCase] | None = None, /, *, excluded_mods: Iterable[str] | None = None) \
        -> partial[Type[unittest.TestCase]] | Type[unittest.TestCase]:
    if excluded_mods is None:
        excluded_mods = set()

    if cls is None:
        return partial(_must_test_all_mods, excluded_mods=excluded_mods)
    return _must_test_all_mods(cls, excluded_mods)


def _must_test_all_mods(cls: Type[unittest.TestCase], excluded_mods: Iterable[str]) -> Type[unittest.TestCase]:
    orignal_tear_down_class = cls.tearDownClass

    @wraps(cls.tearDownClass)
    def wrapper() -> None:
        tested_mods = set(excluded_mods)
        for attr in dir(cls):
            if attr.startswith("test"):
                func = getattr(cls, attr)
                if hasattr(func, "tested_mod"):
                    tested_mods.add(getattr(func, "tested_mod"))

        diff = options.Mods.valid_keys - tested_mods
        if diff:
            raise AssertionError(f"Mods {diff} were not tested")

        return orignal_tear_down_class()

    cls.tearDownClass = wrapper

    return cls


def is_testing_mod(mod: str) -> partial[Callable]:
    return partial(_is_testing_mod, mod=mod)


def _is_testing_mod(func: Callable, mod: str) -> Callable:
    setattr(func, "tested_mod", mod)
    return func

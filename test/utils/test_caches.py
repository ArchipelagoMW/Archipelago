# Tests for caches in Utils.py

import unittest
from typing import Any

from Utils import cache_argsless, cache_self1


class TestCacheArgless(unittest.TestCase):
    def test_cache(self) -> None:
        @cache_argsless
        def func_argless() -> object:
            return object()

        self.assertTrue(func_argless() is func_argless())

    if __debug__:  # assert only available with __debug__
        def test_invalid_decorator(self) -> None:
            with self.assertRaises(Exception):
                @cache_argsless  # type: ignore[arg-type]
                def func_with_arg(_: Any) -> None:
                    pass


class TestCacheSelf1(unittest.TestCase):
    def test_cache(self) -> None:
        class Cls:
            @cache_self1
            def func(self, _: Any) -> object:
                return object()

        o1 = Cls()
        o2 = Cls()
        self.assertTrue(o1.func(1) is o1.func(1))
        self.assertFalse(o1.func(1) is o1.func(2))
        self.assertFalse(o1.func(1) is o2.func(1))

    def test_gc(self) -> None:
        # verify that we don't keep a global reference
        import gc
        import weakref

        class Cls:
            @cache_self1
            def func(self, _: Any) -> object:
                return object()

        o = Cls()
        _ = o.func(o)  # keep a hard ref to the result
        r = weakref.ref(o)  # keep weak ref to the cache
        del o  # remove hard ref to the cache
        gc.collect()
        self.assertFalse(r())  # weak ref should be dead now

    if __debug__:  # assert only available with __debug__
        def test_no_self(self) -> None:
            with self.assertRaises(Exception):
                @cache_self1  # type: ignore[arg-type]
                def func() -> Any:
                    pass

        def test_too_many_args(self) -> None:
            with self.assertRaises(Exception):
                @cache_self1  # type: ignore[arg-type]
                def func(_1: Any, _2: Any, _3: Any) -> Any:
                    pass

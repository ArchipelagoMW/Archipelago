import itertools
import sys
from typing import Any, Callable, Iterable


def classvar_matrix(**kwargs: Iterable[Any]) -> Callable[[type], None]:
    """
    Create a new class for each variation of input, allowing to generate a TestCase matrix / parametrization that
    supports multi-threading and has better reporting for ``unittest --durations=...`` and ``pytest --durations=...``
    than subtests.

    The kwargs will be set as ClassVars in the newly created classes. Use as ::

        @classvar_matrix(var_name=[value1, value2])
        class MyTestCase(unittest.TestCase):
            var_name: typing.ClassVar[...]

    :param kwargs: A dict of ClassVars to set, where key is the variable name and value is a list of all values.
    :return: A decorator to be applied to a class.
    """
    keys: tuple[str]
    values: Iterable[Iterable[Any]]
    keys, values = zip(*kwargs.items())
    values = map(lambda v: sorted(v) if isinstance(v, (set, frozenset)) else v, values)
    permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]

    def decorator(cls: type) -> None:
        mod = sys.modules[cls.__module__]

        for permutation in permutations_dicts:

            class Unrolled(cls):  # type: ignore
                pass

            for k, v in permutation.items():
                setattr(Unrolled, k, v)
            params = ", ".join([f"{k}={repr(v)}" for k, v in permutation.items()])
            params = f"{{{params}}}"

            Unrolled.__module__ = cls.__module__
            Unrolled.__qualname__ = f"{cls.__qualname__}{params}"
            setattr(mod, f"{cls.__name__}{params}", Unrolled)

        return None

    return decorator

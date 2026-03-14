"""Micro benchmark comparing match as "switch" with if-elif and dict access"""

from timeit import timeit


def make_match(count: int) -> str:
    code = f"for val in range({count}):\n    match val:\n"
    for n in range(count):
        m = n + 1
        code += f"        case {n}:\n"
        code += f"            res = {m}\n"
    return code


def make_elif(count: int) -> str:
    code = f"for val in range({count}):\n"
    for n in range(count):
        m = n + 1
        code += f"    {'' if n == 0 else 'el'}if val == {n}:\n"
        code += f"        res = {m}\n"
    return code


def make_dict(count: int, mode: str) -> str:
    if mode == "value":
        code = "dct = {\n"
        for n in range(count):
            m = n + 1
            code += f"    {n}: {m},\n"
        code += "}\n"
        code += f"for val in range({count}):\n    res = dct[val]"
        return code
    elif mode == "call":
        code = ""
        for n in range(count):
            m = n + 1
            code += f"def func{n}():\n    val = {m}\n\n"
        code += "dct = {\n"
        for n in range(count):
            code += f"    {n}: func{n},\n"
        code += "}\n"
        code += f"for val in range({count}):\n    dct[val]()"
        return code
    return ""


def timeit_best_of_5(stmt: str, setup: str = "pass") -> float:
    """
    Benchmark some code, returning the best of 5 runs.
    :param stmt: Code to benchmark
    :param setup: Optional code to set up environment
    :return: Time taken in microseconds
    """
    return min(timeit(stmt, setup, number=10000, globals={}) for _ in range(5)) * 100


def main() -> None:
    for count in (3, 5, 8, 10, 20, 30):
        print(f"value of {count:-2} with match: {timeit_best_of_5(make_match(count)) / count:.3f} us")
        print(f"value of {count:-2} with elif:  {timeit_best_of_5(make_elif(count)) / count:.3f} us")
        print(f"value of {count:-2} with dict:  {timeit_best_of_5(make_dict(count, 'value')) / count:.3f} us")
        print(f"call  of {count:-2} with dict:  {timeit_best_of_5(make_dict(count, 'call')) / count:.3f} us")


if __name__ == "__main__":
    main()

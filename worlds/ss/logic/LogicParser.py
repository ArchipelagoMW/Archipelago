import re

from .Logic import ALL_REQUIREMENTS, MACROS
from ..Items import ITEM_TABLE

def parse_expression(expression: str) -> str:
    """
    This function parses a logical expression as a string and returns a string
    of Python code that can be compiled and ran.

    :param expression: The logical expression string
    :return: A string of uncompiled Python code.
    """
    exp_list = re.split(r"([&|()])", expression)
    exp_list = [i.strip() for i in exp_list]
    
    py_exp = ""
    for i, ex in enumerate(exp_list):
        if ex == "":
            continue
        elif ex == "&":
            py_exp = py_exp + " and "
            continue
        elif ex == "|":
            py_exp = py_exp + " or "
            continue
        elif ex in ["(", ")"]:
            py_exp = py_exp + ex
            continue

        if ex == "Nothing":
            py_exp = py_exp + f"""True"""
        elif ex.startswith("can_reach_region"):
            region = ex.split(" ", maxsplit=1)[1]
            py_exp = py_exp + f"""state.can_reach_region("{region}", player)"""
        elif ex.startswith("option_"):
            py_exp = py_exp + f"""state._ss_{ex}(player)"""
        elif ex.startswith("not option_"):
            py_exp = py_exp + f"""not state._ss_{ex[4:]}(player)"""
        elif ex.startswith("_"):
            py_exp = py_exp + f"""state._ss{ex}(player)"""
        elif ex in MACROS:
            py_exp = py_exp + _get_macro(ex)
        else:
            if " x" in ex:
                ex_list = ex.split(" x")
                assert len(ex_list) == 2, f"Could not find a quantity for expression: {ex}"
                item = ex_list[0]
                quantity = ex_list[1]
                assert quantity.isnumeric(), f"Quantity found is not numeric: {ex}"
                quantity = int(quantity)
                assert quantity <= ITEM_TABLE[item].quantity, f"Quantity required is greater than quantity available: {ex}"
            else:
                item = ex
                quantity = 1

            if item in ITEM_TABLE.keys():
                py_exp = py_exp + f"""state.has("{item}", player, {quantity})"""
            else:
                raise Exception(f"Unknown logic expression: {ex}")

    return py_exp

def _get_macro(macro: str) -> str:
    if macro not in MACROS.keys():
        raise Exception(f"Could not find macro: {macro}")
    return f"""({parse_expression(MACROS[macro])})"""


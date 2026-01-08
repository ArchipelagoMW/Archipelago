"""
Contains various functions that take structures containing AST entries and emits them in pretty-looking lists.
"""

import ast

def emit_list(lst: list[ast.AST], indent: str = "    ") -> str:
    """
    Render a list of AST instances and print them each on their own line, surrounded with square brackets.
    """
    after = ",\n"

    return "[\n" + "".join([indent + ast.unparse(item) + after for item in lst]) + "]"


def emit_set(lst: list[ast.AST], indent: str = "    ") -> str:
    """
    Render a list of AST instances and print them each on their own line, surrounded with curly braces.
    """
    after = ",\n"

    return "{\n" + "".join([indent + ast.unparse(item) + after for item in lst]) + "}"


def emit_dict(items: list[tuple[ast.AST, ast.AST]], indent: str = "    ") -> str:
    """
    Render two list of AST instances (keys and values) and print them each on their own line, surrounded with curly
    braces.
    """
    after = ",\n"

    return "{\n" + "".join([f"{indent}{ast.unparse(key)}: {ast.unparse(value)}{after}" for key, value in items]) + "}"

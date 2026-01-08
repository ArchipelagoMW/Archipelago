"""
Provide the Jinja extension used to generate python files.
"""

import ast
import typing

from jinja2 import Environment
from jinja2.ext import Extension

from . import ast as astgen
from .emit import emit_dict, emit_list, emit_set


def to_code(target: typing.Any, kind: str) -> ast.expr:
    """
    Converts *target* into an AST expression of kind *kind* using codegen's AST module.
    """
    if kind == "constant":
        return ast.Constant(target)
    if kind == "tuple":
        return ast.Tuple([ast.Constant(el) for el in target])
    each_func: typing.Callable[..., ast.expr] | None = getattr(astgen, f"create_expression_{kind}")
    if each_func is None:
        raise RuntimeError(f"No function to emit {kind}")
    return each_func(target)


def emit_list_internal(lst: list[typing.Any], kind: str) -> str:
    """
    Emit a list of any type, using the AST function named for *kind* to transform them to AST objects.
    """
    return emit_list([to_code(el, kind) for el in lst])


def emit_set_internal(lst: list[typing.Any], kind: str) -> str:
    """
    Emit a set of any type, using the AST function named for *kind* to transform them to AST objects.
    """
    return emit_set([to_code(el, kind) for el in lst])


def emit_dict_internal(dct: list[tuple[typing.Any, typing.Any]], kind_key: str, kind_value: str) -> str:
    """
    Emit a dict of any two types, using the AST functions named for *kind_key*  and *kind_value* to transform them to
    AST objects.
    """
    return emit_dict(list(zip(
        [to_code(k, kind_key) for k, _ in dct],
        [to_code(v, kind_value) for _, v in dct]
    )))


class CrossCodeJinjaExtension(Extension):
    """
    Abstract class serving as a basis for this module's jinja extension. It provides filters to be used by this
    APWorld's template files.

    This has to be abstract because the Jinja API seems to require all extensions to be passed in by type, not by
    instance. Use this module's `create_jinja_extension` function to create a concrete type.
    """
    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.filters.update({
            "to_code": to_code,
            "emit_list": emit_list_internal,
            "emit_set": emit_set_internal,
            "emit_dict": emit_dict_internal,
        })

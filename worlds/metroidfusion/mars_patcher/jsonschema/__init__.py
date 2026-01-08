"""
An implementation of JSON Schema for Python.

The main functionality is provided by the validator classes for each of the
supported JSON Schema versions.

Most commonly, `jsonschema.validators.validate` is the quickest way to simply
validate a given instance under a schema, and will create a validator
for you.
"""
import warnings

from ._format import FormatChecker
from ._types import TypeChecker
from .exceptions import SchemaError, ValidationError
from .validators import (
    Draft3Validator,
    Draft4Validator,
    Draft6Validator,
    Draft7Validator,
    Draft201909Validator,
    Draft202012Validator,
    validate,
)


def __getattr__(name):
    if name == "__version__":
        warnings.warn(
            "Accessing jsonschema.__version__ is deprecated and will be "
            "removed in a future release. Use importlib.metadata directly "
            "to query for jsonschema's version.",
            DeprecationWarning,
            stacklevel=2,
        )

        from importlib import metadata
        return metadata.version("jsonschema")
    elif name == "RefResolver":
        from .validators import _RefResolver
        warnings.warn(
            _RefResolver._DEPRECATION_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        return _RefResolver
    elif name == "ErrorTree":
        warnings.warn(
            "Importing ErrorTree directly from the jsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "jsonschema.exceptions instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from .exceptions import ErrorTree
        return ErrorTree
    elif name == "FormatError":
        warnings.warn(
            "Importing FormatError directly from the jsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "jsonschema.exceptions instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from .exceptions import FormatError
        return FormatError
    elif name == "Validator":
        warnings.warn(
            "Importing Validator directly from the jsonschema package "
            "is deprecated and will become an ImportError. Import it from "
            "jsonschema.protocols instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from .protocols import Validator
        return Validator
    elif name == "RefResolutionError":
        from .exceptions import _RefResolutionError
        warnings.warn(
            _RefResolutionError._DEPRECATION_MESSAGE,
            DeprecationWarning,
            stacklevel=2,
        )
        return _RefResolutionError

    format_checkers = {
        "draft3_format_checker": Draft3Validator,
        "draft4_format_checker": Draft4Validator,
        "draft6_format_checker": Draft6Validator,
        "draft7_format_checker": Draft7Validator,
        "draft201909_format_checker": Draft201909Validator,
        "draft202012_format_checker": Draft202012Validator,
    }
    ValidatorForFormat = format_checkers.get(name)
    if ValidatorForFormat is not None:
        warnings.warn(
            f"Accessing jsonschema.{name} is deprecated and will be "
            "removed in a future release. Instead, use the FORMAT_CHECKER "
            "attribute on the corresponding Validator.",
            DeprecationWarning,
            stacklevel=2,
        )
        return ValidatorForFormat.FORMAT_CHECKER

    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = [
    "Draft3Validator",
    "Draft4Validator",
    "Draft6Validator",
    "Draft7Validator",
    "Draft201909Validator",
    "Draft202012Validator",
    "FormatChecker",
    "SchemaError",
    "TypeChecker",
    "ValidationError",
    "validate",
]

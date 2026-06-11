"""Zip-safe CSV loading for the cvaos data packages.

The CSVs live inside the package, which may be a zipped .apworld; paths derived from
``__file__`` do not exist on disk there. Resources are read through the package
loader (``pkgutil.get_data``) instead, which zipimport supports.
"""

from __future__ import annotations

import csv
import io
import pkgutil

__all__ = [
    "open_csv",
    "open_csv_if_exists",
]


def open_csv_if_exists(package: str, filename: str) -> csv.DictReader[str] | None:
    """Return a DictReader over ``filename`` inside ``package``, or None if absent."""
    try:
        raw = pkgutil.get_data(package, filename)
    except OSError:  # zipimport raises OSError, filesystem loaders FileNotFoundError
        return None
    if raw is None:
        return None
    return csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""))


def open_csv(package: str, filename: str) -> csv.DictReader[str]:
    """Return a DictReader over ``filename`` inside ``package``; raise if missing."""
    reader = open_csv_if_exists(package, filename)
    if reader is None:
        raise FileNotFoundError(f"resource {filename!r} not found in package {package}")
    return reader

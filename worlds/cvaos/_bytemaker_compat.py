"""Single import point for bytemaker.

bytemaker >= 0.11 is pure Python (bitarray is only an optional ``[speedups]`` extra
with a pure-Python ``BitVector`` fallback), so it can be vendored for frozen
Archipelago installs, which cannot pip-install. An installed bytemaker wins over the
copy vendored in ``worlds/cvaos/vendor``.
"""

__all__ = [
    "SInt16",
    "UInt8",
    "UInt16",
    "from_bytes_aggregate",
    "to_bytes_aggregate",
]

try:
    from bytemaker.bittypes import SInt16, UInt8, UInt16
    from bytemaker.conversions.aggregate_types import from_bytes_aggregate, to_bytes_aggregate
except ImportError:
    from ._vendor import ensure_vendor_on_sys_path
    ensure_vendor_on_sys_path()
    from bytemaker.bittypes import SInt16, UInt8, UInt16
    from bytemaker.conversions.aggregate_types import from_bytes_aggregate, to_bytes_aggregate

from importlib.util import find_spec

if find_spec("bitarray"):
    from bytemaker.bitvector.bitvector_with_bitarray_speedup import (
        BitsCastable,
        BitsConstructible,
        BitVector,
    )
else:
    from bytemaker.bitvector.bitvector_native import (
        BitsCastable,
        BitsConstructible,
        BitVector,
    )

__all__ = ["BitVector", "BitsCastable", "BitsConstructible"]

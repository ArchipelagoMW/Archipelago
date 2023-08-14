from typing import NamedTuple


class JewelPieces(NamedTuple):
    ne: str
    se: str
    sw: str
    nw: str

    locations = tuple("Top Right/Bottom Right/Bottom Left/Top Left".split("/"))

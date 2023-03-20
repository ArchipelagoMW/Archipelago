import typing


class JewelPieces(typing.NamedTuple):
    ne: str
    se: str
    sw: str
    nw: str

    locations = tuple("Top Right/Bottom Right/Bottom Left/Top Left".split("/"))


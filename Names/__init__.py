import typing


class JewelPieces(typing.NamedTuple):
    ne: str
    nw: str
    sw: str
    se: str

    locations = tuple("Top Right/Top Left/Bottom Left/Bottom Right".split("/"))


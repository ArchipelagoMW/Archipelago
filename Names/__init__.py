import typing


class JewelPieces(typing.NamedTuple):
    nw: str
    ne: str
    sw: str
    se: str

    locations = tuple("Top Left/Top Right/Bottom Left/Bottom Right".split("/"))


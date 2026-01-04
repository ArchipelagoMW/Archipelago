import typing


class RegionRow(typing.NamedTuple):
    name: str
    itemReq: str
    connections: typing.List[str]
    resources: typing.List[str]


class ResourceRow(typing.NamedTuple):
    name: str

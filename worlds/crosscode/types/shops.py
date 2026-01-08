import typing
from dataclasses import dataclass

from .locations import AccessInfo


@dataclass
class ShopData:
    internal_name: str
    name: str
    access: AccessInfo
    metadata: typing.Optional[dict[str, int | float | str]] = None

from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import OkamiWorld


class WarpType(StrEnum):
    MERMAID_SPRING = "Mermaid Spring"
    MIST_WARP = "Mist Warp"

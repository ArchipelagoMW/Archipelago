from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Tuple

from ...strings.tool_names import Tool


class PriceMultipliers:
    CHEAP = 2 / 5
    VERY_CHEAP = 1 / 5


progressive_house = "Progressive House"

# This assumes that the farm house is always available, which might not be true forever...
progressive_house_by_upgrade_name = {
    Tool.farm_house: 0,
    Tool.kitchen: 1,
    Tool.kids_room: 2,
    Tool.cellar: 3
}


def to_progressive_item(tool: str) -> Tuple[str, int]:
    """Return the name of the progressive item and its quantity required to unlock the tool.
    """
    if tool in [Tool.coop, Tool.barn, Tool.shed]:
        return f"Progressive {tool}", 1
    elif tool.startswith("Big"):
        return f"Progressive {tool[tool.index(' ') + 1:]}", 2
    elif tool.startswith("Deluxe"):
        return f"Progressive {tool[tool.index(' ') + 1:]}", 3
    elif tool in progressive_house_by_upgrade_name:
        return progressive_house, progressive_house_by_upgrade_name[tool]

    return tool, 1


def to_location_name(tool: str) -> str:
    return f"{tool} Blueprint"


@dataclass(frozen=True)
class ToolProgressionFeature(ABC):
    is_progressive: ClassVar[bool]
    price_multiplier: float = 1.0

    # to_progressive_item = staticmethod(to_progressive_item)

    # to_location_name = staticmethod(to_location_name)


class ToolProgressionVanilla(ToolProgressionFeature):
    is_progressive = False


class ToolProgressionProgressive(ToolProgressionFeature):
    is_progressive = True

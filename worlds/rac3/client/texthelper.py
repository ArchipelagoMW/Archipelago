from typing import TYPE_CHECKING

from NetUtils import NetworkItem
from worlds.rac3.constants.messages.text_color import RAC3TEXTCOLOR

if TYPE_CHECKING:
    from worlds.rac3.client.client import Rac3Context


def colorize_item_name(item_name: str, item_flags: int) -> str:
    color = RAC3TEXTCOLOR.WHITE  # Filler / Trap = White
    if item_flags & 0b001:
        color = RAC3TEXTCOLOR.MAGENTA  # Progression = Magenta
    elif item_flags & 0b010:
        color = RAC3TEXTCOLOR.BLUE  # Useful = Blue
    return f"{color}{item_name}{RAC3TEXTCOLOR.NORMAL}"


def get_rich_item_name(ctx: 'Rac3Context', net_item: NetworkItem, player_name_after: bool = False) -> str:
    item_name = ctx.item_names.lookup_in_slot(net_item.item, net_item.player)
    item_name = colorize_item_name(item_name, net_item.flags)
    location_name = ctx.location_names.lookup_in_slot(net_item.location, net_item.player)

    if ctx.slot == net_item.player:
        # Item is ours, no need to specify player name
        return f"Found {item_name} at {location_name}"
    else:
        # Item belongs to someone else, give their name
        player_name = ctx.player_names.get(net_item.player, "???")
        if player_name_after:
            return f"Sent {item_name} to {RAC3TEXTCOLOR.GREEN}{player_name}"
        return f"Sent {player_name}'s {item_name}"

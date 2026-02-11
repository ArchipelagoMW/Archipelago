"""This module contains functions for processing the message displayed when sending items"""

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification
from NetUtils import NetworkItem
from worlds.rac3.constants.messages.text_strings import RAC3TEXTFORMATSTRING

if TYPE_CHECKING:
    from worlds.rac3.client.client import Rac3Context


def colorize_item_name(item_name: str, item_flags: int) -> str:
    """Function to colorize the item name"""
    color = RAC3TEXTFORMATSTRING.WHITE  # Filler / Trap = White
    if item_flags & ItemClassification.progression:
        color = RAC3TEXTFORMATSTRING.MAGENTA  # Progression = Magenta
    elif item_flags & ItemClassification.useful:
        color = RAC3TEXTFORMATSTRING.BLUE  # Useful = Blue
    return f"{color}{item_name}{RAC3TEXTFORMATSTRING.NORMAL}"


def get_sent_item_message(ctx: 'Rac3Context', net_item: NetworkItem, player_name_after: bool = False) -> str:
    """Returns the pop-up message to be displayed in game, given the item just collected"""
    item_name = colorize_item_name(ctx.item_names.lookup_in_slot(net_item.item, net_item.player), net_item.flags)
    location_name = ctx.location_names.lookup_in_slot(net_item.location, net_item.player)

    if ctx.slot == net_item.player:
        # Item is ours, no need to specify player name
        return f"Found {item_name} at {location_name}"
    else:
        # Item belongs to someone else, give their name
        player_name = ctx.player_names.get(net_item.player, "???")
        if player_name_after:
            return f"Sent {item_name} to {RAC3TEXTFORMATSTRING.GREEN}{player_name}"
        return f"Sent {player_name}'s {item_name}"

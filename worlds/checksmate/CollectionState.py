from typing import Dict, List, Union
from BaseClasses import CollectionState, Item
from .Items import item_table, progression_items
from .ItemUtils import get_parents, get_children
import logging


class CMCollectionState:
    """Handles the state management for ChecksMate while items are being placed in locations, including
    collecting and removing items, and tracking material values. This work is after items are created."""

    def __init__(self, world):
        self.world = world

    def collect(self, state: CollectionState, item: Item) -> int:
        """Calculate the material value gained from collecting this item."""
        material = 0
        item_count = state.prog_items[self.world.player][item.name]
        # check if there are existing unused upgrades to this piece which are immediately satisfied
        children = get_children(item.name)
        for child in children:
            if item_table[child].material == 0:
                continue
            # TODO: when a child could have multiple parents, check that this is also the least parent
            if item_count < state.prog_items[self.world.player].get(child, 0):
                # we had an upgrade, so add that upgrade to the material count
                material += item_table[child].material
                logging.debug("Adding child " + child + " having count: " + str(state.prog_items[self.world.player].get(child, 0)))
            else:
                # not immediately upgraded, but maybe later
                logging.debug("Added item " + item.name + " had insufficient children " + child + " to upgrade it")
        # check if this is an upgrade which is immediately satisfied by applying it to an existing piece
        parents = get_parents(item.name)
        if len(parents) == 0 or item_table[item.name].material == 0:
            # this is a root element (like a piece), not an upgrade, so we can use it immediately
            material += item_table[item.name].material
        else:
            # this is an upgrade, so we can only apply it if it can find an unsatisfied parent
            fewest_parents = min([state.prog_items[self.world.player].get(parent[0], 0) for parent in parents])
            # TODO: when a parent could have multiple children, check that this is also the least child
            if item_count < fewest_parents * parents[0][1]:
                # found a piece we could upgrade, so apply the upgrade
                material += item_table[item.name].material
                logging.debug("Item " + item.name + " had sufficient parents " + str(fewest_parents) + " to be tried")
            else:
                # not upgrading anything, but maybe later
                logging.debug("Added item " + item.name + " had insufficient parents " + str(fewest_parents))

        logging.debug("Adding " + item.name + " with material value " + str(material))
        return material

    def remove(self, state: CollectionState, item: Item) -> int:
        """Calculate the material value lost from removing this item."""
        material = 0
        item_count = state.prog_items[self.world.player][item.name]
        children = get_children(item.name)
        for child in children:
            if item_table[child].material == 0:
                continue
            # TODO: when a child could have multiple parents, check that this is also the least parent
            if item_count <= state.prog_items[self.world.player][child]:
                material -= item_table[child].material
                logging.debug("Removing child " + child + " having count: " + str(state.prog_items[self.world.player][child]))
            else:
                logging.debug("Removed item " + item.name + " had insufficient children " + child)
        parents = get_parents(item.name)
        if len(parents) == 0 or item_table[item.name].material == 0:
            material -= item_table[item.name].material
        else:
            fewest_parents = min([state.prog_items[self.world.player].get(parent[0], 0) for parent in parents])
            if item_count <= fewest_parents:
                material -= item_table[item.name].material
                logging.debug("Item " + item.name + " had sufficient parents " + str(fewest_parents) + " to be removed")
            else:
                logging.debug("Removed item " + item.name + " had insufficient parents " + str(fewest_parents))

        logging.debug("Removing " + item.name + " with material value " + str(material))
        return material

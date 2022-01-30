from typing import NamedTuple, Union
import logging

from BaseClasses import Item

from ..AutoWorld import World


class GenericWorld(World):
    game = "Archipelago"
    topology_present = False
    item_name_to_id = {
        "Nothing": -1
    }
    location_name_to_id = {
        "Cheat Console": -1,
        "Server": -2
    }
    hidden = True

    def generate_early(self):
        self.world.player_types[self.player] = 0  # mark as spectator

    def create_item(self, name: str) -> Item:
        if name == "Nothing":
            return Item(name, False, -1, self.player)
        raise KeyError(name)


class PlandoItem(NamedTuple):
    item: str
    location: str
    world: Union[bool, str] = False  # False -> own world, True -> not own world
    from_pool: bool = True  # if item should be removed from item pool
    force: str = 'silent'  # false -> warns if item not successfully placed. true -> errors out on failure to place item.

    def warn(self, warning: str):
        if self.force in ['true', 'fail', 'failure', 'none', 'false', 'warn', 'warning']:
            logging.warning(f'{warning}')
        else:
            logging.debug(f'{warning}')

    def failed(self, warning: str, exception=Exception):
        if self.force in ['true', 'fail', 'failure']:
            raise exception(warning)
        else:
            self.warn(warning)


class PlandoConnection(NamedTuple):
    entrance: str
    exit: str
    direction: str  # entrance, exit or both

from .LocationList import location_table

import typing
from enum import Enum
from BaseClasses import Location

class DisableType(Enum): 
    ENABLED = 0
    PENDING = 1
    DISABLED = 2

class OOTLocation(Location): 
    game: str = 'Ocarina of Time'

    def __init__(self, player, name='', address=None, address2=None, default=None, type='Chest', scene=None, parent=None, filter_tags=None, internal=False):
        super(OOTLocation, self).__init__(player, name, address, parent)
        self.address2 = address2
        self.default = default
        self.type = type
        self.scene = scene
        self.internal = internal
        if filter_tags is None: 
            self.filter_tags = None
        else: 
            self.filter_tags = list(filter_tags)
        self.never = False # no idea what this does

        if type == 'Event': 
            self.event = True


def LocationFactory(locations, player: int):
    ret = []
    singleton = False
    if isinstance(locations, str):
        locations = [locations]
        singleton = True
    for location in locations:
        if location in location_table:
            match_location = location
        else:
            match_location = next(filter(lambda k: k.lower() == location.lower(), location_table), None)
        if match_location:
            type, scene, default, addresses, vanilla_item, filter_tags = location_table[match_location]
            if addresses is None:
                addresses = (None, None)
            address, address2 = addresses
            ret.append(OOTLocation(player, match_location, address, address2, default, type, scene, filter_tags=filter_tags))
        else:
            raise KeyError('Unknown Location: %s', location)

    if singleton:
        return ret[0]
    return ret



location_id_offset = 67000
lookup_id_to_name: typing.Dict[int, str] = {(location_id_offset + index): name for (index, name) in enumerate(location_table) 
    if location_table[name][0] not in ['Event', 'Drop', 'HintStone', 'Hint']}


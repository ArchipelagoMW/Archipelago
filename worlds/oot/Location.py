from enum import Enum
from .LocationList import location_table
from BaseClasses import Location

location_id_offset = 67000
locnames_pre_70 = {
    "Gift from Sages",
    "ZR Frogs Zeldas Lullaby",
    "ZR Frogs Eponas Song",
    "ZR Frogs Sarias Song",
    "ZR Frogs Suns Song",
    "ZR Frogs Song of Time",
}
loctypes_70 = {'Beehive', 'Pot', 'FlyingPot', 'Crate', 'SmallCrate', 'RupeeTower', 'Freestanding', 'ActorOverride'}
new_name_order = sorted(location_table.keys(),
    key=lambda name: 2 if location_table[name][0] in loctypes_70
                else 1 if name in locnames_pre_70
                else 0)

location_name_to_id = {name: (location_id_offset + index) for (index, name) in enumerate(new_name_order) 
    if location_table[name][0] not in {'Boss', 'Event', 'Drop', 'HintStone', 'Hint'}}

class DisableType(Enum):
    ENABLED  = 0
    PENDING = 1
    DISABLED = 2

class OOTLocation(Location): 
    game: str = 'Ocarina of Time'

    def __init__(self, player, name='', code=None, address1=None, address2=None,
        default=None, type='Chest', scene=None, parent=None, filter_tags=None,
        internal=False, vanilla_item=None
    ):
        super(OOTLocation, self).__init__(player, name, code, parent)
        self.address1 = address1
        self.address2 = address2
        self.default = default
        self.type = type
        self.scene = scene
        self.internal = internal
        self.vanilla_item = vanilla_item
        if filter_tags is None: 
            self.filter_tags = None
        else: 
            self.filter_tags = list(filter_tags)
        self.never = False # no idea what this does
        self.disabled = DisableType.ENABLED

        if type == 'Event': 
            self.event = True

    @property
    def dungeon(self):
        return self.parent_region.dungeon


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
            address1, address2 = addresses
            ret.append(OOTLocation(player, match_location,
                location_name_to_id.get(match_location, None),
                address1, address2, default, type, scene,
                filter_tags=filter_tags, vanilla_item=vanilla_item))
        else:
            raise KeyError('Unknown Location: %s', location)

    if singleton:
        return ret[0]
    return ret



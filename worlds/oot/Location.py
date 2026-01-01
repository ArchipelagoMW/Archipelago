from enum import Enum
from .LocationList import location_table
from BaseClasses import Location

non_indexed_location_types = {'Boss', 'Event', 'Drop', 'HintStone', 'Hint'}

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
    if location_table[name][0] not in non_indexed_location_types}

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


def build_location_name_groups() -> dict:

    def fix_sing(t) -> tuple:
        if isinstance(t, str):
            return (t,)
        return t

    def rename(d, k1, k2) -> None:
        d[k2] = d[k1]
        del d[k1]

    # whoever wrote the location table didn't realize they need to add a comma to mark a singleton as a tuple
    # so we have to check types unfortunately
    tags = set()
    for v in location_table.values():
        if v[5] is not None:
            tags.update(fix_sing(v[5]))

    sorted_tags = sorted(list(tags))

    ret = {
        tag: {k for k, v in location_table.items()
        if v[5] is not None
            and tag in fix_sing(v[5])
            and v[0] not in non_indexed_location_types}
        for tag in sorted_tags
    }

    # Delete tags which are a combination of other tags
    del ret['Death Mountain']
    del ret['Forest']
    del ret['Gerudo']
    del ret['Kakariko']
    del ret['Market']

    # Delete Vanilla and MQ tags because they are just way too broad
    del ret['Vanilla']
    del ret['Master Quest']

    rename(ret, 'Beehive', 'Beehives')
    rename(ret, 'Cow', 'Cows')
    rename(ret, 'Crate', 'Crates')
    rename(ret, 'Deku Scrub', 'Deku Scrubs')
    rename(ret, 'FlyingPot', 'Flying Pots')
    rename(ret, 'Freestanding', 'Freestanding Items')
    rename(ret, 'Pot', 'Pots')
    rename(ret, 'RupeeTower', 'Rupee Groups')
    rename(ret, 'SmallCrate', 'Small Crates')
    rename(ret, 'the Market', 'Market')
    rename(ret, 'the Graveyard', 'Graveyard')
    rename(ret, 'the Lost Woods', 'Lost Woods')

    return ret


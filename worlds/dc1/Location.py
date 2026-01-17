from BaseClasses import Location, Region
from worlds.dc1.game_id import dc1_name


class DarkCloudLocation(Location):
    game = dc1_name

    def __init__(self, player, name, address, loc_type, region: Region, access=None, event=None):
        super(DarkCloudLocation, self).__init__(player, name, address)
        self.type = loc_type
        self.parent_region = region
        self.access = access

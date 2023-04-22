from typing import List
from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class TowerOfHera(Z3Region, IReward):
    Name = "Tower of Hera"
    Area = "Tower of Hera"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.RegionItems = [ ItemType.KeyTH, ItemType.BigKeyTH, ItemType.MapTH, ItemType.CompassTH]
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 256+115, 0x308162, LocationType.HeraStandingKey, "Tower of Hera - Basement Cage"),
            Location(self, 256+116, 0x1E9AD, LocationType.Regular, "Tower of Hera - Map Chest"),
            Location(self, 256+117, 0x1E9E6, LocationType.Regular, "Tower of Hera - Big Key Chest",
                lambda items: items.KeyTH and items.CanLightTorches())
                .AlwaysAllow(lambda item, items: item.Is(ItemType.KeyTH, self.world)),
            Location(self, 256+118, 0x1E9FB, LocationType.Regular, "Tower of Hera - Compass Chest",
                lambda items: items.BigKeyTH),
            Location(self, 256+119, 0x1E9F8, LocationType.Regular, "Tower of Hera - Big Chest",
                lambda items: items.BigKeyTH),
            Location(self, 256+120, 0x308152, LocationType.Regular, "Tower of Hera - Moldorm",
                lambda items: items.BigKeyTH and self.CanBeatBoss(items)),
            ]

    def CanBeatBoss(self, items: Progression):
        return items.Sword or items.Hammer

    def CanEnter(self, items: Progression):
        return (items.Mirror or items.Hookshot and items.Hammer) and self.world.CanEnter("Light World Death Mountain West", items)

    def CanComplete(self, items: Progression):
        return self.GetLocation("Tower of Hera - Moldorm").Available(items)

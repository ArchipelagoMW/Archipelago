from typing import List
from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class ThievesTown(Z3Region, IReward):
    Name = "Thieves' Town"
    Area = "Thieves' Town"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.RegionItems = [ ItemType.KeyTT, ItemType.BigKeyTT, ItemType.MapTT, ItemType.CompassTT]
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 256+153, 0x1EA01, LocationType.Regular, "Thieves' Town - Map Chest"),
            Location(self, 256+154, 0x1EA0A, LocationType.Regular, "Thieves' Town - Ambush Chest"),
            Location(self, 256+155, 0x1EA07, LocationType.Regular, "Thieves' Town - Compass Chest"),
            Location(self, 256+156, 0x1EA04, LocationType.Regular, "Thieves' Town - Big Key Chest"),
            Location(self, 256+157, 0x1EA0D, LocationType.Regular, "Thieves' Town - Attic",
                lambda items: items.BigKeyTT and items.KeyTT),
            Location(self, 256+158, 0x1EA13, LocationType.Regular, "Thieves' Town - Blind's Cell",
                lambda items: items.BigKeyTT),
            Location(self, 256+159, 0x1EA10, LocationType.Regular, "Thieves' Town - Big Chest",
                lambda items: items.BigKeyTT and items.Hammer and
                    (self.GetLocation("Thieves' Town - Big Chest").ItemIs(ItemType.KeyTT, self.world) or items.KeyTT))
                .AlwaysAllow(lambda item, items: item.Is(ItemType.KeyTT, self.world) and items.Hammer),
            Location(self, 256+160, 0x308156, LocationType.Regular, "Thieves' Town - Blind",
                lambda items: items.BigKeyTT and items.KeyTT and self.CanBeatBoss(items)),
            ]

    def CanBeatBoss(self, items: Progression):
        return items.Sword or items.Hammer or items.Somaria or items.Byrna

    def CanEnter(self, items: Progression):
        return items.MoonPearl and self.world.CanEnter("Dark World North West", items)

    def CanComplete(self, items: Progression):
        return self.GetLocation("Thieves' Town - Blind").Available(items)

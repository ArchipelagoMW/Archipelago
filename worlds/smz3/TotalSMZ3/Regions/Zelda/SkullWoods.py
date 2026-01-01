from typing import List
from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class SkullWoods(Z3Region, IReward):
    Name = "Skull Woods"
    Area = "Skull Woods"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.RegionItems = [ ItemType.KeySW, ItemType.BigKeySW, ItemType.MapSW, ItemType.CompassSW]
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 256+145, 0x1E9A1, LocationType.Regular, "Skull Woods - Pot Prison"),
            Location(self, 256+146, 0x1E992, LocationType.Regular, "Skull Woods - Compass Chest"),
            Location(self, 256+147, 0x1E998, LocationType.Regular, "Skull Woods - Big Chest",
                lambda items: items.BigKeySW)
                .AlwaysAllow(lambda item, items: item.Is(ItemType.BigKeySW, self.world)),
            Location(self, 256+148, 0x1E99B, LocationType.Regular, "Skull Woods - Map Chest"),
            Location(self, 256+149, 0x1E9C8, LocationType.Regular, "Skull Woods - Pinball Room")
                .Allow(lambda item, items: item.Is(ItemType.KeySW, self.world)),
            Location(self, 256+150, 0x1E99E, LocationType.Regular, "Skull Woods - Big Key Chest"),
            Location(self, 256+151, 0x1E9FE, LocationType.Regular, "Skull Woods - Bridge Room",
                lambda items: items.Firerod),
            Location(self, 256+152, 0x308155, LocationType.Regular, "Skull Woods - Mothula",
                lambda items: items.Firerod and items.Sword and items.KeySW >= 3),
            ]

    def CanEnter(self, items: Progression):
        return items.MoonPearl and self.world.CanEnter("Dark World North West", items)

    def CanComplete(self, items: Progression):
        return self.GetLocation("Skull Woods - Mothula").Available(items)

from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class EasternPalace(Z3Region, IReward):
    Name = "Eastern Palace"
    Area = "Eastern Palace"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Reward = RewardType.Null
        self.RegionItems = [ ItemType.BigKeyEP, ItemType.MapEP, ItemType.CompassEP ]
        self.Locations = [
            Location(self, 256+103, 0x1E9B3, LocationType.Regular, "Eastern Palace - Cannonball Chest"),
            Location(self, 256+104, 0x1E9F5, LocationType.Regular, "Eastern Palace - Map Chest"),
            Location(self, 256+105, 0x1E977, LocationType.Regular, "Eastern Palace - Compass Chest"),
            Location(self, 256+106, 0x1E97D, LocationType.Regular, "Eastern Palace - Big Chest",
                lambda items: items.BigKeyEP),
            Location(self, 256+107, 0x1E9B9, LocationType.Regular, "Eastern Palace - Big Key Chest",
                lambda items: items.Lamp),
            Location(self, 256+108, 0x308150, LocationType.Regular, "Eastern Palace - Armos Knights",
                lambda items: items.BigKeyEP and items.Bow and items.Lamp)
            ]

    def CanComplete(self, items: Progression):
        return self.GetLocation("Eastern Palace - Armos Knights").Available(items)

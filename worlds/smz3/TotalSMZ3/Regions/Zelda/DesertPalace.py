from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import ItemType, Progression

class DesertPalace(Z3Region, IReward):
    Name = "Desert Palace"
    Area = "Desert Palace"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Reward = RewardType.Null
        self.RegionItems = [ ItemType.KeyDP, ItemType.BigKeyDP, ItemType.MapDP, ItemType.CompassDP ]
        self.Locations = [
            Location(self, 256+109, 0x1E98F, LocationType.Regular, "Desert Palace - Big Chest",
                lambda items: items.BigKeyDP),
            Location(self, 256+110, 0x308160, LocationType.Regular, "Desert Palace - Torch",
                lambda items: items.Boots),
            Location(self, 256+111, 0x1E9B6, LocationType.Regular, "Desert Palace - Map Chest"),
            Location(self, 256+112, 0x1E9C2, LocationType.Regular, "Desert Palace - Big Key Chest",
                lambda items: items.KeyDP),
            Location(self, 256+113, 0x1E9CB, LocationType.Regular, "Desert Palace - Compass Chest",
                lambda items: items.KeyDP),
            Location(self, 256+114, 0x308151, LocationType.Regular, "Desert Palace - Lanmolas",
                lambda items: (
                    items.CanLiftLight() or
                    items.CanAccessMiseryMirePortal(self.Config) and items.Mirror
                ) and items.BigKeyDP and items.KeyDP and items.CanLightTorches() and self.CanBeatBoss(items))
            ]

    def CanBeatBoss(self, items: Progression):
        return items.Sword or items.Hammer or items.Bow or \
            items.Firerod or items.Icerod or \
            items.Byrna or items.Somaria

    def CanEnter(self, items: Progression):
        return items.Book or \
            items.Mirror and items.CanLiftHeavy() and items.Flute or \
            items.CanAccessMiseryMirePortal(self.Config) and items.Mirror

    def CanComplete(self, items: Progression):
        return self.GetLocation("Desert Palace - Lanmolas").Available(items)

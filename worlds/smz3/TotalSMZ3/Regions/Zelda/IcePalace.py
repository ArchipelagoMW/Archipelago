from typing import List
from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class IcePalace(Z3Region, IReward):
    Name = "Ice Palace"
    Area = "Ice Palace"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Weight = 4
        self.RegionItems = [ ItemType.KeyIP, ItemType.BigKeyIP, ItemType.MapIP, ItemType.CompassIP]
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 256+161, 0x1E9D4, LocationType.Regular, "Ice Palace - Compass Chest"),
            Location(self, 256+162, 0x1E9E0, LocationType.Regular, "Ice Palace - Spike Room",
                lambda items: items.Hookshot or items.KeyIP >= 1 and self.CanNotWasteKeysBeforeAccessible(items, [
                    self.GetLocation("Ice Palace - Map Chest"),
                    self.GetLocation("Ice Palace - Big Key Chest")
                ])),
            Location(self, 256+163, 0x1E9DD, LocationType.Regular, "Ice Palace - Map Chest",
                lambda items: items.Hammer and items.CanLiftLight() and (
                    items.Hookshot or items.KeyIP >= 1 and self.CanNotWasteKeysBeforeAccessible(items, [
                        self.GetLocation("Ice Palace - Spike Room"),
                        self.GetLocation("Ice Palace - Big Key Chest")
                    ])
                )),
            Location(self, 256+164, 0x1E9A4, LocationType.Regular, "Ice Palace - Big Key Chest",
                lambda items: items.Hammer and items.CanLiftLight() and (
                    items.Hookshot or items.KeyIP >= 1 and self.CanNotWasteKeysBeforeAccessible(items, [
                        self.GetLocation("Ice Palace - Spike Room"),
                        self.GetLocation("Ice Palace - Map Chest")
                    ])
                )),
            Location(self, 256+165, 0x1E9E3, LocationType.Regular, "Ice Palace - Iced T Room"),
            Location(self, 256+166, 0x1E995, LocationType.Regular, "Ice Palace - Freezor Chest"),
            Location(self, 256+167, 0x1E9AA, LocationType.Regular, "Ice Palace - Big Chest",
                lambda items: items.BigKeyIP),
            Location(self, 256+168, 0x308157, LocationType.Regular, "Ice Palace - Kholdstare",
                lambda items: items.BigKeyIP and items.Hammer and items.CanLiftLight() and
                    items.KeyIP >= (1 if items.Somaria else 2))
            ]

    def CanNotWasteKeysBeforeAccessible(self, items: Progression, locations: List[Location]):
        return self.world.ForwardSearch or not items.BigKeyIP or any(l.ItemIs(ItemType.BigKeyIP, self.world) for l in locations)

    def CanEnter(self, items: Progression):
        return items.MoonPearl and items.Flippers and items.CanLiftHeavy() and items.CanMeltFreezors()

    def CanComplete(self, items: Progression):
        return self.GetLocation("Ice Palace - Kholdstare").Available(items)
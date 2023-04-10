from typing import List
from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class SwampPalace(Z3Region, IReward):
    Name = "Swamp Palace"
    Area = "Swamp Palace"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Weight = 3
        self.RegionItems = [ ItemType.KeySP, ItemType.BigKeySP, ItemType.MapSP, ItemType.CompassSP]
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 256+135, 0x1EA9D, LocationType.Regular, "Swamp Palace - Entrance")
                .Allow(lambda item, items: self.Config.Keysanity or item.Is(ItemType.KeySP, self.world)),
            Location(self, 256+136, 0x1E986, LocationType.Regular, "Swamp Palace - Map Chest",
                lambda items: items.KeySP),
            Location(self, 256+137, 0x1E989, LocationType.Regular, "Swamp Palace - Big Chest",
                lambda items: items.BigKeySP and items.KeySP and items.Hammer)
                .AlwaysAllow(lambda item, items: item.Is(ItemType.BigKeySP, self.world)),
            Location(self, 256+138, 0x1EAA0, LocationType.Regular, "Swamp Palace - Compass Chest",
                lambda items: items.KeySP and items.Hammer),
            Location(self, 256+139, 0x1EAA3, LocationType.Regular, "Swamp Palace - West Chest",
                lambda items: items.KeySP and items.Hammer),
            Location(self, 256+140, 0x1EAA6, LocationType.Regular, "Swamp Palace - Big Key Chest",
                lambda items: items.KeySP and items.Hammer),
            Location(self, 256+141, 0x1EAA9, LocationType.Regular, "Swamp Palace - Flooded Room - Left",
                lambda items: items.KeySP and items.Hammer and items.Hookshot),
            Location(self, 256+142, 0x1EAAC, LocationType.Regular, "Swamp Palace - Flooded Room - Right",
                lambda items: items.KeySP and items.Hammer and items.Hookshot),
            Location(self, 256+143, 0x1EAAF, LocationType.Regular, "Swamp Palace - Waterfall Room",
                lambda items: items.KeySP and items.Hammer and items.Hookshot),
            Location(self, 256+144, 0x308154, LocationType.Regular, "Swamp Palace - Arrghus",
                lambda items: items.KeySP and items.Hammer and items.Hookshot)
            ]

    def CanEnter(self, items: Progression):
        return items.MoonPearl and items.Mirror and items.Flippers and self.world.CanEnter("Dark World South", items)

    def CanComplete(self, items: Progression):
        return self.GetLocation("Swamp Palace - Arrghus").Available(items)

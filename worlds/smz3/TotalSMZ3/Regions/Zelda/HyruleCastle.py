from typing import List
from ...Region import Z3Region
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import ItemType

class HyruleCastle(Z3Region):
    Name = "Hyrule Castle"
    Area = "Hyrule Castle"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.RegionItems = [ ItemType.KeyHC, ItemType.MapHC]
        sphereOne = -10
        self.Locations = [
            Location(self, 256+91, 0x1EA79, LocationType.Regular, "Sanctuary").Weighted(sphereOne),
            Location(self, 256+92, 0x1EB5D, LocationType.Regular, "Sewers - Secret Room - Left",
                lambda items: items.CanLiftLight() or items.Lamp and items.KeyHC),
            Location(self, 256+93, 0x1EB60, LocationType.Regular, "Sewers - Secret Room - Middle",
                lambda items: items.CanLiftLight() or items.Lamp and items.KeyHC),
            Location(self, 256+94, 0x1EB63, LocationType.Regular, "Sewers - Secret Room - Right",
                lambda items: items.CanLiftLight() or items.Lamp and items.KeyHC),
            Location(self, 256+95, 0x1E96E, LocationType.Regular, "Sewers - Dark Cross",
                lambda items: items.Lamp),
            Location(self, 256+96, 0x1EB0C, LocationType.Regular, "Hyrule Castle - Map Chest").Weighted(sphereOne),
            Location(self, 256+97, 0x1E974, LocationType.Regular, "Hyrule Castle - Boomerang Chest",
                lambda items: items.KeyHC).Weighted(sphereOne),
            Location(self, 256+98, 0x1EB09, LocationType.Regular, "Hyrule Castle - Zelda's Cell",
                lambda items: items.KeyHC).Weighted(sphereOne),
            Location(self, 256+99, 0x5DF45, LocationType.NotInDungeon, "Link's Uncle")
                .Allow(lambda item, items: self.Config.Keysanity or not item.IsDungeonItem()).Weighted(sphereOne),
            Location(self, 256+100, 0x1E971, LocationType.NotInDungeon, "Secret Passage")
                .Allow(lambda item, items: self.Config.Keysanity or not item.IsDungeonItem()).Weighted(sphereOne),
            ]
from ....Region import Z3Region, RewardType
from ....Config import Config
from ....Location import Location, LocationType

class NorthWest(Z3Region):
    Name = "Light World North West"
    Area = "Light World"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        sphereOne = -14
        self.Locations = [
            Location(self, 256+14, 0x589B0, LocationType.Pedestal, "Master Sword Pedestal",
                lambda items: self.world.CanAcquireAll(items, RewardType.AnyPendant)),
            Location(self, 256+15, 0x308013, LocationType.Regular, "Mushroom").Weighted(sphereOne),
            Location(self, 256+16, 0x308000, LocationType.Regular, "Lost Woods Hideout").Weighted(sphereOne),
            Location(self, 256+17, 0x308001, LocationType.Regular, "Lumberjack Tree",
                lambda items: self.world.CanAcquire(items, RewardType.Agahnim) and items.Boots),
            Location(self, 256+18, 0x1EB3F, LocationType.Regular, "Pegasus Rocks",
                lambda items: items.Boots),
            Location(self, 256+19, 0x308004, LocationType.Regular, "Graveyard Ledge",
                lambda items: items.Mirror and items.MoonPearl and self.world.CanEnter("Dark World North West", items)),
            Location(self, 256+20, 0x1E97A, LocationType.Regular, "King's Tomb",
                lambda items: items.Boots and (
                    items.CanLiftHeavy() or
                    items.Mirror and items.MoonPearl and self.world.CanEnter("Dark World North West", items))),
            Location(self, 256+21, 0x1EA8E, LocationType.Regular, "Kakariko Well - Top").Weighted(sphereOne),
            Location(self, 256+22, 0x1EA91, LocationType.Regular, "Kakariko Well - Left").Weighted(sphereOne),
            Location(self, 256+23, 0x1EA94, LocationType.Regular, "Kakariko Well - Middle").Weighted(sphereOne),
            Location(self, 256+24, 0x1EA97, LocationType.Regular, "Kakariko Well - Right").Weighted(sphereOne),
            Location(self, 256+25, 0x1EA9A, LocationType.Regular, "Kakariko Well - Bottom").Weighted(sphereOne),
            Location(self, 256+26, 0x1EB0F, LocationType.Regular, "Blind's Hideout - Top").Weighted(sphereOne),
            Location(self, 256+27, 0x1EB18, LocationType.Regular, "Blind's Hideout - Far Left").Weighted(sphereOne),
            Location(self, 256+28, 0x1EB12, LocationType.Regular, "Blind's Hideout - Left").Weighted(sphereOne),
            Location(self, 256+29, 0x1EB15, LocationType.Regular, "Blind's Hideout - Right").Weighted(sphereOne),
            Location(self, 256+30, 0x1EB1B, LocationType.Regular, "Blind's Hideout - Far Right").Weighted(sphereOne),
            Location(self, 256+31, 0x5EB18, LocationType.Regular, "Bottle Merchant").Weighted(sphereOne),
            Location(self, 256+250, 0x1E9E9, LocationType.Regular, "Chicken House").Weighted(sphereOne),
            Location(self, 256+33, 0x6B9CF, LocationType.Regular, "Sick Kid",
                lambda items: items.Bottle),
            Location(self, 256+34, 0x1E9CE, LocationType.Regular, "Kakariko Tavern").Weighted(sphereOne),
            Location(self, 256+35, 0x308015, LocationType.Regular, "Magic Bat",
                lambda items: items.Powder and (items.Hammer or items.MoonPearl and items.Mirror and items.CanLiftHeavy()))
            ]

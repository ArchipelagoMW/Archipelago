from ....Region import Z3Region, RewardType
from ....Config import Config
from ....Location import Location, LocationType

class NorthEast(Z3Region):
    Name = "Light World North East"
    Area = "Light World"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        sphereOne = -10
        self.Locations = [
            Location(self, 256+36, 0x1DE1C3, LocationType.Regular, "King Zora",
                lambda items: items.CanLiftLight() or items.Flippers),
            Location(self, 256+37, 0x308149, LocationType.Regular, "Zora's Ledge",
                lambda items: items.Flippers),
            Location(self, 256+254, 0x1E9B0, LocationType.Regular, "Waterfall Fairy - Left",
                lambda items: items.Flippers),
            Location(self, 256+39, 0x1E9D1, LocationType.Regular, "Waterfall Fairy - Right",
                lambda items: items.Flippers),
            Location(self, 256+40, 0x308014, LocationType.Regular, "Potion Shop",
                lambda items: items.Mushroom),
            Location(self, 256+41, 0x1EA82, LocationType.Regular, "Sahasrahla's Hut - Left").Weighted(sphereOne),
            Location(self, 256+42, 0x1EA85, LocationType.Regular, "Sahasrahla's Hut - Middle").Weighted(sphereOne),
            Location(self, 256+43, 0x1EA88, LocationType.Regular, "Sahasrahla's Hut - Right").Weighted(sphereOne),
            Location(self, 256+44, 0x5F1FC, LocationType.Regular, "Sahasrahla",
                lambda items: self.world.CanAcquire(items, RewardType.PendantGreen))
            ]

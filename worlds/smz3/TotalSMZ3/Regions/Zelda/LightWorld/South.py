from ....Region import Z3Region
from ....Config import Config
from ....Location import Location, LocationType

class South(Z3Region):
    Name = "Light World South"
    Area = "Light World"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        sphereOne = -10
        self.Locations = [
            Location(self, 256+45, 0x308142, LocationType.Regular, "Maze Race").Weighted(sphereOne),
            Location(self, 256+240, 0x308012, LocationType.Regular, "Library",
                lambda items: items.Boots),
            Location(self, 256+241, 0x30814A, LocationType.Regular, "Flute Spot",
                lambda items: items.Shovel),
            Location(self, 256+242, 0x308003, LocationType.Regular, "South of Grove",
                lambda items: items.Mirror and self.world.CanEnter("Dark World South", items)),
            Location(self, 256+243, 0x1E9BC, LocationType.Regular, "Link's House").Weighted(sphereOne),
            Location(self, 256+244, 0x1E9F2, LocationType.Regular, "Aginah's Cave").Weighted(sphereOne),
            Location(self, 256+51, 0x1EB42, LocationType.Regular, "Mini Moldorm Cave - Far Left").Weighted(sphereOne),
            Location(self, 256+52, 0x1EB45, LocationType.Regular, "Mini Moldorm Cave - Left").Weighted(sphereOne),
            Location(self, 256+53, 0x308010, LocationType.Regular, "Mini Moldorm Cave - NPC").Weighted(sphereOne),
            Location(self, 256+54, 0x1EB48, LocationType.Regular, "Mini Moldorm Cave - Right").Weighted(sphereOne),
            Location(self, 256+251, 0x1EB4B, LocationType.Regular, "Mini Moldorm Cave - Far Right").Weighted(sphereOne),
            Location(self, 256+252, 0x308143, LocationType.Regular, "Desert Ledge",
                lambda items: self.world.CanEnter("Desert Palace", items)),
            Location(self, 256+253, 0x308005, LocationType.Regular, "Checkerboard Cave",
                lambda items: items.Mirror and (
                    items.Flute and items.CanLiftHeavy() or
                    items.CanAccessMiseryMirePortal(Config)
                ) and items.CanLiftLight()),
            Location(self, 256+58, 0x308017, LocationType.Bombos, "Bombos Tablet",
                lambda items: items.Book and items.MasterSword and items.Mirror and self.world.CanEnter("Dark World South", items)),
            Location(self, 256+59, 0x1E98C, LocationType.Regular, "Floodgate Chest").Weighted(sphereOne),
            Location(self, 256+60, 0x308145, LocationType.Regular, "Sunken Treasure").Weighted(sphereOne),
            Location(self, 256+61, 0x308144, LocationType.Regular, "Lake Hylia Island",
                lambda items: items.Flippers and items.MoonPearl and items.Mirror and (
                    self.world.CanEnter("Dark World South", items) or
                    self.world.CanEnter("Dark World North East", items))),
            Location(self, 256+62, 0x6BE7D, LocationType.Regular, "Hobo",
                lambda items: items.Flippers),
            Location(self, 256+63, 0x1EB4E, LocationType.Regular, "Ice Rod Cave").Weighted(sphereOne)
            ]
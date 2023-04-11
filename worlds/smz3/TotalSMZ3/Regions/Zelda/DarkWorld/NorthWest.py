from ....Region import Z3Region, RewardType
from ....Config import Config
from ....Location import Location, LocationType
from ....Item import Progression

class NorthWest(Z3Region):
    Name = "Dark World North West"
    Area = "Dark World"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 256+71, 0x308146, LocationType.Regular, "Bumper Cave",
                lambda items: items.CanLiftLight() and items.Cape),
            Location(self, 256+72, 0x1EDA8, LocationType.Regular, "Chest Game"),
            Location(self, 256+73, 0x1E9EF, LocationType.Regular, "C-Shaped House"),
            Location(self, 256+74, 0x1E9EC, LocationType.Regular, "Brewery"),
            Location(self, 256+75, 0x308006, LocationType.Regular, "Hammer Pegs",
                lambda items: items.CanLiftHeavy() and items.Hammer),
            Location(self, 256+76, 0x30802A, LocationType.Regular, "Blacksmith",
                lambda items: items.CanLiftHeavy()),
            Location(self, 256+77, 0x6BD68, LocationType.Regular, "Purple Chest",
                lambda items: items.CanLiftHeavy())
            ]

    def CanEnter(self, items: Progression):
        return items.MoonPearl and ((
                self.world.CanAcquire(items, RewardType.Agahnim) or
                items.CanAccessDarkWorldPortal(self.Config) and items.Flippers
            ) and items.Hookshot and (items.Flippers or items.CanLiftLight() or items.Hammer) or
            items.Hammer and items.CanLiftLight() or
            items.CanLiftHeavy())

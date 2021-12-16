from Region import Z3Region, RewardType
from Config import Config
from World import World
from Location import Location, LocationType
from Item import Progression

class NorthEast(Z3Region):
    Name = "Dark World North East"
    Area = "Dark World"

    def __init__(self, world: World, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 256+78, 0x1DE185, LocationType.Regular, "Catfish",
                lambda items: items.MoonPearl and items.CanLiftLight()),
            Location(self, 256+79, 0x308147, LocationType.Regular, "Pyramid"),
            Location(self, 256+80, 0x1E980, LocationType.Regular, "Pyramid Fairy - Left",
                lambda items: World.CanAquireAll(items, RewardType.CrystalRed) and items.MoonPearl and World.CanEnter("Dark World South", items) and
                    (items.Hammer or items.Mirror and World.CanAquire(items, RewardType.Agahnim))),
            Location(self, 256+81, 0x1E983, LocationType.Regular, "Pyramid Fairy - Right",
                lambda items: World.CanAquireAll(items, RewardType.CrystalRed) and items.MoonPearl and World.CanEnter("Dark World South", items) and
                    (items.Hammer or items.Mirror and World.CanAquire(items, RewardType.Agahnim)))
            ]

    def CanEnter(self, items: Progression):
        return World.CanAquire(items, RewardType.Agahnim) or items.MoonPearl and (
            items.Hammer and items.CanLiftLight() or
            items.CanLiftHeavy() and items.Flippers or
            items.CanAccessDarkWorldPortal(Config) and items.Flippers)

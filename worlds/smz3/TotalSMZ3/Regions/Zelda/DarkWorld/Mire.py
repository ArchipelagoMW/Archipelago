from ....Region import Z3Region
from ....Config import Config
from ....Location import Location, LocationType
from ....Item import Progression

class Mire(Z3Region):
    Name = "Dark World Mire"
    Area = "Dark World"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 256+89, 0x1EA73, LocationType.Regular, "Mire Shed - Left",
                lambda items: items.MoonPearl),
            Location(self, 256+90, 0x1EA76, LocationType.Regular, "Mire Shed - Right",
                lambda items: items.MoonPearl)
        ]

    def CanEnter(self, items: Progression):
        return items.Flute and items.CanLiftHeavy() or items.CanAccessMiseryMirePortal(Config)

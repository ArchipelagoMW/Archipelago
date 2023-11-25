from .....Region import Z3Region
from .....Config import Config
from .....Location import Location, LocationType
from .....Item import Progression

class East(Z3Region):
    Name = "Dark World Death Mountain East"
    Area = "Dark World"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 256+65, 0x1EB51, LocationType.Regular, "Hookshot Cave - Top Right",
                lambda items: items.MoonPearl and items.Hookshot),
            Location(self, 256+66, 0x1EB54, LocationType.Regular, "Hookshot Cave - Top Left",
                lambda items: items.MoonPearl and items.Hookshot),
            Location(self, 256+67, 0x1EB57, LocationType.Regular, "Hookshot Cave - Bottom Left",
                lambda items: items.MoonPearl and items.Hookshot),
            Location(self, 256+68, 0x1EB5A, LocationType.Regular, "Hookshot Cave - Bottom Right",
                lambda items: items.MoonPearl and (items.Hookshot or items.Boots)),
            Location(self, 256+69, 0x1EA7C, LocationType.Regular, "Superbunny Cave - Top",
                lambda items: items.MoonPearl),
            Location(self, 256+70, 0x1EA7F, LocationType.Regular, "Superbunny Cave - Bottom",
                lambda items: items.MoonPearl)
            ]

    def CanEnter(self, items: Progression):
        return items.CanLiftHeavy() and self.world.CanEnter("Light World Death Mountain East", items)

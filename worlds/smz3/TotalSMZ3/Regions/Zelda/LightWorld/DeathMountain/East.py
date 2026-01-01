from .....Region import Z3Region
from .....Config import Config
from .....Location import Location, LocationType
from .....Item import Progression

class East(Z3Region):
    Name = "Light World Death Mountain East"
    Area = "Death Mountain"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 256+4, 0x308141, LocationType.Regular, "Floating Island",
                lambda items: items.Mirror and items.MoonPearl and items.CanLiftHeavy()),
            Location(self, 256+5, 0x1E9BF, LocationType.Regular, "Spiral Cave"),
            Location(self, 256+6, 0x1EB39, LocationType.Regular, "Paradox Cave Upper - Left"),
            Location(self, 256+7, 0x1EB3C, LocationType.Regular, "Paradox Cave Upper - Right"),
            Location(self, 256+8, 0x1EB2A, LocationType.Regular, "Paradox Cave Lower - Far Left"),
            Location(self, 256+9, 0x1EB2D, LocationType.Regular, "Paradox Cave Lower - Left"),
            Location(self, 256+10, 0x1EB36, LocationType.Regular, "Paradox Cave Lower - Middle"),
            Location(self, 256+11, 0x1EB30, LocationType.Regular, "Paradox Cave Lower - Right"),
            Location(self, 256+12, 0x1EB33, LocationType.Regular, "Paradox Cave Lower - Far Right"),
            Location(self, 256+13, 0x1E9C5, LocationType.Regular, "Mimic Cave",
                lambda items: items.Mirror and items.KeyTR >= 2 and self.world.CanEnter("Turtle Rock", items))
            ]

    def CanEnter(self, items: Progression):
        return self.world.CanEnter("Light World Death Mountain West", items) and (
            items.Hammer and items.Mirror or
            items.Hookshot)
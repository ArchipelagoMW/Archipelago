from .....Region import Z3Region
from .....Config import Config
from .....Location import Location, LocationType
from .....Item import Progression

class West(Z3Region):
    Name = "Light World Death Mountain West"
    Area = "Death Mountain"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 256+0, 0x308016, LocationType.Ether, "Ether Tablet",
                lambda items: items.Book and items.MasterSword and (items.Mirror or items.Hammer and items.Hookshot)),
            Location(self, 256+1, 0x308140, LocationType.Regular, "Spectacle Rock",
                lambda items: items.Mirror),
            Location(self, 256+2, 0x308002, LocationType.Regular, "Spectacle Rock Cave"),
            Location(self, 256+3, 0x1EE9FA, LocationType.Regular, "Old Man",
                lambda items: items.Lamp)
            ]

    def CanEnter(self, items: Progression):
        return items.Flute or items.CanLiftLight() and items.Lamp or items.CanAccessDeathMountainPortal()

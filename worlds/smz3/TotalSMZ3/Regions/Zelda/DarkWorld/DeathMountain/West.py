from .....Region import Z3Region
from .....Config import Config
from .....Location import Location, LocationType

class West(Z3Region):
    Name = "Dark World Death Mountain West"
    Area = "Dark World"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 256+64, 0x1EA8B, LocationType.Regular, "Spike Cave",
                lambda items: items.MoonPearl and items.Hammer and items.CanLiftLight() and
                    (items.CanExtendMagic() and items.Cape or items.Byrna) and
                    self.world.CanEnter("Light World Death Mountain West", items))
            ]
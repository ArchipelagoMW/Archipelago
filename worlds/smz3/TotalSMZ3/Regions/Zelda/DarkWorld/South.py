from ....Region import Z3Region, RewardType
from ....Config import Config
from ....Location import Location, LocationType
from ....Item import Progression

class South(Z3Region):
    Name = "Dark World South"
    Area = "Dark World"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 256+82, 0x308148, LocationType.Regular, "Digging Game"),
            Location(self, 256+83, 0x6B0C7, LocationType.Regular, "Stumpy"),
            Location(self, 256+84, 0x1EB1E, LocationType.Regular, "Hype Cave - Top"),
            Location(self, 256+85, 0x1EB21, LocationType.Regular, "Hype Cave - Middle Right"),
            Location(self, 256+86, 0x1EB24, LocationType.Regular, "Hype Cave - Middle Left"),
            Location(self, 256+87, 0x1EB27, LocationType.Regular, "Hype Cave - Bottom"),
            Location(self, 256+88, 0x308011, LocationType.Regular, "Hype Cave - NPC")
            ]

    def CanEnter(self, items: Progression):
        return items.MoonPearl and ((
                self.world.CanAcquire(items, RewardType.Agahnim) or
                items.CanAccessDarkWorldPortal(self.Config) and items.Flippers
            ) and (items.Hammer or items.Hookshot and (items.Flippers or items.CanLiftLight())) or
            items.Hammer and items.CanLiftLight() or
            items.CanLiftHeavy())

from typing import List
from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class PalaceOfDarkness(Z3Region, IReward):
    Name = "Palace of Darkness"
    Area = "Dark Palace"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.RegionItems = [ ItemType.KeyPD, ItemType.BigKeyPD, ItemType.MapPD, ItemType.CompassPD]
        self.Reward = RewardType.Null
        self.Locations = [
            Location(self, 256+121, 0x1EA5B, LocationType.Regular, "Palace of Darkness - Shooter Room"),
            Location(self, 256+122, 0x1EA37, LocationType.Regular, "Palace of Darkness - Big Key Chest",
                lambda items: items.KeyPD >= (1 if self.GetLocation("Palace of Darkness - Big Key Chest").ItemIs(ItemType.KeyPD, self.world) else
                    6 if (items.Hammer and items.Bow and items.Lamp) or config.Keysanity else 5))
                .AlwaysAllow(lambda item, items: item.Is(ItemType.KeyPD, self.world) and items.KeyPD >= 5),
            Location(self, 256+123, 0x1EA49, LocationType.Regular, "Palace of Darkness - Stalfos Basement",
                lambda items: items.KeyPD >= 1 or items.Bow and items.Hammer),
            Location(self, 256+124, 0x1EA3D, LocationType.Regular, "Palace of Darkness - The Arena - Bridge",
                lambda items: items.KeyPD >= 1 or items.Bow and items.Hammer),
            Location(self, 256+125, 0x1EA3A, LocationType.Regular, "Palace of Darkness - The Arena - Ledge",
                lambda items: items.Bow),
            Location(self, 256+126, 0x1EA52, LocationType.Regular, "Palace of Darkness - Map Chest",
                lambda items: items.Bow),
            Location(self, 256+127, 0x1EA43, LocationType.Regular, "Palace of Darkness - Compass Chest",
                lambda items: items.KeyPD >= (4 if (items.Hammer and items.Bow and items.Lamp) or config.Keysanity else 3)),
            Location(self, 256+128, 0x1EA46, LocationType.Regular, "Palace of Darkness - Harmless Hellway",
                lambda items: items.KeyPD >= ((4 if (items.Hammer and items.Bow and items.Lamp) or config.Keysanity else 3) if 
                        self.GetLocation("Palace of Darkness - Harmless Hellway").ItemIs(ItemType.KeyPD, self.world) else
                        6 if (items.Hammer and items.Bow and items.Lamp) or config.Keysanity else 5))
                .AlwaysAllow(lambda item, items: item.Is(ItemType.KeyPD, self.world) and items.KeyPD >= 5),
            Location(self, 256+129, 0x1EA4C, LocationType.Regular, "Palace of Darkness - Dark Basement - Left",
                lambda items: items.Lamp and items.KeyPD >= (4 if (items.Hammer and items.Bow) or config.Keysanity else 3)),
            Location(self, 256+130, 0x1EA4F, LocationType.Regular, "Palace of Darkness - Dark Basement - Right",
                lambda items: items.Lamp and items.KeyPD >= (4 if (items.Hammer and items.Bow) or config.Keysanity else 3)),
            Location(self, 256+131, 0x1EA55, LocationType.Regular, "Palace of Darkness - Dark Maze - Top",
                lambda items: items.Lamp and items.KeyPD >= (6 if (items.Hammer and items.Bow) or config.Keysanity else 5)),
            Location(self, 256+132, 0x1EA58, LocationType.Regular, "Palace of Darkness - Dark Maze - Bottom",
                lambda items: items.Lamp and items.KeyPD >= (6 if(items.Hammer and items.Bow) or config.Keysanity else 5)),
            Location(self, 256+133, 0x1EA40, LocationType.Regular, "Palace of Darkness - Big Chest",
                lambda items: items.BigKeyPD and items.Lamp and items.KeyPD >= (6 if (items.Hammer and items.Bow) or config.Keysanity else 5)),
            Location(self, 256+134, 0x308153, LocationType.Regular, "Palace of Darkness - Helmasaur King",
                lambda items: items.Lamp and items.Hammer and items.Bow and items.BigKeyPD and items.KeyPD >= 6),
            ]

    def CanEnter(self, items: Progression):
        return items.MoonPearl and self.world.CanEnter("Dark World North East", items)

    def CanComplete(self, items: Progression):
        return self.GetLocation("Palace of Darkness - Helmasaur King").Available(items)

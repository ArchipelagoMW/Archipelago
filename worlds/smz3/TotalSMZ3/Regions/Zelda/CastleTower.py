from ...Region import Z3Region, RewardType, IReward
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class CastleTower(Z3Region, IReward):
    Name = "Castle Tower"
    Area = "Castle Tower"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Reward = RewardType.Agahnim
        self.RegionItems = [ItemType.KeyCT]
        self.Locations = [
            Location(self, 256+101, 0x1EAB5, LocationType.Regular, "Castle Tower - Foyer"),
            Location(self, 256+102, 0x1EAB2, LocationType.Regular, "Castle Tower - Dark Maze",
                lambda items: items.Lamp and items.KeyCT >= 1)
            ]

    def CanEnter(self, items: Progression):
        return items.CanKillManyEnemies() and (items.Cape or items.MasterSword)

    def CanComplete(self, items: Progression):
        return self.CanEnter(items) and items.Lamp and items.KeyCT >= 2 and items.Sword


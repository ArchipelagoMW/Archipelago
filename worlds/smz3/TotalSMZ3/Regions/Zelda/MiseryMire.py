from typing import List
from ...Region import Z3Region, RewardType, IReward, IMedallionAccess
from ...Config import Config
from ...Location import Location, LocationType
from ...Item import Progression, ItemType

class MiseryMire(Z3Region, IReward, IMedallionAccess):
    Name = "Misery Mire"
    Area = "Misery Mire"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Weight = 2
        self.RegionItems = [ ItemType.KeyMM, ItemType.BigKeyMM, ItemType.MapMM, ItemType.CompassMM]
        self.Reward = RewardType.Null
        self.Medallion = None
        self.Locations = [
            Location(self, 256+169, 0x1EA5E, LocationType.Regular, "Misery Mire - Main Lobby",
                lambda items: items.BigKeyMM or items.KeyMM >= 1),
            Location(self, 256+170, 0x1EA6A, LocationType.Regular, "Misery Mire - Map Chest",
                lambda items: items.BigKeyMM or items.KeyMM >= 1),
            Location(self, 256+171, 0x1EA61, LocationType.Regular, "Misery Mire - Bridge Chest"),
            Location(self, 256+172, 0x1E9DA, LocationType.Regular, "Misery Mire - Spike Chest"),
            Location(self, 256+173, 0x1EA64, LocationType.Regular, "Misery Mire - Compass Chest",
                lambda items: items.CanLightTorches() and
                    items.KeyMM >= (2 if self.GetLocation("Misery Mire - Big Key Chest").ItemIs(ItemType.BigKeyMM, self.world) else 3)),
            Location(self, 256+174, 0x1EA6D, LocationType.Regular, "Misery Mire - Big Key Chest",
                lambda items: items.CanLightTorches() and
                    items.KeyMM >= (2 if self.GetLocation("Misery Mire - Compass Chest").ItemIs(ItemType.BigKeyMM, self.world) else 3)),
            Location(self, 256+175, 0x1EA67, LocationType.Regular, "Misery Mire - Big Chest",
                lambda items: items.BigKeyMM),
            Location(self, 256+176, 0x308158, LocationType.Regular, "Misery Mire - Vitreous",
                lambda items: items.BigKeyMM and items.Lamp and items.Somaria)
            ]

    # // Need "CanKillManyEnemies" if implementing swordless
    def CanEnter(self, items: Progression):
        from ...WorldState import Medallion
        return (items.Bombos if self.Medallion == Medallion.Bombos else (
                    items.Ether if self.Medallion == Medallion.Ether else items.Quake)) and items.Sword and \
            items.MoonPearl and (items.Boots or items.Hookshot) and \
            self.world.CanEnter("Dark World Mire", items)

    def CanComplete(self, items: Progression):
        return self.GetLocation("Misery Mire - Vitreous").Available(items)
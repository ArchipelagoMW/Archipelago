from ....Region import SMRegion, IReward, RewardType
from ....Config import Config
from ....Location import Location, LocationType
from ....Item import Progression

class Kraid(SMRegion, IReward):
    Name = "Brinstar Kraid"
    Area = "Brinstar"

    Reward = RewardType.Null

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 43, 0x8F899C, LocationType.Hidden, "Energy Tank, Kraid", lambda items: items.CardBrinstarBoss),
            Location(self, 48, 0x8F8ACA, LocationType.Chozo, "Varia Suit", lambda items: items.CardBrinstarBoss),
            Location(self, 44, 0x8F89EC, LocationType.Hidden, "Missile (Kraid)", lambda items: items.CanUsePowerBombs())
        ]

    def CanEnter(self, items:Progression):
        return (items.CanDestroyBombWalls() or items.SpeedBooster or items.CanAccessNorfairUpperPortal()) and \
            items.Super and items.CanPassBombPassages()

    def CanComplete(self, items:Progression):
        return self.GetLocation("Varia Suit").Available(items)

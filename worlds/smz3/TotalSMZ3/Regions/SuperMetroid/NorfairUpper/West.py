from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class West(SMRegion):
    Name = "Norfair Upper West"
    Area = "Norfair Upper"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 49, 0x8F8AE4, LocationType.Hidden, "Missile (lava room)",
                lambda items: items.Varia and (
                        items.CanOpenRedDoors() and (items.CanFly() or items.HiJump or items.SpeedBooster) or
                        self.world.CanEnter("Norfair Upper East", items) and items.CardNorfairL2
                    ) and items.Morph if self.Logic == SMLogic.Normal else \
                lambda items: items.CanHellRun() and (
                        items.CanOpenRedDoors() and (
                            items.CanFly() or items.HiJump or items.SpeedBooster or
                            items.CanSpringBallJump() or items.Varia and items.Ice
                        ) or
                        self.world.CanEnter("Norfair Upper East", items) and items.CardNorfairL2
                    ) and items.Morph),
            Location(self, 50, 0x8F8B24, LocationType.Chozo, "Ice Beam",
                lambda items: (items.CardNorfairL1 if config.Keysanity else items.Super) and items.CanPassBombPassages() and items.Varia and items.SpeedBooster if self.Logic == SMLogic.Normal else \
                lambda items: (items.CardNorfairL1 if config.Keysanity else items.Super) and items.Morph and (items.Varia or items.HasEnergyReserves(3))),
            Location(self, 51, 0x8F8B46, LocationType.Hidden, "Missile (below Ice Beam)", 
                lambda items: (items.CardNorfairL1 if config.Keysanity else items.Super) and items.CanUsePowerBombs() and items.Varia and items.SpeedBooster if self.Logic == SMLogic.Normal else \
                lambda items: 
                    (items.CardNorfairL1 if config.Keysanity else items.Super) and items.CanUsePowerBombs() and (items.Varia or items.HasEnergyReserves(3)) or
                    (items.Missile or items.Super or items.Wave) and items.Varia and items.SpeedBooster and # /* Blue Gate */
                    # /* Access to Croc's room to get spark */
                    (items.CardNorfairBoss if config.Keysanity else items.Super) and items.CardNorfairL1),
            Location(self, 53, 0x8F8BAC, LocationType.Chozo, "Hi-Jump Boots", 
                lambda items: items.CanOpenRedDoors() and items.CanPassBombPassages()),
            Location(self, 55, 0x8F8BE6, LocationType.Visible, "Missile (Hi-Jump Boots)",
                lambda items: items.CanOpenRedDoors() and items.Morph),
            Location(self, 56, 0x8F8BEC, LocationType.Visible, "Energy Tank (Hi-Jump Boots)", 
                lambda items: items.CanOpenRedDoors())
            ]

    def CanEnter(self, items:Progression):
        return (items.CanDestroyBombWalls() or items.SpeedBooster) and items.Super and items.Morph or items.CanAccessNorfairUpperPortal()
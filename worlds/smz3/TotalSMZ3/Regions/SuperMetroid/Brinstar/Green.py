from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class Green(SMRegion):
    Name = "Brinstar Green"
    Area = "Brinstar"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Weight = -6
        self.Locations = [
            Location(self, 13, 0x8F84AC, LocationType.Chozo, "Power Bomb (green Brinstar bottom)", 
                lambda items: items.CardBrinstarL2 and items.CanUsePowerBombs()),
            Location(self, 15, 0x8F8518, LocationType.Visible, "Missile (green Brinstar below super missile)", 
                lambda items: items.CanPassBombPassages() and items.CanOpenRedDoors()),
            Location(self, 16, 0x8F851E, LocationType.Visible, "Super Missile (green Brinstar top)",
                lambda items: items.CanOpenRedDoors() and items.SpeedBooster if self.Logic == SMLogic.Normal else \
                lambda items: items.CanOpenRedDoors() and (items.Morph or items.SpeedBooster)),
            Location(self, 17, 0x8F852C, LocationType.Chozo, "Reserve Tank, Brinstar", 
                lambda items: items.CanOpenRedDoors() and items.SpeedBooster if self.Logic == SMLogic.Normal else \
                lambda items: items.CanOpenRedDoors() and (items.Morph or items.SpeedBooster)),
            Location(self, 18, 0x8F8532, LocationType.Hidden, "Missile (green Brinstar behind missile)", 
                lambda items: items.SpeedBooster and items.CanPassBombPassages() and items.CanOpenRedDoors() if self.Logic == SMLogic.Normal else \
                lambda items: (items.CanPassBombPassages() or items.Morph and items.ScrewAttack) and items.CanOpenRedDoors()),
            Location(self, 19, 0x8F8538, LocationType.Visible, "Missile (green Brinstar behind reserve tank)",
                lambda items: items.SpeedBooster and items.CanOpenRedDoors() and items.Morph if self.Logic == SMLogic.Normal else \
                lambda items: items.CanOpenRedDoors() and items.Morph),
            Location(self, 30, 0x8F87C2, LocationType.Visible, "Energy Tank, Etecoons", 
                lambda items: items.CardBrinstarL2 and items.CanUsePowerBombs()),
            Location(self, 31, 0x8F87D0, LocationType.Visible, "Super Missile (green Brinstar bottom)",
                lambda items: items.CardBrinstarL2 and items.CanUsePowerBombs() and items.Super)
        ]

    def CanEnter(self, items: Progression):
        return items.CanDestroyBombWalls() or items.SpeedBooster

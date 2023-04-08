from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class Red(SMRegion):
    Name = "Brinstar Red"
    Area = "Brinstar"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 38, 0x8F8876, LocationType.Chozo, "X-Ray Scope",
                lambda items: items.CanUsePowerBombs() and items.CanOpenRedDoors() and (items.Grapple or items.SpaceJump) if self.Logic == SMLogic.Normal else \
                lambda items: items.CanUsePowerBombs() and items.CanOpenRedDoors() and (
                    items.Grapple or items.SpaceJump or
                    (items.CanIbj() or items.HiJump and items.SpeedBooster or items.CanSpringBallJump()) and
                        (items.Varia and items.HasEnergyReserves(3) or items.HasEnergyReserves(5)))),
            Location(self, 39, 0x8F88CA, LocationType.Visible, "Power Bomb (red Brinstar sidehopper room)",
                lambda items: items.CanUsePowerBombs() and items.Super),
            Location(self, 40, 0x8F890E, LocationType.Chozo, "Power Bomb (red Brinstar spike room)",
                lambda items: (items.CanUsePowerBombs() or items.Ice) and items.Super if self.Logic == SMLogic.Normal else \
                lambda items: items.Super),
            Location(self, 41, 0x8F8914, LocationType.Visible, "Missile (red Brinstar spike room)",
                lambda items: items.CanUsePowerBombs() and items.Super),
            Location(self, 42, 0x8F896E, LocationType.Chozo, "Spazer", 
                lambda items: items.CanPassBombPassages() and items.Super)
        ]

    def CanEnter(self, items: Progression):
        if self.Logic == SMLogic.Normal:
            return (items.CanDestroyBombWalls() or items.SpeedBooster) and items.Super and items.Morph or \
                items.CanAccessNorfairUpperPortal() and (items.Ice or items.HiJump or items.SpaceJump)
        else:
            return (items.CanDestroyBombWalls() or items.SpeedBooster) and items.Super and items.Morph or \
                items.CanAccessNorfairUpperPortal() and (items.Ice or items.CanSpringBallJump() or items.HiJump or items.CanFly())
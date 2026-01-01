from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class Pink(SMRegion):
    Name = "Brinstar Pink"
    Area = "Brinstar"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Weight = -4
        self.Locations = [
            Location(self, 14, 0x8F84E4, LocationType.Chozo, "Super Missile (pink Brinstar)", 
                lambda items: items.CardBrinstarBoss and items.CanPassBombPassages() and items.Super if self.Logic == SMLogic.Normal else \
                lambda items: (items.CardBrinstarBoss or items.CardBrinstarL2) and items.CanPassBombPassages() and items.Super),
            Location(self, 21, 0x8F8608, LocationType.Visible, "Missile (pink Brinstar top)"),
            Location(self, 22, 0x8F860E, LocationType.Visible, "Missile (pink Brinstar bottom)"),
            Location(self, 23, 0x8F8614, LocationType.Chozo, "Charge Beam", 
                lambda items: items.CanPassBombPassages()),
            Location(self, 24, 0x8F865C, LocationType.Visible, "Power Bomb (pink Brinstar)", 
                lambda items: items.CanUsePowerBombs() and items.Super and items.HasEnergyReserves(1) if self.Logic == SMLogic.Normal else \
                lambda items: items.CanUsePowerBombs() and items.Super),
            Location(self, 25, 0x8F8676, LocationType.Visible, "Missile (green Brinstar pipe)", 
                lambda items: items.Morph and (items.PowerBomb or items.Super or items.CanAccessNorfairUpperPortal())),
            Location(self, 33, 0x8F87FA, LocationType.Visible, "Energy Tank, Waterway", 
                lambda items: items.CanUsePowerBombs() and items.CanOpenRedDoors() and items.SpeedBooster and (items.HasEnergyReserves(1) or items.Gravity)),
            Location(self, 35, 0x8F8824, LocationType.Visible, "Energy Tank, Brinstar Gate", 
                lambda items: items.CardBrinstarL2 and items.CanUsePowerBombs() and items.Wave and items.HasEnergyReserves(1) if self.Logic == SMLogic.Normal else \
                lambda items: items.CardBrinstarL2 and items.CanUsePowerBombs() and (items.Wave or items.Super))
        ]


    def CanEnter(self, items: Progression):
        if self.Logic == SMLogic.Normal:
            return items.CanOpenRedDoors() and (items.CanDestroyBombWalls() or items.SpeedBooster) or \
            items.CanUsePowerBombs() or \
            items.CanAccessNorfairUpperPortal() and items.Morph and items.Wave and \
                (items.Ice or items.HiJump or items.SpaceJump)
        else:
            return items.CanOpenRedDoors() and (items.CanDestroyBombWalls() or items.SpeedBooster) or \
                items.CanUsePowerBombs() or \
                items.CanAccessNorfairUpperPortal() and items.Morph and (items.Missile or items.Super or items.Wave ) and \
                    (items.Ice or items.HiJump or items.CanSpringBallJump() or items.CanFly())

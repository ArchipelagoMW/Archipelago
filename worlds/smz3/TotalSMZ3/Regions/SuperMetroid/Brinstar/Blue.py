from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType

class Blue(SMRegion):
    Name = "Brinstar Blue"
    Area = "Brinstar"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 26, 0x8F86EC, LocationType.Visible, "Morphing Ball"),
            Location(self, 27, 0x8F874C, LocationType.Visible, "Power Bomb (blue Brinstar)",
                lambda items: items.CanUsePowerBombs()),
            Location(self, 28, 0x8F8798, LocationType.Visible, "Missile (blue Brinstar middle)", 
                lambda items: items.CardBrinstarL1 and items.Morph),
            Location(self, 29, 0x8F879E, LocationType.Hidden, "Energy Tank, Brinstar Ceiling",
                lambda items: items.CardBrinstarL1 and (items.CanFly() or items.HiJump or items.SpeedBooster or items.Ice) if self.Logic == SMLogic.Normal else \
                lambda items: items.CardBrinstarL1),
            Location(self, 34, 0x8F8802, LocationType.Chozo, "Missile (blue Brinstar bottom)", 
                lambda items: items.Morph),
            Location(self, 36, 0x8F8836, LocationType.Visible, "Missile (blue Brinstar top)", 
                lambda items: items.CardBrinstarL1 and items.CanUsePowerBombs()),
            Location(self, 37, 0x8F883C, LocationType.Hidden, "Missile (blue Brinstar behind missile)", 
                lambda items: items.CardBrinstarL1 and items.CanUsePowerBombs())
            ]
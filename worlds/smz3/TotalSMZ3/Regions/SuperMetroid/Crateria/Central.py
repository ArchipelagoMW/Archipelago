from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType

class Central(SMRegion):
    Name = "Crateria Central"
    Area = "Crateria"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 0, 0x8F81CC, LocationType.Visible, "Power Bomb (Crateria surface)",
                lambda items: (items.CardCrateriaL1 if config.Keysanity else items.CanUsePowerBombs()) and (items.SpeedBooster or items.CanFly())),
            Location(self, 12, 0x8F8486, LocationType.Visible, "Missile (Crateria middle)",
                lambda items: items.CanPassBombPassages()),
            Location(self, 6, 0x8F83EE, LocationType.Visible, "Missile (Crateria bottom)",
                lambda items: items.CanDestroyBombWalls()),
            Location(self, 11, 0x8F8478, LocationType.Visible, "Super Missile (Crateria)", 
                lambda items: items.CanUsePowerBombs() and items.HasEnergyReserves(2) and items.SpeedBooster),
            Location(self, 7, 0x8F8404, LocationType.Chozo, "Bombs",
                lambda items: (items.CardCrateriaBoss if config.Keysanity else items.CanOpenRedDoors()) and items.CanPassBombPassages() if self.Logic == SMLogic.Normal else \
                lambda items: (items.CardCrateriaBoss if config.Keysanity else items.CanOpenRedDoors()) and items.Morph)
            ]

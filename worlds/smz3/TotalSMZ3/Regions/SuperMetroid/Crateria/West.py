from ....Region import SMRegion
from ....Config import Config, SMLogic
from ....Location import Location, LocationType
from ....Item import Progression

class West(SMRegion):
    Name = "Crateria West"
    Area = "Crateria"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Locations = [
            Location(self, 8, 0x8F8432, LocationType.Visible, "Energy Tank, Terminator"),
            Location(self, 5, 0x8F8264, LocationType.Visible, "Energy Tank, Gauntlet",
                lambda items: self.CanEnterAndLeaveGauntlet(items) and items.HasEnergyReserves(1) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanEnterAndLeaveGauntlet(items)),
            Location(self, 9, 0x8F8464, LocationType.Visible, "Missile (Crateria gauntlet right)",
                lambda items: self.CanEnterAndLeaveGauntlet(items) and items.CanPassBombPassages() and items.HasEnergyReserves(2) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanEnterAndLeaveGauntlet(items) and items.CanPassBombPassages()),
            Location(self, 10, 0x8F846A, LocationType.Visible, "Missile (Crateria gauntlet left)",
                lambda items: self.CanEnterAndLeaveGauntlet(items) and items.CanPassBombPassages() and items.HasEnergyReserves(2) if self.Logic == SMLogic.Normal else \
                lambda items: self.CanEnterAndLeaveGauntlet(items) and items.CanPassBombPassages())
        ]

    def CanEnter(self, items: Progression):
        return items.CanDestroyBombWalls() or items.SpeedBooster

    def CanEnterAndLeaveGauntlet(self, items: Progression):
        if self.Logic == SMLogic.Normal:
            return items.CardCrateriaL1 and items.Morph and (items.CanFly() or items.SpeedBooster) and (
                    items.CanIbj() or
                    items.CanUsePowerBombs() and items.TwoPowerBombs or
                    items.ScrewAttack)
        else:
            return items.CardCrateriaL1 and (
                    items.Morph and (items.Bombs or items.TwoPowerBombs) or
                    items.ScrewAttack or
                    items.SpeedBooster and items.CanUsePowerBombs() and items.HasEnergyReserves(2))
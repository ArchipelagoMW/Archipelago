from BaseClasses import Region, Location, Entrance, Item, ItemClassification


class SoulBlazerItem(Item):  # or from Items import MyGameItem
    game = "Soul Blazer"  # name of the game/world this item is from

class SoulBlazerItemData():
    id: int
    """Internal item ID"""
    operand: int
    """Either Gems/Exp Quantity or Lair ID"""

    @property
    def operand_bcd(self) -> int:
        """Converts operand to/from SNES BCD"""
        bcd = self.operand % 10
        remainder = self.operand // 10
        digit = 1

        while remainder != 0:
            bcd += (remainder % 10) * (0x10**digit)
            remainder // 10
            digit += 1

        return bcd
    
    @operand_bcd.setter
    def operand_bcd(self, bcd: int):
        decimal = bcd % 0x10
        remainder = bcd // 0x10
        digit = 1

        while remainder != 0:
            decimal += (remainder % 10) * (10**digit)
            remainder // 0x10
            digit += 1

        operand = decimal
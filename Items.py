from BaseClasses import Item
import random


class Bow(Item):

    def __init__(self):
        super(Bow, self).__init__('Bow', True, code=0x0B)


class Book(Item):

    def __init__(self):
        super(Book, self).__init__('Book of Mudora', True, code=0x1D)


class Hammer(Item):

    def __init__(self):
        super(Hammer, self).__init__('Hammer', True, code=0x09)


class Hookshot(Item):

    def __init__(self):
        super(Hookshot, self).__init__('Hookshot', True, code=0x0A)


class Mirror(Item):

    def __init__(self):
        super(Mirror, self).__init__('Magic Mirror', True, code=0x1A)


class Ocarina(Item):
    def __init__(self):
        super(Ocarina, self).__init__('Ocarina', True, code=0x14)


class Boots(Item):
    def __init__(self):
        super(Boots, self).__init__('Pegasus Boots', True, code=0x4B)


class Glove(Item):
    def __init__(self):
        super(Glove, self).__init__('Power Glove', True, code=0x1B)


class Cape(Item):
    def __init__(self):
        super(Cape, self).__init__('Cape', True, code=0x19)


class Mushroom(Item):
    def __init__(self):
        super(Mushroom, self).__init__('Mushroom', True, code=0x29)


class Shovel(Item):
    def __init__(self):
        super(Shovel, self).__init__('Shovel', True, code=0x13)


class Lamp(Item):
    def __init__(self):
        super(Lamp, self).__init__('Lamp', True, code=0x12)


class Powder(Item):
    def __init__(self):
        super(Powder, self).__init__('Magic Powder', True, code=0x0D)


class Pearl(Item):
    def __init__(self):
        super(Pearl, self).__init__('Moon Pearl', True, code=0x1F)


class Somaria(Item):
    def __init__(self):
        super(Somaria, self).__init__('Cane of Somaria', True, code=0x15)


class FireRod(Item):
    def __init__(self):
        super(FireRod, self).__init__('Fire Rod', True, code=0x07)


class Flippers(Item):
    def __init__(self):
        super(Flippers, self).__init__('Flippers', True, code=0x1E)


class IceRod(Item):
    def __init__(self):
        super(IceRod, self).__init__('Ice Rod', True, code=0x08)


class Mitts(Item):
    def __init__(self):
        super(Mitts, self).__init__("Titans Mitts", True, code=0x1C)


class Ether(Item):
    def __init__(self):
        super(Ether, self).__init__('Ether', True, code=0x10)


class Bombos(Item):
    def __init__(self):
        super(Bombos, self).__init__('Bombos', True, code=0x0F)


class Quake(Item):
    def __init__(self):
        super(Quake, self).__init__('Quake', True, code=0x11)


class Bottle(Item):
    def __init__(self):
        super(Bottle, self).__init__('Bottle', True, code=[0x16, 0x2B, 0x2C, 0x2D, 0x3C, 0x3D, 0x48][random.randint(0, 6)])


class MasterSword(Item):
    def __init__(self):
        super(MasterSword, self).__init__('Master Sword', True, code=0x50)


class TemperedSword(Item):
    def __init__(self):
        super(TemperedSword, self).__init__('Tempered Sword', True, code=0x02)


class FighterSword(Item):
    def __init__(self):
        super(FighterSword, self).__init__('Fighter Sword', True, code=0x49)


class GoldenSword(Item):
    def __init__(self):
        super(GoldenSword, self).__init__('GoldenSword', True, code=0x03)


class ProgressiveSword(Item):
    def __init__(self):
        super(ProgressiveSword, self).__init__('Progressive Sword', True, code=0x5E)
        

class ProgressiveGlove(Item):
    def __init__(self):
        super(ProgressiveGlove, self).__init__('Progressive Glove', True, code=0x61)
        
        
class SilverArrows(Item):
    def __init__(self):
        super(SilverArrows, self).__init__('Silver Arrows', True, code=0x58)


class GreenPendant(Item):
    def __init__(self):
        super(GreenPendant, self).__init__('Green Pendant', True, code=[0x04, 0x38, 0x60, 0x00, 0x69, 0x01])


class RedPendant(Item):
    def __init__(self):
        super(RedPendant, self).__init__('Red Pendant', True, code=[0x02, 0x34, 0x60, 0x00, 0x69, 0x02])


class BluePendant(Item):
    def __init__(self):
        super(BluePendant, self).__init__('Blue Pendant', True, code=[0x01, 0x32, 0x60, 0x00, 0x69, 0x03])


class Triforce(Item):
    def __init__(self):
        super(Triforce, self).__init__('Triforce', True, code=0x6A)


class Crystal1(Item):
    def __init__(self):
        super(Crystal1, self).__init__('Crystal 1', True, code=[0x02, 0x34, 0x64, 0x40, 0x7F, 0x06])


class Crystal2(Item):
    def __init__(self):
        super(Crystal2, self).__init__('Crystal 2', True, code=[0x10, 0x34, 0x64, 0x40, 0x79, 0x06])


class Crystal3(Item):
    def __init__(self):
        super(Crystal3, self).__init__('Crystal 3', True, code=[0x40, 0x34, 0x64, 0x40, 0x6C, 0x06])


class Crystal4(Item):
    def __init__(self):
        super(Crystal4, self).__init__('Crystal 4', True, code=[0x20, 0x34, 0x64, 0x40, 0x6D, 0x06])


class Crystal5(Item):
    def __init__(self):
        super(Crystal5, self).__init__('Crystal 5', True, code=[0x04, 0x34, 0x64, 0x40, 0x6E, 0x06])


class Crystal6(Item):
    def __init__(self):
        super(Crystal6, self).__init__('Crystal 6', True, code=[0x01, 0x34, 0x64, 0x40, 0x6F, 0x06])


class Crystal7(Item):
    def __init__(self):
        super(Crystal7, self).__init__('Crystal 7', True, code=[0x08, 0x34, 0x64, 0x40, 0x7C, 0x06])


class SingleArrow(Item):
    def __init__(self):
        super(SingleArrow, self).__init__('Single Arrow', False, code=0x43)


class Arrows10(Item):
    def __init__(self):
        super(Arrows10, self).__init__('Arrows (10)', False, code=0x44)


class ArrowUpgrade10(Item):
    def __init__(self):
        super(ArrowUpgrade10, self).__init__('Arrow Upgrade (+10)', False, code=0x54)


class ArrowUpgrade5(Item):
    def __init__(self):
        super(ArrowUpgrade5, self).__init__('Arrow Upgrade (+5)', False, code=0x53)


class SingleBomb(Item):
    def __init__(self):
        super(SingleBomb, self).__init__('Single Bomb', False, code=0x27)


class Bombs3(Item):
    def __init__(self):
        super(Bombs3, self).__init__('Bombs (3)', False, code=0x28)


class BombUpgrade10(Item):
    def __init__(self):
        super(BombUpgrade10, self).__init__('Bomb Upgrade (+10)', False, code=0x52)


class BombUpgrade5(Item):
    def __init__(self):
        super(BombUpgrade5, self).__init__('Bomb Upgrade (+5)', False, code=0x51)


class BlueMail(Item):
    def __init__(self):
        super(BlueMail, self).__init__('Blue Mail', False, code=0x22)


class RedMail(Item):
    def __init__(self):
        super(RedMail, self).__init__('Red Mail', False, code=0x23)


class ProgressiveArmor(Item):
    def __init__(self):
        super(ProgressiveArmor, self).__init__('Progressive Armor', False, code=0x60)


class BlueBoomerang(Item):
    def __init__(self):
        super(BlueBoomerang, self).__init__('Blue Boomerang', False, code=0x0C)


class RedBoomerang(Item):
    def __init__(self):
        super(RedBoomerang, self).__init__('Red Boomerang', False, code=0x2A)


class BlueShield(Item):
    def __init__(self):
        super(BlueShield, self).__init__('Blue Shield', False, code=0x04)


class RedShield(Item):
    def __init__(self):
        super(RedShield, self).__init__('Red Shield', False, code=0x05)


class MirrorShield(Item):
    def __init__(self):
        super(MirrorShield, self).__init__('Mirror Shield', False, code=0x06)


class ProgressiveShield(Item):
    def __init__(self):
        super(ProgressiveShield, self).__init__('Progressive Shield', False, code=0x5F)


class Net(Item):
    def __init__(self):
        super(Net, self).__init__('Bug Catching Net', False, code=0x21)


class Byrna(Item):
    def __init__(self):
        super(Byrna, self).__init__('Cane of Byrna', False, code=0x18)


class HeartContainer(Item):
    def __init__(self):
        super(HeartContainer, self).__init__('Boss Heart Container', False, code=0x3E)


class SancHeart(Item):
    def __init__(self):
        super(SancHeart, self).__init__('Sanctuary Heart Container', False, code=0x3F)


class PieceOfHeart(Item):
    def __init__(self):
        super(PieceOfHeart, self).__init__('Piece of Heart', False, code=0x17)


class Rupee(Item):
    def __init__(self):
        super(Rupee, self).__init__('Rupee (1)', False, code=0x34)


class Rupees5(Item):
    def __init__(self):
        super(Rupees5, self).__init__('Rupees (5)', False, code=0x35)


class Rupees20(Item):
    def __init__(self):
        super(Rupees20, self).__init__('Rupees (20)', False, code=0x36)


class Rupees50(Item):
    def __init__(self):
        super(Rupees50, self).__init__('Rupees (50)', False, code=0x41)


class Rupees100(Item):
    def __init__(self):
        super(Rupees100, self).__init__('Rupees (100)', False, code=0x40)


class Rupees300(Item):
    def __init__(self):
        super(Rupees300, self).__init__('Rupees (300)', False, code=0x46)


class HalfMagic(Item):
    def __init__(self):
        super(HalfMagic, self).__init__('Magic Upgrade (1/2)', True, code=0x4E)  # can be required to beat mothula in an open seed in very very rare circumstance


class QuarterMagic(Item):
    def __init__(self):
        super(QuarterMagic, self).__init__('Magic Upgrade (1/4)', True, code=0x4F)  # can be required to beat mothula in an open seed in very very rare circumstance


# ToDo Use dungeons specific items once they work correctly

class EPSmallKey(Item):
    def __init__(self):
        super(EPSmallKey, self).__init__('Small Key (Eastern Palace)', False, True, code=0x24)


class EPBigKey(Item):
    def __init__(self):
        super(EPBigKey, self).__init__('Big Key (Eastern Palace)', False, True, code=0x32)
  
        
class EPCompass(Item):
    def __init__(self):
        super(EPCompass, self).__init__('Compass (Eastern Palace)', False, code=0x25)
  
        
class EPMap(Item):
    def __init__(self):
        super(EPMap, self).__init__('Map (Eastern Palace)', False, code=0x33)


class DPSmallKey(Item):
    def __init__(self):
        super(DPSmallKey, self).__init__('Small Key (Desert Palace)', False, True, code=0x24)


class DPBigKey(Item):
    def __init__(self):
        super(DPBigKey, self).__init__('Big Key (Desert Palace)', False, True, code=0x32)


class DPCompass(Item):
    def __init__(self):
        super(DPCompass, self).__init__('Compass (Desert Palace)', False, code=0x25)


class DPMap(Item):
    def __init__(self):
        super(DPMap, self).__init__('Map (Desert Palace)', False, code=0x33)


class THSmallKey(Item):
    def __init__(self):
        super(THSmallKey, self).__init__('Small Key (Tower of Hera)', False, True, code=0x24)


class THBigKey(Item):
    def __init__(self):
        super(THBigKey, self).__init__('Big Key (Tower of Hera)', False, True, code=0x32)


class THCompass(Item):
    def __init__(self):
        super(THCompass, self).__init__('Compass (Tower of Hera)', False, code=0x25)


class THMap(Item):
    def __init__(self):
        super(THMap, self).__init__('Map (Tower of Hera)', False, code=0x33)


class ESSmallKey(Item):
    def __init__(self):
        super(ESSmallKey, self).__init__('Small Key (Escape)', False, True, code=0x24)


class ESBigKey(Item):
    def __init__(self):
        super(ESBigKey, self).__init__('Big Key (Escape)', False, True, code=0x32)


class ESMap(Item):
    def __init__(self):
        super(ESMap, self).__init__('Map (Escape)', False, code=0x33)


class ATSmallKey(Item):
    def __init__(self):
        super(ATSmallKey, self).__init__('Small Key (Agahnims Tower)', False, True, code=0x24)


class PDSmallKey(Item):
    def __init__(self):
        super(PDSmallKey, self).__init__('Small Key (Palace of Darkness)', False, True, code=0x24)


class PDBigKey(Item):
    def __init__(self):
        super(PDBigKey, self).__init__('Big Key (Palace of Darkness)', False, True, code=0x32)


class PDCompass(Item):
    def __init__(self):
        super(PDCompass, self).__init__('Compass (Palace of Darkness)', False, code=0x25)


class PDMap(Item):
    def __init__(self):
        super(PDMap, self).__init__('Map (Palace of Darkness)', False, code=0x33)


class TTSmallKey(Item):
    def __init__(self):
        super(TTSmallKey, self).__init__('Small Key (Thieves Town)', False, True, code=0x24)


class TTBigKey(Item):
    def __init__(self):
        super(TTBigKey, self).__init__('Big Key (Thieves Town)', False, True, code=0x32)


class TTCompass(Item):
    def __init__(self):
        super(TTCompass, self).__init__('Compass (Thieves Town)', False, code=0x25)


class TTMap(Item):
    def __init__(self):
        super(TTMap, self).__init__('Map (Thieves Town)', False, code=0x33)


class SWSmallKey(Item):
    def __init__(self):
        super(SWSmallKey, self).__init__('Small Key (Skull Woods)', False, True, code=0x24)


class SWBigKey(Item):
    def __init__(self):
        super(SWBigKey, self).__init__('Big Key (Skull Woods)', False, True, code=0x32)


class SWCompass(Item):
    def __init__(self):
        super(SWCompass, self).__init__('Compass (Skull Woods)', False, code=0x25)


class SWMap(Item):
    def __init__(self):
        super(SWMap, self).__init__('Map (Skull Woods)', False, code=0x33)


class SPSmallKey(Item):
    def __init__(self):
        super(SPSmallKey, self).__init__('Small Key (Swamp Palace)', False, True, code=0x24)


class SPBigKey(Item):
    def __init__(self):
        super(SPBigKey, self).__init__('Big Key (Swamp Palace)', False, True, code=0x32)


class SPCompass(Item):
    def __init__(self):
        super(SPCompass, self).__init__('Compass (Swamp Palace)', False, code=0x25)


class SPMap(Item):
    def __init__(self):
        super(SPMap, self).__init__('Map (Swamp Palace)', False, code=0x33)


class IPSmallKey(Item):
    def __init__(self):
        super(IPSmallKey, self).__init__('Small Key (Ice Palace)', False, True, code=0x24)


class IPBigKey(Item):
    def __init__(self):
        super(IPBigKey, self).__init__('Big Key (Ice Palace)', False, True, code=0x32)


class IPCompass(Item):
    def __init__(self):
        super(IPCompass, self).__init__('Compass (Ice Palace)', False, code=0x25)


class IPMap(Item):
    def __init__(self):
        super(IPMap, self).__init__('Map (Ice Palace)', False, code=0x33)


class MMSmallKey(Item):
    def __init__(self):
        super(MMSmallKey, self).__init__('Small Key (Misery Mire)', False, True, code=0x24)


class MMBigKey(Item):
    def __init__(self):
        super(MMBigKey, self).__init__('Big Key (Misery Mire)', False, True, code=0x32)


class MMCompass(Item):
    def __init__(self):
        super(MMCompass, self).__init__('Compass (Misery Mire)', False, code=0x25)


class MMMap(Item):
    def __init__(self):
        super(MMMap, self).__init__('Map (Misery Mire)', False, code=0x33)


class TRSmallKey(Item):
    def __init__(self):
        super(TRSmallKey, self).__init__('Small Key (Turtle Rock)', False, True, code=0x24)


class TRBigKey(Item):
    def __init__(self):
        super(TRBigKey, self).__init__('Big Key (Turtle Rock)', False, True, code=0x32)


class TRCompass(Item):
    def __init__(self):
        super(TRCompass, self).__init__('Compass (Turtle Rock)', False, code=0x25)


class TRMap(Item):
    def __init__(self):
        super(TRMap, self).__init__('Map (Turtle Rock)', False, code=0x33)


class GTSmallKey(Item):
    def __init__(self):
        super(GTSmallKey, self).__init__('Small Key (Ganons Tower)', False, True, code=0x24)


class GTBigKey(Item):
    def __init__(self):
        super(GTBigKey, self).__init__('Big Key (Ganons Tower)', False, True, code=0x32)


class GTCompass(Item):
    def __init__(self):
        super(GTCompass, self).__init__('Compass (Ganons Tower)', False, code=0x25)


class GTMap(Item):
    def __init__(self):
        super(GTMap, self).__init__('Map (Ganons Tower)', False, code=0x33)

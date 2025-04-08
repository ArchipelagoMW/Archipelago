from typing import Optional
from ..locations.items import *


class OR:
    __slots__ = ('__items', '__children')

    def __new__(cls, *args):
        if True in args:
            return True
        return super().__new__(cls)

    def __init__(self, *args):
        self.__items = [item for item in args if isinstance(item, str)]
        self.__children = [item for item in args if type(item) not in (bool, str) and item is not None]

        assert self.__items or self.__children, args

    def __repr__(self) -> str:
        return "or%s" % (self.__items+self.__children)

    def remove(self, item) -> None:
        if item in self.__items:
            self.__items.remove(item)

    def hasConsumableRequirement(self) -> bool:
        for item in self.__items:
            if isConsumable(item):
                print("Consumable OR requirement? %r" % self)
                return True
        for child in self.__children:
            if child.hasConsumableRequirement():
                print("Consumable OR requirement? %r" % self)
                return True
        return False

    def test(self, inventory) -> bool:
        for item in self.__items:
            if item in inventory:
                return True
        for child in self.__children:
            if child.test(inventory):
                return True
        return False

    def consume(self, inventory) -> bool:
        for item in self.__items:
            if item in inventory:
                if isConsumable(item):
                    inventory[item] -= 1
                    if inventory[item] == 0:
                        del inventory[item]
                    inventory["%s_USED" % item] = inventory.get("%s_USED" % item, 0) + 1
                return True
        for child in self.__children:
            if child.consume(inventory):
                return True
        return False

    def getItems(self, inventory, target_set) -> None:
        if self.test(inventory):
            return
        for item in self.__items:
            target_set.add(item)
        for child in self.__children:
            child.getItems(inventory, target_set)

    def copyWithModifiedItemNames(self, f) -> "OR":
        return OR(*(f(item) for item in self.__items), *(child.copyWithModifiedItemNames(f) for child in self.__children))


class AND:
    __slots__ = ('__items', '__children')

    def __new__(cls, *args):
        if False in args:
            return False
        return super().__new__(cls)

    def __init__(self, *args):
        self.__items = [item for item in args if isinstance(item, str)]
        self.__children = [item for item in args if type(item) not in (bool, str) and item is not None]

    def __repr__(self) -> str:
        return "and%s" % (self.__items+self.__children)

    def remove(self, item) -> None:
        if item in self.__items:
            self.__items.remove(item)

    def hasConsumableRequirement(self) -> bool:
        for item in self.__items:
            if isConsumable(item):
                return True
        for child in self.__children:
            if child.hasConsumableRequirement():
                return True
        return False

    def test(self, inventory) -> bool:
        for item in self.__items:
            if item not in inventory:
                return False
        for child in self.__children:
            if not child.test(inventory):
                return False
        return True

    def consume(self, inventory) -> bool:
        for item in self.__items:
            if isConsumable(item):
                inventory[item] -= 1
                if inventory[item] == 0:
                    del inventory[item]
                inventory["%s_USED" % item] = inventory.get("%s_USED" % item, 0) + 1
        for child in self.__children:
            if not child.consume(inventory):
                return False
        return True

    def getItems(self, inventory, target_set) -> None:
        if self.test(inventory):
            return
        for item in self.__items:
            target_set.add(item)
        for child in self.__children:
            child.getItems(inventory, target_set)

    def copyWithModifiedItemNames(self, f) -> "AND":
        return AND(*(f(item) for item in self.__items), *(child.copyWithModifiedItemNames(f) for child in self.__children))


class COUNT:
    __slots__ = ('__item', '__amount')

    def __init__(self, item: str, amount: int) -> None:
        self.__item = item
        self.__amount = amount

    def __repr__(self) -> str:
        return "<%dx%s>" % (self.__amount, self.__item)

    def hasConsumableRequirement(self) -> bool:
        if isConsumable(self.__item):
            return True
        return False

    def test(self, inventory) -> bool:
        return inventory.get(self.__item, 0) >= self.__amount

    def consume(self, inventory) -> None:
        if isConsumable(self.__item):
            inventory[self.__item] -= self.__amount
            if inventory[self.__item] == 0:
                del inventory[self.__item]
            inventory["%s_USED" % self.__item] = inventory.get("%s_USED" % self.__item, 0) + self.__amount

    def getItems(self, inventory, target_set) -> None:
        if self.test(inventory):
            return
        target_set.add(self.__item)

    def copyWithModifiedItemNames(self, f) -> "COUNT":
        return COUNT(f(self.__item), self.__amount)


class COUNTS:
    __slots__ = ('__items', '__amount')

    def __init__(self, items, amount):
        self.__items = items
        self.__amount = amount

    def __repr__(self) -> str:
        return "<%dx%s>" % (self.__amount, self.__items)

    def hasConsumableRequirement(self) -> bool:
        for item in self.__items:
            if isConsumable(item):
                print("Consumable COUNTS requirement? %r" % (self))
                return True
        return False

    def test(self, inventory) -> bool:
        count = 0
        for item in self.__items:
            count += inventory.get(item, 0)
        return count >= self.__amount

    def consume(self, inventory) -> None:
        for item in self.__items:
            if isConsumable(item):
                inventory[item] -= self.__amount
                if inventory[item] == 0:
                    del inventory[item]
                inventory["%s_USED" % item] = inventory.get("%s_USED" % item, 0) + self.__amount

    def getItems(self, inventory, target_set) -> None:
        if self.test(inventory):
            return
        for item in self.__items:
            target_set.add(item)

    def copyWithModifiedItemNames(self, f) -> "COUNTS":
        return COUNTS([f(item) for item in self.__items], self.__amount)


class FOUND:
    __slots__ = ('__item', '__amount')

    def __init__(self, item: str, amount: int) -> None:
        self.__item = item
        self.__amount = amount

    def __repr__(self) -> str:
        return "{%dx%s}" % (self.__amount, self.__item)

    def hasConsumableRequirement(self) -> bool:
        return False

    def test(self, inventory) -> bool:
        return inventory.get(self.__item, 0) + inventory.get("%s_USED" % self.__item, 0) >= self.__amount

    def consume(self, inventory) -> None:
        pass

    def getItems(self, inventory, target_set) -> None:
        if self.test(inventory):
            return
        target_set.add(self.__item)

    def copyWithModifiedItemNames(self, f) -> "FOUND":
        return FOUND(f(self.__item), self.__amount)


def hasConsumableRequirement(requirements) -> bool:
    if isinstance(requirements, str):
        return isConsumable(requirements)
    if requirements is None:
        return False
    return requirements.hasConsumableRequirement()


def isConsumable(item) -> bool:
    if item is None:
        return False
    #if item.startswith("RUPEES_") or item == "RUPEES":
    #    return True
    if item.startswith("KEY"):
        return True
    return False


class RequirementsSettings:
    def __init__(self, options):
        self.bush = OR(SWORD, MAGIC_POWDER, MAGIC_ROD, POWER_BRACELET, BOOMERANG)
        self.attack = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG)
        self.attack_hookshot = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # switches, hinox, shrouded stalfos
        self.attack_hookshot_powder = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT, MAGIC_POWDER) # zols, keese, moldorm
        self.attack_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # ?
        self.attack_hookshot_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # vire
        self.attack_no_boomerang = OR(SWORD, BOMB, BOW, MAGIC_ROD, HOOKSHOT) # teleporting owls
        self.attack_skeleton = OR(SWORD, BOMB, BOW, BOOMERANG, HOOKSHOT)  # cannot kill skeletons with the fire rod
        self.rear_attack = OR(SWORD, BOMB) # mimic
        self.rear_attack_range = OR(MAGIC_ROD, BOW) # mimic
        self.fire = OR(MAGIC_POWDER, MAGIC_ROD) # torches
        self.push_hardhat = OR(SHIELD, SWORD, HOOKSHOT, BOOMERANG)

        self.boss_requirements = [
            SWORD,  # D1 boss
            AND(OR(SWORD, MAGIC_ROD), POWER_BRACELET),  # D2 boss
            AND(PEGASUS_BOOTS, SWORD),  # D3 boss
            AND(FLIPPERS, OR(SWORD, MAGIC_ROD, BOW)),  # D4 boss
            AND(HOOKSHOT, SWORD),  # D5 boss
            BOMB,  # D6 boss
            AND(OR(MAGIC_ROD, SWORD, HOOKSHOT), COUNT(SHIELD, 2)),  # D7 boss
            MAGIC_ROD,  # D8 boss
            self.attack_hookshot_no_bomb,  # D9 boss
        ]
        self.miniboss_requirements = {
            "ROLLING_BONES":    self.attack_hookshot,
            "HINOX":            self.attack_hookshot,
            "DODONGO":          BOMB,
            "CUE_BALL":         SWORD,
            "GHOMA":            OR(BOW, HOOKSHOT),
            "SMASHER":          POWER_BRACELET,
            "GRIM_CREEPER":     self.attack_hookshot_no_bomb,
            "BLAINO":           SWORD,
            "AVALAUNCH":        self.attack_hookshot,
            "GIANT_BUZZ_BLOB":  MAGIC_POWDER,
            "MOBLIN_KING":      SWORD,
            "ARMOS_KNIGHT":     OR(BOW, MAGIC_ROD, SWORD),
        }

        # Adjust for options
        if options.bowwow != 'normal':
            # We cheat in bowwow mode, we pretend we have the sword, as bowwow can pretty much do all what the sword ca$            # Except for taking out bushes (and crystal pillars are removed)
            self.bush.remove(SWORD)
        if options.logic == "casual":
            # In casual mode, remove the more complex kill methods
            self.bush.remove(MAGIC_POWDER)
            self.attack_hookshot_powder.remove(MAGIC_POWDER)
            self.attack.remove(BOMB)
            self.attack_hookshot.remove(BOMB)
            self.attack_hookshot_powder.remove(BOMB)
            self.attack_no_boomerang.remove(BOMB)
            self.attack_skeleton.remove(BOMB)
        if options.logic == "hard":
            self.boss_requirements[3] = AND(FLIPPERS, OR(SWORD, MAGIC_ROD, BOW, BOMB))  # bomb angler fish
            self.boss_requirements[6] = OR(MAGIC_ROD, AND(BOMB, BOW), COUNT(SWORD, 2), AND(OR(SWORD, HOOKSHOT, BOW), SHIELD))  # evil eagle 3 cycle magic rod / bomb arrows / l2 sword, and bow kill
        if options.logic == "glitched":
            self.boss_requirements[3] = AND(FLIPPERS, OR(SWORD, MAGIC_ROD, BOW, BOMB))  # bomb angler fish
            self.boss_requirements[6] = OR(MAGIC_ROD, BOMB, BOW, HOOKSHOT, COUNT(SWORD, 2), AND(SWORD, SHIELD))  # evil eagle off screen kill or 3 cycle with bombs
        if options.logic == "hell":
            self.boss_requirements[3] = AND(FLIPPERS, OR(SWORD, MAGIC_ROD, BOW, BOMB))  # bomb angler fish
            self.boss_requirements[6] = OR(MAGIC_ROD, BOMB, BOW, HOOKSHOT, COUNT(SWORD, 2), AND(SWORD, SHIELD))  # evil eagle off screen kill or 3 cycle with bombs
            self.boss_requirements[7] = OR(MAGIC_ROD, COUNT(SWORD, 2)) # hot head sword beams
            self.miniboss_requirements["GIANT_BUZZ_BLOB"] = OR(MAGIC_POWDER, COUNT(SWORD,2)) # use sword beams to damage buzz blob

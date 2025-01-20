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
        self.pit_bush = OR(SWORD, MAGIC_POWDER, MAGIC_ROD, BOOMERANG, BOMB) # unique
        self.attack = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG)
        self.attack_hookshot = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # hinox, shrouded stalfos
        self.hit_switch = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # hit switches in dungeons
        self.attack_hookshot_powder = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT, MAGIC_POWDER) # zols, keese, moldorm
        self.attack_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # ?
        self.attack_hookshot_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # vire
        self.attack_no_boomerang = OR(SWORD, BOMB, BOW, MAGIC_ROD, HOOKSHOT) # teleporting owls
        self.attack_skeleton = OR(SWORD, BOMB, BOW, BOOMERANG, HOOKSHOT)  # cannot kill skeletons with the fire rod
        self.attack_gibdos = OR(SWORD, BOMB, BOW, BOOMERANG, AND(MAGIC_ROD, HOOKSHOT)) # gibdos are only stunned with hookshot, but can be burnt to jumping stalfos first with magic rod
        self.attack_pols_voice = OR(BOMB, MAGIC_ROD, AND(OCARINA, SONG1)) # BOW works, but isn't as reliable as it needs 4 arrows.
        self.attack_wizrobe = OR(BOMB, MAGIC_ROD) # BOW works, but isn't as reliable as it needs 4 arrows.
        self.stun_wizrobe = OR(BOOMERANG, MAGIC_POWDER, HOOKSHOT)
        self.rear_attack = OR(SWORD, BOMB) # mimic
        self.rear_attack_range = OR(MAGIC_ROD, BOW) # mimic
        self.fire = OR(MAGIC_POWDER, MAGIC_ROD) # torches
        self.push_hardhat = OR(SHIELD, SWORD, HOOKSHOT, BOOMERANG)
        self.shuffled_magnifier = TRADING_ITEM_MAGNIFYING_GLASS # overwritten if vanilla trade items

        self.throw_pot = POWER_BRACELET # grab pots to kill enemies
        self.throw_enemy = POWER_BRACELET # grab stunned enemies to kill enemies
        self.tight_jump = FEATHER # jumps that are possible but are tight to make it across
        self.super_jump = AND(FEATHER, OR(SWORD, BOW, MAGIC_ROD)) # standard superjump for glitch logic
        self.super_jump_boots = AND(PEGASUS_BOOTS, FEATHER, OR(SWORD, BOW, MAGIC_ROD)) # boots dash into wall for unclipped superjump
        self.super_jump_feather = FEATHER # using only feather to align and jump off walls
        self.super_jump_sword = AND(FEATHER, SWORD) # unclipped superjumps
        self.super_jump_rooster = AND(ROOSTER, OR(SWORD, BOW, MAGIC_ROD)) # use rooster instead of feather to superjump off walls (only where rooster is allowed to be used)
        self.shaq_jump = FEATHER # use interactable objects (keyblocks / pushable blocks)
        self.boots_superhop = AND(PEGASUS_BOOTS, OR(MAGIC_ROD, BOW)) # dash into walls, pause, unpause and use weapon + hold direction away from wall. Only works in peg rooms
        self.boots_roosterhop = AND(PEGASUS_BOOTS, ROOSTER) # dash towards a wall, pick up the rooster and throw it away from the wall before hitting the wall to get a superjump
        self.jesus_jump = FEATHER # pause on the frame of hitting liquid (water / lava) to be able to jump again on unpause
        self.jesus_buffer = PEGASUS_BOOTS # use a boots bonk to get on top of liquid (water / lava), then use buffers to get into positions
        self.damage_boost_special = options.hardmode == "none" # use damage to cross pits / get through forced barriers without needing an enemy that can be eaten by bowwow
        self.damage_boost = (options.bowwow == "normal") & (options.hardmode == "none")  # Use damage to cross pits / get through forced barriers
        self.sideways_block_push = True # wall clip pushable block, get against the edge and push block to move it sideways
        self.wall_clip = True # push into corners to get further into walls, to avoid collision with enemies along path (see swamp flowers for example) or just getting a better position for jumps
        self.pit_buffer_itemless = True # walk on top of pits and buffer down
        self.pit_buffer = FEATHER # jump on top of pits and buffer to cross vertical gaps
        self.pit_buffer_boots = OR(PEGASUS_BOOTS, FEATHER) # use boots or feather to cross gaps
        self.boots_jump = AND(PEGASUS_BOOTS, FEATHER) # use boots jumps to cross 4 gap spots or other hard to reach spots
        self.boots_bonk = PEGASUS_BOOTS # bonk against walls in 2d sections to get to higher places (no pits involved usually)
        self.boots_bonk_pit = PEGASUS_BOOTS # use boots bonks to cross 1 tile gaps
        self.boots_bonk_2d_spikepit = AND(PEGASUS_BOOTS, "MEDICINE2") # use iframes from medicine to get a boots dash going in 2d spike pits (kanalet secret passage, d3 2d section to boss)
        self.boots_bonk_2d_hell = PEGASUS_BOOTS # seperate boots bonks from hell logic which are harder?
        self.boots_dash_2d = PEGASUS_BOOTS # use boots to dash over 1 tile gaps in 2d sections
        self.hookshot_spam_pit = HOOKSHOT # use hookshot with spam to cross 1 tile gaps
        self.hookshot_clip = AND(HOOKSHOT, options.superweapons == False) # use hookshot at specific angles to hookshot past blocks (see forest north log cave, dream shrine entrance for example)
        self.hookshot_clip_block = HOOKSHOT # use hookshot spam with enemies to clip through entire blocks (d5 room before gohma, d2 pots room before boss)
        self.hookshot_over_pit = HOOKSHOT # use hookshot while over a pit to reach certain areas (see d3 vacuum room, d5 north of crossroads for example)
        self.hookshot_jump = AND(HOOKSHOT, FEATHER) # while over pits, on the first frame after the hookshot is retracted you can input a jump to cross big pit gaps
        self.bookshot = AND(FEATHER, HOOKSHOT) # use feather on A, hookshot on B on the same frame to get a speedy hookshot that can be used to clip past blocks
        self.bomb_trigger = BOMB # drop two bombs at the same time to trigger cutscenes or pickup items (can use pits, or screen transitions
        self.shield_bump = SHIELD # use shield to knock back enemies or knock off enemies when used in combination with superjumps
        self.text_clip = False & options.nagmessages # trigger a text box on keyblock or rock or obstacle while holding diagonal to clip into the side. Removed from logic for now
        self.jesus_rooster = AND(ROOSTER, options.hardmode != "oracle") # when transitioning on top of water, buffer the rooster out of sq menu to spawn it. Then do an unbuffered pickup of the rooster as soon as you spawn again to pick it up
        self.zoomerang = AND(PEGASUS_BOOTS, FEATHER, BOOMERANG) # after starting a boots dash, buffer boomerang (on b), feather and the direction you're dashing in to get boosted in certain directions

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
            "GHOMA":            OR(BOW, HOOKSHOT, MAGIC_ROD, BOOMERANG),
            "SMASHER":          POWER_BRACELET,
            "GRIM_CREEPER":     self.attack_hookshot_no_bomb,
            "BLAINO":           SWORD,
            "AVALAUNCH":        self.attack_hookshot,
            "GIANT_BUZZ_BLOB":  MAGIC_POWDER,
            "MOBLIN_KING":      SWORD,
            "ARMOS_KNIGHT":     OR(BOW, MAGIC_ROD, SWORD),
        }

        # Adjust for options
        if not options.tradequest:
            self.shuffled_magnifier = True # completing trade quest not required
        if options.hardmode == "ohko":
            self.miniboss_requirements["ROLLING_BONES"] = OR(BOW, MAGIC_ROD, BOOMERANG, AND(FEATHER, self.attack_hookshot)) # should not deal with roller damage
        if options.bowwow != "normal":
            # We cheat in bowwow mode, we pretend we have the sword, as bowwow can pretty much do all what the sword ca$            # Except for taking out bushes (and crystal pillars are removed)
            self.bush.remove(SWORD)
            self.pit_bush.remove(SWORD)
            self.hit_switch.remove(SWORD)
        if options.logic == "casual":
            # In casual mode, remove the more complex kill methods
            self.bush.remove(MAGIC_POWDER)
            self.attack_hookshot_powder.remove(MAGIC_POWDER)
            self.attack.remove(BOMB)
            self.attack_hookshot.remove(BOMB)
            self.attack_hookshot_powder.remove(BOMB)
            self.attack_no_boomerang.remove(BOMB)
            self.attack_skeleton.remove(BOMB)

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            self.boss_requirements[1] = AND(OR(SWORD, MAGIC_ROD, BOMB), POWER_BRACELET)  # bombs + bracelet genie
            self.boss_requirements[3] = AND(FLIPPERS, OR(SWORD, MAGIC_ROD, BOW, BOMB))  # bomb angler fish
            self.boss_requirements[6] = OR(MAGIC_ROD, AND(BOMB, BOW), COUNT(SWORD, 2), AND(OR(SWORD, HOOKSHOT, BOW), SHIELD))  # evil eagle 3 cycle magic rod / bomb arrows / l2 sword, and bow kill
            self.attack_pols_voice = OR(BOMB, MAGIC_ROD, AND(OCARINA, SONG1), AND(self.stun_wizrobe, self.throw_enemy, BOW)) # wizrobe stun has same req as pols voice stun
            self.attack_wizrobe = OR(BOMB, MAGIC_ROD, AND(self.stun_wizrobe, self.throw_enemy, BOW))

        if options.logic == 'glitched' or options.logic == 'hell':
            self.boss_requirements[6] = OR(MAGIC_ROD, BOMB, BOW, HOOKSHOT, COUNT(SWORD, 2), AND(SWORD, SHIELD))  # evil eagle off screen kill or 3 cycle with bombs

        if options.logic == "hell":
            self.boss_requirements[7] = OR(MAGIC_ROD, COUNT(SWORD, 2)) # hot head sword beams
            self.miniboss_requirements["GHOMA"] = OR(BOW, HOOKSHOT, MAGIC_ROD, BOOMERANG, AND(OCARINA, BOMB, OR(SONG1, SONG3)))  # use bombs to kill gohma, with ocarina to get good timings
            self.miniboss_requirements["GIANT_BUZZ_BLOB"] = OR(MAGIC_POWDER, COUNT(SWORD,2)) # use sword beams to damage buzz blob

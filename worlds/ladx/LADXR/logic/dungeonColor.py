from .requirements import *
from .location import Location
from ..locations.all import *


class DungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=9)
        room2 = Location(dungeon=9).connect(entrance, r.attack_hookshot_powder)
        room2.add(DungeonChest(0x314))  # key
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=9).add(OwlStatue(0x308), OwlStatue(0x30F)).connect(room2, STONE_BEAK9)
        room2_weapon = Location(dungeon=9).connect(room2, AND(r.attack_hookshot, POWER_BRACELET))
        room2_weapon.add(DungeonChest(0x311))  # stone beak
        room2_lights = Location(dungeon=9).connect(room2, OR(r.attack_hookshot, SHIELD))
        room2_lights.add(DungeonChest(0x30F))  # compass chest
        room2_lights.add(DroppedKey(0x308))

        Location(dungeon=9).connect(room2, AND(KEY9, FOUND(KEY9, 3), r.miniboss_requirements[world_setup.miniboss_mapping["c2"]])).add(DungeonChest(0x302))  # nightmare key after slime mini boss
        room3 = Location(dungeon=9).connect(room2, AND(KEY9, FOUND(KEY9, 2), r.miniboss_requirements[world_setup.miniboss_mapping["c1"]])) # After the miniboss
        room4 = Location(dungeon=9).connect(room3, POWER_BRACELET)  # need to lift a pot to reveal button
        room4.add(DungeonChest(0x306))  # map
        room4karakoro = Location(dungeon=9).add(DroppedKey(0x307)).connect(room4, AND(r.attack_hookshot, POWER_BRACELET))  # require item to knock Karakoro enemies into shell
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=9).add(OwlStatue(0x30A)).connect(room4, STONE_BEAK9)
        room5 = Location(dungeon=9).connect(room4, OR(r.attack_hookshot, SHIELD)) # lights room
        room6 = Location(dungeon=9).connect(room5, AND(KEY9, FOUND(KEY9, 3))) # room with switch and nightmare door
        pre_boss = Location(dungeon=9).connect(room6, OR(r.hit_switch, AND(PEGASUS_BOOTS, FEATHER)))  # before the boss, require item to hit switch or jump past raised blocks
        boss = Location(dungeon=9).connect(pre_boss, AND(NIGHTMARE_KEY9, r.boss_requirements[world_setup.boss_mapping[8]]))
        boss.add(TunicFairy(0), TunicFairy(1))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            room2.connect(entrance, r.throw_pot) # throw pots at enemies
            room2_weapon.connect(room2, r.attack_hookshot_no_bomb) # knock the karakoro into the pit without picking them up. 
            pre_boss.connect(room6, r.tight_jump) # before the boss, jump past raised blocks without boots

        if options.logic == 'hell':
            room2_weapon.connect(room2, r.attack_hookshot) # also have a bomb as option to knock the karakoro into the pit without bracelet 
            room2_weapon.connect(room2, r.shield_bump) # shield bump karakoro into the holes
            room4karakoro.connect(room4, r.shield_bump) # shield bump karakoro into the holes
            
        self.entrance = entrance


class NoDungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=9)
        boss = Location(dungeon=9).connect(entrance, r.boss_requirements[world_setup.boss_mapping[8]])
        boss.add(TunicFairy(0), TunicFairy(1))

        self.entrance = entrance

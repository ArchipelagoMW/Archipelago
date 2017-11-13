from Items import ItemFactory
from Fill import fill_restrictive
import random

#This file sets the item pools for various modes. Timed modes and triforce hunt are enforced first, and then extra items are specified per mode to fill in the remaining space.
#Some basic items that various modes require are placed here, including pendants and crystals. Medallion requirements for the two relevant entrances are also decided.

alwaysitems = ['Bombos', 'Book of Mudora', 'Bow', 'Cane of Somaria', 'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp',
              'Cape', 'Magic Powder', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Bug Catching Net', 'Cane of Byrna']
progressivegloves = ['Progressive Glove'] * 2
basicgloves = ['Power Glove', 'Titans Mitts']

normalbottles = ['Bottle', 'BottleRedPotion', 'BottleGreenPotion', 'BottleBluePotion', 'BottleFairy', 'BottleBee', 'BottleGoodBee']
hardbottles = ['Bottle', 'BottleRedPotion', 'BottleGreenPotion', 'BottleBluePotion', 'BottleBee', 'BottleGoodBee']

normalbaseitems = (['Blue Boomerang', 'Red Boomerang', 'Silver Arrows', 'Magic Upgrade (1/2)'] + ['Rupees (300)'] * 4 +
                  ['Single Arrow', 'Sanctuary Heart Container', 'Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24)
normalfirst15extra = ['Rupees (100)', 'Rupees (300)', 'Rupees (50)'] + ['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6
normalsecond15extra = ['Bombs (3)'] * 10 + ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupee (1)']
normalthird10extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 3 + ['Arrows (10)', 'Rupee (1)', 'Rupees (5)']
normalfourth5extra = ['Arrows (10)'] * 2 + ['Rupees (20)'] * 2 + ['Rupees (5)']
normalfinal25extra = ['Rupees (20)'] * 23 + ['Rupees (5)'] * 2
normaltimedohko = ['Green Clock'] * 25
normaltimedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10
normaltriforcehunt = ['Triforce Piece'] * 30
normalprogressivesword = ['Progressive Sword'] * 3
normalbasicsword = ['Master Sword', 'Tempered Sword', 'Golden Sword']
normalswordless = ['Rupees (20)'] * 4
normalprogressiveshield = ['Progressive Shield'] * 3
normalbasicshield = ['Blue Shield', 'Red Shield', 'Mirror Shield']
normalprogressivearmor = ['Progressive Armor'] * 2
normalbasicarmor = ['Blue Mail', 'Red Mail']

easybaseitems = (['Blue Boomerang', 'Red Boomerang', 'Silver Arrows'] + ['Rupees (300)'] * 4 + ['Magic Upgrade (1/2)'] * 2 +
                ['Single Arrow', 'Sanctuary Heart Container', 'Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 12)
easyextra = ['Piece of Heart'] * 12 + ['Rupees (300)']
easylimitedextra = ['Boss Heart Container'] * 3
easyfirst15extra = ['Rupees (100)'] + ['Rupees (50)'] + ['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6 + ['Bombs (3)']
easysecond10extra = ['Bombs (3)'] * 9 + ['Rupee (1)']
easythird5extra = ['Rupees (50)'] * 2 + ['Arrows (10)'] * 2 + ['Rupees (5)']
easyfinal25extra = ['Rupees (50)'] * 4 + ['Rupees (20)'] * 14 + ['Rupee (1)'] + ['Arrows (10)'] * 3 + ['Rupees (5)'] * 3
easytimedohko = ['Green Clock'] * 25
easytimedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 5
easytimedotherextra = ['Red Clock'] * 5
easytriforcehunt = ['Triforce Piece'] * 30
easyprogressivesword = ['Progressive Sword'] * 7
easybasicsword = ['Fighter Sword', 'Master Sword', 'Master Sword', 'Tempered Sword', 'Tempered Sword', 'Golden Sword', 'Golden Sword']
easyswordless = ['Rupees (20)'] * 8
easyprogressiveshield = ['Progressive Shield'] * 6
easybasicshield = ['Blue Shield', 'Blue Shield', 'Red Shield', 'Red Shield', 'Mirror Shield', 'Mirror Shield']
easyprogressivearmor = ['Progressive Armor'] * 4
easybasicarmor = ['Blue Mail', 'Blue Mail', 'Red Mail', 'Red Mail']

hardbaseitems = (['Silver Arrows', 'Single Arrow'] + ['Rupees (300)'] + ['Rupees (100)'] * 2 + ['Rupees (50)'] + ['Bombs (3)'] +
                ['Boss Heart Container'] * 5 + ['Piece of Heart'] * 24)
hardfirst20extra = ['Bombs (3)'] * 4 + ['Single Bomb'] * 4 + ['Rupees (5)'] * 5 + ['Rupee (1)'] * 2 + ['Rupees (100)'] + ['Rupees (50)'] * 4
hardsecond20extra = ['Single Bomb'] * 4 + ['Rupees (5)'] * 10 + ['Rupees (20)']  * 2 + ['Rupee (1)'] * 3 + ['Arrows (10)']
hardthird20extra = ['Arrows (10)'] * 4 + ['Rupees (20)']  * 3 + ['Rupees (5)'] * 3 + ['Single Bomb'] * 5 + ['Single Arrow'] * 5
hardfinal20extra = ['Single Bomb'] * 4 + ['Rupees (5)'] * 2 + ['Single Arrow'] * 14
hardtimedohko = ['Green Clock'] * 20
hardtimedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10
hardtriforcehunt = ['Triforce Piece'] * 40
hardprogressivesword = ['Progressive Sword'] * 3
hardbasicsword = ['Master Sword', 'Master Sword', 'Tempered Sword']
hardswordless = ['Rupees (20)'] * 4
hardprogressiveshield = ['Progressive Shield'] * 3
hardbasicshield = ['Blue Shield', 'Red Shield', 'Red Shield']
hardarmor = ['Progressive Armor', 'Progressive Armor']

expertbaseitems = (['Single Arrow', 'Rupees (300)', 'Rupees (100)', 'Bombs (3)', 'Arrows (10)'] + ['Rupees (50)'] * 4 + ['Rupees (5)'] * 5 +
                  ['Rupees (20)'] + ['Single Bomb'] * 2 + ['Piece of Heart'] * 24)
expertfirst15extra = ['Single Bomb'] * 13 + ['Rupees (20)'] * 2
expertsecond25extra = ['Single Bomb'] * 8 + ['Single Arrow'] * 9 + ['Rupees (20)']  * 3 + ['Rupee (1)'] * 5
expertthird15extra = ['Rupees (5)'] * 5 + ['Single Bomb'] * 3 + ['Rupees (20)'] * 2 + ['Single Arrow'] * 5
expertfinal25extra = ['Single Bomb'] * 4 + ['Rupees (20)']  * 3 + ['Single Arrow'] * 18
experttimedohko = ['Green Clock'] * 20 + ['Red Clock'] * 5
experttimedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10
experttriforcehunt = ['Triforce Piece'] * 40
expertprogressivesword = ['Progressive Sword'] * 3
expertbasicsword = ['Fighter Sword', 'Master Sword', 'Master Sword']
expertswordless = ['Rupees (20)'] * 3 + ['Silver Arrows']

insanebaseitems = (['Single Arrow', 'Bombs (3)', 'Arrows (10)'] + ['Rupees (50)'] * 3 + ['Rupees (5)'] * 10 + ['Rupees (300)'] * 4 + ['Rupees (100)'] * 3 +
                  ['Rupee (1)'] * 4 + ['Single Bomb'] * 4)
insanefirst15extra = ['Single Bomb'] * 4 + ['Single Arrow'] * 4 + ['Rupee (1)'] * 4 + ['Rupees (300)'] + ['Rupees (100)'] + ['Rupees (50)']
insanesecond25extra = ['Single Bomb'] * 7 + ['Single Arrow'] * 7 + ['Rupee (1)'] * 7 + ['Rupees (20)'] * 4
insanethird10extra = ['Single Bomb'] * 3 + ['Single Arrow'] * 3 + ['Rupee (1)'] * 3 + ['Rupees (20)']
insanefourth15extra = ['Single Bomb'] * 5 + ['Single Arrow'] * 5 + ['Rupee (1)'] * 5
insanefinal25extra = ['Single Bomb'] * 2 + ['Single Arrow'] * 10 + ['Rupee (1)'] * 7 + ['Rupees (20)'] * 6
insanetimedohko = ['Green Clock'] * 20 + ['Red Clock'] * 5
insanetimedother = ['Green Clock'] * 20 + ['Blue Clock'] * 10 + ['Red Clock'] * 10
insanetriforcehunt = ['Triforce Piece'] * 50
insaneprogressivesword = ['Progressive Sword'] * 3
insanebasicsword = ['Fighter Sword', 'Master Sword', 'Master Sword']
insaneswordless = ['Rupees (20)'] * 3 + ['Silver Arrows']

def generate_itempool(world):
    if (world.difficulty not in ['easy', 'normal', 'hard', 'expert', 'insane'] or world.goal not in ['ganon', 'pedestal', 'dungeons', 'triforcehunt', 'crystals']
       or world.mode not in ['open', 'standard', 'swordless'] or world.timer not in ['none', 'display', 'timed', 'timed-ohko', 'timed-countdown'] or world.progressive not in ['on', 'off', 'random']):
        raise NotImplementedError('Not supported yet')

    world.push_item('Ganon', ItemFactory('Triforce'), False)
    world.get_location('Ganon').event = True
    world.push_item('Agahnim 1', ItemFactory('Beat Agahnim 1'), False)
    world.get_location('Agahnim 1').event = True
    world.push_item('Agahnim 2', ItemFactory('Beat Agahnim 2'), False)
    world.get_location('Agahnim 2').event = True

    # set up item pool
    world.itempool = ItemFactory(alwaysitems)
    if world.progressive == 'on':
        world.itempool.extend(ItemFactory(progressivegloves))
    elif world.progressive == 'off':
        world.itempool.extend(ItemFactory(basicgloves))
    else:
        randvalue = random.randint(0, 1)
        if (randvalue == 0):
            world.itempool.extend(ItemFactory(progressivegloves))
        else:
            world.itempool.extend(ItemFactory(basicgloves))

    # insanity shuffle doesn't have fake LW/DW logic so for now guaranteed Mirror and Moon Pearl at the start
    if world.shuffle == 'insanity':
        world.push_item('Link\'s House', ItemFactory('Magic Mirror'), False)
        world.get_location('Link\'s House').event = True
        world.push_item('Sanctuary', ItemFactory('Moon Pearl'), False)
        world.get_location('Sanctuary').event = True
    else:
        world.itempool.extend(ItemFactory(['Magic Mirror', 'Moon Pearl']))

    if world.timer == 'display':
        world.clock_mode = 'stopwatch'

    if world.difficulty == 'normal':
        world.itempool.extend(ItemFactory(normalbaseitems))
        for i in range (0, 4):
            thisbottle = normalbottles[random.randint(0, 6)]
            world.itempool.append(ItemFactory(thisbottle))
        extraitems = 70
        if world.timer in ['timed', 'timed-countdown']:
            world.itempool.extend(ItemFactory(normaltimedother))
            extraitems = extraitems - 40
            world.clock_mode = 'stopwatch' if world.timer == 'timed' else 'countdown'
        elif world.timer == 'timed-ohko':
            world.itempool.extend(ItemFactory(normaltimedohko))
            extraitems = extraitems - 25
            world.clock_mode = 'ohko'
        if world.goal == 'triforcehunt':
            world.itempool.extend(ItemFactory(normaltriforcehunt))
            extraitems = extraitems - 30
            world.treasure_hunt_count = 20
            world.treasure_hunt_icon = 'Triforce Piece'
        if extraitems > 0:
            world.itempool.extend(ItemFactory(normalfirst15extra))
            extraitems = extraitems - 15
            print(extraitems)
        if extraitems > 0:
            world.itempool.extend(ItemFactory(normalsecond15extra))
            extraitems = extraitems - 15
            print(extraitems)
        if extraitems > 0:
            world.itempool.extend(ItemFactory(normalthird10extra))
            extraitems = extraitems - 10
            print(extraitems)
        if extraitems > 0:
            world.itempool.extend(ItemFactory(normalfourth5extra))
            extraitems = extraitems - 5
            print(extraitems)
        if extraitems > 0:
            world.itempool.extend(ItemFactory(normalfinal25extra))
            extraitems = extraitems - 25
            print(extraitems)
        if world.progressive == 'on':
            world.itempool.extend(ItemFactory(normalprogressiveshield))
            world.itempool.extend(ItemFactory(normalprogressivearmor))
        elif world.progressive == 'off':
            world.itempool.extend(ItemFactory(normalbasicshield))
            world.itempool.extend(ItemFactory(normalbasicarmor))
        else:
            randvalue = random.randint(0, 1)
            if (randvalue == 0):
                world.itempool.extend(ItemFactory(normalprogressiveshield))
            else:
                world.itempool.extend(ItemFactory(normalbasicshield))
            randvalue = random.randint(0, 1)
            if (randvalue == 0):
                world.itempool.extend(ItemFactory(normalprogressivearmor))
            else:
                world.itempool.extend(ItemFactory(normalbasicarmor))
        if world.mode == 'swordless':
            world.itempool.extend(ItemFactory(normalswordless))
        elif world.mode == 'standard':
            if world.progressive == 'on':
                world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(normalprogressivesword))
            elif world.progressive == 'off':
                world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(normalbasicsword))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(normalprogressivesword))
                else:
                    world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(normalbasicsword))
        else:
            if world.progressive == 'on':
                world.itempool.extend(ItemFactory(normalprogressivesword))
                world.itempool.extend(ItemFactory(['Progressive Sword']))
            elif world.progressive == 'off':
                world.itempool.extend(ItemFactory(normalbasicsword))
                world.itempool.extend(ItemFactory(['Fighter Sword']))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.itempool.extend(ItemFactory(normalprogressivesword))
                    world.itempool.extend(ItemFactory(['Progressive Sword']))
                else:
                    world.itempool.extend(ItemFactory(normalbasicsword))
                    world.itempool.extend(ItemFactory(['Fighter Sword']))

    elif world.difficulty == 'easy':
        world.itempool.extend(ItemFactory(easybaseitems))
        for i in range (0, 8):
            thisbottle = normalbottles[random.randint(0, 6)]
            world.itempool.append(ItemFactory(thisbottle))
        extraitems = 70
        if world.timer in ['timed', 'timed-countdown']:
            world.itempool.extend(ItemFactory(easytimedother))
            extraitems = extraitems - 40
            world.clock_mode = 'stopwatch' if world.timer == 'timed' else 'countdown'
        elif world.timer == 'timed-ohko':
            world.itempool.extend(ItemFactory(easytimedohko))
            extraitems = extraitems - 25
            world.clock_mode = 'ohko'
        if world.goal == 'triforcehunt':
            world.itempool.extend(ItemFactory(easytriforcehunt))
            extraitems = extraitems - 30
            world.treasure_hunt_count = 10
            world.treasure_hunt_icon = 'Triforce Piece'
        if extraitems == 0:
            world.itempool.extend(ItemFactory(easylimitedextra))
        else:
            world.itempool.extend(ItemFactory(easyextra))
            if world.timer in ['timed', 'timed-countdown']:
                world.itempool.extend(ItemFactory(easytimedotherextra))
        extraitems = extraitems - 15
        if extraitems > 0:
            world.itempool.extend(ItemFactory(easyfirst15extra))
            extraitems = extraitems - 15
        if extraitems > 0:
            world.itempool.extend(ItemFactory(easysecond10extra))
            extraitems = extraitems - 10
        if extraitems > 0:
            world.itempool.extend(ItemFactory(easythird5extra))
            extraitems = extraitems - 5
        if extraitems > 0:
            world.itempool.extend(ItemFactory(easyfinal25extra))
            extraitems = extraitems - 25
        if world.progressive == 'on':
            world.itempool.extend(ItemFactory(easyprogressiveshield))
            world.itempool.extend(ItemFactory(easyprogressivearmor))
        elif world.progressive == 'off':
            world.itempool.extend(ItemFactory(easybasicshield))
            world.itempool.extend(ItemFactory(easybasicarmor))
        else:
            randvalue = random.randint(0, 1)
            if (randvalue == 0):
                world.itempool.extend(ItemFactory(easyprogressiveshield))
            else:
                world.itempool.extend(ItemFactory(easybasicshield))
            randvalue = random.randint(0, 1)
            if (randvalue == 0):
                world.itempool.extend(ItemFactory(easyprogressivearmor))
            else:
                world.itempool.extend(ItemFactory(easybasicarmor))
        if world.mode == 'swordless':
            world.itempool.extend(ItemFactory(easyswordless))
        elif world.mode == 'standard':
            if world.progressive == 'on':
                world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(easyprogressivesword))
            elif world.progressive == 'off':
                world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(easybasicsword))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(easyprogressivesword))
                else:
                    world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(easybasicsword))
        else:
            if world.progressive == 'on':
                world.itempool.extend(ItemFactory(easyprogressivesword))
                world.itempool.extend(ItemFactory(['Progressive Sword']))
            elif world.progressive == 'off':
                world.itempool.extend(ItemFactory(easybasicsword))
                world.itempool.extend(ItemFactory(['Fighter Sword']))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.itempool.extend(ItemFactory(easyprogressivesword))
                    world.itempool.extend(ItemFactory(['Progressive Sword']))
                else:
                    world.itempool.extend(ItemFactory(easybasicsword))
                    world.itempool.extend(ItemFactory(['Fighter Sword']))

    elif world.difficulty == 'hard':
        world.itempool.extend(ItemFactory(hardbaseitems))
        for i in range (0, 4):
            thisbottle = hardbottles[random.randint(0, 5)]
            world.itempool.append(ItemFactory(thisbottle))
        extraitems = 80
        if world.timer in ['timed', 'timed-countdown']:
            world.itempool.extend(ItemFactory(hardtimedother))
            extraitems = extraitems - 40
            world.clock_mode = 'stopwatch' if world.timer == 'timed' else 'countdown'
        elif world.timer == 'timed-ohko':
            world.itempool.extend(ItemFactory(hardtimedohko))
            extraitems = extraitems - 25
            world.clock_mode = 'ohko'
        if world.goal == 'triforcehunt':
            world.itempool.extend(ItemFactory(hardtriforcehunt))
            extraitems = extraitems - 40
            world.treasure_hunt_count = 30
            world.treasure_hunt_icon = 'Triforce Piece'
        if extraitems > 0:
            world.itempool.extend(ItemFactory(hardfirst20extra))
            extraitems = extraitems - 20
        if extraitems > 0:
            world.itempool.extend(ItemFactory(hardsecond20extra))
            extraitems = extraitems - 20
        if extraitems > 0:
            world.itempool.extend(ItemFactory(hardthird20extra))
            extraitems = extraitems - 20
        if extraitems > 0:
            world.itempool.extend(ItemFactory(hardfinal20extra))
            extraitems = extraitems - 20
        world.itempool.extend(ItemFactory(hardarmor))
        if world.progressive == 'on':
            world.itempool.extend(ItemFactory(hardprogressiveshield))
        elif world.progressive == 'off':
            world.itempool.extend(ItemFactory(hardbasicshield))
        else:
            randvalue = random.randint(0, 1)
            if (randvalue == 0):
                world.itempool.extend(ItemFactory(hardprogressiveshield))
            else:
                world.itempool.extend(ItemFactory(hardbasicshield))
        if world.mode == 'swordless':
            world.itempool.extend(ItemFactory(hardswordless))
        elif world.mode == 'standard':
            if world.progressive == 'on':
                world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(hardprogressivesword))
            elif world.progressive == 'off':
                world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(hardbasicsword))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(hardprogressivesword))
                else:
                    world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(hardbasicsword))
        else:
            if world.progressive == 'on':
                world.itempool.extend(ItemFactory(hardprogressivesword))
                world.itempool.extend(ItemFactory(['Progressive Sword']))
            elif world.progressive == 'off':
                world.itempool.extend(ItemFactory(hardbasicsword))
                world.itempool.extend(ItemFactory(['Fighter Sword']))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.itempool.extend(ItemFactory(hardprogressivesword))
                    world.itempool.extend(ItemFactory(['Progressive Sword']))
                else:
                    world.itempool.extend(ItemFactory(hardbasicsword))
                    world.itempool.extend(ItemFactory(['Fighter Sword']))

    elif world.difficulty == 'expert':
        world.itempool.extend(ItemFactory(expertbaseitems))
        thisbottle = hardbottles[random.randint(0, 5)]
        for i in range (0, 4):
            world.itempool.append(ItemFactory(thisbottle))
        extraitems = 80
        if world.timer in ['timed', 'timed-countdown']:
            world.itempool.extend(ItemFactory(experttimedother))
            extraitems = extraitems - 40
            world.clock_mode = 'stopwatch' if world.timer == 'timed' else 'countdown'
        elif world.timer == 'timed-ohko':
            world.itempool.extend(ItemFactory(experttimedohko))
            extraitems = extraitems - 25
            world.clock_mode = 'ohko'
        if world.goal == 'triforcehunt':
            world.itempool.extend(ItemFactory(experttriforcehunt))
            extraitems = extraitems - 40
            world.treasure_hunt_count = 40
            world.treasure_hunt_icon = 'Triforce Piece'
        if extraitems > 0:
            world.itempool.extend(ItemFactory(expertfirst15extra))
            extraitems = extraitems - 15
        if extraitems > 0:
            world.itempool.extend(ItemFactory(expertsecond25extra))
            extraitems = extraitems - 25
        if extraitems > 0:
            world.itempool.extend(ItemFactory(expertthird15extra))
            extraitems = extraitems - 15
        if extraitems > 0:
            world.itempool.extend(ItemFactory(expertfinal25extra))
            extraitems = extraitems - 25
        if world.mode == 'swordless':
            world.itempool.extend(ItemFactory(expertswordless))
        elif world.mode == 'standard':
            if world.progressive == 'on':
                world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(expertprogressivesword))
            elif world.progressive == 'off':
                world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(expertbasicsword))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(expertprogressivesword))
                else:
                    world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(expertbasicsword))
        else:
            if world.progressive == 'on':
                world.itempool.extend(ItemFactory(expertprogressivesword))
                world.itempool.extend(ItemFactory(['Progressive Sword']))
            elif world.progressive == 'off':
                world.itempool.extend(ItemFactory(expertbasicsword))
                world.itempool.extend(ItemFactory(['Fighter Sword']))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.itempool.extend(ItemFactory(expertprogressivesword))
                    world.itempool.extend(ItemFactory(['Progressive Sword']))
                else:
                    world.itempool.extend(ItemFactory(expertbasicsword))
                    world.itempool.extend(ItemFactory(['Fighter Sword']))

    elif world.difficulty == 'insane':
        world.itempool.extend(ItemFactory(insanebaseitems))
        thisbottle = hardbottles[random.randint(0, 5)]
        for i in range (0, 4):
            world.itempool.append(ItemFactory(thisbottle))
        extraitems = 90
        if world.timer in ['timed', 'timed-countdown']:
            world.itempool.extend(ItemFactory(insanetimedother))
            extraitems = extraitems - 40
            world.clock_mode = 'stopwatch' if world.timer == 'timed' else 'countdown'
        elif world.timer == 'timed-ohko':
            world.itempool.extend(ItemFactory(insanetimedohko))
            extraitems = extraitems - 25
            world.clock_mode = 'ohko'
        if world.goal == 'triforcehunt':
            world.itempool.extend(ItemFactory(insanetriforcehunt))
            extraitems = extraitems - 50
            world.treasure_hunt_count = 50
            world.treasure_hunt_icon = 'Triforce Piece'
        if extraitems > 0:
            world.itempool.extend(ItemFactory(insanefirst15extra))
            extraitems = extraitems - 15
        if extraitems > 0:
            world.itempool.extend(ItemFactory(insanesecond25extra))
            extraitems = extraitems - 25
        if extraitems > 0:
            world.itempool.extend(ItemFactory(insanethird10extra))
            extraitems = extraitems - 10
        if extraitems > 0:
            world.itempool.extend(ItemFactory(insanefourth15extra))
            extraitems = extraitems - 15
        if extraitems > 0:
            world.itempool.extend(ItemFactory(insanefinal25extra))
            extraitems = extraitems - 25
        if world.mode == 'swordless':
            world.itempool.extend(ItemFactory(insaneswordless))
        elif world.mode == 'standard':
            if world.progressive == 'on':
                world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(insaneprogressivesword))
            elif world.progressive == 'off':
                world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                world.get_location('Link\'s Uncle').event = True
                world.itempool.extend(ItemFactory(insanebasicsword))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.push_item('Link\'s Uncle', ItemFactory('Progressive Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(insaneprogressivesword))
                else:
                    world.push_item('Link\'s Uncle', ItemFactory('Fighter Sword'), False)
                    world.get_location('Link\'s Uncle').event = True
                    world.itempool.extend(ItemFactory(insanebasicsword))
        else:
            if world.progressive == 'on':
                world.itempool.extend(ItemFactory(insaneprogressivesword))
                world.itempool.extend(ItemFactory(['Progressive Sword']))
            elif world.progressive == 'off':
                world.itempool.extend(ItemFactory(insanebasicsword))
                world.itempool.extend(ItemFactory(['Fighter Sword']))
            else:
                randvalue = random.randint(0, 1)
                if (randvalue == 0):
                    world.itempool.extend(ItemFactory(insaneprogressivesword))
                    world.itempool.extend(ItemFactory(['Progressive Sword']))
                else:
                    world.itempool.extend(ItemFactory(insanebasicsword))
                    world.itempool.extend(ItemFactory(['Fighter Sword']))

    if world.goal == 'pedestal':
        world.push_item('Master Sword Pedestal', ItemFactory('Triforce'), False)
        world.get_location('Master Sword Pedestal').event = True

    # shuffle medallions
    mm_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    tr_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    world.required_medallions = (mm_medallion, tr_medallion)

    # distribute crystals
    crystals = ItemFactory(['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6'])
    crystal_locations = [world.get_location('Turtle Rock - Prize'), world.get_location('Eastern Palace - Prize'), world.get_location('Desert Palace - Prize'), world.get_location('Tower of Hera - Prize'), world.get_location('Palace of Darkness - Prize'),
                         world.get_location('Thieves Town - Prize'), world.get_location('Skull Woods - Prize'), world.get_location('Swamp Palace - Prize'), world.get_location('Ice Palace - Prize'),
                         world.get_location('Misery Mire - Prize')]

    random.shuffle(crystal_locations)

    fill_restrictive(world, world.get_all_state(keys=True), crystal_locations, crystals)
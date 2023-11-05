from ..logic.smbool import SMBool
import os
import sys
from pathlib import Path

# the different difficulties available
easy = 1
medium = 5
hard = 10
harder = 25
hardcore = 50
mania = 100
god = mania*2
samus = god*2
impossibru = samus*2
infinity = sys.maxsize

diff2text = {
    0: 'baby',
    easy: 'easy',
    medium: 'medium',
    hard: 'hard',
    harder: 'very hard',
    hardcore: 'hardcore',
    mania: 'mania',
    god: 'god',
    samus: 'samus',
    impossibru: 'impossibru',
    infinity: 'infinity'
}

text2diff = {
    'baby': 0,
    'easy': easy,
    'medium': medium,
    'hard': hard,
    'harder': harder,
    'very hard': harder,
    'hardcore': hardcore,
    'mania': mania,
    'god': god,
    'samus': samus,
    'impossibru': impossibru,
    'infinity': infinity
}

def diff4solver(difficulty):
    if difficulty == -1:
        return ("break", "break")
    elif difficulty < medium:
        return ("easy", "easy")
    elif difficulty < hard:
        return ("medium", "medium")
    elif difficulty < harder:
        return ("hard", "hard")
    elif difficulty < hardcore:
        return ("harder", "very hard")
    elif difficulty < mania:
        return ("hardcore", "hardcore")
    else:
        return ("mania", "mania")

# allow multiple local repo
appDir = str(Path(__file__).parents[4])

def isKnows(knows):
    return knows[0:len('__')] != '__' and knows[0] == knows[0].upper()

def isBossKnows(knows):
    ret = None
    if isKnows(knows) and 'boss' in Knows.desc[knows]:
        ret = Knows.desc[knows]['boss']
    return ret

class Knows:
    knowsDict = {}
    # the different technics to know (cf. http://deanyd.net/sm/index.php?title=Item_Randomizer)
    # and the personnal perceived difficulty.
    # False means: I can't do this technic or I don't know it.

    # store the descriptions used by the website along side the definition of the knows
    desc = {}

    # used across the game
    WallJump = SMBool(True, easy, ['WallJump'])
    desc['WallJump'] = {'display': 'Wall Jump',
                        'title': 'Kick-jump from wall: wall to wall, single wall climb',
                        'href': 'https://wiki.supermetroid.run/Walljump',
                        'rooms': [],
                        'readonly' : True}

    ShineSpark = SMBool(True, easy, ['ShineSpark'])
    desc['ShineSpark'] = {'display': 'Shinespark',
                          'title': 'With Speed Booster, press down to activate Shinespark. Then launch it in every possible direction, from ground or mid-air',
                          'href': 'https://wiki.supermetroid.run/Shinespark',
                          'rooms': [],
                          'readonly' : True}

    MidAirMorph = SMBool(True, easy, ['MidAirMorph'])
    desc['MidAirMorph'] = {'display': 'Mid-air Morph',
                           'title': 'Activate Morph Ball while jumping straight up (keep jump pressed) to reach high places in Morph Ball form without bomb jumping',
                           'href': None,
                           'rooms': [],
                           'readonly' : True}

    CrouchJump = SMBool(True, easy, ['CrouchJump'])
    desc['CrouchJump'] = {'display': 'Crouch Jump',
                          'title': 'Jump higher by crouching before jumping',
                          'href': "https://www.youtube.com/watch?v=aTbubkfc7iE",
                          'rooms': [],
                          'readonly' : True}

    UnequipItem = SMBool(True, easy, ['UnequipItem'])
    desc['UnequipItem'] = {'display': 'Unequip an item',
                          'title': 'Unequip Gravity suit to have more time to morph after jumping or unequip Hi-Jump Boots to jump to limit jump height',
                           # TODO::add a video with all the occurences
                          'href': None,
                          'rooms': ['Main Street', 'Spring Ball Room', 'West Ocean'],
                          'readonly' : True}

    Mockball = SMBool(True, easy, ['Mockball'])
    desc['Mockball'] = {'display': 'Mockball',
                        'title': 'Morph from running without loosing momentum to get Early Super and Ice Beam',
                        'href': 'https://wiki.supermetroid.run/index.php?title=Mockball',
                        'rooms': ['Early Supers Room', 'Ice Beam Gate Room']}

    SimpleShortCharge = SMBool(True, easy, ['SimpleShortCharge'])
    desc['SimpleShortCharge'] = {'display': 'Simple Short Charge',
                                 'title': 'Activate SpeedBooster faster than normal by delaying run button input',
                                 'href': 'https://wiki.supermetroid.run/index.php?title=Quick_charge',
                                 'rooms': ['Parlor and Alcatraz', 'Waterway Energy Tank Room',
                                           'Landing Site', 'Crateria Keyhunter Room', 'Blue Brinstar Energy Tank Room',
                                           'Crateria Super Room', 'Main Street', "Golden Torizo's Room"]}

    InfiniteBombJump = SMBool(True, medium, ['InfiniteBombJump'])
    desc['InfiniteBombJump'] = {'display': 'Infinite Bomb-Jump',
                                'title': 'To access certain locations without Hi-Jump or Space-Jump',
                                'href': 'https://www.youtube.com/watch?v=Qfmcm7hkXP4',
                                'rooms': ['Blue Brinstar Energy Tank Room', 'Bubble Mountain', 'Screw Attack Room', 'Mama Turtle Room', 'Plasma Room', "Draygon's Room", 'Landing Site', 'Crocomire Escape', 'Post Crocomire Farming Room', 'Post Crocomire Jump Room', 'Warehouse Entrance', 'The Worst Room In The Game', 'Mt. Everest', 'The Moat', 'Red Brinstar Fireflea Room', 'Crab Hole', 'Cathedral Entrance', 'Red Tower', 'The Precious Room']}

    GreenGateGlitch = SMBool(True, medium, ['GreenGateGlitch'])
    desc['GreenGateGlitch'] = {'display': 'Green Gate Glitch',
                               'title': 'Open gates from other side to access Screw Attack and Crocomire',
                               'href': 'https://wiki.supermetroid.run/index.php?title=Gate_Glitch',
                               'rooms': ['Green Hill Zone', 'Grapple Tutorial Room 3', 'Fast Ripper Room', 'Upper Norfair Farming Room', 'Crab Tunnel', 'Double Chamber']}

    ShortCharge = SMBool(False, 0, ['ShortCharge'])
    desc['ShortCharge'] = {'display': 'Tight Short Charge',
                           'title': 'Activate SpeedBooster really fast (3 taps or stutter 3)',
                           'href': 'https://wiki.supermetroid.run/index.php?title=Short_Charge',
                           'rooms': ['Red Tower', 'Landing Site', 'Gauntlet Energy Tank Room', 'Plasma Room',
                                     'Post Crocomire Jump Room', 'Crocomire Escape', 'Wasteland', 'Kraid Room']}

    GravityJump = SMBool(True, hard, ['GravityJump'])
    desc['GravityJump'] = {'display': 'Gravity-Jump',
                           'title': "Super Hi-Jumps in water/lava using game's bug",
                           'href': 'https://wiki.supermetroid.run/index.php?title=14%25#Gravity_Jump',
                           'rooms': ["Draygon's Room", 'The Moat', 'Lava Dive Room',
                                     'Crab Hole', 'Mt. Everest', 'The Precious Room']}

    SpringBallJump = SMBool(True, hard, ['SpringBallJump'])
    desc['SpringBallJump'] = {'display': 'SpringBall-Jump',
                              'title': 'Do a SpringBall Jump from a jump to Access to Wrecked Ship Etank without anything else, Suitless Maridia navigation',
                              'href': 'https://www.twitch.tv/videos/147442861',
                              'rooms': ['Sponge Bath', 'East Ocean',
                                        'Main Street', 'Crab Shaft', 'Pseudo Plasma Spark Room',
                                        'Mama Turtle Room', 'The Precious Room', 'Spring Ball Room', 'East Sand Hole',
                                        'Cathedral Entrance', 'Crocomire Escape', 'Post Crocomire Jump Room',
                                        'Red Brinstar Fireflea Room', 'Lower Norfair Fireflea Room']}

    SpringBallJumpFromWall = SMBool(True, harder, ['SpringBallJumpFromWall'])
    desc['SpringBallJumpFromWall'] = {'display': 'SpringBall-Jump from wall',
                                      'title': 'Do a SpringBall jump after a Wall jump to exit Screw Attack area, climb Worst Room without Hi-Jump',
                                      'href': 'https://youtu.be/3bTe2MN7mS4',
                                      'rooms': ['Screw Attack Room', 'The Worst Room In The Game', 'Bubble Mountain',
                                                'Mama Turtle Room', 'Plasma Room', 'Cathedral Entrance']}

    GetAroundWallJump = SMBool(True, hard, ['GetAroundWallJump'])
    desc['GetAroundWallJump'] = {'display': 'Get around Wall-Jump',
                                 'title': 'Tricky Wall-Jumps where you have to get around the platform you want to Wall-Jump on using Hi-Jump boots',
                                 'href': 'https://www.youtube.com/watch?v=2GPx-6ARSIw&t=137s',
                                 'rooms': ['The Worst Room In The Game',
                                           'Bubble Mountain', 'Plasma Room']}

    # bosses
    DraygonGrappleKill = SMBool(True, medium, ['DraygonGrappleKill'])
    desc['DraygonGrappleKill'] = {'display': 'Draygon Grapple Kill',
                                  'title': 'Instant kill on Draygon with electric grapple',
                                  'href': 'https://www.youtube.com/watch?v=gcemRrXqCbE',
                                  'rooms': ["Draygon's Room"],
                                  'boss': "Draygon"}

    DraygonSparkKill = SMBool(False, mania, ['DraygonSparkKill'])
    desc['DraygonSparkKill'] = {'display': 'Draygon Spark Kill',
                                'title': 'Kill Draygon using Speed Booster and shinesparks',
                                'href': None, # TODO
                                'rooms': ["Draygon's Room"],
                                'boss': "Draygon"}

    MicrowaveDraygon = SMBool(True, easy, ['MicrowaveDraygon'])
    desc['MicrowaveDraygon'] = {'display': 'Microwave Draygon',
                                'title': 'Charge/Plasma/X-Ray glitch on Draygon',
                                'href': 'https://www.youtube.com/watch?v=tj0VybUH6ZY',
                                'rooms': ["Draygon's Room"],
                                'boss': "Draygon"}

    MicrowavePhantoon = SMBool(True, medium, ['MicrowavePhantoon'])
    desc['MicrowavePhantoon'] = {'display': 'Microwave Phantoon',
                                 'title': 'Same as Draygon, with a few missiles to start',
                                 'href': 'https://youtu.be/tox6blvT5Ao',
                                 'rooms': ["Phantoon's Room"],
                                 'boss': "Phantoon"}

    # mini-bosses
    LowAmmoCroc = SMBool(False, 0, ['LowAmmoCroc'])
    desc['LowAmmoCroc'] = {'display': 'Low Ammo Crocomire fight',
                           'title': 'Use drops to fight Crocomire with no charge and just 10 missiles, or 5 missiles/5 supers. With the technique disabled and no charge beam, VARIA requires 5000 damage worth of ammo.',
                           'href': None,
                           'rooms': ["Crocomire's Room"]}

    LowStuffBotwoon = SMBool(False, 0, ['LowStuffBotwoon'])
    desc['LowStuffBotwoon'] = {'display': 'Low Ammo/Health Botwoon fight',
                              'title': 'Fight Botwoon with no charge and just 3500 damage worth of ammo (Botwoon has 3000 HP). With the technique disabled, VARIA requires 6000 damage worth of ammo (if no charge beam) and 4 tanks of energy (with no suits).',
                              'href': None,
                              'rooms': ["Botwoon's Room"]}

    LowStuffGT = SMBool(False, 0, ['LowStuffGT'])
    desc['LowStuffGT'] = {'display': 'Low Ammo/Health Golden Torizo',
                          'title': "Fight GT with either charge beam or 5 supers and nothing else. Otherwise require either 30 supers or Charge+Plasma and 4 tanks of energy (with Varia).",
                          'href': None,
                          'rooms': ["Golden Torizo's Room"]}

    # End Game
    IceZebSkip = SMBool(False, 0, ['IceZebSkip'])
    desc['IceZebSkip'] = {'display': 'Ice Zeb Skip',
                          'title': 'Skip the Zebetites with Ice beam',
                          'href': 'https://youtu.be/udowj-vMzMA',
                          'rooms': ['Mother Brain Room']}

    SpeedZebSkip = SMBool(False, 0, ['SpeedZebSkip'])
    desc['SpeedZebSkip'] = {'display': 'Speed Zeb Skip',
                            'title': 'Skip the Zebetites with a shinespark',
                            'href': 'https://www.youtube.com/watch?v=jEAgdWQ9kLQ',
                            'rooms': ['Mother Brain Room']}
    # maridia WJs
    HiJumpMamaTurtle = SMBool(False, 0, ['HiJumpMamaTurtle'])
    desc['HiJumpMamaTurtle'] = {'display': 'Mama Turtle E-Tank with High-Jump+Speed',
                                'title': 'Access Mama Turtle E-Tank with High-Jump and Speed Booster (and Morph or X-Ray to turn around without moving)',
                                'href': 'https://www.youtube.com/watch?v=1DINqLnINc8',
                                'rooms': ['Mama Turtle Room']}

    MaridiaWallJumps = SMBool(True, medium, ['MaridiaWallJumps'])
    desc['MaridiaWallJumps'] = {'display': 'Various Maridia wall jumps',
                                'title': 'Kinda tricky wall jumps to: access items in West Sand Hole without Spring Ball or Bombs, exit Spring Ball area without Hi Jump, exit Crab Hole with Gravity+Hi-Jump',
                                'href': 'https://youtu.be/F3xAJem6VlA',
                                'rooms': ['West Sand Hole', 'Spring Ball Room', 'Crab Hole']}

    MtEverestGravJump = SMBool(False, 0, ['MtEverestGravJump'])
    desc['MtEverestGravJump'] = {'display': 'Mount Everest Gravity Jump',
                                'title': 'Access Mount Everest top door by doing a crouch+gravity jump in the last couple frames possible',
                                'href': 'https://www.youtube.com/watch?v=sZLEzdTgJbI',
                                'rooms': ['Mt. Everest']}

    # underwater grav-less
    GravLessLevel1 = SMBool(True, hardcore, ['GravLessLevel1'])
    desc['GravLessLevel1'] = {'display': 'Level 1',
                              'title': 'Make your way underwater with Hi-Jump and Ice, freezing crabs and fishes. Access Botwoon with grapple.',
                              'href': 'https://www.youtube.com/watch?v=c2xoPigezvM',
                              'rooms': ['Main Street', 'Mt. Everest', 'Crab Shaft', 'Pseudo Plasma Spark Room',
                                        'Aqueduct', 'Botwoon Hallway', "Botwoon's Room", 'Botwoon Energy Tank Room',
                                        'Crab Hole', 'Crab Tunnel', 'East Ocean']}

    GravLessLevel2 = SMBool(False, 0, ['GravLessLevel2'])
    desc['GravLessLevel2'] = {'display': 'Level 2',
                              'title': "Level 1 + access Draygon's lair and do the Draygon fight (exiting Draygon are separate techniques)",
                              'href': None,
                              'rooms': ['Halfie Climb Room', 'Colosseum', 'The Precious Room', "Draygon's Room",
                                        'East Cactus Alley Room', 'West Cactus Alley Room']}

    GravLessLevel3 = SMBool(False, 0, ['GravLessLevel3'])
    desc['GravLessLevel3'] = {'display': 'Level 3',
                               'title': 'Level 2 and : no problem getting out of sand suitless, traverse mini-draygons area, wall jumps to access items in the left sand pit, access missile location in the right sand pit.',
                               'href': 'https://www.youtube.com/watch?v=Fn2z0ByOcj4',
                               'rooms': ['West Sand Hole', 'East Sand Hole',
                                         'West Sand Hall', 'East Sand Hall']}
    # Area difficulties

    # Brinstar
    CeilingDBoost = SMBool(True, easy, ['CeilingDBoost'])
    desc['CeilingDBoost'] = {'display': 'Ceiling Damage Boost',
                             'title': 'Hit an enemy at the right time to get the item in Blue Brinstar Ceiling',
                             'href': 'https://www.metroid2002.com/3/early_items_blue_brinstar_energy_tank.php',
                             'rooms': ['Blue Brinstar Energy Tank Room']}

    BillyMays = SMBool(True, easy, ['BillyMays'])
    desc['BillyMays'] = {'display': 'Billy Mays access without Gravity or Space Jump',
                         'title': 'Jump through the door to get on the invisible platform',
                         'href': 'https://youtu.be/LOyj4CuOWik',
                         'rooms': ['Blue Brinstar Boulder Room']}

    AlcatrazEscape = SMBool(True, harder, ['AlcatrazEscape'])
    desc['AlcatrazEscape'] = {'display': 'Alcatraz Escape',
                              'title': 'Escape from Bomb area using its entrance tunnel',
                              'href': 'https://www.youtube.com/watch?v=XSBeLJJafjY',
                              'rooms': ['Parlor and Alcatraz']}

    ReverseGateGlitch = SMBool(True, medium, ['ReverseGateGlitch'])
    desc['ReverseGateGlitch'] = {'display': 'Reverse Gate Glitch',
                                 'title': 'Open wave gate in Pink Brinstar from bottom left corner with Hi-Jump',
                                 'href': 'https://wiki.supermetroid.run/Pink_Brinstar_Hopper_Room',
                                 'rooms': ['Pink Brinstar Hopper Room']}

    ReverseGateGlitchHiJumpLess = SMBool(False, 0, ['ReverseGateGlitchHiJumpLess'])
    desc['ReverseGateGlitchHiJumpLess'] = {'display': 'Reverse Gate Glitch w/o Hi-Jump',
                                           'title': 'Open wave gate in Pink Brinstar from bottom left corner without Hi-Jump',
                                           'href': 'https://wiki.supermetroid.run/Pink_Brinstar_Hopper_Room',
                                           'rooms': ['Pink Brinstar Hopper Room']}

    EarlyKraid = SMBool(True, easy, ['EarlyKraid'])
    desc['EarlyKraid'] = {'display': 'Early Kraid',
                          'title': 'Access Kraid area by Wall-Jumping',
                          'href': 'https://www.youtube.com/watch?v=rHMHqTHHqHs',
                          'rooms': ['Warehouse Entrance']}

    XrayDboost = SMBool(False, 0, ['XrayDboost'])
    desc['XrayDboost'] = {'display': 'X-Ray Damage Boost',
                          'title': 'Get to X-Ray location without Space-Jump, Grapple (no energy requirements), Ice+Hi-Jump or Bombs (see Hard Room settings)',
                          'href': 'https://www.twitch.tv/videos/168724062',
                          'rooms': ['Red Brinstar Fireflea Room']}

    XrayIce = SMBool(True, hard, ['XrayIce'])
    desc['XrayIce'] = {'display': 'X-Ray Ice Climb',
                       'title': 'Get to X-Ray location with Ice beam and no Hi-Jump (see Hard Room settings for energy requirements)',
                       'href': 'https://www.youtube.com/watch?v=j36noNULtI8',
                       'rooms': ['Red Brinstar Fireflea Room']}

    RedTowerClimb = SMBool(True, harder, ['RedTowerClimb'])
    desc['RedTowerClimb'] = {'display': 'Red Tower Climb',
                             'title': 'Climb Red Tower without Ice or Space-Jump',
                             'href': 'https://www.youtube.com/watch?v=g3goe6PZ4o0',
                             'rooms': ['Red Tower']}

    RonPopeilScrew = SMBool(False, 0, ['RonPopeilScrew'])
    desc['RonPopeilScrew'] = {'display': 'Bomb-less Ron Popeil Missiles',
                              'title': 'Access the most behind missile in Green Brinstar Reserve with Morph and Screw Attack',
                              'href': 'https://wiki.supermetroid.run/Brinstar_Reserve_Tank_Room',
                              'rooms': ['Brinstar Reserve Tank Room']}

    OldMBWithSpeed = SMBool(False, mania, ['OldMBWithSpeed'])
    desc['OldMBWithSpeed'] = {'display': 'Old Mother Brain with Speed',
                              'title': 'Access Old Mother Brain Missile pack location with just the Speed Booster',
                              'href': 'https://www.youtube.com/watch?v=-SO2QykqnZw',
                              'rooms': ['Climb', 'Pit Room']}

    Moondance = SMBool(False, mania, ['Moondance'])
    desc['Moondance'] = {'display': 'Moondance',
                         'title': 'Access Etecoons area using moonfall shenanigans',
                         'href': 'http://crocomi.re/92',
                         'rooms': ['Green Brinstar Main Shaft']}
    # Gauntlet
    HiJumpLessGauntletAccess = SMBool(False, 0, ['HiJumpLessGauntletAccess'])
    desc['HiJumpLessGauntletAccess'] = {'display': 'Gauntlet Access w/o Hi-Jump',
                                        'title': 'Access Gauntlet area using really tricky Wall-Jumps',
                                        'href': 'https://www.youtube.com/watch?v=uVU2X-egOTI&t=25s',
                                        'rooms': ['Landing Site']}

    HiJumpGauntletAccess = SMBool(True, harder, ['HiJumpGauntletAccess'])
    desc['HiJumpGauntletAccess'] = {'display': 'Hi-Jump Gauntlet Access',
                                    'title': 'Access Gauntlet area using tricky Wall-Jumps',
                                    'href': 'https://www.youtube.com/watch?v=2a6mf-kB60U',
                                    'rooms': ['Landing Site']}

    LowGauntlet = SMBool(False, 0, ['LowGauntlet'])
    desc['LowGauntlet'] = {'display': 'Gauntlet Minors Access',
                           'title': 'Access Gauntlet minors with SpeedBooster, 1 Etank and 1 Power Bomb pack',
                           'href': 'https://www.youtube.com/watch?v=JU6BFcjuR4c',
                           'rooms': ['Landing Site', 'Gauntlet Entrance', 'Gauntlet Energy Tank Room']}

    # Norfair
    IceEscape = SMBool(False, 0, ['IceEscape'])
    desc['IceEscape'] = {'display': 'Ice Escape',
                         'title': 'Freeze the platforms and exit Ice Beam area without bombs',
                         'href': 'https://www.youtube.com/watch?v=lFJPqu8qk54',
                         'rooms': ['Ice Beam Acid Room']}

    WallJumpCathedralExit = SMBool(True, easy, ['WallJumpCathedralExit'])
    desc['WallJumpCathedralExit'] = {'display': 'Wall Jump to exit Cathedral',
                                     'title': 'Use a delayed wall jump to exit Cathedral',
                                     'href': 'https://www.youtube.com/watch?v=CqQik2z6IkE',
                                     'rooms': ['Cathedral Entrance']}

    BubbleMountainWallJump = SMBool(True, medium, ['BubbleMountainWallJump'])
    desc['BubbleMountainWallJump'] = {'display': 'Bubble Mountain wall jump',
                                      'title': 'Run from the save room and get up Bubble Mountain without Hi-Jump',
                                      'href': 'https://youtu.be/2RmbFRCMlUg',
                                      'rooms': ['Bubble Mountain']}

    DoubleChamberWallJump = SMBool(True, easy, ['DoubleChamberWallJump'])
    desc['DoubleChamberWallJump'] =  {'display': 'Double Chamber wall jump',
                                      'title': 'Climb up Double Chamber (pre-Wave Beam room) after entering through the bottom door',
                                      'href': 'https://www.youtube.com/watch?v=MVaaoW8Y_VU',
                                      'rooms': ['Double Chamber']}

    NovaBoost = SMBool(False, 0, ['NovaBoost'])
    desc['NovaBoost'] = {'display': 'Nova Boost',
                         'title': 'Use a D-Boost on the Sova to enter Cathedral',
                         'href': 'https://www.twitch.tv/videos/144055441',
                         'rooms': ['Cathedral Entrance']}

    NorfairReserveDBoost = SMBool(False, 0, ['NorfairReserveDBoost'])
    desc['NorfairReserveDBoost'] = {'display': 'Norfair Reserve Damage Boost',
                                    'title': 'Use a D-Boost to reach Norfair Reserve area',
                                    'href': 'https://youtu.be/PglBIsdAiFI',
                                    'rooms': ['Bubble Mountain']}

    CrocPBsDBoost = SMBool(False, 0, ['CrocPBsDBoost'])
    desc['CrocPBsDBoost'] = {'display': 'Crocomire Power Bombs Damage Boost',
                             'title': 'Use a D-Boost to reach Crocomire Power Bombs',
                             'href': 'https://youtu.be/ld8FC_Q9c6Y',
                             'rooms': ['Post Crocomire Farming Room']}

    CrocPBsIce = SMBool(False, 0, ['CrocPBsIce'])
    desc['CrocPBsIce'] = {'display': 'Crocomire Power Bombs with Ice Beam',
                          'title': 'Get the farm bugs up and freeze them to reach Crocomire Power Bombs',
                          'href': 'https://www.youtube.com/watch?v=ERer642mil8',
                          'rooms': ['Post Crocomire Farming Room']}

    IceMissileFromCroc = SMBool(False, 0, ['IceMissileFromCroc'])
    desc['IceMissileFromCroc'] = {'display': 'Missile under Ice beam from Crocomire',
                                  'title': 'Access missile pack under Ice beam location by reverse sparking Crocomire speedway',
                                  'href': 'https://clips.twitch.tv/CrackyConfidentMomEagleEye',
                                  'rooms': ['Crocomire Speedway']}

    FrogSpeedwayWithoutSpeed = SMBool(False, 0, ['FrogSpeedwayWithoutSpeed'])
    desc['FrogSpeedwayWithoutSpeed'] = {'display': 'Frog speedway without speed',
                                        'title': 'Traverse frog speedway from right to left, without Speed Booster, but with Wave and either Spazer or Plasma',
                                        'href': 'https://puu.sh/CvsCT/7757bb4f62.mp4',
                                        'rooms': ['Frog Speedway']}

    LavaDive = SMBool(True, harder, ['LavaDive'])
    desc['LavaDive'] = {'display': 'Lava Dive',
                        'title': 'Enter Lower Norfair with Varia and Hi-Jump',
                        'href': 'https://www.youtube.com/watch?v=pdyBy_54dB0',
                        'rooms': ['Lava Dive Room']}

    LavaDiveNoHiJump = SMBool(False, 0, ['LavaDiveNoHiJump'])
    desc['LavaDiveNoHiJump'] = {'display': 'Hi-Jump less Lava Dive',
                                'title': 'Enter Lower Norfair with just the Varia suit',
                                'href': 'https://www.youtube.com/watch?v=qmlSDfw8FXQ',
                                'rooms': ['Lava Dive Room']}

    WorstRoomIceCharge = SMBool(True, mania, ['WorstRoomIceCharge'])
    desc['WorstRoomIceCharge'] = {'display': 'Worst Room Ice and Charge',
                                  'title': 'Go through Worst Room In The Game JUST by freezing pirates',
                                  'href': 'https://www.youtube.com/watch?v=AYK7LREbLI8',
                                  'rooms': ['The Worst Room In The Game']}

    WorstRoomWallJump = SMBool(False, 0, ['WorstRoomWallJump'])
    desc['WorstRoomWallJump'] = {'display': 'Worst Room insane wall jump',
                                  'title': 'Do the frame+pixel perfect wall jump to get out Worst Room without Hi-Jump',
                                  'href': 'https://clips.twitch.tv/FuriousHeartlessArugulaStrawBeary',
                                  'rooms': ['The Worst Room In The Game']}

    ScrewAttackExit = SMBool(True, medium, ['ScrewAttackExit'])
    desc['ScrewAttackExit'] = {'display': 'Screw Attack Exit',
                               'title': 'Gain momentum with Hi-Jump and Speed Booster from Golden Torizo Energy Recharge room, then Wall Jump in Screw Attack room, destroying the ceiling with Screw Attack.',
                               'href': 'https://youtu.be/l-L6zzpqim4',
                               'rooms': ['Screw Attack Room']}

    ScrewAttackExitWithoutScrew = SMBool(False, 0, ['ScrewAttackExitWithoutScrew'])
    desc['ScrewAttackExitWithoutScrew'] = {'display': 'Screw Attack Exit without Screw',
                                           'title': 'Destroy the ceiling, then jump from inside the door with Hi-Jump and Speed Booster to climb up in Screw Attack room',
                                           'href': 'https://youtu.be/2Ws0Zokg-SQ',
                                           'rooms': ['Screw Attack Room']}

    FirefleasWalljump = SMBool(False, 0, ['FirefleasWalljump'])
    desc['FirefleasWalljump'] = {'display': 'Firefleas Wall Jump',
                                 'title': 'Get back up from bottom of firefleas without movement items or Ice Beam',
                                 'href': 'https://youtu.be/tp4V9aNKp64',
                                 'rooms': ['Lower Norfair Fireflea Room']}

    DodgeLowerNorfairEnemies = SMBool(False, 0, ['DodgeLowerNorfairEnemies'])
    desc['DodgeLowerNorfairEnemies'] = {'display': 'Dodge Lower Norfair Enemies',
                                        'title': 'Go through hard-hitting enemies in Lower Norfair without taking damage or killing them',
                                        'href': 'https://www.youtube.com/watch?v=5yuBK0YFulA',
                                        'rooms': ["Three Musketeers' Room", "Wasteland", 'Red Kihunter Shaft', 'The Worst Room In The Game']}

    # wrecked ship
    ContinuousWallJump = SMBool(False, 0, ['ContinuousWallJump'])
    desc['ContinuousWallJump'] = {'display': 'Continuous Wall-Jump',
                                  'title': 'Get over the Moat using CWJ',
                                  'href': 'https://www.youtube.com/watch?v=4HVhTwwax6g',
                                  'rooms': ['The Moat']}

    DiagonalBombJump = SMBool(True, mania, ['DiagonalBombJump'])
    desc['DiagonalBombJump'] = {'display': 'Diagonal Bomb-Jump',
                                'title': 'Get over The Moat using Bomb-Jumps',
                                'href': 'https://www.youtube.com/watch?v=9Q8WGKCVb40',
                                'rooms': ['The Moat']}

    MockballWs = SMBool(True, hardcore, ['MockballWs'])
    desc['MockballWs'] = {'display': 'Mockball Wrecked Ship',
                          'title': 'Get over the moat using Mockball and Spring Ball',
                          'href': 'https://www.youtube.com/watch?v=WYxtRF--834',
                          'rooms': ['The Moat']}

    # wrecked ship etank access ("sponge bath" room)
    SpongeBathBombJump = SMBool(True, mania, ['SpongeBathBombJump'])
    desc['SpongeBathBombJump'] = {'display': 'SpongeBath Bomb-Jump',
                                  'title': 'Get through Sponge Bath room with Bomb-Jumps',
                                  'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw',
                                  'rooms': ['Sponge Bath']}

    SpongeBathHiJump = SMBool(True, easy, ['SpongeBathHiJump'])
    desc['SpongeBathHiJump'] = {'display': 'SpongeBath Hi-Jump',
                                'title': 'Get through sponge bath room with Hi-Jump and Wall-Jumps',
                                'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw',
                                'rooms': ['Sponge Bath']}

    SpongeBathSpeed = SMBool(True, medium, ['SpongeBathSpeed'])
    desc['SpongeBathSpeed'] = {'display': 'SpongeBath Speed',
                               'title': 'Get through sponge bath room with Speed Booster and Wall-Jumps',
                               'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw',
                               'rooms': ['Sponge Bath']}

    # Maridia
    # Suitless
    TediousMountEverest = SMBool(False, 0, ['TediousMountEverest'])
    desc['TediousMountEverest'] = {'display': 'Mt. Everest without anything',
                                    'title': 'Make your way through Mt. Everest with nothing but Ice and Hi-Jump',
                                    'href': 'https://www.youtube.com/watch?v=chFbX9rRV_k&t=123s',
                                    'rooms': ['Mt. Everest']}

    DoubleSpringBallJump = SMBool(False, 0, ['DoubleSpringBallJump'])
    desc['DoubleSpringBallJump'] = {'display': 'Double SpringBall-Jump',
                                    'title': 'With Hi-Jump boots do two SpringBall-Jumps in a row',
                                    'href': 'https://youtu.be/KohE3e8sGLQ',
                                    'rooms': ['Mt. Everest', "Draygon's Room", 'Halfie Climb Room']}

    BotwoonToDraygonWithIce = SMBool(False, 0, ['BotwoonToDraygonWithIce'])
    desc['BotwoonToDraygonWithIce'] = {'display': 'Botwoon to Draygon with Ice',
                                        'title': 'When past Botwoon, access Draygon using Hi-Jump and Ice only',
                                        'href': 'https://www.twitch.tv/videos/480882188',
                                        'rooms': ['Halfie Climb Room', 'Colosseum']}

    WestSandHoleSuitlessWallJumps = SMBool(False, 0, ['WestSandHoleSuitlessWallJumps'])
    desc['WestSandHoleSuitlessWallJumps'] = {'display': 'West Sand Hole suitless Wall Jumps',
                                     'title': 'Access items in West Sand Hole (aka Left Sand Pit) with just Hi-Jump',
                                     'href': 'https://www.youtube.com/watch?v=Fn2z0ByOcj4',
                                     'rooms': ['West Sand Hole']}

    # Suitless Draygon
    DraygonRoomGrappleExit = SMBool(False, 0, ['DraygonRoomGrappleExit'])
    desc['DraygonRoomGrappleExit'] = {'display': 'Exit Draygon room with the Grapple',
                                      'title': 'Use Grapple to bounce them morph and demorph up to the platform',
                                      'href': 'https://www.youtube.com/watch?v=i2OGuFpcfiw&t=154s',
                                      'rooms': ["Draygon's Room"]}

    DraygonRoomCrystalFlash = SMBool(False, 0, ['DraygonRoomCrystalFlash'])
    desc['DraygonRoomCrystalFlash'] = {'display': 'Exit Draygon room or precious room with a shine spark',
                                       'title': 'Doing a Crystal flash and being grabbed by Draygon gives a free shine spark',
                                       'href': 'https://www.youtube.com/watch?v=hrHHfvGD3wo&t=625s',
                                       'rooms': ["Draygon's Room"]}

    PreciousRoomXRayExit = SMBool(False, 0, ['PreciousRoomXRayExit'])
    desc['PreciousRoomXRayExit'] = {'display': 'Exit the Precious room with an Xray glitch',
                                    'title': 'Use an XrayScope glitch to climb out of the Precious room',
                                    'href': 'https://www.youtube.com/watch?v=i2OGuFpcfiw&t=160s',
                                    'rooms': ['The Precious Room']}

    PreciousRoomGravJumpExit = SMBool(False, 0, ['PreciousRoomGravJumpExit'])
    desc['PreciousRoomGravJumpExit'] = {'display': 'Exit the Precious room with a Gravity Jump',
                                        'title': 'Jump through the exit door into the water in the next room to climb up with a Gravity Jump',
                                        'href': 'https://www.twitch.tv/jooniejoone/clip/StylishVainPorcupineVoHiYo',
                                        'rooms': ['The Precious Room', 'Colosseum']}

    # clips
    MochtroidClip = SMBool(True, medium, ['MochtroidClip'])
    desc['MochtroidClip'] = {'display': 'Mochtroid Clip',
                             'title': 'Get to Botwoon with Ice Beam',
                             'href': 'https://wiki.supermetroid.run/index.php?title=14%25#Mochtroid_Clip',
                             'rooms': ['Botwoon Hallway']}

    PuyoClip = SMBool(False, 0, ['PuyoClip'])
    desc['PuyoClip'] = {'display': 'Puyo Clip',
                        'title': 'Get to Spring Ball with Gravity Suit and Ice Beam',
                        'href': 'https://www.youtube.com/watch?v=e5ZH_9paSLw',
                        'rooms': ['Pants Room']}

    PuyoClipXRay = SMBool(False, 0, ['PuyoClipXRay'])
    desc['PuyoClipXRay'] = {'display': 'Puyo Clip with X-Ray',
                            'title': 'Get to Spring Ball with Gravity Suit, Ice Beam and X-Ray',
                            'href': 'https://youtu.be/83JajzNyZtQ',
                            'rooms': ['Pants Room']}

    SnailClip = SMBool(False, 0, ['SnailClip'])
    desc['SnailClip'] = {'display': 'Snail Clip',
                         'title': 'Access Aqueduct Missile and Super Missile without SpeedBooster',
                         'href': 'https://www.youtube.com/watch?v=fBQubU6h11U&t=70s',
                         'rooms': ['Aqueduct']}

    SuitlessPuyoClip = SMBool(False, 0, ['SuitlessPuyoClip'])
    desc['SuitlessPuyoClip'] = {'display': 'Suitless Puyo Clip',
                                'title': 'Do the Puyo clip with Hi Jump and without Gravity',
                                'href': 'https://snipaclip.com/watch/HomelyImpartialVampireFloof',
                                'rooms': ['Pants Room']}

    CrystalFlashClip = SMBool(False, 0, ['CrystalFlashClip'])
    desc['CrystalFlashClip'] = {'display': 'Crystal Flash Clip',
                               'title': 'Use a Crystal Flash to clip through crumble blocks to get to Botwoon or Shaktool, using Gravity and Bombs',
                               'href': 'https://www.youtube.com/watch?v=z2c3u8ICO6A',
                               'rooms': ['Botwoon Hallway', 'East Pants Room']}

    SuitlessCrystalFlashClip = SMBool(False, 0, ['SuitlessCrystalFlashClip'])
    desc['SuitlessCrystalFlashClip'] = {'display': 'Suitless Crystal Flash Clip',
                               'title': 'Use a Crystal Flash to clip through crumble blocks to get to Botwoon or Shaktool',
                               'href': 'https://www.youtube.com/watch?v=BUzmHsk0H7k',
                               'rooms': ['Botwoon Hallway', 'East Pants Room']}

    # plasma room
    KillPlasmaPiratesWithSpark = SMBool(False, 0, ['KillPlasmaPiratesWithSpark'])
    desc['KillPlasmaPiratesWithSpark'] = {'display': 'Kill Plasma Pirates with Spark',
                                          'title': 'Use shinesparks to kill the pirates in Plasma Beam room',
                                          'href': 'https://youtu.be/nORE1HkP64E',
                                          'rooms': ['Plasma Room']}

    KillPlasmaPiratesWithCharge = SMBool(True, hard, ['KillPlasmaPiratesWithCharge'])
    desc['KillPlasmaPiratesWithCharge'] = {'display': 'Kill Plasma Pirates with Charge',
                                           'title': 'Use pseudo-screw to kill the pirates in Plasma Beam room',
                                           'href': 'https://youtu.be/hn6nrjUGmSk',
                                           'rooms': ['Plasma Room']}

    # spring ball access
    AccessSpringBallWithHiJump = SMBool(True, easy, ['AccessSpringBallWithHiJump'])
    desc['AccessSpringBallWithHiJump'] = {'display': 'Access Spring Ball location with Hi-Jump',
                                          'title': 'With Gravity and Hi-Jump, jump to get through the grapple hole',
                                          'href': 'https://youtu.be/mHiSd3kebHo',
                                          'rooms': ['Pants Room']}

    AccessSpringBallWithSpringBallBombJumps = SMBool(False, 0, ['AccessSpringBallWithSpringBallBombJumps'])
    desc['AccessSpringBallWithSpringBallBombJumps'] = {'display': 'Access Spring Ball location with bomb jumps and spring ball',
                                                       'title': 'With Gravity, bounce on the sand and bomb jump up to get through the grapple hole',
                                                       'href': 'https://youtu.be/VbR6z3aZuWg',
                                                       'rooms': ['Pants Room']}

    AccessSpringBallWithBombJumps = SMBool(False, 0, ['AccessSpringBallWithBombJumps'])
    desc['AccessSpringBallWithBombJumps'] = {'display': 'Access Spring Ball location with bomb jumps only',
                                             'title': 'With Gravity, bomb jump up from the sand to get through the grapple hole',
                                             'href': 'https://youtu.be/8s_Tng-3oZM',
                                             'rooms': ['Pants Room']}

    AccessSpringBallWithSpringBallJump = SMBool(False, 0, ['AccessSpringBallWithSpringBallJump'])
    desc['AccessSpringBallWithSpringBallJump'] = {'display': 'Access Spring Ball location with a spring ball jump',
                                                  'title': 'With Gravity, use a spring ball jump, either from the sand or a ledge to get through the grapple hole',
                                                  'href': 'https://youtu.be/YrmAqwJxbYs',
                                                  'rooms': ['Pants Room']}

    AccessSpringBallWithXRayClimb = SMBool(False, 0, ['AccessSpringBallWithXRayClimb'])
    desc['AccessSpringBallWithXRayClimb'] = {'display': 'Access Spring Ball location with X-Ray climbing',
                                             'title': 'Use inbounds X-Ray climbing to get past the grapple hole. Can be required suitless if suitless movement level 3 is enabled.',
                                             'href': 'https://youtu.be/I-f5X5cNypA',
                                             'rooms': ['Pants Room']}

    AccessSpringBallWithGravJump = SMBool(False, 0, ['AccessSpringBallWithGravJump'])
    desc['AccessSpringBallWithGravJump'] = {'display': 'Access Spring Ball location with a Gravity jump',
                                             'title': 'Do a tricky gravity jump from the sand and get through the grapple hole',
                                             'href': 'https://www.twitch.tv/videos/480378897',
                                             'rooms': ['Pants Room']}

    AccessSpringBallWithFlatley = SMBool(False, 0, ['AccessSpringBallWithFlatley'])
    desc['AccessSpringBallWithFlatley'] = {'display': 'Access Spring Ball location suitless with a flatley jump and Space Jump',
                                           'title': 'Do a suitless flatley jump to get through the grapple hole, and get out of the water with Space Jump',
                                           'href': 'https://www.youtube.com/watch?v=8JHsAGeUdhQ',
                                           'rooms': ['Pants Room']}

    categories = {
        'Common': [
            {'knows': ['WallJump', 'ShineSpark', 'MidAirMorph', 'CrouchJump', 'UnequipItem'],
             'title': 'Basics'},
            {'knows': ['Mockball', 'SimpleShortCharge', 'InfiniteBombJump', 'GreenGateGlitch',
                       'GravityJump', 'GetAroundWallJump',
                       'SpringBallJump', 'SpringBallJumpFromWall', 'ShortCharge'],
             'title': 'Used across the game'}
        ],
        'Crateria/Brinstar': [
            {'knows': ['AlcatrazEscape', 'HiJumpGauntletAccess', 'HiJumpLessGauntletAccess', 'LowGauntlet', 'OldMBWithSpeed'],
             'title': 'Crateria'},
            {'knows': ['CeilingDBoost', 'BillyMays', 'EarlyKraid',
                       'ReverseGateGlitch', 'ReverseGateGlitchHiJumpLess',
                       'RedTowerClimb', 'XrayDboost', 'XrayIce',
                       'RonPopeilScrew', 'Moondance'],
             'title': 'Brinstar'}
        ],
        'Wrecked Ship': [
            {'knows': ['ContinuousWallJump', 'DiagonalBombJump', 'MockballWs'],
             'title': 'Access'},
            {'knows': ['SpongeBathHiJump', 'SpongeBathSpeed', 'SpongeBathBombJump'],
             'title': 'Sponge Bath'}
        ],
        'Maridia 1/2': [
            {'knows': ['GravLessLevel1', 'GravLessLevel2', 'GravLessLevel3'],
             'title': 'Underwater movement without Gravity Suit'},
            {'knows': ['MochtroidClip', 'PuyoClip', 'PuyoClipXRay',
                       'SnailClip', 'CrystalFlashClip'],
             'title': 'Clips'},
            {'knows': ['KillPlasmaPiratesWithCharge', 'KillPlasmaPiratesWithSpark'],
             'title': 'Plasma Room'},
            {'knows': ['HiJumpMamaTurtle', 'MaridiaWallJumps', 'MtEverestGravJump'],
             'title': 'Jumps'}
        ],
        'Maridia 2/2': [
            {'knows': ['AccessSpringBallWithHiJump', 'AccessSpringBallWithSpringBallBombJumps',
                       'AccessSpringBallWithBombJumps', 'AccessSpringBallWithSpringBallJump',
                       'AccessSpringBallWithGravJump', 'AccessSpringBallWithXRayClimb', 'AccessSpringBallWithFlatley'],
             'title': 'Spring Ball Access'},
            {'knows': ['DraygonRoomGrappleExit', 'DraygonRoomCrystalFlash', 'PreciousRoomXRayExit', 'PreciousRoomGravJumpExit'],
             'title': 'Suitless Draygon Exit'},
            {'knows': ['WestSandHoleSuitlessWallJumps', 'DoubleSpringBallJump', 'TediousMountEverest',
                       'BotwoonToDraygonWithIce', 'SuitlessCrystalFlashClip',
                       'SuitlessPuyoClip'],
             'title': 'Obscure suitless stuff'}
        ],
        'Upper Norfair': [
            {'knows': ['WallJumpCathedralExit', 'IceEscape', 'FrogSpeedwayWithoutSpeed', 'NovaBoost'],
              'title': 'Main Upper Norfair'},
            {'knows': ['BubbleMountainWallJump', 'NorfairReserveDBoost', 'DoubleChamberWallJump'],
             'title': 'Bubble Mountain'},
            {'knows': ['CrocPBsIce', 'CrocPBsDBoost', 'IceMissileFromCroc'],
             'title': 'Crocomire'}
        ],
        'Lower Norfair': [
            {'knows': ['LavaDive', 'LavaDiveNoHiJump'],
              'title': 'Access'},
            {'knows': ['ScrewAttackExit', 'ScrewAttackExitWithoutScrew'],
              'title': 'Screw Attack'},
            {'knows': ['WorstRoomIceCharge', 'WorstRoomWallJump'],
              'title': 'Worst Room In The Game'},
            {'knows': [ 'FirefleasWalljump', 'DodgeLowerNorfairEnemies'],
             'title': 'Other'}
        ],
        'Bosses/End': [
            {'knows': ['DraygonGrappleKill', 'DraygonSparkKill', 'MicrowaveDraygon', 'MicrowavePhantoon'],
             'title': 'Bosses'},
            {'knows': ['LowAmmoCroc', 'LowStuffBotwoon', 'LowStuffGT'],
             'title': 'Mini-Bosses'},
            {'knows': ['IceZebSkip', 'SpeedZebSkip'],
             'title': 'End Game'}
        ]
    }

    def knows(self, name, diff):
        k = getattr(self, name)
        return k.bool and k.difficulty <= diff

def isSettings(settings):
    return settings[0:len('__')] != '__'

class Settings:
    SettingsDict = {}
    # boss difficulty tables :
    #
    # key is boss name. value is a dictionary where you define:
    #
    # 1. Rate : the rate of time in which you can land shots. For example
    # : 0.5 means you can land shots half the time in the boss (30secs in
    # a given minute). It represents a combination of the fraction of the
    # time you can hit the boss and your general accuracy against the boss.
    # If no information is given here, the fight will be
    # considered to be 2 minutes, regardless of anything else.
    #
    # 2. Energy : a dictionary where key is total energy you have divided by 100
    # (the initial 99 energy count as 1).
    # value is estimated difficulty *for a 2-minute fight*, with Varia
    # suit only.
    # If not defined, the one below will be chosen, or the minimum one if
    # no below entry is defined. You can give any difficulty number
    # instead of the fixed values defined above.
    #
    # Actual difficulty calculation will also take into account estimated
    # fight duration. Difficulty will be multiplied with the ratio against
    # 2-minutes value entered here. The ammo margin will also be
    # considered if you do not have charge.
    #
    # If not enough info is provided here, base difficulty will be medium.

    # logic behind the presets : the ones where you find the boss difficult are
    # calibrated to give 'hard' in vanilla situations, the default are calibrated
    # to give 'medium' in vanilla situations, just above gives 'easy' in vanilla
    # situations, and top settings basically discards the boss except for extreme
    # situations (very low energy or firepower)
    bossesDifficultyPresets = {
        'Kraid' : {
            "He's annoying" : {
                'Rate' : 0.0075,
                'Energy' : {
                    0.5 : hard,
                    1 : medium,
                    2 : easy
                }
            },
            'Default' : {
                'Rate' : 0.015,
                'Energy' : {
                    0.5 : hard,
                    1.5 : medium,
                    2.5 : easy
                }
            },
            'Quick Kill' : {
                'Rate' : 1,
                'Energy' : {
                    0.5 : easy
                }
            }
        },
        'Phantoon' : {
            'A lot of trouble' : {
                'Rate' : 0.01,
                'Energy' : {
                    1.5 : mania,
                    3 : hardcore,
                    4 : harder,
                    5 : hard,
                    7 : medium,
                    10 : easy
                }
            },
            'Default' : {
                'Rate' : 0.015,
                'Energy' : {
                    0.5 : samus,
                    1 : mania,
                    2 : hardcore,
                    4 : harder,
                    5 : hard,
                    6 : medium,
                    10 : easy
                }
            },
            'Used to it' : {
                'Rate' : 0.02,
                'Energy' : {
                    0.5 : 150,
                    1 : (mania+hardcore)/2,
                    2 : harder,
                    2.5 : hard,
                    4 : medium,
                    6 : easy
                }
            },
            'No problemo' : {
                'Rate' : 0.02,
                'Energy' : {
                    0.5 : harder,
                    1 : hard,
                    2 : medium,
                    3 : easy
                }
            }
        },
        'Draygon' : {
            'A lot of trouble' : {
                'Rate' : 0.025,
                'Energy' : {
                    1 : mania,
                    6 : hardcore,
                    8 : harder,
                    11 : hard,
                    14 : medium,
                    20 : easy
                },
            },
            'Default' : {
                'Rate' : 0.05,
                'Energy' : {
                    0.5 : samus,
                    1 : mania,
                    6 : hardcore,
                    8 : harder,
                    11 : hard,
                    14 : medium,
                    20 : easy
                },
            },
            'Used to it' : {
                'Rate' : 0.06,
                'Energy' : {
                    1 : mania,
                    4 : hardcore,
                    6 : harder,
                    8 : hard,
                    11 : medium,
                    14 : easy
                },
            },
            'No problemo' : {
                'Rate' : 0.08,
                'Energy' : {
                    1 : mania,
                    4 : hardcore,
                    5 : harder,
                    6 : hard,
                    8 : medium,
                    12 : easy
                },
            }
        },
        'Ridley' : {
            "I'm scared!" : {
                'Rate' : 0.047,
                'Energy' : {
                    1 : mania,
                    7 : hardcore,
                    11 : harder,
                    14 : hard,
                    20 : medium
                },
            },
            'Default' : {
                'Rate' : 0.12,
                'Energy' : {
                    0.5 : samus,
                    1 : mania,
                    6 : hardcore,
                    8 : harder,
                    12 : hard,
                    20 : medium,
                    36 : easy
                },
            },
            'Used to it' : {
                'Rate' : 0.16,
                'Energy' : {
                    1 : mania,
                    6 : hardcore,
                    8 : harder,
                    10 : hard,
                    14 : medium,
                    20 : easy
                },
            },
            'Piece of cake' : {
                'Rate' : 0.3,
                'Energy' : {
                    1 : mania,
                    3 : hardcore,
                    4 : harder,
                    6 : hard,
                    8 : medium,
                    10 : easy
                }
            }
        },
        # 2 = 6 tanks/no suits. 4 = 3 tanks + Varia
        'MotherBrain' : {
            "It can get ugly" : {
                'Rate' : 0.18,
                'Energy' : {
                    2 : impossibru,
                    4 : mania,
                    8 : hardcore,
                    12 : harder,
                    16 : hard,
                    24 : medium,
                    32 : easy
                }
            },
            'Default' : {
                'Rate' : 0.25,
                'Energy' : {
                    2 : impossibru,
                    4 : mania,
                    8 : hardcore,
                    12 : harder,
                    16 : hard,
                    20 : medium,
                    24 : easy
                }
            },
            'Is this really the last boss?': {
                'Rate' : 0.5,
                'Energy' : {
                    2 : impossibru,
                    4 : mania,
                    6 : hardcore,
                    8 : harder,
                    12 : hard,
                    14 : medium,
                    20 : easy
                }
            },
            'Nice cutscene bro' : {
                'Rate' : 0.6,
                'Energy' : {
                    2 : mania,
                    4 : hard,
                    8 : medium,
                    12 : easy
                }
            }
        }
    }

    bossesDifficulty = {
        'Kraid' : bossesDifficultyPresets['Kraid']['Default'],
        'Phantoon' : bossesDifficultyPresets['Phantoon']['Default'],
        'Draygon' : bossesDifficultyPresets['Draygon']['Default'],
        'Ridley' : bossesDifficultyPresets['Ridley']['Default'],
        'MotherBrain' : bossesDifficultyPresets['MotherBrain']['Default']
    }

    # hell run table
    # set entry to None to disable
    hellRunPresets = {
        'Ice' : {
            'No thanks' : None,
            # get comfortable before going in
            'Gimme energy' : [(4, hardcore), (5, harder), (6, hard), (10, medium)],
            # balanced setting
            'Default' : [(3, harder), (4, hard), (5, medium)],
            # you don't mind doing hell runs at all
            'Bring the heat' : [(2, harder), (3, hard), (4, medium)],
            # RBO runner
            'I run RBO' : [(2, medium), (3, easy)],
            'Solution' : [(2, hardcore), (3, harder), (4, hard), (5, medium)],
        },
        'MainUpperNorfair' : {
            'No thanks' : None,
            'Gimme energy' : [(5, mania), (6, hardcore), (8, harder), (10, hard), (14, medium)],
            'Default' : [(4, mania), (5, hardcore), (6, hard), (9, medium)],
            'Bring the heat' : [(3, mania), (4, harder), (5, hard), (7, medium)],
            'I run RBO' : [(3, harder), (4, hard), (5, medium), (6, easy)],
            'Solution' : [(3, samus), (4, mania), (5, hardcore), (6, hard), (9, medium)]
        },
        'LowerNorfair' : {
            'Default' : None,
            'Bring the heat' : [(10, mania), (13, hardcore), (18, harder)],
            'I run RBO' : [(8, mania), (9, hardcore), (11, harder), (14, hard), (18, medium)],
            'Solution' : [(8, impossibru), (18, mania)]
        }
    }

    hellRuns = {
        # Ice Beam hell run
        'Ice' : hellRunPresets['Ice']['Default'],
        # rest of upper norfair
        'MainUpperNorfair' : hellRunPresets['MainUpperNorfair']['Default'],
        'LowerNorfair' : hellRunPresets['LowerNorfair']['Default']
    }

    # centralize all the hellruns coeffs
    hellRunsTable = {
        'Ice': {
            'Norfair Entrance -> Ice Beam': {'mult': 1.0, 'minE': 2, 'hellRun': 'Ice'},
            'Norfair Entrance -> Croc via Ice': {'mult': 1.5, 'minE': 2, 'hellRun': 'Ice'},
            'Croc -> Norfair Entrance': {'mult': 2.0, 'minE': 1, 'hellRun': 'Ice'},
            'Croc -> Bubble Mountain': {'mult': 2.0, 'minE': 1, 'hellRun': 'Ice'}
        },
        'MainUpperNorfair': {
            'Norfair Entrance -> Bubble': {'mult': 1.0, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Norfair Entrance': {'mult': 0.75, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Norfair Entrance -> Cathedral Missiles': {'mult': 0.66, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Cathedral Missiles': {'mult': 0.66, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Norfair Entrance -> Croc via Frog': {'mult': 2.0, 'minE': 1, 'hellRun': 'MainUpperNorfair'},
            'Norfair Entrance -> Croc via Frog w/Wave': {'mult': 4.0, 'minE': 1, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Norfair Reserve Missiles': {'mult': 3.0, 'minE': 1, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Norfair Reserve': {'mult': 1.0, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Speed Booster': {'mult': 1.0, 'minE': 3, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Speed Booster w/Speed': {'mult': 2.0, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Wave': {'mult': 0.75, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Kronic Boost Room': {'mult': 1.25, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Kronic Boost Room wo/Bomb': {'mult': 0.5, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Bubble -> Croc': {'mult': 2.0, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Bubble Top <-> Bubble Bottom': {'mult': 0.357, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Croc -> Grapple Escape Missiles': {'mult': 1.0, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Croc -> Ice Missiles': {'mult': 1.0, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Single Chamber <-> Bubble Mountain': {'mult': 1.25, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Kronic Boost Room -> Bubble Mountain Top': {'mult': 0.5, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Kronic Boost Room <-> Croc': {'mult': 1.0, 'minE': 2, 'hellRun': 'MainUpperNorfair'},
            'Croc -> Norfair Entrance': {'mult': 1.25, 'minE': 2, 'hellRun': 'MainUpperNorfair'}
        },
        'LowerNorfair': {
            'Main': {'mult':1.0, 'minE':8, 'hellRun':'LowerNorfair'},
            'Entrance -> GT via Chozo': {'mult':0.8, 'minE':8, 'hellRun':'LowerNorfair'}
        }
    }

    hardRoomsPresets = {
        'X-Ray' : {
            'Aarghh' : [(10, hard), (14, medium)],
            "I don't like spikes" : [(8, hard), (10, medium), (14, easy)],
            'Default' : [(6, hard), (8, medium), (10, easy)],
            "I don't mind spikes" : [(4, hard), (6, medium), (8, easy)],
            'D-Boost master': [(1, hardcore), (2, harder), (3, hard), (4, medium), (6, easy)],
            'Solution' : [(1, samus), (4, mania), (6, hard), (8, medium), (10, easy)],
        },
        'Gauntlet' : {
            'Aarghh' : [(5, hard), (10, medium)],
            "I don't like acid" : [(1, harder), (2, hard), (5, medium), (10, easy)],
            'Default' : [(0, harder), (1, hard), (3, medium), (6, easy)]
        }
    }

    hardRooms = {
        'X-Ray' : hardRoomsPresets['X-Ray']['Default'],
        'Gauntlet' : hardRoomsPresets['Gauntlet']['Default']
    }

    # various settings used in difficulty computation
    algoSettings = {
        # Boss Fights

        # number of missiles fired per second during boss battles
        # (used along with Rate)
        'missilesPerSecond' : 3,
        # number of supers fired per second during boss battles
        # (used along with Rate)
        'supersPerSecond' : 1.85,
        # number of power bombs fired per second during boss battles
        # (used along with Rate)
        'powerBombsPerSecond' : 0.33,
        # number of charged shots per second (at most 1)
        'chargedShotsPerSecond' : 0.75,
        # firepower grabbed by picking up drops during boss battles
        # in missiles per minute (1 super = 3 missiles)
        'missileDropsPerMinute' : 12,
        # if no charge beam, amount of ammo margin to consider the boss
        # fight as 'normal' (1.5 = 50% more for instance)
        # boss fight difficulty will be linearly increased between this value
        # and 1
        'ammoMarginIfNoCharge' : 1.5,
        # divide the difficulty by this amount if charge
        'phantoonFlamesAvoidBonusCharge' : 1.2,
        # divide the difficulty by this amount if screw
        'phantoonFlamesAvoidBonusScrew' : 1.5,
        # multiply the difficulty by this amount if no charge and few missiles
        'phantoonLowMissileMalus' : 1.2,
        # multiply the difficulty by this amount if you have to fight with water physics
        'draygonNoGravityMalus' : 2.0,
        # if gravity+no morph
        'draygonNoMorphMalus' : 2.0,
        # if gravity+screw
        'draygonScrewBonus' : 2.0,
        # dmg reduction factor for bosses giving drops.
        # Varia (2) is considered "standard" dmg reduction.
        # this is to take into account the impact of health drops
        # relative to how hard the boss hits
        'dmgReductionDifficultyFactor' : 1.5
    }

def isButton(button):
    return button[0:len('__')] != '__'

class Controller:
    ControllerDict = {}
    # controller mapping
    A = "Jump"
    B = "Dash"
    X = "Shoot"
    Y = "Item Cancel"
    L = "Angle Down"
    R = "Angle Up"
    Select = "Item Select"
    Moonwalk = False

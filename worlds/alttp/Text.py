# -*- coding: UTF-8 -*-
from collections import OrderedDict
import logging

text_addresses = {'Pedestal': (0x180300, 256),
                  'Triforce': (0x180400, 256),
                  'Uncle': (0x180500, 256),
                  'Ganon1': (0x180600, 256),
                  'Ganon2': (0x180700, 256),
                  'Blind': (0x180800, 256),
                  'TavernMan': (0x180C00, 256),
                  'Sahasrahla1': (0x180A00, 256),
                  'Sahasrahla2': (0x180B00, 256),
                  'BombShop1': (0x180E00, 256),
                  'BombShop2': (0x180D00, 256),
                  'PyramidFairy': (0x180900, 256),
                  'EtherTablet': (0x180F00, 256),
                  'BombosTablet': (0x181000, 256),
                  'Ganon1Invincible': (0x181100, 256),
                  'Ganon2Invincible': (0x181200, 256)}


Uncle_texts = [
    'Good Luck!\nYou will need it.',
    'Forward this message to 10 other people or this seed will be awful.',
    'I hope you like your seeds bootless and fluteless.',
    '10\n9\n8\n7\n6\n5\n4\n3\n2\n1\nGo!',
    'I\'m off to visit cousin Fritzl.',
    'Don\'t forget to check Antlion Cave.'
] * 2 + [
    "We're out of\nWeetabix. To\nthe store!",
    "This seed is\nbootless\nuntil boots.",
    "Why do we only\nhave one bed?",
    "This is the\nonly textbox.",
    "I'm going to\ngo watch the\nMoth tutorial.",
    "This seed is\nthe worst.",
    "Chasing tail.\nFly ladies.\nDo not follow.",
    "I feel like\nI've done this\nbefore…",
    "Magic Cape can\npass through\nthe barrier!",
    "I am not your\nreal uncle.",
    "You're going\nto have a very\nbad time.",
    "Today you\nwill have\nbad luck.",
    "I am leaving\nforever.\nGoodbye.",
    "Don't worry.\nI got this\ncovered.",
    "Race you to\nthe castle!",
    "\n      hi",
    "I'm just going\nout for a\npack of smokes",
    "It's dangerous\nto go alone.\nSee ya!",
    "Are you a bad\nenough dude to\nrescue Zelda?",
    "\n\n    I AM ERROR",
    "This seed is\nsub 2 hours,\nguaranteed.",
    "The chest is\na secret to\neverybody.",
    "I'm off to\nfind the\nwind fish.",
    "The shortcut\nto Ganon\nis this way!",
    "The moon is\ncrashing! Run\nfor your life!",
    "Time to fight\nhe who must\nnot be named.",
    "Red Mail\nis for\ncowards.",
    "Hey!\n\nListen!",
    "Well\nexcuuuuuse me,\nprincess!",
    "5,000 Rupee\nreward for >\nYou're boned.",
    "Welcome to\nStoops Lonk's\nHoose",
    "Erreur de\ntraduction.\nsvp reessayer",
    "I could beat\nit in an hour\nand one life.",
    "I thought this\nwas open mode?",
    "Get to the\nchop...\ncastle!",
    "Come with me\nif you want\nto live",
    "I must go\nmy planet\nneeds me",
    "Are we in\ngo mode yet?",
    "Darn, I\nthought this\nwas combo.",
    "Don't check\nanything I\nwouldn't!",
    "I know where\nthe bow is!",
    "This message\nwill self\ndestruct.",
    "Time to cast\nMeteo on\nGanon!",
    "I have a\nlong, full\nlife ahead!",
    "Why did that\nsoda have a\nskull on it?",
    "Something\nrandom just\ncame up.",
    "I'm bad at\nthis. Can you\ndo it for me?",
    "Link!\n   Wake up!\n      ... Bye!",
    "Text me when\nyou hit\ngo mode.",
    "Turn off the\nstove before\nyou leave.",
    "It's raining.\nI'm taking\nthe umbrella.",
    "Count to 30.\nThen come\nfind me.",
    "Gonna shuffle\nall the items\nreal quick.",
]
Triforce_texts = [
                     'Product has Hole in center. Bad seller, 0 out of 5.',
                     'Who stole the fourth triangle?',
                     'Trifource?\nMore Like Tritrice, am I right?'
                     '\n  Well Done!',
                     'You just wasted 2 hours of your life.',
                     'This was meant to be a trapezoid\n   Success!',  # Contributed by caitsith2
                     'This was meant to be a trapezoid',
                 ] * 2 + [
    "\n     GG",
    "All your base\nare belong\nto us.",
    "You have ended\nthe domination\nof Dr. Wily",
    " Thanks for\n  playing!!!",
    "\n  You Win!",
    "  Thank you!\n  Your quest\n   is over.",
    "Your princess \n is in another\n castle."
    "\n  I'm sorry",
    "  Whelp…\n   that just\n    happened",
    "   Oh hey…\n    it's you",
    "\n  Wheeeeee!!",
    "  Time for\n   another one?",
    "and\n\n         scene",
    "\n  Got 'em!!",
    "\nThe valuuue!!!",
    "Cool seed,\n\nright?",
    "\n  We did it!",
    "\n   O  M  G",
    " Hello.  Will\n  you be my\n   friend?",
    "The Wind Fish\nwill wake\nsoon.    Hoot!",
    "Meow meow meow\nMeow meow meow\n  Oh my god!",
    "Ahhhhhhhhh\nYa ya yaaaah\nYa ya yaaah",
    ".done\n\n.comment lol",
    "You get to\ndrink from\nthe firehose",
    "Do you prefer\n bacon, pork,\n   or ham?",
    "You get one\nwish.  Choose\nwisely, hero!",
    "Can you please\nbreak us three\nup?  Thanks.",
    "  Pick us up\n  before we\n  get dizzy!",
    "Thank you,\nMikey. You’re\n2 minutes late",
    "This was a\n7000 series\ntrain.",
    "   I'd buy\n   that for\n   a rupee!",
    " Did you like\n   that bow\n  placement?",
    "I promise the\nnext seed will\nbe better.",
    "\n   Honk.",
]
BombShop2_texts = ['Bombs!\nBombs!\nBiggest!\nBestest!\nGreatest!\nBoomiest!']
Sahasrahla2_texts = ['You already have my item.', 'Why are you still talking to me?', 'Have you met my brother, Hasarahshla?']
Blind_texts = [
    "I hate insect\npuns, they\nreally bug me.",
    "I haven't seen\nthe eye doctor\nin years.",
    "I don't see\nyou having a\nbright future.",
    "Are you doing\na blind run\nof this game?",
    "Pizza joke? No\nI think it's a\nbit too cheesy",
    "A novice skier\noften jumps to\ncontusions.",
    "The beach?\nI'm not shore\nI can make it.",
    "Rental agents\noffer quarters\nfor dollars.",
    "I got my tires\nfixed for a\nflat rate.",
    "New light bulb\ninvented?\nEnlighten me.",
    "A baker's job\nis a piece of\ncake.",
    "My optometrist\nsaid I have\nvision!",
    "When you're a\nbaker, don't\nloaf around.",
    "Broken pencils\nare pointless.",
    "A tap dancer's\nroutine runs\nhot and cold.",
    "A weeknight is\na tiny\nnobleman.",
    "The chimney\nsweep wore a\nsoot and tye.",
    "Gardeners like\nto spring into\naction.",
    "Bad at nuclear\nphysics. I\nGot no fission",
    "Flint and\nsteel are a\ngood match.",
    "I'd peg you\nas a fan of\nthe hammer.",
    "Archers give\ngifts tied\nwith a bow.",
    "A healed\ngambler is\nall better.",
    "Any old sword\nwill make the\ncut here.",
    "Lazy wyrms\nkeep dragon\ntheir feet.",
    "Percussionist\nmasters drum\nup audiences.",
    "Retrievers\nlove fetch\nquests.",
    "Sausage is\nthe wurst.",
    "I tried to\ncatch fog,\nbut I mist.",
    "Winter is a\ngreat time\nto chill.",
    "Pyramids?\nI never saw\nthe point.",
    "Stone golems\nare created as\nblank slates.",
    "Desert humor\nis often dry.",
    "Ganon is a\nbacon of\ndespair!",
    "Butchering\ncows means\nhigh steaks.",
    "I can't search\nthe web...\nToo many links",
    "I can whistle\nMost pitches\nbut I can't C",
    "The Blinds\nStore is\ncurtain death",
    "Dark Aga Rooms\nare not a\nbright idea.",
    "Best advice\nfor a Goron?\nBe Boulder.",
    "Equestrian\nservices are\na stable job.",
    "Do I like\ndrills? Just\na bit.",
    "I'd shell out\ngood rupees\nfor a conch.",
    "Current\naffairs are\nshocking!",
    "Agriculture\nis a growing\nfield.",
    "Did you hear\nabout the guy\nwhose whole\nleft side was\ncut off?\nHe's all right\nnow.",
    "What do you\ncall a bee\nthat lives in\nAmerica?\nA USB.",
    "Leather is\ngreat for\nsneaking\naround because\nit's made of\nhide.",
]
Ganon1_texts = [
    "Start your day\nsmiling with a\ndelicious\nwhole grain\nbreakfast\ncreated for\nyour\nincredible\ninsides.",
    "You drove\naway my other\nself, Agahnim,\ntwo times…\nBut, I won't\ngive you the\nTriforce.\nI'll defeat\nyou!",
    "Impa says that\nthe mark on\nyour hand\nmeans that you\nare the hero\nchosen to\nawaken Zelda.\nYour blood can\nresurrect me.",
    "Don't stand,\n\ndon't stand so\nDon't stand so\n\nclose to me\nDon't stand so\nclose to me\nBack off buddy",
    "So ya\nThought ya\nMight like to\ngo to the show\nTo feel the\nwarm thrill of\nconfusion\nThat space\ncadet glow.",
    "Like other\npulmonate land\ngastropods,\nthe majority\nof land slugs\nhave two pairs\nof 'feelers'\nor tentacles,\non their head.",
    "If you were a\nburrito, what\nkind of a\nburrito would\nyou be?\nMe, I fancy I\nwould be a\nspicy barbacoa\nburrito.",
    "I am your\nfather's\nbrother's\nnephew's\ncousin's\nformer\nroommate. What\ndoes that make\nus, you ask?",
    "I'll be more\neager about\nencouraging\nthinking\noutside the\nbox when there\nis evidence of\nany thinking\ninside it.",
    "If we're not\nmeant to have\nmidnight\nsnacks, then\nwhy is there\na light in the\nfridge?\n",
    "I feel like we\nkeep ending up\nhere.\n\nDon't you?\n\nIt's like\ndeja vu\nall over again",
    "Did you know?\nThe biggest\nand heaviest\ncheese ever\nproduced\nweighed\n57,518 pounds\nand was 32\nfeet long.",
    "Now there was\na time, When\nyou loved me\nso. I couldn't\ndo wrong,\nAnd now you\nneed to know.\nSo How you\nlike me now?",
    "Did you know?\nNutrition\nexperts\nrecommend that\nat least half\nof our daily\ngrains come\nfrom whole\ngrain products",
    "The Hemiptera\nor true bugs\nare an order\nof insects\ncovering 50k\nto 80k species\nlike aphids,\ncicadas, and\nshield bugs.",
    "Thanks for\ndropping in.\nThe first\npassengers\nin a hot\nair balloon\nwere a duck,\na sheep,\nand a rooster.",
    "You think you\nare so smart?\n\nI bet you\ndidn't know\nyou can't hum\nwhile holding\nyour nose\nclosed.",
    "grumble,\n\ngrumble…\ngrumble,\n\ngrumble…\nSeriously, you\nwere supposed\nto bring food.",
    "Join me hero,\nand I shall\nmake your face\nthe greatest\nin the Dark\nWorld!\n\nOr else you\nwill die!",
    "Why rule over\na desert full\nof stereotypes\nwhen I can\ncorrupt a\nworld into\npure evil and\nrule over\nthat instead?",
    "When I conquer\nthe Light\nWorld, I'll\nhold a parade\nof all my\nmonsters to\ndemonstrate my\nmight to the\npeople!",
    "Life, dreams,\nhope...\nWhere'd they\ncome from? And\nwhere are they\nheaded?  These\nthings... I am\ngoing to\ndestroy!",
    "My minions all\nfailed to\nguard those\nitems?!\n\nWhy am I\nsurrounded by\nincompetent\nfools?!",
    "Bacon dates to\n1500 BCE and\nrefers to the\nback of a pig.\nThe average\nAmerican eats\n18 pounds of\nRoman \"petaso\"\nevery year.",
    "The enrichment\nCenter would\nLike to remind\nYou that the\nCompanion\nDuck will not\nbetray you\nand in fact\ncannot speak.",
    "Goose is\nactually the\nterm for\nfemale geese,\nmale geese are\ncalled\nganders.",
]
TavernMan_texts = [
    "What do you\ncall a blind\ndinosaur?\na doyouthink-\nhesaurus.",
    "A blind man\nwalks into\na bar.\nAnd a table.\nAnd a chair.",
    "What do ducks\nlike to eat?\n\nQuackers!",
    "How do you\nset up a party\nin space?\n\nYou planet!",
    "I'm glad I\nknow sign\nlanguage.\nIt's pretty\nhandy.",
    "What did Zelda\nsay to Link at\na secure door?\n\nTRIFORCE!",
    "I am on a\nseafood diet.\n\nEvery time\nI see food,\nI eat it.",
    "I've decided\nto sell my\nvacuum.\nIt was just\ngathering\ndust.",
    "What's the best\ntime to go to\nthe dentist?\n\nTooth-hurtie!",
    "Why can't a\nbike stand on\nits own?\n\nIt's two-tired!",
    "If you haven't\nfound Quake\nyet…\nit's not your\nfault.",
    "Why is Peter\nPan always\nflying?\nBecause he\nNeverlands!",
    "I once told a\njoke to Armos.\n\nBut he\nremained\nstone-faced!",
    "Lanmola was\nlate to our\ndinner party.\nHe just came\nfor the desert",
    "Moldorm is\nsuch a\nprankster.\nAnd I fall for\nit every time!",
    "Helmasaur is\nthrowing a\nparty.\nI hope it's\na masquerade!",
    "I'd like to\nknow Arrghus\nbetter.\nBut he won't\ncome out of\nhis shell!",
    "Mothula didn't\nhave much fun\nat the party.\nHe's immune to\nspiked punch!",
    "Don't set me\nup with that\nlady from\nSteve's Town.\n\n\nI'm not\ninterested in\na Blind date!",
    "Kholdstare is\nafraid to go\nto the circus.\nHungry kids\nthought he was\ncotton candy!",
    "I asked who\nVitreous' best\nfriends are.\nHe said,\n'Me, Myself,\nand Eye!'",
    "Trinexx can be\na hothead or\nhe can be an\nice guy. In\nthe end, he's\na solid\nindividual!",
    "Bari thought I\nhad moved out\nof town.\nHe was shocked\nto see me!",
    "I can only get\nWeetabix\naround here.\nI have to go\nto Steve's\nTown for Count\nChocula!",
    "Don't argue\nwith a frozen\nDeadrock.\nHe'll never\nchange his\nposition!",
    "I offered a\ndrink to a\nself-loathing\nGhini.\nHe said he\ndidn't like\nspirits!",
    "I was supposed\nto meet Gibdo\nfor lunch.\nBut he got\nwrapped up in\nsomething!",
    "Goriya sure\nhas changed\nin this game.\nI hope he\ncomes back\naround!",
    "Hinox actually\nwants to be a\nlawyer.\nToo bad he\nbombed the\nBar exam!",
    "I'm surprised\nMoblin's tusks\nare so gross.\nHe always has\nhis Trident\nwith him!",
    "Don't tell\nStalfos I'm\nhere.\nHe has a bone\nto pick with\nme!",
    "I got\nWallmaster to\nhelp me move\nfurniture.\nHe was really\nhandy!",
    "Wizzrobe was\njust here.\nHe always\nvanishes right\nbefore we get\nthe check!",
    "I shouldn't\nhave picked up\nZora's tab.\nThat guy\ndrinks like\na fish!",
    "I was sharing\na drink with\nPoe.\nFor no reason,\nhe left in a\nheartbeat!",
    "Don't trust\nhorsemen on\nDeath Mountain.\nThey're Lynel\nthe time!",
    "Today's\nspecial is\nbattered bat.\nGot slapped\nfor offering a\nlady a Keese!",
    "Don't walk\nunder\npropellered\npineapples.\nYou may end up\nwearing\na pee hat!",
    "My girlfriend\nburrowed under\nthe sand.\nSo I decided\nto Leever!",
    "Geldman wants\nto be a\nBroadway star.\nHe's always\npracticing\nJazz Hands!",
    "Octoballoon\nmust be mad\nat me.\nHe blows up\nat the sight\nof me!",
    "Toppo is a\ntotal pothead.\n\nHe hates it\nwhen you take\naway his grass",
    "I lost my\nshield by\nthat house.\nWhy did they\nput up a\nPikit fence?!",
    "Know that fox\nin Steve's\nTown?\nHe'll Pikku\npockets if you\naren't careful",
    "Dash through\nDark World\nbushes.\nYou'll see\nGanon is tryin\nto Stal you!",
    "Eyegore!\n\nYou gore!\nWe all gore\nthose jerks\nwith arrows!",
    "I like my\nwhiskey neat.\n\nSome prefer it\nOctoroks!",
    "I consoled\nFreezor over a\ncup of coffee.\nHis problems\njust seemed to\nmelt away!",
    "Magic droplets\nof water don't\nshut up.\nThey just\nKyameron!",
    "I bought hot\nwings for\nSluggula.\nThey gave him\nexplosive\ndiarrhea!",
    "Hardhat Beetle\nwon't\nLet It Be?\nTell it to Get\nBack or give\nit a Ticket to\nRide down\na hole!",
]

junk_texts = [
    "{C:GREEN}\nAgitha's good\nin Hyrule\nWarriors.   >",
    "{C:GREEN}\nConsult Fi if\nthe batteries\nare low.    >",
    "{C:GREEN}\nThere is no\n3rd quest in\nthis game.  >",
    "{C:GREEN}\nI am Error.\n \n            >",
    "{C:GREEN}\nThe Wind Fish\nknows all in\nhere. Hoot! >",
    "{C:GREEN}\nThere are no\nwallets in\nthis game.  >",
    "{C:GREEN}\nCrossbow\nTraining is\na fun game. >",
    "{C:GREEN}\nThe shrine\ncontains\nMagnesis.   >",
    "{C:GREEN}\nThe loftwing\nlet the duck\ntake over.  >",
    "{C:GREEN}\nStasis would\nbe very\noverpowered.>",
    "{C:GREEN}\nIt’s a secret\nto everybody.\n            >",
    "{C:GREEN}\nDodongo\ndislikes\nsmoke.      >",
    "{C:GREEN}\n> Digdogger\nhates certain\nkind of sound.",
    "{C:GREEN}\nI bet you’d\nlike to have\nmore bombs. >",
    "{C:GREEN}\n>Secret power\nis said to be\nin the arrow.",
    "{C:GREEN}\nAim at the\neyes of Gohma.\n            >",
    "{C:GREEN}\nGrumble,\ngrumble…\n            >",
    # "{C:GREEN}\n10th enemy\nhas the bomb.\n            >", removed as people may assume it applies to this game
    "{C:GREEN}\nGo to the\nnext room.\n            >",
    "{C:GREEN}\n>Thanks, @\nYou’re the\nhero of Hyrule",
    "{C:GREEN}\nThere’s always\nmoney in the\nBanana Stand>",
    "{C:GREEN}\n \nJust walk away\n            >",
    "{C:GREEN}\neverybody is\nlooking for\nsomething   >",
    # "{C:GREEN}\nSpring Ball\nare behind\nRidley      >",  removed as people may assume it's a real hint
    "{C:GREEN}\nThe gnome asks\nyou to guess\nhis name.   >",
    "{C:GREEN}\nI heard beans\non toast is a\ngreat meal. >",
    "{C:GREEN}\n> Sweetcorn\non pizza is a\ngreat choice.",
    "{C:GREEN}\nI bet a nice\ncup of tea\nwould help! >",
    "{C:GREEN}\nI bet you\nexpected help,\ndidn't you? >",
    "{C:GREEN}\nLearn to make\nplogues, easy\nand yummy!  >",
    "{C:GREEN}\nI don't know\nwhere it is\neither.  >",
    "{C:GREEN}\nA dog exists\nsomewhere. >",
    "{C:GREEN}\nIf all else\nfails use\nfire.  >",
    "{C:GREEN}\nItems are\nrequired to\nwin.  >",
    "{C:GREEN}\nDid you try\nchecking\nvanilla?  >",
    "{C:GREEN}\n> If you find\nmy lunch,\ndon't eat it.",
    "{C:GREEN}\nDeadrocks are\nannoying.  >",
    "{C:GREEN}\nMist Form\nis in the\nCatacombs.  >",
    "{C:GREEN}\nMaybe you\ncould hire a\ndetective?  >",
    "{C:GREEN}\n>  READ\nor the owl\nwill eat you.",
    "{C:GREEN}\nOther randos\nexist too!\nTry some!  >",
]

KingsReturn_texts = [
    'Who is this even',
    'The Harem'
] * 2 + [
    "the return of the king",
    "fellowship of the ring",
    "the two towers",
]
Sanctuary_texts = [
    'A Priest\'s love'
] * 2 + [
    "the loyal priest",
    "read a book",
    "sits in own pew",
]
Sahasrahla_names = [
    "sahasralah", "sabotaging", "sacahuista", "sacahuiste", "saccharase", "saccharide", "saccharify",
    "saccharine", "saccharins", "sacerdotal", "sackcloths", "salmonella", "saltarelli", "saltarello",
    "saltations", "saltbushes", "saltcellar", "saltshaker", "salubrious", "sandgrouse", "sandlotter",
    "sandstorms", "sandwiched", "sauerkraut", "schipperke", "schismatic", "schizocarp", "schmalzier",
    "schmeering", "schmoosing", "shibboleth", "shovelnose", "sahananana", "sarararara", "salamander",
    "sharshalah", "shahabadoo", "sassafrass", "saddlebags", "sandalwood", "shagadelic", "sandcastle",
    "saltpeters", "shabbiness", "shlrshlrsh", "sassyralph", "sallyacorn",
]

Kakariko_texts = ["{}'s homecoming"]
Blacksmiths_texts = [
    'frogs for bread',
    'That\'s not a sword',
    'The Rupeesmiths'
] * 1 + [
    "the dwarven breadsmiths"
]
DeathMountain_texts = [
    "the lost old man",
    "gary the old man",
    "Your ad here"
]
LostWoods_texts = [
    'thieves\' stump',
    'He\'s got wood',
] * 2 + [
    "the forest thief",
    "dancing pickles",
    "flying vultures",
]
WishingWell_texts = [
    "venus. queen of faeries",
    "Venus was her name",
    "I'm your Venus",
    "Yeah, baby, shes got it",
    "Venus, I'm your fire",
    "Venus, At your desire",
    "Venus Love Chain",
    "Venus Crescent Beam",
]
DesertPalace_texts = ['vultures rule the desert', 'literacy moves']
MountainTower_texts = ['the bully makes a friend', 'up up and away']
LinksHouse_texts = ['your uncle recovers', 'Home Sweet Home', 'Only one bed']
Lumberjacks_texts = [
    'Chop Chop'
] * 2 + [
    "twin lumberjacks",
    "fresh flapjacks",
    "two woodchoppers",
    "double lumberman",
    "lumberclones",
    "woodfellas",
    "dos axes",
]
SickKid_texts = ['Next Time Stay Down']
Zora_texts = ['Splashes For Sale', 'Slippery when wet']
MagicShop_texts = ['Drug deal', 'Shrooms for days']
FluteBoy_texts = ['Stumped']


class Credits(object):
    def __init__(self):
        self.credit_scenes = {
            'castle': [
                SceneSmallCreditLine(19, 'The return of the King'),
                SceneLargeCreditLine(23, 'Hyrule Castle'),
            ],
            'sanctuary': [
                SceneSmallCreditLine(19, 'The loyal priest'),
                SceneLargeCreditLine(23, 'Sanctuary'),
            ],
            'kakariko': [
                SceneSmallCreditLine(19, "Sahasralah's Homecoming"),
                SceneLargeCreditLine(23, 'Kakariko Town'),
            ],
            'desert': [
                SceneSmallCreditLine(19, 'vultures rule the desert'),
                SceneLargeCreditLine(23, 'Desert Palace'),
            ],
            'hera': [
                SceneSmallCreditLine(19, 'the bully makes a friend'),
                SceneLargeCreditLine(23, 'Mountain Tower'),
            ],
            'house': [
                SceneSmallCreditLine(19, 'your uncle recovers'),
                SceneLargeCreditLine(23, 'Your House'),
            ],
            'zora': [
                SceneSmallCreditLine(19, 'finger webs for sale'),
                SceneLargeCreditLine(23, "Zora's Waterfall"),
            ],
            'witch': [
                SceneSmallCreditLine(19, 'the witch and assistant'),
                SceneLargeCreditLine(23, 'Magic Shop'),
            ],
            'lumberjacks': [
                SceneSmallCreditLine(19, 'twin lumberjacks'),
                SceneLargeCreditLine(23, "Woodsmen's Hut"),
            ],
            'grove': [
                SceneSmallCreditLine(19, 'flute boy plays again'),
                SceneLargeCreditLine(23, 'Haunted Grove'),
            ],
            'well': [
                SceneSmallCreditLine(19, 'venus, queen of faeries'),
                SceneLargeCreditLine(23, 'Wishing Well'),
            ],
            'smithy': [
                SceneSmallCreditLine(19, 'the dwarven swordsmiths'),
                SceneLargeCreditLine(23, 'Smithery'),
            ],
            'kakariko2': [
                SceneSmallCreditLine(19, 'the bug-catching kid'),
                SceneLargeCreditLine(23, 'Kakariko Town'),
            ],
            'bridge': [
                SceneSmallCreditLine(19, 'the lost old man'),
                SceneLargeCreditLine(23, 'Death Mountain'),
            ],
            'woods': [
                SceneSmallCreditLine(19, 'the forest thief'),
                SceneLargeCreditLine(23, 'Lost Woods'),
            ],
            'pedestal': [
                SceneSmallCreditLine(19, 'and the master sword'),
                SceneSmallAltCreditLine(21, 'sleeps again...'),
                SceneLargeCreditLine(23, 'Forever!'),
            ],
        }

        self.scene_order = ['castle', 'sanctuary', 'kakariko', 'desert', 'hera', 'house', 'zora', 'witch',
                            'lumberjacks', 'grove', 'well', 'smithy', 'kakariko2', 'bridge', 'woods', 'pedestal']

    def update_credits_line(self, scene, line, text):
        scenes = self.credit_scenes

        text = text[:32]
        scenes[scene][line].text = text

    def get_bytes(self):
        pointers = []
        data = bytearray()
        for scene_name in self.scene_order:
            scene = self.credit_scenes[scene_name]
            pointers.append(len(data))

            for part in scene:
                data += part.as_bytes()

        pointers.append(len(data))
        return (pointers, data)

class CreditLine(object):
    """Base class of credit lines"""

    def __init__(self, text, align='center'):
        self.text = text
        self.align = align

    @property
    def x(self):
        if self.align == 'left':
            x = 0
        elif self.align == 'right':
            x = 32 - len(self.text)
        else:  # center
            x = (32 - len(self.text)) // 2
        return x


class SceneCreditLine(CreditLine):
    """Base class for credit lines for the scene portion of the credits"""
    def __init__(self, y, text, align='center'):
        self.y = y
        super().__init__(text, align)

    def header(self, x=None, y=None, length=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if length is None:
            length = len(self.text)
        header = (0x6000 | (y >> 5 << 11) | ((y & 0x1F) << 5) | (x >> 5 << 10) | (x & 0x1F)) << 16 | (length * 2 - 1)
        return bytearray([header >> 24 & 0xFF, header >> 16 & 0xFF, header >> 8 & 0xFF, header & 0xFF])


class SceneSmallCreditLine(SceneCreditLine):
    def as_bytes(self):
        buf = bytearray()
        buf.extend(self.header())
        buf.extend(GoldCreditMapper.convert(self.text))

        # handle upper half of apostrophe character if present
        if "'" in self.text:
            apos = "".join([',' if x == "'" else ' ' for x in self.text])
            buf.extend(self.header(self.x + apos.index(','), self.y - 1, len(apos.strip())))
            buf.extend(GoldCreditMapper.convert(apos.strip()))

        # handle lower half of comma character if present
        if ',' in self.text:
            commas = "".join(["'" if x == ',' else ' ' for x in self.text])
            buf.extend(self.header(self.x + commas.index("'"), self.y + 1, len(commas.strip())))
            buf.extend(GoldCreditMapper.convert(commas.strip()))

        return buf


class SceneSmallAltCreditLine(SceneCreditLine):
    def as_bytes(self):
        buf = bytearray()
        buf += self.header()
        buf += GreenCreditMapper.convert(self.text)
        return buf


class SceneLargeCreditLine(SceneCreditLine):
    def as_bytes(self):
        buf = bytearray()
        buf += self.header()
        buf += LargeCreditTopMapper.convert(self.text)

        buf += self.header(self.x, self.y + 1)
        buf += LargeCreditBottomMapper.convert(self.text)
        return buf

class MultiByteTextMapper(object):
    @classmethod
    def convert(cls, text, maxbytes=256):
        outbuf = MultiByteCoreTextMapper.convert(text)

        # check for max length
        if len(outbuf) > maxbytes - 2:
            outbuf = outbuf[:maxbytes - 2]
            # Note: this could crash if the last byte is part of a two byte command
            # depedning on how well the command handles a value of 0x7F.
            # Should probably do something about this.

        outbuf.append(0x7F)
        outbuf.append(0x7F)
        return outbuf

class MultiByteCoreTextMapper(object):
    special_commands = {
        "{SPEED0}": [0x7A, 0x00],
        "{SPEED1}": [0x7A, 0x01],
        "{SPEED2}": [0x7A, 0x02],
        "{SPEED6}": [0x7A, 0x06],
        "{PAUSE1}": [0x78, 0x01],
        "{PAUSE3}": [0x78, 0x03],
        "{PAUSE5}": [0x78, 0x05],
        "{PAUSE7}": [0x78, 0x07],
        "{PAUSE9}": [0x78, 0x09],
        "{INPUT}": [0x7E],
        "{CHOICE}": [0x68],
        "{ITEMSELECT}": [0x69],
        "{CHOICE2}": [0x71],
        "{CHOICE3}": [0x72],
        "{HARP}": [0x79, 0x2D],
        "{MENU}": [0x6D, 0x00],
        "{BOTTOM}": [0x6D, 0x00],
        "{NOBORDER}": [0x6B, 0x02],
        "{CHANGEPIC}": [0x67, 0x67],
        "{CHANGEMUSIC}": [0x67],
        "{PAGEBREAK}" : [0x7D],
        "{INTRO}": [0x6E, 0x00, 0x77, 0x07, 0x7A, 0x03, 0x6B, 0x02, 0x67],
        "{NOTEXT}": [0x6E, 0x00, 0x6B, 0x04],
        "{IBOX}": [0x6B, 0x02, 0x77, 0x07, 0x7A, 0x03],
        "{C:GREEN}": [0x77, 0x07],
        "{C:YELLOW}": [0x77, 0x02],
    }

    @classmethod
    def convert(cls, text, pause=True, wrap=14):
        text = text.upper()
        lines = text.split('\n')
        outbuf = bytearray()
        lineindex = 0
        is_intro = '{INTRO}' in text
        first_line=True

        while lines:
            linespace = wrap
            line = lines.pop(0)
            if line.startswith('{'):
                if line == '{PAGEBREAK}':
                    if lineindex % 3 != 0:
                        # insert a wait for keypress, unless we just did so
                        outbuf.append(0x7E)
                    lineindex = 0
                outbuf.extend(cls.special_commands[line])
                continue

            words = line.split(' ')
            if first_line:
                first_line=False
            else:
                outbuf.append(0x74 if lineindex == 0 else 0x75 if lineindex == 1 else 0x76)  # line starter
            pending_space = False
            while words:
                word = words.pop(0)
                # sanity check: if the word we have is more than 14 characters, we take as much as we can still fit and push the rest back for later
                if cls.wordlen(word) > wrap:
                    (word_first, word_rest) = cls.splitword(word, linespace)
                    words.insert(0, word_rest)
                    lines.insert(0, ' '.join(words))

                    outbuf.extend(RawMBTextMapper.convert(word_first))
                    break

                if cls.wordlen(word) <= linespace:
                    if pending_space:
                        outbuf.extend(RawMBTextMapper.convert(' '))
                    if cls.wordlen(word) < linespace:
                        pending_space = True
                    linespace -= cls.wordlen(word) + 1 if pending_space else 0
                    outbuf.extend(RawMBTextMapper.convert(word))
                else:
                    # ran out of space, push word and lines back and continue with next line
                    words.insert(0, word)
                    lines.insert(0, ' '.join(words))
                    break

            if is_intro and lineindex < 3:
                outbuf.extend([0xFF]*linespace)

            has_more_lines = len(lines) > 1 or (lines and not lines[0].startswith('{'))

            lineindex += 1
            if pause and lineindex % 3 == 0 and has_more_lines:
                outbuf.append(0x7E)
            if lineindex >= 3 and has_more_lines and lines[0] != '{PAGEBREAK}':
                outbuf.append(0x73)
        return outbuf

    @classmethod
    def wordlen(cls, word):
        l = 0
        offset = 0
        while offset < len(word):
            c_len, offset = cls.charlen(word, offset)
            l += c_len
        return l

    @classmethod
    def splitword(cls, word, length):
        l = 0
        offset = 0
        while True:
            c_len, new_offset = cls.charlen(word, offset)
            if l+c_len > length:
                break
            l += c_len
            offset = new_offset
        return (word[0:offset], word[offset:])

    @classmethod
    def charlen(cls, word, offset):
        c = word[offset]
        if c in ['>', '¼', '½', '♥']:
            return (2, offset+1)
        if c in ['@']:
            return (4, offset+1)
        if c in ['ᚋ', 'ᚌ', 'ᚍ', 'ᚎ']:
            return (2, offset+1)
        return (1, offset+1)

class CompressedTextMapper(object):
    two_byte_commands = [
        0x6B, 0x6C, 0x6D, 0x6E,
        0x77, 0x78, 0x79, 0x7A
    ]
    specially_coded_commands = {
        0x73: 0xF6,
        0x74: 0xF7,
        0x75: 0xF8,
        0x76: 0xF9,
        0x7E: 0xFA,
        0x7A: 0xFC,
    }

    @classmethod
    def convert(cls, text, pause=True, max_bytes_expanded=0x800, wrap=14):
        inbuf = MultiByteCoreTextMapper.convert(text, pause, wrap)

        # Links name will need 8 bytes in the target buffer
        # and two will be used by the terminator
        # (Variables will use 2 bytes, but they start as 2 bytes)
        bufsize = len(inbuf) + 7 * inbuf.count(0x6A) + 2
        if bufsize > max_bytes_expanded:
            raise ValueError("Uncompressed string too long for buffer")
        inbuf.reverse()
        outbuf = bytearray()
        outbuf.append(0xfb) # terminator for previous record
        while inbuf:
            val = inbuf.pop()
            if val == 0xFF:
                outbuf.append(val)
            elif val == 0x00:
                outbuf.append(inbuf.pop())
            elif val == 0x01: #kanji
                outbuf.append(0xFD)
                outbuf.append(inbuf.pop())
            elif val >= 0x67:
                if val in cls.specially_coded_commands:
                    outbuf.append(cls.specially_coded_commands[val])
                else:
                    outbuf.append(0xFE)
                    outbuf.append(val)
                if val in cls.two_byte_commands:
                    outbuf.append(inbuf.pop())
            else:
                raise ValueError("Unexpected byte found in uncompressed string")
        return outbuf

class CharTextMapper(object):
    number_offset = None
    alpha_offset = 0
    char_map = {}
    @classmethod
    def map_char(cls, char):
        if cls.number_offset is not None:
            if  0x30 <= ord(char) <= 0x39:
                return ord(char) + cls.number_offset
        if 0x61 <= ord(char) <= 0x7A:
            return ord(char) + cls.alpha_offset
        return cls.char_map.get(char, cls.char_map[' '])

    @classmethod
    def convert(cls, text):
        buf = bytearray()
        for char in text.lower():
            buf.append(cls.map_char(char))
        return buf

class RawMBTextMapper(CharTextMapper):
    char_map = {' ': 0xFF,
                '『': 0xC4,
                '』': 0xC5,
                '?': 0xC6,
                '!': 0xC7,
                ',': 0xC8,
                '-': 0xC9,
                "🡄": 0xCA,
                "🡆": 0xCB,
                '…': 0xCC,
                '.': 0xCD,
                '~': 0xCE,
                '～': 0xCE,
                '@': [0x6A], # Links name (only works if compressed)
                '>': [0x00, 0xD2, 0x00, 0xD3], # Link's face
                "'": 0xD8,
                '’': 0xD8,
                '%': 0xDD, # Hylian Bird
                '^': 0xDE, # Hylian Ankh
                '=': 0xDF, # Hylian Wavy Lines
                '↑': 0xE0,
                '↓': 0xE1,
                '→': 0xE2,
                '←': 0xE3,
                '≥': 0xE4, # Cursor
                '¼': [0x00, 0xE5, 0x00, 0xE7], # ¼ heart
                '½': [0x00, 0xE6, 0x00, 0xE7], # ½ heart
                '¾': [0x00, 0xE8, 0x00, 0xE9], # ¾ heart
                '♥': [0x00, 0xEA, 0x00, 0xEB], # full heart
                'ᚋ': [0x6C, 0x00], # var 0
                'ᚌ': [0x6C, 0x01], # var 1
                'ᚍ': [0x6C, 0x02], # var 2
                'ᚎ': [0x6C, 0x03], # var 3
                'あ': 0x00,
                'い': 0x01,
                'う': 0x02,
                'え': 0x03,
                'お': 0x04,
                'や': 0x05,
                'ゆ': 0x06,
                'よ': 0x07,
                'か': 0x08,
                'き': 0x09,
                'く': 0x0A,
                'け': 0x0B,
                'こ': 0x0C,
                'わ': 0x0D,
                'を': 0x0E,
                'ん': 0x0F,
                'さ': 0x10,
                'し': 0x11,
                'す': 0x12,
                'せ': 0x13,
                'そ': 0x14,
                'が': 0x15,
                'ぎ': 0x16,
                'ぐ': 0x17,
                'た': 0x18,
                'ち': 0x19,
                'つ': 0x1A,
                'て': 0x1B,
                'と': 0x1C,
                'げ': 0x1D,
                'ご': 0x1E,
                'ざ': 0x1F,
                'な': 0x20,
                'に': 0x21,
                'ぬ': 0x22,
                'ね': 0x23,
                'の': 0x24,
                'じ': 0x25,
                'ず': 0x26,
                'ぜ': 0x27,
                'は': 0x28,
                'ひ': 0x29,
                'ふ': 0x2A,
                'へ': 0x2B,
                'ほ': 0x2C,
                'ぞ': 0x2D,
                'だ': 0x2E,
                'ぢ': 0x2F,
                'ま': 0x30,
                'み': 0x31,
                'む': 0x32,
                'め': 0x33,
                'も': 0x34,
                'づ': 0x35,
                'で': 0x36,
                'ど': 0x37,
                'ら': 0x38,
                'り': 0x39,
                'る': 0x3A,
                'れ': 0x3B,
                'ろ': 0x3C,
                'ば': 0x3D,
                'び': 0x3E,
                'ぶ': 0x3F,
                'べ': 0x40,
                'ぼ': 0x41,
                'ぱ': 0x42,
                'ぴ': 0x43,
                'ぷ': 0x44,
                'ぺ': 0x45,
                'ぽ': 0x46,
                'ゃ': 0x47,
                'ゅ': 0x48,
                'ょ': 0x49,
                'っ': 0x4A,
                'ぁ': 0x4B,
                'ぃ': 0x4C,
                'ぅ': 0x4D,
                'ぇ': 0x4E,
                'ぉ': 0x4F,
                'ア': 0x50,
                'イ': 0x51,
                'ウ': 0x52,
                'エ': 0x53,
                'オ': 0x54,
                'ヤ': 0x55,
                'ユ': 0x56,
                'ヨ': 0x57,
                'カ': 0x58,
                'キ': 0x59,
                'ク': 0x5A,
                'ケ': 0x5B,
                'コ': 0x5C,
                'ワ': 0x5D,
                'ヲ': 0x5E,
                'ン': 0x5F,
                'サ': 0x60,
                'シ': 0x61,
                'ス': 0x62,
                'セ': 0x63,
                'ソ': 0x64,
                'ガ': 0x65,
                'ギ': 0x66,
                'グ': 0x67,
                'タ': 0x68,
                'チ': 0x69,
                'ツ': 0x6A,
                'テ': 0x6B,
                'ト': 0x6C,
                'ゲ': 0x6D,
                'ゴ': 0x6E,
                'ザ': 0x6F,
                'ナ': 0x70,
                'ニ': 0x71,
                'ヌ': 0x72,
                'ネ': 0x73,
                'ノ': 0x74,
                'ジ': 0x75,
                'ズ': 0x76,
                'ゼ': 0x77,
                'ハ': 0x78,
                'ヒ': 0x79,
                'フ': 0x7A,
                'ヘ': 0x7B,
                'ホ': 0x7C,
                'ゾ': 0x7D,
                'ダ': 0x7E,
                'マ': 0x80,
                'ミ': 0x81,
                'ム': 0x82,
                'メ': 0x83,
                'モ': 0x84,
                'ヅ': 0x85,
                'デ': 0x86,
                'ド': 0x87,
                'ラ': 0x88,
                'リ': 0x89,
                'ル': 0x8A,
                'レ': 0x8B,
                'ロ': 0x8C,
                'バ': 0x8D,
                'ビ': 0x8E,
                'ブ': 0x8F,
                'ベ': 0x90,
                'ボ': 0x91,
                'パ': 0x92,
                'ピ': 0x93,
                'プ': 0x94,
                'ペ': 0x95,
                'ポ': 0x96,
                'ャ': 0x97,
                'ュ': 0x98,
                'ョ': 0x99,
                'ッ': 0x9A,
                'ァ': 0x9B,
                'ィ': 0x9C,
                'ゥ': 0x9D,
                'ェ': 0x9E,
                'ォ': 0x9F}

    kanji = {"娘": 0x00,
             "城": 0x01,
             "行": 0x02,
             "教": 0x03,
             "会": 0x04,
             "神": 0x05,
             "父": 0x06,
             "訪": 0x07,
             "頼": 0x08,
             "通": 0x09,
             "願": 0x0A,
             "平": 0x0B,
             "和": 0x0C,
             "司": 0x0D,
             "書": 0x0E,
             "戻": 0x0F,
             "様": 0x10,
             "子": 0x11,
             "湖": 0x12,
             "達": 0x13,
             "彼": 0x14,
             "女": 0x15,
             "言": 0x16,
             "祭": 0x17,
             "早": 0x18,
             "雨": 0x19,
             "剣": 0x1A,
             "盾": 0x1B,
             "解": 0x1C,
             "抜": 0x1D,
             "者": 0x1E,
             "味": 0x1F,
             "方": 0x20,
             "無": 0x21,
             "事": 0x22,
             "出": 0x23,
             "本": 0x24,
             "当": 0x25,
             "私": 0x26,
             "他": 0x27,
             "救": 0x28,
             "倒": 0x29,
             "度": 0x2A,
             "国": 0x2B,
             "退": 0x2C,
             "魔": 0x2D,
             "伝": 0x2E,
             "説": 0x2F,
             "必": 0x30,
             "要": 0x31,
             "良": 0x32,
             "地": 0x33,
             "図": 0x34,
             "印": 0x35,
             "思": 0x36,
             "気": 0x37,
             "人": 0x38,
             "間": 0x39,
             "兵": 0x3A,
             "病": 0x3B,
             "法": 0x3C,
             "屋": 0x3D,
             "手": 0x3E,
             "住": 0x3F,
             "連": 0x40,
             "恵": 0x41,
             "表": 0x42,
             "金": 0x43,
             "王": 0x44,
             "信": 0x45,
             "裏": 0x46,
             "取": 0x47,
             "引": 0x48,
             "入": 0x49,
             "口": 0x4A,
             "開": 0x4B,
             "見": 0x4C,
             "正": 0x4D,
             "幸": 0x4E,
             "運": 0x4F,
             "呼": 0x50,
             "物": 0x51,
             "付": 0x52,
             "紋": 0x53,
             "章": 0x54,
             "所": 0x55,
             "家": 0x56,
             "闇": 0x57,
             "読": 0x58,
             "左": 0x59,
             "側": 0x5A,
             "札": 0x5B,
             "穴": 0x5C,
             "道": 0x5D,
             "男": 0x5E,
             "大": 0x5F,
             "声": 0x60,
             "下": 0x61,
             "犯": 0x62,
             "花": 0x63,
             "深": 0x64,
             "森": 0x65,
             "水": 0x66,
             "若": 0x67,
             "美": 0x68,
             "探": 0x69,
             "今": 0x6A,
             "士": 0x6B,
             "店": 0x6C,
             "好": 0x6D,
             "代": 0x6E,
             "名": 0x6F,
             "迷": 0x70,
             "立": 0x71,
             "上": 0x72,
             "光": 0x73,
             "点": 0x74,
             "目": 0x75,
             "的": 0x76,
             "押": 0x77,
             "前": 0x78,
             "夜": 0x79,
             "十": 0x7A,
             "字": 0x7B,
             "北": 0x7C,
             "急": 0x7D,
             "昔": 0x7E,
             "果": 0x7F,
             "奥": 0x80,
             "選": 0x81,
             "続": 0x82,
             "結": 0x83,
             "定": 0x84,
             "悪": 0x85,
             "向": 0x86,
             "歩": 0x87,
             "時": 0x88,
             "使": 0x89,
             "古": 0x8A,
             "何": 0x8B,
             "村": 0x8C,
             "長": 0x8D,
             "配": 0x8E,
             "匹": 0x8F,
             "殿": 0x90,
             "守": 0x91,
             "精": 0x92,
             "知": 0x93,
             "山": 0x94,
             "誰": 0x95,
             "足": 0x96,
             "冷": 0x97,
             "黄": 0x98,
             "力": 0x99,
             "宝": 0x9A,
             "求": 0x9B,
             "先": 0x9C,
             "消": 0x9D,
             "封": 0x9E,
             "捕": 0x9F,
             "勇": 0xA0,
             "年": 0xA1,
             "姿": 0xA2,
             "話": 0xA3,
             "色": 0xA4,
             "々": 0xA5,
             "真": 0xA6,
             "紅": 0xA7,
             "場": 0xA8,
             "炎": 0xA9,
             "空": 0xAA,
             "面": 0xAB,
             "音": 0xAC,
             "吹": 0xAD,
             "中": 0xAE,
             "祈": 0xAF,
             "起": 0xB0,
             "右": 0xB1,
             "念": 0xB2,
             "再": 0xB3,
             "生": 0xB4,
             "庭": 0xB5,
             "路": 0xB6,
             "部": 0xB7,
             "川": 0xB8,
             "血": 0xB9,
             "完": 0xBA,
             "矢": 0xBB,
             "現": 0xBC,
             "在": 0xBD,
             "全": 0xBE,
             "体": 0xBF,
             "文": 0xC0,
             "秘": 0xC1,
             "密": 0xC2,
             "感": 0xC3,
             "賢": 0xC4,
             "陣": 0xC5,
             "残": 0xC6,
             "百": 0xC7,
             "近": 0xC8,
             "朝": 0xC9,
             "助": 0xCA,
             "術": 0xCB,
             "粉": 0xCC,
             "火": 0xCD,
             "注": 0xCE,
             "意": 0xCF,
             "走": 0xD0,
             "敵": 0xD1,
             "玉": 0xD2,
             "復": 0xD3,
             "活": 0xD4,
             "塔": 0xD5,
             "来": 0xD6,
             "帰": 0xD7,
             "忘": 0xD8,
             "東": 0xD9,
             "青": 0xDA,
             "持": 0xDB,
             "込": 0xDC,
             "逃": 0xDD,
             "銀": 0xDE,
             "勝": 0xDF,
             "集": 0xE0,
             "始": 0xE1,
             "攻": 0xE2,
             "撃": 0xE3,
             "命": 0xE4,
             "老": 0xE5,
             "心": 0xE6,
             "新": 0xE7,
             "世": 0xE8,
             "界": 0xE9,
             "箱": 0xEA,
             "木": 0xEB,
             "対": 0xEC,
             "特": 0xED,
             "賊": 0xEE,
             "洞": 0xEF,
             "支": 0xF0,
             "盗": 0xF1,
             "族": 0xF2,
             "能": 0xF3,
             #"力": 0xF4,
             "多": 0xF5,
             "聖": 0xF6,
             "両": 0xF7,
             "民": 0xF8,
             "予": 0xF9,
             "小": 0xFA,
             "強": 0xFB,
             "投": 0xFC,
             "服": 0xFD,
             "月": 0xFE,
             "姫": 0xFF}
    alpha_offset = 0x49
    number_offset = 0x70

    @classmethod
    def map_char(cls, char):
        if char in cls.kanji:
            return [0x01, cls.kanji[char]]
        return super().map_char(char)

    @classmethod
    def convert(cls, text):
        buf = bytearray()
        for char in text.lower():
            res = cls.map_char(char)
            if isinstance(res, int):
                buf.extend([0x00, res])
            else:
                buf.extend(res)
        return buf


class GoldCreditMapper(CharTextMapper):
    char_map = {' ': 0x9F,
                ',': 0x34,
                "'": 0x35,
                '-': 0x36,
                '.': 0x37,}
    alpha_offset = -0x47


class GreenCreditMapper(CharTextMapper):
    char_map = {' ': 0x9F,
                '·': 0x52,
                '.': 0x52}
    alpha_offset = -0x29

class RedCreditMapper(CharTextMapper):
    char_map = {' ': 0x9F}
    alpha_offset = -0x61

class LargeCreditTopMapper(CharTextMapper):
    char_map = {' ': 0x9F,
                "'": 0x77,
                '!': 0x78,
                '.': 0xA0,
                '#': 0xA1,
                '/': 0xA2,
                ':': 0xA3,
                ',': 0xA4,
                '?': 0xA5,
                '=': 0xA6,
                '"': 0xA7,
                '-': 0xA8,
                '·': 0xA9,
                '•': 0xA9,
                '◢': 0xAA,
                '◣': 0xAB,}
    alpha_offset = -0x04
    number_offset = 0x23


class LargeCreditBottomMapper(CharTextMapper):
    char_map = {' ': 0x9F,
                "'": 0x9D,
                '!': 0x9E,
                '.': 0xC0,
                '#': 0xC1,
                '/': 0xC2,
                ':': 0xC3,
                ',': 0xC4,
                '?': 0xC5,
                '=': 0xC6,
                '"': 0xC7,
                '-': 0xC8,
                '·': 0xC9,
                '•': 0xC9,
                '◢': 0xCA,
                '◣': 0xCB,}
    alpha_offset = 0x22
    number_offset = 0x49

class TextTable(object):
    SIZE = 0x7355

    valid_keys = [
        "set_cursor",
        "set_cursor2",
        "game_over_menu",
        "var_test",
        "follower_no_enter",
        "choice_1_3",
        "choice_2_3",
        "choice_3_3",
        "choice_1_2",
        "choice_2_2",
        "uncle_leaving_text",
        "uncle_dying_sewer",
        "tutorial_guard_1",
        "tutorial_guard_2",
        "tutorial_guard_3",
        "tutorial_guard_4",
        "tutorial_guard_5",
        "tutorial_guard_6",
        "tutorial_guard_7",
        "priest_sanctuary_before_leave",
        "sanctuary_enter",
        "zelda_sanctuary_story",
        "priest_sanctuary_before_pendants",
        "priest_sanctuary_after_pendants_before_master_sword",
        "priest_sanctuary_dying",
        "zelda_save_sewers",
        "priest_info",
        "zelda_sanctuary_before_leave",
        "telepathic_intro",
        "telepathic_reminder",
        "zelda_go_to_throne",
        "zelda_push_throne",
        "zelda_switch_room_pull",
        "zelda_save_lets_go",
        "zelda_save_repeat",
        "zelda_before_pendants",
        "zelda_after_pendants_before_master_sword",
        "telepathic_zelda_right_after_master_sword",
        "zelda_sewers",
        "zelda_switch_room",
        "kakariko_saharalasa_wife",
        "kakariko_saharalasa_wife_sword_story",
        "kakariko_saharalasa_wife_closing",
        "kakariko_saharalasa_after_master_sword",
        "kakariko_alert_guards",
        "sahasrahla_quest_have_pendants",
        "sahasrahla_quest_have_master_sword",
        "sahasrahla_quest_information",
        "sahasrahla_bring_courage",
        "sahasrahla_have_ice_rod",
        "telepathic_sahasrahla_beat_agahnim",
        "telepathic_sahasrahla_beat_agahnim_no_pearl",
        "sahasrahla_have_boots_no_icerod",
        "sahasrahla_have_courage",
        "sahasrahla_found",
        "sign_rain_north_of_links_house",
        "sign_north_of_links_house",
        "sign_path_to_death_mountain",
        "sign_lost_woods",
        "sign_zoras",
        "sign_outside_magic_shop",
        "sign_death_mountain_cave_back",
        "sign_east_of_links_house",
        "sign_south_of_lumberjacks",
        "sign_east_of_desert",
        "sign_east_of_sanctuary",
        "sign_east_of_castle",
        "sign_north_of_lake",
        "sign_desert_thief",
        "sign_lumberjacks_house",
        "sign_north_kakariko",
        "witch_bring_mushroom",
        "witch_brewing_the_item",
        "witch_assistant_no_bottle",
        "witch_assistant_no_empty_bottle",
        "witch_assistant_informational",
        "witch_assistant_no_bottle_buying",
        "potion_shop_no_empty_bottles",
        "item_get_lamp",
        "item_get_boomerang",
        "item_get_bow",
        "item_get_shovel",
        "item_get_magic_cape",
        "item_get_powder",
        "item_get_flippers",
        "item_get_power_gloves",
        "item_get_pendant_courage",
        "item_get_pendant_power",
        "item_get_pendant_wisdom",
        "item_get_mushroom",
        "item_get_book",
        "item_get_moonpearl",
        "item_get_compass",
        "item_get_map",
        "item_get_ice_rod",
        "item_get_fire_rod",
        "item_get_ether",
        "item_get_bombos",
        "item_get_quake",
        "item_get_hammer",
        "item_get_flute",
        "item_get_cane_of_somaria",
        "item_get_hookshot",
        "item_get_bombs",
        "item_get_bottle",
        "item_get_big_key",
        "item_get_titans_mitts",
        "item_get_magic_mirror",
        "item_get_fake_mastersword",
        "post_item_get_mastersword",
        "item_get_red_potion",
        "item_get_green_potion",
        "item_get_blue_potion",
        "item_get_bug_net",
        "item_get_blue_mail",
        "item_get_red_mail",
        "item_get_temperedsword",
        "item_get_mirror_shield",
        "item_get_cane_of_byrna",
        "missing_big_key",
        "missing_magic",
        "item_get_pegasus_boots",
        "talking_tree_info_start",
        "talking_tree_info_1",
        "talking_tree_info_2",
        "talking_tree_info_3",
        "talking_tree_info_4",
        "talking_tree_other",
        "item_get_pendant_power_alt",
        "item_get_pendant_wisdom_alt",
        "game_shooting_choice",
        "game_shooting_yes",
        "game_shooting_no",
        "game_shooting_continue",
        "pond_of_wishing",
        "pond_item_select",
        "pond_item_test",
        "pond_will_upgrade",
        "pond_item_test_no",
        "pond_item_test_no_no",
        "pond_item_boomerang",
        "pond_item_shield",
        "pond_item_silvers",
        "pond_item_bottle_filled",
        "pond_item_sword",
        "pond_of_wishing_happiness",
        "pond_of_wishing_choice",
        "pond_of_wishing_bombs",
        "pond_of_wishing_arrows",
        "pond_of_wishing_full_upgrades",
        "mountain_old_man_first",
        "mountain_old_man_deadend",
        "mountain_old_man_turn_right",
        "mountain_old_man_lost_and_alone",
        "mountain_old_man_drop_off",
        "mountain_old_man_in_his_cave_pre_agahnim",
        "mountain_old_man_in_his_cave",
        "mountain_old_man_in_his_cave_post_agahnim",
        "tavern_old_man_awake",
        "tavern_old_man_unactivated_flute",
        "tavern_old_man_know_tree_unactivated_flute",
        "tavern_old_man_have_flute",
        "chicken_hut_lady",
        "running_man",
        "game_race_sign",
        "sign_bumper_cave",
        "sign_catfish",
        "sign_north_village_of_outcasts",
        "sign_south_of_bumper_cave",
        "sign_east_of_pyramid",
        "sign_east_of_bomb_shop",
        "sign_east_of_mire",
        "sign_village_of_outcasts",
        "sign_before_wishing_pond",
        "sign_before_catfish_area",
        "castle_wall_guard",
        "gate_guard",
        "telepathic_tile_eastern_palace",
        "telepathic_tile_tower_of_hera_floor_4",
        "hylian_text_1",
        "mastersword_pedestal_translated",
        "telepathic_tile_spectacle_rock",
        "telepathic_tile_swamp_entrance",
        "telepathic_tile_thieves_town_upstairs",
        "telepathic_tile_misery_mire",
        "hylian_text_2",
        "desert_entry_translated",
        "telepathic_tile_under_ganon",
        "telepathic_tile_palace_of_darkness",
        "telepathic_tile_desert_bonk_torch_room",
        "telepathic_tile_castle_tower",
        "telepathic_tile_ice_large_room",
        "telepathic_tile_turtle_rock",
        "telepathic_tile_ice_entrance",
        "telepathic_tile_ice_stalfos_knights_room",
        "telepathic_tile_tower_of_hera_entrance",
        "houlihan_room",
        "caught_a_bee",
        "caught_a_fairy",
        "no_empty_bottles",
        "game_race_boy_time",
        "game_race_girl",
        "game_race_boy_success",
        "game_race_boy_failure",
        "game_race_boy_already_won",
        "game_race_boy_sneaky",
        "bottle_vendor_choice",
        "bottle_vendor_get",
        "bottle_vendor_no",
        "bottle_vendor_already_collected",
        "bottle_vendor_bee",
        "bottle_vendor_fish",
        "hobo_item_get_bottle",
        "blacksmiths_what_you_want",
        "blacksmiths_paywall",
        "blacksmiths_extra_okay",
        "blacksmiths_tempered_already",
        "blacksmiths_temper_no",
        "blacksmiths_bogart_sword",
        "blacksmiths_get_sword",
        "blacksmiths_shop_before_saving",
        "blacksmiths_shop_saving",
        "blacksmiths_collect_frog",
        "blacksmiths_still_working",
        "blacksmiths_saving_bows",
        "blacksmiths_hammer_anvil",
        "dark_flute_boy_storytime",
        "dark_flute_boy_get_shovel",
        "dark_flute_boy_no_get_shovel",
        "dark_flute_boy_flute_not_found",
        "dark_flute_boy_after_shovel_get",
        "shop_fortune_teller_lw_hint_0",
        "shop_fortune_teller_lw_hint_1",
        "shop_fortune_teller_lw_hint_2",
        "shop_fortune_teller_lw_hint_3",
        "shop_fortune_teller_lw_hint_4",
        "shop_fortune_teller_lw_hint_5",
        "shop_fortune_teller_lw_hint_6",
        "shop_fortune_teller_lw_hint_7",
        "shop_fortune_teller_lw_no_rupees",
        "shop_fortune_teller_lw",
        "shop_fortune_teller_lw_post_hint",
        "shop_fortune_teller_lw_no",
        "shop_fortune_teller_lw_hint_8",
        "shop_fortune_teller_lw_hint_9",
        "shop_fortune_teller_lw_hint_10",
        "shop_fortune_teller_lw_hint_11",
        "shop_fortune_teller_lw_hint_12",
        "shop_fortune_teller_lw_hint_13",
        "shop_fortune_teller_lw_hint_14",
        "shop_fortune_teller_lw_hint_15",
        "dark_sanctuary",
        "dark_sanctuary_hint_0",
        "dark_sanctuary_no",
        "dark_sanctuary_hint_1",
        "dark_sanctuary_yes",
        "dark_sanctuary_hint_2",
        "sick_kid_no_bottle",
        "sick_kid_trade",
        "sick_kid_post_trade",
        "desert_thief_sitting",
        "desert_thief_following",
        "desert_thief_question",
        "desert_thief_question_yes",
        "desert_thief_after_item_get",
        "desert_thief_reassure",
        "hylian_text_3",
        "tablet_ether_book",
        "tablet_bombos_book",
        "magic_bat_wake",
        "magic_bat_give_half_magic",
        "intro_main",
        "intro_throne_room",
        "intro_zelda_cell",
        "intro_agahnim",
        "pickup_purple_chest",
        "bomb_shop",
        "bomb_shop_big_bomb",
        "bomb_shop_big_bomb_buy",
        "item_get_big_bomb",
        "kiki_second_extortion",
        "kiki_second_extortion_no",
        "kiki_second_extortion_yes",
        "kiki_first_extortion",
        "kiki_first_extortion_yes",
        "kiki_first_extortion_no",
        "kiki_leaving_screen",
        "blind_in_the_cell",
        "blind_by_the_light",
        "blind_not_that_way",
        "aginah_l1sword_no_book",
        "aginah_l1sword_with_pendants",
        "aginah",
        "aginah_need_better_sword",
        "aginah_have_better_sword",
        "catfish",
        "catfish_after_item",
        "lumberjack_right",
        "lumberjack_left",
        "lumberjack_left_post_agahnim",
        "fighting_brothers_right",
        "fighting_brothers_right_opened",
        "fighting_brothers_left",
        "maiden_crystal_1",
        "maiden_crystal_2",
        "maiden_crystal_3",
        "maiden_crystal_4",
        "maiden_crystal_5",
        "maiden_crystal_6",
        "maiden_crystal_7",
        "maiden_ending",
        "maiden_confirm_understood",
        "barrier_breaking",
        "maiden_crystal_7_again",
        "agahnim_zelda_teleport",
        "agahnim_magic_running_away",
        "agahnim_hide_and_seek_found",
        "agahnim_defeated",
        "agahnim_final_meeting",
        "zora_meeting",
        "zora_tells_cost",
        "zora_get_flippers",
        "zora_no_cash",
        "zora_no_buy_item",
        "kakariko_saharalasa_grandson",
        "kakariko_saharalasa_grandson_next",
        "dark_palace_tree_dude",
        "fairy_wishing_ponds",
        "fairy_wishing_ponds_no",
        "pond_of_wishing_no",
        "pond_of_wishing_return_item",
        "pond_of_wishing_throw",
        "pond_pre_item_silvers",
        "pond_of_wishing_great_luck",
        "pond_of_wishing_good_luck",
        "pond_of_wishing_meh_luck",
        "pond_of_wishing_bad_luck",
        "pond_of_wishing_fortune",
        "item_get_14_heart",
        "item_get_24_heart",
        "item_get_34_heart",
        "item_get_whole_heart",
        "item_get_sanc_heart",
        "fairy_fountain_refill",
        "death_mountain_bullied_no_pearl",
        "death_mountain_bullied_with_pearl",
        "death_mountain_bully_no_pearl",
        "death_mountain_bully_with_pearl",
        "shop_darkworld_enter",
        "game_chest_village_of_outcasts",
        "game_chest_no_cash",
        "game_chest_not_played",
        "game_chest_played",
        "game_chest_village_of_outcasts_play",
        "shop_first_time",
        "shop_already_have",
        "shop_buy_shield",
        "shop_buy_red_potion",
        "shop_buy_arrows",
        "shop_buy_bombs",
        "shop_buy_bee",
        "shop_buy_heart",
        "shop_first_no_bottle_buy",
        "shop_buy_no_space",
        "ganon_fall_in",
        "ganon_phase_3",
        "lost_woods_thief",
        "blinds_hut_dude",
        "end_triforce",
        "toppi_fallen",
        "kakariko_tavern_fisherman",
        "thief_money",
        "thief_desert_rupee_cave",
        "thief_ice_rupee_cave",
        "telepathic_tile_south_east_darkworld_cave",
        "cukeman",
        "cukeman_2",
        "potion_shop_no_cash",
        "kakariko_powdered_chicken",
        "game_chest_south_of_kakariko",
        "game_chest_play_yes",
        "game_chest_play_no",
        "game_chest_lost_woods",
        "kakariko_flophouse_man_no_flippers",
        "kakariko_flophouse_man",
        "menu_start_2",
        "menu_start_3",
        "menu_pause",
        "game_digging_choice",
        "game_digging_start",
        "game_digging_no_cash",
        "game_digging_end_time",
        "game_digging_come_back_later",
        "game_digging_no_follower",
        "menu_start_4",
        "ganon_fall_in_alt",
        "ganon_phase_3_alt",
        "sign_east_death_mountain_bridge",
        "fish_money",
        "sign_ganons_tower",
        "sign_ganon",
        "ganon_phase_3_no_bow",
        "ganon_phase_3_no_silvers_alt",
        "ganon_phase_3_no_silvers",
        "ganon_phase_3_silvers",
        "murahdahla",
    ]

    def __init__(self):
        self._text = OrderedDict()
        self.setDefaultText()

    def __getitem__(self, key):
        return self._text[key]

    def __contains__(self, key):
        return key in self._text

    def __setitem__(self, key, value):
        if not key in self._text:
            raise KeyError(key)
        if isinstance(value, str):
            self._text[key] = CompressedTextMapper.convert(value)
        else:
            self._text[key] = value

    def getBytes(self, pad=False):
        logger = logging.getLogger('')
        data = b''.join(self._text.values())
        logger.debug("translation space remaining: %i", self.SIZE - len(data))

        if len(data) > self.SIZE:
            raise Exception("Text data is too large to fit")

        if pad:
            return data.ljust(self.SIZE, b'\xff')
        return data

    def removeUnwantedText(self):
        nomessage = bytes(CompressedTextMapper.convert("{NOTEXT}", False))
        messages_to_zero = [
            #escort Messages
            'zelda_go_to_throne',
            'zelda_push_throne',
            'zelda_switch_room_pull',
            'zelda_switch_room',
            'zelda_sewers',
            'mountain_old_man_first',
            'mountain_old_man_deadend',
            'mountain_old_man_turn_right',
            'blind_not_that_way',

            # Note: Maiden text gets skipped by a change we will keep, so technically we don't need to replace them
            # Replacing them anyway to make more room in translation table
            'maiden_crystal_1',
            'maiden_crystal_2',
            'maiden_crystal_3',
            'maiden_crystal_4',
            'maiden_crystal_5',
            'maiden_crystal_6',
            'maiden_crystal_7',
            'maiden_ending',
            'maiden_confirm_understood',
            'maiden_crystal_7_again',

            # item pickup text
            'item_get_lamp',
            'item_get_boomerang',
            'item_get_bow',
            'item_get_shovel',
            'item_get_magic_cape',
            'item_get_powder',
            'item_get_flippers',
            'item_get_power_gloves',
            'item_get_pendant_courage',
            'item_get_pendant_power',
            'item_get_pendant_wisdom',
            'item_get_mushroom',
            'item_get_book',
            'item_get_moonpearl',
            'item_get_compass',
            'item_get_map', #60
            'item_get_ice_rod',
            'item_get_fire_rod',
            'item_get_ether',
            'item_get_bombos',
            'item_get_quake',
            'item_get_hammer',
            'item_get_flute',
            'item_get_cane_of_somaria',
            'item_get_hookshot',
            'item_get_bombs',
            'item_get_bottle',
            'item_get_big_key',
            'item_get_titans_mitts',
            'item_get_magic_mirror',
            'item_get_fake_mastersword',
            'post_item_get_mastersword',
            'item_get_red_potion',
            'item_get_green_potion',
            'item_get_blue_potion',
            'item_get_bug_net',
            'item_get_blue_mail',
            'item_get_red_mail',
            'item_get_temperedsword',
            'item_get_mirror_shield',
            'item_get_cane_of_byrna',
            'item_get_pegasus_boots',
            'item_get_pendant_wisdom_alt',
            'item_get_pendant_power_alt',
            'pond_item_boomerang',
            'blacksmiths_tempered_already', #!! For some reason this is coded as a recieve message
            'item_get_whole_heart',
            'item_get_sanc_heart',
            'item_get_14_heart',
            'item_get_24_heart',
            'item_get_34_heart',
            'pond_item_test',
            'pond_will_upgrade',

            # misc
            'agahnim_final_meeting',
            'agahnim_hide_and_seek_found',
            'telepathic_sahasrahla_beat_agahnim',
            'telepathic_sahasrahla_beat_agahnim_no_pearl',
            'magic_bat_wake',
            'magic_bat_give_half_magic',
            'mountain_old_man_in_his_cave_pre_agahnim',
            'mountain_old_man_in_his_cave',
            'mountain_old_man_in_his_cave_post_agahnim',
            'priest_sanctuary_before_leave',
            'priest_sanctuary_before_pendants',
            'priest_sanctuary_after_pendants_before_master_sword',
            'zelda_sanctuary_before_leave',
            'zelda_before_pendants',
            'zelda_after_pendants_before_master_sword',
            'zelda_save_sewers',
            'zelda_save_lets_go',
            'zelda_save_repeat',
            'priest_info',
            'sanctuary_enter',
            'zelda_sanctuary_story',
            'sick_kid_trade',
            'hobo_item_get_bottle',
            'sahasrahla_have_courage',
            'sahasrahla_found',
            'sahasrahla_have_boots_no_icerod',
            'sahasrahla_bring_courage',
            'sahasrahla_quest_have_master_sword',
            'shop_darkworld_enter',
            'shop_first_time',
            'shop_buy_shield',
            'shop_buy_red_potion',
            'shop_buy_arrows',
            'shop_buy_bombs',
            'shop_buy_bee',
            'shop_buy_heart',
            'bomb_shop_big_bomb_buy',
            'item_get_big_bomb',
            'catfish',
            'catfish_after_item',
            'zora_meeting',
            'zora_tells_cost',
            'zora_get_flippers',
            'zora_no_cash',
            'zora_no_buy_item',
            'agahnim_zelda_teleport',
            'agahnim_magic_running_away',
            'blind_in_the_cell',
            'kiki_first_extortion',
            'kiki_first_extortion_yes',
            'kiki_second_extortion',
            'kiki_second_extortion_yes',
            'witch_brewing_the_item',
            'barrier_breaking',
            'mountain_old_man_lost_and_alone',
            'mountain_old_man_drop_off',
            'pickup_purple_chest',
            'agahnim_defeated',
            'blacksmiths_collect_frog',
            'blacksmiths_what_you_want',
            'blacksmiths_get_sword',
            'blacksmiths_shop_saving',
            'blacksmiths_paywall',
            'blacksmiths_extra_okay',
            'blacksmiths_bogart_sword',
            'blacksmiths_tempered_already',
            'missing_magic',
            'witch_assistant_no_empty_bottle',
            'witch_assistant_informational',
            'bottle_vendor_choice',
            'bottle_vendor_get',
            'game_digging_choice',
            'game_digging_start',
            'dark_flute_boy_storytime',
            'dark_flute_boy_get_shovel',
            'thief_money',
            'game_chest_village_of_outcasts',
            'game_chest_village_of_outcasts_play',
            'hylian_text_2',
            'desert_entry_translated',
            'uncle_dying_sewer',
            'telepathic_intro',
            'desert_thief_sitting',
            'desert_thief_following',
            'desert_thief_question',
            'desert_thief_question_yes',
            'desert_thief_after_item_get',
            'desert_thief_reassure',
            'pond_item_bottle_filled'
        ]

        for msg in messages_to_zero:
            self[msg] = nomessage

    def setDefaultText(self):
        text = self._text
        text['set_cursor'] = bytearray([0xFB, 0xFC, 0x00, 0xF9, 0xFF, 0xFF, 0xFF, 0xF8, 0xFF, 0xFF, 0xE4, 0xFE, 0x68])
        text['set_cursor2'] = bytearray([0xFB, 0xFC, 0x00, 0xF8, 0xFF, 0xFF, 0xFF, 0xF9, 0xFF, 0xFF, 0xE4, 0xFE, 0x68])
        text['game_over_menu'] = CompressedTextMapper.convert("{SPEED0}\nSave-Continue\nSave-Quit\nContinue", False)
        text['var_test'] = CompressedTextMapper.convert("0= ᚋ, 1= ᚌ\n2= ᚍ, 3= ᚎ", False)
        text['follower_no_enter'] = CompressedTextMapper.convert("Can't you take me some place nice.")
        text['choice_1_3'] = bytearray([0xFB, 0xFC, 0x00, 0xF7, 0xE4, 0xF8, 0xFF, 0xF9, 0xFF, 0xFE, 0x71])
        text['choice_2_3'] = bytearray([0xFB, 0xFC, 0x00, 0xF7, 0xFF, 0xF8, 0xE4, 0xF9, 0xFF, 0xFE, 0x71])
        text['choice_3_3'] = bytearray([0xFB, 0xFC, 0x00, 0xF7, 0xFF, 0xF8, 0xFF, 0xF9, 0xE4, 0xFE, 0x71])
        text['choice_1_2'] = bytearray([0xFB, 0xFC, 0x00, 0xF7, 0xE4, 0xF8, 0xFF, 0xFE, 0x72])
        text['choice_2_2'] = bytearray([0xFB, 0xFC, 0x00, 0xF7, 0xFF, 0xF8, 0xE4, 0xFE, 0x72])
        text['uncle_leaving_text'] = CompressedTextMapper.convert("I'm just going out for a pack of smokes.")
        text['uncle_dying_sewer'] = CompressedTextMapper.convert("I've fallen and I can't get up, take this.")
        text['tutorial_guard_1'] = CompressedTextMapper.convert("Only adults should travel at night.")
        # 10
        text['tutorial_guard_2'] = CompressedTextMapper.convert("You can press X to see the Map.")
        text['tutorial_guard_3'] = CompressedTextMapper.convert("Press the A button to lift things by you.")
        text['tutorial_guard_4'] = CompressedTextMapper.convert("When you has a sword, press B to slash it.")
        text['tutorial_guard_5'] = CompressedTextMapper.convert("このメッセージはニホンゴでそのまま") # on purpose
        text['tutorial_guard_6'] = CompressedTextMapper.convert("Are we really still reading these?")
        text['tutorial_guard_7'] = CompressedTextMapper.convert("Jeez! There really are a lot of things.")
        text['priest_sanctuary_before_leave'] = CompressedTextMapper.convert("Go be a hero!")
        text['sanctuary_enter'] = CompressedTextMapper.convert("YAY!\nYou saved Zelda!")
        text['zelda_sanctuary_story'] = CompressedTextMapper.convert("Do you want to hear me say this again?\n{HARP}\n  ≥ no\n    yes\n{CHOICE}")
        text['priest_sanctuary_before_pendants'] = CompressedTextMapper.convert("Go'on and get them pendants so you can beat up Agahnim.")
        text['priest_sanctuary_after_pendants_before_master_sword'] = CompressedTextMapper.convert("Kudos! But seriously, you should be getting the master sword, not having a kegger in here.")
        text['priest_sanctuary_dying'] = CompressedTextMapper.convert("They took her to the castle! Take your sword and save her!")
        text['zelda_save_sewers'] = CompressedTextMapper.convert("You saved me!")
        text['priest_info'] = CompressedTextMapper.convert("So, I'm the dude that will protect Zelda. Don't worry, I got this covered.")
        text['zelda_sanctuary_before_leave'] = CompressedTextMapper.convert("Be careful!")
        text['telepathic_intro'] = CompressedTextMapper.convert("{NOBORDER}\n{SPEED6}\nHey, come find me and help me!")
        # 20
        text['telepathic_reminder'] = CompressedTextMapper.convert("{NOBORDER}\n{SPEED6}\nI'm in the castle basement.")
        text['zelda_go_to_throne'] = CompressedTextMapper.convert("Go north to the throne.")
        text['zelda_push_throne'] = CompressedTextMapper.convert("Let's push it from the left!")
        text['zelda_switch_room_pull'] = CompressedTextMapper.convert("Pull this lever using A.")
        text['zelda_save_lets_go'] = CompressedTextMapper.convert("Let's get out of here!")
        text['zelda_save_repeat'] = CompressedTextMapper.convert("I like talking, do you?\n  ≥ no\n    yes\n{CHOICE}")
        text['zelda_before_pendants'] = CompressedTextMapper.convert("You need to find all the pendants…\n\n\nNumpty.")
        text['zelda_after_pendants_before_master_sword'] = CompressedTextMapper.convert("Very pretty pendants, but really you should be getting that sword in the forest!")
        text['telepathic_zelda_right_after_master_sword'] = CompressedTextMapper.convert("{NOBORDER}\n{SPEED6}\nHi @,\nHave you been thinking about me?\narrrrrgghh…\n… … …")
        text['zelda_sewers'] = CompressedTextMapper.convert("Just a little further to the Sanctuary.")
        text['zelda_switch_room'] = CompressedTextMapper.convert("The Sanctuary!\n\nPull my finger")
        text['kakariko_saharalasa_wife'] = CompressedTextMapper.convert("Heya, @!\nLong time no see.\nYou want a master sword?\n\nWell good luck with that.")
        text['kakariko_saharalasa_wife_sword_story'] = CompressedTextMapper.convert("It occurs to me that I like toast and jam, but cheese and crackers is better.\nYou like?\n  ≥ cheese\n    jam\n{CHOICE}")
        text['kakariko_saharalasa_wife_closing'] = CompressedTextMapper.convert("Anywho, I have things to do. You see those 2 ovens?\n\nYeah 2!\nWho has 2 ovens nowadays?")
        text['kakariko_saharalasa_after_master_sword'] = CompressedTextMapper.convert("Cool sword!\n\n\n…\n\n\n…\n\n\nPlease save us")
        text['kakariko_alert_guards'] = CompressedTextMapper.convert("GUARDS! HELP!\nThe creeper\n@ is here!")
        # 30
        text['sahasrahla_quest_have_pendants'] = CompressedTextMapper.convert("{BOTTOM}\nCool beans, but I think you should mosey on over to the lost woods.")
        text['sahasrahla_quest_have_master_sword'] = CompressedTextMapper.convert("{BOTTOM}\nThat's a pretty sword, but I'm old, forgetful, and old. Why don't you go do all the hard work while I hang out in this hut.")
        text['sahasrahla_quest_information'] = CompressedTextMapper.convert(
            "{BOTTOM}\n"
            + "Sahasrahla, I am. You would do well to find the 3 pendants from the 3 dungeons in the Light World.\n"
            + "Understand?\n  ≥ yes\n    no\n{CHOICE}")
        text['sahasrahla_bring_courage'] = CompressedTextMapper.convert(
            "{BOTTOM}\n"
            + "While you're here, could you do me a solid and get the green pendant from that dungeon?\n"
            + "{HARP}\nI'll give you a present if you do.")
        text['sahasrahla_have_ice_rod'] = CompressedTextMapper.convert("{BOTTOM}\nLike, I sit here, and tell you what to do?\n\n\nAlright, go and find all the maidens, there are, like, maybe 7 of them. I dunno anymore. I'm old.")
        text['telepathic_sahasrahla_beat_agahnim'] = CompressedTextMapper.convert("{NOBORDER}\n{SPEED6}\nNice, so you beat Agahnim. Now you must beat Ganon. Good Luck!")
        text['telepathic_sahasrahla_beat_agahnim_no_pearl'] = CompressedTextMapper.convert("{NOBORDER}\n{SPEED6}\nOh, also you forgot the Moon Pearl, dingus. Go back and find it!")
        text['sahasrahla_have_boots_no_icerod'] = CompressedTextMapper.convert("{BOTTOM}\nCave in South East has a cool item.")
        text['sahasrahla_have_courage'] = CompressedTextMapper.convert("{BOTTOM}\nLook, you have the green pendant! I'll give you something. Go kill the other two bosses for more pendant fun!")
        text['sahasrahla_found'] = CompressedTextMapper.convert("{BOTTOM}\nYup!\n\nI'm the old man you are looking for. I'll keep it short and sweet: Go into that dungeon, then bring me the green pendant and talk to me again.")
        text['sign_rain_north_of_links_house'] = CompressedTextMapper.convert("↑ Dying Uncle\n  This way…")
        text['sign_north_of_links_house'] = CompressedTextMapper.convert("> Randomizer") #"> Randomizer The telepathic tiles can have hints!"
        text['sign_path_to_death_mountain'] = CompressedTextMapper.convert("Cave to lost, old man.\nGood luck.")
        text['sign_lost_woods'] = CompressedTextMapper.convert("\n↑ Lost Woods")
        text['sign_zoras'] = CompressedTextMapper.convert("Danger!\nDeep water!\nZoras!")
        text['sign_outside_magic_shop'] = CompressedTextMapper.convert("Welcome to the Magic Shoppe")
        # 40
        text['sign_death_mountain_cave_back'] = CompressedTextMapper.convert("Cave away from sky cabbages")
        text['sign_east_of_links_house'] = CompressedTextMapper.convert("↓ Lake Hylia\n\n Also, a shop")
        text['sign_south_of_lumberjacks'] = CompressedTextMapper.convert("← Kakariko\n  Village")
        text['sign_east_of_desert'] = CompressedTextMapper.convert("← Desert\n\n     It's hot.")
        text['sign_east_of_sanctuary'] = CompressedTextMapper.convert("↑→ Potions!\n\nWish waterfall")
        text['sign_east_of_castle'] = CompressedTextMapper.convert("→ East Palace\n\n← Castle")
        text['sign_north_of_lake'] = CompressedTextMapper.convert("\n Lake  Hiriah")
        text['sign_desert_thief'] = CompressedTextMapper.convert("Don't talk to me or touch my sign!")
        text['sign_lumberjacks_house'] = CompressedTextMapper.convert("Lumberjacks, Inc.\nYou see 'em, we saw 'em.")
        text['sign_north_kakariko'] = CompressedTextMapper.convert("↓ Kakariko\n  Village")
        text['witch_bring_mushroom'] = CompressedTextMapper.convert("Double, double toil and trouble!\nBring me a mushroom!")
        text['witch_brewing_the_item'] = CompressedTextMapper.convert("This mushroom is busy brewing. Come back later.")
        text['witch_assistant_no_bottle'] = CompressedTextMapper.convert("A bottle for your thoughts? or to put potions in.")
        text['witch_assistant_no_empty_bottle'] = CompressedTextMapper.convert("Gotta use your stuff before you can get more.")
        text['witch_assistant_informational'] = CompressedTextMapper.convert("Red is life\nGreen is magic\nBlue is both\nI'll heal you for free though.")
        text['witch_assistant_no_bottle_buying'] = CompressedTextMapper.convert("If only you had something to put that in, like a bottle…")
        # 50
        text['potion_shop_no_empty_bottles'] = CompressedTextMapper.convert("Whoa, bucko!\nNo empty bottles.")
        text['item_get_lamp'] = CompressedTextMapper.convert("Lamp! You can see in the dark, and light torches.")
        text['item_get_boomerang'] = CompressedTextMapper.convert("Boomerang! Press START to select it.")
        text['item_get_bow'] = CompressedTextMapper.convert("You're in bow mode now!")
        text['item_get_shovel'] = CompressedTextMapper.convert("This is my new mop. My friend George, he gave me this mop. It's a pretty good mop. It's not as good as my old mop. I miss my old mop. But it's still a good mop.")
        text['item_get_magic_cape'] = CompressedTextMapper.convert("Finally! we get to play Invisble Man!")
        text['item_get_powder'] = CompressedTextMapper.convert("It's the powder. Let's cause some mischief!")
        text['item_get_flippers'] = CompressedTextMapper.convert("Splish! Splash! Let's go take a bath!")
        text['item_get_power_gloves'] = CompressedTextMapper.convert("Feel the power! You can now lift light rocks! Rock on!")
        text['item_get_pendant_courage'] = CompressedTextMapper.convert("We have the Pendant of Courage! How brave!")
        text['item_get_pendant_power'] = CompressedTextMapper.convert("We have the Pendant of Power! How robust!")
        text['item_get_pendant_wisdom'] = CompressedTextMapper.convert("We have the Pendant of Wisdom! How astute!")
        text['item_get_mushroom'] = CompressedTextMapper.convert("A Mushroom! Don't eat it. Find a witch.")
        text['item_get_book'] = CompressedTextMapper.convert("It book! U R now litterit!")
        text['item_get_moonpearl'] = CompressedTextMapper.convert("I found a shiny marble! No more hops!")
        text['item_get_compass'] = CompressedTextMapper.convert("A compass! I can now find the boss.")
        # 60
        text['item_get_map'] = CompressedTextMapper.convert("Yo! You found a MAP! Press X to see it.")
        text['item_get_ice_rod'] = CompressedTextMapper.convert("It's the Ice Rod! Freeze Ray time.")
        text['item_get_fire_rod'] = CompressedTextMapper.convert("A Rod that shoots fire? Let's burn all the things!")
        text['item_get_ether'] = CompressedTextMapper.convert("We can chill out with this!")
        text['item_get_bombos'] = CompressedTextMapper.convert("Let's set everything on fire, and melt things!")
        text['item_get_quake'] = CompressedTextMapper.convert("Time to make the earth shake, rattle, and roll!")
        text['item_get_hammer'] = CompressedTextMapper.convert("STOP!\n\nHammer Time!") # 66
        text['item_get_flute'] = CompressedTextMapper.convert("Finally! We can play the Song of Time!")
        text['item_get_cane_of_somaria'] = CompressedTextMapper.convert("Make blocks!\nThrow blocks!\nsplode Blocks!")
        text['item_get_hookshot'] = CompressedTextMapper.convert("BOING!!!\nBOING!!!\nSay no more…")
        text['item_get_bombs'] = CompressedTextMapper.convert("BOMBS! Use A to pick 'em up, throw 'em, get hurt!")
        text['item_get_bottle'] = CompressedTextMapper.convert("It's a terrarium. I hope we find a lizard!")
        text['item_get_big_key'] = CompressedTextMapper.convert("Yo! You got a Big Key!")
        text['item_get_titans_mitts'] = CompressedTextMapper.convert("So, like, you can now lift anything.\nANYTHING!")
        text['item_get_magic_mirror'] = CompressedTextMapper.convert("We could stare at this all day or, you know, beat Ganon…")
        text['item_get_fake_mastersword'] = CompressedTextMapper.convert("It's the Master Sword! …or not…\n\n         FOOL!")
        # 70
        text['post_item_get_mastersword'] = CompressedTextMapper.convert("{NOBORDER}\n{SPEED6}\n@, you got the sword!\n{CHANGEMUSIC}\nNow let's go beat up Agahnim!")
        text['item_get_red_potion'] = CompressedTextMapper.convert("Red goo to go! Nice!")
        text['item_get_green_potion'] = CompressedTextMapper.convert("Green goo to go! Nice!")
        text['item_get_blue_potion'] = CompressedTextMapper.convert("Blue goo to go! Nice!")
        text['item_get_bug_net'] = CompressedTextMapper.convert("Surprise Net! Let's catch stuff!")
        text['item_get_blue_mail'] = CompressedTextMapper.convert("Blue threads? Less damage activated!")
        text['item_get_red_mail'] = CompressedTextMapper.convert("You feel the power of the eggplant on your head.")
        text['item_get_temperedsword'] = CompressedTextMapper.convert("Nice… I now have a craving for Cheetos.")
        text['item_get_mirror_shield'] = CompressedTextMapper.convert("Pit would be proud!")
        text['item_get_cane_of_byrna'] = CompressedTextMapper.convert("It's the Blue Cane. You can now protect yourself with lag!")
        text['missing_big_key'] = CompressedTextMapper.convert("Something is missing…\nThe Big Key?")
        text['missing_magic'] = CompressedTextMapper.convert("Something is missing…\nMagic meter?")
        text['item_get_pegasus_boots'] = CompressedTextMapper.convert("Finally, it's bonking time!\nHold A to dash")
        text['talking_tree_info_start'] = CompressedTextMapper.convert("Whoa! I can talk again!")
        text['talking_tree_info_1'] = CompressedTextMapper.convert("Yank on the pitchfork in the center of town, ya heard it here.")
        text['talking_tree_info_2'] = CompressedTextMapper.convert("Ganon is such a dingus, no one likes him, ya heard it here.")
        # 80
        text['talking_tree_info_3'] = CompressedTextMapper.convert("There is a portal near the Lost Woods, ya heard it here.")
        text['talking_tree_info_4'] = CompressedTextMapper.convert("Use bombs to quickly kill the Hinox, ya heard it here.")
        text['talking_tree_other'] = CompressedTextMapper.convert("I can breathe!")
        text['item_get_pendant_power_alt'] = CompressedTextMapper.convert("We have the Pendant of Power! How robust!")
        text['item_get_pendant_wisdom_alt'] = CompressedTextMapper.convert("We have the Pendant of Wisdom! How astute!")
        text['game_shooting_choice'] = CompressedTextMapper.convert("20 rupees.\n5 arrows.\nWin rupees!\nWant to play?\n  ≥ yes\n    no\n{CHOICE}")
        text['game_shooting_yes'] = CompressedTextMapper.convert("Let's do this!")
        text['game_shooting_no'] = CompressedTextMapper.convert("Where are you going? Straight up!")
        text['game_shooting_continue'] = CompressedTextMapper.convert("Keep playing?\n  ≥ yes\n    no\n{CHOICE}")
        text['pond_of_wishing'] = CompressedTextMapper.convert("-Wishing Pond-\n\n On Vacation")
        text['pond_item_select'] = CompressedTextMapper.convert("Pick something\nto throw in.\n{ITEMSELECT}")
        text['pond_item_test'] = CompressedTextMapper.convert("You toss this?\n  ≥ yup\n    wrong\n{CHOICE}")
        text['pond_will_upgrade'] = CompressedTextMapper.convert("You're honest, so I'll give you a present.")
        text['pond_item_test_no'] = CompressedTextMapper.convert("You sure?\n  ≥ oh yeah\n    um\n{CHOICE}")
        text['pond_item_test_no_no'] = CompressedTextMapper.convert("Well, I don't want it, so take it back.")
        text['pond_item_boomerang'] = CompressedTextMapper.convert("I don't much like you, so have this worse Boomerang.")
        # 90
        text['pond_item_shield'] = CompressedTextMapper.convert("I grant you the ability to block fireballs. Don't lose this to a pikit!")
        text['pond_item_silvers'] = CompressedTextMapper.convert("So, wouldn't it be nice to kill Ganon? These should help in the final phase.")
        text['pond_item_bottle_filled'] = CompressedTextMapper.convert("Bottle Filled!\nMoney Saved!")
        text['pond_item_sword'] = CompressedTextMapper.convert("Thank you for the sword, here is a stick of butter.")
        text['pond_of_wishing_happiness'] = CompressedTextMapper.convert("Happiness up!\nYou are now\nᚌᚋ happy!")
        text['pond_of_wishing_choice'] = CompressedTextMapper.convert("Your wish?\n  ≥more bombs\n   more arrows\n{CHOICE}")
        text['pond_of_wishing_bombs'] = CompressedTextMapper.convert("Woo-hoo!\nYou can now\ncarry ᚌᚋ bombs")
        text['pond_of_wishing_arrows'] = CompressedTextMapper.convert("Woo-hoo!\nYou can now\nhold ᚌᚋ arrows")
        text['pond_of_wishing_full_upgrades'] = CompressedTextMapper.convert("Youhave all I can give you, here are your rupees back.")
        text['mountain_old_man_first'] = CompressedTextMapper.convert("Look out for holes, and monsters.")
        text['mountain_old_man_deadend'] = CompressedTextMapper.convert("Oh, goody, hearts in jars! This place is creepy.")
        text['mountain_old_man_turn_right'] = CompressedTextMapper.convert("Turn right. Let's get out of this place.")
        text['mountain_old_man_lost_and_alone'] = CompressedTextMapper.convert("Hello. I can't see anything. Take me with you.")
        text['mountain_old_man_drop_off'] = CompressedTextMapper.convert("Here's a thing to help you, good luck!")
        text['mountain_old_man_in_his_cave_pre_agahnim'] = CompressedTextMapper.convert("You need to beat the tower at the top of the mountain.")
        text['mountain_old_man_in_his_cave'] = CompressedTextMapper.convert("You can find stuff in the tower at the top of this mountain.\nCome see me if you'd like to be healed.")
        # A0
        text['mountain_old_man_in_his_cave_post_agahnim'] = CompressedTextMapper.convert("You should be heading to the castle… you have a portal there now.\nSay hi anytime you like.")
        text['tavern_old_man_awake'] = CompressedTextMapper.convert("Life? Love? Happiness? The question you should really ask is: Was this generated by Stoops Alu or Stoops Jet?")
        text['tavern_old_man_unactivated_flute'] = CompressedTextMapper.convert("You should play that flute for the weathervane, cause reasons.")
        text['tavern_old_man_know_tree_unactivated_flute'] = CompressedTextMapper.convert("You should play that flute for the weathervane, cause reasons.")
        text['tavern_old_man_have_flute'] = CompressedTextMapper.convert("Life? Love? Happiness? The question you should really ask is: Was this generated by Stoops Alu or Stoops Jet?")
        text['chicken_hut_lady'] = CompressedTextMapper.convert("This is\nChristos' hut.\n\nHe's out, searching for a bow.")
        text['running_man'] = CompressedTextMapper.convert("Catch me,\nIf you can!")
        text['game_race_sign'] = CompressedTextMapper.convert("Why are you reading this sign? Run!!!")
        text['sign_bumper_cave'] = CompressedTextMapper.convert("You need Cape, but not Hookshot")
        text['sign_catfish'] = CompressedTextMapper.convert("toss rocks\ntoss items\ntoss cookies")
        text['sign_north_village_of_outcasts'] = CompressedTextMapper.convert("↑ Skull Woods\n\n↓ Steve's Town")
        text['sign_south_of_bumper_cave'] = CompressedTextMapper.convert("\n→ Dark Sanctuary")
        text['sign_east_of_pyramid'] = CompressedTextMapper.convert("\n→ Dark Palace")
        text['sign_east_of_bomb_shop'] = CompressedTextMapper.convert("\n← Bomb Shoppe")
        text['sign_east_of_mire'] = CompressedTextMapper.convert("\n← Misery Mire\n no way in.\n no way out.")
        text['sign_village_of_outcasts'] = CompressedTextMapper.convert("Have a Trulie Awesome Day!")
        # B0
        text['sign_before_wishing_pond'] = CompressedTextMapper.convert("waterfall\nup ahead\nmake wishes")
        text['sign_before_catfish_area'] = CompressedTextMapper.convert("→↑ Have you met Woeful Ike?")
        text['castle_wall_guard'] = CompressedTextMapper.convert("Looking for a Princess? Look downstairs.")
        text['gate_guard'] = CompressedTextMapper.convert("No Lonks Allowed!")
        text['telepathic_tile_eastern_palace'] = CompressedTextMapper.convert("{NOBORDER}\nYou need a Bow to get past the red Eyegore. derpy")
        text['telepathic_tile_tower_of_hera_floor_4'] = CompressedTextMapper.convert("{NOBORDER}\nIf you find a shiny ball, you can be you in the Dark World.")
        text['hylian_text_1'] = CompressedTextMapper.convert("%== %== %==\n ^ %==% ^\n%== ^%%^ ==^")
        text['mastersword_pedestal_translated'] = CompressedTextMapper.convert("A test of strength: If you have 3 pendants, I'm yours.")
        text['telepathic_tile_spectacle_rock'] = CompressedTextMapper.convert("{NOBORDER}\n{NOBORDER}\nUse the Mirror, or the Hookshot and Hammer, to get to Tower of Hera!")
        text['telepathic_tile_swamp_entrance'] = CompressedTextMapper.convert("{NOBORDER}\nDrain the floodgate to raise the water here!")
        text['telepathic_tile_thieves_town_upstairs'] = CompressedTextMapper.convert("{NOBORDER}\nBlind hate's bright light.")
        text['telepathic_tile_misery_mire'] = CompressedTextMapper.convert("{NOBORDER}\nLighting 4 torches will open your way forward!")
        text['hylian_text_2'] = CompressedTextMapper.convert("%%^= %==%\n ^ =%^=\n==%= ^^%^")
        text['desert_entry_translated'] = CompressedTextMapper.convert(
            "Kneel before this stone, and magic will move around you.")
        text['telepathic_tile_under_ganon'] = CompressedTextMapper.convert("Haha")
        text['telepathic_tile_palace_of_darkness'] = CompressedTextMapper.convert(
            "{NOBORDER}\nThis is a funny looking Enemizer")
        # C0
        text['telepathic_tile_desert_bonk_torch_room'] = CompressedTextMapper.convert("{NOBORDER}\nThings can be knocked down, if you fancy yourself a dashing dude.")
        text['telepathic_tile_castle_tower'] = CompressedTextMapper.convert("{NOBORDER}\nYou can reflect Agahnim's energy with Sword, Bug-net or Hammer.")
        text['telepathic_tile_ice_large_room'] = CompressedTextMapper.convert("{NOBORDER}\nAll right stop collaborate and listen\nIce is back with my brand new invention")
        text['telepathic_tile_turtle_rock'] = CompressedTextMapper.convert("{NOBORDER}\nYou shall not pass… without the red cane")
        text['telepathic_tile_ice_entrance'] = CompressedTextMapper.convert("{NOBORDER}\nYou can use Fire Rod or Bombos to pass.")
        text['telepathic_tile_ice_stalfos_knights_room'] = CompressedTextMapper.convert("{NOBORDER}\nKnock 'em down and then bomb them dead.")
        text['telepathic_tile_tower_of_hera_entrance'] = CompressedTextMapper.convert(
            "{NOBORDER}\nThis is a bad place, with a guy who will make you fall…\n\n\na lot.")
        text['houlihan_room'] = CompressedTextMapper.convert(
            "Multiworld Tournament winners\nSGLive 2021 BadmoonZ")
        text['caught_a_bee'] = CompressedTextMapper.convert("Caught a Bee\n  ≥ keep\n    release\n{CHOICE}")
        text['caught_a_fairy'] = CompressedTextMapper.convert("Caught Fairy!\n  ≥ keep\n    release\n{CHOICE}")
        text['no_empty_bottles'] = CompressedTextMapper.convert("Whoa, bucko!\nNo empty bottles.")
        text['game_race_boy_time'] = CompressedTextMapper.convert("Your time was\nᚎᚍ min ᚌᚋ sec.")
        text['game_race_girl'] = CompressedTextMapper.convert("You have 15 seconds,\nGo… Go… Go…")
        text['game_race_boy_success'] = CompressedTextMapper.convert("Nice!\nYou can have this trash!")
        text['game_race_boy_failure'] = CompressedTextMapper.convert("Too slow!\nI keep my\nprecious!")
        text['game_race_boy_already_won'] = CompressedTextMapper.convert("You already have your prize, dingus!")
        # D0
        text['game_race_boy_sneaky'] = CompressedTextMapper.convert("Thought you could sneak in, eh?")
        text['bottle_vendor_choice'] = CompressedTextMapper.convert("I gots bottles.\nYous gots 100 rupees?\n  ≥ I want\n    no way!\n{CHOICE}")
        text['bottle_vendor_get'] = CompressedTextMapper.convert("Nice! Hold it up son! Show the world what you got!")
        text['bottle_vendor_no'] = CompressedTextMapper.convert("Fine! I didn't want your money anyway.")
        text['bottle_vendor_already_collected'] = CompressedTextMapper.convert("Dude! You already have it.")
        text['bottle_vendor_bee'] = CompressedTextMapper.convert("Cool! A bee! Here's 100 rupees.")
        text['bottle_vendor_fish'] = CompressedTextMapper.convert("Whoa! A fish! You walked this all the way here?")
        text['hobo_item_get_bottle'] = CompressedTextMapper.convert("You think life is rough? I guess you can take my last item. Except this tent. That's MY tent!")
        text['blacksmiths_what_you_want'] = CompressedTextMapper.convert("Nice of you to come back!\nWould you like us mess with your sword?\n  ≥ Temper\n    It's fine\n{CHOICE}")
        text['blacksmiths_paywall'] = CompressedTextMapper.convert("It's 10 rupees\n  ≥ Easy\n    Hang on…\n{CHOICE}")
        text['blacksmiths_extra_okay'] = CompressedTextMapper.convert("Are you sure you're sure?\n  ≥ Ah, yup\n    Hang on…\n{CHOICE}")
        text['blacksmiths_tempered_already'] = CompressedTextMapper.convert("Whelp… We can't make this any better.")
        text['blacksmiths_temper_no'] = CompressedTextMapper.convert("Oh, come by any time!")
        text['blacksmiths_bogart_sword'] = CompressedTextMapper.convert("We're going to have to take it to work on it.")
        text['blacksmiths_get_sword'] = CompressedTextMapper.convert("Sword is donw. Now, back to our bread!")
        text['blacksmiths_shop_before_saving'] = CompressedTextMapper.convert("I lost my friend. Help me find him!")
        # E0
        text['blacksmiths_shop_saving'] = CompressedTextMapper.convert("You found him! Colour me happy! Come back right away and we will bang on your sword.")
        text['blacksmiths_collect_frog'] = CompressedTextMapper.convert("Ribbit! Ribbit! Let's find my partner. To the shop!")
        text['blacksmiths_still_working'] = CompressedTextMapper.convert("Something this precious takes time… Come back later.")
        text['blacksmiths_saving_bows'] = CompressedTextMapper.convert("Thanks!\n\nThanks!")
        text['blacksmiths_hammer_anvil'] = CompressedTextMapper.convert("Dernt Take Er Jerbs!")
        text['dark_flute_boy_storytime'] = CompressedTextMapper.convert("Hi!\nI'm Stumpy\nI've been chillin' in this world for a while now, but I miss my flute. If I gave you a shovel, would you go digging for it?\n  ≥ sure\n    nahh\n{CHOICE}")
        text['dark_flute_boy_get_shovel'] = CompressedTextMapper.convert("Schaweet! Here you go. Happy digging!")
        text['dark_flute_boy_no_get_shovel'] = CompressedTextMapper.convert("Oh I see, not good enough for you… FINE!")
        text['dark_flute_boy_flute_not_found'] = CompressedTextMapper.convert("Still haven't found the item? Dig in the Light World around here, dingus!")
        text['dark_flute_boy_after_shovel_get'] = CompressedTextMapper.convert("So I gave you an item, and you're still here.\n\n\n\n\n\nI mean, we can sit here and stare at each other, if you like…\n\n\n\n\n\n\n\nFine, I guess you should just go.")
        text['shop_fortune_teller_lw_hint_0'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, the book opens the desert")
        text['shop_fortune_teller_lw_hint_1'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, nothing doing")
        text['shop_fortune_teller_lw_hint_2'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, I'm cheap")
        text['shop_fortune_teller_lw_hint_3'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, am I cheap?")
        text['shop_fortune_teller_lw_hint_4'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, Zora lives at the end of the river")
        text['shop_fortune_teller_lw_hint_5'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, The Cape can pass through the barrier")
        text['shop_fortune_teller_lw_hint_6'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, Spin, Hammer, or Net to hurt Agahnim")
        text['shop_fortune_teller_lw_hint_7'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, You can jump in the well by the blacksmiths")
        text['shop_fortune_teller_lw_no_rupees'] = CompressedTextMapper.convert("{BOTTOM}\nThe black cats are hungry, come back with rupees")
        text['shop_fortune_teller_lw'] = CompressedTextMapper.convert("{BOTTOM}\nWelcome to the Fortune Shoppe!\nFancy a read?\n  ≥I must know\n   negative\n{CHOICE}")
        text['shop_fortune_teller_lw_post_hint'] = CompressedTextMapper.convert("{BOTTOM}\nFor ᚋᚌ rupees\nIt is done.\nBe gone!")
        text['shop_fortune_teller_lw_no'] = CompressedTextMapper.convert("{BOTTOM}\nWell then, why did you even come in here?")
        text['shop_fortune_teller_lw_hint_8'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, why you do?")
        text['shop_fortune_teller_lw_hint_9'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, panda crackers")
        text['shop_fortune_teller_lw_hint_10'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, the missing blacksmith is south of the Village of Outcasts")
        text['shop_fortune_teller_lw_hint_11'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, open chests to get stuff")
        text['shop_fortune_teller_lw_hint_12'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, you can buy a new bomb at the Bomb Shoppe")
        text['shop_fortune_teller_lw_hint_13'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, big bombs blow up cracked walls in pyramids")
        text['shop_fortune_teller_lw_hint_14'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, you need all the crystals to open Ganon's Tower")
        text['shop_fortune_teller_lw_hint_15'] = CompressedTextMapper.convert("{BOTTOM}\nBy the black cats, Silver Arrows will defeat Ganon in his final phase")
        text['dark_sanctuary'] = CompressedTextMapper.convert("For 20 rupees I'll tell you something?\nHow about it?\n  ≥ yes\n    no\n{CHOICE}")
        text['dark_sanctuary_hint_0'] = CompressedTextMapper.convert("I once was a tea kettle, but then I moved up in the world, and now you can see me as this. Makes you wonder. What I could be next time.")
        # 100
        text['dark_sanctuary_no'] = CompressedTextMapper.convert("Then go away!")
        text['dark_sanctuary_hint_1'] = CompressedTextMapper.convert("There is a thief in the desert, he can open creepy chests that follow you. But now that we have that out of the way, Do you like my hair? I've spent eons getting it this way.")
        text['dark_sanctuary_yes'] = CompressedTextMapper.convert("With Crystals 5&6, you can find a great fairy in the pyramid.\n\nFlomp Flomp, Whizzle Whomp")
        text['dark_sanctuary_hint_2'] = CompressedTextMapper.convert(
            "All I can say is that my life is pretty plain,\n"
            + "I like watchin' the puddles gather rain,\n"
            + "And all I can do is just pour some tea for two,\n"
            + "And speak my point of view but it's not sane,\n"
            + "It's not sane")
        text['sick_kid_no_bottle'] = CompressedTextMapper.convert("{BOTTOM}\nI'm sick! Show me a bottle, get something!")
        text['sick_kid_trade'] = CompressedTextMapper.convert("{BOTTOM}\nCool Bottle! Here's something for you.")
        text['sick_kid_post_trade'] = CompressedTextMapper.convert("{BOTTOM}\nLeave me alone\nI'm sick. You have my item.")
        text['desert_thief_sitting'] = CompressedTextMapper.convert("………………………")
        text['desert_thief_following'] = CompressedTextMapper.convert("why……………")
        text['desert_thief_question'] = CompressedTextMapper.convert("I was a thief, I open purple chests!\nKeep secret?\n  ≥ sure thing\n    never!\n{CHOICE}")
        text['desert_thief_question_yes'] = CompressedTextMapper.convert("Cool, bring me any purple chests you find.")
        text['desert_thief_after_item_get'] = CompressedTextMapper.convert("You tell anyone and I will give you such a pinch!")
        text['desert_thief_reassure'] = CompressedTextMapper.convert("Bring chests. It's a secret to everyone.")
        text['hylian_text_3'] = CompressedTextMapper.convert("^^ ^%=^= =%=\n=%% =%%=^\n==%^= %=^^%")
        text['tablet_ether_book'] = CompressedTextMapper.convert("Can you make things fall out of the sky? With the Master Sword, you can!")
        text['tablet_bombos_book'] = CompressedTextMapper.convert("Can you make things fall out of the sky? With the Master Sword, you can!")
        # 110
        text['magic_bat_wake'] = CompressedTextMapper.convert("You bum! I was sleeping! Where's my magic bolts?")
        text['magic_bat_give_half_magic'] = CompressedTextMapper.convert("How you like me now?")
        text['intro_main'] = CompressedTextMapper.convert(
            "{INTRO}\n Archipelago Randomizer\n{PAUSE3}\n A Link to\n   the Past\n"
            "{PAUSE3}\n{PAUSE3}\nAfter mostly disregarding what happened in the first two games.\n"
            "{PAUSE3}\nLink awakens to his uncle leaving the house.\n{PAUSE3}\nHe just runs out the door,\n"
            "{PAUSE3}\ninto the rainy night.\n{PAUSE3}\n{CHANGEPIC}\n"
            "Ganon has moved around all the items in Hyrule and beyond.\n"
            "{PAUSE7}\nYou will have to find all the items necessary to beat Ganon.\n"
            "{PAUSE7}\nThis is your chance to be a hero.\n{PAUSE3}\n{CHANGEPIC}\n"
            "You should probably beat Ganon.\n{PAUSE9}\n{CHANGEPIC}", False)
        text['intro_throne_room'] = CompressedTextMapper.convert("{IBOX}\nLook at this Stalfos on the throne.", False)
        text['intro_zelda_cell'] = CompressedTextMapper.convert("{IBOX}\nIt is your time to shine!", False)
        text['intro_agahnim'] = CompressedTextMapper.convert("{IBOX}\nAlso, you need to defeat this guy!", False)
        text['pickup_purple_chest'] = CompressedTextMapper.convert("A curious box. Let's take it with us!")
        text['bomb_shop'] = CompressedTextMapper.convert("30 bombs for 100 rupees. Good deals all day!")
        text['bomb_shop_big_bomb'] = CompressedTextMapper.convert("30 bombs for 100 rupees, 100 rupees 1 BIG bomb. Good deals all day!")
        text['bomb_shop_big_bomb_buy'] = CompressedTextMapper.convert("Thanks!\nBoom goes the dynamite!")
        text['item_get_big_bomb'] = CompressedTextMapper.convert("YAY! press A to splode it!")
        text['kiki_second_extortion'] = CompressedTextMapper.convert("For 100 more, I'll open this place.\nHow about it?\n  ≥ open\n    nah\n{CHOICE}")
        text['kiki_second_extortion_no'] = CompressedTextMapper.convert("Heh, good luck getting in.")
        text['kiki_second_extortion_yes'] = CompressedTextMapper.convert("Yay! Rupees!\nOkay, let's do this!")
        text['kiki_first_extortion'] = CompressedTextMapper.convert("I'm Kiki, I like rupees, may I have 10?\nHow about it?\n  ≥ yes\n    no\n{CHOICE}")
        text['kiki_first_extortion_yes'] = CompressedTextMapper.convert("Nice. I'll tag along with you for a bit.")
        # 120
        text['kiki_first_extortion_no'] = CompressedTextMapper.convert("Pfft. I have no reason to hang. See ya!")
        text['kiki_leaving_screen'] = CompressedTextMapper.convert("No no no no no! We should play by my rules! Goodbye…")
        text['blind_in_the_cell'] = CompressedTextMapper.convert("You saved me!\nPlease get me out of here!")
        text['blind_by_the_light'] = CompressedTextMapper.convert("Aaaahhhh~!\nS-so bright~!")
        text['blind_not_that_way'] = CompressedTextMapper.convert("No! Don't go that way!")
        text['aginah_l1sword_no_book'] = CompressedTextMapper.convert("I once had a fish dinner. I still remember it to this day.")
        text['aginah_l1sword_with_pendants'] = CompressedTextMapper.convert("Do you remember when I was young?\n\nI sure don't.")
        text['aginah'] = CompressedTextMapper.convert("So, I've been living in this cave for years, and you think you can just come along and bomb open walls?")
        text['aginah_need_better_sword'] = CompressedTextMapper.convert("Once, I farted in this cave so bad all the jazz hands guys ran away and hid in the sand.")
        text['aginah_have_better_sword'] = CompressedTextMapper.convert("Pandas are very vicious animals. Never forget…\n\n\n\n\nI never will")
        text['catfish'] = CompressedTextMapper.convert("You woke me from my nap! Take this, and get out!")
        text['catfish_after_item'] = CompressedTextMapper.convert("I don't have anything else for you!\nTake this!")
        # 12C
        text['lumberjack_right'] = CompressedTextMapper.convert("One of us always lies.")
        text['lumberjack_left'] = CompressedTextMapper.convert("One of us always tells the truth.")
        text['lumberjack_left_post_agahnim'] = CompressedTextMapper.convert("One of us likes peanut butter.")
        text['fighting_brothers_right'] = CompressedTextMapper.convert("I walled off my brother Leo\n\nWhat a dingus.\n")
        # 130
        text['fighting_brothers_right_opened'] = CompressedTextMapper.convert("Now I should probably talk to him…")
        text['fighting_brothers_left'] = CompressedTextMapper.convert("Did you come from my brothers room?\n\nAre we cool?")
        text['maiden_crystal_1'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nI have a pretty red dress.\n{SPEED1}\nJust thought I would tell you.")
        text['maiden_crystal_2'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nI have a pretty blue dress.\n{SPEED1}\nJust thought I would tell you.")
        text['maiden_crystal_3'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nI have a pretty gold dress.\n{SPEED1}\nJust thought I would tell you.")
        text['maiden_crystal_4'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nI have a pretty redder dress.\n{SPEED1}\nJust thought I would tell you.")
        text['maiden_crystal_5'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nI have a pretty green dress.\n{SPEED1}\nJust thought I would tell you.")
        text['maiden_crystal_6'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nI have a pretty green dress.\n{SPEED1}\nJust thought I would tell you.")
        text['maiden_crystal_7'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nIt's about friggin time.\n{SPEED1}\nDo you know how long I've been waiting?")
        text['maiden_ending'] = CompressedTextMapper.convert("May the way of the hero lead to the Triforce")
        text['maiden_confirm_understood'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nCapisce?\n  ≥ Yes\n    No\n{CHOICE}")
        text['barrier_breaking'] = CompressedTextMapper.convert("What did the seven crystals say to Ganon's Tower?")
        text['maiden_crystal_7_again'] = CompressedTextMapper.convert("{SPEED2}\n{BOTTOM}\n{NOBORDER}\nIt's about friggin time.\n{SPEED1}\nDo you know how long I have been waiting?")
        text['agahnim_zelda_teleport'] = CompressedTextMapper.convert("I am a magician, and this is my act. Watch as I make this girl disappear")
        text['agahnim_magic_running_away'] = CompressedTextMapper.convert("And now, the end is near\nAnd so I face the final curtain\nMy friend, I'll say it clear\nI'll state my case, of which I'm certain\nI've lived a life that's full\nI've traveled each and every highway\nBut more, much more than this\nI did it my way")
        text['agahnim_hide_and_seek_found'] = CompressedTextMapper.convert("Peek-a-boo!")
        text['agahnim_defeated'] = CompressedTextMapper.convert("Arrrgggghhh. Well you're coming with me!")
        text['agahnim_final_meeting'] = CompressedTextMapper.convert("You have done well to come this far. Now, die!")
        # 142
        text['zora_meeting'] = CompressedTextMapper.convert("What do you want?\n  ≥ Flippers\n    Nothin'\n{CHOICE}")
        text['zora_tells_cost'] = CompressedTextMapper.convert("Fine! But they aren't cheap. You got 500 rupees?\n  ≥ Duh\n    Oh carp\n{CHOICE}")
        text['zora_get_flippers'] = CompressedTextMapper.convert("Here's some Flippers for you! Swim little fish, swim.")
        text['zora_no_cash'] = CompressedTextMapper.convert("Fine!\nGo get some more money first.")
        text['zora_no_buy_item'] = CompressedTextMapper.convert("Wah hoo! Well, whenever you want to see these gills, stop on by.")
        text['kakariko_saharalasa_grandson'] = CompressedTextMapper.convert("My grandpa is over in the East. I'm bad with directions. I'll mark your map. Best of luck!\n{HARP}")
        text['kakariko_saharalasa_grandson_next'] = CompressedTextMapper.convert("Someday I'll be in a high school band!")
        text['dark_palace_tree_dude'] = CompressedTextMapper.convert("Did you know…\n\n\nA tree typically has many secondary branches supported clear of the ground by the trunk. This trunk typically contains woody tissue for strength, and vascular tissue to carry materials from one part of the tree to another.")
        text['fairy_wishing_ponds'] = CompressedTextMapper.convert("\n-wishing pond-\n\nThrow item in?\n  ≥ Yesh\n    No\n{CHOICE}")
        text['fairy_wishing_ponds_no'] = CompressedTextMapper.convert("\n   stop it!")
        text['pond_of_wishing_no'] = CompressedTextMapper.convert("\n  fine then!")
        text['pond_of_wishing_return_item'] = CompressedTextMapper.convert("Okay. Here's your item back, cause I can't use it. I'm stuck in this fountain")
        text['pond_of_wishing_throw'] = CompressedTextMapper.convert("How many?\n  ≥ᚌᚋ rupees\n   ᚎᚍ rupees\n{CHOICE}")
        text['pond_pre_item_silvers'] = CompressedTextMapper.convert("I like you, so here's a thing you can use to beat up Ganon.")
        # 150
        text['pond_of_wishing_great_luck'] = CompressedTextMapper.convert("\nis great luck")
        text['pond_of_wishing_good_luck'] = CompressedTextMapper.convert("\n is good luck")
        text['pond_of_wishing_meh_luck'] = CompressedTextMapper.convert("\n is meh luck")
        # Repurposed to no items in Randomizer
        text['pond_of_wishing_bad_luck'] = CompressedTextMapper.convert("Why you come in here and pretend like you have something this fountain wants? Come back with bottles!")
        text['pond_of_wishing_fortune'] = CompressedTextMapper.convert("by the way, your fortune,")
        text['item_get_14_heart'] = CompressedTextMapper.convert("3 more to go\n      ¼\nYay!")
        text['item_get_24_heart'] = CompressedTextMapper.convert("2 more to go\n      ½\nWhee!")
        text['item_get_34_heart'] = CompressedTextMapper.convert("1 more to go\n      ¾\nGood job!")
        text['item_get_whole_heart'] = CompressedTextMapper.convert("You got a whole ♥!!\nGo you!")
        text['item_get_sanc_heart'] = CompressedTextMapper.convert("You got a whole ♥!\nGo you!")
        text['fairy_fountain_refill'] = CompressedTextMapper.convert("Well done, lettuce have a cup of tea…")
        text['death_mountain_bullied_no_pearl'] = CompressedTextMapper.convert("The following license applies to the base patch for the randomizer.\n\nCopyright (c) 2017 LLCoolDave\n\nCopyright (c) 2021 Berserker66\n\nCopyright (c) 2021 CaitSith2\n\nCopyright 2016, 2017 Equilateral IT\n\n Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.")
        text['death_mountain_bullied_with_pearl'] = CompressedTextMapper.convert("The software is provided \"as is\", without warranty of any kind, express or implied, including but not limited to the warranties of\nmerchantability,\nfitness for a particular purpose and\nnoninfringement.\nIn no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the Software or the use or other dealings in the software.")
        text['death_mountain_bully_no_pearl'] = CompressedTextMapper.convert("Add garlic, ginger and apple and cook for 2 minutes. Add carrots, potatoes, garam masala and curry powder and stir well. Add tomato paste, stir well and slowly add red wine and bring to a boil. Add sugar, soy sauce and water, stir and bring to a boil again.")
        text['death_mountain_bully_with_pearl'] = CompressedTextMapper.convert("I think I forgot how to smile…")
        text['shop_darkworld_enter'] = CompressedTextMapper.convert("It's dangerous outside, buy my crap for safety.")
        # 160
        text['game_chest_village_of_outcasts'] = CompressedTextMapper.convert("Pay 30 rupees, open 2 chests. Are you lucky?\nSo, Play game?\n  ≥ play\n    never!\n{CHOICE}")
        text['game_chest_no_cash'] = CompressedTextMapper.convert("So, like, you need 30 rupees.\nSilly!")
        text['game_chest_not_played'] = CompressedTextMapper.convert("You want to play a game?\nTalk to me.")
        text['game_chest_played'] = CompressedTextMapper.convert("You've opened the chests!\nTime to go.")
        text['game_chest_village_of_outcasts_play'] = CompressedTextMapper.convert("Alright, brother!\nGo play!")
        text['shop_first_time'] = CompressedTextMapper.convert("Welcome to my shop! Select stuff with A.\nDO IT NOW!")
        text['shop_already_have'] = CompressedTextMapper.convert("So, like, you already have one of those.")
        text['shop_buy_shield'] = CompressedTextMapper.convert("Thanks! Now you can block fire balls.")
        text['shop_buy_red_potion'] = CompressedTextMapper.convert("Red goo, so good! It's like a fairy in a bottle, except you have to activate it yourself.")
        text['shop_buy_arrows'] = CompressedTextMapper.convert("Arrows! Cause you were too lazy to look under some pots!")
        text['shop_buy_bombs'] = CompressedTextMapper.convert("You bought bombs. What, couldn't find any under bushes?")
        text['shop_buy_bee'] = CompressedTextMapper.convert("He's my best friend. Please take care of him, and never lose him.")
        text['shop_buy_heart'] = CompressedTextMapper.convert("You really just bought this?")
        text['shop_first_no_bottle_buy'] = CompressedTextMapper.convert("Why does no one own bottles? Go find one first!")
        text['shop_buy_no_space'] = CompressedTextMapper.convert("You are carrying to much crap, go use some of it first!")
        text['ganon_fall_in'] = CompressedTextMapper.convert("You drove\naway my other\nself, Agahnim,\ntwo times…\nBut, I won't\ngive you the\nTriforce.\nI'll defeat\nyou!")
        # 170
        text['ganon_phase_3'] = CompressedTextMapper.convert("Can you beat\nmy darkness\ntechnique?")
        text['lost_woods_thief'] = CompressedTextMapper.convert("Did you just vent?")
        text['blinds_hut_dude'] = CompressedTextMapper.convert("I'm just some dude. This is Blind's hut.")
        text['end_triforce'] = CompressedTextMapper.convert("{SPEED2}\n{MENU}\n{NOBORDER}\n     G G")
        text['toppi_fallen'] = CompressedTextMapper.convert("Ouch!\n\nYou Jerk!")
        text['kakariko_tavern_fisherman'] = CompressedTextMapper.convert("Don't argue\nwith a frozen\nDeadrock.\nHe'll never\nchange his\nposition!")
        text['thief_money'] = CompressedTextMapper.convert("It's a secret to everyone.")
        text['thief_desert_rupee_cave'] = CompressedTextMapper.convert("So you, like, busted down my door, and are being a jerk by talking to me? Normally I would be angry and make you pay for it, but I bet you're just going to break all my pots and steal my 50 rupees.")
        text['thief_ice_rupee_cave'] = CompressedTextMapper.convert("I'm a rupee pot farmer. One day I will take over the world with my skillz. Have you met my brother in the desert? He's way richer than I am.")
        text['telepathic_tile_south_east_darkworld_cave'] = CompressedTextMapper.convert("~~ dev cave ~~\n  no farming\n   required")
        text['cukeman'] = CompressedTextMapper.convert("Hey mon!")
        text['cukeman_2'] = CompressedTextMapper.convert("You found Shabadoo, huh?\nNiiiiice.")
        text['potion_shop_no_cash'] = CompressedTextMapper.convert("Yo! I'm not running a charity here.")
        text['kakariko_powdered_chicken'] = CompressedTextMapper.convert("Smallhacker…\n\n\nWas hiding, you found me!\n\n\nOkay, you can leave now.")
        text['game_chest_south_of_kakariko'] = CompressedTextMapper.convert("Pay 20 rupees, open 1 chest. Are you lucky?\nSo, Play game?\n  ≥ play\n    never!\n{CHOICE}")
        text['game_chest_play_yes'] = CompressedTextMapper.convert("Good luck then")
        # 180
        text['game_chest_play_no'] = CompressedTextMapper.convert("Well fine, I didn't want your rupees.")
        text['game_chest_lost_woods'] = CompressedTextMapper.convert("Pay 100 rupees open 1 chest. Are you lucky?\nSo, Play game?\n  ≥ play\n    never!\n{CHOICE}")
        text['kakariko_flophouse_man_no_flippers'] = CompressedTextMapper.convert("I really hate mowing my yard.\nI moved my house and everyone else's to avoid it.\n{PAGEBREAK}\nI hope you don't mind.")
        text['kakariko_flophouse_man'] = CompressedTextMapper.convert("I really hate mowing my yard.\nI moved my house and everyone else's to avoid it.\n{PAGEBREAK}\nI hope you don't mind.")
        text['menu_start_2'] = CompressedTextMapper.convert("{MENU}\n{SPEED0}\n≥@'s house\n Sanctuary\n{CHOICE3}", False)
        text['menu_start_3'] = CompressedTextMapper.convert("{MENU}\n{SPEED0}\n≥@'s house\n Sanctuary\n Mountain Cave\n{CHOICE2}", False)
        text['menu_pause'] = CompressedTextMapper.convert("{SPEED0}\n≥continue\n save and quit\n{CHOICE3}", False)
        text['game_digging_choice'] = CompressedTextMapper.convert("Have 80 Rupees? Want to play digging game?\n  ≥yes\n   no\n{CHOICE}")
        text['game_digging_start'] = CompressedTextMapper.convert("Okay, use the shovel with Y!")
        text['game_digging_no_cash'] = CompressedTextMapper.convert("Shovel rental is 80 rupees.\nI have all day")
        text['game_digging_end_time'] = CompressedTextMapper.convert("Time's up!\nTime for you to go.")
        text['game_digging_come_back_later'] = CompressedTextMapper.convert("Come back later, I have to bury things.")
        text['game_digging_no_follower'] = CompressedTextMapper.convert("Something is following you. I don't like.")
        text['menu_start_4'] = CompressedTextMapper.convert("{MENU}\n{SPEED0}\n≥@'s house\n Mountain Cave\n{CHOICE3}", False)
        # Start of new text data
        text['ganon_fall_in_alt'] = CompressedTextMapper.convert("You think you\nare ready to\nface me?\n\nI will not die\n\nunless you\ncomplete your\ngoals. Dingus!")
        text['ganon_phase_3_alt'] = CompressedTextMapper.convert("Got wax in\nyour ears?\nI cannot die!")
        # 190
        text['sign_east_death_mountain_bridge'] = CompressedTextMapper.convert("How did you get up here?")
        text['fish_money'] = CompressedTextMapper.convert("It's a secret to everyone.")
        text['sign_ganons_tower'] = CompressedTextMapper.convert("You need all 7 crystals to enter.")
        text['sign_ganon'] = CompressedTextMapper.convert("You need all 7 crystals to beat Ganon.")
        text['ganon_phase_3_no_bow'] = CompressedTextMapper.convert("You have no bow. Dingus!")
        text['ganon_phase_3_no_silvers_alt'] = CompressedTextMapper.convert("You can't best me without silver arrows!")
        text['ganon_phase_3_no_silvers'] = CompressedTextMapper.convert("You can't best me without silver arrows!")
        text['ganon_phase_3_silvers'] = CompressedTextMapper.convert("Oh no! Silver! My one true weakness!")
        text['murahdahla'] = CompressedTextMapper.convert("Hello @. I\nam Murahdahla, brother of\nSahasrahla and Aginah. Behold the power of\ninvisibility.\n{PAUSE3}\n… … …\nWait! you can see me? I knew I should have\nhidden in  a hollow tree.")
        text['end_pad_data'] = bytearray([0xfb])
        text['terminator'] = bytearray([0xFF, 0xFF])

class TriviaQuestion():
    question: list
    correct_answer: str
    incorrect_answer_1: str
    incorrect_answer_2: str

    def __init__(self, question: list, correct_answer: str, incorrect_answer_1: str, incorrect_answer_2: str):
        self.question = question.copy()
        self.correct_answer = correct_answer
        self.incorrect_answer_1 = incorrect_answer_1
        self.incorrect_answer_2 = incorrect_answer_2

        
trivia_addrs = {
    "easy": [
        0x34F800,
        0x34F900,
        0x34FA00,
        0x34FB00,
        0x34FC00,
        0x34FD00,
    ],
    "medium": [
        0x34F850,
        0x34F950,
        0x34FA50,
        0x34FB50,
        0x34FC50,
        0x34FD50,
    ],
    "hard": [
        0x34F8A0,
        0x34F9A0,
        0x34FAA0,
        0x34FBA0,
        0x34FCA0,
        0x34FDA0,
    ],
}

excluded_questions = [
    2*8, 
    7*8,
    9*8,
    10*8,
    12*8,
    16*8,
    24*8,
    27*8,
    30*8,
    35*8,
    36*8,
    41*8,
    45*8,
]

original_correct_answers = {
    # Galleon
    0: 0,
    1: 0,
    2: 2,
    3: 1,
    4: 1,
    5: 2,
    6: 1,
    7: 0,
    8: 2,
    # Cauldron
    9: 1,
    10: 0,
    11: 0,
    12: 2,
    13: 1,
    14: 0,
    15: 1,
    16: 2,
    17: 2,
    # Quay
    18: 0,
    19: 1,
    20: 2,
    21: 1,
    22: 2,
    23: 1,
    24: 1,
    25: 0,
    26: 2,
    # Kremland
    27: 2,
    28: 0,
    29: 2,
    30: 1,
    31: 1,
    32: 0,
    33: 2,
    34: 1,
    35: 2,
    # Gulch
    36: 0,
    37: 1,
    38: 2,
    39: 2,
    40: 1,
    41: 1,
    42: 2,
    43: 0,
    44: 0,
    # Keep
    45: 1,
    46: 2,
    47: 1,
    48: 0,
    49: 2,
    50: 1,
    51: 1,
    52: 0,
    53: 2,
}
        
trivia_easy_a_link_to_the_past = [
    TriviaQuestion(
        [
            """°""", 
            """  In A Link to the Past, what°""", 
            """   is the name of the boss in°""", 
            """         Desert Palace?°""", 
            """°""", 
            """°""", 
        ],
        """Lanmola°°""", 
        """Twinmold°°""", 
        """Molgera°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  When does Armor Knights turn°""", 
            """   red in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """When there's one left°°""", 
        """After defeating one°°""", 
        """They're always red°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  How many eyes Moldorm has in°""", 
            """      A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """2°°""", 
        """8°°""", 
        """5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   Where's Moldorm weak point°""", 
            """     in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """In the tail°°""", 
        """In the left eye°°""", 
        """In the head°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  What's a valid way to remove°""", 
            """     Helmasaur King's mask°""", 
            """     in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """With the hammer°°""", 
        """With Bombos°°""", 
        """With the tempered sword°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which weapons are needed°""", 
            """      to defeat Trinexx in°""", 
            """      A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """Ice Rod and Fire Rod°°""", 
        """Cane of Somaria and°        Ice rod°""", 
        """Fire Rod and°        Cane of Byrna°""", 
    ),
]

trivia_easy_actraiser = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """In ActRaiser, what's the name of°""", 
            """  the final area of the game?°""", 
            """°""", 
            """°""", 
        ],
        """Death Heim°°""", 
        """Death Heimr°°""", 
        """Death Helm°°""", 
    ),
]

trivia_easy_astalon = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ Where does Astalon take place?°""", 
            """°""", 
            """°""", 
            """°""", 
        ],
        """In a Tower°°""", 
        """In a Castle°°""", 
        """In a Mansion°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """In Astalon, what are the colors°""", 
            """  of the different keys/doors°""", 
            """          in the game?°""", 
            """°""", 
            """°""", 
        ],
        """Blue, Red and White°°""", 
        """Blue, Purple and Green°°""", 
        """Blue, Gray and Orange°°""", 
    ),
]

trivia_easy_castlevania_circle_of_the_moon = [
    TriviaQuestion(
        [
            """        In Castlevania:°""", 
            """      Circle of the Moon,°""", 
            """         what does the°""", 
            """       abbreviation "DSS"°""", 
            """           stand for?°""", 
            """°""", 
        ],
        """Dual Setup System°°""", 
        """Defense/Strike System°°""", 
        """It has no meaning°°""", 
    ),
]

trivia_easy_cave_story = [
    TriviaQuestion(
        [
            """°""", 
            """     What's the name of the°""", 
            """ upgraded version of the Polar°""", 
            """   Star Weapon in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """Spur°°""", 
        """Polar Two°°""", 
        """Whimsical Star°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Cave Story, what's the°""", 
            """   item that allows quenching°""", 
            """          fireplaces?°""", 
            """°""", 
            """°""", 
        ],
        """Jellyfish Juice°°""", 
        """Sprinkler°°""", 
        """Charcoal°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which objects are shoot°""", 
            """     from a level 3 Nemesis°""", 
            """         in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """Rubber ducks°°""", 
        """Bubbles°°""", 
        """Missiles°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  What makes Mimigas turn into°""", 
            """    monsters in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """Eating a red flower°°""", 
        """Getting stressed°°""", 
        """Drinking a lot of water°°""", 
    ),
]

trivia_easy_diddy_kong_racing = [
    TriviaQuestion(
        [
            """°""", 
            """ How many missiles are given by°""", 
            """ the third red balloon upgrade°""", 
            """     in Diddy Kong Racing?°""", 
            """°""", 
            """°""", 
        ],
        """10 missiles°°""", 
        """8 missiles°°""", 
        """12 missiles°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     Which of the following°""", 
            """    characters isn't part of°""", 
            """      Diddy Kong Racing's°""", 
            """        playable roster?°""", 
            """°""", 
        ],
        """Dixie°°""", 
        """Conker°°""", 
        """Banjo°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which Snowflake Mountain°""", 
            """    race contains a Wish Key°""", 
            """     in Diddy Kong Racing?°""", 
            """°""", 
            """°""", 
        ],
        """Snowball Valley°°""", 
        """Frosty Village°°""", 
        """Everfrost Peak°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """      Where's the Wish Key°""", 
            """       in Ancient Lake in°""", 
            """       Diddy Kong Racing?°""", 
            """°""", 
            """°""", 
        ],
        """Above an offtrack ramp°°""", 
        """Below a dinosaur foot°°""", 
        """Underwater°°""", 
    ),
]

trivia_easy_donkey_kong_country_2 = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  What's the name of your fish°""", 
            """       companion in DKC2?°""", 
            """°""", 
            """°""", 
        ],
        """Glimmer°°""", 
        """Glitter°°""", 
        """Grizzly°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  What's the name of your blue°""", 
            """  swordfish companion in DKC2?°""", 
            """°""", 
            """°""", 
        ],
        """Enguarde°°""", 
        """Pointy°°""", 
        """Eduardo°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Donkey Kong Country 2,°""", 
            """   what are the colors of the°""", 
            """    crocodile heads you can°""", 
            """    jump on in Hot-Head Hop?°""", 
            """°""", 
        ],
        """Green and Brown°°""", 
        """Red and Blue°°""", 
        """Blue and Green°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Donkey Kong Country 2,°""", 
            """ how many times do you have to°""", 
            """     hit Krow to kill him?°""", 
            """°""", 
            """°""", 
        ],
        """4°°""", 
        """6°°""", 
        """10°°""", 
    ),
]

trivia_easy_donkey_kong_country_3 = [
    TriviaQuestion(
        [
            """°""", 
            """     How many brother bears°""", 
            """     are present in Donkey°""", 
            """        Kong Country 3?°""", 
            """°""", 
            """°""", 
        ],
        """13°°""", 
        """10°°""", 
        """15°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which item you need to give°""", 
            """   Barter in order obtain his°""", 
            """     No. 6 wrench in Donkey°""", 
            """        Kong Country 3?°""", 
            """°""", 
        ],
        """A mirror°°""", 
        """A flower°°""", 
        """A bowling ball°°""", 
    ),
]

trivia_easy_earthbound = [
    TriviaQuestion(
        [
            """°""", 
            """ In EarthBound, what flavor of°""", 
            """ yogurt can the Gourmet Yogurt°""", 
            """        Machine produce?°""", 
            """°""", 
            """°""", 
        ],
        """Trout°°""", 
        """Peanut°°""", 
        """Tofu°°""", 
    ),
]

trivia_easy_final_fantasy_mystic_quest = [
    TriviaQuestion(
        [
            """°""", 
            """       In Final Fantasy:°""", 
            """   Mystic Quest, what is the°""", 
            """           level cap?°""", 
            """°""", 
            """°""", 
        ],
        """41°°""", 
        """40°°""", 
        """99°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In a vanilla playthrough of°""", 
            """  Final Fantasy: Mystic Quest,°""", 
            """  where do you find Excalibur?°""", 
            """°""", 
            """°""", 
        ],
        """Pazuzu's Tower°°""", 
        """Mac's Ship°°""", 
        """Doom Castle°°""", 
    ),
]

trivia_easy_hollow_knight = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Hollow Knight, who do you°""", 
            """  fight in Teacher's Archive?°""", 
            """°""", 
            """°""", 
        ],
        """Uumuu°°""", 
        """Uuwuu°°""", 
        """Jelly Kingsh°°""", 
    ),
]

trivia_easy_kingdom_hearts = [
]

trivia_easy_kingdom_hearts_2 = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ How many Keyblades Roxas pulls°""", 
            """      out afront of Axel?°""", 
            """°""", 
            """°""", 
        ],
        """TWO!?°°""", 
        """FIVE!?°°""", 
        """THREE!?°°""", 
    ),
]

trivia_easy_kirby_64_the_crystal_shards = [
    TriviaQuestion(
        [
            """°""", 
            """ How many different statues can°""", 
            """    be seen with Cutter+Rock°""", 
            """          in Kirby 64?°""", 
            """°""", 
            """°""", 
        ],
        """6°°""", 
        """4°°""", 
        """8°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  How many battle phases does°""", 
            """     Acro have in Kirby 64?°""", 
            """°""", 
            """°""", 
        ],
        """2°°""", 
        """1°°""", 
        """3°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which power is required°""", 
            """    to collect Pop Star 1's°""", 
            """      third crystal shard°""", 
            """          in Kirby 64?°""", 
            """°""", 
        ],
        """Bomb°°""", 
        """Stone°°""", 
        """Spark°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of the following items°""", 
            """  Adeleine draws for you when°""", 
            """     you are at full health°""", 
            """          in Kirby 64?°""", 
            """°""", 
        ],
        """A 1-Up°°""", 
        """A Maxim Tomato°°""", 
        """An invincibility candy°°""", 
    ),
]

trivia_easy_kirbys_dream_land_3 = [
    TriviaQuestion(
        [
            """°""", 
            """       What's the name of°""", 
            """      your blue friend in°""", 
            """     Kirby's Dream Land 3?°""", 
            """°""", 
            """°""", 
        ],
        """Gooey°°""", 
        """Guey°°""", 
        """Goofy°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """       What's the name of°""", 
            """       your cat friend in°""", 
            """     Kirby's Dream Land 3?°""", 
            """°""", 
            """°""", 
        ],
        """Nago°°""", 
        """Rick°°""", 
        """Chuchu°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """       What's the name of°""", 
            """      your bird friend in°""", 
            """     Kirby's Dream Land 3?°""", 
            """°""", 
            """°""", 
        ],
        """Pitch°°""", 
        """Coo°°""", 
        """Kine°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """       Which enemy grants°""", 
            """       the cutter ability°""", 
            """    in Kirby's Dream Land 3?°""", 
            """°""", 
            """°""", 
        ],
        """Sir Kibble°°""", 
        """Rocky°°""", 
        """Bobo°°""", 
    ),
]

trivia_easy_majoras_mask_recompiled = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ What's the name of your fairy°""", 
            """  companion in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """Tatl°°""", 
        """Tael°°""", 
        """Navi°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which mask is required to°""", 
            """    properly fight Twinmold°""", 
            """       in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """Giant's Mask°°""", 
        """Bunny Hood°°""", 
        """Keaton Mask°°""", 
    ),
]

trivia_easy_math = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """What is the result of 6/2(1+2)?°""", 
            """°""", 
            """°""", 
            """°""", 
        ],
        """9°°""", 
        """1°°""", 
        """5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """            1-(-1)=?°""", 
            """°""", 
            """°""", 
            """°""", 
        ],
        """2°°""", 
        """0°°""", 
        """-2°°""", 
    ),
]

trivia_easy_mega_man_2 = [
    TriviaQuestion(
        [
            """°""", 
            """  What is the total amount of°""", 
            """     E-Tanks you can carry°""", 
            """         in Mega Man 2?°""", 
            """°""", 
            """°""", 
        ],
        """4°°""", 
        """9°°""", 
        """5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """     Who is the main villan°""", 
            """         of Mega Man 2?°""", 
            """°""", 
            """°""", 
        ],
        """Dr. Wily°°""", 
        """Dr. Light°°""", 
        """Dr. Cossack°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Mega Man 2, What is the°""", 
            """   Primary Weakness you need°""", 
            """        to beat Air Man?°""", 
            """°""", 
            """°""", 
        ],
        """Leaf Shield°°""", 
        """Atomic Fire°°""", 
        """You Cannot Beat Him°°""", 
    ),
]

trivia_easy_mega_man_3 = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   In Mega Man 3, who is the°""", 
            """   main villain of the game?°""", 
            """°""", 
            """°""", 
        ],
        """Dr. Wily°°""", 
        """Dr. Wiley°°""", 
        """Dr. Willy°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Mega Man 3, who is behind°""", 
            """   the identity of Break Man?°""", 
            """°""", 
            """°""", 
        ],
        """Proto Man°°""", 
        """Roll°°""", 
        """Shadow Man°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   In Mega Man 3, What is the°""", 
            """  name of your dog companion?°""", 
            """°""", 
            """°""", 
        ],
        """Rush°°""", 
        """Tango°°""", 
        """Beat°°""", 
    ),
]

trivia_easy_mega_man_x = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  Who's the main antagonist in°""", 
            """          Mega Man X?°""", 
            """°""", 
            """°""", 
        ],
        """Sigma°°""", 
        """Ligma°°""", 
        """Sugoma°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   In which Mega Man X stage°""", 
            """ can you find the Legs Capsule?°""", 
            """°""", 
            """°""", 
        ],
        """Chill Penguin°°""", 
        """Sting Chameleon°°""", 
        """Storm Eagle°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which Maverick has to be°""", 
            """  beaten in order to turn off°""", 
            """ the lights in Spark Mandrill's°""", 
            """      stage in Mega Man X?°""", 
            """°""", 
        ],
        """Storm Eagle°°""", 
        """Launch Octopus°°""", 
        """Chill Penguin°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which Maverick has to be°""", 
            """   beaten in order to freeze°""", 
            """     Flame Mammoth's stage°""", 
            """         in Mega Man X?°""", 
            """°""", 
        ],
        """Chill Penguin°°""", 
        """Launch Octopus°°""", 
        """Storm Eagle°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   What's NOT a valid method°""", 
            """    for destroying igloos in°""", 
            """          Mega Man X?°""", 
            """°""", 
            """°""", 
        ],
        """Boomerang Cutter°°""", 
        """Hadouken°°""", 
        """Fire Wave°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In which Mega Man X stage°""", 
            """    can the Hadouken Capsule°""", 
            """           be found?°""", 
            """°""", 
            """°""", 
        ],
        """Armored Armadillo°°""", 
        """Sting Chameleon°°""", 
        """Boomer Kuwanger°°""", 
    ),
]

trivia_easy_mega_man_x2 = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  Who are the main antagonists°""", 
            """        of Mega Man X2?°""", 
            """°""", 
            """°""", 
        ],
        """X-Hunters°°""", 
        """Mechaniloids°°""", 
        """Flame Chasers°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  What's the name of the area°""", 
            """     where the final battle°""", 
            """    happens in Mega Man X2?°""", 
            """°""", 
            """°""", 
        ],
        """Central Computer°°""", 
        """Weather Control°°""", 
        """X-Hunter Stage°°""", 
    ),
]

trivia_easy_mega_man_x3 = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  Who's the main antagonist of°""", 
            """          Mega Man X3?°""", 
            """°""", 
            """°""", 
        ],
        """Dr. Doppler°°""", 
        """Dr. Serges°°""", 
        """Dr. Wily°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ In whose level is the Chimera°""", 
            """ Armor located in Mega Man X3?°""", 
            """°""", 
            """°""", 
        ],
        """Blast Hornet°°""", 
        """Sting Chameleon°°""", 
        """Gravity Beetle°°""", 
    ),
]

trivia_easy_ocarina_of_time = [
    TriviaQuestion(
        [
            """°""", 
            """   In Ocarina of Time, which°""", 
            """ dungeon has a room that is not°""", 
            """  shown when you get its map?°""", 
            """°""", 
            """°""", 
        ],
        """Inside the Deku Tree°°""", 
        """Fire Temple°°""", 
        """Bottom of the Well°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which Ocarina of Time song°""", 
            """   allows to change the time°""", 
            """    of the day in the game?°""", 
            """°""", 
            """°""", 
        ],
        """Sun's Song°°""", 
        """Song of Time°°""", 
        """Song of Storms°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which Ocarina of Time song°""", 
            """      is required to open°""", 
            """       the Door of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Song of Time°°""", 
        """Zelda's Lullaby°°""", 
        """Prelude of Light°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which boss can be found°""", 
            """   at the end of Water Temple°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Morpha°°""", 
        """Barinade°°""", 
        """Volvagia°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    What's the name of your°""", 
            """       fairy companion in°""", 
            """        Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Navi°°""", 
        """Tatl°°""", 
        """Malon°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which boots can be found at°""", 
            """     the end of Ice Cavern°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Iron Boots°°""", 
        """Hover Boots°°""", 
        """Kokiri Boots°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ How can players force Business°""", 
            """   Scrubs out of their holes°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """By reflecting their°        projectiles°""", 
        """By talking to them°°""", 
        """By getting hit by them°°""", 
    ),
]

trivia_easy_overcooked_2 = [
    TriviaQuestion(
        [
            """°""", 
            """     How many Kevin levels°""", 
            """     are there in the base°""", 
            """      Overcooked! 2 game?°""", 
            """°""", 
            """°""", 
        ],
        """8°°""", 
        """4°°""", 
        """6°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  What is the name of the dog°""", 
            """       in Overcooked! 2?°""", 
            """°""", 
            """°""", 
        ],
        """Kevin°°""", 
        """Poochy°°""", 
        """Richard°°""", 
    ),
]

trivia_easy_paper_mario = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Paper Mario 64, how many°""", 
            """  party members can Mario get?°""", 
            """°""", 
            """°""", 
        ],
        """8°°""", 
        """7°°""", 
        """6°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Paper Mario 64, what is°""", 
            """    the name of Lakilester's°""", 
            """          girlfriend?°""", 
            """°""", 
            """°""", 
        ],
        """Lakilulu°°""", 
        """Lakisophia°°""", 
        """Merluvlee°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, how many°""", 
            """   times do you fight against°""", 
            """  Jr. Troopa in all of Mario's°""", 
            """           adventure?°""", 
            """°""", 
        ],
        """6°°""", 
        """5°°""", 
        """7°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Paper Mario 64, in what°""", 
            """     village you can get a°""", 
            """          Koopa Leaf?°""", 
            """°""", 
            """°""", 
        ],
        """Koopa Village°°""", 
        """Toad Town°°""", 
        """Goomba Village°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Paper Mario 64, where can°""", 
            """  you find pebbles as a item?°""", 
            """°""", 
            """°""", 
        ],
        """Shiver Mountain°°""", 
        """Lavalava Island°°""", 
        """Mt. Rugged°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    In Paper Mario 64, which°""", 
            """    Berry restores more HP?°""", 
            """°""", 
            """°""", 
        ],
        """Red Berry°°""", 
        """Blue Berry°°""", 
        """Yellow Berry°°""", 
    ),
    TriviaQuestion(
        [
            """  In Paper Mario, your regular°""", 
            """     Jump attacks hit your°""", 
            """    opponents twice. Do your°""", 
            """    opponents' defense stats°""", 
            """   get applied to the damage°""", 
            """     dealt this way twice?°""", 
        ],
        """Yes°°""", 
        """No°°""", 
        """I've never played it°°""", 
    ),
]

trivia_easy_pokemon_crystal = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Pokemon Crystal, what are°""", 
            """  the 2 regions you can visit?°""", 
            """°""", 
            """°""", 
        ],
        """Johto and Kanto°°""", 
        """Johto and Hoenn°°""", 
        """Kanto and Hoenn°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ In Pokemon Crystal, how do you°""", 
            """     wake up the Sudowoodo?°""", 
            """°""", 
            """°""", 
        ],
        """Using the Squirtbottle°°""", 
        """Using the PokeFlute°°""", 
        """Using the Wailmer Pail°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, who is°""", 
            """ the Gym Leader who specializes°""", 
            """         in Bug types?°""", 
            """°""", 
            """°""", 
        ],
        """Bugsy°°""", 
        """Burgh°°""", 
        """Brock°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, who is°""", 
            """ the Gym Leader who specializes°""", 
            """        in Flying types?°""", 
            """°""", 
            """°""", 
        ],
        """Falkner°°""", 
        """Flannery°°""", 
        """Fantina°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """ shiny pokemon can be found in°""", 
            """       the Lake of Rage?°""", 
            """°""", 
            """°""", 
        ],
        """Gyarados°°""", 
        """Dragonair°°""", 
        """Lapras°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, who is°""", 
            """ the Gym Leader who specializes°""", 
            """        in Normal types?°""", 
            """°""", 
            """°""", 
        ],
        """Whitney°°""", 
        """Will°°""", 
        """Wallace°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    In Pokemon Crystal, what°""", 
            """     is your starting town?°""", 
            """°""", 
            """°""", 
        ],
        """New Bark Town°°""", 
        """Azalea Town°°""", 
        """Pallet Town°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Pokemon Crystal, which of°""", 
            """  these is NOT a Johto Badge?°""", 
            """°""", 
            """°""", 
        ],
        """Mine Badge°°""", 
        """Glacier Badge°°""", 
        """Hive Badge°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, who is°""", 
            """ the Gym Leader who specializes°""", 
            """        in Ghost types?°""", 
            """°""", 
            """°""", 
        ],
        """Morty°°""", 
        """Misty°°""", 
        """Melony°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, who is°""", 
            """ the Gym Leader who specializes°""", 
            """       in Fighting types?°""", 
            """°""", 
            """°""", 
        ],
        """Chuck°°""", 
        """Cheren°°""", 
        """Chili°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, who is°""", 
            """ the Gym Leader who specializes°""", 
            """        in Steel types?°""", 
            """°""", 
            """°""", 
        ],
        """Jasmine°°""", 
        """Janine°°""", 
        """Jessie°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, who is°""", 
            """ the Gym Leader who specializes°""", 
            """         in Ice types?°""", 
            """°""", 
            """°""", 
        ],
        """Pryce°°""", 
        """Proton°°""", 
        """Prince°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, who is°""", 
            """ the Gym Leader who specializes°""", 
            """        in Dragon types?°""", 
            """°""", 
            """°""", 
        ],
        """Clair°°""", 
        """Claire°°""", 
        """Clay°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, which of°""", 
            """ these places is NOT located in°""", 
            """        Goldenrod City?°""", 
            """°""", 
            """°""", 
        ],
        """Dance Theater°°""", 
        """Name Rater's House°°""", 
        """Game Corner°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, where do°""", 
            """  you see the Legendary Beasts°""", 
            """        the first time?°""", 
            """°""", 
            """°""", 
        ],
        """Burned Tower°°""", 
        """Tin Tower°°""", 
        """Radio Tower°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """   Johto Gym has no trainers°""", 
            """   other than the Gym Leader?°""", 
            """°""", 
            """°""", 
        ],
        """Olivine Gym°°""", 
        """Violet Gym°°""", 
        """Cianwood Gym°°""", 
    ),
]

trivia_easy_pokemon_emerald = [
]

trivia_easy_pokemon_red_and_blue = [
    TriviaQuestion(
        [
            """°""", 
            """    In Pokemon Red and Blue,°""", 
            """     does TM28 contain the°""", 
            """        move Tombstoner?°""", 
            """°""", 
            """°""", 
        ],
        """No°°""", 
        """Yes°°""", 
        """Sometimes°°""", 
    ),
]

trivia_easy_rabiribi = [
    TriviaQuestion(
        [
            """°""", 
            """    In which Rabi-Ribi area°""", 
            """      can Ribbon be found°""", 
            """      for the first time?°""", 
            """°""", 
            """°""", 
        ],
        """Spectral Cave°°""", 
        """Starting Forest°°""", 
        """Forgotten Cave°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  Which character can you find°""", 
            """ at Rabi-Ribi's Aurora Palace?°""", 
            """°""", 
            """°""", 
        ],
        """Nieve°°""", 
        """Kotri°°""", 
        """Cicini°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ Which Rabi-Ribi item lets you°""", 
            """          jump higher?°""", 
            """°""", 
            """°""", 
        ],
        """Rabi Slippers°°""", 
        """Bunny Whirl°°""", 
        """Bunny Amulet°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which of Ribbon's weapons°""", 
            """       allows her to use°""", 
            """       Red type attacks?°""", 
            """°""", 
            """°""", 
        ],
        """Explode Shot°°""", 
        """Healing Staff°°""", 
        """Sunny Beam°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     What's the name of the°""", 
            """     character found at the°""", 
            """       end of Rabi-Ribi's°""", 
            """        System Interior?°""", 
            """°""", 
        ],
        """Syaro°°""", 
        """Cicini°°""", 
        """Nixie°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which item lets Erina use°""", 
            """      her ultimate attack°""", 
            """         in Rabi-Ribi?°""", 
            """°""", 
            """°""", 
        ],
        """Bunny Amulet°°""", 
        """Hammer Wave°°""", 
        """Soul Heart°°""", 
    ),
]

trivia_easy_risk_of_rain_2 = [
    TriviaQuestion(
        [
            """°""", 
            """ In Risk of Rain 2, which item°""", 
            """  allows you to execute bosses°""", 
            """   in one hit and guarantee a°""", 
            """       yellow item drop?°""", 
            """°""", 
        ],
        """Trophy Hunter's Tricorn°°""", 
        """The Crowdfunder°°""", 
        """Recycler°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which item can be obtained°""", 
            """    from Cleansing Pools in°""", 
            """        Risk of Rain 2?°""", 
            """°""", 
            """°""", 
        ],
        """Irradiant Pearl°°""", 
        """Interstellar Desk Plant°°""", 
        """Topaz Brooch°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which Risk of Rain 2 item°""", 
            """       allows players to°""", 
            """        ignite enemies?°""", 
            """°""", 
            """°""", 
        ],
        """Gasoline°°""", 
        """Forgive Me Please°°""", 
        """Medkit°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which Risk of Rain 2 item°""", 
            """       allows players to°""", 
            """        prevent debuffs?°""", 
            """°""", 
            """°""", 
        ],
        """Ben's Raincoat°°""", 
        """Aegis°°""", 
        """Medkit°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which Risk of Rain 2 item°""", 
            """   allows players to corrupt°""", 
            """  all of their Tougher Times?°""", 
            """°""", 
            """°""", 
        ],
        """Safer Spaces°°""", 
        """Plasma Shrimp°°""", 
        """Needletick°°""", 
    ),
]

trivia_easy_sonic_adventure_2_battle = [
]

trivia_easy_super_mario_64 = [
    TriviaQuestion(
        [
            """°""", 
            """     In Super Mario 64, how°""", 
            """  many stars are required for°""", 
            """    the first MIPS to spawn?°""", 
            """°""", 
            """°""", 
        ],
        """15°°""", 
        """16°°""", 
        """20°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In Super Mario 64, when°""", 
            """    you dive near a penguin,°""", 
            """         the penguin...°""", 
            """°""", 
            """°""", 
        ],
        """Dives°°""", 
        """Does nothing°°""", 
        """Walks away°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """      In SM64, the 1-Up at°""", 
            """   the top of the flagpole in°""", 
            """    Whomp's Fortress will...°""", 
            """°""", 
            """°""", 
        ],
        """Follow you°°""", 
        """Drop down°°""", 
        """Float°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In SM64, how many times°""", 
            """   do you have to throw King°""", 
            """     Bob-Omb to defeat him?°""", 
            """°""", 
            """°""", 
        ],
        """3°°""", 
        """4°°""", 
        """5°°""", 
    ),
]

trivia_easy_super_mario_world = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  How many exits are there in°""", 
            """       Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """96°°""", 
        """100°°""", 
        """92°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  How many 3-Up Moons exist in°""", 
            """       Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """7°°""", 
        """6°°""", 
        """8°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Super Mario World, which°""", 
            """    of the following levels°""", 
            """   doesn't have a Magikoopa?°""", 
            """°""", 
            """°""", 
        ],
        """Iggy's Castle°°""", 
        """Larry's Castle°°""", 
        """Lemmy's Castle°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Super Mario World, what's°""", 
            """  the message built with coins°""", 
            """      at the end of Funky?°""", 
            """°""", 
            """°""", 
        ],
        """YOU ARE A SUPER PLAYER!!°°""", 
        """YOU ARE SUPER PLAYER!!°°""", 
        """YOU IS A SUPER PLAYER!!°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Super Mario World, how°""", 
            """ many coin arrows are there in°""", 
            """       Vanilla Secret 3?°""", 
            """°""", 
            """°""", 
        ],
        """5°°""", 
        """3°°""", 
        """4°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Super Mario World, what°""", 
            """     causes Pokeys to have°""", 
            """    5 segments instead of 3?°""", 
            """°""", 
            """°""", 
        ],
        """Riding a Yoshi°°""", 
        """Having a Fire Flower°°""", 
        """A P-Switch is active°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    What's the color of the°""", 
            """     Switch Palace located°""", 
            """   inside Forest of Illusion°""", 
            """     in Super Mario World?°""", 
            """°""", 
        ],
        """Blue°°""", 
        """Green°°""", 
        """Red°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    What's the color of the°""", 
            """     Switch Palace located°""", 
            """      inside Vanilla Dome°""", 
            """     in Super Mario World?°""", 
            """°""", 
        ],
        """Red°°""", 
        """Blue°°""", 
        """Yellow°°""", 
    ),
]

trivia_easy_super_metroid = [
    TriviaQuestion(
        [
            """°""", 
            """    In Super Metroid, which°""", 
            """   of these beam combinations°""", 
            """        is not possible?°""", 
            """°""", 
            """°""", 
        ],
        """Spazer + Plasma°°""", 
        """Ice + Plasma°°""", 
        """Wave + Plasma°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """       In Super Metroid,°""", 
            """     what item allows Samus°""", 
            """    to move freely in water?°""", 
            """°""", 
            """°""", 
        ],
        """Gravity Suit°°""", 
        """Wet Suit°°""", 
        """Diving Suit°°""", 
    ),
]

trivia_easy_symphony_of_the_night = [
    TriviaQuestion(
        [
            """°""", 
            """   In Symphony of the Night,°""", 
            """       what does the item°""", 
            """       "Secret Boots" do?°""", 
            """°""", 
            """°""", 
        ],
        """Makes Alucard taller°°""", 
        """Nothing°°""", 
        """Reveals breakable walls°°""", 
    ),
]

trivia_easy_terraria = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ In Terraria, what is the color°""", 
            """      of Retinazer pupil?°""", 
            """°""", 
            """°""", 
        ],
        """Red°°""", 
        """Green°°""", 
        """Blue°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ In Terraria, what is the color°""", 
            """      of Spazmatism pupil?°""", 
            """°""", 
            """°""", 
        ],
        """Green°°""", 
        """Red°°""", 
        """Blue°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Terraria, which boss has°""", 
            """      the spawn message of°""", 
            """   "The air is getting colder°""", 
            """        around you..."?°""", 
            """°""", 
        ],
        """Skeletron Prime°°""", 
        """The Destroyer°°""", 
        """The Twins°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Terraria, which boss has°""", 
            """      the spawn message of°""", 
            """     "This is going to be a°""", 
            """      terrible night..."?°""", 
            """°""", 
        ],
        """The Twins°°""", 
        """Skeletron Prime°°""", 
        """The Destroyer°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In Terraria, what is the°""", 
            """  name of the soul that drops°""", 
            """         The Destroyer?°""", 
            """°""", 
            """°""", 
        ],
        """Soul of Might°°""", 
        """Soul of Fright°°""", 
        """Soul of Sight°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In Terraria, what is the°""", 
            """  name of the soul that drops°""", 
            """        Skeletron Prime?°""", 
            """°""", 
            """°""", 
        ],
        """Soul of Fright°°""", 
        """Soul of Might°°""", 
        """Soul of Sight°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In Terraria, what is the°""", 
            """  name of the soul that drops°""", 
            """           The Twins?°""", 
            """°""", 
            """°""", 
        ],
        """Soul of Sight°°""", 
        """Soul of Fright°°""", 
        """Soul of Might°°""", 
    ),
]

trivia_easy_the_legend_of_zelda = [
]

trivia_easy_vvvvvv = [
    TriviaQuestion(
        [
            """°""", 
            """      Which of these songs°""", 
            """       from VVVVVV has a°""", 
            """         voice sample?°""", 
            """°""", 
            """°""", 
        ],
        """Pressure Cooker°°""", 
        """Passion for Exploring°°""", 
        """Potential for Anything°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    What is the name of the°""", 
            """    collectibles in VVVVVV?°""", 
            """°""", 
            """°""", 
        ],
        """Trinkets°°""", 
        """Artifacts°°""", 
        """Orbs°°""", 
    ),
]

trivia_easy_yoshis_island = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """      What is the name of°""", 
            """   the dog in Yoshi's Island?°""", 
            """°""", 
            """°""", 
        ],
        """Poochy°°""", 
        """Kevin°°""", 
        """Richard°°""", 
    ),
]

trivia_hard_a_link_to_the_past = [
    TriviaQuestion(
        [
            """°""", 
            """ In A Link to the Past, in the°""", 
            """    official manual, what is°""", 
            """      Ganondorf last name?°""", 
            """°""", 
            """°""", 
        ],
        """Dragmire°°""", 
        """Mandrag°°""", 
        """Dorf°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In A Link to the Past, which°""", 
            """    of the following is the°""", 
            """         correct name?°""", 
            """°""", 
            """°""", 
        ],
        """Sahasrahla°°""", 
        """Sahasarhla°°""", 
        """Sahasrala°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  When you can find the Super°""", 
            """  Bomb in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """After completing°        Ice Palace & Misery Mire°""", 
        """After visting the°        Cursed Fairy°""", 
        """After Rescuing Zelda°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  Where is the Magic Mushroom°""", 
            """      located at in ALTTP?°""", 
            """°""", 
            """°""", 
        ],
        """In a damp, misty glen°        in the Lost Woods°""", 
        """In a open, rainy glen°        in the Lost Woods°""", 
        """In a dry, rocky glen°        in the Lost Woods°""", 
    ),
]

trivia_hard_actraiser = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """In ActRaiser, how many pedestals°""", 
            """   can be found in the game?°""", 
            """°""", 
            """°""", 
        ],
        """68°°""", 
        """75°°""", 
        """59°°""", 
    ),
]

trivia_hard_astalon = [
]

trivia_hard_castlevania_circle_of_the_moon = [
    TriviaQuestion(
        [
            """        In Castlevania:°""", 
            """      Circle of the Moon,°""", 
            """    which DSS cards are used°""", 
            """   to replicate the effect of°""", 
            """     the Sherman Ring from°""", 
            """        Aria of Sorrow?°""", 
        ],
        """Venus & Cockatrice°°""", 
        """Pluto & Mandragora°°""", 
        """AoS doesn't have cards°°""", 
    ),
]

trivia_hard_cave_story = [
    TriviaQuestion(
        [
            """°""", 
            """    On which Cave Story area°""", 
            """       is it possible to°""", 
            """        find Monster X?°""", 
            """°""", 
            """°""", 
        ],
        """Labyrinth W°°""", 
        """Labyrinth I°°""", 
        """Labyrinth M°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ How many mimigas can be found°""", 
            """     at Sand Zone Residence°""", 
            """         in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """4°°""", 
        """3°°""", 
        """5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which event is required to°""", 
            """   happen in order to pick up°""", 
            """    Mr. Little at Cementery°""", 
            """         in Cave Story?°""", 
            """°""", 
        ],
        """Speak to Mrs. Little°°""", 
        """Reach Plantation°°""", 
        """Defeat Ma Pignon°°""", 
    ),
    TriviaQuestion(
        [
            """ What's the name of the mimiga°""", 
            """    that spawns hearts when°""", 
            """     talking to them after°""", 
            """    defeating the Doctor in°""", 
            """     Balcony in Cave Story?°""", 
            """°""", 
        ],
        """Chaco°°""", 
        """Chie°°""", 
        """Santa°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     What's the name of the°""", 
            """    unique creature found at°""", 
            """    Reservoir in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """Chinfish°°""", 
        """Midorin°°""", 
        """Porcupine Fish°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ Who caused Ballos to be driven°""", 
            """  into insanity in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """The king°°""", 
        """The doctor°°""", 
        """His sister°°""", 
    ),
]

trivia_hard_diddy_kong_racing = [
    TriviaQuestion(
        [
            """°""", 
            """  Which cheat code makes every°""", 
            """       balloon be yellow°""", 
            """     in Diddy Kong Racing?°""", 
            """°""", 
            """°""", 
        ],
        """BODYARMOR°°""", 
        """NOYELLOWSTUFF°°""", 
        """ROCKETFUEL°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Where's the Wish Key in°""", 
            """       Boulder Canyon in°""", 
            """       Diddy Kong Racing?°""", 
            """°""", 
            """°""", 
        ],
        """In a hidden alcove°°""", 
        """Behind a waterfall°°""", 
        """Underwater°°""", 
    ),
]

trivia_hard_donkey_kong_country_2 = [
    TriviaQuestion(
        [
            """°""", 
            """ In K. Rool Duel, how many oil°""", 
            """   barrels can you see in the°""", 
            """          background?°""", 
            """°""", 
            """°""", 
        ],
        """8°°""", 
        """7°°""", 
        """9°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ In K. Rool Duel, what numbers°""", 
            """   can be seen on the dice in°""", 
            """          the cockpit?°""", 
            """°""", 
            """°""", 
        ],
        """A pair of 2°°""", 
        """6 and 4°°""", 
        """3 and 5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """In K. Rool Duel, which of these°""", 
            """  is NOT a background object?°""", 
            """°""", 
            """°""", 
        ],
        """4 Giant Bananas°°""", 
        """A black tire°°""", 
        """A SNES controller°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Monkey Museum, how much°""", 
            """ does a terrarium of winky the°""", 
            """           frog cost?°""", 
            """°""", 
            """°""", 
        ],
        """$5=°°""", 
        """$2=°°""", 
        """$3=°°""", 
    ),
]

trivia_hard_donkey_kong_country_3 = [
    TriviaQuestion(
        [
            """     Which of the following°""", 
            """  conditions are required for°""", 
            """   Flupperius Petallus Pongus°""", 
            """    to fully bloom in Donkey°""", 
            """     Kong Country 3's map?°""", 
            """°""", 
        ],
        """Clear Razor Ridge°°""", 
        """Give Bramble a flower°°""", 
        """Defeat KAOS at Mekanos°°""", 
    ),
]

trivia_hard_earthbound = [
]

trivia_hard_final_fantasy_mystic_quest = [
    TriviaQuestion(
        [
            """°""", 
            """       In Final Fantasy:°""", 
            """   Mystic Quest, what is the°""", 
            """   damage formula for bombs?°""", 
            """°""", 
            """°""", 
        ],
        """WATK*2.25/Count-MonDEF°°""", 
        """WATK*2.5-MonDEF°°""", 
        """WATK*2.5/Count-MonDEF°°""", 
    ),
]

trivia_hard_hollow_knight = [
    TriviaQuestion(
        [
            """°""", 
            """ In Hollow Knight, how much Geo°""", 
            """ do you need to be able to buy°""", 
            """    all unbreakable charms?°""", 
            """°""", 
            """°""", 
        ],
        """37,286 geo°°""", 
        """36,886 geo°°""", 
        """36,000 geo°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Hollow Knight, which of°""", 
            """    these is NOT a title for°""", 
            """       Grey Prince Zote?°""", 
            """°""", 
            """°""", 
        ],
        """Courageous°°""", 
        """Sensual°°""", 
        """Vigorous°°""", 
    ),
]

trivia_hard_kingdom_hearts = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  What does Sora says to Riku°""", 
            """  while on Hook's Pirate Ship°""", 
            """°""", 
            """°""", 
        ],
        """You're Stupid!°°""", 
        """I Implore to Reconsider!°°""", 
        """I'm sorry Riku!°°""", 
    ),
]

trivia_hard_kingdom_hearts_2 = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """In the hit game Kingdom Hearts 2°""", 
            """    What does DTD stand for?°""", 
            """°""", 
            """°""", 
        ],
        """Door to Darkness°°""", 
        """Darkness to Doors°°""", 
        """Darkness to Darkness°°""", 
    ),
]

trivia_hard_kirby_64_the_crystal_shards = [
    TriviaQuestion(
        [
            """°""", 
            """  What's the name of the boss°""", 
            """  at the end of Shiver Star's°""", 
            """   second stage in Kirby 64?°""", 
            """°""", 
            """°""", 
        ],
        """Big Mopoo°°""", 
        """HR-H°°""", 
        """Big Chilly°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     Which of the following°""", 
            """  Aqua Star stages in Kirby 64°""", 
            """   doesn't require any powers°""", 
            """ to collect its crystal shards?°""", 
            """°""", 
        ],
        """Stage 4°°""", 
        """Stage 2°°""", 
        """Stage 3°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ How many different food items°""", 
            """ can be produced via Ice-Spark°""", 
            """          in Kirby 64?°""", 
            """°""", 
            """°""", 
        ],
        """8°°""", 
        """5°°""", 
        """10°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of the following food°""", 
            """ items can't be found outdoors°""", 
            """          in Kirby 64?°""", 
            """°""", 
            """°""", 
        ],
        """Flan°°""", 
        """Cake°°""", 
        """Ice cream bar°°""", 
    ),
]

trivia_hard_kirbys_dream_land_3 = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   What animal species Pon is°""", 
            """    in Kirby's Dream Land 3?°""", 
            """°""", 
            """°""", 
        ],
        """Tanuki°°""", 
        """Cat°°""", 
        """Kitsune°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which enemy in Kirby's Dream°""", 
            """    Land 3 can hold as many°""", 
            """   different weapons as there°""", 
            """     are powers for Kirby?°""", 
            """°""", 
        ],
        """Bukiset°°""", 
        """Galbo°°""", 
        """Tick°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In some Kirby's Dream Land 3°""", 
            """    levels you can find some°""", 
            """     Waddlee Dees riding...°""", 
            """°""", 
            """°""", 
        ],
        """A Nruff°°""", 
        """A parasol°°""", 
        """A Bobo°°""", 
    ),
]

trivia_hard_majoras_mask_recompiled = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   How do you obtain Romani's°""", 
            """     Mask in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """Protect Cremia's wagon°        from the Gorman brothers°""", 
        """Help Romani defend the°        ranch°""", 
        """Talking to Guru-Guru°        in the Laundry Pool°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    How do you obtain Garo's°""", 
            """     Mask in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """Win a horse race in the°        Gorman Track°""", 
        """Giving a Red Potion to°        Shiro in Ikana Canyon°""", 
        """Finishing first at the°        Goron race°""", 
    ),
]

trivia_hard_math = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    Which is the last prime°""", 
            """      number before 1000?°""", 
            """°""", 
            """°""", 
        ],
        """997°°""", 
        """999°°""", 
        """987°°""", 
    ),
]

trivia_hard_mega_man_2 = [
    TriviaQuestion(
        [
            """°""", 
            """   What is the number of Yoku°""", 
            """   Blocks in Heat Man's stage°""", 
            """         in Mega Man 2?°""", 
            """°""", 
            """°""", 
        ],
        """36°°""", 
        """32°°""", 
        """28°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In total, How many bosses°""", 
            """    (rematches included) are°""", 
            """         in Mega Man 2?°""", 
            """°""", 
            """°""", 
        ],
        """22°°""", 
        """14°°""", 
        """8°°""", 
    ),
]

trivia_hard_mega_man_3 = [
    TriviaQuestion(
        [
            """°""", 
            """  In Mega Man 3, What computer°""", 
            """      brand does Dr. Light°""", 
            """        have in his lab?°""", 
            """°""", 
            """°""", 
        ],
        """IBM°°""", 
        """IGN°°""", 
        """MAC°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   What is the serial number°""", 
            """    of Blues in Mega Man 3?°""", 
            """°""", 
            """°""", 
        ],
        """DLN. 000°°""", 
        """DRN. 001°°""", 
        """DWN. 001°°""", 
    ),
]

trivia_hard_mega_man_x = [
    TriviaQuestion(
        [
            """°""", 
            """ What's the name of the sorting°""", 
            """   method used for Bospider's°""", 
            """    movement in Mega Man X?°""", 
            """°""", 
            """°""", 
        ],
        """Ghost Leg°°""", 
        """Drawing Straws°°""", 
        """Rock-Paper-Scissors°°""", 
    ),
]

trivia_hard_mega_man_x2 = [
    TriviaQuestion(
        [
            """°""", 
            """ Which of the following colors°""", 
            """    is the strongest form of°""", 
            """     Raider Killer in MMX2?°""", 
            """°""", 
            """°""", 
        ],
        """Purple°°""", 
        """Red°°""", 
        """Blue°°""", 
    ),
]

trivia_hard_mega_man_x3 = [
    TriviaQuestion(
        [
            """°""", 
            """   What song is very similar°""", 
            """  to Neon Tiger's Stage Theme°""", 
            """        in Mega Man X3?°""", 
            """°""", 
            """°""", 
        ],
        """My Michelle°°""", 
        """November Rain°°""", 
        """Who cares°°""", 
    ),
]

trivia_hard_ocarina_of_time = [
    TriviaQuestion(
        [
            """°""", 
            """   Which reward is granted by°""", 
            """     scoring 1500 points in°""", 
            """      Horseback Archery in°""", 
            """        Ocarina of Time?°""", 
            """°""", 
        ],
        """A quiver upgrade°°""", 
        """A piece of heart°°""", 
        """Ice Arrows°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    How many nighttime Gold°""", 
            """    Skulltulas can be found°""", 
            """      at Lon Lon Ranch in°""", 
            """        Ocarina of Time?°""", 
            """°""", 
        ],
        """3°°""", 
        """4°°""", 
        """5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   What's the name of the owl°""", 
            """   found in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Kaepora Gaebora°°""", 
        """Kapoeira Gapora°°""", 
        """Gaepora Keapora°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    How do you get the Happy°""", 
            """      Mask Shop to open in°""", 
            """        Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Speaking to a gatekeeper°        in DMT in Kakariko°""", 
        """Finding the salesman in°        Goron City°""", 
        """Entering the shop at°        night°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In which dungeon players°""", 
            """    can find a Green Bubble°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Spirit Temple°°""", 
        """Fire Temple°°""", 
        """Dodongo's Cavern°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  How many boxes can be found°""", 
            """      at Haunted Wasteland°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """5°°""", 
        """6°°""", 
        """4°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    What's one of the prizes°""", 
            """     players can receive at°""", 
            """     Bombchu Bowling Alley°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
        ],
        """A purple rupee°°""", 
        """A deku seed bag upgrade°°""", 
        """An empty bottle°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ How can players break beehives°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """With a Bombchu°°""", 
        """With the Megaton Hammer°°""", 
        """With a rock°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ How can players force Business°""", 
            """   Scrubs out of their holes°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """By using the Megaton°        Hammer°""", 
        """By throwing a rock at°        them°""", 
        """With a charged spin°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Where you can fin the Business°""", 
            """    Scrub that sells a Piece°""", 
            """      of Heart to players°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
        ],
        """Hyrule Field°°""", 
        """Sacred Forest Meadow°°""", 
        """Lost Woods°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """Where you can find the Business°""", 
            """  Scrub that sells a Deku Nut°""", 
            """  capacity upgrade to players°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
        ],
        """Sacred Forest Meadow°°""", 
        """Lost Woods°°""", 
        """Hyrule Fied°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   How can players stop Blade°""", 
            """   Traps in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """With an Ice arrow°°""", 
        """With a bomb°°""", 
        """With Din's Fire°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ In Ocarina of Time, where can°""", 
            """       Dinolfos be found?°""", 
            """°""", 
            """°""", 
        ],
        """Gerudo Training Ground°°""", 
        """Fire Temple°°""", 
        """Dodongo's Cavern°°""", 
    ),
]

trivia_hard_overcooked_2 = [
]

trivia_hard_paper_mario = [
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, which of°""", 
            """  the following badges you can°""", 
            """ NOT buy in Rowf's badge shop?°""", 
            """°""", 
            """°""", 
        ],
        """I Spy°°""", 
        """All or Nothing°°""", 
        """Mega Quake°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Paper Mario 64, what is°""", 
            """      the name of Sushie's°""", 
            """           daughter?°""", 
            """°""", 
            """°""", 
        ],
        """Sashimie°°""", 
        """Namerie°°""", 
        """Tammy Tuna°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, how many°""", 
            """      letters do you help°""", 
            """       Parakarry deliver?°""", 
            """°""", 
            """°""", 
        ],
        """25°°""", 
        """10°°""", 
        """12°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, which of°""", 
            """ the following is NOT a status°""", 
            """    effect you can get after°""", 
            """     eating a Strange Cake?°""", 
            """°""", 
        ],
        """Paralyzed°°""", 
        """Electrified°°""", 
        """Sleepy°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ In Paper Mario 64, in Merlow's°""", 
            """    badge shop, which of the°""", 
            """  following is more expensive°""", 
            """            to buy?°""", 
            """°""", 
        ],
        """Money Money°°""", 
        """Peekaboo°°""", 
        """Zap Tap°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, which of°""", 
            """  the following items restore°""", 
            """            more HP?°""", 
            """°""", 
            """°""", 
        ],
        """Yoshi Cookie°°""", 
        """Koopasta°°""", 
        """Jelly Super°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, which of°""", 
            """  the following items restores°""", 
            """            more HP?°""", 
            """°""", 
            """°""", 
        ],
        """Frozen Fries°°""", 
        """Potato Salad°°""", 
        """Spicy Soup°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, which of°""", 
            """  the following items restore°""", 
            """            more FP?°""", 
            """°""", 
            """°""", 
        ],
        """Coco Pop°°""", 
        """Bubble Berry°°""", 
        """Nutty Cake°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, which of°""", 
            """  the following items restore°""", 
            """            more FP?°""", 
            """°""", 
            """°""", 
        ],
        """Healthy Juice°°""", 
        """Shroom Cake°°""", 
        """Lime Candy°°""", 
    ),
]

trivia_hard_pokemon_crystal = [
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, in which°""", 
            """ of these locations can you NOT°""", 
            """      find a Week Sibling?°""", 
            """°""", 
            """°""", 
        ],
        """Route 34°°""", 
        """Route 29°°""", 
        """Route 32°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In Pokemon Crystal, who°""", 
            """     of these people is NOT°""", 
            """        a Radio Host DJ?°""", 
            """°""", 
            """°""", 
        ],
        """Tom°°""", 
        """Reed°°""", 
        """Ben°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """In Pokemon Crystal, which of these°""", 
            """  items is NOT a prize in the°""", 
            """     Bug-Catching Contest?°""", 
            """°""", 
            """°""", 
        ],
        """Moon Stone°°""", 
        """Sun Stone°°""", 
        """Everstone°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Pokemon Crystal, how many°""", 
            """ aides are there in Oak's Lab?°""", 
            """°""", 
            """°""", 
        ],
        """3°°""", 
        """2°°""", 
        """1°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, how many°""", 
            """  breakable rocks are there in°""", 
            """         Cianwood City?°""", 
            """°""", 
            """°""", 
        ],
        """6°°""", 
        """4°°""", 
        """2°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, how many°""", 
            """  breakable rocks are there in°""", 
            """           Route 40?°""", 
            """°""", 
            """°""", 
        ],
        """3°°""", 
        """4°°""", 
        """2°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, how many°""", 
            """  breakable rocks are there in°""", 
            """           Dark Cave?°""", 
            """°""", 
            """°""", 
        ],
        """4°°""", 
        """3°°""", 
        """2°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, how many°""", 
            """   boulders are there in the°""", 
            """        Blackthorn Gym?°""", 
            """°""", 
            """°""", 
        ],
        """6°°""", 
        """4°°""", 
        """8°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, which of°""", 
            """  the Johto Gym Guides is NOT°""", 
            """   inside his respective Gym?°""", 
            """°""", 
            """°""", 
        ],
        """Cianwood Gym Guide°°""", 
        """Azalea Gym Guide°°""", 
        """Olivine Gym Guide°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, how many°""", 
            """  cuttable trees are there in°""", 
            """         Lake of Rage?°""", 
            """°""", 
            """°""", 
        ],
        """5°°""", 
        """4°°""", 
        """6°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, how many°""", 
            """    berry trees are there in°""", 
            """           Route 42?°""", 
            """°""", 
            """°""", 
        ],
        """3°°""", 
        """2°°""", 
        """1°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, what is°""", 
            """the color of the pokemon machine°""", 
            """      in the Hall of Fame?°""", 
            """°""", 
            """°""", 
        ],
        """Blue°°""", 
        """Gray°°""", 
        """Red°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, how many°""", 
            """  phone numbers can you store°""", 
            """        in the Pokegear?°""", 
            """°""", 
            """°""", 
        ],
        """10°°""", 
        """15°°""", 
        """5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, which of°""", 
            """ these places is NOT located in°""", 
            """          Violet City?°""", 
            """°""", 
            """°""", 
        ],
        """Poke Seer°°""", 
        """Pokemon Academy°°""", 
        """Sprout Tower°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, how much°""", 
            """money do the Rocket Grunts steal°""", 
            """ from you in the Route 43 gate?°""", 
            """°""", 
            """°""", 
        ],
        """$1000°°""", 
        """$2000°°""", 
        """$500°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """    of these Trainer Classes°""", 
            """    can you NOT find in the°""", 
            """         Dragon's Den?°""", 
            """°""", 
        ],
        """PokeManiac°°""", 
        """Twins°°""", 
        """Cooltrainer°°""", 
    ),
]

trivia_hard_pokemon_emerald = [
]

trivia_hard_pokemon_red_and_blue = [
]

trivia_hard_rabiribi = [
]

trivia_hard_risk_of_rain_2 = [
]

trivia_hard_sonic_adventure_2_battle = [
    TriviaQuestion(
        [
            """     In Sonic Adventure 2,°""", 
            """       what is guaranteed°""", 
            """     to grant you a Perfect°""", 
            """      Bonus and an A-Rank°""", 
            """     at the end of a stage?°""", 
            """°""", 
        ],
        """Holding all the rings°°""", 
        """Getting all animals°°""", 
        """Getting a low time°°""", 
    ),
]

trivia_hard_super_mario_64 = [
    TriviaQuestion(
        [
            """°""", 
            """  In Super Mario 64, how many°""", 
            """ balusters (pegs) are there in°""", 
            """  the lobby of Peach's Castle?°""", 
            """°""", 
            """°""", 
        ],
        """120°°""", 
        """100°°""", 
        """128°°""", 
    ),
]

trivia_hard_super_mario_world = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    What is the serial code°""", 
            """    of the US SMW cartridge?°""", 
            """°""", 
            """°""", 
        ],
        """SNS-MW-USA°°""", 
        """SNSN-MW-USA°°""", 
        """SHVC-MW-USA°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which of the following levels°""", 
            """   in Super Mario World has a°""", 
            """    Powerup Roulette inside?°""", 
            """°""", 
            """°""", 
        ],
        """Forest of Illusion 1°°""", 
        """Vanilla Dome 3°°""", 
        """Forest of Illusion 3°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of the following Super°""", 
            """   Mario World levels has two°""", 
            """      sets of Hidden 1-Up?°""", 
            """°""", 
            """°""", 
        ],
        """Valley of Bowser 2°°""", 
        """Yoshi's Island 4°°""", 
        """Donut Plains 4°°""", 
    ),
    TriviaQuestion(
        [
            """    What's the minimal item°""", 
            """     requirement in Vanilla°""", 
            """    Dome 1's Normal Exit in°""", 
            """       Super Mario World?°""", 
            """    Account for out of logic°""", 
            """      situations as well.°""", 
        ],
        """Nothing°°""", 
        """Run + Super Star°°""", 
        """1 Progressive Powerup°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    How many Mega Moles are°""", 
            """  there in Valley of Bowser 1°""", 
            """     in Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """20°°""", 
        """16°°""", 
        """24°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     In Super Mario World,°""", 
            """     which of the following°""", 
            """      levels doesn't have°""", 
            """        Munchers in it?°""", 
            """°""", 
        ],
        """Valley of Bowser 3°°""", 
        """Chocolate Secret°°""", 
        """Valley of Bowser 1°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  What causes Hammer Bros. to°""", 
            """   launch hammers more often°""", 
            """     in Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """Being in a submap°°""", 
        """Riding a Yoshi°°""", 
        """Having a powerup°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   What happens when you face°""", 
            """    Bowser at his castle and°""", 
            """ don't have enough Boss Tokens°""", 
            """    in Super Mario World AP?°""", 
            """°""", 
        ],
        """Keeps dropping balls°°""", 
        """Stomps Mario°°""", 
        """Goes away°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which Yoshi color can be found°""", 
            """       at Star World 1 in°""", 
            """       Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """Red°°""", 
        """Green°°""", 
        """Yellow°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Super Mario World, which°""", 
            """  doors at Valley Ghost House°""", 
            """      allows you to reach°""", 
            """        the Normal Exit?°""", 
            """°""", 
        ],
        """Third and Fourth°°""", 
        """Fourth and Fifth°°""", 
        """First and Third°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ What can be found at the very°""", 
            """    end of Sunken Ghost Ship°""", 
            """     in Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """Three 1-Up mushrooms°°""", 
        """Several spike balls°°""", 
        """A goal sphere°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     Which of the following°""", 
            """     castles doesn't have a°""", 
            """   freestanding red mushroom°""", 
            """     in Super Mario World?°""", 
            """°""", 
        ],
        """Roy's Castle°°""", 
        """Larry's Castle°°""", 
        """Ludwig's Castle°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of the following items°""", 
            """ are the bare minimum to obtain°""", 
            """ Chocolate Island 2 normal exit°""", 
            """     in Super Mario World?°""", 
            """°""", 
        ],
        """Nothing°°""", 
        """P-Switch°°""", 
        """Run + Red Switch Palace°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of the following items°""", 
            """ are the bare minimum to obtain°""", 
            """   Iggy's Castle normal exit°""", 
            """     in Super Mario World?°""", 
            """°""", 
        ],
        """Climb°°""", 
        """P-Switch°°""", 
        """Climb + P-Switch°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which of the following levels°""", 
            """    doesn't feature Skewers°""", 
            """     in Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """Forest Fortress°°""", 
        """Valley Fortress°°""", 
        """Wendy's Castle°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    How many 1-Ups from 1-Up°""", 
            """   Mushrooms are possible to°""", 
            """      collect in Gnarly in°""", 
            """       Super Mario World?°""", 
            """°""", 
        ],
        """6°°""", 
        """2°°""", 
        """4°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which Super Mario World°""", 
            """     level has Blue Switch°""", 
            """         Palace blocks?°""", 
            """°""", 
            """°""", 
        ],
        """Valley of Bowser 4°°""", 
        """Forest of Illusion 2°°""", 
        """Vanilla Secret 2°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which Super Mario World°""", 
            """     level doesn't have Red°""", 
            """     Switch Palace blocks?°""", 
            """°""", 
            """°""", 
        ],
        """Chocolate Island 5°°""", 
        """Wendy's Castle°°""", 
        """Chocolate Fortress°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ Which Super Mario World castle°""", 
            """ doesn't have automatic stairs?°""", 
            """°""", 
            """°""", 
        ],
        """Lemmy's Castle°°""", 
        """Larry's Castle°°""", 
        """Ludwig's Castle°°""", 
    ),
]

trivia_hard_super_metroid = [
    TriviaQuestion(
        [
            """°""", 
            """    What Super Metroid item°""", 
            """    is in the room you enter°""", 
            """    after defeating Ridley?°""", 
            """°""", 
            """°""", 
        ],
        """Energy Tank°°""", 
        """Power Bombs°°""", 
        """Screw Attack°°""", 
    ),
]

trivia_hard_symphony_of_the_night = [
    TriviaQuestion(
        [
            """   In Symphony of the Night,°""", 
            """ what is the name of the enemy°""", 
            """  that can only be encountered°""", 
            """    once in the entire game,°""", 
            """       excluding bosses?°""", 
            """°""", 
        ],
        """Mudman°°""", 
        """Yorick°°""", 
        """Dodo Bird°°""", 
    ),
    TriviaQuestion(
        [
            """     Which bible verse does°""", 
            """  Dracula quote in the ending°""", 
            """        to Castlevania:°""", 
            """  Symphony of the Night in the°""", 
            """       original release?°""", 
            """°""", 
        ],
        """Matthew 16:26°°""", 
        """Matthew 9:5°°""", 
        """Solomon 2:9°°""", 
    ),
]

trivia_hard_terraria = [
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """   following is NOT a debuff°""", 
            """            candle?°""", 
            """°""", 
            """°""", 
        ],
        """Peace Candle°°""", 
        """Shadow Candle°°""", 
        """Water Candle°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In Terraria, what is the°""", 
            """    drop rate of the Rod of°""", 
            """            Discord?°""", 
            """°""", 
            """°""", 
        ],
        """1/500°°""", 
        """1/600°°""", 
        """1/300°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    In Terraria, what is the°""", 
            """  drop rate of any Biome Key?°""", 
            """°""", 
            """°""", 
        ],
        """1/2500°°""", 
        """1/3000°°""", 
        """1/2000°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """      following Yoyos has°""", 
            """       highest drop rate?°""", 
            """°""", 
            """°""", 
        ],
        """Yelets°°""", 
        """Cascade°°""", 
        """Kraken°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """    following items is NOT a°""", 
            """       Rarity Tier Lime?°""", 
            """°""", 
            """°""", 
        ],
        """Nail Gun°°""", 
        """Black Belt°°""", 
        """Rod of Discord°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """    following items is NOT a°""", 
            """       Rarity Tier Cyan?°""", 
            """°""", 
            """°""", 
        ],
        """Heat Ray°°""", 
        """0x33's Aviators°°""", 
        """Arkhalis°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """    following items is NOT a°""", 
            """       Rarity Tier Pink?°""", 
            """°""", 
            """°""", 
        ],
        """Destroyer Emblem°°""", 
        """Amphibian Boots°°""", 
        """Terraprisma°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Terraria, which enemy can°""", 
            """  cause the "Blackout" debuff?°""", 
            """°""", 
            """°""", 
        ],
        """Ragged Caster°°""", 
        """Necromancer°°""", 
        """That is not a debuff!°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """   following is NOT a debuff°""", 
            """          in the game?°""", 
            """°""", 
            """°""", 
        ],
        """Asphyxiated°°""", 
        """Withered Weapon°°""", 
        """Stoned°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """   following is NOT a debuff°""", 
            """          in the game?°""", 
            """°""", 
            """°""", 
        ],
        """Drunk°°""", 
        """Obstructed°°""", 
        """Oozed°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """   following is NOT a buff in°""", 
            """           the game?°""", 
            """°""", 
            """°""", 
        ],
        """Lovestruck°°""", 
        """Clairvoyance°°""", 
        """Strategist°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """  following is NOT a whip buff°""", 
            """      effect in the game?°""", 
            """°""", 
            """°""", 
        ],
        """Striking Moment°°""", 
        """Durendal's Blessing°°""", 
        """Harvest Time°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """ following is NOT a flask buff°""", 
            """          in the game?°""", 
            """°""", 
            """°""", 
        ],
        """Ice°°""", 
        """Nanites°°""", 
        """Confetti°°""", 
    ),
]

trivia_hard_the_legend_of_zelda = [
    TriviaQuestion(
        [
            """ What is the name of the board°""", 
            """  game based on The Legend of°""", 
            """   Zelda on the NES, wherein°""", 
            """  you move Link tokens around°""", 
            """  an overworld map lifted from°""", 
            """    the game's official art?°""", 
        ],
        """The Hyrule Fantasy°°""", 
        """The Legend of Zelda°°""", 
        """Tabletop Simulator°°""", 
    ),
]

trivia_hard_vvvvvv = [
]

trivia_hard_yoshis_island = [
]

trivia_medium_a_link_to_the_past = [
    TriviaQuestion(
        [
            """°""", 
            """  What's a valid way to remove°""", 
            """     Helmasaur King's mask°""", 
            """     in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """With bombs°°""", 
        """With the golden sword°°""", 
        """With the Cane of Somaria°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  What's the name of the boss°""", 
            """   found at the end of Swamp°""", 
            """ Palace in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """Arrghus°°""", 
        """Kholdstare°°""", 
        """Vitreous°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ Where is the Bombos medallion°""", 
            """ located in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """In a cliff in the Desert°°""", 
        """In the Lake of Ill Omen°°""", 
        """West of Tower of Hera°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  Where is the Quake medallion°""", 
            """ located in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """In the Lake of Ill Omen°°""", 
        """In a cliff in the Desert°°""", 
        """West of Tower of Hera°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  Where is the Ether medallion°""", 
            """ located in A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """West of Tower of Hera°°""", 
        """In the Lake of Ill Omen°°""", 
        """In a cliff in the Desert°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ Which medallions are required°""", 
            """  to beat A Link to the Past?°""", 
            """°""", 
            """°""", 
        ],
        """Ether & Quake°°""", 
        """Quake & Bombos°°""", 
        """Bombos & Ether°°""", 
    ),
]

trivia_medium_actraiser = [
    TriviaQuestion(
        [
            """°""", 
            """    In ActRaiser, what's the°""", 
            """      name of the boss in°""", 
            """        Northwall Act 1?°""", 
            """°""", 
            """°""", 
        ],
        """Merman Fly°°""", 
        """Flying Mermaid°°""", 
        """Mermen Flew°°""", 
    ),
]

trivia_medium_astalon = [
    TriviaQuestion(
        [
            """°""", 
            """In Astalon, how many cyclops do°""", 
            """you have to kill on Cyclops Den°""", 
            """    to open the boss' door?°""", 
            """°""", 
            """°""", 
        ],
        """35°°""", 
        """25°°""", 
        """45°°""", 
    ),
]

trivia_medium_castlevania_circle_of_the_moon = [
    TriviaQuestion(
        [
            """°""", 
            """        In Castlevania:°""", 
            """      Circle of the Moon,°""", 
            """       which enemy drops°""", 
            """       the Needle Armor?°""", 
            """°""", 
        ],
        """Nightmare°°""", 
        """Lilith°°""", 
        """Succubus°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """        In Castlevania:°""", 
            """      Circle of the Moon,°""", 
            """       what is the player°""", 
            """     character's full name?°""", 
            """°""", 
        ],
        """Nathan Graves°°""", 
        """Nathan Belmont°°""", 
        """Nathan Morris°°""", 
    ),
]

trivia_medium_cave_story = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """     How do you obtain the°""", 
            """   Alien Medal in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """No hit run vs Ironhead°°""", 
        """Defeat Ma Pignon°°""", 
        """No hit run vs Red Ogre°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which Cave Story weapons are°""", 
            """     needed to trade in for°""", 
            """      the Snake weapon at°""", 
            """      the Labyrinth Shop?°""", 
            """°""", 
        ],
        """Polar Star & Fireball°°""", 
        """Polar Star & Spur°°""", 
        """Machine Gun & Bubbler°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """     Where does Cave Story°""", 
            """          takes place?°""", 
            """°""", 
            """°""", 
        ],
        """In a floating island°°""", 
        """In an archipelago°°""", 
        """In an underground city°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     When does Chaba at the°""", 
            """     Labyrinth Shop grants°""", 
            """ the player the Whimsical Star°""", 
            """         in Cave Story?°""", 
            """°""", 
        ],
        """Own the Spur weapon°°""", 
        """After draining Curly°°""", 
        """Saved King in Sand Zone°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Cave Story, which of the°""", 
            """   following enemies can't be°""", 
            """      found in Grasstown?°""", 
            """°""", 
            """°""", 
        ],
        """Basu°°""", 
        """Mannan°°""", 
        """Puchi°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  Which was Curly and Quote's°""", 
            """ true objective in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """Destroy the Demon Crown°°""", 
        """Help the Doctor°°""", 
        """Retrieve Jenka's dogs°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   How do you gain access to°""", 
            """     Sand Zone's Warehouse°""", 
            """         in Cave Story?°""", 
            """°""", 
            """°""", 
        ],
        """Retrieving Jenka's dogs°°""", 
        """Defeating Omega°°""", 
        """Talking with Curly°°""", 
    ),
]

trivia_medium_diddy_kong_racing = [
    TriviaQuestion(
        [
            """°""", 
            """     What's the name of the°""", 
            """     boss at Sherbet Island°""", 
            """     in Diddy Kong Racing?°""", 
            """°""", 
            """°""", 
        ],
        """Bubbler°°""", 
        """Bluey°°""", 
        """Smokey°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  At Diddy Kong Racing's final°""", 
            """  race, what is Wizpig riding°""", 
            """    to challenge the racer?°""", 
            """°""", 
            """°""", 
        ],
        """A rocket°°""", 
        """Nothing°°""", 
        """A banana°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which combination of vehicles°""", 
            """  can be used at Dino Domain's°""", 
            """  races in Diddy Kong Racing's°""", 
            """        Adventure mode?°""", 
            """°""", 
        ],
        """Car & Plane°°""", 
        """Car, Hovercraft & Plane°°""", 
        """Car & Hovercraft°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which combination of vehicles°""", 
            """can be used at Sherbet Island's°""", 
            """  races in Diddy Kong Racing's°""", 
            """        Adventure mode?°""", 
            """°""", 
        ],
        """Car & Hovercraft°°""", 
        """Car, Hovercraft & Plane°°""", 
        """Hovercraft & Plane°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  How do you unlock Drumstick°""", 
            """     in Diddy Kong Racing?°""", 
            """°""", 
            """°""", 
        ],
        """Run over a rooster frog°°""", 
        """Beat several time trials°°""", 
        """Beat Wizpig 1°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   When do you receive magic°""", 
            """  codes in Diddy Kong Racing?°""", 
            """°""", 
            """°""", 
        ],
        """Beating any Wizpig°°""", 
        """Beat a time trial°°""", 
        """Finishing a trophy race°°""", 
    ),
]

trivia_medium_donkey_kong_country_2 = [
    TriviaQuestion(
        [
            """°""", 
            """   In Donkey Kong Country 2,°""", 
            """  how many times does Clapper°""", 
            """  the Seal appear in the game?°""", 
            """°""", 
            """°""", 
        ],
        """14°°""", 
        """13°°""", 
        """12°°""", 
    ),
]

trivia_medium_donkey_kong_country_3 = [
    TriviaQuestion(
        [
            """°""", 
            """  Which tool is Funky playing°""", 
            """    with at Funky's Rentals°""", 
            """     when you visit him in°""", 
            """     Donkey Kong Country 3?°""", 
            """°""", 
        ],
        """A hammer°°""", 
        """A blowtorch strainer°°""", 
        """A brushed iron°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which brother bear in Donkey°""", 
            """ Kong Country 3 asks the Kongs°""", 
            """  to deliver a present to Blue°""", 
            """      in Cotton Top Cove?°""", 
            """°""", 
        ],
        """Blizzard°°""", 
        """Boomer°°""", 
        """Brash°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     What's the name of the°""", 
            """     main villian of Donkey°""", 
            """        Kong Country 3?°""", 
            """°""", 
            """°""", 
        ],
        """Baron K. Roolenstein°°""", 
        """Kaptain K. Rool°°""", 
        """KAOS°°""", 
    ),
]

trivia_medium_earthbound = [
    TriviaQuestion(
        [
            """°""", 
            """   In EarthBound, what is the°""", 
            """  name of the monkey who wants°""", 
            """        the King Banana?°""", 
            """°""", 
            """°""", 
        ],
        """Man K. Man°°""", 
        """Talah Rama°°""", 
        """Bubble Monkey°°""", 
    ),
]

trivia_medium_final_fantasy_mystic_quest = [
    TriviaQuestion(
        [
            """°""", 
            """       In Final Fantasy:°""", 
            """     Mystic Quest, how many°""", 
            """    weapons deal Axe element°""", 
            """            damage?°""", 
            """°""", 
        ],
        """Four°°""", 
        """Three°°""", 
        """Axe isn't an element°°""", 
    ),
    TriviaQuestion(
        [
            """     In the Final Fantasy:°""", 
            """    Mystic Quest Archipelago°""", 
            """  implementation, do you need°""", 
            """  Reuben in your party to save°""", 
            """  Arion, his dad, from the end°""", 
            """          of the Mine?°""", 
        ],
        """No, just Mega Grenades°°""", 
        """Yes°°""", 
        """No, just kill Jinn°°""", 
    ),
    TriviaQuestion(
        [
            """     In the Final Fantasy:°""", 
            """    Mystic Quest Archipelago°""", 
            """    implementation, what is°""", 
            """  Kaeli's mom obsessed with if°""", 
            """  you turn on the "Kaeli's Mom°""", 
            """     Fights Minotaur" flag?°""", 
        ],
        """The Void from FF5°°""", 
        """Woodcutting°°""", 
        """Death°°""", 
    ),
]

trivia_medium_hollow_knight = [
    TriviaQuestion(
        [
            """°""", 
            """   In Hollow Knight, how many°""", 
            """       Charm Notches does°""", 
            """     Carefree Melody cost?°""", 
            """°""", 
            """°""", 
        ],
        """3°°""", 
        """2°°""", 
        """4°°""", 
    ),
    TriviaQuestion(
        [
            """ In Hollow Knight, if you have°""", 
            """    Flukenest, Glowing Womb,°""", 
            """  Shape of Unn, Spore Shroom,°""", 
            """    Weaversong and Hiveblood°""", 
            """    equipped, how many Charm°""", 
            """     Notches are you using?°""", 
        ],
        """14°°""", 
        """13°°""", 
        """Can't equip that many!°°""", 
    ),
]

trivia_medium_kingdom_hearts = [
    TriviaQuestion(
        [
            """°""", 
            """      In Kingdom Hearts 1:°""", 
            """  What is one of the required°""", 
            """   items to craft the rift to°""", 
            """     leave Destiny Islands?°""", 
            """°""", 
        ],
        """Cloth°°""", 
        """Bungee Cord°°""", 
        """Duck Tape°°""", 
    ),
]

trivia_medium_kingdom_hearts_2 = [
]

trivia_medium_kirby_64_the_crystal_shards = [
    TriviaQuestion(
        [
            """°""", 
            """  What's the name of the first°""", 
            """  enemy boss you encounter at°""", 
            """     Pop Star in Kirby 64?°""", 
            """°""", 
            """°""", 
        ],
        """Big N-Z°°""", 
        """Waddle Doo°°""", 
        """Whispy Woods°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  How many enemy ambushes are°""", 
            """  at Ripple Star's third stage°""", 
            """          in Kirby 64?°""", 
            """°""", 
            """°""", 
        ],
        """5°°""", 
        """6°°""", 
        """4°°""", 
    ),
]

trivia_medium_kirbys_dream_land_3 = [
    TriviaQuestion(
        [
            """°""", 
            """     What's the name of the°""", 
            """      Kirby-like enemy in°""", 
            """     Kirby's Dream Land 3?°""", 
            """°""", 
            """°""", 
        ],
        """Batamon°°""", 
        """Gordo°°""", 
        """KeKe°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which mid-boss grants you°""", 
            """     the needle ability in°""", 
            """     Kirby's Dreamn Land 3?°""", 
            """°""", 
            """°""", 
        ],
        """Captain Stitch°°""", 
        """Haboki°°""", 
        """Blocky°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In some Kirby's Dream Land 3°""", 
            """    levels you can find some°""", 
            """     Waddlee Dees riding...°""", 
            """°""", 
            """°""", 
        ],
        """A raft°°""", 
        """A minecart°°""", 
        """An inner tube°°""", 
    ),
]

trivia_medium_majoras_mask_recompiled = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ How's the Gibdo Mask obtained°""", 
            """       in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """Playing Song of Healing°        to Pamela's father°""", 
        """Collecting Cuccos in°        Romani Ranch°""", 
        """Give a Rock Sirloin°        to a hungry Goron°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which mask in Majora's Mask°""", 
            """ allows Link to not fall sleep°""", 
            """   during Anju's grandmother°""", 
            """            stories?°""", 
            """°""", 
        ],
        """All-Night Mask°°""", 
        """Kamaro's Mask°°""", 
        """Stone Mask°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  How do you obtain the Stone°""", 
            """     Mask in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """Giving a Red Potion to°        Shiro in Ikana Canyon°""", 
        """In a treasure chest°        inside Beneath the Well°""", 
        """Finishing first at the°        Goron race°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  How do you obtain the Bremen°""", 
            """     Mask in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """Talking to Guru-Guru°        in the Laundry Pool°""", 
        """Finishing the Anju and°        Kafei side quest°""", 
        """Giving a Red Potion to°        Shiro in Ikana Canyon°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ How do you obtain the Mask of°""", 
            """    Truth in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """Breaking the Resident's°        curse in Woodfall°""", 
        """Talking to Guru-Guru°        in the Laundry Pool°""", 
        """In a treasure chest°        inside Beneath the Well°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ How do you obtain the Mask of°""", 
            """    Scents in Majora's Mask?°""", 
            """°""", 
            """°""", 
        ],
        """From Deku Butler at the°        Deku Shrine°""", 
        """Breaking the Resident's°        curse in Woodfall°""", 
        """Talking to Kamaro in°        Termina Field°""", 
    ),
]

trivia_medium_math = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """        1+1+1+1+1+1*0=?°""", 
            """°""", 
            """°""", 
            """°""", 
        ],
        """5°°""", 
        """0°°""", 
        """6°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     What's the name of the°""", 
            """      following equation?°""", 
            """             y=mx+c°""", 
            """°""", 
            """°""", 
        ],
        """Slope-Intercept Form°°""", 
        """Circle°°""", 
        """Quadratic Equation°°""", 
    ),
]

trivia_medium_mega_man_2 = [
    TriviaQuestion(
        [
            """°""", 
            """   What is the most effective°""", 
            """    weapon against Metal Man°""", 
            """         in Mega Man 2?°""", 
            """°""", 
            """°""", 
        ],
        """Metal Blade°°""", 
        """Time Stopper°°""", 
        """Quick Boomerang°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   The Boss of the Third Wily°""", 
            """       Stage in Megaman 2°""", 
            """        is based on... ?°""", 
            """°""", 
            """°""", 
        ],
        """Guts Man°°""", 
        """Concrete Man°°""", 
        """Crash Man°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  What is the weakness of the°""", 
            """   final boss in Mega Man 2?°""", 
            """°""", 
            """°""", 
        ],
        """Bubble Lead°°""", 
        """Metal Blade°°""", 
        """Crash Bomb°°""", 
    ),
    TriviaQuestion(
        [
            """    In Mega Man 2, how many°""", 
            """  Robot Masters take more than°""", 
            """  one point of damage from the°""", 
            """    Metal Blade on Difficult°""", 
            """             mode?°""", 
            """°""", 
        ],
        """Four°°""", 
        """Two°°""", 
        """One°°""", 
    ),
]

trivia_medium_mega_man_3 = [
    TriviaQuestion(
        [
            """°""", 
            """   In Mega Man 3, which Robot°""", 
            """     Masters does Doc Robot°""", 
            """   copy in Spark Man's Stage?°""", 
            """°""", 
            """°""", 
        ],
        """Metal & Quick°°""", 
        """Metal & Air°°""", 
        """Metal & Heat°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    What is not a Rush form°""", 
            """         in Mega Man 3?°""", 
            """°""", 
            """°""", 
        ],
        """Rush Drill°°""", 
        """Rush Marine°°""", 
        """Rush Jet°°""", 
    ),
    TriviaQuestion(
        [
            """   In Mega Man 3, how can you°""", 
            """   extend the amount of time°""", 
            """  you spend on Rush Jet if you°""", 
            """  do not have access to weapon°""", 
            """        energy pickups?°""", 
            """°""", 
        ],
        """By jumping°°""", 
        """By sliding°°""", 
        """By firing your buster°°""", 
    ),
]

trivia_medium_mega_man_x = [
    TriviaQuestion(
        [
            """°""", 
            """ Which inputs should be entered°""", 
            """ in order to summon a Hadouken°""", 
            """         in Mega Man X?°""", 
            """°""", 
            """°""", 
        ],
        """236°°""", 
        """214°°""", 
        """632°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which of the following weapons°""", 
            """ can be used to deal damage to°""", 
            """   Wolf Sigma in Mega Man X?°""", 
            """°""", 
            """°""", 
        ],
        """Level 3 Charge Buster°°""", 
        """Shotgun Ice°°""", 
        """Hadouken°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of Rangda Bangda's eye°""", 
            """   colors follows the player°""", 
            """         in Mega Man X?°""", 
            """°""", 
            """°""", 
        ],
        """Blue°°""", 
        """Green°°""", 
        """Red°°""", 
    ),
]

trivia_medium_mega_man_x2 = [
    TriviaQuestion(
        [
            """°""", 
            """ Which of the following stages°""", 
            """     in Mega Man X2 doesn't°""", 
            """     feature a Ride Armor?°""", 
            """°""", 
            """°""", 
        ],
        """Desert Base°°""", 
        """Dinosaur Tank°°""", 
        """Energen Crystal°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    At minimum, what do you°""", 
            """  need to reach the Heart Tank°""", 
            """  in Crystal Snail's stage in°""", 
            """          Mega Man X2?°""", 
            """°""", 
        ],
        """Nothing°°""", 
        """Strike Chain°°""", 
        """Arms + S. Burner°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which inputs should be entered°""", 
            """      in order to perform°""", 
            """  a Shoryuken in Mega Man X2?°""", 
            """°""", 
            """°""", 
        ],
        """632°°""", 
        """214°°""", 
        """236°°""", 
    ),
    TriviaQuestion(
        [
            """ Which of the following methods°""", 
            """     is not valid to reach°""", 
            """      the Heart Tank found°""", 
            """        at Dinosaur Tank°""", 
            """        in Mega Man X2?°""", 
            """°""", 
        ],
        """Block from Crystal H.°°""", 
        """Charged S. Burner°°""", 
        """Shoryuken°°""", 
    ),
]

trivia_medium_mega_man_x3 = [
    TriviaQuestion(
        [
            """°""", 
            """   Who's the boss that can be°""", 
            """   fought at the bottom door°""", 
            """   of Dr. Doppler's Lab 1 in°""", 
            """          Mega Man X3?°""", 
            """°""", 
        ],
        """Godkarmachine O Inary°°""", 
        """Press Disposer°°""", 
        """Volt Kurageil°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    What is the name of the°""", 
            """ combined form of Bit and Byte°""", 
            """        in Mega Man X3?°""", 
            """°""", 
            """°""", 
        ],
        """Godkarmachine O'Inary°°""", 
        """Bettabyte°°""", 
        """Press Disposer°°""", 
    ),
]

trivia_medium_ocarina_of_time = [
    TriviaQuestion(
        [
            """°""", 
            """      What is the name of°""", 
            """        Mamamu Yan's dog°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Richard°°""", 
        """Kevin°°""", 
        """Poochy°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  In Ocarina of Time, what is°""", 
            """  the name of the blue Cucco?°""", 
            """°""", 
            """°""", 
        ],
        """Cojiro°°""", 
        """Kafei°°""", 
        """Pocket Cucco°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Ocarina of Time, what is°""", 
            """  the 8th item in the Trading°""", 
            """           Sequence?°""", 
            """°""", 
            """°""", 
        ],
        """Prescription°°""", 
        """Odd Mushroom°°""", 
        """Poacher's Saw°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   How do you gain access to°""", 
            """      Dodongo's Cavern in°""", 
            """        Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Blowing up a boulder°        at the entrance°""", 
        """Make a Goron eat the°        boulder at the entrance°""", 
        """Ask the Darunia to move°        the boulder°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  How can you beat Dodongo in°""", 
            """  Ocarina of Time if you don't°""", 
            """   have access to a Bomb Bag?°""", 
            """°""", 
            """°""", 
        ],
        """With Bomb Flowers°°""", 
        """With Deku Nuts°°""", 
        """With the Slingshot°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """  How do you obtain the Magic°""", 
            """   Meter in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """As a gift from the°        Great Fairy of Power°""", 
        """As a dungeon reward in°        Forest Temple°""", 
        """As a gift from Zelda°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  How can you cross the broken°""", 
            """   bridge at Gerudo Valley in°""", 
            """        Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """Jumping with Epona°°""", 
        """Floating with a Cucco°°""", 
        """With a magic plant°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  How can you cross the broken°""", 
            """   bridge at Gerudo Valley in°""", 
            """        Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """With the longshot°°""", 
        """Via Kaepora Gaebora°°""", 
        """A well timed backflip°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Ocarina of Time, which°""", 
            """  medallions are required for°""", 
            """  Kakariko Village be on fire?°""", 
            """°""", 
            """°""", 
        ],
        """Forest, Fire and Water°°""", 
        """Only Forest°°""", 
        """Forest and Fire°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    What's the prize players°""", 
            """     can receive as adults°""", 
            """      in the Fishing Pond°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
        ],
        """A golden scale°°""", 
        """A piece of heart°°""", 
        """A quiver upgrade°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    What's one of the prizes°""", 
            """     players can receive at°""", 
            """     Bombchu Bowling Alley°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
        ],
        """A Bomb Bag upgrade°°""", 
        """A golden rupee°°""", 
        """Deku nuts°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ How can players break beehives°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
            """°""", 
        ],
        """With a Boomerang°°""", 
        """With a Deku nut°°""", 
        """With a bush°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Where you can fin the Business°""", 
            """ Scrub that sells a Deku Stick°""", 
            """  capacity upgrade to players°""", 
            """      in Ocarina of Time?°""", 
            """°""", 
        ],
        """Lost Woods°°""", 
        """Sacred Forest Meadow°°""", 
        """Hyrule Field°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ In Ocarina of Time, where can°""", 
            """       Lizalfos be found?°""", 
            """°""", 
            """°""", 
        ],
        """Fire Temple°°""", 
        """Spirit Temple°°""", 
        """Forest Temple°°""", 
    ),
]

trivia_medium_overcooked_2 = [
]

trivia_medium_paper_mario = [
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, how many°""", 
            """  letters does Parakarry lost°""", 
            """    in the Mushroom Kingdom?°""", 
            """°""", 
            """°""", 
        ],
        """12°°""", 
        """10°°""", 
        """25°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In Paper Mario 64 after°""", 
            """    chapter 5, where can you°""", 
            """          get Melons?°""", 
            """°""", 
            """°""", 
        ],
        """Trading with Y. Yoshi°°""", 
        """A Specific palm tree°°""", 
        """In Yoshi's Cabana°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Paper Mario 64, how many°""", 
            """    times can you hit Whacka°""", 
            """    before they "disappear"?°""", 
            """°""", 
            """°""", 
        ],
        """8°°""", 
        """10°°""", 
        """6°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Paper Mario 64, what is°""", 
            """  the name of the place where°""", 
            """    the Star Rod was stolen?°""", 
            """°""", 
            """°""", 
        ],
        """Star Haven°°""", 
        """Shooting Star Summit°°""", 
        """Star Hill°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    In Paper Mario 64, which°""", 
            """   candy can you use to bribe°""", 
            """    the Anti Guy in the Shy°""", 
            """         Guy's Toy Box?°""", 
            """°""", 
        ],
        """Lemon Candy°°""", 
        """Lime Candy°°""", 
        """Honey Candy°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ In Paper Mario 64, who is the°""", 
            """   star spirit you rescue in°""", 
            """         Cloudy Climb?°""", 
            """°""", 
            """°""", 
        ],
        """Klevar°°""", 
        """Kalmar°°""", 
        """Mamar°°""", 
    ),
]

trivia_medium_pokemon_crystal = [
    TriviaQuestion(
        [
            """°""", 
            """    In Pokemon Crystal, what°""", 
            """    item is needed to enter°""", 
            """           Tin Tower?°""", 
            """°""", 
            """°""", 
        ],
        """Clear Bell°°""", 
        """Clear Wing°°""", 
        """Lost Bell°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ In Pokemon Crystal, how do you°""", 
            """ wake up the sleeping Snorlax?°""", 
            """°""", 
            """°""", 
        ],
        """Using the Pokegear Radio°°""", 
        """Using the PokeFlute°°""", 
        """Using the SquirtBottle°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ In Pokemon Crystal, where are°""", 
            """   the Radio Towers located?°""", 
            """°""", 
            """°""", 
        ],
        """Goldenrod and Lavender°°""", 
        """Goldenrod and Saffron°°""", 
        """Ecruteak and Olivine°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ In Pokemon Crystal, which Gym°""", 
            """ Leaders do you meet outside of°""", 
            """   their Gyms the first time?°""", 
            """°""", 
            """°""", 
        ],
        """Morty and Jasmine°°""", 
        """Morty and Clair°°""", 
        """Jasmine and Clair°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """    of these Trainer Classes°""", 
            """    can you NOT find in the°""", 
            """         National Park?°""", 
            """°""", 
        ],
        """PokeManiac°°""", 
        """Pokefan°°""", 
        """Lass°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """ legendary Pokemon can be found°""", 
            """ in the deep of Whirl Islands?°""", 
            """°""", 
            """°""", 
        ],
        """Lugia°°""", 
        """Suicune°°""", 
        """Mewtwo°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """  Trainer Classes can be found°""", 
            """       on Goldenrod Gym?°""", 
            """°""", 
            """°""", 
        ],
        """Lass and Beauty°°""", 
        """Lass and Picnicker°°""", 
        """Picnicker and Beauty°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """  Trainer Classes can be found°""", 
            """        on Ecruteak Gym?°""", 
            """°""", 
            """°""", 
        ],
        """Sage and Medium°°""", 
        """PokeManiac and Medium°°""", 
        """Sage and Channeler°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """  Trainer Classes can be found°""", 
            """         on Azalea Gym?°""", 
            """°""", 
            """°""", 
        ],
        """Bug Catcher and Twins°°""", 
        """Bug Catcher and Camper°°""", 
        """Bug Catcher and Picnicker°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Pokemon Crystal, which°""", 
            """  Trainer Classes can be found°""", 
            """        on Mahogany Gym?°""", 
            """°""", 
            """°""", 
        ],
        """Skier and Boarder°°""", 
        """Skier and Gentleman°°""", 
        """Lass and Gentleman°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, which is°""", 
            """ the only Trainer Classes found°""", 
            """         on Violet Gym?°""", 
            """°""", 
            """°""", 
        ],
        """Bird Keeper°°""", 
        """Camper°°""", 
        """Youngster°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, which is°""", 
            """  the only Trainer Class found°""", 
            """       on Blackthorn Gym?°""", 
            """°""", 
            """°""", 
        ],
        """Cooltrainer°°""", 
        """PokeManiac°°""", 
        """Gentleman°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Crystal, which is°""", 
            """  the only Trainer Class found°""", 
            """        in Cianwood Gym?°""", 
            """°""", 
            """°""", 
        ],
        """Blackbelt°°""", 
        """Sailor°°""", 
        """Cue Ball°°""", 
    ),
]

trivia_medium_pokemon_emerald = [
    TriviaQuestion(
        [
            """°""", 
            """  In Pokemon Emerald, how many°""", 
            """    fishing spots can Feebas°""", 
            """         be caught on?°""", 
            """°""", 
            """°""", 
        ],
        """Six°°""", 
        """Four°°""", 
        """Eight°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     How do you originally°""", 
            """      obtain a Jirachi in°""", 
            """        Pokemon Emerald?°""", 
            """°""", 
            """°""", 
        ],
        """Trade from R/S°°""", 
        """Reward from Birch°°""", 
        """Trade from Colosseum°°""", 
    ),
]

trivia_medium_pokemon_red_and_blue = [
]

trivia_medium_rabiribi = [
    TriviaQuestion(
        [
            """°""", 
            """ Which of the following colors°""", 
            """ is NOT present in Rabi-Ribi's°""", 
            """     Rainbow Crystal boss?°""", 
            """°""", 
            """°""", 
        ],
        """Gray°°""", 
        """Violet°°""", 
        """Yellow°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """   Which buff can't be bought°""", 
            """  from Rabi Rabi Town members?°""", 
            """°""", 
            """°""", 
        ],
        """Speed Up°°""", 
        """HP Regen°°""", 
        """Give ATK Down°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    Which buff can be bought°""", 
            """  from Rabi Rabi Town members?°""", 
            """°""", 
            """°""", 
        ],
        """Arrest°°""", 
        """Defense Boost°°""", 
        """Lucky Seven°°""", 
    ),
]

trivia_medium_risk_of_rain_2 = [
    TriviaQuestion(
        [
            """°""", 
            """   Which of Risk of Rain 2's°""", 
            """      void items corrupts°""", 
            """        Tri-Tip Daggers?°""", 
            """°""", 
            """°""", 
        ],
        """Needletick°°""", 
        """Plasma Shrimp°°""", 
        """Polylute°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which Risk of Rain 2 item°""", 
            """       allows players to°""", 
            """        ignite enemies?°""", 
            """°""", 
            """°""", 
        ],
        """Molten Perforator°°""", 
        """Ignition Tank°°""", 
        """Shattering Justice°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which Risk of Rain 2 item°""", 
            """   allows players to corrupt°""", 
            """   all of their yellow items?°""", 
            """°""", 
            """°""", 
        ],
        """Newly Hatched Zoea°°""", 
        """Lysate Cell°°""", 
        """Voidsent Flame°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   Which Risk of Rain 2 item°""", 
            """ allows players to corrupt all°""", 
            """  of their Will-o'-the wisps?°""", 
            """°""", 
            """°""", 
        ],
        """Voidsent Flame°°""", 
        """Lysate Cell°°""", 
        """Weeping Fungus°°""", 
    ),
]

trivia_medium_sonic_adventure_2_battle = [
    TriviaQuestion(
        [
            """°""", 
            """ What is the max amount of Chao°""", 
            """       allowed per garden°""", 
            """     in Sonic Adventure 2?°""", 
            """°""", 
            """°""", 
        ],
        """Eight Chao°°""", 
        """Six Chao°°""", 
        """Ten Chao°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Sonic Adventure 2, what°""", 
            """ colour do all the grind rails°""", 
            """        in space share?°""", 
            """°""", 
            """°""", 
        ],
        """Yellow°°""", 
        """Red°°""", 
        """Purple°°""", 
    ),
]

trivia_medium_super_mario_64 = [
    TriviaQuestion(
        [
            """°""", 
            """  In Super Mario 64, if Mario°""", 
            """   gets squished by an object°""", 
            """     for a long time, he...°""", 
            """°""", 
            """°""", 
        ],
        """Gets killed°°""", 
        """Gets softlocked°°""", 
        """Gets pushed through°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """    In SM64, how many coins°""", 
            """ are there in Jolly Roger Bay?°""", 
            """°""", 
            """°""", 
        ],
        """104°°""", 
        """101°°""", 
        """103°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """      In which version of°""", 
            """        SM64 was the BLJ°""", 
            """        glitch patched?°""", 
            """°""", 
            """°""", 
        ],
        """Shindou Edition°°""", 
        """European°°""", 
        """Wii Virtual Console°°""", 
    ),
]

trivia_medium_super_mario_world = [
    TriviaQuestion(
        [
            """°""", 
            """°""", 
            """ How many pairs of pipes exist°""", 
            """     in Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """6°°""", 
        """12°°""", 
        """8°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which of the following levels°""", 
            """    in Super Mario World has°""", 
            """  enemies trapped in bubbles?°""", 
            """°""", 
            """°""", 
        ],
        """Forest of Illusion 3°°""", 
        """Donut Plains 2°°""", 
        """Chocolate Island 5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of the following Super°""", 
            """   Mario World levels doesn't°""", 
            """  have enough Dragon Coins for°""", 
            """    a 1-Up/sending a check?°""", 
            """°""", 
        ],
        """Chocolate Secret°°""", 
        """Valley of Bowser 2°°""", 
        """Way Cool°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of the following items°""", 
            """    aren't needed for Forest°""", 
            """  of Illusion 4's Dragon Coins°""", 
            """  checks in Super Mario World?°""", 
            """°""", 
        ],
        """Run°°""", 
        """Fire Flower°°""", 
        """P-Switch°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Super Mario World, how°""", 
            """    many Dragon Coins can be°""", 
            """    found in Donut Secret 1?°""", 
            """°""", 
            """°""", 
        ],
        """7°°""", 
        """5°°""", 
        """6°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  In Super Mario World, which°""", 
            """    of the following levels°""", 
            """   doesn't have a bonus room?°""", 
            """°""", 
            """°""", 
        ],
        """Butter Bridge 2°°""", 
        """Morton's Castle°°""", 
        """Chocolate Island 5°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """  Which of the following ghost°""", 
            """   houses has a Big Boo fight°""", 
            """     in Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """Donut Secret House°°""", 
        """Forest Ghost House°°""", 
        """Valley Ghost House°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ What's an item that Magikoopas°""", 
            """   can spawn with their magic°""", 
            """     in Super Mario World?°""", 
            """°""", 
            """°""", 
        ],
        """A 1-Up mushroom°°""", 
        """A fire flower°°""", 
        """A coin with a smile°°""", 
    ),
    TriviaQuestion(
        [
            """  In Super Mario World, yellow°""", 
            """ colored Yoshis have a special°""", 
            """     ability when carrying°""", 
            """      a shell on its mouth°""", 
            """    which allows them to...°""", 
            """°""", 
        ],
        """Create an earthquake°°""", 
        """Spit three fireballs°°""", 
        """Grow wings°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ Which Forest of Illusion level°""", 
            """    in Super Mario World has°""", 
            """         a Midway Gate?°""", 
            """°""", 
            """°""", 
        ],
        """Forest of Illusion 1°°""", 
        """Forest of Illusion 2°°""", 
        """Forest Secret Area°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """    Which Super Mario World°""", 
            """   level has the most Yellow°""", 
            """     Switch Palace blocks?°""", 
            """°""", 
            """°""", 
        ],
        """Yoshi's Island 3°°""", 
        """Donut Plains 1°°""", 
        """Chocolate Island 2°°""", 
    ),
]

trivia_medium_super_metroid = [
]

trivia_medium_symphony_of_the_night = [
    TriviaQuestion(
        [
            """°""", 
            """   In Symphony of the Night,°""", 
            """     what items do you need°""", 
            """   to unlock the hidden area°""", 
            """      in Castle Entrance?°""", 
            """°""", 
        ],
        """Soul of Wolf & Bat°°""", 
        """Holy Glasses°°""", 
        """Spike Breaker°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Symphony of the Night,°""", 
            """ what is an alternative way to°""", 
            """  chain Gravity Jumps without°""", 
            """          Leap Stone?°""", 
            """°""", 
        ],
        """De-transforming mid-air°°""", 
        """Spamming X mid-air°°""", 
        """Casting Sword Brothers°°""", 
    ),
]

trivia_medium_terraria = [
    TriviaQuestion(
        [
            """°""", 
            """ In Terraria, what is the name°""", 
            """   of the achievement you get°""", 
            """   after defeating Deerclops°""", 
            """      for the first time?°""", 
            """°""", 
        ],
        """An Eye For An Eye°°""", 
        """Eye on You°°""", 
        """Hero of Etheria°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """ In Terraria, what is the name°""", 
            """   of the achievement you get°""", 
            """  after defeating Queen Slime°""", 
            """      for the first time?°""", 
            """°""", 
        ],
        """Just Desserts°°""", 
        """Sticky Situation°°""", 
        """Gelatin World Tour°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """   In Terraria, which of the°""", 
            """   following bosses does NOT°""", 
            """    have an "about to spawn°""", 
            """           message"?°""", 
            """°""", 
        ],
        """Eater of Worlds°°""", 
        """Eye of Cthulhu°°""", 
        """Mechdusa°°""", 
    ),
    TriviaQuestion(
        [
            """°""", 
            """     In Terraria, how many°""", 
            """ wing-type accessories can you°""", 
            """  craft with Souls of Flight?°""", 
            """°""", 
            """°""", 
        ],
        """15°°""", 
        """14°°""", 
        """12°°""", 
    ),
]

trivia_medium_the_legend_of_zelda = [
]

trivia_medium_vvvvvv = [
]

trivia_medium_yoshis_island = [
]


trivia_data = {
    "Terraria": [
        trivia_easy_terraria, 
        trivia_medium_terraria, 
        trivia_hard_terraria,
    ],
    "Yoshi's Island": [
        trivia_easy_yoshis_island, 
        trivia_medium_yoshis_island, 
        trivia_hard_yoshis_island,
    ],
    "Final Fantasy Mystic Quest": [
        trivia_easy_final_fantasy_mystic_quest, 
        trivia_medium_final_fantasy_mystic_quest, 
        trivia_hard_final_fantasy_mystic_quest,
    ],
    "A Link to the Past": [
        trivia_easy_a_link_to_the_past, 
        trivia_medium_a_link_to_the_past, 
        trivia_hard_a_link_to_the_past,
    ],
    "Cave Story": [
        trivia_easy_cave_story, 
        trivia_medium_cave_story, 
        trivia_hard_cave_story,
    ],
    "Mega Man X2": [
        trivia_easy_mega_man_x2, 
        trivia_medium_mega_man_x2, 
        trivia_hard_mega_man_x2,
    ],
    "Ocarina of Time": [
        trivia_easy_ocarina_of_time, 
        trivia_medium_ocarina_of_time, 
        trivia_hard_ocarina_of_time,
    ],
    "Rabi-Ribi": [
        trivia_easy_rabiribi, 
        trivia_medium_rabiribi, 
        trivia_hard_rabiribi,
    ],
    "EarthBound": [
        trivia_easy_earthbound, 
        trivia_medium_earthbound, 
        trivia_hard_earthbound,
    ],
    "Majora's Mask Recompiled": [
        trivia_easy_majoras_mask_recompiled, 
        trivia_medium_majoras_mask_recompiled, 
        trivia_hard_majoras_mask_recompiled,
    ],
    "Math": [
        trivia_easy_math, 
        trivia_medium_math, 
        trivia_hard_math,
    ],
    "Super Mario World": [
        trivia_easy_super_mario_world, 
        trivia_medium_super_mario_world, 
        trivia_hard_super_mario_world,
    ],
    "Kirby's Dream Land 3": [
        trivia_easy_kirbys_dream_land_3, 
        trivia_medium_kirbys_dream_land_3, 
        trivia_hard_kirbys_dream_land_3,
    ],
    "The Legend of Zelda": [
        trivia_easy_the_legend_of_zelda, 
        trivia_medium_the_legend_of_zelda, 
        trivia_hard_the_legend_of_zelda,
    ],
    "Overcooked! 2": [
        trivia_easy_overcooked_2, 
        trivia_medium_overcooked_2, 
        trivia_hard_overcooked_2,
    ],
    "Donkey Kong Country 2": [
        trivia_easy_donkey_kong_country_2, 
        trivia_medium_donkey_kong_country_2, 
        trivia_hard_donkey_kong_country_2,
    ],
    "Paper Mario": [
        trivia_easy_paper_mario, 
        trivia_medium_paper_mario, 
        trivia_hard_paper_mario,
    ],
    "Kingdom Hearts": [
        trivia_easy_kingdom_hearts, 
        trivia_medium_kingdom_hearts, 
        trivia_hard_kingdom_hearts,
    ],
    "Diddy Kong Racing": [
        trivia_easy_diddy_kong_racing, 
        trivia_medium_diddy_kong_racing, 
        trivia_hard_diddy_kong_racing,
    ],
    "Pokemon Red and Blue": [
        trivia_easy_pokemon_red_and_blue, 
        trivia_medium_pokemon_red_and_blue, 
        trivia_hard_pokemon_red_and_blue,
    ],
    "Mega Man 2": [
        trivia_easy_mega_man_2, 
        trivia_medium_mega_man_2, 
        trivia_hard_mega_man_2,
    ],
    "Donkey Kong Country 3": [
        trivia_easy_donkey_kong_country_3, 
        trivia_medium_donkey_kong_country_3, 
        trivia_hard_donkey_kong_country_3,
    ],
    "Hollow Knight": [
        trivia_easy_hollow_knight, 
        trivia_medium_hollow_knight, 
        trivia_hard_hollow_knight,
    ],
    "Kirby 64 - The Crystal Shards": [
        trivia_easy_kirby_64_the_crystal_shards, 
        trivia_medium_kirby_64_the_crystal_shards, 
        trivia_hard_kirby_64_the_crystal_shards,
    ],
    "Mega Man X3": [
        trivia_easy_mega_man_x3, 
        trivia_medium_mega_man_x3, 
        trivia_hard_mega_man_x3,
    ],
    "Actraiser": [
        trivia_easy_actraiser, 
        trivia_medium_actraiser, 
        trivia_hard_actraiser,
    ],
    "Risk of Rain 2": [
        trivia_easy_risk_of_rain_2, 
        trivia_medium_risk_of_rain_2, 
        trivia_hard_risk_of_rain_2,
    ],
    "Super Metroid": [
        trivia_easy_super_metroid, 
        trivia_medium_super_metroid, 
        trivia_hard_super_metroid,
    ],
    "Castlevania - Circle of the Moon": [
        trivia_easy_castlevania_circle_of_the_moon, 
        trivia_medium_castlevania_circle_of_the_moon, 
        trivia_hard_castlevania_circle_of_the_moon,
    ],
    "VVVVVV": [
        trivia_easy_vvvvvv, 
        trivia_medium_vvvvvv, 
        trivia_hard_vvvvvv,
    ],
    "Mega Man X": [
        trivia_easy_mega_man_x, 
        trivia_medium_mega_man_x, 
        trivia_hard_mega_man_x,
    ],
    "Kingdom Hearts 2": [
        trivia_easy_kingdom_hearts_2, 
        trivia_medium_kingdom_hearts_2, 
        trivia_hard_kingdom_hearts_2,
    ],
    "Mega Man 3": [
        trivia_easy_mega_man_3, 
        trivia_medium_mega_man_3, 
        trivia_hard_mega_man_3,
    ],
    "Super Mario 64": [
        trivia_easy_super_mario_64, 
        trivia_medium_super_mario_64, 
        trivia_hard_super_mario_64,
    ],
    "Pokemon Emerald": [
        trivia_easy_pokemon_emerald, 
        trivia_medium_pokemon_emerald, 
        trivia_hard_pokemon_emerald,
    ],
    "Symphony of the Night": [
        trivia_easy_symphony_of_the_night, 
        trivia_medium_symphony_of_the_night, 
        trivia_hard_symphony_of_the_night,
    ],
    "Pokemon Crystal": [
        trivia_easy_pokemon_crystal, 
        trivia_medium_pokemon_crystal, 
        trivia_hard_pokemon_crystal,
    ],
    "Sonic Adventure 2 Battle": [
        trivia_easy_sonic_adventure_2_battle, 
        trivia_medium_sonic_adventure_2_battle, 
        trivia_hard_sonic_adventure_2_battle,
    ],
    "Astalon": [
        trivia_easy_astalon, 
        trivia_medium_astalon, 
        trivia_hard_astalon,
    ],
}


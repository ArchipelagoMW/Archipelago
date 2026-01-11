# Data module for dialog data.

from ...randomizer.logic import utils
from ...randomizer.logic.patch import Patch

# This table isn't complete.
# And some of the single char replacements should be done via string.translate,
compression_table = [
    ('\n', '\x01'),
    (' and ', '\x15'),
    (' the', '\x0E'),
    (' you', '\x0F'),
    (' to ', '\x11'),
    ('    ', '\x0A'),
    (' so', '\x17'),
    ('is ', '\x16'),
    ("'s ", '\x12'),
    ('   ', '\x09'),
    (' I ', '\x14'),
    ('  ', '\x08'),
    ('in', '\x10'),
    ('Mario', '\x13'),
    ("'", '\x9B'),
    (':', '\x8E'),
    ('~', '\x3A'),
]

DIALOG_POINTER_BASE_ADDRESS = 0x37e000


def compress(string):
    # TODO: Use \x0B to compress longer spacings..
    for token, char in compression_table:
        string = string.replace(token, char)
    return string + '\x00'  # Null terminate strings.


# Formatting is tricky. Probably should test it out in the game itself.
# 1. Use newlines. If a string goes too long, sometimes it wraps around to the
#    other side and sometimes it softlocks the game. Definitely test these first
#    before updating.
wish_strings = list(map(compress, [
    '\n\n    I wish for fish.',
    '\n\n    I weesh for quiche.',
    '\n\n    I wish I was a little bit taller.',
    '\n\n    I wish I was a baller.',
    '\n\n    I wish for more wishes!',
    '\n\n    I wish I was in this game.',
    '\n\n    SMRPG is the best\n    Final Fantasy!',
    '\n\n    I wish this was\n    Ecco the Dolphin.',
    '\n\n    (Hope this is a better\n     seed than last time)',
    '\n\n    When\'s Marvel?',
    '\n\n    Just 200 more fights\n    till General Leo\n    joins my party!',
    '\n\n    Please let Culex\n    be at Hammer Bros.',
    '\n\n    I hope can get out of level 3.',
    '\n\n    I wish I could count to 10.',
    '\n\n    I wish this seed would end.',
    '\n\n    I wish there was a\n    star piece here.',
    '\n\n    I wish I was a tadpole.',
    '\n\n    I wish Geno was in Smash.',
    '\nOh,\nI wish, I wish\nI hadn\'t killed that fish.',
    'Like the moon over\nthe day, my genius and brawn\nare lost on these fools. \x24Haiku',
    '\n\n    Escalators, escalators,\n    escalators.....\n    ...eeeeeeeels...',
    '\n\n    I wish someone would come\n    visit me and my crystal\n    pals in Monstrotown.',
    '\n\n    I wish Pain Man was\n    in this game... ',
    '\n\n    I wish I could\n    get a sub-3:00.',
    '\n\n    I wish I was an\n    Oscar Mayer weiner.',
    '\n\n    I wish I could share\n    my wisdom with the world.',
    '\n\n    I wish Mario would\n    stop skipping me!\n    ~Mack',
    '\n\n    One of the most important\n    skills you can have\n    is just being lucky!',
    '\n\n    I wish someone would\n    play randomizers with me.',
    '\n\n    I wish Nintendo would\n    return to Paper Mario 64\n    and The Thousand-Year Door.',
    '\n\n    I wish somebody would\n    stop rearranging the\n    stock in my store!',
    '\n\n    I wish we raced using\n    currency that wasn\'t\n    also food.',
    '\n\n    I wish I had\n    Justin\'s luck.',
    '\n\n    Expecting a wish?\x03\n\n      TOO BAD.\n    WALUIGI TIME.',
    '\n\n    It\'s now safe to turn off\n    your Super Nintendo.\x0D\xFF\n    Just kidding!',
    '\n\n    No wish for you!!',
    '\n\n    Tenth enemy has the wish!',
    '\n\n    I wish I could grant\n    meta-wishes...',
    '\n\n    I see the stars pieces,\n    but I have to find an\n    octagon!',
    '\n\n    I wish my computer could\n    play this.',
    '\n\n    I wish you\'d come to my house.\n    Do some stuff at my house.\n    Play some Kaizo at my house.',
    '\n\n    I wish Ridley I weren\'t\n    too big to fit in this game',
    '\n\n    Yo Mario, I\'m really happy\n    for you, Imma let you finish,\n    but Sonic had one of the best\n    video games of all time...\n    one of the best video games\n    of all time!',
    '\n\n    I wish Bowsette were canon.',
    '\n\n    I understand why they do it,\n    but I wish they\'d give\n    an option to remove the beeping.',
    '\n\n    I wish the Bowser warp\n    was still a thing.',
    '\n\n    I wish Mario would stop\n    dropping me down pits.',
]))

wish_dialogs = [
    3111,
    3108,
    3110,
    3109,
    3116,
    3327,
    3114,
    3326,
    3115,
    3106,
    3275,
    3113,
    3325,
    3105,
    3112,
    3107,
]


class Wishes:
    def __init__(self, world):
        self.world = world
        self.wishes = []

    @property
    def name(self):
        return self.__class__.__name__

    def get_patch(self):
        """
        Returns:
            randomizer.logic.patch.Patch: Patch data
        """
        patch = Patch()

        # A big assumption here is that the dialogs aren't getting relocated
        # out if the 0x240000 bank.
        for dialog_id, pointer, wish in self.wishes:
            table_entry = DIALOG_POINTER_BASE_ADDRESS + dialog_id * 2
            patch.add_data(table_entry, utils.ByteField((pointer - 4) & 0xFFFF, num_bytes=2).as_bytes())
            patch.add_data(pointer, wish)

        return patch


quiz_dialogs = list(range(1842, 1882))
wrong_indexes = [[1, 2], [0, 2], [0, 1]]


class Quiz:
    def __init__(self, world):
        self.world = world
        self.questions = []

    @property
    def name(self):
        return self.__class__.__name__

    def get_patch(self):
        """
        Returns:
            randomizer.logic.patch.Patch: Patch data
        """
        patch = Patch()

        for dialog_id, pointer, question in self.questions:
            table_entry = DIALOG_POINTER_BASE_ADDRESS + dialog_id * 2
            patch.add_data(table_entry, utils.ByteField((pointer - 8) & 0xFFFF, num_bytes=2).as_bytes())
            if question:
                patch.add_data(pointer, question)

        return patch


class Question:
    def __init__(self, question, correct, wrong_1, wrong_2):
        self.question = question
        self.correct_answer = correct
        self.wrong_answers = [wrong_1, wrong_2]

    def get_string(self, correct_index):
        answers = [''] * 3
        answers[correct_index] = ' \x07  ' + self.correct_answer + '\n'
        index_1, index_2 = wrong_indexes[correct_index]
        answers[index_1] = ' \x07  ' + self.wrong_answers[0] + '\n'
        answers[index_2] = ' \x07  ' + self.wrong_answers[1] + '\n'
        final_string = self.question + '\x03' + ''.join(answers)
        final_string = final_string[:-1]  # Remove trailing newline from final answer.
        return compress(final_string)

    @property
    def string_length(self):
        return len(self.get_string(0))

    def __len__(self):
        return self.string_length


def get_quiz_questions():
    """Get new list of potential quiz questions for the randomizer.

    Returns:
        list[Question]: List of questions.

    """
    # New static quiz questions we added.
    acc = [
        Question('What game gives\nyou the Star Egg?', 'Look The Other Way', 'Blackjack', 'Pokemon'),
        Question('Who is Yoshi\'s nemesis?', 'Boshi', 'Broshi', 'Raz'),
        Question('What can you trade\nthe Shiny Stone for?', 'Carbo Cookie', 'Fireworks', 'A Frog Coin'),
        Question('Which isn\'t a setting\non Monstro Town\'s Pinwheel?', 'Blow', 'Gust', 'Blast'),
        Question('How does Mario taste?', 'Ack! Sour!', 'YES! THIS is YUMMY!', 'Mmm, tastes peachy...'),
        Question('How does Mallow taste?', 'YES! THIS is YUMMY!', 'Mmm, tastes peachy...', 'Ack! Sour!'),
        Question('How does Geno taste?', 'Bitter, but not bad...', 'Ack! Sour!', 'Yuck! How repulsive!'),
        Question('How does Bowser taste?', 'Yuck! How repulsive!', 'Bitter, but not bad...', 'YES! THIS is YUMMY!'),
        Question('How does Toadstool taste?', 'Mmm, tastes peachy...', 'YES! THIS is YUMMY!', 'Bitter, but not bad...'),
        Question('Like the moon over\nthe day, my genius and brawn...', 'are lost on these fools.',
                 'are hollow echoes.', 'are without equal.'),
        Question('Which of these is NOT\na card for the Juice Bar?', 'Baritone Card', 'Tenor Card', 'Soprano Card'),
        Question('What type of clothes\nare normally sold\nin Nimbus Land?', 'Fuzzy', 'Happy', 'Thick'),
        Question('Where did Samus Aran\nstay the night?', 'Mushroom Kingdom', 'Rose Town', 'Nimbus Land'),
        Question('Where did Link\nstay the night?', 'Rose Town', 'Mushroom Kingdom', 'Nimbus Land'),
        Question('Which enemy uses Blast?', 'Earth Crystal', 'Wind Crystal', 'Fire Crystal'),
        Question('Which enemy uses Drain?', 'Fire Crystal', 'Wind Crystal', 'Earth Crystal'),
        Question('Which enemy uses Light Beam?', 'Wind Crystal', 'Water Crystal', 'Earth Crystal'),
        Question('Which enemy uses Crystal?', 'Water Crystal', 'Wind Crystal', 'Fire Crystal'),
        Question('Which equip allows you to\njump through enemy defenses?', 'Jump Shoes', 'Zoom Shoes', 'Spring Shoes'),
        Question('How many wishes\ncan you interact with\non Star Hill?', '12', '10', '15'),
        Question('Jawful is...?', 'Sleeping', 'Enraptured', 'Ready to launch!'),
        Question('Valentina\'s hair is\nmade of a...?', 'Parrot', 'Plant', 'Octopus'),
        Question('Who knocks out Mario?', 'Gaz', 'Raz', 'Garro'),
        Question('What does Dyna get\ninto the business of?', 'Trading', 'Selling items', 'Giving hints'),
        Question('Who summons Bahamutt?', 'Magikoopa', 'Belome', 'Box Boy'),
        Question('The Gardener wants to hit\nthe lottery without what?', 'Paying taxes', 'Skiing',
                 'Getting his picture taken'),
        Question('Who is the cloud enemy\nin Land\'s End?', 'Mokura', 'Bokura', 'Goku'),
        Question('Who gets mad if you\nstand on their head?', 'Johnny', 'Frogfucius', 'Jinx'),
        Question('What does Bowser love\nthe scent of?', 'Boiling lava', 'Flower beds', 'Green donkeys'),
        Question('How many bolts hold together\nthe inner factory battlefield?', '4', '3', '5'),
        Question('How much damage does a\nboosted Ice Bomb normally do\nagainst Czar Dragon?', '420', '210', '69'),
        Question('What snake boss does\nDomino join up with?', 'Mad Adder', 'Earthlink', 'Culex'),
        Question('Who is NOT a hidden\nchest boss?', 'Fautso', 'Box Boy', 'Chester'),
        Question('What is Geno\'s move\nthat knocks out Mario?', 'Shooting Star Shot', 'Special Beam Cannon',
                 'Spirit Gun'),
        Question('Vat ist zee name of\nzee cake you fight\nin Marrymore?', 'Bundt', 'German Chocolate', 'Pound'),
        Question('How many more points in\nGoomba Thumping are needed\nto win another reward?', '2', '4', '6'),
        Question('How many hidden treasure\nchests are in the\nvanilla game?', '39', '38', '40'),
        Question('Which accessory does NOT\nprovide an attack boost\nto the equipped character?', 'Ghost Medal',
                 'Troopa Pin ', 'Quartz Charm'),
        Question('What is Johnny looking\nat in the end credits?', 'Sunset', 'Mario', 'His ship'),
        Question('How many citizens are at\nMallow\'s coronation ceremony?', '12', '9', '5'),
        Question('Who is flying Bowser\'s\nclown car in the\nending cutscene?', 'Shy Guy', 'Terrapin', 'Magikoopa'),
        Question('Who does Yoshi race against\nin the ending cutscene?', 'Croco', 'Boshi', 'Mario'),
        Question('How many Toads are in\nToadofsky\'s choir?', '7', '4', '10'),
        Question('Who does Booster\nend up marrying?', 'Valentina', 'Toadstool', 'Raini'),
        Question('How many Toads immediately\nfollow Luigi in the parade?', '5', '3', '2'),
        Question('What makes a sound when\na hidden chest is near?', 'Signal Ring', 'B\'tub Ring', 'Safety Ring'),
        Question('Which type of armor\nis normally only usable\nby Bowser?', 'Courage', 'Fire', 'Sailor'),
        Question('What happens when a\nYoshi Cookie fails?', 'Get Yoshi Candy instead', 'Enemy bites Yoshi\'s tongue',
                 'Yoshi lays an egg'),
        Question('What is the travelling\nToad looking for?', 'Grate Guy\'s Casino', 'Best inn to stay at',
                 'Star pieces'),
        Question('Which does NOT normally\ngive immunity to\ninstant death attacks?', 'Super Suit', 'Attack Scarf',
                 'Quartz Charm'),
        Question('Which enemy is NOT found\nin the same location\nas the others?', 'Wiggler', 'Mukumuku', 'Mastadoom'),
        Question('How many tentacles does\nKing Calimari have?', '8', '6', '10'),
        Question('Which is NOT one of the\nAxem Rangers?', 'Blue', 'Pink', 'Red'),
        Question('Which is NOT one of\nCountdown\'s attacks?', 'Boulder', 'Mega Recover', 'Aurora Flash'),
        Question('Which attack does Mack\nuse on you?', 'Flame Wall', 'S\'Crow Dust', 'Static E!'),
        Question('Who do you attack\ninstead of Bowser\nin the prologue?', 'Kinklink', 'Throne', 'Support'),
        Question('Where is the Goomba\nthumping game located?', 'Pipe Vault', 'Moleville', 'Monstro Town'),
        Question('Which is NOT normally\none of Mallow\'s\nspecial attacks?', 'Mute', 'Psychopath', 'Snowy'),
        Question('What special attack does\nMario normally start with?', 'Jump', 'Fire Orb', 'Crusher'),
        Question('Who does Toadstool\nalmost marry?', 'Booster', 'Bowser', 'Mario'),
        Question('What menu option appears\nwhen your fourth\nparty member joins?', 'Switch', 'Team', 'Power'),
        Question('What did Croco steal\nfrom Mallow?', 'Frog Coin', 'Wallet', 'Kerokerocola'),
        Question('What does Hammer Bro use\nwhen one is defeated?', 'Valor Up', 'Vigor Up', 'Versatility Up'),
        Question('What is the name of\nMario\'s house?', 'The Pipehouse', 'Mario Manor', 'The Goomba Hole'),
        Question('Where do you fight\nBowser in the prologue?', 'On chandeliers', 'Over a lava pit', 'A large arena'),
    ]

    return acc


# Vanilla questions to backfill with if we don't have enough other ones.
backfill_questions = [
    Question('How much...does a\nfemale beetle cost?', '1 coin', '50 coins', 'A frog coin'),
    Question('What does Belome\nreally like to turn people into?', 'Scarecrows', 'Ice cream cones', 'Mushrooms'),
    Question('What is Raini\'s\nhusband\'s name?', 'Raz', 'Romeo', 'Gaz'),
    Question('What\'s the name of\nthe boss at the Sunken Ship?', 'Johnny', 'Jimmy', 'Jackson'),
    Question('Booster is what\ngeneration?', '7th', '8th', '78th'),
    Question('Where is the 3rd\nStar Piece normally found?', 'Moleville', 'Forest Maze', 'Star Hill'),
    Question('Johnny loves WHICH\nbeverage?...', 'Currant juice', 'Grape juice', 'Boysenberry smoothie'),
    Question('In the Moleville blues,\nit\'s said that the moles are\ncovered in what?', 'Soil', 'Dirt', 'Slugs'),
    Question('What color are the\ncurtains in Mario\'s house?', 'Blue', 'Green', 'Red'),
    Question('Yaridovich is what?', 'A boss', 'A new breed of cattle', 'A special attack'),
    Question('The boy at the inn in\nMushroom Kingdom was playing\nwith...What?', 'Game Boy', 'Super NES',
             'Virtual Boy'),
    Question('What did Carroboscis\nturn into?', 'A carrot', 'A beet', 'A radish'),
    Question('Who is the famous\nsculptor in Nimbus Land?', 'Garro', 'Gaz', 'Goya'),
    Question('What is Hinopio in\ncharge of at the middle counter?', 'The inn', 'Weapons', 'Items'),
    Question('Who is the ultimate\nenemy in this adventure?', 'Smithy', 'Bowser', 'Goomba'),
    Question('Who is the leader of\nThe Axem Rangers?', 'Red', 'Black', 'Green'),
    Question('What\'s the name of\nJagger\'s "sensei#?', 'Jinx', 'Dinky', 'Johnny'),
    Question('How many underlings\ndoes Croco have?', '3', '2', '4'),
    Question('What was Toadstool\ndoing when she was kidnapped by\nBowser?', 'She was looking at flowers',
             'She was playing cards', 'She was digging for worms'),
    Question('Who is the famous\ncomposer at Tadpole Pond?', 'Toadofsky', 'Toadoskfy', 'Frogfucius'),
    Question('Which monster does\nnot appear in Booster Tower?', 'Terrapin', 'Jester', 'Bob-omb'),
    Question('The boy getting his\npicture taken at Marrymore\ncan\'t wait \'til which season?', 'Skiing', 'Hunting',
             'Baseball'),
    Question('What technique does Bowser\nnormally learn at Level 15?', 'Crusher', 'Bowser Crush', 'Terrorize'),
    Question('What words does\nShy Away use when he sings?', 'La dee dah:', 'Dum dee dah:', 'Dum lee lah:'),
    Question('What does Birdo\ncome out of?', 'An eggshell', 'A barrel', 'A basket'),
    Question('What\'s the first\nmonster you see in the Pipe Vault?', 'Sparky', 'Goomba', 'Chompweed'),
    Question('What\'s the password\nin the Sunken Ship?', 'Pearls', 'Corals', 'Oyster'),
    Question('What was Mallow \nasked to get for Frogfucius?', 'Cricket Pie', 'Honey Syrup', 'Carbo Cookie'),
    Question('Mite is Dyna\'s...\nWHAT?', 'Little brother', 'Big sister', 'Second cousin'),
    Question('What does the Red\nEssence do?', 'Gives you strength', 'Makes you sleepy', 'Relieves back pain'),
    Question('How long have the\ncouple inside the chapel been\nwaiting for their wedding?', '30 minutes', '1 hour',
             '45 minutes'),
    Question('What do Culex, Jinx,\nand Goomba have in common?', 'They live in Monstro Town', 'They are immortal',
             'They all like bratwurst'),
    Question('What is the 4th\nselection on the Menu screen?', 'Equip', 'Important Items', 'Special Items'),
    Question('The man getting his\npicture taken at Marrymore\nhates what?', 'Getting his picture taken',
             'Getting married', 'Mowing the lawn on Sundays'),
    Question('Where is the 1st\nStar Piece normally found?', 'Mushroom Kingdom', 'Bowser\'s Keep', 'Mario\'s Pad'),
    Question('How many legs does\nWiggler have?', '6', '10', '8'),
    Question('What\'s the full name\nof the boss at the Sunken Ship?', 'Jonathan Jones', 'Johnny Jones',
             'Jesse James Jones'),
    Question('Who helped you up the\ncliff at Land\'s End?', 'Sky Troopas', 'Sky Troops', 'Flying Troopa'),
    Question('What color is the\nend of Dodo\'s beak?', 'Red', 'Yellow', 'Orange'),
    Question('What\'s the chef\'s\nname at Marrymore?', 'Torte', 'Blintz', 'Gateau'),
]

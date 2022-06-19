from typing import Optional, Union, Iterable, NamedTuple

from BaseClasses import Item, MultiWorld, ItemClassification as IC


class ItemData(NamedTuple):
    classification: IC
    item_type: Optional[str]
    item_code: Union[Optional[int], Iterable[int]]
    pedestal_hint: Optional[str]
    pedestal_credit: Optional[str]
    sick_kid_credit: Optional[str]
    zora_credit: Optional[str]
    witch_credit: Optional[str]
    flute_boy_credit: Optional[str]
    hint_text: Optional[str]
    item_id: int = None


class ALttPItem(Item):
    game: str = 'A Link to the Past'
    item_type: str = None
    pedestal_hint_text: str
    pedestal_credit_text: str
    sick_kid_credit_text: str
    zora_credit_text: str
    potion_shop_credit_text: str
    flute_boy_credit_text: str
    hint_text: str
    item_code: Union[Optional[int], Iterable[int]]

    def __init__(self, name: str, player: int, data: ItemData):
        super().__init__(name, data.advancement, data.item_id, player)
        self.pedestal_hint_text = data.pedestal_hint
        self.pedestal_credit_text = data.pedestal_credit
        self.sick_kid_credit_text = data.sick_kid_credit
        self.zora_credit_text = data.zora_credit
        self.potion_shop_credit_text = data.witch_credit
        self.flute_boy_credit_text = data.flute_boy_credit
        self.hint_text = data.hint_text
        self.trap = data.trap
        self.item_code = data.item_code
        if data.item_type:
            self.item_type = data.item_type

    @property
    def crystal(self) -> bool:
        return self.type == 'crystal'

    @property
    def small_key(self) -> bool:
        return self.type == 'small_key'

    @property
    def big_key(self) -> bool:
        return self.type == 'big_key'

    @property
    def map(self) -> bool:
        return self.type == 'map'

    @property
    def compass(self) -> bool:
        return self.type == 'compass'

    @property
    def dungeon_item(self) -> Optional[str]:
        if self.small_key or self.big_key or self.map or self.compass:
            return self.type

    @property
    def locked_dungeon_item(self):
        return self.location.locked and self.dungeon_item


def get_beemizer_item(world: MultiWorld, item: Item):
    if item.name not in trap_replaceable:
        return item
    if not world.beemizer_total_chance or world.random.random() > (world.beemizer_total_chance / 100):
        return item
    if not world.beemizer_trap_chance or world.random.random() > (world.beemizer_trap_chance / 100):
        return world.create_item('Bee')
    return world.create_item('Bee Trap')


# Format: Name: (Advancement, Type, ItemCode, Pedestal Hint Text, Pedestal Credit Text, Sick Kid Credit Text, Zora Credit Text, Witch Credit Text, Flute Boy Credit Text, Hint Text, AP Code, Trap)
item_table = {
    'Bow': ItemData(IC.progression, None, 0x0B, 'You have\nchosen the\narcher class.', 'the stick and twine', 'arrow-slinging kid', 'arrow sling for sale', 'witch and robin hood', 'archer boy shoots again', 'the Bow', 5000),
    'Progressive Bow': ItemData(IC.progression, None, 0x64, 'You have\nchosen the\narcher class.', 'the stick and twine', 'arrow-slinging kid', 'arrow sling for sale', 'witch and robin hood', 'archer boy shoots again', 'a Bow', 5001),
    'Progressive Bow (Alt)': ItemData(IC.progression, None, 0x65, 'You have\nchosen the\narcher class.', 'the stick and twine', 'arrow-slinging kid', 'arrow sling for sale', 'witch and robin hood', 'archer boy shoots again', 'a Bow', 5002),
    'Silver Arrows': ItemData(IC.progression, None, 0x58, 'Do you fancy\nsilver tipped\narrows?', 'and the ganonsbane', 'ganon-killing kid', 'ganon doom for sale', 'fungus for pork','archer boy shines again', 'the Silver Arrows', 5003),
    'Silver Bow': ItemData(IC.progression, None, 0x3B, 'Buy 1 Silver\nget Archery\nfor free.', 'the baconmaker', 'ganon-killing kid', 'ganon doom for sale', 'fungus for pork', 'archer boy shines again', 'the Silver Bow', 5004),
    'Book of Mudora': ItemData(IC.progression, None, 0x1D, 'Hylian\nfor\nDingusses.', 'and the story book', 'the scholarly kid', 'moon runes for sale', 'drugs for literacy', 'book-worm boy can read again', 'the Book', 5005),
    'Hammer': ItemData(IC.progression, None, 0x09, 'stop\nhammer time!', 'and m c hammer', 'hammer-smashing kid', 'm c hammer for sale', 'stop...   hammer time', 'stop, hammer time', 'the Hammer', 5006),
    'Hookshot': ItemData(IC.progression, None, 0x0A, 'BOING!!!\nBOING!!!\nBOING!!!', 'and the tickle beam', 'tickle-monster kid', 'tickle beam for sale', 'witch and tickle boy', 'beam boy tickles again', 'the Hookshot', 5007),
    'Magic Mirror': ItemData(IC.progression, None, 0x1A, 'Isn\'t your\nreflection so\npretty?', 'the face reflector', 'the narcissistic kid', 'your face for sale', 'trades looking-glass', 'narcissistic boy is happy again', 'the Mirror', 5008),
    'Flute': ItemData(IC.progression, None, 0x14, 'Save the duck\nand fly to\nfreedom!', 'and the duck call', 'the duck-call kid', 'duck call for sale', 'duck-calls for trade', 'flute boy plays again', 'the Flute', 5009),
    'Pegasus Boots': ItemData(IC.progression, None, 0x4B, 'Gotta go fast!', 'and the sprint shoes', 'the running-man kid', 'sprint shoe for sale', 'shrooms for speed', 'gotta-go-fast boy runs again', 'the Boots', 5010),
    'Power Glove': ItemData(IC.progression, None, 0x1B, 'Now you can\nlift weak\nstuff!', 'and the grey mittens', 'body-building kid', 'lift glove for sale', 'fungus for gloves', 'body-building boy lifts again', 'the Glove', 5011),
    'Cape': ItemData(IC.progression, None, 0x19, 'Wear this to\nbecome\ninvisible!', 'the camouflage cape', 'red riding-hood kid', 'red hood for sale', 'hood from a hood', 'dapper boy hides again', 'the Cape', 5012),
    'Mushroom': ItemData(IC.progression, None, 0x29, 'I\'m a fun guy!\n\nI\'m a funghi!', 'and the legal drugs', 'the drug-dealing kid', 'legal drugs for sale', 'shroom swap', 'shroom boy sells drugs again', 'the Mushroom', 5013),
    'Shovel': ItemData(IC.progression, None, 0x13, 'Can\n   You\n      Dig it?', 'and the spade', 'archaeologist kid', 'dirt spade for sale', 'can you dig it', 'shovel boy digs again', 'the Shovel', 5014),
    'Lamp': ItemData(IC.progression, None, 0x12, 'Baby, baby,\nbaby.\nLight my way!', 'and the flashlight', 'light-shining kid', 'flashlight for sale', 'fungus for illumination', 'illuminated boy can see again', 'the Lamp', 5015),
    'Magic Powder': ItemData(IC.progression, None, 0x0D, 'you can turn\nanti-faeries\ninto faeries', 'and the magic sack', 'the sack-holding kid', 'magic sack for sale', 'the witch and assistant', 'magic boy plays marbles again', 'the Powder', 5016),
    'Moon Pearl': ItemData(IC.progression, None, 0x1F, '  Bunny Link\n      be\n     gone!', 'and the jaw breaker', 'fortune-telling kid', 'lunar orb for sale', 'shrooms for moon rock', 'moon boy plays ball again', 'the Moon Pearl', 5017),
    'Cane of Somaria': ItemData(IC.progression, None, 0x15, 'I make blocks\nto hold down\nswitches!', 'and the red blocks', 'the block-making kid', 'block stick for sale', 'block stick for trade', 'cane boy makes blocks again', 'the Red Cane', 5018),
    'Fire Rod': ItemData(IC.progression, None, 0x07, 'I\'m the hot\nrod. I make\nthings burn!', 'and the flamethrower', 'fire-starting kid', 'rage rod for sale', 'fungus for rage-rod', 'firestarter boy burns again', 'the Fire Rod', 5019),
    'Flippers': ItemData(IC.progression, None, 0x1E, 'fancy a swim?', 'and the toewebs', 'the swimming kid', 'finger webs for sale', 'shrooms let you swim', 'swimming boy swims again', 'the Flippers', 5020),
    'Ice Rod': ItemData(IC.progression, None, 0x08, 'I\'m the cold\nrod. I make\nthings freeze!', 'and the freeze ray', 'the ice-bending kid', 'freeze ray for sale', 'fungus for ice-rod', 'ice-cube boy freezes again', 'the Ice Rod', 5021),
    'Titans Mitts': ItemData(IC.progression, None, 0x1C, 'Now you can\nlift heavy\nstuff!', 'and the golden glove', 'body-building kid', 'carry glove for sale', 'fungus for bling-gloves', 'body-building boy has gold again', 'the Mitts', 5022),
    'Bombos': ItemData(IC.progression, None, 0x0F, 'Burn, baby,\nburn! Fear my\nring of fire!', 'and the swirly coin', 'coin-collecting kid', 'swirly coin for sale', 'shrooms for swirly-coin', 'medallion boy melts room again', 'Bombos', 5023),
    'Ether': ItemData(IC.progression, None, 0x10, 'This magic\ncoin freezes\neverything!', 'and the bolt coin', 'coin-collecting kid', 'bolt coin for sale', 'shrooms for bolt-coin', 'medallion boy sees floor again', 'Ether', 5024),
    'Quake': ItemData(IC.progression, None, 0x11, 'Maxing out the\nRichter scale\nis what I do!', 'and the wavy coin', 'coin-collecting kid', 'wavy coin for sale', 'shrooms for wavy-coin', 'medallion boy shakes dirt again', 'Quake', 5025),
    'Bottle': ItemData(IC.progression, None, 0x16, 'Now you can\nstore potions\nand stuff!', 'and the terrarium', 'the terrarium kid', 'terrarium for sale', 'special promotion', 'bottle boy has terrarium again', 'a bottle', 5026),
    'Bottle (Red Potion)': ItemData(IC.progression, None, 0x2B, 'Hearty red goop!', 'and the red goo', 'the liquid kid', 'potion for sale', 'free samples', 'bottle boy has red goo again', 'a bottle', 5027),
    'Bottle (Green Potion)': ItemData(IC.progression, None, 0x2C, 'Refreshing green goop!', 'and the green goo', 'the liquid kid', 'potion for sale', 'free samples', 'bottle boy has green goo again', 'a bottle', 5028),
    'Bottle (Blue Potion)': ItemData(IC.progression, None, 0x2D, 'Delicious blue goop!', 'and the blue goo', 'the liquid kid', 'potion for sale', 'free samples', 'bottle boy has blue goo again', 'a bottle', 5029),
    'Bottle (Fairy)': ItemData(IC.progression, None, 0x3D, 'Save me and I will revive you', 'and the captive', 'the tingle kid','hostage for sale', 'fairy dust and shrooms', 'bottle boy has friend again', 'a bottle', 5030),
    'Bottle (Bee)': ItemData(IC.progression, None, 0x3C, 'I will sting your foes a few times', 'and the sting buddy', 'the beekeeper kid', 'insect for sale', 'shroom pollenation', 'bottle boy has mad bee again', 'a bottle', 5031),
    'Bottle (Good Bee)': ItemData(IC.progression, None, 0x48, 'I will sting your foes a whole lot!', 'and the sparkle sting', 'the beekeeper kid', 'insect for sale', 'shroom pollenation', 'bottle boy has beetor again', 'a bottle', 5032),
    'Master Sword': ItemData(IC.progression, 'Sword', 0x50, 'I beat barries and pigs alike', 'and the master sword', 'sword-wielding kid', 'glow sword for sale', 'fungus for blue slasher', 'sword boy fights again', 'the Master Sword', 5033),
    'Tempered Sword': ItemData(IC.progression, 'Sword', 0x02, 'I stole the\nblacksmith\'s\njob!', 'the tempered sword', 'sword-wielding kid', 'flame sword for sale', 'fungus for red slasher', 'sword boy fights again', 'the Tempered Sword', 5034),
    'Fighter Sword': ItemData(IC.progression, 'Sword', 0x49, 'A pathetic\nsword rests\nhere!', 'the tiny sword', 'sword-wielding kid', 'tiny sword for sale', 'fungus for tiny slasher', 'sword boy fights again', 'the Small Sword', 5035),
    'Golden Sword': ItemData(IC.progression, 'Sword', 0x03, 'The butter\nsword rests\nhere!', 'and the butter sword', 'sword-wielding kid', 'butter for sale', 'cap churned to butter', 'sword boy fights again', 'the Golden Sword', 5036),
    'Progressive Sword': ItemData(IC.progression, 'Sword', 0x5E, 'a better copy\nof your sword\nfor your time', 'the unknown sword', 'sword-wielding kid', 'sword for sale', 'fungus for some slasher', 'sword boy fights again', 'a Sword', 5037),
    'Progressive Glove': ItemData(IC.progression, None, 0x61, 'a way to lift\nheavier things', 'and the lift upgrade', 'body-building kid', 'some glove for sale', 'fungus for gloves', 'body-building boy lifts again', 'a Glove', 5038),
    'Green Pendant': ItemData(IC.progression, 'Crystal', (0x04, 0x38, 0x62, 0x00, 0x69, 0x01), None, None, None, None, None, None, "the green pendant", item_id=5039),
    'Blue Pendant': ItemData(IC.progression, 'Crystal', (0x02, 0x34, 0x60, 0x00, 0x69, 0x02), None, None, None, None, None, None, "the blue pendant", item_id=5040),
    'Red Pendant': ItemData(IC.progression, 'Crystal', (0x01, 0x32, 0x60, 0x00, 0x69, 0x03), None, None, None, None, None, None, "the red pendant", item_id=5041),
    'Triforce': ItemData(IC.progression, None, 0x6A, '\n   YOU WIN!', 'and the triforce', 'victorious kid', 'victory for sale', 'fungus for the win', 'greedy boy wins game again', 'the Triforce', 5042),
    'Power Star': ItemData(IC.progression, None, 0x6B, 'a small victory', 'and the power star', 'star-struck kid', 'star for sale', 'see stars with shroom', 'mario powers up again', 'a Power Star', 5043),
    'Triforce Piece': ItemData(IC.progression, None, 0x6C, 'a small victory', 'and the thirdforce', 'triangular kid', 'triangle for sale', 'fungus for triangle', 'wise boy has triangle again', 'a Triforce Piece', 5044),
    'Crystal 1': ItemData(IC.progression, 'Crystal', (0x02, 0x34, 0x64, 0x40, 0x7F, 0x06), None, None, None, None, None, None, "a blue crystal", item_id=5045),
    'Crystal 2': ItemData(IC.progression, 'Crystal', (0x10, 0x34, 0x64, 0x40, 0x79, 0x06), None, None, None, None, None, None, "a blue crystal", item_id=5046),
    'Crystal 3': ItemData(IC.progression, 'Crystal', (0x40, 0x34, 0x64, 0x40, 0x6C, 0x06), None, None, None, None, None, None, "a blue crystal", item_id=5047),
    'Crystal 4': ItemData(IC.progression, 'Crystal', (0x20, 0x34, 0x64, 0x40, 0x6D, 0x06), None, None, None, None, None, None, "a blue crystal", item_id=5048),
    'Crystal 5': ItemData(IC.progression, 'Crystal', (0x04, 0x32, 0x64, 0x40, 0x6E, 0x06), None, None, None, None, None, None, "a red crystal", item_id=5049),
    'Crystal 6': ItemData(IC.progression, 'Crystal', (0x01, 0x32, 0x64, 0x40, 0x6F, 0x06), None, None, None, None, None, None, "a red crystal", item_id=5050),
    'Crystal 7': ItemData(IC.progression, 'Crystal', (0x08, 0x34, 0x64, 0x40, 0x7C, 0x06), None, None, None, None, None, None, "a blue crystal", item_id=5051),
    'Single Arrow': ItemData(IC.filler, None, 0x43, 'a lonely arrow\nsits here.', 'and the arrow', 'stick-collecting kid', 'sewing needle for sale', 'fungus for arrow', 'archer boy sews again', 'an arrow', item_id=5052),
    'Arrows (10)': ItemData(IC.filler, None, 0x44, 'This will give\nyou ten shots\nwith your bow!', 'and the arrow pack','stick-collecting kid', 'sewing kit for sale', 'fungus for arrows', 'archer boy sews again','ten arrows', 5053),
    'Arrow Upgrade (+10)': ItemData(IC.filler, None, 0x54, 'increase arrow\nstorage, low\nlow price', 'and the quiver', 'quiver-enlarging kid', 'arrow boost for sale', 'witch and more skewers', 'upgrade boy sews more again', 'arrow capacity', 5054),
    'Arrow Upgrade (+5)': ItemData(IC.filler, None, 0x53, 'increase arrow\nstorage, low\nlow price', 'and the quiver', 'quiver-enlarging kid', 'arrow boost for sale', 'witch and more skewers', 'upgrade boy sews more again', 'arrow capacity', 5055),
    'Single Bomb': ItemData(IC.filler, None, 0x27, 'I make things\ngo BOOM! But\njust once.', 'and the explosion', 'the bomb-holding kid', 'firecracker for sale', 'blend fungus into bomb', '\'splosion boy explodes again', 'a bomb', 5056),
    'Bombs (3)': ItemData(IC.filler, None, 0x28, 'I make things\ngo triple\nBOOM!!!', 'and the explosions', 'the bomb-holding kid', 'firecrackers for sale', 'blend fungus into bombs', '\'splosion boy explodes again', 'three bombs', 5057),
    'Bombs (10)': ItemData(IC.filler, None, 0x31, 'I make things\ngo BOOM! Ten\ntimes!', 'and the explosions', 'the bomb-holding kid', 'firecrackers for sale', 'blend fungus into bombs', '\'splosion boy explodes again', 'ten bombs', 5058),
    'Bomb Upgrade (+10)': ItemData(IC.filler, None, 0x52, 'increase bomb\nstorage, low\nlow price', 'and the bomb bag', 'boom-enlarging kid', 'bomb boost for sale', 'the shroom goes boom', 'upgrade boy explodes more again', 'bomb capacity', 5059),
    'Bomb Upgrade (+5)': ItemData(IC.filler, None, 0x51, 'increase bomb\nstorage, low\nlow price', 'and the bomb bag', 'boom-enlarging kid', 'bomb boost for sale', 'the shroom goes boom', 'upgrade boy explodes more again', 'bomb capacity', 5060),
    'Blue Mail': ItemData(IC.useful, None, 0x22, 'Now you\'re a\nblue elf!', 'and the banana hat', 'the protected kid', 'banana hat for sale', 'the clothing store', 'tailor boy banana hatted again', 'the Blue Mail', 5061),
    'Red Mail': ItemData(IC.useful, None, 0x23, 'Now you\'re a\nred elf!', 'and the eggplant hat', 'well-protected kid', 'purple hat for sale', 'the nice clothing store', 'tailor boy fears nothing again', 'the Red Mail', 5062),
    'Progressive Mail': ItemData(IC.useful, None, 0x60, 'time for a\nchange of\nclothes?', 'and the unknown hat', 'the protected kid', 'new hat for sale', 'the clothing store', 'tailor boy has threads again', 'some armor', 5063),
    'Blue Boomerang': ItemData(IC.progression, None, 0x0C, 'No matter what\nyou do, blue\nreturns to you', 'and the bluemarang', 'the bat-throwing kid', 'bent stick for sale', 'fungus for puma-stick', 'throwing boy plays fetch again', 'the Blue Boomerang', 5064),
    'Red Boomerang': ItemData(IC.filler, None, 0x2A, 'No matter what\nyou do, red\nreturns to you', 'and the badmarang', 'the bat-throwing kid', 'air foil for sale', 'fungus for return-stick', 'magical boy plays fetch again', 'the Red Boomerang', 5065),
    'Blue Shield': ItemData(IC.filler, None, 0x04, 'Now you can\ndefend against\npebbles!', 'and the stone blocker', 'shield-wielding kid', 'shield for sale', 'fungus for shield', 'shield boy defends again', 'the Blue Shield', 5066),
    'Red Shield': ItemData(IC.filler, None, 0x05, 'Now you can\ndefend against\nfireballs!', 'and the shot blocker', 'shield-wielding kid', 'fire shield for sale', 'fungus for fire shield', 'shield boy defends again', 'the Red Shield', 5067),
    'Mirror Shield': ItemData(IC.progression, None, 0x06, 'Now you can\ndefend against\nlasers!', 'and the laser blocker', 'shield-wielding kid', 'face shield for sale', 'fungus for face shield', 'shield boy defends again', 'the Mirror Shield', 5068),
    'Progressive Shield': ItemData(IC.progression, None, 0x5F, 'have a better\nblocker in\nfront of you', 'and the new shield', 'shield-wielding kid', 'shield for sale', 'fungus for shield', 'shield boy defends again', 'a shield', 5069),
    'Bug Catching Net': ItemData(IC.progression, None, 0x21, 'Let\'s catch\nsome bees and\nfaeries!', 'and the bee catcher', 'the bug-catching kid', 'stick web for sale', 'fungus for butterflies', 'wrong boy catches bees again', 'the Bug Net', 5070),
    'Cane of Byrna': ItemData(IC.progression, None, 0x18, 'Use this to\nbecome\ninvincible!', 'and the bad cane', 'the spark-making kid', 'spark stick for sale', 'spark-stick for trade', 'cane boy encircles again', 'the Blue Cane', 5071),
    'Boss Heart Container': ItemData(IC.filler, None, 0x3E, 'Maximum health\nincreased!\nYeah!', 'and the full heart', 'the life-giving kid', 'love for sale', 'fungus for life', 'life boy feels love again', 'a heart', 5072),
    'Sanctuary Heart Container': ItemData(IC.filler, None, 0x3F, 'Maximum health\nincreased!\nYeah!', 'and the full heart', 'the life-giving kid', 'love for sale', 'fungus for life', 'life boy feels love again', 'a heart', 5073),
    'Piece of Heart': ItemData(IC.filler, None, 0x17, 'Just a little\npiece of love!', 'and the broken heart', 'the life-giving kid', 'little love for sale', 'fungus for life', 'life boy feels some love again', 'a heart piece', 5074),
    'Rupee (1)': ItemData(IC.filler, None, 0x34, 'Just pocket\nchange. Move\nright along.', 'the pocket change', 'poverty-struck kid', 'life lesson for sale', 'buying cheap drugs', 'destitute boy has snack again', 'a green rupee', 5075),
    'Rupees (5)': ItemData(IC.filler, None, 0x35, 'Just pocket\nchange. Move\nright along.', 'the pocket change', 'poverty-struck kid', 'life lesson for sale', 'buying cheap drugs', 'destitute boy has snack again', 'a blue rupee', 5076),
    'Rupees (20)': ItemData(IC.filler, None, 0x36, 'Just couch\ncash. Move\nright along.', 'and the couch cash', 'the piggy-bank kid', 'life lesson for sale', 'the witch buying drugs', 'destitute boy has lunch again', 'a red rupee', 5077),
    'Rupees (50)': ItemData(IC.filler, None, 0x41, 'A rupee pile!\nOkay?', 'and the rupee pile', 'the well-off kid', 'life lesson for sale', 'buying okay drugs', 'destitute boy has dinner again', 'fifty rupees', 5078),
    'Rupees (100)': ItemData(IC.filler, None, 0x40, 'A rupee stash!\nHell yeah!', 'and the rupee stash', 'the kind-of-rich kid', 'life lesson for sale', 'buying good drugs', 'affluent boy goes drinking again', 'one hundred rupees', 5079),
    'Rupees (300)': ItemData(IC.filler, None, 0x46, 'A rupee hoard!\nHell yeah!', 'and the rupee hoard', 'the really-rich kid', 'life lesson for sale', 'buying the best drugs', 'fat-cat boy is rich again', 'three hundred rupees', 5080),
    'Rupoor': ItemData(IC.filler, None, 0x59, 'a debt collector', 'and the toll-booth', 'the toll-booth kid', 'double loss for sale', 'witch stole your rupees', 'affluent boy steals rupees', 'a rupoor', 5081),
    'Red Clock': ItemData(IC.filler, None, 0x5B, 'a waste of time', 'the ruby clock', 'the ruby-time kid', 'red time for sale', 'for ruby time', 'moment boy travels time again', 'a red clock', 5082),
    'Blue Clock': ItemData(IC.filler, None, 0x5C, 'a bit of time', 'the sapphire clock', 'sapphire-time kid', 'blue time for sale', 'for sapphire time', 'moment boy time travels again', 'a blue clock', 5083),
    'Green Clock': ItemData(IC.filler, None, 0x5D, 'a lot of time', 'the emerald clock', 'the emerald-time kid', 'green time for sale', 'for emerald time', 'moment boy adjusts time again', 'a red clock', 5084),
    'Single RNG': ItemData(IC.filler, None, 0x62, 'something you don\'t yet have', None, None, None, None, 'unknown boy somethings again', 'a new mystery', 5085),
    'Multi RNG': ItemData(IC.filler, None, 0x63, 'something you may already have', None, None, None, None, 'unknown boy somethings again', 'a total mystery', 5086),
    'Magic Upgrade (1/2)': ItemData(IC.progression, None, 0x4E, 'Your magic\npower has been\ndoubled!', 'and the spell power', 'the magic-saving kid', 'wizardry for sale', 'mekalekahi mekahiney ho', 'magic boy saves magic again', 'Half Magic', 5087),  # can be required to beat mothula in an open seed in very very rare circumstance
    'Magic Upgrade (1/4)': ItemData(IC.progression, None, 0x4F, 'Your magic\npower has been\nquadrupled!', 'and the spell power', 'the magic-saving kid', 'wizardry for sale', 'mekalekahi mekahiney ho', 'magic boy saves magic again', 'Quarter Magic', 5088),  # can be required to beat mothula in an open seed in very very rare circumstance
    'Small Key (Eastern Palace)': ItemData(IC.progression, 'SmallKey', 0xA2, 'A small key to Armos Knights', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Eastern Palace', 5089),
    'Big Key (Eastern Palace)': ItemData(IC.progression, 'BigKey', 0x9D, 'A big key to Armos Knights', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Eastern Palace', 5090),
    'Compass (Eastern Palace)': ItemData(IC.filler, 'Compass', 0x8D, 'Now you can find the Armos Knights!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Eastern Palace', 5091),
    'Map (Eastern Palace)': ItemData(IC.filler, 'Map', 0x7D, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Eastern Palace', 5092),
    'Small Key (Desert Palace)': ItemData(IC.progression, 'SmallKey', 0xA3, 'A small key to the desert', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Desert Palace', 5093),
    'Big Key (Desert Palace)': ItemData(IC.progression, 'BigKey', 0x9C, 'A big key to the desert', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Desert Palace', 5094),
    'Compass (Desert Palace)': ItemData(IC.filler, 'Compass', 0x8C, 'Now you can find Lanmolas!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Desert Palace', 5095),
    'Map (Desert Palace)': ItemData(IC.filler, 'Map', 0x7C, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Desert Palace', 5096),
    'Small Key (Tower of Hera)': ItemData(IC.progression, 'SmallKey', 0xAA, 'A small key to Hera', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Tower of Hera', 5097),
    'Big Key (Tower of Hera)': ItemData(IC.progression, 'BigKey', 0x95, 'A big key to Hera', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Tower of Hera', 5098),
    'Compass (Tower of Hera)': ItemData(IC.filler, 'Compass', 0x85, 'Now you can find Moldorm!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Tower of Hera', 5099),
    'Map (Tower of Hera)': ItemData(IC.filler, 'Map', 0x75, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Tower of Hera', 5100),
    'Small Key (Hyrule Castle)': ItemData(IC.progression, 'SmallKey', 0xA0, 'A small key to the castle', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Hyrule Castle', 5101),
    'Big Key (Hyrule Castle)': ItemData(IC.progression, 'BigKey', 0x9F, 'A big key to the castle', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Hyrule Castle', 5102),
    'Compass (Hyrule Castle)': ItemData(IC.filler, 'Compass', 0x8F, 'Now you can find no boss!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Hyrule Castle', 5103),
    'Map (Hyrule Castle)': ItemData(IC.filler, 'Map', 0x7F, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Hyrule Castle', 5104),
    'Small Key (Agahnims Tower)': ItemData(IC.progression, 'SmallKey', 0xA4, 'A small key to Agahnim', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Castle Tower', 5105),
    # doors-specific items, baserom will not be able to understand these
    'Big Key (Agahnims Tower)': ItemData(IC.progression, 'BigKey', 0x9B, 'A big key to Agahnim', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Castle Tower', 5106),
    'Compass (Agahnims Tower)': ItemData(IC.filler, 'Compass', 0x8B, 'Now you can find Aga1!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds null again', 'a compass to Castle Tower', 5107),
    'Map (Agahnims Tower)': ItemData(IC.filler, 'Map', 0x7B, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Castle Tower', 5108),
    # end of doors-specific items
    'Small Key (Palace of Darkness)': ItemData(IC.progression, 'SmallKey', 0xA6, 'A small key to darkness', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Palace of Darkness', 5109),
    'Big Key (Palace of Darkness)': ItemData(IC.progression, 'BigKey', 0x99, 'A big key to darkness', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Palace of Darkness', 5110),
    'Compass (Palace of Darkness)': ItemData(IC.filler, 'Compass', 0x89, 'Now you can find Helmasaur King!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Palace of Darkness', 5111),
    'Map (Palace of Darkness)': ItemData(IC.filler, 'Map', 0x79, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Palace of Darkness', 5112),
    'Small Key (Thieves Town)': ItemData(IC.progression, 'SmallKey', 0xAB, 'A small key to thievery', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Thieves\' Town', 5113),
    'Big Key (Thieves Town)': ItemData(IC.progression, 'BigKey', 0x94, 'A big key to thievery', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Thieves\' Town', 5114),
    'Compass (Thieves Town)': ItemData(IC.filler, 'Compass', 0x84, 'Now you can find Blind!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Thieves\' Town', 5115),
    'Map (Thieves Town)': ItemData(IC.filler, 'Map', 0x74, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Thieves\' Town', 5116),
    'Small Key (Skull Woods)': ItemData(IC.progression, 'SmallKey', 0xA8, 'A small key to the woods', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Skull Woods', 5117),
    'Big Key (Skull Woods)': ItemData(IC.progression, 'BigKey', 0x97, 'A big key to the woods', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Skull Woods', 5118),
    'Compass (Skull Woods)': ItemData(IC.filler, 'Compass', 0x87, 'Now you can find Mothula!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Skull Woods', 5119),
    'Map (Skull Woods)': ItemData(IC.filler, 'Map', 0x77, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Skull Woods', 5120),
    'Small Key (Swamp Palace)': ItemData(IC.progression, 'SmallKey', 0xA5, 'A small key to the swamp', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Swamp Palace', 5121),
    'Big Key (Swamp Palace)': ItemData(IC.progression, 'BigKey', 0x9A, 'A big key to the swamp', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Swamp Palace', 5122),
    'Compass (Swamp Palace)': ItemData(IC.filler, 'Compass', 0x8A, 'Now you can find Arrghus!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Swamp Palace', 5123),
    'Map (Swamp Palace)': ItemData(IC.filler, 'Map', 0x7A, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Swamp Palace', 5124),
    'Small Key (Ice Palace)': ItemData(IC.progression, 'SmallKey', 0xA9, 'A small key to the iceberg', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Ice Palace', 5125),
    'Big Key (Ice Palace)': ItemData(IC.progression, 'BigKey', 0x96, 'A big key to the iceberg', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Ice Palace', 5126),
    'Compass (Ice Palace)': ItemData(IC.filler, 'Compass', 0x86, 'Now you can find Kholdstare!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Ice Palace', 5127),
    'Map (Ice Palace)': ItemData(IC.filler, 'Map', 0x76, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Ice Palace', 5128),
    'Small Key (Misery Mire)': ItemData(IC.progression, 'SmallKey', 0xA7, 'A small key to the mire', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Misery Mire', 5129),
    'Big Key (Misery Mire)': ItemData(IC.progression, 'BigKey', 0x98, 'A big key to the mire', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Misery Mire', 5130),
    'Compass (Misery Mire)': ItemData(IC.filler, 'Compass', 0x88, 'Now you can find Vitreous!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Misery Mire', 5131),
    'Map (Misery Mire)': ItemData(IC.filler, 'Map', 0x78, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Misery Mire', 5132),
    'Small Key (Turtle Rock)': ItemData(IC.progression, 'SmallKey', 0xAC, 'A small key to the pipe maze', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Turtle Rock', 5133),
    'Big Key (Turtle Rock)': ItemData(IC.progression, 'BigKey', 0x93, 'A big key to the pipe maze', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Turtle Rock', 5134),
    'Compass (Turtle Rock)': ItemData(IC.filler, 'Compass', 0x83, 'Now you can find Trinexx!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Turtle Rock', 5135),
    'Map (Turtle Rock)': ItemData(IC.filler, 'Map', 0x73, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Turtle Rock', 5136),
    'Small Key (Ganons Tower)': ItemData(IC.progression, 'SmallKey', 0xAD, 'A small key to the evil tower', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key to Ganon\'s Tower', 5137),
    'Big Key (Ganons Tower)': ItemData(IC.progression, 'BigKey', 0x92, 'A big key to the evil tower', 'and the big key', 'the big-unlock kid', 'big key for sale', 'face key fungus', 'key boy opens chest again', 'a big key to Ganon\'s Tower', 5138),
    'Compass (Ganons Tower)': ItemData(IC.filler, 'Compass', 0x82, 'Now you can find Agahnim!', 'and the compass', 'the magnetic kid', 'compass for sale', 'magnetic fungus', 'compass boy finds boss again', 'a compass to Ganon\'s Tower', 5139),
    'Map (Ganons Tower)': ItemData(IC.filler, 'Map', 0x72, 'A tightly folded map rests here', 'and the map', 'cartography kid', 'map for sale', 'a map to shrooms', 'map boy navigates again', 'a map to Ganon\'s Tower', 5140),
    'Small Key (Universal)': ItemData(IC.filler, None, 0xAF, 'A small key for any door', 'and the key', 'the unlocking kid', 'keys for sale', 'unlock the fungus', 'key boy opens door again', 'a small key', 5141),
    'Nothing': ItemData(IC.trap, None, 0x5A, 'Some Hot Air', 'and the Nothing', 'the zen kid', 'outright theft', 'shroom theft', 'empty boy is bored again', 'nothing', 5142),
    'Bee Trap': ItemData(IC.trap, None, 0xB0, 'We will sting your face a whole lot!', 'and the sting buddies', 'the beekeeper kid', 'insects for sale', 'shroom pollenation', 'bottle boy has mad bees again', 'Friendship', 5143),
    'Faerie': ItemData(IC.filler, None, 0xB1, 'Save me and I will revive you', 'and the captive', 'the tingle kid','hostage for sale', 'fairy dust and shrooms', 'bottle boy has friend again', 'a faerie', 5144),
    'Good Bee': ItemData(IC.filler, None, 0xB2, 'Save me and I will sting you (sometimes)', 'and the captive', 'the tingle kid','hostage for sale', 'good dust and shrooms', 'bottle boy has friend again', 'a bee', 5145),
    'Magic Jar': ItemData(IC.filler, None, 0xB3, '', '', '','', '', '', '', 5146),
    'Apple': ItemData(IC.filler, None, 0xB4, '', '', '','', '', '', '', 5147),
     #   'Hint': ItemData(False, None, 0xB5, '', '', '','', '', '', ''),
     #   'Bomb Trap': ItemData(False, None, 0xB6, '', '', '','', '', '', ''),
    'Red Potion': ItemData(IC.filler, None, 0x2E, 'Hearty red goop!', 'and the red goo', 'the liquid kid', 'potion for sale', 'free samples', 'bottle boy has red goo again', 'a red potion', 5148),
    'Green Potion': ItemData(IC.filler, None, 0x2F, 'Refreshing green goop!', 'and the green goo', 'the liquid kid', 'potion for sale', 'free samples', 'bottle boy has green goo again', 'a green potion', 5149),
    'Blue Potion': ItemData(IC.filler, None, 0x30, 'Delicious blue goop!', 'and the blue goo', 'the liquid kid', 'potion for sale', 'free samples', 'bottle boy has blue goo again', 'a blue potion', 5150),
    'Bee': ItemData(IC.trap, None, 0x0E, 'I will sting your foes a few times', 'and the sting buddy', 'the beekeeper kid', 'insect for sale', 'shroom pollenation', 'bottle boy has mad bee again', 'a bee', 5151),
    'Small Heart': ItemData(IC.filler, None, 0x42, 'Just a little\npiece of love!', 'and the heart', 'the life-giving kid', 'little love for sale', 'fungus for life', 'life boy feels some love again', 'a heart', 5152),
    'Activated Flute': ItemData(IC.progression, None, 0x4A, 'Save the duck\nand fly to\nfreedom!', 'and the duck call', 'the duck-call kid', 'duck call for sale', 'duck-calls for trade', 'flute boy plays again', 'the Flute', 5153),
    'Beat Agahnim 1': ItemData(IC.progression, 'Event', None, None, None, None, None, None, None, None),
    'Beat Agahnim 2': ItemData(IC.progression, 'Event', None, None, None, None, None, None, None, None),
    'Get Frog': ItemData(IC.progression, 'Event', None, None, None, None, None, None, None, None),
    'Return Smith': ItemData(IC.progression, 'Event', None, None, None, None, None, None, None, None),
    'Pick Up Purple Chest': ItemData(IC.progression, 'Event', None, None, None, None, None, None, None, None),
    'Open Floodgate': ItemData(IC.progression, 'Event', None, None, None, None, None, None, None, None),
}

progression_mapping = {
    "Golden Sword": ("Progressive Sword", 4),
    "Tempered Sword": ("Progressive Sword", 3),
    "Master Sword": ("Progressive Sword", 2),
    "Fighter Sword": ("Progressive Sword", 1),
    "Titans Mitts": ("Progressive Glove", 2),
    "Power Glove": ("Progressive Glove", 1),
    "Blue Shield": ("Progressive Shield", 1),
    "Red Shield": ("Progressive Shield", 2),
    "Mirror Shield": ("Progressive Shield", 3),
    "Silver Bow": ("Progressive Bow", 2),
    "Bow": ("Progressive Bow", 1)
}

item_name_groups = {
    "Bows":
        {"Bow", "Silver Arrows", "Silver Bow", "Progressive Bow (Alt)", "Progressive Bow"},
    "Gloves":
        {"Power Glove", "Progressive Glove", "Titans Mitts"},
    "Medallions":
        {"Ether", "Bombos", "Quake"}
}

# generic groups, (Name, substring)
_simple_groups = {
    ("Swords", "Sword"),
    ("Shields", "Shield"),
    ("Mails", "Mail"),

    ("Boomerangs", "Boomerang"),

    ("Rods", "Rod"),
    ("Canes", "Cane"),

    ("Upgrades", "Upgrade"), # Capacity and Magic Upgrades

    ("Small Keys", "Small Key"),
    ("Big Keys", "Big Key"),
    ("Compasses", "Compass"),
    ("Maps", "Map"),

    ("Bottles", "Bottle"),
    ("Potions", "Potion"),

    ("Rupees", "Rupee"),
    ("Clocks", "Clock"),

    ("Crystals", "Crystal"),
    ("Pendants", "Pendant")
}

for basename, substring in _simple_groups:
    tempset = item_name_groups[basename] = set()
    for itemname in item_table:
        if substring in itemname:
            tempset.add(itemname)

del (_simple_groups)


everything = {name for name, data in item_table.items() if type(data.item_code) == int}
progression_items = {name for name in everything if
                     item_table[name].classification in {IC.progression, IC.progression_skip_balancing}}
item_name_groups['Progression Items'] = progression_items
item_name_groups['Non Progression Items'] = everything - progression_items

trap_replaceable = item_name_groups['Rupees'] | {'Arrows (10)', 'Single Bomb', 'Bombs (3)', 'Bombs (10)', 'Nothing'}

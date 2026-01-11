from enum import Enum

from .FFTRegion import FFTRegion
from .regions import Mandalia, Grog, Zirekile, BariausHill, Finath, Dolbodar, Fovoham, Bethla, \
    Zaland, BerveniaVolcano, Riovanes, Lenalia, Lesalia, Araguay, BariausValley, Sweegy, Yuguo, Bed, BerveniaCity, \
    Germinas, Zeklaus, Doguola, Poeskas, Zigolis, Dorter, Goug, Zeakden, Nelveska, DeepDungeon, Goland, Zeltennia


class MonsterNames(Enum):
    YELLOW_CHOCOBO = "Yellow Chocobo"
    BLACK_CHOCOBO = "Black Chocobo"
    RED_CHOCOBO = "Red Chocobo"

    GOBLIN = "Goblin"
    BLACK_GOBLIN = "Black Goblin"
    GOBBLEDEGUCK = "Gobbledeguck"

    RED_PANTHER = "Red Panther"
    CUAR = "Cuar"
    VAMPIRE = "Vampire"

    BOMB = "Bomb"
    GRENADE = "Grenade"
    EXPLOSIVE = "Explosive"

    SKELETON = "Skeleton"
    BONE_SNATCH = "Bone Snatch"
    LIVING_BONE = "Living Bone"

    GHOUL = "Ghoul"
    GUST = "Gust"
    REVNANT = "Revnant"

    FLOATIBALL = "Floatiball"
    AHRIMAN = "Ahriman"
    PLAGUE = "Plague"

    PISCO_DEMON = "Pisco Demon"
    SQUIDLARKIN = "Squidlarkin"
    MINDFLARE = "Mindflare"

    JURAVIS = "Juravis"
    STEEL_HAWK = "Steel Hawk"
    COCATORIS = "Cocatoris"

    BULL_DEMON = "Bull Demon"
    MINITAURUS = "Minitaurus"
    SACRED = "Sacred"

    MORBOL = "Morbol"
    OCHU = "Ochu"
    GREAT_MORBOL = "Great Morbol"

    WOODMAN = "Woodman"
    TRENT = "Trent"
    TAIJU = "Taiju"

    DRAGON = "Dragon"
    BLUE_DRAGON = "Blue Dragon"
    RED_DRAGON = "Red Dragon"

    BEHEMOTH = "Behemoth"
    KING_BEHEMOTH = "King Behemoth"
    DARK_BEHEMOTH = "Dark Behemoth"

    HYUDRA = "Hyudra"
    HYDRA = "Hydra"
    TIAMAT = "Tiamat"

    URIBO = "Uribo"
    PORKY = "Porky"
    WILDBOW = "Wildbow"

class MonsterFamilies(Enum):
    CHOCOBO = "Chocobo"
    GOBLIN = "Goblin"
    PANTHER = "Panther"
    BOMB = "Bomb"
    SKELETON = "Skeleton"
    GHOST = "Ghost"
    AHRIMAN = "Ahriman"
    MINDFLAYER = "Mindflayer"
    BIRD = "Bird"
    MINOTAUR = "Minotaur"
    MALBORO = "Malboro"
    TREANT = "Treant"
    DRAGON = "Dragon"
    BEHEMOTH = "Behemoth"
    HYDRA = "Hydra"
    PIG = "Pig"

monster_families: dict[MonsterFamilies, list[MonsterNames]] = {
    MonsterFamilies.CHOCOBO: [MonsterNames.YELLOW_CHOCOBO, MonsterNames.BLACK_CHOCOBO, MonsterNames.RED_CHOCOBO],
    MonsterFamilies.GOBLIN: [MonsterNames.GOBLIN, MonsterNames.BLACK_GOBLIN, MonsterNames.GOBBLEDEGUCK],
    MonsterFamilies.PANTHER: [MonsterNames.RED_PANTHER, MonsterNames.CUAR, MonsterNames.VAMPIRE],
    MonsterFamilies.BOMB: [MonsterNames.BOMB, MonsterNames.GRENADE, MonsterNames.EXPLOSIVE],
    MonsterFamilies.SKELETON: [MonsterNames.SKELETON, MonsterNames.BONE_SNATCH, MonsterNames.LIVING_BONE],
    MonsterFamilies.GHOST: [MonsterNames.GHOUL, MonsterNames.GUST, MonsterNames.REVNANT],
    MonsterFamilies.AHRIMAN: [MonsterNames.FLOATIBALL, MonsterNames.AHRIMAN, MonsterNames.PLAGUE],
    MonsterFamilies.MINDFLAYER: [MonsterNames.PISCO_DEMON, MonsterNames.SQUIDLARKIN, MonsterNames.MINDFLARE],
    MonsterFamilies.BIRD: [MonsterNames.JURAVIS, MonsterNames.STEEL_HAWK, MonsterNames.COCATORIS],
    MonsterFamilies.MINOTAUR: [MonsterNames.BULL_DEMON, MonsterNames.MINITAURUS, MonsterNames.SACRED],
    MonsterFamilies.MALBORO: [MonsterNames.MORBOL, MonsterNames.OCHU, MonsterNames.GREAT_MORBOL],
    MonsterFamilies.TREANT: [MonsterNames.WOODMAN, MonsterNames.TRENT, MonsterNames.TAIJU],
    MonsterFamilies.DRAGON: [MonsterNames.DRAGON, MonsterNames.BLUE_DRAGON, MonsterNames.RED_DRAGON],
    MonsterFamilies.BEHEMOTH: [MonsterNames.BEHEMOTH, MonsterNames.KING_BEHEMOTH, MonsterNames.DARK_BEHEMOTH],
    MonsterFamilies.HYDRA: [MonsterNames.HYUDRA, MonsterNames.HYDRA, MonsterNames.TIAMAT],
    MonsterFamilies.PIG: [MonsterNames.URIBO, MonsterNames.PORKY, MonsterNames.WILDBOW]
}

monster_family_lookup: dict[MonsterNames, MonsterFamilies] = {}

for family, monsters in monster_families.items():
    for monster in monsters:
        monster_family_lookup[monster] = family


class RegionAccessRequirement:
    access_regions: list[type[FFTRegion]]
    battle_level: int
    sidequest: bool

    def __init__(self, access_regions: list[type[FFTRegion]], battle_level: int, sidequest: bool = False):
        self.access_regions = access_regions
        self.battle_level = battle_level
        self.sidequest = sidequest

class MonsterRegion:
    monster_name: MonsterNames
    gallione_locations: list[RegionAccessRequirement] = []
    fovoham_locations: list[RegionAccessRequirement] = []
    lesalia_locations: list[RegionAccessRequirement] = []
    lionel_locations: list[RegionAccessRequirement] = []
    zeltennia_locations: list[RegionAccessRequirement] = []
    limberry_locations: list[RegionAccessRequirement] = []
    murond_locations: list[RegionAccessRequirement] = []
    compiled_requirements: list[RegionAccessRequirement] = []

    def __init__(self, name: MonsterNames):
        self.monster_name = name

yellow_chocobo = MonsterRegion(MonsterNames.YELLOW_CHOCOBO)
yellow_chocobo.gallione_locations = [RegionAccessRequirement([Mandalia], 0)]
yellow_chocobo.fovoham_locations = [RegionAccessRequirement([Grog], 0)]
yellow_chocobo.lesalia_locations = [RegionAccessRequirement([Zirekile], 0)]
yellow_chocobo.lionel_locations = [RegionAccessRequirement([BariausHill], 0)]
yellow_chocobo.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
yellow_chocobo.limberry_locations = [RegionAccessRequirement([Dolbodar], 9)]

black_chocobo = MonsterRegion(MonsterNames.BLACK_CHOCOBO)
black_chocobo.gallione_locations = [RegionAccessRequirement([Mandalia], 5)]
black_chocobo.fovoham_locations = [RegionAccessRequirement([Fovoham], 0)]
black_chocobo.lesalia_locations = [
    RegionAccessRequirement([Zirekile], 5),
    RegionAccessRequirement([Zirekile, Zaland], 0),
    RegionAccessRequirement([Zirekile, Bethla], 2),
    RegionAccessRequirement([BerveniaVolcano, Riovanes], 9)
]
black_chocobo.lionel_locations = [RegionAccessRequirement([BariausHill], 0)]
black_chocobo.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
black_chocobo.limberry_locations = [RegionAccessRequirement([Dolbodar], 9)]

red_chocobo = MonsterRegion(MonsterNames.RED_CHOCOBO)
red_chocobo.gallione_locations = [RegionAccessRequirement([Lenalia], 5)]
red_chocobo.fovoham_locations = [RegionAccessRequirement([Grog, Lesalia], 2)]
red_chocobo.lesalia_locations = [
    RegionAccessRequirement([Zirekile, Bethla], 5),
    RegionAccessRequirement([Zirekile, Zaland], 5),
    RegionAccessRequirement([BerveniaVolcano, Riovanes], 9)
]
red_chocobo.lionel_locations = [RegionAccessRequirement([BariausHill], 0)]
red_chocobo.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
red_chocobo.limberry_locations = [RegionAccessRequirement([Dolbodar], 9)]

goblin = MonsterRegion(MonsterNames.GOBLIN)
goblin.gallione_locations = [RegionAccessRequirement([Mandalia], 0)]
goblin.fovoham_locations = [
    RegionAccessRequirement([Fovoham, Lenalia], 0),
    RegionAccessRequirement([Grog, Lesalia], 5)
]
goblin.lesalia_locations = [RegionAccessRequirement([Araguay], 0)]
goblin.lionel_locations = [RegionAccessRequirement([BariausValley], 0)]
goblin.zeltennia_locations = [RegionAccessRequirement([Finath], 9)]
goblin.limberry_locations = [RegionAccessRequirement([Dolbodar], 0)]

black_goblin = MonsterRegion(MonsterNames.BLACK_GOBLIN)
black_goblin.gallione_locations = [RegionAccessRequirement([Sweegy], 0)]
black_goblin.fovoham_locations = [RegionAccessRequirement([Yuguo], 2)]
black_goblin.lesalia_locations = [RegionAccessRequirement([Araguay], 0)]
black_goblin.lionel_locations = [RegionAccessRequirement([BariausValley], 0)]
black_goblin.limberry_locations = [RegionAccessRequirement([Dolbodar], 0)]

gobbledeguck = MonsterRegion(MonsterNames.GOBBLEDEGUCK)
gobbledeguck.gallione_locations = [RegionAccessRequirement([Mandalia], 5)]
gobbledeguck.fovoham_locations = [RegionAccessRequirement([Yuguo], 5)]
gobbledeguck.lesalia_locations = [RegionAccessRequirement([Araguay], 8)]
gobbledeguck.lionel_locations = [RegionAccessRequirement([BariausValley], 2)]
gobbledeguck.limberry_locations = [RegionAccessRequirement([Dolbodar], 5)]

red_panther = MonsterRegion(MonsterNames.RED_PANTHER)
red_panther.gallione_locations = [RegionAccessRequirement([Mandalia], 0)]
red_panther.fovoham_locations = [RegionAccessRequirement([Grog], 0)]
red_panther.lesalia_locations = [RegionAccessRequirement([Araguay], 0)]
red_panther.lionel_locations = [RegionAccessRequirement([BariausValley], 0)]
red_panther.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
red_panther.limberry_locations = [RegionAccessRequirement([Bed], 5)]

cuar = MonsterRegion(MonsterNames.CUAR)
cuar.gallione_locations = [
    RegionAccessRequirement([Sweegy], 5),
    RegionAccessRequirement([Lenalia, Fovoham], 2),
]
cuar.fovoham_locations = [RegionAccessRequirement([Grog], 2)]
cuar.lesalia_locations = [RegionAccessRequirement([Araguay], 0)]
cuar.lionel_locations = [RegionAccessRequirement([BariausValley], 2)]
cuar.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
cuar.limberry_locations = [RegionAccessRequirement([Bed, BerveniaCity], 0)]

vampire = MonsterRegion(MonsterNames.VAMPIRE)
vampire.gallione_locations = [RegionAccessRequirement([Sweegy], 5)]
vampire.fovoham_locations = [RegionAccessRequirement([Yuguo], 5)]
vampire.lesalia_locations = [RegionAccessRequirement([Araguay], 5)]
vampire.lionel_locations = [RegionAccessRequirement([BariausValley], 2)]
vampire.zeltennia_locations = [RegionAccessRequirement([Germinas], 5)]
vampire.limberry_locations = [RegionAccessRequirement([Bed, BerveniaCity], 2)]

bomb = MonsterRegion(MonsterNames.BOMB)
bomb.gallione_locations = [RegionAccessRequirement([Sweegy], 0)]
bomb.fovoham_locations = [RegionAccessRequirement([Yuguo], 0)]
bomb.lesalia_locations = [RegionAccessRequirement([Zeklaus], 0)]
bomb.lionel_locations = [RegionAccessRequirement([BariausHill], 0)]
bomb.zeltennia_locations = [RegionAccessRequirement([Doguola], 5)]
bomb.limberry_locations = [RegionAccessRequirement([Poeskas], 0)]

grenade = MonsterRegion(MonsterNames.GRENADE)
grenade.gallione_locations = [RegionAccessRequirement([Mandalia], 5)]
grenade.fovoham_locations = [RegionAccessRequirement([Grog], 0)]
grenade.lesalia_locations = [RegionAccessRequirement([Zeklaus], 0)]
grenade.lionel_locations = [RegionAccessRequirement([BariausHill], 5)]
grenade.zeltennia_locations = [RegionAccessRequirement([Doguola, Grog], 5)]
grenade.limberry_locations = [RegionAccessRequirement([Poeskas], 0)]

explosive = MonsterRegion(MonsterNames.EXPLOSIVE)
explosive.gallione_locations = [RegionAccessRequirement([Sweegy], 8)]
explosive.fovoham_locations = [RegionAccessRequirement([Grog, Zeltennia], 5)]
explosive.lesalia_locations = [
    RegionAccessRequirement([BerveniaVolcano], 5),
    RegionAccessRequirement([BerveniaVolcano, Riovanes], 2)
]
explosive.lionel_locations = [RegionAccessRequirement([BariausHill], 5)]
explosive.zeltennia_locations = [RegionAccessRequirement([Doguola, Grog], 5)]
explosive.limberry_locations = [RegionAccessRequirement([Poeskas], 0)]

skeleton = MonsterRegion(MonsterNames.SKELETON)
skeleton.gallione_locations = [RegionAccessRequirement([Sweegy], 0)]
skeleton.fovoham_locations = [RegionAccessRequirement([Yuguo], 0)]
skeleton.lesalia_locations = [RegionAccessRequirement([Zeklaus, Dorter], 0)]
skeleton.lionel_locations = [RegionAccessRequirement([Zigolis], 0)]
skeleton.limberry_locations = [RegionAccessRequirement([Dolbodar], 0)]

bone_snatch = MonsterRegion(MonsterNames.BONE_SNATCH)
bone_snatch.gallione_locations = [RegionAccessRequirement([Sweegy], 5)]
bone_snatch.fovoham_locations = [RegionAccessRequirement([Yuguo], 0)]
bone_snatch.lesalia_locations = [RegionAccessRequirement([Araguay], 0)]
bone_snatch.lionel_locations = [RegionAccessRequirement([Zigolis], 0)]
bone_snatch.limberry_locations = [RegionAccessRequirement([Dolbodar], 0)]

living_bone = MonsterRegion(MonsterNames.LIVING_BONE)
living_bone.gallione_locations = [RegionAccessRequirement([Sweegy], 5)]
living_bone.lesalia_locations = [RegionAccessRequirement([BerveniaVolcano], 5)]
living_bone.lionel_locations = [RegionAccessRequirement([Zigolis, Goug], 5)]
living_bone.limberry_locations = [RegionAccessRequirement([Dolbodar], 2)]

ghoul = MonsterRegion(MonsterNames.GHOUL)
ghoul.fovoham_locations = [RegionAccessRequirement([Yuguo], 0)]
ghoul.lesalia_locations = [RegionAccessRequirement([Araguay, Dorter], 0)]
ghoul.lionel_locations = [RegionAccessRequirement([Zigolis], 0)]
ghoul.limberry_locations = [RegionAccessRequirement([Poeskas], 0)]

gust = MonsterRegion(MonsterNames.GUST)
gust.fovoham_locations = [RegionAccessRequirement([Yuguo], 0)]
gust.lesalia_locations = [RegionAccessRequirement([Araguay, Dorter], 2)]
gust.lionel_locations = [RegionAccessRequirement([Zigolis], 2)]
gust.limberry_locations = [RegionAccessRequirement([Poeskas], 0)]

revnant = MonsterRegion(MonsterNames.REVNANT)
revnant.fovoham_locations = [RegionAccessRequirement([Yuguo], 5)]
revnant.lesalia_locations = [RegionAccessRequirement([Araguay, Dorter], 5)]
revnant.lionel_locations = [RegionAccessRequirement([Zigolis], 5)]
revnant.limberry_locations = [RegionAccessRequirement([Poeskas], 2)]

floatiball = MonsterRegion(MonsterNames.FLOATIBALL)
floatiball.fovoham_locations = [RegionAccessRequirement([Fovoham], 0)]
floatiball.lesalia_locations = [RegionAccessRequirement([Zirekile], 0)]
floatiball.lionel_locations = [RegionAccessRequirement([Zigolis], 0)]
floatiball.limberry_locations = [RegionAccessRequirement([Bed], 0)]

ahriman = MonsterRegion(MonsterNames.AHRIMAN)
ahriman.fovoham_locations = [RegionAccessRequirement([Fovoham], 0)]
ahriman.lesalia_locations = [
    RegionAccessRequirement([Zirekile, Bethla], 2),
    RegionAccessRequirement([BerveniaVolcano, Riovanes], 0)
]
ahriman.lionel_locations = [RegionAccessRequirement([Zigolis, Goug], 2)]
ahriman.limberry_locations = [RegionAccessRequirement([Bed], 0)]

plague = MonsterRegion(MonsterNames.PLAGUE)
plague.fovoham_locations = [RegionAccessRequirement([Fovoham], 8)]
plague.lesalia_locations = [
    RegionAccessRequirement([BerveniaVolcano, Riovanes], 5),
    RegionAccessRequirement([Goland], 8, sidequest=True)
]
plague.lionel_locations = [RegionAccessRequirement([BariausValley], 9)]
plague.zeltennia_locations = [RegionAccessRequirement([Germinas], 5)]
plague.limberry_locations = [RegionAccessRequirement([Bed, BerveniaCity], 5)]

pisco_demon = MonsterRegion(MonsterNames.PISCO_DEMON)
pisco_demon.gallione_locations = [
    RegionAccessRequirement([Lenalia], 2),
    RegionAccessRequirement([Lenalia, Fovoham], 0)
]
pisco_demon.fovoham_locations = [RegionAccessRequirement([Fovoham], 0)]
pisco_demon.lesalia_locations = [RegionAccessRequirement([Zirekile], 0)]
pisco_demon.lionel_locations = [RegionAccessRequirement([BariausValley], 0)]
pisco_demon.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
pisco_demon.limberry_locations = [RegionAccessRequirement([Dolbodar], 0)]

squidlarkin = MonsterRegion(MonsterNames.SQUIDLARKIN)
squidlarkin.gallione_locations = [RegionAccessRequirement([Lenalia], 2)]
squidlarkin.fovoham_locations = [RegionAccessRequirement([Fovoham], 0)]
squidlarkin.lesalia_locations = [RegionAccessRequirement([Zirekile], 0)]
squidlarkin.lionel_locations = [RegionAccessRequirement([BariausValley], 0)]
squidlarkin.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
squidlarkin.limberry_locations = [RegionAccessRequirement([Dolbodar], 0)]

mindflare = MonsterRegion(MonsterNames.MINDFLARE)
mindflare.fovoham_locations = [RegionAccessRequirement([Fovoham], 2)]
mindflare.lesalia_locations = [RegionAccessRequirement([Zirekile, Zaland], 2)]
mindflare.lionel_locations = [RegionAccessRequirement([BariausValley], 2)]
mindflare.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
mindflare.limberry_locations = [RegionAccessRequirement([Dolbodar], 5)]

juravis = MonsterRegion(MonsterNames.JURAVIS)
juravis.fovoham_locations = [RegionAccessRequirement([Fovoham, Zeakden], 0)]
juravis.lesalia_locations = [RegionAccessRequirement([BerveniaVolcano], 0)]
juravis.lionel_locations = [RegionAccessRequirement([BariausValley], 2)]
juravis.zeltennia_locations = [RegionAccessRequirement([Germinas], 0)]

steel_hawk = MonsterRegion(MonsterNames.STEEL_HAWK)
steel_hawk.fovoham_locations = [RegionAccessRequirement([Fovoham, Zeakden], 2)]
steel_hawk.lesalia_locations = [RegionAccessRequirement([Zeklaus], 0)]
steel_hawk.lionel_locations = [RegionAccessRequirement([BariausValley], 2)]
steel_hawk.zeltennia_locations = [RegionAccessRequirement([Germinas], 0)]
steel_hawk.limberry_locations = [RegionAccessRequirement([Poeskas], 2)]

cocatoris = MonsterRegion(MonsterNames.COCATORIS)
cocatoris.fovoham_locations = [RegionAccessRequirement([Fovoham], 0)]
cocatoris.lesalia_locations = [RegionAccessRequirement([Zeklaus], 5)]
cocatoris.lionel_locations = [RegionAccessRequirement([BariausValley], 5)]
cocatoris.limberry_locations = [RegionAccessRequirement([Poeskas, Germinas], 2)]

bull_demon = MonsterRegion(MonsterNames.BULL_DEMON)
bull_demon.gallione_locations = [RegionAccessRequirement([Sweegy], 0)]
bull_demon.fovoham_locations = [
    RegionAccessRequirement([Fovoham], 5),
    RegionAccessRequirement([Fovoham, Zeakden], 0),
]
bull_demon.lesalia_locations = [RegionAccessRequirement([Zeklaus], 0)]
bull_demon.lionel_locations = [RegionAccessRequirement([BariausHill], 0)]
bull_demon.zeltennia_locations = [RegionAccessRequirement([Doguola], 0)]
bull_demon.limberry_locations = [RegionAccessRequirement([Dolbodar], 0)]

minitaurus = MonsterRegion(MonsterNames.MINITAURUS)
minitaurus.fovoham_locations = [RegionAccessRequirement([Fovoham], 5)]
minitaurus.lesalia_locations = [RegionAccessRequirement([Zeklaus], 5)]
minitaurus.lionel_locations = [RegionAccessRequirement([BariausValley], 2)]
minitaurus.zeltennia_locations = [RegionAccessRequirement([Germinas], 0)]
minitaurus.limberry_locations = [RegionAccessRequirement([Poeskas], 2)]

sacred = MonsterRegion(MonsterNames.SACRED)
sacred.fovoham_locations = [
    RegionAccessRequirement([Fovoham], 8),
    RegionAccessRequirement([Fovoham, Lenalia], 5)
]
sacred.lesalia_locations = [RegionAccessRequirement([Zeklaus], 5)]
sacred.lionel_locations = [RegionAccessRequirement([BariausHill], 5)]
sacred.limberry_locations = [RegionAccessRequirement([Dolbodar], 9)]

morbol = MonsterRegion(MonsterNames.MORBOL)
morbol.gallione_locations = [RegionAccessRequirement([Mandalia], 5)]
morbol.fovoham_locations = [RegionAccessRequirement([Fovoham], 2)]
morbol.lesalia_locations = [RegionAccessRequirement([Araguay], 2)]
morbol.lionel_locations = [RegionAccessRequirement([Zigolis], 0)]
morbol.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]
morbol.limberry_locations = [RegionAccessRequirement([Dolbodar], 0)]

ochu = MonsterRegion(MonsterNames.OCHU)
ochu.gallione_locations = [RegionAccessRequirement([Lenalia], 5)]
ochu.lesalia_locations = [RegionAccessRequirement([Araguay], 5)]
ochu.lionel_locations = [RegionAccessRequirement([Zigolis], 5)]
ochu.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]

great_morbol = MonsterRegion(MonsterNames.GREAT_MORBOL)
great_morbol.zeltennia_locations = [RegionAccessRequirement([Finath], 8)]

woodman = MonsterRegion(MonsterNames.WOODMAN)
woodman.gallione_locations = [RegionAccessRequirement([Sweegy], 5)]
woodman.fovoham_locations = [RegionAccessRequirement([Yuguo], 0)]
woodman.lesalia_locations = [RegionAccessRequirement([Araguay], 5)]
woodman.zeltennia_locations = [RegionAccessRequirement([Doguola], 2)]

trent = MonsterRegion(MonsterNames.TRENT)
trent.gallione_locations = [RegionAccessRequirement([Sweegy], 5)]
trent.fovoham_locations = [RegionAccessRequirement([Yuguo], 0)]
trent.lesalia_locations = [RegionAccessRequirement([Araguay], 2)]
trent.zeltennia_locations = [RegionAccessRequirement([Finath], 2)]

taiju = MonsterRegion(MonsterNames.TAIJU)
taiju.fovoham_locations = [RegionAccessRequirement([Yuguo], 5)]
taiju.lesalia_locations = [RegionAccessRequirement([Araguay], 5)]
taiju.zeltennia_locations = [RegionAccessRequirement([Finath], 8)]
taiju.murond_locations = [RegionAccessRequirement([DeepDungeon], 10, sidequest=True)]

dragon = MonsterRegion(MonsterNames.DRAGON)
dragon.gallione_locations = [RegionAccessRequirement([Lenalia], 0)]
dragon.lesalia_locations = [RegionAccessRequirement([Zeklaus], 5)]
dragon.lionel_locations = [RegionAccessRequirement([BariausHill], 9)]
dragon.zeltennia_locations = [RegionAccessRequirement([Germinas], 0)]
dragon.limberry_locations = [RegionAccessRequirement([Bed], 2)]

blue_dragon = MonsterRegion(MonsterNames.BLUE_DRAGON)
blue_dragon.gallione_locations = [RegionAccessRequirement([Mandalia], 9)]
blue_dragon.fovoham_locations = [RegionAccessRequirement([Grog], 0)]
blue_dragon.lionel_locations = [RegionAccessRequirement([BariausValley], 5)]
blue_dragon.zeltennia_locations = [RegionAccessRequirement([Finath], 8)]
blue_dragon.limberry_locations = [
    RegionAccessRequirement([Bed], 8),
    RegionAccessRequirement([Bed, BerveniaCity], 5)
]

red_dragon = MonsterRegion(MonsterNames.RED_DRAGON)
red_dragon.gallione_locations = [RegionAccessRequirement([Mandalia], 9)]
red_dragon.lesalia_locations = [RegionAccessRequirement([Zeklaus], 5)]
red_dragon.lionel_locations = [RegionAccessRequirement([BariausHill], 9)]
red_dragon.zeltennia_locations = [RegionAccessRequirement([Finath], 0)]

behemoth = MonsterRegion(MonsterNames.BEHEMOTH)
behemoth.lesalia_locations = [RegionAccessRequirement([BerveniaVolcano], 2)]
behemoth.lionel_locations = [RegionAccessRequirement([BariausValley], 5)]
behemoth.zeltennia_locations = [RegionAccessRequirement([Doguola], 0)]
behemoth.limberry_locations = [RegionAccessRequirement([Poeskas], 0)]

king_behemoth = MonsterRegion(MonsterNames.KING_BEHEMOTH)
king_behemoth.lesalia_locations = [RegionAccessRequirement([BerveniaVolcano, Riovanes], 9)]
king_behemoth.lionel_locations = [RegionAccessRequirement([BariausHill], 9)]
king_behemoth.limberry_locations = [
    RegionAccessRequirement([Poeskas, Germinas], 0),
    RegionAccessRequirement([Bed], 5)
]

dark_behemoth = MonsterRegion(MonsterNames.DARK_BEHEMOTH)
dark_behemoth.lionel_locations = [RegionAccessRequirement([BariausHill], 9)]
dark_behemoth.limberry_locations = [RegionAccessRequirement([Poeskas], 8)]

hyudra = MonsterRegion(MonsterNames.HYUDRA)
hyudra.lionel_locations = [RegionAccessRequirement([BariausHill], 9)]
hyudra.zeltennia_locations = [RegionAccessRequirement([Nelveska], 12, sidequest=True)]

hydra = MonsterRegion(MonsterNames.HYDRA)
hydra.lionel_locations = [RegionAccessRequirement([BariausHill], 9)]

tiamat = MonsterRegion(MonsterNames.TIAMAT)
tiamat.lionel_locations = [RegionAccessRequirement([BariausHill], 9)]

uribo = MonsterRegion(MonsterNames.URIBO)
uribo.lesalia_locations = [RegionAccessRequirement([Goland], 8, sidequest=True)]
uribo.lionel_locations = [RegionAccessRequirement([Zigolis], 6)]
uribo.zeltennia_locations = [RegionAccessRequirement([Finath], 12)]
uribo.limberry_locations = [RegionAccessRequirement([Dolbodar], 2)]

porky = MonsterRegion(MonsterNames.PORKY)
porky.limberry_locations = [RegionAccessRequirement([Dolbodar], 9)]

wildbow = MonsterRegion(MonsterNames.WILDBOW)

monster_locations = [
    yellow_chocobo, black_chocobo, red_chocobo,
    goblin, black_goblin, gobbledeguck,
    red_panther, cuar, vampire,
    bomb, grenade, explosive,
    skeleton, bone_snatch, living_bone,
    ghoul, gust, revnant,
    floatiball, ahriman, plague,
    pisco_demon, squidlarkin, mindflare,
    juravis, steel_hawk, cocatoris,
    bull_demon, minitaurus, sacred,
    morbol, ochu, great_morbol,
    woodman, trent, taiju,
    dragon, blue_dragon, red_dragon,
    behemoth, king_behemoth, dark_behemoth,
    hyudra, hydra, tiamat,
    uribo, porky, wildbow
]

monster_locations_lookup: dict[str, MonsterRegion] = {
    monster.monster_name.value: monster for monster in monster_locations
}

for monster in monster_locations:
    monster.compiled_requirements = [
        *monster.gallione_locations,
        *monster.fovoham_locations,
        *monster.lesalia_locations,
        *monster.lionel_locations,
        *monster.zeltennia_locations,
        *monster.limberry_locations,
        *monster.murond_locations
    ]
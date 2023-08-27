from typing import List, Tuple, Optional, Callable, NamedTuple
from BaseClasses import MultiWorld
from .LevelLogic import YoshiLogic
from .Options import get_option_value


class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    LevelID: int
    rule: Callable = lambda state: True


def get_locations(multiworld: Optional[MultiWorld], player: Optional[int], boss_order: Optional[list], luigi_pieces: Optional[int]) -> Tuple[LocationData, ...]:

    logic = YoshiLogic(multiworld, player, boss_order, luigi_pieces)

    location_table: List[LocationData] = [

    LocationData('1-1', 'Make Eggs, Throw Eggs: Red Coins', 0x305020, 0x00, lambda state: logic._11Coins(state)),
    LocationData('1-1', 'Make Eggs, Throw Eggs: Flowers', 0x305021, 0x00, lambda state: logic._11Flowers(state)),
    LocationData('1-1', 'Make Eggs, Throw Eggs: Stars', 0x305022, 0x00, lambda state: logic._11Stars(state)),
    LocationData('1-1', 'Make Eggs, Throw Eggs: Level Clear', 0x00, 0x305023, lambda state: logic._11Clear(state)),

    LocationData('1-2', 'Watch Out Below!: Red Coins', 0x305024, 0x01, lambda state: logic._12Coins(state)),
    LocationData('1-2', 'Watch Out Below!: Flowers', 0x305025, 0x01, lambda state: logic._12Flowers(state)),
    LocationData('1-2', 'Watch Out Below!: Stars', 0x305026, 0x01, lambda state: logic._12Stars(state)),
    LocationData('1-2', 'Watch Out Below!: Level Clear', 0x305027, 0x01, lambda state: logic._12Clear(state)),

    LocationData('1-3', 'The Cave Of Chomp Rock: Red Coins', 0x305028, 0x02, lambda state: logic._13Coins(state)),
    LocationData('1-3', 'The Cave Of Chomp Rock: Flowers', 0x305029, 0x02, lambda state: logic._13Flowers(state)),
    LocationData('1-3', 'The Cave Of Chomp Rock: Stars', 0x30502A, 0x02, lambda state: logic._13Stars(state)),
    LocationData('1-3', 'The Cave Of Chomp Rock: Level Clear', 0x30502B, 0x02, lambda state: logic._13Clear(state)),

    LocationData("1-4", "Burt The Bashful's Fort: Red Coins", 0x30502C, 0x03, lambda state: logic._14Coins(state)),
    LocationData("1-4", "Burt The Bashful's Fort: Flowers", 0x30502D, 0x03, lambda state: logic._14Flowers(state)),
    LocationData("1-4", "Burt The Bashful's Fort: Stars", 0x30502E, 0x03, lambda state: logic._14Stars(state)),
    LocationData("1-4", "Burt The Bashful's Fort: Level Clear", 0x30502F, 0x03, lambda state: logic._14CanFightBoss(state)),
    LocationData("Burt The Bashful's Boss Room", 'Burt The Bashful Defeated', None, lambda state: logic._14Boss(state)),

    LocationData("1-5", "Hop! Hop! Donut Lifts: Red Coins", 0x305031, 0x04, lambda state: logic._15Coins(state)),
    LocationData("1-5", "Hop! Hop! Donut Lifts: Flowers", 0x305032, 0x04, lambda state: logic._15Flowers(state)),
    LocationData("1-5", "Hop! Hop! Donut Lifts: Stars", 0x305033, 0x04, lambda state: logic._15Stars(state)),
    LocationData("1-5", "Hop! Hop! Donut Lifts: Level Clear", 0x305034, 0x04, lambda state: logic._15Clear(state)),

    LocationData("1-6", "Shy-Guys On Stilts: Red Coins", 0x305035, 0x05, lambda state: logic._16Coins(state)),
    LocationData("1-6", "Shy-Guys On Stilts: Flowers", 0x305036, 0x05, lambda state: logic._16Flowers(state)),
    LocationData("1-6", "Shy-Guys On Stilts: Stars", 0x305037, 0x05, lambda state: logic._16Stars(state)),
    LocationData("1-6", "Shy-Guys On Stilts: Level Clear", 0x305038, 0x05, lambda state: logic._16Clear(state)),

    LocationData("1-7", "Touch Fuzzy Get Dizzy: Red Coins", 0x305039, 0x06, lambda state: logic._17Coins(state)),
    LocationData("1-7", "Touch Fuzzy Get Dizzy: Flowers", 0x30503A, 0x06, lambda state: logic._17Flowers(state)),
    LocationData("1-7", "Touch Fuzzy Get Dizzy: Stars", 0x30503B, 0x06, lambda state: logic._17Stars(state)),
    LocationData("1-7", "Touch Fuzzy Get Dizzy: Level Clear", 0x30503C, 0x06, lambda state: logic._17Clear(state)),
    LocationData("1-7", 'Touch Fuzzy Get Dizzy: Gather Coins', None, lambda state: logic._17Game(state)),

    LocationData("1-8", "Salvo The Slime's Castle: Red Coins", 0x30503D, 0x07, lambda state: logic._18Coins(state)),
    LocationData("1-8", "Salvo The Slime's Castle: Flowers", 0x30503E, 0x07, lambda state: logic._18Flowers(state)),
    LocationData("1-8", "Salvo The Slime's Castle: Stars", 0x30503F, 0x07, lambda state: logic._18Stars(state)),
    LocationData("1-8", "Salvo The Slime's Castle: Level Clear", 0x305040, 0x07, lambda state: logic._18CanFightBoss(state)),
    LocationData("Salvo The Slime's Boss Room", 'Salvo The Slime Defeated', None, lambda state: logic._18Boss(state)),

    LocationData("Flip Cards", 'Flip Cards', None, 0x09),
    ############################################################################################
    LocationData("2-1", "Visit Koopa And Para-Koopa: Red Coins", 0x305041, 0x0C, lambda state: logic._21Coins(state)),
    LocationData("2-1", "Visit Koopa And Para-Koopa: Flowers", 0x305042, 0x0C, lambda state: logic._21Flowers(state)),
    LocationData("2-1", "Visit Koopa And Para-Koopa: Stars", 0x305043, 0x0C, lambda state: logic._21Stars(state)),
    LocationData("2-1", "Visit Koopa And Para-Koopa: Level Clear", 0x305044, 0x0C, lambda state: logic._21Clear(state)),

    LocationData("2-2", "The Baseball Boys: Red Coins", 0x305045, 0x0D, lambda state: logic._22Coins(state)),
    LocationData("2-2", "The Baseball Boys: Flowers", 0x305046, 0x0D, lambda state: logic._22Flowers(state)),
    LocationData("2-2", "The Baseball Boys: Stars", 0x305047, 0x0D, lambda state: logic._22Stars(state)),
    LocationData("2-2", "The Baseball Boys: Level Clear", 0x305048, 0x0D, lambda state: logic._22Clear(state)),

    LocationData("2-3", "What's Gusty Taste Like?: Red Coins", 0x305049, 0x0E, lambda state: logic._23Coins(state)),
    LocationData("2-3", "What's Gusty Taste Like?: Flowers", 0x30504A, 0x0E, lambda state: logic._23Flowers(state)),
    LocationData("2-3", "What's Gusty Taste Like?: Stars", 0x30504B, 0x0E, lambda state: logic._23Stars(state)),
    LocationData("2-3", "What's Gusty Taste Like?: Level Clear", 0x30504C, 0x0E, lambda state: logic._23Clear(state)),

    LocationData("2-4", "Bigger Boo's Fort: Red Coins", 0x30504D, 0x0F, lambda state: logic._24Coins(state)),
    LocationData("2-4", "Bigger Boo's Fort: Flowers", 0x30504E, 0x0F, lambda state: logic._24Flowers(state)),
    LocationData("2-4", "Bigger Boo's Fort: Stars", 0x30504F, 0x0F, lambda state: logic._24Stars(state)),
    LocationData("2-4", "Bigger Boo's Fort: Level Clear", 0x305050, 0x0F, lambda state: logic._24CanFightBoss(state)),
    LocationData("Bigger Boo's Boss Room", 'Bigger Boo Defeated', None, lambda state: logic._24Boss(state)),

    LocationData("2-5", "Watch Out For Lakitu: Red Coins", 0x305051, 0x10, lambda state: logic._25Coins(state)),
    LocationData("2-5", "Watch Out For Lakitu: Flowers", 0x305052, 0x10, lambda state: logic._25Flowers(state)),
    LocationData("2-5", "Watch Out For Lakitu: Stars", 0x305053, 0x10, lambda state: logic._25Stars(state)),
    LocationData("2-5", "Watch Out For Lakitu: Level Clear", 0x305054, 0x10, lambda state: logic._25Clear(state)),

    LocationData("2-6", "The Cave Of The Mystery Maze: Red Coins", 0x305055, 0x11, lambda state: logic._26Coins(state)),
    LocationData("2-6", "The Cave Of The Mystery Maze: Flowers", 0x305056, 0x11, lambda state: logic._26Flowers(state)),
    LocationData("2-6", "The Cave Of The Mystery Maze: Stars", 0x305057, 0x11, lambda state: logic._26Stars(state)),
    LocationData("2-6", "The Cave Of The Mystery Maze: Level Clear", 0x305058, 0x11, lambda state: logic._26Clear(state)),
    LocationData("2-6", 'The Cave Of the Mystery Maze: Seed Spitting Contest', None, lambda state: logic._26Game(state)),

    LocationData("2-7", "Lakitu's Wall: Red Coins", 0x305059, 0x12, lambda state: logic._27Coins(state)),
    LocationData("2-7", "Lakitu's Wall: Flowers", 0x30505A, 0x12, lambda state: logic._27Flowers(state)),
    LocationData("2-7", "Lakitu's Wall: Stars", 0x30505B, 0x12, lambda state: logic._27Stars(state)),
    LocationData("2-7", "Lakitu's Wall: Level Clear", 0x30505C, 0x12, lambda state: logic._27Clear(state)),
    LocationData("2-7", "Lakitu's Wall: Gather Coins", None, lambda state: logic._27Game(state)),

    LocationData("2-8", "The Potted Ghost's Castle: Red Coins", 0x30505D, 0x13, lambda state: logic._28Coins(state)),
    LocationData("2-8", "The Potted Ghost's Castle: Flowers", 0x30505E, 0x13, lambda state: logic._28Flowers(state)),
    LocationData("2-8", "The Potted Ghost's Castle: Stars", 0x30505F, 0x13, lambda state: logic._28Stars(state)),
    LocationData("2-8", "The Potted Ghost's Castle: Level Clear", 0x305060, 0x13, lambda state: logic._28CanFightBoss(state)),
    LocationData("Roger The Ghost's Boss Room", 'Roger The Ghost Defeated', None, lambda state: logic._28Boss(state)),
    ###############################################################################################
    LocationData("3-1", "Welcome To Monkey World!: Red Coins", 0x305061, 0x18, lambda state: logic._31Coins(state)),
    LocationData("3-1", "Welcome To Monkey World!: Flowers", 0x305062, 0x18, lambda state: logic._31Flowers(state)),
    LocationData("3-1", "Welcome To Monkey World!: Stars", 0x305063, 0x18, lambda state: logic._31Stars(state)),
    LocationData("3-1", "Welcome To Monkey World!: Level Clear", 0x305064, 0x18, lambda state: logic._31Clear(state)),

    LocationData("3-2", "Jungle Rhythm...: Red Coins", 0x305065, 0x19, lambda state: logic._32Coins(state)),
    LocationData("3-2", "Jungle Rhythm...: Flowers", 0x305066, 0x19, lambda state: logic._32Flowers(state)),
    LocationData("3-2", "Jungle Rhythm...: Stars", 0x305067, 0x19, lambda state: logic._32Stars(state)),
    LocationData("3-2", "Jungle Rhythm...: Level Clear", 0x305068, 0x19, lambda state: logic._32Clear(state)),

    LocationData("3-3", "Nep-Enuts' Domain: Red Coins", 0x305069, 0x1A, lambda state: logic._33Coins(state)),
    LocationData("3-2", "Nep-Enuts' Domain: Flowers", 0x30506A, 0x1A, lambda state: logic._33Flowers(state)),
    LocationData("3-2", "Nep-Enuts' Domain: Stars", 0x30506B, 0x1A, lambda state: logic._33Stars(state)),
    LocationData("3-2", "Nep-Enuts' Domain: Level Clear", 0x30506C, 0x1A, lambda state: logic._33Clear(state)),

    LocationData("3-4", "Prince Froggy's Fort: Red Coins", 0x30506D, 0x1B, lambda state: logic._34Coins(state)),
    LocationData("3-4", "Prince Froggy's Fort: Flowers", 0x30506E, 0x1B, lambda state: logic._34Flowers(state)),
    LocationData("3-4", "Prince Froggy's Fort: Stars", 0x30506F, 0x1B, lambda state: logic._34Stars(state)),
    LocationData("3-4", "Prince Froggy's Fort: Level Clear", 0x305070, 0x1B, lambda state: logic._34CanFightBoss(state)),
    LocationData("Prince Froggy's Boss Room", 'Prince Froggy Defeated', None, lambda state: logic._34Boss(state)),

    LocationData("3-5", "Jammin' Through The Trees: Red Coins", 0x305071, 0x1C, lambda state: logic._35Coins(state)),
    LocationData("3-5", "Jammin' Through The Trees: Flowers", 0x305072, 0x1C, lambda state: logic._35Flowers(state)),
    LocationData("3-5", "Jammin' Through The Trees: Stars", 0x305073, 0x1C, lambda state: logic._35Stars(state)),
    LocationData("3-5", "Jammin' Through The Trees: Level Clear", 0x305074, 0x1C, lambda state: logic._35Clear(state)),

    LocationData("3-6", "The Cave Of Harry Hedgehog: Red Coins", 0x305075, 0x1D, lambda state: logic._36Coins(state)),
    LocationData("3-6", "The Cave Of Harry Hedgehog: Flowers", 0x305076, 0x1D, lambda state: logic._36Flowers(state)),
    LocationData("3-6", "The Cave Of Harry Hedgehog: Stars", 0x305077, 0x1D, lambda state: logic._36Stars(state)),
    LocationData("3-6", "The Cave Of Harry Hedgehog: Level Clear", 0x305078, 0x1D, lambda state: logic._36Clear(state)),

    LocationData("3-7", "Monkeys' Favorite Lake: Red Coins", 0x305079, 0x1E, lambda state: logic._37Coins(state)),
    LocationData("3-7", "Monkeys' Favorite Lake: Flowers", 0x30507A, 0x1E, lambda state: logic._37Flowers(state)),
    LocationData("3-7", "Monkeys' Favorite Lake: Stars", 0x30507B, 0x1E, lambda state: logic._37Stars(state)),
    LocationData("3-7", "Monkeys' Favorite Lake: Level Clear", 0x30507C, 0x1E, lambda state: logic._37Clear(state)),

    LocationData("3-8", "Naval Piranha's Castle: Red Coins", 0x30507D, 0x1F, lambda state: logic._38Coins(state)),
    LocationData("3-8", "Naval Piranha's Castle: Flowers", 0x30507E, 0x1F, lambda state: logic._38Flowers(state)),
    LocationData("3-8", "Naval Piranha's Castle: Stars", 0x30507F, 0x1F, lambda state: logic._38Stars(state)),
    LocationData("3-8", "Naval Piranha's Castle: Level Clear", 0x305080, 0x1F, lambda state: logic._38CanFightBoss(state)),
    LocationData("Naval Piranha's Boss Room", 'Naval Piranha Defeated', None, lambda state: logic._38Boss(state)),

    LocationData("Drawing Lots", 'Drawing Lots', None, 0x21),
    ##############################################################################################
    LocationData("4-1", "GO! GO! MARIO!!: Red Coins", 0x305081, 0x24, lambda state: logic._41Coins(state)),
    LocationData("4-1", "GO! GO! MARIO!!: Flowers", 0x305082, 0x24, lambda state: logic._41Flowers(state)),
    LocationData("4-1", "GO! GO! MARIO!!: Stars", 0x305083, 0x24, lambda state: logic._41Stars(state)),
    LocationData("4-1", "GO! GO! MARIO!!: Level Clear", 0x305084, 0x24, lambda state: logic._41Clear(state)),

    LocationData("4-2", "The Cave Of The Lakitus: Red Coins", 0x305085, 0x25, lambda state: logic._42Coins(state)),
    LocationData("4-2", "The Cave Of The Lakitus: Flowers", 0x305086, 0x25, lambda state: logic._42Flowers(state)),
    LocationData("4-2", "The Cave Of The Lakitus: Stars", 0x305087, 0x25, lambda state: logic._42Stars(state)),
    LocationData("4-2", "The Cave Of The Lakitus: Level Clear", 0x305088, 0x25, lambda state: logic._42Clear(state)),

    LocationData("4-3", "Don't Look Back!: Red Coins", 0x305089, 0x26, lambda state: logic._43Coins(state)),
    LocationData("4-3", "Don't Look Back!: Flowers", 0x30508A, 0x26, lambda state: logic._43Flowers(state)),
    LocationData("4-3", "Don't Look Back!: Stars", 0x30508B, 0x26, lambda state: logic._43Stars(state)),
    LocationData("4-3", "Don't Look Back!: Level Clear", 0x30508C, 0x26, lambda state: logic._43Clear(state)),

    LocationData("4-4", "Marching Milde's Fort: Red Coins", 0x30508D, 0x27, lambda state: logic._44Coins(state)),
    LocationData("4-4", "Marching Milde's Fort: Flowers", 0x30508E, 0x27, lambda state: logic._44Flowers(state)),
    LocationData("4-4", "Marching Milde's Fort: Stars", 0x30508F, 0x27, lambda state: logic._44Stars(state)),
    LocationData("4-4", "Marching Milde's Fort: Level Clear", 0x305090, 0x27, lambda state: logic._44CanFightBoss(state)),
    LocationData("Marching Milde's Boss Room", 'Marching Milde Defeated', None, lambda state: logic._44Boss(state)),

    LocationData("4-5", "Chomp Rock Zone: Red Coins", 0x305091, 0x28, lambda state: logic._45Coins(state)),
    LocationData("4-5", "Chomp Rock Zone: Flowers", 0x305092, 0x28, lambda state: logic._45Flowers(state)),
    LocationData("4-5", "Chomp Rock Zone: Stars", 0x305093, 0x28, lambda state: logic._45Stars(state)),
    LocationData("4-5", "Chomp Rock Zone: Level Clear", 0x305094, 0x28, lambda state: logic._45Clear(state)),

    LocationData("4-6", "Lake Shore Paradise: Red Coins", 0x305095, 0x29, lambda state: logic._46Coins(state)),
    LocationData("4-6", "Lake Shore Paradise: Flowers", 0x305096, 0x29, lambda state: logic._46Flowers(state)),
    LocationData("4-6", "Lake Shore Paradise: Stars", 0x305097, 0x29, lambda state: logic._46Stars(state)),
    LocationData("4-6", "Lake Shore Paradise: Level Clear", 0x305098, 0x29, lambda state: logic._46Clear(state)),

    LocationData("4-7", "Ride Like The Wind: Red Coins", 0x305099, 0x2A, lambda state: logic._47Coins(state)),
    LocationData("4-7", "Ride Like The Wind: Flowers", 0x30509A, 0x2A, lambda state: logic._47Flowers(state)),
    LocationData("4-7", "Ride Like The Wind: Stars", 0x30509B, 0x2A, lambda state: logic._47Stars(state)),
    LocationData("4-7", "Ride Like The Wind: Level Clear", 0x30509C, 0x2A, lambda state: logic._47Clear(state)),
    LocationData("4-7", 'Ride Like The Wind: Gather Coins', None, lambda state: logic._47Game(state)),

    LocationData("4-8", "Hookbill The Koopa's Castle: Red Coins", 0x30509D, 0x2B, lambda state: logic._48Coins(state)),
    LocationData("4-8", "Hookbill The Koopa's Castle: Flowers", 0x30509E, 0x2B, lambda state: logic._48Flowers(state)),
    LocationData("4-8", "Hookbill The Koopa's Castle: Stars", 0x30509F, 0x2B, lambda state: logic._48Stars(state)),
    LocationData("4-8", "Hookbill The Koopa's Castle: Level Clear", 0x3050A0, 0x2B, lambda state: logic._48CanFightBoss(state)),
    LocationData("Hookbill The Koopa's Boss Room", 'Hookbill The Koopa Defeated', None, lambda state: logic._48Boss(state)),

    LocationData("Match Cards", 'Match Cards', None, 0x2D),
    ######################################################################################################
    LocationData("5-1", "BLIZZARD!!!: Red Coins", 0x3050A1, 0x30, lambda state: logic._51Coins(state)),
    LocationData("5-1", "BLIZZARD!!!: Flowers", 0x3050A2, 0x30, lambda state: logic._51Flowers(state)),
    LocationData("5-1", "BLIZZARD!!!: Stars", 0x3050A3, 0x30, lambda state: logic._51Stars(state)),
    LocationData("5-1", "BLIZZARD!!!: Level Clear", 0x3050A4, 0x30, lambda state: logic._51Clear(state)),

    LocationData("5-2", "Ride The Ski Lifts: Red Coins", 0x3050A5, 0x31, lambda state: logic._52Coins(state)),
    LocationData("5-2", "Ride The Ski Lifts: Flowers", 0x3050A6, 0x31, lambda state: logic._52Flowers(state)),
    LocationData("5-2", "Ride The Ski Lifts: Stars", 0x3050A7, 0x31, lambda state: logic._52Stars(state)),
    LocationData("5-2", "Ride The Ski Lifts: Level Clear", 0x3050A8, 0x31, lambda state: logic._52Clear(state)),

    LocationData("5-3", "Danger - Icy Conditions Ahead: Red Coins", 0x3050A9, 0x32, lambda state: logic._53Coins(state)),
    LocationData("5-3", "Danger - Icy Conditions Ahead: Flowers", 0x3050AA, 0x32, lambda state: logic._53Flowers(state)),
    LocationData("5-3", "Danger - Icy Conditions Ahead: Stars", 0x3050AB, 0x32, lambda state: logic._53Stars(state)),
    LocationData("5-3", "Danger - Icy Conditions Ahead: Level Clear", 0x3050AC, 0x32, lambda state: logic._53Clear(state)),

    LocationData("5-4", "Sluggy The Unshaven's Fort: Red Coins", 0x3050AD, 0x33, lambda state: logic._54Coins(state)),
    LocationData("5-4", "Sluggy The Unshaven's Fort: Flowers", 0x3050AE, 0x33, lambda state: logic._54Flowers(state)),
    LocationData("5-4", "Sluggy The Unshaven's Fort: Stars", 0x3050AF, 0x33, lambda state: logic._54Stars(state)),
    LocationData("5-4", "Sluggy The Unshaven's Fort: Level Clear", 0x3050B0, 0x33, lambda state: logic._54CanFightBoss(state)),
    LocationData("Sluggy The Unshaven's Boss Room", 'Sluggy The Unshaven Defeated', None, lambda state: logic._54Boss(state)),

    LocationData("5-5", "Goonie Rides!: Red Coins", 0x3050B1, 0x34, lambda state: logic._55Coins(state)),
    LocationData("5-5", "Goonie Rides!: Flowers", 0x3050B2, 0x34, lambda state: logic._55Flowers(state)),
    LocationData("5-5", "Goonie Rides!: Stars", 0x3050B3, 0x34, lambda state: logic._55Stars(state)),
    LocationData("5-5", "Goonie Rides!: Level Clear", 0x3050B4, 0x34, lambda state: logic._55Clear(state)),

    LocationData("5-6", "Welcome To Cloud World: Red Coins", 0x3050B5, 0x35, lambda state: logic._56Coins(state)),
    LocationData("5-6", "Welcome To Cloud World: Flowers", 0x3050B6, 0x35, lambda state: logic._56Flowers(state)),
    LocationData("5-6", "Welcome To Cloud World: Stars", 0x3050B7, 0x35, lambda state: logic._56Stars(state)),
    LocationData("5-6", "Welcome To Cloud World: Level Clear", 0x3050B8, 0x35, lambda state: logic._56Clear(state)),

    LocationData("5-7", "Shifting Platforms Ahead: Red Coins", 0x3050B9, 0x36, lambda state: logic._57Coins(state)),
    LocationData("5-7", "Shifting Platforms Ahead: Flowers", 0x3050BA, 0x36, lambda state: logic._57Flowers(state)),
    LocationData("5-7", "Shifting Platforms Ahead: Stars", 0x3050BB, 0x36, lambda state: logic._57Stars(state)),
    LocationData("5-7", "Shifting Platforms Ahead: Level Clear", 0x3050BC, 0x36, lambda state: logic._57Clear(state)),

    LocationData("5-8", "Raphael The Raven's Castle: Red Coins", 0x3050BD, 0x37, lambda state: logic._58Coins(state)),
    LocationData("5-8", "Raphael The Raven's Castle: Flowers", 0x3050BE, 0x37, lambda state: logic._58Flowers(state)),
    LocationData("5-8", "Raphael The Raven's Castle: Stars", 0x3050BF, 0x37, lambda state: logic._58Stars(state)),
    LocationData("5-8", "Raphael The Raven's Castle: Level Clear", 0x3050C0, 0x37, lambda state: logic._58CanFightBoss(state)),
    LocationData("Raphael The Raven's Boss Room", 'Raphael The Raven Defeated', None, lambda state: logic._58Boss(state)),
    ######################################################################################################

    LocationData("6-1", "Scary Skeleton Goonies!: Red Coins", 0x3050C1, 0x3C, lambda state: logic._61Coins(state)),
    LocationData("6-1", "Scary Skeleton Goonies!: Flowers", 0x3050C2, 0x3C, lambda state: logic._61Flowers(state)),
    LocationData("6-1", "Scary Skeleton Goonies!: Stars", 0x3050C3, 0x3C, lambda state: logic._61Stars(state)),
    LocationData("6-1", "Scary Skeleton Goonies!: Level Clear", 0x3050C4, 0x3C, lambda state: logic._61Clear(state)),

    LocationData("6-2", "The Cave Of The Bandits: Red Coins", 0x3050C5, 0x3D, lambda state: logic._62Coins(state)),
    LocationData("6-2", "The Cave Of The Bandits: Flowers", 0x3050C6, 0x3D, lambda state: logic._62Flowers(state)),
    LocationData("6-2", "The Cave Of The Bandits: Stars", 0x3050C7, 0x3D, lambda state: logic._62Stars(state)),
    LocationData("6-2", "The Cave Of The Bandits: Level Clear", 0x3050C8, 0x3D, lambda state: logic._62Clear(state)),

    LocationData("6-3", "Beware The Spinning Logs: Red Coins", 0x3050C9, 0x3E, lambda state: logic._63Coins(state)),
    LocationData("6-3", "Beware The Spinning Logs: Flowers", 0x3050CA, 0x3E, lambda state: logic._63Flowers(state)),
    LocationData("6-3", "Beware The Spinning Logs: Stars", 0x3050CB, 0x3E, lambda state: logic._63Stars(state)),
    LocationData("6-3", "Beware The Spinning Logs: Level Clear", 0x3050CC, 0x3E, lambda state: logic._63Clear(state)),

    LocationData("6-4", "Tap-Tap The Red Nose's Fort: Red Coins", 0x3050CD, 0x3F, lambda state: logic._64Coins(state)),
    LocationData("6-4", "Tap-Tap The Red Nose's Fort: Flowers", 0x3050CE, 0x3F, lambda state: logic._64Flowers(state)),
    LocationData("6-4", "Tap-Tap The Red Nose's Fort: Stars", 0x3050CF, 0x3F, lambda state: logic._64Stars(state)),
    LocationData("6-4", "Tap-Tap The Red Nose's Fort: Level Clear", 0x3050D0, 0x3F, lambda state: logic._64CanFightBoss(state)),
    LocationData("Tap-Tap The Red Nose's Boss Room", 'Tap-Tap The Red Nose Defeated', None, lambda state: logic._64Boss(state)),

    LocationData("6-5", "The Very Loooooong Cave: Red Coins", 0x3050D1, 0x40, lambda state: logic._65Coins(state)),
    LocationData("6-5", "The Very Loooooong Cave: Flowers", 0x3050D2, 0x40, lambda state: logic._65Flowers(state)),
    LocationData("6-5", "The Very Loooooong Cave: Stars", 0x3050D3, 0x40, lambda state: logic._65Stars(state)),
    LocationData("6-5", "The Very Loooooong Cave: Level Clear", 0x3050D4, 0x40, lambda state: logic._65Clear(state)),

    LocationData("6-6", "The Deep, Underground Maze: Red Coins", 0x3050D5, 0x41, lambda state: logic._66Coins(state)),
    LocationData("6-6", "The Deep, Underground Maze: Flowers", 0x3050D6, 0x41, lambda state: logic._66Flowers(state)),
    LocationData("6-6", "The Deep, Underground Maze: Stars", 0x3050D7, 0x41, lambda state: logic._66Stars(state)),
    LocationData("6-6", "The Deep, Underground Maze: Level Clear", 0x3050D8, 0x41, lambda state: logic._66Clear(state)),

    LocationData("6-7", "KEEP MOVING!!!!: Red Coins", 0x3050D9, 0x42, lambda state: logic._67Coins(state)),
    LocationData("6-7", "KEEP MOVING!!!!: Flowers", 0x3050DA, 0x42, lambda state: logic._67Flowers(state)),
    LocationData("6-7", "KEEP MOVING!!!!: Stars", 0x3050DB, 0x42, lambda state: logic._67Stars(state)),
    LocationData("6-7", "KEEP MOVING!!!!: Level Clear", 0x3050DC, 0x42, lambda state: logic._67Clear(state)),

    LocationData("6-8", "King Bowser's Castle: Red Coins", 0x3050DD, 0x43, lambda state: logic._68Coins(state)),
    LocationData("6-8", "King Bowser's Castle: Flowers", 0x3050DE, 0x43, lambda state: logic._68Flowers(state)),
    LocationData("6-8", "King Bowser's Castle: Stars", 0x3050DF, 0x43, lambda state: logic._68Stars(state))
    ]

    if not multiworld or get_option_value(multiworld, player, "extras_enabled") == 1:
        location_table += ( 
            LocationData("1-Extra", "Poochy Ain't Stupid: Red Coins", 0x3050E0, 0x08, lambda state: logic._1ECoins(state)),
            LocationData("1-Extra", "Poochy Ain't Stupid: Flowers", 0x3050E1, 0x08, lambda state: logic._1EFlowers(state)),
            LocationData("1-Extra", "Poochy Ain't Stupid: Stars", 0x3050E2, 0x08, lambda state: logic._1EStars(state)),
            LocationData("1-Extra", "Poochy Ain't Stupid: Level Clear", 0x3050E3, 0x08, lambda state: logic._1EClear(state)),

            LocationData("2-Extra", "Hit That Switch!!: Red Coins", 0x3050E4, 0x14, lambda state: logic._2ECoins(state)),
            LocationData("2-Extra", "Hit That Switch!!: Flowers", 0x3050E5, 0x14, lambda state: logic._2EFlowers(state)),
            LocationData("2-Extra", "Hit That Switch!!: Stars", 0x3050E6, 0x14, lambda state: logic._2EStars(state)),
            LocationData("2-Extra", "Hit That Switch!!: Level Clear", 0x3050E7, 0x14, lambda state: logic._2EClear(state)),

            LocationData("3-Extra", "More Monkey Madness: Red Coins", 0x3050E8, 0x20, lambda state: logic._3ECoins(state)),
            LocationData("3-Extra", "More Monkey Madness: Flowers", 0x3050E9, 0x20, lambda state: logic._3EFlowers(state)),
            LocationData("3-Extra", "More Monkey Madness: Stars", 0x3050EA, 0x20, lambda state: logic._3EStars(state)),
            LocationData("3-Extra", "More Monkey Madness: Level Clear", 0x3050EB, 0x20, lambda state: logic._3EClear(state)),

            LocationData("4-Extra", "The Impossible? Maze: Red Coins", 0x3050EC, 0x2C, lambda state: logic._4ECoins(state)),
            LocationData("4-Extra", "The Impossible? Maze: Flowers", 0x3050ED, 0x2C, lambda state: logic._4EFlowers(state)),
            LocationData("4-Extra", "The Impossible? Maze: Stars", 0x3050EE, 0x2C, lambda state: logic._4EStars(state)),
            LocationData("4-Extra", "The Impossible? Maze: Level Clear", 0x3050EF, 0x2C, lambda state: logic._4EClear(state)),

            LocationData("5-Extra", "Kamek's Revenge: Red Coins", 0x3050F0, 0x38, lambda state: logic._5ECoins(state)),
            LocationData("5-Extra", "Kamek's Revenge: Flowers", 0x3050F1, 0x38, lambda state: logic._5EFlowers(state)),
            LocationData("5-Extra", "Kamek's Revenge: Stars", 0x3050F2, 0x38, lambda state: logic._5EStars(state)),
            LocationData("5-Extra", "Kamek's Revenge: Level Clear", 0x3050F3, 0x38, lambda state: logic._5EClear(state)),

            LocationData("6-Extra", "Castles - Masterpiece Set: Red Coins", 0x3050F4, 0x44, lambda state: logic._6ECoins(state)),
            LocationData("6-Extra", "Castles - Masterpiece Set: Flowers", 0x3050F5, 0x44, lambda state: logic._6EFlowers(state)),
            LocationData("6-Extra", "Castles - Masterpiece Set: Stars", 0x3050F6, 0x44, lambda state: logic._6EStars(state)),
            LocationData("6-Extra", "Castles - Masterpiece Set: Level Clear", 0x3050F7, 0x44, lambda state: logic._6EClear(state)),
        )

    if not multiworld or get_option_value(multiworld, player, "minigame_checks") == 1 or get_option_value(multiworld, player, "minigame_checks") == 3:
        location_table += ( 
            LocationData("1-3", "The Cave Of Chomp Rock: Bandit Game", 0x3050F8, 0x02, lambda state: logic._13Game(state)),
            LocationData("1-7", "Touch Fuzzy Get Dizzy: Bandit Game", 0x3050F9, 0x06, lambda state: logic._17Game(state)),
            LocationData("2-1", "Visit Koopa And Para-Koopa: Bandit Game", 0x3050FA, 0x0C, lambda state: logic._21Game(state)),
            LocationData("2-3", "What's Gusty Taste Like?: Bandit Game", 0x3050FB, 0x0E, lambda state: logic._23Game(state)),
            LocationData("2-6", "The Cave Of The Mystery Maze: Bandit Game", 0x3050FC, 0x11, lambda state: logic._26Game(state)),
            LocationData("2-7", "Lakitu's Wall: Bandit Game", 0x3050FD, 0x12, lambda state: logic._27Game(state)),
            LocationData("3-2", "Jungle Rhythm...: Bandit Game", 0x3050FE, 0x19, lambda state: logic._32Game(state)),
            LocationData("3-7", "Monkeys' Favorite Lake: Bandit Game", 0x3050FF, 0x1E, lambda state: logic._37Game(state)),
            LocationData("4-2", "The Cave Of The Lakitus: Bandit Game", 0x305100, 0x25, lambda state: logic._42Game(state)),
            LocationData("4-6", "Lake Shore Paradise: Bandit Game", 0x305101, 0x29, lambda state: logic._46Game(state)),
            LocationData("4-7", "Ride Like The Wind: Bandit Game", 0x305102, 0x2A, lambda state: logic._47Game(state)),
            LocationData("5-1", "BLIZZARD!!!: Bandit Game", 0x305103, 0x30, lambda state: logic._51Game(state)),
            LocationData("6-1", "Scary Skeleton Goonies!: Bandit Game", 0x305104, 0x3C, lambda state: logic._61Game(state)),
            LocationData("6-7", "KEEP MOVING!!!!: Bandit Game", 0x305105, 0x42, lambda state: logic._67Game(state)),
        )

    if not multiworld or get_option_value(multiworld, player, "minigame_checks") >= 2:
        location_table += ( 
            LocationData("Flip Cards", "Flip Cards: Victory", 0x305106, 0x09),
            LocationData("Scratch And Match", "Scratch And Match: Victory", 0x305107, 0x15),
            LocationData("Drawing Lots", "Drawing Lots: Victory", 0x305108, 0x21),
            LocationData("Match Cards", "Match Cards: Victory", 0x305109, 0x2D),
            LocationData("Roulette", "Roulette: Victory", 0x30510A, 0x39),
            LocationData("Slot Machine", "Slot Machine: Victory", 0x30510B, 0x45),
        )

    if not multiworld or get_option_value(multiworld, player, "goal") == 1:
        location_table += ( 
            LocationData("Overworld", 'Reconstituted Luigi', None, lambda state: logic.ReconstituteLuigi(state)),
        )
    if not multiworld or get_option_value(multiworld, player, "goal") == 0:
        location_table += ( 
            LocationData("Bowser's Room", "King Bowser's Castle: Level Clear", None, lambda state: logic._68Clear(state)),
        )
    return tuple(location_table)
from .RandomBattleMappings import *
from .StoryBattleMappings import *
#region Battle Mappings Lists
gallione_only_randoms: list[BattleMapping] = [
    MandaliaPlainsNorth1,
    MandaliaPlainsNorth2,
    MandaliaPlainsNorth3,
    MandaliaPlainsNorth4,
    MandaliaPlainsSouth1,
    MandaliaPlainsSouth2,
    MandaliaPlainsSouth3,
    MandaliaPlainsSouth4,
    MandaliaPlainsSouth5,
    MandaliaPlainsWest1,
    MandaliaPlainsWest2,
    MandaliaPlainsWest3,
    MandaliaPlainsWest4,
    SweegyWoodsEast1,
    SweegyWoodsEast2,
    SweegyWoodsEast3,
    SweegyWoodsEast4,
    SweegyWoodsEast5,
    SweegyWoodsWest1,
    SweegyWoodsWest2,
    SweegyWoodsWest3,
    SweegyWoodsWest4,
    LenaliaPlateauSouth1,
    LenaliaPlateauSouth2,
    LenaliaPlateauSouth3,
    LenaliaPlateauSouth4,
    LenaliaPlateauSouth5
]

gallione_randoms_from_fovoham: list[BattleMapping] = [
    LenaliaPlateauNorth1,
    LenaliaPlateauNorth2,
    LenaliaPlateauNorth3,
    LenaliaPlateauNorth4
]

gallione_randoms: list[BattleMapping] = [*gallione_only_randoms, *gallione_randoms_from_fovoham]

gallione_story_fights: list[BattleMapping] = [
    GarilandFight,
    MandaliaPlains,
    SweegyWoods,
    DorterTradeCity1,
    Miluda1,
    Miluda2,
    FortZeakden,
    Dorter2,
    Adramelk
]

gallione_fights: list[BattleMapping] = [*gallione_randoms, *gallione_story_fights]

fovoham_only_randoms: list[BattleMapping] = [
    FovohamPlainsEast1,
    FovohamPlainsEast2,
    FovohamPlainsEast3,
    FovohamPlainsEast4,
    YuguoWoodsEast1,
    YuguoWoodsEast2,
    YuguoWoodsEast3,
    YuguoWoodsEast4,
    YuguoWoodsEast5,
    YuguoWoodsWest1,
    YuguoWoodsWest2,
    YuguoWoodsWest3,
    YuguoWoodsWest4,
    GrogHillWest1,
    GrogHillWest2,
    GrogHillWest3,
    GrogHillWest4
]

fovoham_randoms_from_gallione: list[BattleMapping] = [
    FovohamPlainsWest1,
    FovohamPlainsWest2,
    FovohamPlainsWest3,
    FovohamPlainsWest4,
    FovohamPlainsWest5,
    FovohamPlainsSouth1,
    FovohamPlainsSouth2,
    FovohamPlainsSouth3,
    FovohamPlainsSouth4
]

fovoham_randoms_from_lesalia: list[BattleMapping] = [
    GrogHillSouth1,
    GrogHillSouth2,
    GrogHillSouth3,
    GrogHillSouth4,
    GrogHillSouth5
]

fovoham_randoms_from_zeltennia: list[BattleMapping] = [
    GrogHillEast1,
    GrogHillEast2,
    GrogHillEast3,
    GrogHillEast4
]

fovoham_randoms: list[BattleMapping] = [
    *fovoham_only_randoms, *fovoham_randoms_from_gallione,
    *fovoham_randoms_from_lesalia, *fovoham_randoms_from_zeltennia
]

fovoham_story_fights: list[BattleMapping] = [
    Wiegraf1,
    GrogHill,
    RescueRafa,
    YuguoWoods,
    RiovanesCastleEntrance,
    InsideofRiovanesCastle,
    RooftopofRiovanesCastle
]

fovoham_fights: list[BattleMapping] = [*fovoham_randoms, *fovoham_story_fights]

lesalia_only_randoms: list[BattleMapping] = [
    BerveniaVolcanoSouth1,
    BerveniaVolcanoSouth2,
    BerveniaVolcanoSouth3,
    BerveniaVolcanoSouth4,
    ZeklausDesertNorth1,
    ZeklausDesertNorth2,
    ZeklausDesertNorth3,
    ZeklausDesertNorth4,
    ZeklausDesertEast1,
    ZeklausDesertEast2,
    ZeklausDesertEast3,
    ZeklausDesertEast4,
    AraguayWoodsEast1,
    AraguayWoodsEast2,
    AraguayWoodsEast3,
    AraguayWoodsEast4,
    ZirekileFallsWest1,
    ZirekileFallsWest2,
    ZirekileFallsWest3,
    ZirekileFallsWest4
]

lesalia_randoms_from_gallione: list[BattleMapping] = [
    AraguayWoodsWest1,
    AraguayWoodsWest2,
    AraguayWoodsWest3,
    AraguayWoodsWest4,
    AraguayWoodsWest5,
]

lesalia_randoms_from_fovoham: list[BattleMapping] = [
    BerveniaVolcanoNorth1,
    BerveniaVolcanoNorth2,
    BerveniaVolcanoNorth3,
    BerveniaVolcanoNorth4,
    BerveniaVolcanoNorth5
]

lesalia_randoms_from_lionel: list[BattleMapping] = [
    ZirekileFallsSouth1,
    ZirekileFallsSouth2,
    ZirekileFallsSouth3,
    ZirekileFallsSouth4,
]

lesalia_randoms_from_limberry: list[BattleMapping] = [
    ZirekileFallsEast1,
    ZirekileFallsEast2,
    ZirekileFallsEast3,
    ZirekileFallsEast4,
    ZirekileFallsEast5,
]

lesalia_randoms: list[BattleMapping] = [
    *lesalia_only_randoms, *lesalia_randoms_from_gallione, *lesalia_randoms_from_fovoham,
    *lesalia_randoms_from_lionel, *lesalia_randoms_from_limberry
]

lesalia_story_fights: list[BattleMapping] = [
    SandRatCellar,
    AraguayWoods,
    ZirekileFalls,
    GolandCoalCity,
    OutsideLesaliaGateZalmo1,
    CollieryUndergroundThirdFloor,
    CollieryUndergroundSecondFloor,
    CollieryUndergroundFirstFloor
]

lesalia_fights: list[BattleMapping] = [*lesalia_randoms, *lesalia_story_fights]

lionel_only_randoms: list[BattleMapping] = [
    BariusHillNorth1,
    BariusHillNorth2,
    BariusHillNorth3,
    BariusHillNorth4,
    BariusHillSouth1,
    BariusHillSouth2,
    BariusHillSouth3,
    BariusHillSouth4,
    BariusHillSouth5,
    ZigolisSwampEast1,
    ZigolisSwampEast2,
    ZigolisSwampEast3,
    ZigolisSwampEast4
]

lionel_randoms_from_murond: list[BattleMapping] = [
    ZigolisSwampWest1,
    ZigolisSwampWest2,
    ZigolisSwampWest3,
    ZigolisSwampWest4,
    ZigolisSwampWest5,
]

lionel_randoms: list[BattleMapping] = [*lionel_only_randoms, *lionel_randoms_from_murond]

lionel_story_fights: list[BattleMapping] = [
    ZalandFortCity,
    BariausHill,
    ZigolisSwamp,
    BariausValley,
    GolgorandExecutionSite,
    LionelCastleGate,
    InsideofLionelCastle
]

lionel_fights: list[BattleMapping] = [*lionel_randoms, *lionel_story_fights]

zeltennia_only_randoms: list[BattleMapping] = [
    DoguolaPassEast1,
    DoguolaPassEast2,
    DoguolaPassEast3,
    DoguolaPassEast4,
    FinathRiverEast1,
    FinathRiverEast2,
    FinathRiverEast3,
    FinathRiverEast4,
    FinathRiverEast5,
    FinathRiverWest1,
    FinathRiverWest2,
    FinathRiverWest3,
    FinathRiverWest4,
    GerminasPeakNorth1,
    GerminasPeakNorth2,
    GerminasPeakNorth3,
    GerminasPeakNorth4,
    GerminasPeakNorth5
]

zeltennia_randoms_from_fovoham: list[BattleMapping] = [
    DoguolaPassWest1,
    DoguolaPassWest2,
    DoguolaPassWest3,
    DoguolaPassWest4,
    DoguolaPassWest5
]

zeltennia_randoms_from_limberry: list[BattleMapping] = [
    GerminasPeakSouth1,
    GerminasPeakSouth2,
    GerminasPeakSouth3,
    GerminasPeakSouth4,
]

zeltennia_randoms: list[BattleMapping] = [
    *zeltennia_only_randoms, *zeltennia_randoms_from_fovoham, *zeltennia_randoms_from_limberry
]

zeltennia_story_fights: list[BattleMapping] = [
    DoguolaPass,
    BerveniaFreeCity,
    FinathRiver,
    ZalmoII,
    GerminasPeak,
    NelveskaTemple,
    Zarghidas
]

zeltennia_fights: list[BattleMapping] = [*zeltennia_randoms, *zeltennia_story_fights]

limberry_only_randoms: list[BattleMapping] = [
    BedDesertSouth1,
    BedDesertSouth2,
    BedDesertSouth3,
    BedDesertSouth4,
    DolbodarSwampEast1,
    DolbodarSwampEast2,
    DolbodarSwampEast3,
    DolbodarSwampEast4,
    DolbodarSwampWest1,
    DolbodarSwampWest2,
    DolbodarSwampWest3,
    DolbodarSwampWest4,
    DolbodarSwampWest5,
    PoeskasLakeSouth1,
    PoeskasLakeSouth2,
    PoeskasLakeSouth3,
    PoeskasLakeSouth4
]

limberry_randoms_from_zeltennia: list[BattleMapping] = [
    BedDesertNorth1,
    BedDesertNorth2,
    BedDesertNorth3,
    BedDesertNorth4,
    BedDesertNorth5,
    PoeskasLakeNorth1,
    PoeskasLakeNorth2,
    PoeskasLakeNorth3,
    PoeskasLakeNorth4,
    PoeskasLakeNorth5,
]

limberry_randoms: list[BattleMapping] = [*limberry_only_randoms, *limberry_randoms_from_zeltennia]

limberry_story_fights: list[BattleMapping] = [
    BalkI,
    NorthWallofBethlaGarrison,
    SouthWallofBethlaGarrison,
    BethlaSluice,
    PoeskasLake,
    OutsideofLimberryCastle,
    ElmdorII,
    Zalera
]

limberry_fights: list[BattleMapping] = [*limberry_randoms, *limberry_story_fights]

nogias_fights: list[BattleMapping] = [
    Nogias1,
    Nogias2,
    Nogias3,
    Nogias4,
]

terminate_fights: list[BattleMapping] = [
    Terminate1,
    Terminate2,
    Terminate3,
    Terminate4,
]

delta_fights: list[BattleMapping] = [
    Delta1,
    Delta2,
    Delta3,
    Delta4,
]

valkyries_fights: list[BattleMapping] = [
    Valkyries1,
    Valkyries2,
    Valkyries3,
    Valkyries4
]

mlapan_fights: list[BattleMapping] = [
    Mlapan1,
    Mlapan2,
    Mlapan3,
    Mlapan4
]

tiger_fights: list[BattleMapping] = [
    Tiger1,
    Tiger2,
    Tiger3,
    Tiger4
]

bridge_fights: list[BattleMapping] = [
    Bridge1,
    Bridge2,
    Bridge3,
    Bridge4
]

voyage_fights: list[BattleMapping] = [
    Voyage1,
    Voyage2,
    Voyage3,
    Voyage4
]

horror_fights: list[BattleMapping] = [
    Horror1,
    Horror2,
    Horror3,
    Horror4
]

deep_dungeon_fights: list[BattleMapping] = [
    *nogias_fights, *terminate_fights, *delta_fights, *valkyries_fights,
    *mlapan_fights, *tiger_fights, *bridge_fights, *voyage_fights, *horror_fights, DDENDversusElidibs
]

murond_story_fights: list[BattleMapping] = [
    GougMachineCity,
    UndergroundBookStorageSecondFloor,
    UndergroundBookStorageThirdFloor,
    UndergroundBookStorageFirstFloor,
    StMurondTemple,
    HallofStMurondTemple,
    ChapelofStMurondTemple,
    UndergroundBookStorageFourthFloor,
    UndergroundBookStorageFifthFloor,
    MurondDeathCity,
    LostSacredPrecincts,
    GraveyardofAirships1,
    GraveyardofAirships2,
    *deep_dungeon_fights
]

all_randoms: list[BattleMapping] = [
    *gallione_randoms, *fovoham_randoms, *lesalia_randoms, *lionel_randoms,
    *zeltennia_randoms, *limberry_randoms
]

all_story_fights: list[BattleMapping] = [
    *gallione_story_fights, *fovoham_story_fights, *lesalia_story_fights,
    *lionel_story_fights, *zeltennia_story_fights, *limberry_story_fights, *murond_story_fights
]

all_fights: list[BattleMapping] = [*all_randoms, *all_story_fights]
#endregion

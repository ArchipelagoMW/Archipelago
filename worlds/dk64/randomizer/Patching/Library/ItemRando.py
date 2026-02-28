"""Library functions for Item Rando."""

import random
from enum import IntEnum, auto
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Items import Items
from randomizer.Enums.Types import Types
from randomizer.Enums.Locations import Locations

IceTrapMasks = {
    Items.IceTrapBubble: Types.Banana,
    Items.IceTrapReverse: Types.Banana,
    Items.IceTrapSlow: Types.Banana,
    Items.IceTrapBubbleBean: Types.Bean,
    Items.IceTrapReverseBean: Types.Bean,
    Items.IceTrapSlowBean: Types.Bean,
    Items.IceTrapBubbleKey: Types.Key,
    Items.IceTrapReverseKey: Types.Key,
    Items.IceTrapSlowKey: Types.Key,
    Items.IceTrapDisableA: Types.Banana,
    Items.IceTrapDisableABean: Types.Bean,
    Items.IceTrapDisableAKey: Types.Key,
    Items.IceTrapDisableB: Types.Banana,
    Items.IceTrapDisableBBean: Types.Bean,
    Items.IceTrapDisableBKey: Types.Key,
    Items.IceTrapDisableZ: Types.Banana,
    Items.IceTrapDisableZBean: Types.Bean,
    Items.IceTrapDisableZKey: Types.Key,
    Items.IceTrapDisableCU: Types.Banana,
    Items.IceTrapDisableCUBean: Types.Bean,
    Items.IceTrapDisableCUKey: Types.Key,
    Items.IceTrapGetOutGB: Types.Banana,
    Items.IceTrapGetOutBean: Types.Bean,
    Items.IceTrapGetOutKey: Types.Key,
    Items.IceTrapDryGB: Types.Banana,
    Items.IceTrapDryBean: Types.Bean,
    Items.IceTrapDryKey: Types.Key,
    Items.IceTrapFlipGB: Types.Banana,
    Items.IceTrapFlipBean: Types.Bean,
    Items.IceTrapFlipKey: Types.Key,
    Items.IceTrapBubbleFairy: Types.Fairy,
    Items.IceTrapReverseFairy: Types.Fairy,
    Items.IceTrapSlowFairy: Types.Fairy,
    Items.IceTrapDisableAFairy: Types.Fairy,
    Items.IceTrapDisableBFairy: Types.Fairy,
    Items.IceTrapDisableZFairy: Types.Fairy,
    Items.IceTrapDisableCUFairy: Types.Fairy,
    Items.IceTrapGetOutFairy: Types.Fairy,
    Items.IceTrapDryFairy: Types.Fairy,
    Items.IceTrapFlipFairy: Types.Fairy,
    Items.IceTrapIceFloorGB: Types.Banana,
    Items.IceTrapIceFloorBean: Types.Bean,
    Items.IceTrapIceFloorKey: Types.Key,
    Items.IceTrapIceFloorFairy: Types.Fairy,
    Items.IceTrapPaperGB: Types.Banana,
    Items.IceTrapPaperBean: Types.Bean,
    Items.IceTrapPaperKey: Types.Key,
    Items.IceTrapPaperFairy: Types.Fairy,
    Items.IceTrapSlipGB: Types.Banana,
    Items.IceTrapSlipBean: Types.Bean,
    Items.IceTrapSlipKey: Types.Key,
    Items.IceTrapSlipFairy: Types.Fairy,
    Items.IceTrapAnimalGB: Types.Banana,
    Items.IceTrapAnimalBean: Types.Bean,
    Items.IceTrapAnimalKey: Types.Key,
    Items.IceTrapAnimalFairy: Types.Fairy,
    Items.IceTrapRockfallGB: Types.Banana,
    Items.IceTrapRockfallBean: Types.Bean,
    Items.IceTrapRockfallKey: Types.Key,
    Items.IceTrapRockfallFairy: Types.Fairy,
    Items.IceTrapDisableTagGB: Types.Banana,
    Items.IceTrapDisableTagBean: Types.Bean,
    Items.IceTrapDisableTagKey: Types.Key,
    Items.IceTrapDisableTagFairy: Types.Fairy,
}
IceTrapMaskIndexes = [Types.Banana, Types.Bean, Types.Key, Types.Fairy]

hint_indexes = [
    [Items.JapesDonkeyHint, Items.AztecDonkeyHint, Items.FactoryDonkeyHint, Items.GalleonDonkeyHint, Items.ForestDonkeyHint, Items.CavesDonkeyHint, Items.CastleDonkeyHint],
    [Items.JapesDiddyHint, Items.AztecDiddyHint, Items.FactoryDiddyHint, Items.GalleonDiddyHint, Items.ForestDiddyHint, Items.CavesDiddyHint, Items.CastleDiddyHint],
    [Items.JapesLankyHint, Items.AztecLankyHint, Items.FactoryLankyHint, Items.GalleonLankyHint, Items.ForestLankyHint, Items.CavesLankyHint, Items.CastleLankyHint],
    [Items.JapesTinyHint, Items.AztecTinyHint, Items.FactoryTinyHint, Items.GalleonTinyHint, Items.ForestTinyHint, Items.CavesTinyHint, Items.CastleTinyHint],
    [Items.JapesChunkyHint, Items.AztecChunkyHint, Items.FactoryChunkyHint, Items.GalleonChunkyHint, Items.ForestChunkyHint, Items.CavesChunkyHint, Items.CastleChunkyHint],
]

move_indexes = {
    Kongs.donkey: [
        Items.Coconut,
        Items.Bongos,
        Items.BaboonBlast,
        Items.StrongKong,
        Items.GorillaGrab,
    ],
    Kongs.diddy: [
        Items.Peanut,
        Items.Guitar,
        Items.ChimpyCharge,
        Items.RocketbarrelBoost,
        Items.SimianSpring,
    ],
    Kongs.lanky: [
        Items.Grape,
        Items.Trombone,
        Items.Orangstand,
        Items.BaboonBalloon,
        Items.OrangstandSprint,
    ],
    Kongs.tiny: [
        Items.Feather,
        Items.Saxophone,
        Items.MiniMonkey,
        Items.PonyTailTwirl,
        Items.Monkeyport,
    ],
    Kongs.chunky: [
        Items.Pineapple,
        Items.Triangle,
        Items.HunkyChunky,
        Items.PrimatePunch,
        Items.GorillaGone,
    ],
    Kongs.any: [
        Items.ProgressiveAmmoBelt,
        Items.ProgressiveAmmoBelt2,
        Items.ProgressiveInstrumentUpgrade,
        Items.ProgressiveInstrumentUpgrade2,
        Items.ProgressiveInstrumentUpgrade3,
        Items.ProgressiveSlam,
        Items.ProgressiveSlam2,
        Items.ProgressiveSlam3,
        Items.Swim,
        Items.Oranges,
        Items.Barrels,
        Items.Vines,
        Items.Camera,
        Items.Shockwave,
        Items.CameraAndShockwave,
        Items.Climbing,
        Items.SniperSight,
        Items.HomingAmmo,
    ],
}


def getHintKong(item: Items) -> int:
    """Get the Kong index for a hint item."""
    for index, lst in enumerate(hint_indexes):
        if item in lst:
            return index
    return None


def getMoveKong(item: Items) -> int:
    """Get the Kong enum for a move."""
    for kong, lst in move_indexes.items():
        if item in lst:
            return kong
    return None


class CustomActors(IntEnum):
    """Custom Actors Enum."""

    NintendoCoin = 345
    RarewareCoin = auto()
    Null = auto()
    PotionDK = auto()
    PotionDiddy = auto()
    PotionLanky = auto()
    PotionTiny = auto()
    PotionChunky = auto()
    PotionAny = auto()
    KongDK = auto()
    KongDiddy = auto()
    KongLanky = auto()
    KongTiny = auto()
    KongChunky = auto()
    KongDisco = auto()
    KongKrusha = auto()
    Bean = auto()
    Pearl = auto()
    Fairy = auto()
    IceTrapGB = auto()
    IceTrapBean = auto()
    IceTrapKey = auto()
    Medal = auto()
    JetpacItemOverlay = auto()
    CrankyItem = auto()
    FunkyItem = auto()
    CandyItem = auto()
    SnideItem = auto()
    ZingerFlamethrower = auto()
    Scarab = auto()
    HintItemDK = auto()
    KopDummy = auto()
    HintItemDiddy = auto()
    HintItemLanky = auto()
    HintItemTiny = auto()
    HintItemChunky = auto()
    ArchipelagoItem = auto()
    IceTrapFairy = auto()
    SlipPeel = auto()
    SpecialArchipelagoItem = auto()
    FoolsArchipelagoItem = auto()
    TrapArchipelagoItem = auto()
    SpreadCounter = auto()
    GuardDisableA = auto()
    GuardDisableZ = auto()
    GuardGetOut = auto()
    GuardTag = auto()


class GraphicOverlay(IntEnum):
    """Graphic Overlay Enum."""

    Banana = 0
    Blueprint = auto()
    Key = auto()
    Crown = auto()
    CompanyCoin = auto()
    Medal = auto()
    CrankyPotion = auto()
    FunkyPotion = auto()
    CandyPotion = auto()
    TrainingBarrel = auto()
    Shockwave = auto()
    Kong = auto()
    Bean = auto()
    Pearl = auto()
    Fairy = auto()
    RainbowCoin = auto()
    IceTrapBubble = auto()
    JunkMelon = auto()
    CrankyItem = auto()
    FunkyItem = auto()
    CandyItem = auto()
    SnideItem = auto()
    NoItem = auto()
    IceTrapReverse = auto()
    IceTrapSlow = auto()
    Hint = auto()
    IceTrapDisableA = auto()
    IceTrapDisableB = auto()
    IceTrapDisableZ = auto()
    IceTrapDisableCU = auto()


class ArcadeRewards(IntEnum):
    """Enum of Arcade Rewards."""

    NintendoCoin = 0  # Or No Item
    Bean = auto()
    Blueprint = auto()
    Crown = auto()
    Fairy = auto()
    Banana = auto()
    Key = auto()
    Medal = auto()
    Pearl = auto()
    PotionDK = auto()
    PotionDiddy = auto()
    PotionLanky = auto()
    PotionTiny = auto()
    PotionChunky = auto()
    PotionAny = auto()
    Donkey = auto()
    Diddy = auto()
    Lanky = auto()
    Tiny = auto()
    Chunky = auto()
    RainbowCoin = auto()
    RarewareCoin = auto()
    JunkItem = auto()
    IceTrap = auto()
    Cranky = auto()
    Funky = auto()
    Candy = auto()
    Snide = auto()
    Hint = auto()
    BPDK = auto()
    BPDiddy = auto()
    BPLanky = auto()
    BPTiny = auto()
    BPChunky = auto()
    APItem = auto()


class JetpacRewards(IntEnum):
    """Enum of Jetpac Rewards."""

    RarewareCoin = 0  # Or NoItem
    Bean = auto()
    Blueprint = auto()
    Crown = auto()
    Fairy = auto()
    Banana = auto()
    Key = auto()
    Medal = auto()
    Pearl = auto()
    Potion = auto()
    Kong = auto()
    RainbowCoin = auto()
    NintendoCoin = auto()
    JunkItem = auto()
    IceTrap = auto()
    Cranky = auto()
    Funky = auto()
    Candy = auto()
    Snide = auto()
    Hint = auto()
    APItem = auto()


class BuyText(IntEnum):
    """Enum of items in the order of buy text."""

    blast = 0
    strong = auto()
    grab = auto()
    charge = auto()
    rocket = auto()
    spring = auto()
    ostand = auto()
    balloon = auto()
    sprint = auto()
    mini = auto()
    ptt = auto()
    port = auto()
    hunky = auto()
    punch = auto()
    gone = auto()
    slam = auto()
    coconut = auto()
    peanut = auto()
    grape = auto()
    feather = auto()
    pineapple = auto()
    homing = auto()
    sniper = auto()
    ammo_belt = auto()
    bongos = auto()
    guitar = auto()
    trombone = auto()
    sax = auto()
    triangle = auto()
    instrument_upgrade = auto()
    dive = auto()
    orange = auto()
    barrel = auto()
    vine = auto()
    climb = auto()
    camera = auto()
    shockwave = auto()
    camera_and_shockwave = auto()
    golden_banana = auto()
    crown = auto()
    medal = auto()
    key = auto()
    blueprint = auto()
    nin_coin = auto()
    rw_coin = auto()
    bean = auto()
    pearl = auto()
    kong = auto()
    fairy = auto()
    ice_trap = auto()
    hint = auto()
    terminator = auto()  # Used for nobuytext calculations


class NoBuyText(IntEnum):
    """Enum of items in the order of can't buy text."""

    special_move = 0
    slam = auto()
    gun = auto()
    gun_upgrade = auto()
    ammo_belt = auto()
    instrument = auto()
    training_move = auto()
    fairy_move = auto()
    misc_item = auto()
    golden_banana = auto()
    blueprint = auto()
    medal = auto()
    kong = auto()


class TrackerItems(IntEnum):
    """Tracker Items Enum."""

    COCONUT = 0
    BONGOS = auto()
    GRAB = auto()
    STRONG = auto()
    BLAST = auto()
    PEANUT = auto()
    GUITAR = auto()
    CHARGE = auto()
    ROCKET = auto()
    SPRING = auto()
    GRAPE = auto()
    TROMBONE = auto()
    OSTAND = auto()
    OSPRINT = auto()
    BALLOON = auto()
    FEATHER = auto()
    SAX = auto()
    PTT = auto()
    MINI = auto()
    MONKEYPORT = auto()
    PINEAPPLE = auto()
    TRIANGLE = auto()
    PUNCH = auto()
    HUNKY = auto()
    GONE = auto()
    SLAM = auto()
    SLAM_HAS = auto()
    HOMING = auto()
    SNIPER = auto()
    AMMOBELT = auto()
    INSTRUMENT_UPG = auto()
    DIVE = auto()
    ORANGE = auto()
    BARREL = auto()
    VINE = auto()
    CAMERA = auto()
    SHOCKWAVE = auto()
    KEY1 = auto()
    KEY2 = auto()
    KEY3 = auto()
    KEY4 = auto()
    KEY5 = auto()
    KEY6 = auto()
    KEY7 = auto()
    KEY8 = auto()
    MELON_2 = auto()
    MELON_3 = auto()
    INSUPG_1 = auto()
    INSUPG_2 = auto()
    BELT_1 = auto()
    BELT_2 = auto()
    CRANKY = auto()
    FUNKY = auto()
    CANDY = auto()
    SNIDE = auto()
    CLIMB = auto()
    TERMINATOR = auto()


class LocationSelection:
    """Class which contains information pertaining to assortment."""

    def __init__(
        self,
        *,
        vanilla_item=None,
        placement_data=None,
        is_reward_point=False,
        flag=None,
        kong=Kongs.any,
        location=None,
        name="",
        is_shop=False,
        price=0,
        placement_index=0,
        can_have_item=True,
        can_place_item=True,
        shop_locked=False,
        shared=False,
        order=0,
    ):
        """Initialize with given data."""
        self.name = name
        self.old_item = vanilla_item
        self.placement_data = placement_data
        self.old_flag = flag
        self.old_kong = kong
        self.reward_spot = is_reward_point
        self.location = location
        self.is_shop = is_shop
        self.price = price
        self.placement_index = placement_index
        self.can_have_item = can_have_item
        self.can_place_item = can_place_item
        self.shop_locked = shop_locked
        self.shared = shared
        self.order = order
        self.move_name = ""
        self.new_type: Types = None
        self.new_flag: int = None
        self.new_kong: Kongs = None
        self.new_item: Items = None

    def PlaceFlag(self, flag, kong):
        """Place item for assortment."""
        self.new_flag = flag
        self.new_kong = kong


pregiven_item_order = [
    Items.BaboonBlast,
    Items.StrongKong,
    Items.GorillaGrab,
    Items.ChimpyCharge,
    Items.RocketbarrelBoost,
    Items.SimianSpring,
    Items.Orangstand,
    Items.BaboonBalloon,
    Items.OrangstandSprint,
    Items.MiniMonkey,
    Items.PonyTailTwirl,
    Items.Monkeyport,
    Items.HunkyChunky,
    Items.PrimatePunch,
    Items.GorillaGone,
    Items.ProgressiveSlam,
    Items.ProgressiveSlam,
    Items.ProgressiveSlam,
    Items.Coconut,
    Items.Peanut,
    Items.Grape,
    Items.Feather,
    Items.Pineapple,
    Items.Bongos,
    Items.Guitar,
    Items.Trombone,
    Items.Saxophone,
    Items.Triangle,
    Items.ProgressiveAmmoBelt,
    Items.ProgressiveAmmoBelt,
    Items.HomingAmmo,
    Items.SniperSight,
    Items.ProgressiveInstrumentUpgrade,
    Items.ProgressiveInstrumentUpgrade,
    Items.ProgressiveInstrumentUpgrade,
    Items.Swim,
    Items.Oranges,
    Items.Barrels,
    Items.Vines,
    Items.Camera,
    Items.Shockwave,
    Items.Climbing,
]


class ItemPlacementData:
    """Class to store information pertaining to writing Item Rando data."""

    def __init__(
        self,
        model_index: list[int] = None,
        model_two_index: list[int] = None,
        actor_index: list[int] = None,
        arcade_reward_index: list[int] = None,
        jetpac_reward_index: list[int] = None,
        overlay: list[GraphicOverlay] = None,
        index_getter=None,
        preview_text: str = "",
        special_preview_text: dict = {},
        scale: float = 0.25,
    ):
        """Initialize with given parameters."""
        self.has_model = model_index is not None
        self.model_index = model_index
        self.model_two_index = model_two_index
        self.arcade_reward_index = arcade_reward_index
        self.jetpac_reward_index = jetpac_reward_index
        self.actor_index = actor_index
        self.overlay = overlay
        if index_getter is None:
            self.index_getter = lambda item: 0
        else:
            self.index_getter = index_getter
        if isinstance(preview_text, list):
            self.preview_text = [f"\x04{text}\x04" for text in preview_text]
        else:
            self.preview_text = f"\x04{preview_text}\x04"
        temp_data = {}
        for key, string_or_list in special_preview_text.items():
            if isinstance(string_or_list, list):
                temp_data[key] = [f"\x04{text}\x04" for text in string_or_list]
            else:
                temp_data[key] = f"\x04{string_or_list}\x04"
        self.special_preview_text = temp_data.copy()
        self.scale = scale


item_db = {
    Types.Banana: ItemPlacementData(
        model_index=[0x69],
        model_two_index=[0x74],
        actor_index=[45],
        arcade_reward_index=[ArcadeRewards.Banana],
        jetpac_reward_index=[JetpacRewards.Banana],
        overlay=[GraphicOverlay.Banana],
        preview_text="GOLDEN BANANA",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BANANA OF PURE GOLD",
            Locations.ForestDiddyOwlRace: "BRIGHT FRUIT OF GOLD",
        },
    ),
    Types.Key: ItemPlacementData(
        model_index=[0xF5],
        model_two_index=[0x13C],
        actor_index=[72],
        arcade_reward_index=[ArcadeRewards.Key],
        jetpac_reward_index=[JetpacRewards.Key],
        overlay=[GraphicOverlay.Key],
        preview_text="BOSS KEY",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "KEY TO DAVY JONES LOCKER",
            Locations.ForestDiddyOwlRace: "HEAVY DOOR OPENER",
        },
        scale=0.17,
    ),
    Types.Crown: ItemPlacementData(
        model_index=[0xF4],
        model_two_index=[0x18D],
        actor_index=[86],
        arcade_reward_index=[ArcadeRewards.Crown],
        jetpac_reward_index=[JetpacRewards.Crown],
        overlay=[GraphicOverlay.Crown],
        preview_text="BATTLE CROWN",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "CROWN TO PLACE ATOP YER HEAD",
            Locations.ForestDiddyOwlRace: "CIRCLE OF RULING",
        },
    ),
    Types.Fairy: ItemPlacementData(
        model_index=[0x3D],
        model_two_index=[0x25C],
        actor_index=[CustomActors.Fairy],
        arcade_reward_index=[ArcadeRewards.Fairy],
        jetpac_reward_index=[JetpacRewards.Fairy],
        overlay=[GraphicOverlay.Fairy],
        preview_text="BANANA FAIRY",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "MAGICAL FLYING PIXIE",
            Locations.ForestDiddyOwlRace: "SMALL WINGED CREATURE",
        },
    ),
    Types.Shop: ItemPlacementData(
        model_index=[0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB],
        model_two_index=[0x5B, 0x1F2, 0x59, 0x1F3, 0x1F5, 0x1F6],
        arcade_reward_index=[
            ArcadeRewards.PotionDK,
            ArcadeRewards.PotionDiddy,
            ArcadeRewards.PotionLanky,
            ArcadeRewards.PotionTiny,
            ArcadeRewards.PotionChunky,
            ArcadeRewards.PotionAny,
        ],
        actor_index=[
            CustomActors.PotionDK,
            CustomActors.PotionDiddy,
            CustomActors.PotionLanky,
            CustomActors.PotionTiny,
            CustomActors.PotionChunky,
            CustomActors.PotionAny,
        ],
        jetpac_reward_index=[JetpacRewards.Potion] * 6,
        overlay=[GraphicOverlay.CrankyPotion] * 6,  # Handled elsewhere
        index_getter=lambda item: getMoveKong(item),
        preview_text="POTION",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BOTTLE OF GROG",
            Locations.ForestDiddyOwlRace: "STRANGE BREW",
        },
    ),
    Types.Shockwave: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        arcade_reward_index=[ArcadeRewards.PotionAny],
        jetpac_reward_index=[JetpacRewards.Potion],
        overlay=[GraphicOverlay.Shockwave],
        preview_text="POTION",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BOTTLE OF GROG",
            Locations.ForestDiddyOwlRace: "STRANGE BREW",
        },
    ),
    Types.TrainingBarrel: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        arcade_reward_index=[ArcadeRewards.PotionAny],
        jetpac_reward_index=[JetpacRewards.Potion],
        overlay=[GraphicOverlay.TrainingBarrel],
        preview_text="POTION",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BOTTLE OF GROG",
            Locations.ForestDiddyOwlRace: "STRANGE BREW",
        },
    ),
    Types.Climbing: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        arcade_reward_index=[ArcadeRewards.PotionAny],
        jetpac_reward_index=[JetpacRewards.Potion],
        overlay=[GraphicOverlay.TrainingBarrel],
        preview_text="POTION",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BOTTLE OF GROG",
            Locations.ForestDiddyOwlRace: "STRANGE BREW",
        },
    ),
    Types.Kong: ItemPlacementData(
        model_index=[4, 1, 6, 9, 0xC],
        model_two_index=[0x257, 0x258, 0x259, 0x25A, 0x25B],
        actor_index=[
            CustomActors.KongDK,
            CustomActors.KongDiddy,
            CustomActors.KongLanky,
            CustomActors.KongTiny,
            CustomActors.KongChunky,
        ],
        arcade_reward_index=[
            ArcadeRewards.Donkey,
            ArcadeRewards.Diddy,
            ArcadeRewards.Lanky,
            ArcadeRewards.Tiny,
            ArcadeRewards.Chunky,
        ],
        jetpac_reward_index=[JetpacRewards.Kong] * 5,
        overlay=[GraphicOverlay.Kong],
        index_getter=lambda item: (Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky).index(item),
        preview_text="KONG",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "WEIRD MONKEY",
            Locations.ForestDiddyOwlRace: "NOISY JUNGLE BEAST",
        },
    ),
    Types.FakeItem: ItemPlacementData(
        model_index=[0x103, 0x127, 0x128, 0x12B],
        model_two_index=[0x25D, 0x264, 0x265, 0x299],
        actor_index=[
            CustomActors.IceTrapGB,
            CustomActors.IceTrapBean,
            CustomActors.IceTrapKey,
            CustomActors.IceTrapFairy,
        ],
        arcade_reward_index=[ArcadeRewards.IceTrap] * 4,
        jetpac_reward_index=[JetpacRewards.IceTrap] * 4,
        overlay=[GraphicOverlay.IceTrapBubble] * 4,
        index_getter=lambda item: IceTrapMaskIndexes.index(IceTrapMasks[item]),
        preview_text="GLODEN BANANE",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BANANA OF FOOLS GOLD",
            Locations.ForestDiddyOwlRace: "SOMETHING THAT DOESN'T BELONG",
        },
    ),
    Types.Bean: ItemPlacementData(
        model_index=[0x104],
        model_two_index=[0x198],
        actor_index=[CustomActors.Bean],
        arcade_reward_index=[ArcadeRewards.Bean],
        jetpac_reward_index=[JetpacRewards.Bean],
        overlay=[GraphicOverlay.Bean],
        preview_text="BEAN",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "QUESTIONABLE VEGETABLE",
            Locations.ForestDiddyOwlRace: "TINY SEED OF LIFE",
        },
    ),
    Types.Pearl: ItemPlacementData(
        model_index=[0x106],
        model_two_index=[0x1B4],
        actor_index=[CustomActors.Pearl],
        arcade_reward_index=[ArcadeRewards.Pearl],
        jetpac_reward_index=[JetpacRewards.Pearl],
        overlay=[GraphicOverlay.Pearl],
        preview_text="PEARL",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BLACK PEARL",
            Locations.ForestDiddyOwlRace: "WHITE GEM OF THE OCEAN",
        },
    ),
    Types.Medal: ItemPlacementData(
        model_index=[0x108],
        model_two_index=[0x90],
        actor_index=[CustomActors.Medal],
        arcade_reward_index=[ArcadeRewards.Medal],
        jetpac_reward_index=[JetpacRewards.Medal],
        overlay=[GraphicOverlay.Medal],
        preview_text="BANANA MEDAL",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "MEDALLION",
            Locations.ForestDiddyOwlRace: "FRUIT EARNED HONOR",
        },
        scale=0.22,
    ),
    Types.NintendoCoin: ItemPlacementData(
        model_index=[0x10A],
        model_two_index=[0x48],
        actor_index=[CustomActors.NintendoCoin],
        arcade_reward_index=[ArcadeRewards.NintendoCoin],
        jetpac_reward_index=[JetpacRewards.NintendoCoin],
        overlay=[GraphicOverlay.CompanyCoin],
        preview_text="NINTENDO COIN",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "ANCIENT DOUBLOON",
            Locations.ForestDiddyOwlRace: "A PUBLISHERS TREASURED TOKEN",
        },
        scale=0.4,
    ),
    Types.RarewareCoin: ItemPlacementData(
        model_index=[0x10C],
        model_two_index=[0x28F],
        actor_index=[CustomActors.RarewareCoin],
        arcade_reward_index=[ArcadeRewards.RarewareCoin],
        jetpac_reward_index=[JetpacRewards.RarewareCoin],
        overlay=[GraphicOverlay.CompanyCoin],
        preview_text="RAREWARE COIN",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "DOUBLOON OF THE RAREST KIND",
            Locations.ForestDiddyOwlRace: "ANCIENT RARE PRIZE",
        },
        scale=0.4,
    ),
    Types.JunkItem: ItemPlacementData(
        model_index=[0x10E],
        model_two_index=[0x25E],
        actor_index=[0x2F],
        arcade_reward_index=[ArcadeRewards.JunkItem],
        jetpac_reward_index=[JetpacRewards.JunkItem],
        overlay=[GraphicOverlay.JunkMelon],
        preview_text="JUNK ITEM",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "HEAP OF JUNK",
            Locations.ForestDiddyOwlRace: "WORTHLESS TRINKET",
        },
    ),
    Types.Cranky: ItemPlacementData(
        model_index=[0x11],
        model_two_index=[0x25F],
        actor_index=[CustomActors.CrankyItem],
        arcade_reward_index=[ArcadeRewards.Cranky],
        jetpac_reward_index=[JetpacRewards.Cranky],
        overlay=[GraphicOverlay.CrankyItem],
        preview_text="SHOPKEEPER",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BARTERING SOUL",
            Locations.ForestDiddyOwlRace: "WATCHER OF WARES",
        },
    ),
    Types.Funky: ItemPlacementData(
        model_index=[0x12],
        model_two_index=[0x260],
        actor_index=[CustomActors.FunkyItem],
        arcade_reward_index=[ArcadeRewards.Funky],
        jetpac_reward_index=[JetpacRewards.Funky],
        overlay=[GraphicOverlay.FunkyItem],
        preview_text="SHOPKEEPER",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BARTERING SOUL",
            Locations.ForestDiddyOwlRace: "WATCHER OF WARES",
        },
    ),
    Types.Candy: ItemPlacementData(
        model_index=[0x13],
        model_two_index=[0x261],
        actor_index=[CustomActors.CandyItem],
        arcade_reward_index=[ArcadeRewards.Candy],
        jetpac_reward_index=[JetpacRewards.Candy],
        overlay=[GraphicOverlay.CandyItem],
        preview_text="SHOPKEEPER",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "BARTERING SOUL",
            Locations.ForestDiddyOwlRace: "WATCHER OF WARES",
        },
    ),
    Types.Snide: ItemPlacementData(
        model_index=[0x1F],
        model_two_index=[0x262],
        actor_index=[CustomActors.SnideItem],
        arcade_reward_index=[ArcadeRewards.Snide],
        jetpac_reward_index=[JetpacRewards.Snide],
        overlay=[GraphicOverlay.SnideItem],
        preview_text="SHOPKEEPER",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "NERDY SOUL",
            Locations.ForestDiddyOwlRace: "THINKER OF MYSTERIES",
        },
    ),
    Types.Hint: ItemPlacementData(
        model_index=[0x11B, 0x11D, 0x11F, 0x121, 0x123],
        model_two_index=[638, 649, 650, 651, 652],
        actor_index=[
            CustomActors.HintItemDK,
            CustomActors.HintItemDiddy,
            CustomActors.HintItemLanky,
            CustomActors.HintItemTiny,
            CustomActors.HintItemChunky,
        ],
        arcade_reward_index=[ArcadeRewards.Hint] * 5,
        jetpac_reward_index=[JetpacRewards.Hint] * 5,
        overlay=[GraphicOverlay.Hint],
        index_getter=lambda item: getHintKong(item),
        preview_text="HINT",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "LAYTON RIDDLE",
            Locations.ForestDiddyOwlRace: "SMALL MORSEL OF WISDOM SHARED",
        },
    ),
    Types.Blueprint: ItemPlacementData(
        model_index=[0x12E, 0x12F, 0x130, 0x131, 0x132],
        model_two_index=[0xDE, 0xE0, 0xE1, 0xDD, 0xDF],
        actor_index=[78, 75, 77, 79, 76],
        overlay=[GraphicOverlay.Blueprint],
        arcade_reward_index=[
            ArcadeRewards.BPDK,
            ArcadeRewards.BPDiddy,
            ArcadeRewards.BPLanky,
            ArcadeRewards.BPTiny,
            ArcadeRewards.BPChunky,
        ],
        jetpac_reward_index=[JetpacRewards.Blueprint] * 5,
        index_getter=lambda item: (item - Items.DonkeyBlueprint) % 5,
        preview_text="BLUEPRINT",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "MAP O' DEATH MACHINE",
            Locations.ForestDiddyOwlRace: "PLANS UPON A PARCHMENT",
        },
        scale=2,
    ),
    Types.RainbowCoin: ItemPlacementData(
        model_index=[0x12D],
        model_two_index=[0xB7],
        actor_index=[0x8C],
        arcade_reward_index=[ArcadeRewards.RainbowCoin],
        jetpac_reward_index=[JetpacRewards.RainbowCoin],
        overlay=[GraphicOverlay.RainbowCoin],
        preview_text="RAINBOW COIN",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "COLORFUL COIN HIDDEN FOR 17 YEARS",
            Locations.ForestDiddyOwlRace: "COLORS BOUND IN A CIRCLE",
        },
    ),
    Types.NoItem: ItemPlacementData(
        model_two_index=[0],
        actor_index=[CustomActors.Null],
        arcade_reward_index=[ArcadeRewards.NintendoCoin],
        jetpac_reward_index=[JetpacRewards.RarewareCoin],
        overlay=[GraphicOverlay.NoItem],
        preview_text="NOTHING",
        special_preview_text={
            Locations.GalleonDonkeySealRace: "DIDDLY SQUAT",
            Locations.ForestDiddyOwlRace: "EMPTY AIR ONLY",
        },
    ),
    Types.ArchipelagoItem: ItemPlacementData(
        model_index=[0x125, 0x134, 0x136, 0x138],
        model_two_index=[0x291, 0x292, 0x293, 0x294],
        actor_index=[CustomActors.ArchipelagoItem, CustomActors.SpecialArchipelagoItem, CustomActors.FoolsArchipelagoItem, CustomActors.TrapArchipelagoItem],
        arcade_reward_index=[ArcadeRewards.APItem] * 4,
        jetpac_reward_index=[JetpacRewards.APItem] * 4,
        overlay=[GraphicOverlay.Hint] * 4,
        index_getter=lambda item: [Items.ArchipelagoItem, Items.SpecialArchipelagoItem, Items.FoolsArchipelagoItem, Items.TrapArchipelagoItem].index(item),
        preview_text=["SPECIAL AP ITEM", "USEFUL AP ITEM", "JUNK AP ITEM", "SPECIAL AP ITEM"],
        special_preview_text={
            Locations.GalleonDonkeySealRace: ["ANOTHER MAN'S TREASURE", "ANOTHER PIRATE'S EYEPATCH", "ONE MAN'S TRASH", "ONE MAN'S TREESURE"],
            Locations.ForestDiddyOwlRace: ["A RABBIT'S FOOT", "A PENNY", "A BLACK CAT", "A RABBTI'S FOOT"],
        },
    ),
}

FILLER_MAPPING = {
    Types.FillerBanana: Types.Banana,
    Types.FillerCrown: Types.Crown,
    Types.FillerFairy: Types.Fairy,
    Types.FillerMedal: Types.Medal,
    Types.FillerPearl: Types.Pearl,
    Types.FillerRainbowCoin: Types.RainbowCoin,
}


def getItemDBEntry(type: Types) -> ItemPlacementData:
    """Get the item db entry for an item type."""
    if type in FILLER_MAPPING:
        return item_db[FILLER_MAPPING[type]]
    if type is None:
        return item_db[Types.NoItem]
    return item_db[type]


def getIceTrapText(input_text: str) -> str:
    """Get the text associated with ice traps."""
    while True:
        characters = list(input_text)
        new_characters = []
        vowels = ["A", "E", "I", "O", "U"]
        vowels_in_string = [x for x in characters if x in vowels]
        unique_vowels = list(set(vowels_in_string))
        if len(vowels_in_string) < 3 or len(unique_vowels) < 2:
            if len(vowels_in_string) == 0:
                # Not sure what to do for strings with no vowels
                return input_text
            vowel_index = 0
            target_vowel_index = random.randint(0, len(vowels_in_string))
            for char in characters:
                if char in vowels:
                    if target_vowel_index == vowel_index:
                        new_characters.append(random.choice(vowels))
                        vowel_index += 1
                        continue
                    vowel_index += 1
                new_characters.append(char)
            new_text = "".join(new_characters)
        else:
            # More vowels
            vowel_idxs = random.sample(range(len(vowels_in_string)), 2)
            vowel_a = vowels_in_string[vowel_idxs[0]]
            vowel_b = vowels_in_string[vowel_idxs[1]]
            if vowel_a == vowel_b:
                continue
            vowels_in_string[vowel_idxs[1]] = vowel_a
            vowels_in_string[vowel_idxs[0]] = vowel_b
            for char in characters:
                if char in vowels:
                    new_characters.append(vowels_in_string.pop(0))
                else:
                    new_characters.append(char)
            new_text = "".join(new_characters)
        if new_text != input_text:
            return new_text


def getModelFromItem(item: Items, item_type: Types) -> int:
    """Get the model index associated with an item."""
    if item_type not in item_db and item_type not in FILLER_MAPPING:
        return None
    item_db_entry = getItemDBEntry(item_type)
    if not item_db_entry.has_model:
        return None
    index = item_db_entry.index_getter(item)
    return item_db_entry.model_index[index]


def getPropFromItem(item: Items, item_type: Types) -> int:
    """Get the prop index associated with an item."""
    index = getItemDBEntry(item_type).index_getter(item)
    return getItemDBEntry(item_type).model_two_index[index]


def getModelMask(item: Items) -> Types:
    """Get the model mask for an ice trap."""
    return IceTrapMasks.get(item, Types.Banana)


def getItemPreviewText(item_type: Types, location: Locations, allow_special_text: bool = True, masked_model: Types = None, item: Items = None) -> str:
    """Get the preview text for an item."""
    reference_item = item_type
    if item_type == Types.FakeItem:
        reference_item = masked_model
    if reference_item not in item_db and reference_item not in FILLER_MAPPING and reference_item is not None:
        return ""
    item_data = getItemDBEntry(reference_item)

    # Handle array-based preview text (like Archipelago items)
    if isinstance(item_data.preview_text, list) and item is not None:
        try:
            index = item_data.index_getter(item)
            text = item_data.preview_text[index]
        except (ValueError, IndexError):
            text = item_data.preview_text[0] if item_data.preview_text else ""
    else:
        text = item_data.preview_text if isinstance(item_data.preview_text, str) else (item_data.preview_text[0] if item_data.preview_text else "")

    if allow_special_text:
        special_text_data = item_data.special_preview_text.get(location)
        if isinstance(special_text_data, list) and item is not None:
            try:
                index = item_data.index_getter(item)
                text = special_text_data[index]
            except (ValueError, IndexError):
                pass  # Keep the default text
        elif special_text_data is not None:
            text = special_text_data

    if item_type == Types.FakeItem:
        return getIceTrapText(text)
    elif item_type == Types.ArchipelagoItem and item == Items.TrapArchipelagoItem:
        return getIceTrapText(text)
    return text


item_shop_text_mapping = {
    # Kongs
    Items.Donkey: (BuyText.kong, NoBuyText.kong),
    Items.Diddy: (BuyText.kong, NoBuyText.kong),
    Items.Lanky: (BuyText.kong, NoBuyText.kong),
    Items.Tiny: (BuyText.kong, NoBuyText.kong),
    Items.Chunky: (BuyText.kong, NoBuyText.kong),
    Items.Cranky: (BuyText.kong, NoBuyText.kong),
    Items.Funky: (BuyText.kong, NoBuyText.kong),
    Items.Candy: (BuyText.kong, NoBuyText.kong),
    Items.Snide: (BuyText.kong, NoBuyText.kong),
    # Training
    Items.Vines: (BuyText.vine, NoBuyText.training_move),
    Items.Swim: (BuyText.dive, NoBuyText.training_move),
    Items.Oranges: (BuyText.orange, NoBuyText.training_move),
    Items.Barrels: (BuyText.barrel, NoBuyText.training_move),
    Items.Climbing: (BuyText.climb, NoBuyText.training_move),
    # Slams
    Items.ProgressiveSlam: (BuyText.slam, NoBuyText.slam),
    Items.ProgressiveSlam2: (BuyText.slam, NoBuyText.slam),
    Items.ProgressiveSlam3: (BuyText.slam, NoBuyText.slam),
    # Special Moves
    Items.BaboonBlast: (BuyText.blast, NoBuyText.special_move),
    Items.StrongKong: (BuyText.strong, NoBuyText.special_move),
    Items.GorillaGrab: (BuyText.grab, NoBuyText.special_move),
    Items.ChimpyCharge: (BuyText.charge, NoBuyText.special_move),
    Items.RocketbarrelBoost: (BuyText.rocket, NoBuyText.special_move),
    Items.SimianSpring: (BuyText.spring, NoBuyText.special_move),
    Items.Orangstand: (BuyText.ostand, NoBuyText.special_move),
    Items.BaboonBalloon: (BuyText.balloon, NoBuyText.special_move),
    Items.OrangstandSprint: (BuyText.sprint, NoBuyText.special_move),
    Items.MiniMonkey: (BuyText.mini, NoBuyText.special_move),
    Items.PonyTailTwirl: (BuyText.ptt, NoBuyText.special_move),
    Items.Monkeyport: (BuyText.port, NoBuyText.special_move),
    Items.HunkyChunky: (BuyText.hunky, NoBuyText.special_move),
    Items.PrimatePunch: (BuyText.punch, NoBuyText.special_move),
    Items.GorillaGone: (BuyText.gone, NoBuyText.special_move),
    # Guns
    Items.Coconut: (BuyText.coconut, NoBuyText.gun),
    Items.Peanut: (BuyText.peanut, NoBuyText.gun),
    Items.Grape: (BuyText.grape, NoBuyText.gun),
    Items.Feather: (BuyText.feather, NoBuyText.gun),
    Items.Pineapple: (BuyText.pineapple, NoBuyText.gun),
    # Gun Upgrades
    Items.HomingAmmo: (BuyText.homing, NoBuyText.gun_upgrade),
    Items.SniperSight: (BuyText.sniper, NoBuyText.gun_upgrade),
    Items.ProgressiveAmmoBelt: (BuyText.ammo_belt, NoBuyText.ammo_belt),
    Items.ProgressiveAmmoBelt2: (BuyText.ammo_belt, NoBuyText.ammo_belt),
    # Instruments
    Items.Bongos: (BuyText.bongos, NoBuyText.instrument),
    Items.Guitar: (BuyText.guitar, NoBuyText.instrument),
    Items.Trombone: (BuyText.trombone, NoBuyText.instrument),
    Items.Saxophone: (BuyText.sax, NoBuyText.instrument),
    Items.Triangle: (BuyText.triangle, NoBuyText.instrument),
    # Instrument Upgrades
    Items.ProgressiveInstrumentUpgrade: (BuyText.instrument_upgrade, NoBuyText.instrument),
    Items.ProgressiveInstrumentUpgrade2: (BuyText.instrument_upgrade, NoBuyText.instrument),
    Items.ProgressiveInstrumentUpgrade3: (BuyText.instrument_upgrade, NoBuyText.instrument),
    # Fairy Moves
    Items.Camera: (BuyText.camera, NoBuyText.fairy_move),
    Items.Shockwave: (BuyText.shockwave, NoBuyText.fairy_move),
    Items.CameraAndShockwave: (BuyText.camera_and_shockwave, NoBuyText.fairy_move),
    # Company Coins
    Items.NintendoCoin: (BuyText.nin_coin, NoBuyText.misc_item),
    Items.RarewareCoin: (BuyText.rw_coin, NoBuyText.misc_item),
    # Boss Keys
    Items.JungleJapesKey: (BuyText.key, NoBuyText.misc_item),
    Items.AngryAztecKey: (BuyText.key, NoBuyText.misc_item),
    Items.FranticFactoryKey: (BuyText.key, NoBuyText.misc_item),
    Items.GloomyGalleonKey: (BuyText.key, NoBuyText.misc_item),
    Items.FungiForestKey: (BuyText.key, NoBuyText.misc_item),
    Items.CrystalCavesKey: (BuyText.key, NoBuyText.misc_item),
    Items.CreepyCastleKey: (BuyText.key, NoBuyText.misc_item),
    Items.HideoutHelmKey: (BuyText.key, NoBuyText.misc_item),
    # Misc Items
    Items.GoldenBanana: (BuyText.golden_banana, NoBuyText.golden_banana),
    Items.BananaFairy: (BuyText.fairy, NoBuyText.misc_item),
    Items.BananaMedal: (BuyText.medal, NoBuyText.medal),
    Items.BattleCrown: (BuyText.crown, NoBuyText.misc_item),
    Items.Bean: (BuyText.bean, NoBuyText.misc_item),
    Items.Pearl: (BuyText.pearl, NoBuyText.misc_item),
    Items.FillerPearl: (BuyText.pearl, NoBuyText.misc_item),
    Items.FillerBanana: (BuyText.golden_banana, NoBuyText.golden_banana),
    Items.FillerFairy: (BuyText.fairy, NoBuyText.misc_item),
    Items.FillerCrown: (BuyText.crown, NoBuyText.misc_item),
    Items.FillerMedal: (BuyText.medal, NoBuyText.medal),
    # Ice Traps
    Items.IceTrapBubble: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapReverse: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlow: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapBubbleBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapReverseBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlowBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapBubbleKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapReverseKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlowKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableA: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableABean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableAKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableBBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableBKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableZ: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableZBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableZKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableCU: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableCUBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableCUKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapGetOutGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapGetOutBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapGetOutKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDryGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDryBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDryKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapFlipGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapFlipBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapFlipKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapBubbleFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapReverseFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlowFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableAFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableBFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableZFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableCUFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapGetOutFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDryFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapFlipFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapIceFloorGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapIceFloorBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapIceFloorKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapIceFloorFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapPaperGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapPaperBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapPaperKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapPaperFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlipGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlipBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlipKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlipFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapAnimalGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapAnimalBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapAnimalKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapAnimalFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapRockfallGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapRockfallBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapRockfallKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapRockfallFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableTagGB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableTagBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableTagKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableTagFairy: (BuyText.ice_trap, NoBuyText.misc_item),
    # Items not yet considered
    # Items.RainbowCoin: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.FillerRainbowCoin: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkCrystal: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkMelon: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkAmmo: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkFilm: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkOrange: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.ArchipelagoItem: (BuyText.blueprint, NoBuyText.misc_item),
    # Hints
    Items.JapesDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.JapesDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.JapesLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.JapesTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.JapesChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    # Blueprint
    Items.DonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.DiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.LankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.TinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.ChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
}

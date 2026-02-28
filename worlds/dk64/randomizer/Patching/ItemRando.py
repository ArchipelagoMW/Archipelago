"""Apply item rando changes."""

from randomizer.Enums.Maps import Maps
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Settings import ItemRandoListSelected, MicrohintsEnabled, TrainingBarrels, SpoilerHints
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Patching.Library.DataTypes import intf_to_float
from randomizer.Patching.Library.Generic import setItemReferenceName, ReqItems
from randomizer.Patching.Library.ItemRando import (
    getModelFromItem,
    getItemPreviewText,
    getPropFromItem,
    getModelMask,
    getItemDBEntry,
    item_shop_text_mapping,
    BuyText,
    TrackerItems,
    LocationSelection,
)
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames, CompTextFiles, ItemPreview
from randomizer.Patching.Library.ASM import getItemTableWriteAddress, populateOverlayOffsets, getSym, getROMAddress, Overlay, writeValue, patchBonus, getBonusIndex
from randomizer.Patching.Patcher import LocalROM
from randomizer.CompileHints import getHelmProgItems, GetRegionIdOfLocation
from randomizer.Lists.WrinklyHints import kong_list
import randomizer.ItemPool as ItemPool
import unicodedata

TRAINING_LOCATIONS = (
    Locations.IslesSwimTrainingBarrel,
    Locations.IslesVinesTrainingBarrel,
    Locations.IslesOrangesTrainingBarrel,
    Locations.IslesBarrelsTrainingBarrel,
)
THEMATIC_TEXT = True

kong_flags = (385, 6, 70, 66, 117)

subitems = (Items.JunkOrange, Items.JunkAmmo, Items.JunkCrystal, Items.JunkMelon, Items.JunkFilm)
shop_owner_types = (Types.Cranky, Types.Funky, Types.Snide, Types.Candy)


class TextboxChange:
    """Class to store information which pertains to a change of textbox information."""

    def __init__(
        self,
        location,
        file_index,
        textbox_index,
        text_replace,
        default_type: Types,
        default_item: Items,
        replacement_text="|",
        force_pipe=False,
    ):
        """Initialize with given paremeters."""
        self.location = location
        self.file_index = file_index
        self.textbox_index = textbox_index
        self.text_replace = text_replace  # Text which is going to be replaced with replacement_text
        self.replacement_text = replacement_text
        self.force_pipe = force_pipe  # If True, don't replace with item name upon checking later. Instead, will be replaced in RDRAM dynamically
        self.default_type = default_type
        self.default_item = default_item


textboxes = [
    TextboxChange(Locations.AztecTinyBeetleRace, 14, 0, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana, "\x04|\x04", True),
    TextboxChange(Locations.CavesLankyBeetleRace, 14, 0, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana, "\x04|\x04", True),
    TextboxChange(Locations.JapesDiddyMinecarts, CompTextFiles.PreviewsFlavor, ItemPreview.JapesMinecartIntro, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.JapesDiddyMinecarts, CompTextFiles.PreviewsFlavor, ItemPreview.JapesMinecartReward, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.JapesDiddyMinecarts, CompTextFiles.PreviewsFlavor, ItemPreview.JapesMinecartFail, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.ForestChunkyMinecarts, CompTextFiles.PreviewsFlavor, ItemPreview.FungiMinecartIntro, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.ForestChunkyMinecarts, CompTextFiles.PreviewsFlavor, ItemPreview.FungiMinecartFail, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.CastleDonkeyMinecarts, CompTextFiles.PreviewsFlavor, ItemPreview.CastleMinecartIntro, "BE A WINNER", Types.Banana, Items.GoldenBanana, "WIN A |"),
    TextboxChange(Locations.CastleDonkeyMinecarts, CompTextFiles.PreviewsFlavor, ItemPreview.CastleMinecartReward, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.IslesDonkeyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.IslesDiddyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.IslesLankyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.IslesTinyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.IslesChunkyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.FactoryTinyCarRace, CompTextFiles.PreviewsFlavor, ItemPreview.FactoryCarRace, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(
        Locations.GalleonTinyPearls,
        CompTextFiles.PreviewsFlavor,
        ItemPreview.MermaidIntro,
        "OF THEM BACK.",
        Types.Banana,
        Items.GoldenBanana,
        "OF THEM BACK. IF YOU HELP ME FIND THEM, I WILL REWARD YOU WITH A |",
    ),
    TextboxChange(Locations.GalleonTinyPearls, CompTextFiles.PreviewsFlavor, ItemPreview.MermaidReward, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(
        Locations.GalleonTinyPearls,
        CompTextFiles.PreviewsFlavor,
        ItemPreview.MermaidMissing,
        "ALTOGETHER.",
        Types.Banana,
        Items.GoldenBanana,
        "ALTOGETHER. IF YOU FIND THEM ALL, YOU WILL RECEIVE A |",
    ),
    TextboxChange(Locations.AztecDiddyVultureRace, CompTextFiles.PreviewsFlavor, ItemPreview.VulturePreview, "PRIZE", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.AztecDonkeyFreeLlama, CompTextFiles.PreviewsFlavor, ItemPreview.LlamaTalk, "ALL THIS SAND", Types.Banana, Items.GoldenBanana, "THIS |"),
    TextboxChange(Locations.AztecDonkeyFreeLlama, CompTextFiles.PreviewsFlavor, ItemPreview.LlamaRescue, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.RarewareCoin, CompTextFiles.PreviewsFlavor, ItemPreview.JetpacIntro, "RAREWARE COIN", Types.RarewareCoin, Items.RarewareCoin),  # Rareware Coin
    TextboxChange(Locations.RarewareCoin, CompTextFiles.PreviewsFlavor, ItemPreview.JetpacReward, "RAREWARE COIN", Types.RarewareCoin, Items.RarewareCoin),  # Rareware Coin
    TextboxChange(Locations.ForestLankyRabbitRace, CompTextFiles.PreviewsFlavor, ItemPreview.RabbitFinalRaceIntro, "TROPHY", Types.Banana, Items.GoldenBanana, "| TROPHY"),
    TextboxChange(Locations.ForestLankyRabbitRace, CompTextFiles.PreviewsFlavor, ItemPreview.RabbitFirstRaceReward, "TROPHY", Types.Banana, Items.GoldenBanana, "| TROPHY"),
    TextboxChange(Locations.ForestLankyRabbitRace, CompTextFiles.PreviewsFlavor, ItemPreview.RabbitFinalRaceReward, "TROPHY", Types.Banana, Items.GoldenBanana, "| TROPHY"),
    TextboxChange(Locations.ForestChunkyApple, CompTextFiles.PreviewsFlavor, ItemPreview.AppleIntro, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.ForestChunkyApple, CompTextFiles.PreviewsFlavor, ItemPreview.ApplePickUp, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.ForestChunkyApple, CompTextFiles.PreviewsFlavor, ItemPreview.AppleReward, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.GalleonDonkeySealRace, CompTextFiles.PreviewsFlavor, ItemPreview.Seal, "CHEST O' GOLD", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.RarewareBanana, CompTextFiles.PreviewsFlavor, ItemPreview.RarewareGB, "REWARD ANYONE", Types.Banana, Items.GoldenBanana, "REWARD ANYONE WITH A |"),
    TextboxChange(Locations.CavesLankyCastle, CompTextFiles.PreviewsFlavor, ItemPreview.IceTomato, "HOW ABOUT IT", Types.Banana, Items.GoldenBanana, "HOW ABOUT A |"),
    TextboxChange(Locations.CastleTinyCarRace, CompTextFiles.PreviewsFlavor, ItemPreview.CastleCarRace, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(
        Locations.ForestDiddyOwlRace,
        CompTextFiles.PreviewsFlavor,
        ItemPreview.OwlRace,
        "WHEN YOU CAN FLY",
        Types.Banana,
        Items.GoldenBanana,
        "WHEN YOU CAN FLY TO HAVE A CHANCE TO RECEIVE A |",
    ),
    TextboxChange(Locations.ForestTinySpiderBoss, CompTextFiles.PreviewsFlavor, ItemPreview.SpiderIntro, "\x04GOLDEN BANANA\x04", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.CavesChunky5DoorIgloo, CompTextFiles.PreviewsFlavor, ItemPreview.ChunkyIgloo, "\x04GOLDEN BANANA\x04", Types.Banana, Items.GoldenBanana),
]

level_names = {
    Levels.JungleJapes: "Jungle Japes",
    Levels.AngryAztec: "Angry Aztec",
    Levels.FranticFactory: "Frantic Factory",
    Levels.GloomyGalleon: "Gloomy Galleon",
    Levels.FungiForest: "Fungi Forest",
    Levels.CrystalCaves: "Crystal Caves",
    Levels.CreepyCastle: "Creepy Castle",
    Levels.DKIsles: "DK Isles",
    Levels.HideoutHelm: "Hideout Helm",
}

kong_names = {
    Kongs.donkey: "Donkey Kong",
    Kongs.diddy: "Diddy",
    Kongs.lanky: "Lanky",
    Kongs.tiny: "Tiny",
    Kongs.chunky: "Chunky",
    Kongs.any: "Any Kong",
}


class ItemPatchingInfo:
    """Class to store information regarding how an item is patched into ROM."""

    def __init__(self, response_type: int, level: int = 0, kong: int = 0, audiovisual_medal: int = 0):
        """Initialize with given parameters."""
        self.response_type = response_type
        self.level = level
        self.kong = kong
        self.audiovisual_medal = audiovisual_medal


def getItemPatchingFromList(list_set: list, item: Items, type_str: str, throw_error: bool = True):
    """Get the move index from a list."""
    if item not in list_set:
        if throw_error:
            raise Exception(f"{type_str} Type provided, but invalid {type_str} item provided resulting in search mismatch")
        return None
    return list_set.index(item)


ice_trap_data = [
    [Items.IceTrapBubble, Items.IceTrapBubbleBean, Items.IceTrapBubbleKey, Items.IceTrapBubbleFairy],
    [Items.IceTrapReverse, Items.IceTrapReverseBean, Items.IceTrapReverseKey, Items.IceTrapReverseFairy],
    [Items.IceTrapSlow, Items.IceTrapSlowBean, Items.IceTrapSlowKey, Items.IceTrapSlowFairy],
    [],  # Super Bubble
    [Items.IceTrapDisableA, Items.IceTrapDisableABean, Items.IceTrapDisableAKey, Items.IceTrapDisableAFairy],
    [Items.IceTrapDisableB, Items.IceTrapDisableBBean, Items.IceTrapDisableBKey, Items.IceTrapDisableBFairy],
    [Items.IceTrapDisableZ, Items.IceTrapDisableZBean, Items.IceTrapDisableZKey, Items.IceTrapDisableZFairy],
    [Items.IceTrapDisableCU, Items.IceTrapDisableCUBean, Items.IceTrapDisableCUKey, Items.IceTrapDisableCUFairy],
    [Items.IceTrapGetOutGB, Items.IceTrapGetOutBean, Items.IceTrapGetOutKey, Items.IceTrapGetOutFairy],
    [Items.IceTrapDryGB, Items.IceTrapDryBean, Items.IceTrapDryKey, Items.IceTrapDryFairy],
    [Items.IceTrapFlipGB, Items.IceTrapFlipBean, Items.IceTrapFlipKey, Items.IceTrapFlipFairy],
    [Items.IceTrapIceFloorGB, Items.IceTrapIceFloorBean, Items.IceTrapIceFloorKey, Items.IceTrapIceFloorFairy],
    [Items.IceTrapPaperGB, Items.IceTrapPaperBean, Items.IceTrapPaperKey, Items.IceTrapPaperFairy],
    [Items.IceTrapSlipGB, Items.IceTrapSlipBean, Items.IceTrapSlipKey, Items.IceTrapSlipFairy],
    [],  # Instant Slip
    [Items.IceTrapAnimalGB, Items.IceTrapAnimalBean, Items.IceTrapAnimalKey, Items.IceTrapAnimalFairy],
    [Items.IceTrapRockfallGB, Items.IceTrapRockfallBean, Items.IceTrapRockfallKey, Items.IceTrapRockfallFairy],
    [Items.IceTrapDisableTagGB, Items.IceTrapDisableTagBean, Items.IceTrapDisableTagKey, Items.IceTrapDisableTagFairy],
]


def getItemPatchingData(item_type: Types, item: Items, kong_override: int = None) -> ItemPatchingInfo:
    """Get the data associated with how an item is patched into ROM from various attributes."""
    simple_types = {
        Types.Banana: ReqItems.GoldenBanana,
        Types.Fairy: ReqItems.Fairy,
        Types.Crown: ReqItems.Crown,
        Types.Medal: ReqItems.Medal,
        Types.Bean: ReqItems.Bean,
        Types.Pearl: ReqItems.Pearl,
        Types.RainbowCoin: ReqItems.RainbowCoin,
        Types.JunkItem: ReqItems.JunkItem,
        Types.FillerBanana: ReqItems.GoldenBanana,
        Types.FillerFairy: ReqItems.Fairy,
        Types.FillerCrown: ReqItems.Crown,
        Types.FillerMedal: ReqItems.Medal,
        Types.FillerPearl: ReqItems.Pearl,
        Types.FillerRainbowCoin: ReqItems.RainbowCoin,
    }
    if item_type in simple_types:
        return ItemPatchingInfo(simple_types[item_type])
    elif item_type == Types.NintendoCoin:
        return ItemPatchingInfo(ReqItems.CompanyCoin, 0, 0)
    elif item_type == Types.RarewareCoin:
        return ItemPatchingInfo(ReqItems.CompanyCoin, 0, 1)
    elif item_type == Types.Key:
        key_index = getItemPatchingFromList(ItemPool.Keys(), item, "Key")
        return ItemPatchingInfo(ReqItems.Key, key_index)
    elif item_type == Types.FakeItem:
        for effect_index, idx_lst in enumerate(ice_trap_data):
            if item in idx_lst:
                return ItemPatchingInfo(ReqItems.IceTrap, idx_lst.index(item), effect_index + 1)
        raise Exception("Ice Trap Type provided, but invalid Ice Trap item provided resulting in search mismatch")
    elif item_type == Types.Blueprint:
        return ItemPatchingInfo(ReqItems.Blueprint, 0, item - Items.DonkeyBlueprint)
    elif item_type == Types.Kong:
        kong_lst = [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]
        kong_index = getItemPatchingFromList(kong_lst, item, "Kong")
        return ItemPatchingInfo(ReqItems.Kong, 0, kong_index)
    elif item_type in (Types.Hint, Types.ProgressiveHint):
        hint_index = getItemPatchingFromList(ItemPool.HintItems(), item, "Hint")
        hint_level = int(hint_index / 5)
        hint_kong = hint_index % 5
        return ItemPatchingInfo(ReqItems.Hint, hint_level, hint_kong)
    elif item_type in (Types.Shockwave, Types.Shop, Types.Climbing, Types.TrainingBarrel):
        # Special Moves
        idx_lst = [Items.BaboonBlast, Items.ChimpyCharge, Items.Orangstand, Items.MiniMonkey, Items.HunkyChunky]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(ReqItems.Move, 0, idx, 1)
        idx_lst = [Items.StrongKong, Items.RocketbarrelBoost, Items.BaboonBalloon, Items.PonyTailTwirl, Items.PrimatePunch]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(ReqItems.Move, 1, idx, 1)
        idx_lst = [Items.GorillaGrab, Items.SimianSpring, Items.OrangstandSprint, Items.Monkeyport, Items.GorillaGone]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(ReqItems.Move, 2, idx, 1)
        # Slam
        if item in [Items.ProgressiveSlam, Items.ProgressiveSlam2, Items.ProgressiveSlam3]:
            return ItemPatchingInfo(ReqItems.Move, 3, 0, 1)
        # Gun
        idx_lst = [Items.Coconut, Items.Peanut, Items.Grape, Items.Feather, Items.Pineapple]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(ReqItems.Move, 4, idx, 2)
        # Homing/Sniper
        if item == Items.HomingAmmo:
            return ItemPatchingInfo(ReqItems.Move, 5, 2)
        if item == Items.SniperSight:
            return ItemPatchingInfo(ReqItems.Move, 6, 2)
        # Ammo Belt
        if item in (Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt2):
            return ItemPatchingInfo(ReqItems.Move, 7, 2)
        # Instrument
        idx_lst = [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(ReqItems.Move, 8, idx, 3)
        # Progressive Instrument Upgrades
        if item in (Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3):
            return ItemPatchingInfo(ReqItems.Move, 9, 0, 3)
        # Misc flag moves
        idx_lst = [Items.Swim, Items.Oranges, Items.Barrels, Items.Vines, Items.Camera, Items.Shockwave]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            visual_index = 1
            if item == Items.Camera:
                visual_index = 4
            elif item == Items.Shockwave:
                visual_index = 5
            return ItemPatchingInfo(ReqItems.Move, 10, idx, visual_index)
        # Climbing
        if item == Items.Climbing:
            return ItemPatchingInfo(ReqItems.Move, 11, 0, 1)
        # Camera Combo
        if item == Items.CameraAndShockwave:
            return ItemPatchingInfo(ReqItems.Move, 12, 0, 1)
        raise Exception("Could not find valid move")
    elif item is None or item == Items.NoItem or item_type is None or item_type == Types.NoItem:
        return ItemPatchingInfo(0)
    elif item_type in (Types.Cranky, Types.Funky, Types.Candy, Types.Snide):
        shopkeeper_lst = [Items.Cranky, Items.Funky, Items.Candy, Items.Snide]
        shopkeeper_index = getItemPatchingFromList(shopkeeper_lst, item, "Shopkeeper")
        return ItemPatchingInfo(ReqItems.Shopkeeper, 0, shopkeeper_index)
    elif item_type == Types.ArchipelagoItem:
        arch_item_list = (
            Items.ArchipelagoItem,
            Items.SpecialArchipelagoItem,
            Items.FoolsArchipelagoItem,
            Items.TrapArchipelagoItem,
        )
        # Use kong_override if provided to differentiate AP items in shops
        kong_value = kong_override if kong_override is not None else 0
        return ItemPatchingInfo(ReqItems.ArchipelagoItem, arch_item_list.index(item), kong_value)
    raise Exception(f"Invalid item for patching: {item_type.name}, {item}")


def appendTextboxChange(spoiler, file_index: int, textbox_index: int, search: str, target: str):
    """Alter a specific textbox."""
    data = {"textbox_index": textbox_index, "mode": "replace", "search": search, "target": target}
    if file_index in spoiler.text_changes:
        spoiler.text_changes[file_index].append(data)
    else:
        spoiler.text_changes[file_index] = [data]


def writeBuyText(item: Items, address: int, ROM_COPY: LocalROM):
    """Write the buy text to the world based on the item."""
    ROM_COPY.seek(address)
    if item is None or item == Items.NoItem:
        ROM_COPY.writeMultipleBytes(0, 2)
        return
    data = item_shop_text_mapping.get(item, (0, 0))
    ROM_COPY.write(data[0])
    ROM_COPY.write(data[1] + BuyText.terminator)


COUNT_STRUCT_SIZE = 0x1E
KONG_STRUCT_SIZE = 0x3
EXTRA_STRUCT_OFFSET = COUNT_STRUCT_SIZE + (5 * KONG_STRUCT_SIZE)
TRACKER_ITEM_PAIRING = {
    TrackerItems.COCONUT: {
        "item": Items.Coconut,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.donkey * KONG_STRUCT_SIZE) + 1, "mode": "or", "value": 1}],
    },
    TrackerItems.BONGOS: {
        "item": Items.Bongos,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.donkey * KONG_STRUCT_SIZE) + 2, "mode": "or", "value": 1}],
    },
    TrackerItems.GRAB: {
        "item": Items.GorillaGrab,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.donkey * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 4}],
    },
    TrackerItems.STRONG: {
        "item": Items.StrongKong,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.donkey * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 2}],
    },
    TrackerItems.BLAST: {
        "item": Items.BaboonBlast,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.donkey * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 1}],
    },
    TrackerItems.PEANUT: {
        "item": Items.Peanut,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.diddy * KONG_STRUCT_SIZE) + 1, "mode": "or", "value": 1}],
    },
    TrackerItems.GUITAR: {
        "item": Items.Guitar,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.diddy * KONG_STRUCT_SIZE) + 2, "mode": "or", "value": 1}],
    },
    TrackerItems.CHARGE: {
        "item": Items.ChimpyCharge,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.diddy * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 1}],
    },
    TrackerItems.ROCKET: {
        "item": Items.RocketbarrelBoost,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.diddy * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 2}],
    },
    TrackerItems.SPRING: {
        "item": Items.SimianSpring,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.diddy * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 4}],
    },
    TrackerItems.GRAPE: {
        "item": Items.Grape,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.lanky * KONG_STRUCT_SIZE) + 1, "mode": "or", "value": 1}],
    },
    TrackerItems.TROMBONE: {
        "item": Items.Trombone,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.lanky * KONG_STRUCT_SIZE) + 2, "mode": "or", "value": 1}],
    },
    TrackerItems.OSTAND: {
        "item": Items.Orangstand,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.lanky * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 1}],
    },
    TrackerItems.OSPRINT: {
        "item": Items.OrangstandSprint,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.lanky * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 4}],
    },
    TrackerItems.BALLOON: {
        "item": Items.BaboonBalloon,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.lanky * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 2}],
    },
    TrackerItems.FEATHER: {
        "item": Items.Feather,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.tiny * KONG_STRUCT_SIZE) + 1, "mode": "or", "value": 1}],
    },
    TrackerItems.SAX: {
        "item": Items.Saxophone,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.tiny * KONG_STRUCT_SIZE) + 2, "mode": "or", "value": 1}],
    },
    TrackerItems.PTT: {
        "item": Items.PonyTailTwirl,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.tiny * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 2}],
    },
    TrackerItems.MINI: {
        "item": Items.MiniMonkey,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.tiny * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 1}],
    },
    TrackerItems.MONKEYPORT: {
        "item": Items.Monkeyport,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.tiny * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 4}],
    },
    TrackerItems.PINEAPPLE: {
        "item": Items.Pineapple,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.chunky * KONG_STRUCT_SIZE) + 1, "mode": "or", "value": 1}],
    },
    TrackerItems.TRIANGLE: {
        "item": Items.Triangle,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.chunky * KONG_STRUCT_SIZE) + 2, "mode": "or", "value": 1}],
    },
    TrackerItems.PUNCH: {
        "item": Items.PrimatePunch,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.chunky * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 2}],
    },
    TrackerItems.HUNKY: {
        "item": Items.HunkyChunky,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.chunky * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 1}],
    },
    TrackerItems.GONE: {
        "item": Items.GorillaGone,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (Kongs.chunky * KONG_STRUCT_SIZE) + 0, "mode": "or", "value": 4}],
    },
    TrackerItems.HOMING: {
        "item": Items.HomingAmmo,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (x * KONG_STRUCT_SIZE) + 1, "mode": "or", "value": 2} for x in range(5)],
    },
    TrackerItems.SNIPER: {
        "item": Items.SniperSight,
        "packets": [{"offset": COUNT_STRUCT_SIZE + (x * KONG_STRUCT_SIZE) + 1, "mode": "or", "value": 4} for x in range(5)],
    },
    TrackerItems.DIVE: {
        "item": Items.Swim,
        "packets": [{"offset": 0x18, "mode": "or", "value": 0x80}],
    },
    TrackerItems.ORANGE: {
        "item": Items.Oranges,
        "packets": [{"offset": 0x18, "mode": "or", "value": 0x40}],
    },
    TrackerItems.BARREL: {
        "item": Items.Barrels,
        "packets": [{"offset": 0x18, "mode": "or", "value": 0x20}],
    },
    TrackerItems.VINE: {
        "item": Items.Vines,
        "packets": [{"offset": 0x18, "mode": "or", "value": 0x10}],
    },
    TrackerItems.CAMERA: {
        "item": Items.Camera,
        "packets": [{"offset": 0x18, "mode": "or", "value": 0x8}],
    },
    TrackerItems.SHOCKWAVE: {
        "item": Items.Shockwave,
        "packets": [{"offset": 0x18, "mode": "or", "value": 0x4}],
    },
    TrackerItems.CLIMB: {
        "item": Items.Climbing,
        "packets": [{"offset": EXTRA_STRUCT_OFFSET + 3, "mode": "set", "value": 1}],
    },
}
TRACKER_SHOPKEEPER_PAIRING = {
    TrackerItems.CRANKY: Items.Cranky,
    TrackerItems.FUNKY: Items.Funky,
    TrackerItems.CANDY: Items.Candy,
    TrackerItems.SNIDE: Items.Snide,
}


def calculateInitFileScreen(spoiler, ROM_COPY: LocalROM):
    """Calculate the items that need to be shown on the file screen for a new file, as well as the struct to give starting items."""
    OTHER_STARTING_ITEMS = {
        Locations.IslesVinesTrainingBarrel: Items.Vines,
        Locations.IslesSwimTrainingBarrel: Items.Swim,
        Locations.IslesOrangesTrainingBarrel: Items.Oranges,
        Locations.IslesBarrelsTrainingBarrel: Items.Barrels,
        Locations.ShopOwner_Location00: Items.Cranky,
        Locations.ShopOwner_Location01: Items.Funky,
        Locations.ShopOwner_Location02: Items.Candy,
        Locations.ShopOwner_Location03: Items.Snide,
    }
    if (not spoiler.settings.fast_start_beginning_of_game) or spoiler.settings.archipelago:
        del OTHER_STARTING_ITEMS[Locations.IslesVinesTrainingBarrel]
        del OTHER_STARTING_ITEMS[Locations.IslesSwimTrainingBarrel]
        del OTHER_STARTING_ITEMS[Locations.IslesOrangesTrainingBarrel]
        del OTHER_STARTING_ITEMS[Locations.IslesBarrelsTrainingBarrel]
    elif spoiler.settings.training_barrels != TrainingBarrels.normal:
        # If the training barrels are inaccessible, remove them from starting items to avoid errant training moves
        if spoiler.LocationList[Locations.IslesVinesTrainingBarrel].inaccessible:
            del OTHER_STARTING_ITEMS[Locations.IslesVinesTrainingBarrel]
        if spoiler.LocationList[Locations.IslesSwimTrainingBarrel].inaccessible:
            del OTHER_STARTING_ITEMS[Locations.IslesSwimTrainingBarrel]
        if spoiler.LocationList[Locations.IslesOrangesTrainingBarrel].inaccessible:
            del OTHER_STARTING_ITEMS[Locations.IslesOrangesTrainingBarrel]
        if spoiler.LocationList[Locations.IslesBarrelsTrainingBarrel].inaccessible:
            del OTHER_STARTING_ITEMS[Locations.IslesBarrelsTrainingBarrel]
    found_shopkeeper = False
    if spoiler.settings.shuffle_items:
        for item in spoiler.item_assignment:
            if item.location >= Locations.ShopOwner_Location00 and item.location <= Locations.ShopOwner_Location03:
                found_shopkeeper = True
            if item.can_have_item:
                if item.location in list(OTHER_STARTING_ITEMS.keys()):
                    OTHER_STARTING_ITEMS[item.location] = item.new_item
    if not found_shopkeeper and ItemRandoListSelected.shopowners in spoiler.settings.item_rando_list_selected:
        OTHER_STARTING_ITEMS[Locations.ShopOwner_Location00] = Items.NoItem
        OTHER_STARTING_ITEMS[Locations.ShopOwner_Location01] = Items.NoItem
        OTHER_STARTING_ITEMS[Locations.ShopOwner_Location02] = Items.NoItem
        OTHER_STARTING_ITEMS[Locations.ShopOwner_Location03] = Items.NoItem
    starting_slam_level = 0
    starting_belt_level = 0
    starting_ins_upg_level = 0
    has_melon_2 = False
    starting_items = list(OTHER_STARTING_ITEMS.values()) + spoiler.pregiven_items
    for item in starting_items:
        if item in (Items.ProgressiveSlam, Items.ProgressiveSlam2, Items.ProgressiveSlam3):
            starting_slam_level += 1
        elif item in (Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt2):
            starting_belt_level += 1
        elif item in (Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3):
            starting_ins_upg_level += 1
            has_melon_2 = True
        elif item in (Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle):
            has_melon_2 = True
    offset_dict = populateOverlayOffsets(ROM_COPY)
    base_addr = getROMAddress(getSym("pregiven_status"), Overlay.Custom, offset_dict)
    starting_move_packets = []
    for x in range(TrackerItems.TERMINATOR):
        value = 0
        give_move_packets = []
        if x in TRACKER_ITEM_PAIRING:
            checked_items = [TRACKER_ITEM_PAIRING[x]["item"]]
            if x in (TrackerItems.CAMERA, TrackerItems.SHOCKWAVE):
                checked_items.append(Items.CameraAndShockwave)
            for checked_item in checked_items:
                if checked_item in starting_items:
                    value = 1
                    give_move_packets.extend(TRACKER_ITEM_PAIRING[x]["packets"])
        elif x in [TrackerItems.SLAM, TrackerItems.SLAM_HAS]:
            value = starting_slam_level
            give_move_packets.append({"offset": EXTRA_STRUCT_OFFSET + 1, "mode": "set", "value": starting_slam_level})
        elif x == TrackerItems.MELON_2:
            if has_melon_2:
                value = 1
        elif x == TrackerItems.MELON_3:
            if starting_ins_upg_level > 1:
                value = 1
        elif x == TrackerItems.INSUPG_1:
            if starting_ins_upg_level > 0:
                value = 1
        elif x == TrackerItems.INSUPG_2:
            if starting_ins_upg_level > 2:
                value = 1
        elif x == TrackerItems.BELT_1:
            if starting_belt_level > 0:
                value = 1
        elif x == TrackerItems.BELT_2:
            if starting_belt_level > 1:
                value = 1
        elif x == TrackerItems.AMMOBELT:
            value = starting_belt_level
        elif x == TrackerItems.INSTRUMENT_UPG:
            if starting_ins_upg_level > 2:
                value = 2
            elif starting_ins_upg_level > 0:
                value = 1
        elif x >= TrackerItems.KEY1 and x <= TrackerItems.KEY8:
            keys_turned_in = [0, 1, 2, 3, 4, 5, 6, 7]
            if len(spoiler.settings.krool_keys_required) > 0:
                for key in spoiler.settings.krool_keys_required:
                    key_index = key - 4
                    if key_index in keys_turned_in:
                        keys_turned_in.remove(key_index)
            key = x - TrackerItems.KEY1
            if key in keys_turned_in:
                value = 1
                give_move_packets.append({"offset": 0xA, "mode": "or", "value": 1 << key})
        elif x in list(TRACKER_SHOPKEEPER_PAIRING.keys()):
            matching_item = TRACKER_SHOPKEEPER_PAIRING[x]
            if matching_item in list(OTHER_STARTING_ITEMS.values()):
                value = 1
        ROM_COPY.seek(base_addr + x)
        ROM_COPY.writeMultipleBytes(value, 1)
        starting_move_packets.extend(give_move_packets)
    # Melons
    melon_count = 1
    if starting_ins_upg_level > 1:
        melon_count = 3
    elif has_melon_2:
        melon_count = 2
    starting_move_packets.append({"offset": EXTRA_STRUCT_OFFSET + 0, "mode": "set", "value": melon_count})
    # Instrument Upgrades
    if starting_ins_upg_level > 0:
        starting_move_packets.extend([{"offset": COUNT_STRUCT_SIZE + (x * KONG_STRUCT_SIZE) + 2, "mode": "or", "value": (2 << starting_ins_upg_level) - 2} for x in range(5)])
    # Belts
    starting_move_packets.append({"offset": EXTRA_STRUCT_OFFSET + 2, "mode": "set", "value": starting_belt_level})
    # Kongs
    # Unlock All Kongs
    kong_items = [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]
    starting_kongs = []
    if spoiler.settings.starting_kongs_count == 5:
        starting_move_packets.append({"offset": 0xB, "mode": "set", "value": 0x1F})
        starting_kongs = kong_items.copy()
    else:
        bin_value = 0
        for x in spoiler.settings.starting_kong_list:
            bin_value |= 1 << x
            starting_kongs.append(kong_items[x])
        starting_move_packets.append({"offset": 0xB, "mode": "set", "value": bin_value})
    for kong in starting_kongs:
        setItemReferenceName(spoiler, kong, 0, "Starting Kong", 0)

    # Starting moves writer
    starting_item_base_addr = getROMAddress(getSym("starting_item_data"), Overlay.Custom, offset_dict)
    ROM_COPY.seek(starting_item_base_addr)
    for _ in range(EXTRA_STRUCT_OFFSET + 4):
        ROM_COPY.writeMultipleBytes(0, 1)  # Clear cache
    for packet in starting_move_packets:
        ROM_COPY.seek(starting_item_base_addr + packet["offset"])
        mode = packet["mode"]
        value = packet["value"]
        size = packet.get("size", 1)
        if mode == "set":
            ROM_COPY.writeMultipleBytes(value, size)
        else:
            old_value = int.from_bytes(ROM_COPY.readBytes(size), "big")
            ROM_COPY.seek(starting_item_base_addr + packet["offset"])
            if mode == "add":
                ROM_COPY.writeMultipleBytes(value + old_value, size)
            elif mode == "or":
                ROM_COPY.writeMultipleBytes(old_value | value, size)


NUMBERS_AS_WORDS = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE"]

HOLDABLE_LOCATION_INFO = {
    Locations.HoldableBoulderIslesNearAztec: {
        "map_id": Maps.Isles,
        "spawner_id": 12,
    },
    Locations.HoldableBoulderIslesNearCaves: {
        "map_id": Maps.Isles,
        "spawner_id": 13,
    },
    Locations.HoldableBoulderAztec: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 4,
    },
    Locations.HoldableBoulderCavesSmall: {
        "map_id": Maps.CrystalCaves,
        "spawner_id": 0,
    },
    Locations.HoldableBoulderCavesLarge: {
        "map_id": Maps.CrystalCaves,
        "spawner_id": 1,
    },
    Locations.HoldableBoulderMuseum: {
        "map_id": Maps.CastleMuseum,
        "spawner_id": 0,
    },
    Locations.HoldableBoulderJapesLobby: {
        "map_id": Maps.JungleJapesLobby,
        "spawner_id": 2,
    },
    Locations.HoldableBoulderCastleLobby: {
        "map_id": Maps.CreepyCastleLobby,
        "spawner_id": 0,
    },
    Locations.HoldableBoulderCavesLobby: {
        "map_id": Maps.CrystalCavesLobby,
        "spawner_id": 5,
    },
    Locations.HoldableKegMillFrontNear: {
        "map_id": Maps.ForestMillFront,
        "spawner_id": 5,
    },
    Locations.HoldableKegMillFrontFar: {
        "map_id": Maps.ForestMillFront,
        "spawner_id": 7,
    },
    Locations.HoldableKegMillRear: {
        "map_id": Maps.ForestMillBack,
        "spawner_id": 4,
    },
    Locations.HoldableVaseCircle: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 3,
    },
    Locations.HoldableVaseColon: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 2,
    },
    Locations.HoldableVaseTriangle: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 1,
    },
    Locations.HoldableVasePlus: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 0,
    },
}


def alterTextboxRequirements(spoiler):
    """Alters various textboxes based on the requirement count changing."""
    pearl_req = spoiler.settings.mermaid_gb_pearls
    for file in [CompTextFiles.PreviewsFlavor, CompTextFiles.PreviewsNormal]:
        appendTextboxChange(spoiler, file, ItemPreview.MermaidMissing, "FIVE MISSING PEARLS", f"{NUMBERS_AS_WORDS[pearl_req]} MISSING PEARL{'S' if pearl_req != 1 else ''}")
    all_text = ""
    if pearl_req == 5:
        all_text = "ALL "
    plea_including_pearl_count = f"PLEASE TRY AND GET {all_text}{NUMBERS_AS_WORDS[pearl_req]} OF THEM BACK"
    for x in textboxes:
        if x.location == Locations.GalleonTinyPearls and x.textbox_index == ItemPreview.MermaidIntro:
            x.text_replace = plea_including_pearl_count
            x.replacement_text = f"IF YOU HELP ME FIND {all_text}{NUMBERS_AS_WORDS[pearl_req]} OF THEM, I WILL REWARD YOU WITH A |"
    for file in [CompTextFiles.PreviewsFlavor, CompTextFiles.PreviewsNormal]:
        appendTextboxChange(spoiler, file, ItemPreview.MermaidIntro, "PLEASE TRY AND GET THEM BACK", plea_including_pearl_count)
    fairy_req = spoiler.settings.rareware_gb_fairies
    if fairy_req != 20:
        for file in [CompTextFiles.PreviewsFlavor, CompTextFiles.PreviewsNormal]:
            appendTextboxChange(spoiler, file, ItemPreview.RarewareGB, "FIND THEM ALL", f"FIND {fairy_req} OF THEM")
        appendTextboxChange(spoiler, 40, 0, "RESCUED ALL THE BANANA FAIRIES", "RESCUED THE BANANA FAIRIES")
    appendTextboxChange(spoiler, 40, 4, "MUST GET FAIRIES", f"MUST GET {fairy_req} FAIRIES")


def pushItemMicrohints(spoiler):
    """Push hint for the micro-hints system."""
    helm_prog_items = getHelmProgItems(spoiler)
    hinted_items = [
        # Key = Item, Value = (Textbox index in text file 19, (all_accepted_settings))
        (helm_prog_items[0], ItemPreview.PortMicro, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (helm_prog_items[1], ItemPreview.GoneMicro, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Bongos, ItemPreview.BongosMicro, [MicrohintsEnabled.all]),
        (Items.Triangle, ItemPreview.TriangleMicro, [MicrohintsEnabled.all]),
        (Items.Saxophone, ItemPreview.SaxMicro, [MicrohintsEnabled.all]),
        (Items.Trombone, ItemPreview.TromboneMicro, [MicrohintsEnabled.all]),
        (Items.Guitar, ItemPreview.GuitarMicro, [MicrohintsEnabled.all]),
        (Items.ProgressiveSlam, ItemPreview.SlamMicro, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Cranky, ItemPreview.CrankyMicro, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Funky, ItemPreview.FunkyMicro, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Candy, ItemPreview.CandyMicro, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Snide, ItemPreview.SnideMicro, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
    ]
    for item_hint, item_data in enumerate(hinted_items):
        if spoiler.settings.microhints_enabled in list(item_data[2]):
            if ItemList[item_data[0]].name in spoiler.microhints:
                data = {
                    "textbox_index": item_data[1],
                    "mode": "replace_whole",
                    "target": spoiler.microhints[ItemList[item_data[0]].name],
                }
                for file in [CompTextFiles.PreviewsFlavor, CompTextFiles.PreviewsNormal]:
                    if file in spoiler.text_changes:
                        spoiler.text_changes[file].append(data)
                    else:
                        spoiler.text_changes[file] = [data]


def writeNullShopSlot(ROM_COPY: LocalROM, location: int):
    """Write an empty shop slot."""
    ROM_COPY.seek(location)
    for _ in range(3):
        ROM_COPY.writeMultipleBytes(0, 2)


def writeShopData(ROM_COPY: LocalROM, location: int, ipd: ItemPatchingInfo, price: int):
    """Write shop data to slot."""
    if ipd is not None:
        ROM_COPY.seek(location)
        ROM_COPY.writeMultipleBytes(ipd.response_type, 1)
        ROM_COPY.writeMultipleBytes(ipd.level, 1)
        ROM_COPY.writeMultipleBytes(ipd.kong, 1)
        ROM_COPY.writeMultipleBytes(ipd.audiovisual_medal, 1)
    ROM_COPY.seek(location + 4)
    ROM_COPY.writeMultipleBytes(0, 1)  # Pad
    ROM_COPY.writeMultipleBytes(price, 1)


def getHintKongFromFlag(flag: int) -> int:
    """Get the kong associated with a hint from it's flag."""
    return (flag - 0x384) % 5


def setItemInWorld(ROM_COPY: LocalROM, offset: int, base_flag: int, current_flag: int):
    """Write item to world array."""
    delta = current_flag - base_flag
    flag_offset = delta >> 3
    flag_shift = delta & 7
    ROM_COPY.seek(offset + flag_offset)
    raw = int.from_bytes(ROM_COPY.readBytes(1), "big")
    ROM_COPY.seek(offset + flag_offset)
    ROM_COPY.writeMultipleBytes(raw | (1 << flag_shift), 1)


def getActorIndex(item):
    """Get actor index from item."""
    item_type = item.new_type
    if item_type is None:
        item_type = Types.NoItem
    index = getItemDBEntry(item_type).index_getter(item.new_item)
    return getItemDBEntry(item_type).actor_index[index]


model_two_items = [
    0x74,  # GB
    0xDE,  # BP - DK
    0xE0,  # BP - Diddy
    0xE1,  # BP - Lanky
    0xDD,  # BP - Tiny
    0xDF,  # BP - Chunky
    0x48,  # Nintendo Coin
    0x28F,  # Rareware Coin
    0x13C,  # Key
    0x18D,  # Crown
    0x90,  # Medal
    0x288,  # Rareware GB
    0x198,  # Bean
    0x1B4,  # Pearls
]

POINTER_ROM_ENEMIES = 0x1FF9000


def normalize_location_name(name: str):
    """Normalize a location name so it can be patched in."""
    res = "".join([x for xi, x in enumerate([*name]) if x != "\n" and xi < 30])
    res = unicodedata.normalize("NFKD", res)
    res = "".join(char for char in res if char.isascii())
    return res


def place_randomized_items(spoiler, ROM_COPY: LocalROM):
    """Place randomized items into ROM."""
    sav = spoiler.settings.rom_data
    ROM_COPY.seek(sav + 0x1EC)
    ROM_COPY.writeMultipleBytes(0xF0, 1)
    spoiler.japes_rock_actor = 45
    spoiler.aztec_vulture_actor = 45
    FAST_START = spoiler.settings.fast_start_beginning_of_game
    if spoiler.settings.shuffle_items:
        ROM_COPY.seek(sav + 0x034)
        ROM_COPY.write(1)  # Item Rando Enabled
        item_data: list[LocationSelection] = spoiler.item_assignment

        map_items = {}
        offset_dict = populateOverlayOffsets(ROM_COPY)
        pushItemMicrohints(spoiler)
        pregiven_shop_owners = None
        # Place first move, if fast start is off
        if not FAST_START:
            placed_item = spoiler.first_move_item
            write_space = spoiler.settings.move_location_data + (6 * 125)
            if placed_item is None:
                # Is Nothing
                writeNullShopSlot(ROM_COPY, write_space)
            else:
                prog_flags = {
                    Items.ProgressiveSlam: [0x3BC, 0x3BD, 0x3BE],
                    Items.ProgressiveAmmoBelt: [0x292, 0x293],
                    Items.ProgressiveInstrumentUpgrade: [0x294, 0x295, 0x296],
                }
                if placed_item in prog_flags:
                    item_flag = prog_flags[placed_item][0]
                else:
                    item_flag = ItemList[placed_item].rando_flag
                if item_flag is not None and item_flag & 0x8000:
                    # Is move
                    writeShopData(ROM_COPY, write_space, None, 0)  # What to do here?
                else:
                    # Is Flagged Item
                    writeShopData(ROM_COPY, write_space, None, 0)  # What to do here?
        # Go through bijection
        for item in item_data:
            if item.can_have_item:
                # Write placement
                # For shop items, pass kong_override to differentiate AP items
                kong_override = None
                if item.is_shop and item.placement_index and len(item.placement_index) > 0:
                    # Extract kong from placement index: kong = int((index % 40) / 8)
                    first_placement = item.placement_index[0]
                    if first_placement < 120:  # Regular shop slots (not shared/training)
                        kong_override = int((first_placement % 40) / 8)
                item_properties = getItemPatchingData(item.new_type, item.new_item, kong_override)
                if item.is_shop:
                    # Write in placement index
                    movespaceOffset = spoiler.settings.move_location_data
                    if item.location in TRAINING_LOCATIONS:
                        if not FAST_START:
                            # Add to bonus table
                            old_tflag = 0x182 + TRAINING_LOCATIONS.index(item.location)
                            bonus_index = getBonusIndex(ROM_COPY, offset_dict, old_tflag)
                            if bonus_index is not None:
                                patchBonus(ROM_COPY, bonus_index, offset_dict, spawn_actor=getActorIndex(item), level=item_properties.level, item_kong=item_properties.kong)
                    for placement in item.placement_index:
                        write_space = movespaceOffset + (6 * placement)
                        if item.new_type is None:
                            # Is Nothing
                            # First check if there is an item here
                            ROM_COPY.seek(write_space)
                            check = int.from_bytes(ROM_COPY.readBytes(1), "big")
                            if check == 0 or placement >= 120:  # No Item
                                writeNullShopSlot(ROM_COPY, write_space)
                        else:
                            # Is Flagged Item
                            price_var = 0
                            if isinstance(item.price, list):
                                price_var = 0
                            else:
                                price_var = item.price
                            writeShopData(ROM_COPY, write_space, item_properties, price_var)
                        if spoiler.settings.enable_shop_hints and placement < 120:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.Shop, placement, offset_dict)
                            writeBuyText(item.new_item, addr, ROM_COPY)
                elif item.location >= Locations.TurnInDKIslesDonkeyBlueprint and item.location <= Locations.TurnInCreepyCastleChunkyBlueprint:
                    if item.location <= Locations.TurnInDKIslesChunkyBlueprint:
                        index = 35 + (item.location - Locations.TurnInDKIslesDonkeyBlueprint)
                    else:
                        index = item.location - Locations.TurnInJungleJapesDonkeyBlueprint
                    snide_reward_addr_start = getROMAddress(getSym("snide_rewards"), Overlay.Custom, offset_dict)
                    ROM_COPY.seek(snide_reward_addr_start + (index * 8))
                    if item.new_type is None or item.new_type == Types.NoItem:
                        ROM_COPY.writeMultipleBytes(0, 2)
                        ROM_COPY.writeMultipleBytes(0, 2)
                    else:
                        obj_index = getPropFromItem(item.new_item, item.new_type)
                        ROM_COPY.writeMultipleBytes(obj_index, 2)
                        ROM_COPY.writeMultipleBytes(0, 2)
                    ROM_COPY.writeMultipleBytes(item_properties.response_type, 1)
                    ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                    ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                    ROM_COPY.writeMultipleBytes(item_properties.audiovisual_medal, 1)
                elif not item.reward_spot:
                    for map_id in item.placement_data:
                        if map_id not in map_items:
                            map_items[map_id] = []
                        if item.new_type is None:
                            map_items[map_id].append(
                                {
                                    "id": item.placement_data[map_id],
                                    "obj": Types.NoItem,
                                    "loc": item.location,
                                    "kong": 0,
                                    "flag": 0,
                                    "upscale": 1,
                                    "shared": False,
                                    "subitem": Items.NoItem,
                                }
                            )
                        else:
                            numerator = getItemDBEntry(item.new_type).scale
                            denominator = getItemDBEntry(item.old_item).scale
                            upscale = numerator / denominator
                            map_items[map_id].append(
                                {
                                    "id": item.placement_data[map_id],
                                    "obj": item.new_type,
                                    "loc": item.location,
                                    "kong": item.new_kong,
                                    "flag": item.new_flag,
                                    "upscale": upscale,
                                    "shared": item.shared,
                                    "subitem": item.new_item,
                                }
                            )
                    if item.location == Locations.NintendoCoin:
                        spoiler.arcade_item_reward = item.new_item
                        db_item = getItemDBEntry(item.new_type)
                        db_index = db_item.index_getter(item.new_item)
                        arcade_reward_index = db_item.arcade_reward_index[db_index]
                        ROM_COPY.seek(sav + 0x110)
                        ROM_COPY.write(arcade_reward_index)
                        addr = getItemTableWriteAddress(ROM_COPY, Types.NintendoCoin, 0, offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.write(item_properties.response_type)
                        ROM_COPY.write(item_properties.level)
                        ROM_COPY.write(item_properties.kong)
                        ROM_COPY.write(item_properties.audiovisual_medal)
                    elif item.location == Locations.RarewareCoin:
                        spoiler.jetpac_item_reward = item.new_item
                        db_item = getItemDBEntry(item.new_type)
                        db_index = db_item.index_getter(item.new_item)
                        jetpac_reward_index = db_item.jetpac_reward_index[db_index]
                        ROM_COPY.seek(sav + 0x111)
                        ROM_COPY.write(jetpac_reward_index)
                        addr = getItemTableWriteAddress(ROM_COPY, Types.RarewareCoin, 1, offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.write(item_properties.response_type)
                        ROM_COPY.write(item_properties.level)
                        ROM_COPY.write(item_properties.kong)
                        ROM_COPY.write(item_properties.audiovisual_medal)
                    elif item.location in (Locations.ForestDonkeyBaboonBlast, Locations.CavesDonkeyBaboonBlast):
                        # Autocomplete bonus barrel fix
                        actor_index = getActorIndex(item)
                        bonus_index = getBonusIndex(ROM_COPY, offset_dict, item.old_flag)
                        if bonus_index is not None:
                            patchBonus(ROM_COPY, bonus_index, offset_dict, spawn_actor=actor_index, level=item_properties.level, item_kong=item_properties.kong)
                else:
                    if item.old_item != Types.Medal:
                        actor_index = getActorIndex(item)
                    if item.old_item == Types.Blueprint:
                        # Write to BP Table
                        # Just needs to store an array of actors spawned
                        addr = getItemTableWriteAddress(ROM_COPY, Types.Blueprint, item.old_flag - 469, offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                        ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                        patchBonus(ROM_COPY, (item.old_flag - 469) + 54, offset_dict, spawn_actor=actor_index, level=item_properties.level, item_kong=item_properties.kong)
                    elif item.old_item == Types.Crown:
                        # Write to Crown Table
                        crown_flags = [0x261, 0x262, 0x263, 0x264, 0x265, 0x268, 0x269, 0x266, 0x26A, 0x267]
                        addr = getItemTableWriteAddress(ROM_COPY, Types.Crown, crown_flags.index(item.old_flag), offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                        ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                    elif item.old_item == Types.Key:
                        key_flags = [26, 74, 138, 168, 236, 292, 317, 380]
                        addr = getItemTableWriteAddress(ROM_COPY, Types.Key, key_flags.index(item.old_flag), offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                        ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                    elif item.old_item == Types.RainbowCoin:
                        index = item.location - Locations.RainbowCoin_Location00
                        if index < 16:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.RainbowCoin, index, offset_dict)
                            ROM_COPY.seek(addr)
                            ROM_COPY.writeMultipleBytes(actor_index, 2)
                            ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                            ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                        else:
                            raise Exception("Dirt Patch Item Placement Error")
                    elif item.old_item == Types.CrateItem:
                        index = item.location - Locations.MelonCrate_Location00
                        if index < 13:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.CrateItem, index, offset_dict)
                            ROM_COPY.seek(addr)
                            ROM_COPY.writeMultipleBytes(actor_index, 2)
                            ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                            ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                        else:
                            raise Exception("Melon Crate Item Placement Error")
                    elif item.old_item == Types.BoulderItem:
                        index = item.location - Locations.HoldableBoulderIslesNearAztec
                        if index < 16:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.BoulderItem, index, offset_dict)
                            ROM_COPY.seek(addr)
                            ROM_COPY.writeMultipleBytes(actor_index, 2)
                            ROM_COPY.writeMultipleBytes(HOLDABLE_LOCATION_INFO[item.location]["map_id"], 2)
                            ROM_COPY.writeMultipleBytes(HOLDABLE_LOCATION_INFO[item.location]["spawner_id"], 2)
                            ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                            ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                        else:
                            raise Exception("Melon Crate Item Placement Error")
                    elif item.old_item == Types.Enemies:
                        index = item.location - Locations.JapesMainEnemy_Start
                        ROM_COPY.seek(POINTER_ROM_ENEMIES + (index * 8))
                        ROM_COPY.writeMultipleBytes(spoiler.enemy_location_list[item.location].map, 1)
                        ROM_COPY.writeMultipleBytes(spoiler.enemy_location_list[item.location].id, 1)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        ROM_COPY.writeMultipleBytes(item_properties.response_type, 1)
                        ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                        ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                        ROM_COPY.writeMultipleBytes(item_properties.audiovisual_medal, 1)
                    elif item.old_item in (Types.Medal, Types.Hint, Types.HalfMedal):
                        offset = None
                        if item.old_item in (Types.Medal, Types.HalfMedal):
                            if item.old_item == Types.Medal:
                                offset = item.old_flag - 549
                                if item.old_flag >= 0x3C6 and item.old_flag < 0x3CB:  # Isles Medals
                                    offset = 40 + (item.old_flag - 0x3C6)
                            elif item.old_item == Types.HalfMedal:
                                offset = 45 + (item.old_flag - 0x3D6)
                        elif item.old_item == Types.Hint:
                            offset = item.old_flag - 0x384
                        addr = getItemTableWriteAddress(ROM_COPY, item.old_item, offset, offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.write(item_properties.response_type)
                        ROM_COPY.write(item_properties.level)
                        ROM_COPY.write(item_properties.kong)
                        ROM_COPY.write(item_properties.audiovisual_medal)
                    elif item.location in (Locations.JapesChunkyBoulder, Locations.AztecLankyVulture):
                        # Write to Boulder/Vulture Spawn Location
                        offset = 0
                        if item.location == Locations.AztecLankyVulture:
                            offset = 4
                        ram_start = getSym("extra_actor_spawns")
                        rom_addr = getROMAddress(ram_start + offset, Overlay.Custom, offset_dict)
                        ROM_COPY.seek(rom_addr)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        ROM_COPY.writeMultipleBytes(item_properties.level, 1)
                        ROM_COPY.writeMultipleBytes(item_properties.kong, 1)
                    elif item.old_item == Types.Banana:
                        # Bonus GB Table
                        bonus_index = getBonusIndex(ROM_COPY, offset_dict, item.old_flag)
                        if bonus_index is not None:
                            patchBonus(ROM_COPY, bonus_index, offset_dict, spawn_actor=actor_index, level=item_properties.level, item_kong=item_properties.kong)
                    elif item.old_item == Types.Fairy:
                        # Fairy Item
                        model = getModelFromItem(item.new_item, item.new_type)
                        if model is not None:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.Fairy, item.old_flag - 589, offset_dict)
                            ROM_COPY.seek(addr)
                            ROM_COPY.writeMultipleBytes(model, 2)
                            ROM_COPY.writeMultipleBytes(0, 2)
                            ROM_COPY.write(item_properties.response_type)
                            ROM_COPY.write(item_properties.level)
                            ROM_COPY.write(item_properties.kong)
                            ROM_COPY.write(item_properties.audiovisual_medal)
                    elif item.old_item == Types.Kong:
                        kong_idx = {
                            Locations.DiddyKong: 0,
                            Locations.LankyKong: 1,
                            Locations.TinyKong: 2,
                            Locations.ChunkyKong: 3,
                        }
                        if item.location in kong_idx:
                            model = getModelFromItem(item.new_item, item.new_type)
                            if model is not None:
                                idx = kong_idx[item.location]
                                no_texture_tuple = (
                                    Types.Candy,
                                    Types.Climbing,
                                    Types.Cranky,
                                    Types.Fairy,
                                    Types.FillerFairy,
                                    Types.Funky,
                                    Types.Shockwave,
                                    Types.Shop,
                                    Types.TrainingBarrel,
                                )
                                has_no_textures = item.new_type in no_texture_tuple or getModelMask(item.new_item) in no_texture_tuple
                                addr = getItemTableWriteAddress(ROM_COPY, Types.Kong, idx, offset_dict)
                                ROM_COPY.seek(addr)
                                ROM_COPY.writeMultipleBytes(model, 2)
                                ROM_COPY.writeMultipleBytes(has_no_textures, 1)
                                ROM_COPY.writeMultipleBytes(0, 1)
                                ROM_COPY.write(item_properties.response_type)
                                ROM_COPY.write(item_properties.level)
                                ROM_COPY.write(item_properties.kong)
                                ROM_COPY.write(item_properties.audiovisual_medal)
            if item.new_type == Types.Hint:
                offset = item.new_item - Items.JapesDonkeyHint
                tied_region = GetRegionIdOfLocation(spoiler, item.location)
                spoiler.tied_hint_regions[offset] = spoiler.RegionList[tied_region].hint_name
            ref_index = 0
            if item.new_item == Items.ProgressiveAmmoBelt:
                ref_index = item.new_flag - 0x292
            elif item.new_item == Items.ProgressiveInstrumentUpgrade:
                ref_index = item.new_flag - 0x294
            elif item.new_item == Items.ProgressiveSlam:
                ref_index = item.new_flag - 0x3BC
            setItemReferenceName(spoiler, item.new_item, ref_index, spoiler.LocationList[item.location].name, item.old_flag)
            # Handle pre-given shops, only ran into if shop owners are in the pool
            if item.old_item in shop_owner_types:
                if pregiven_shop_owners is None:
                    pregiven_shop_owners = []
                if item.new_type in shop_owner_types:
                    pregiven_shop_owners.append(item.new_type)
                elif item.new_item != Items.NoItem and item.new_type is not None:
                    raise Exception(f"Invalid item {item.new_item.name} placed in shopkeeper slot. This shouldn't happen.")
        # Patch pre-given shops
        if pregiven_shop_owners is not None:  # Shop owners in pool
            data = 0
            or_data = {
                Types.Cranky: 0x80,
                Types.Funky: 0x40,
                Types.Candy: 0x20,
                Types.Snide: 0x10,
            }
            for x in or_data:
                if x not in spoiler.settings.shuffled_location_types:
                    data |= or_data[x]
            for x in pregiven_shop_owners:
                data |= or_data[x]
            ROM_COPY.seek(sav + 0x1EC)
            ROM_COPY.writeMultipleBytes(data, 1)

        # Update Diddy Cage text to the actual Freeing Kong rather than Funky
        kong_name = kong_list[spoiler.settings.diddy_freeing_kong].upper()

        if 3 not in spoiler.text_changes:
            spoiler.text_changes[3] = []

        spoiler.text_changes[3].append(
            {
                "textbox_index": 2,
                "mode": "replace",
                "search": "FUNKY'S HELP",
                "target": kong_name + "'S HELP",
            }
        )

        # Text stuff
        if spoiler.settings.item_reward_previews:
            for textbox in textboxes:
                new_type = textbox.default_type
                new_item = textbox.default_item
                for item in item_data:
                    if textbox.location == item.location:
                        new_type = item.new_type
                        new_item = item.new_item
                replacement = textbox.replacement_text
                if not textbox.force_pipe:
                    # Use the standard item preview text
                    reward_text = getItemPreviewText(new_type, textbox.location, True, getModelMask(new_item), new_item)
                    replacement = replacement.replace("|", reward_text)
                file_data = {
                    textbox.file_index: {
                        "textbox_index": textbox.textbox_index,
                        "mode": "replace",
                        "search": textbox.text_replace,
                        "target": replacement,
                    }
                }
                if textbox.file_index == CompTextFiles.PreviewsFlavor:
                    replacement = textbox.replacement_text
                    if not textbox.force_pipe:
                        reward_text = getItemPreviewText(new_type, textbox.location, False, getModelMask(new_item), new_item)
                    replacement = replacement.replace("|", reward_text)
                    file_data[CompTextFiles.PreviewsNormal] = {
                        "textbox_index": textbox.textbox_index,
                        "mode": "replace",
                        "search": textbox.text_replace,
                        "target": replacement,
                    }
                for file in file_data:
                    if file in spoiler.text_changes:
                        spoiler.text_changes[file].append(file_data[file])
                    else:
                        spoiler.text_changes[file] = [file_data[file]]
            beetle_data = {
                Locations.AztecTinyBeetleRace: "aztec_beetle",
                Locations.CavesLankyBeetleRace: "caves_beetle",
            }
            beetle_locations = list(beetle_data.keys())
            for item in item_data:
                if item.location in beetle_locations:
                    VERSION_STRING_START = getSym(beetle_data[item.location])
                    addr = getROMAddress(VERSION_STRING_START, Overlay.Custom, offset_dict)
                    item_text = getItemPreviewText(item.new_type, item.location, THEMATIC_TEXT, getModelMask(new_item), item.new_item)
                    ROM_COPY.seek(addr)
                    ROM_COPY.writeBytes(bytes(f"{item_text}\0", "ascii"))
            minor_item = "\x05FOR A FOOLISH GAME\x05"
            major_item = "\x04FOR SOMETHING YOU MIGHT NEED ON YOUR QUEST\x04"
            if 8 not in spoiler.text_changes:
                spoiler.text_changes[8] = []
            major_items = spoiler.majorItems
            new_item = Items.RarewareCoin
            for item in item_data:
                if item.location == Locations.RarewareCoin:
                    new_item = item.new_item
            if new_item in [Items.ArchipelagoItem, Items.SpecialArchipelagoItem, Items.FoolsArchipelagoItem, Items.TrapArchipelagoItem]:
                placed_text = major_item if new_item == Items.ArchipelagoItem else minor_item
            else:
                placed_text = major_item if new_item in major_items else minor_item

            spoiler.text_changes[8].append({"textbox_index": 0, "mode": "replace", "search": "FOR MY AMAZING SURPRISE", "target": placed_text})

        # Setup Changes
        for map_id in map_items:
            cont_map_setup_address = getPointerLocation(TableNames.Setups, map_id)
            ROM_COPY.seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for item in range(model2_count):
                start = cont_map_setup_address + 4 + (item * 0x30)
                ROM_COPY.seek(start + 0x2A)
                item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                for item_slot in map_items[map_id]:
                    if item_slot["id"] != item_id:
                        continue
                    ROM_COPY.seek(start + 0x28)
                    old_item = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    if old_item not in model_two_items:
                        continue
                    ROM_COPY.seek(start + 0x28)
                    item_obj_index = getPropFromItem(item_slot["subitem"], item_slot["obj"])
                    ROM_COPY.writeMultipleBytes(item_obj_index, 2)
                    extra_data = getItemPatchingData(item_slot["obj"], item_slot["subitem"], item_slot.get("kong"))
                    if extra_data is not None:
                        ROM_COPY.seek(start + 0x10)
                        ROM_COPY.writeMultipleBytes(extra_data.response_type, 1)
                        ROM_COPY.writeMultipleBytes(extra_data.level, 1)
                        ROM_COPY.writeMultipleBytes(extra_data.kong, 1)
                    if item_slot["loc"] == Locations.IslesChunkyPoundtheX:
                        writeValue(ROM_COPY, 0x80747D4A, Overlay.Static, item_obj_index, offset_dict)
                    # Scaling fix
                    ROM_COPY.seek(start + 0xC)
                    old_scale = intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    new_scale = old_scale * item_slot["upscale"]
                    ROM_COPY.seek(start + 0xC)
                    ROM_COPY.writeFloat(new_scale)
        # Remove GBs from Snide's
        if spoiler.settings.snide_reward_rando:
            cont_map_setup_address = getPointerLocation(TableNames.Setups, Maps.Snide)
            ROM_COPY.seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for item in range(model2_count):
                start = cont_map_setup_address + 4 + (item * 0x30)
                ROM_COPY.seek(start + 0x2A)
                item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if item_id in (2, 3, 4, 0x10, 0x12, 0x13, 0x14, 0x15):  # Item IDs for the snide GBs
                    ROM_COPY.seek(start + 0x28)
                    ROM_COPY.writeMultipleBytes(0, 2)  # Set to nothing object
            # Speed up the path points for points 2, 3 and 4
            path_address = getPointerLocation(TableNames.Paths, Maps.Snide)
            ROM_COPY.seek(path_address)
            path_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            offset = 2
            for x in range(path_count):
                ROM_COPY.seek(path_address + offset + 2)
                point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                for y in range(point_count):
                    point_start = path_address + offset + 6 + (y * 10)
                    if y < 2:
                        continue
                    ROM_COPY.seek(point_start + 8)
                    ROM_COPY.writeMultipleBytes(2, 1)  # Double the speed at this path point
                offset += 6
                offset += point_count * 10


def place_spoiler_hint_data(sav, spoiler, ROM_COPY: LocalROM):
    """Place the array data for spoiler hints."""
    if spoiler.settings.spoiler_hints == SpoilerHints.off:
        return
    ROM_COPY.seek(sav + 0x12F)
    ROM_COPY.writeMultipleBytes(spoiler.settings.spoiler_hints, 1)
    # Compute & Write Table
    base_addr = getROMAddress(getSym("spoiler_items"), Overlay.Custom, populateOverlayOffsets(ROM_COPY))
    level_index_mapping = {
        Levels.JungleJapes: 0,
        Levels.AngryAztec: 1,
        Levels.FranticFactory: 2,
        Levels.GloomyGalleon: 3,
        Levels.FungiForest: 4,
        Levels.CrystalCaves: 5,
        Levels.CreepyCastle: 6,
        Levels.DKIsles: 7,
        Levels.HideoutHelm: 8,
    }
    ROM_COPY.seek(base_addr)
    for level, local_spoiler in spoiler.level_spoiler.items():
        if level in ("starting_info", "point_spread"):
            continue
        for item in local_spoiler.level_items:
            points = item["points"]
            if points == 0:
                continue
            flag = item["flag"]
            if flag == 0:
                continue
            level_index = level_index_mapping.get(level, 9)
            ROM_COPY.writeMultipleBytes(flag, 2)
            ROM_COPY.writeMultipleBytes(points, 1)
            ROM_COPY.writeMultipleBytes(level_index, 1)

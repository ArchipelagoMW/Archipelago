"""Apply item rando changes."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Settings import MicrohintsEnabled
from randomizer.Enums.Types import Types
from randomizer.Enums.MoveTypes import MoveTypes
from randomizer.Lists.Item import ItemList
from randomizer.Patching.Library.DataTypes import float_to_hex, intf_to_float
from randomizer.Lists.EnemyTypes import enemy_location_list
from randomizer.Patching.Library.Generic import setItemReferenceName, CustomActors
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Patcher import LocalROM
from randomizer.CompileHints import getHelmProgItems, GetRegionIdOfLocation


model_two_indexes = {
    Types.Banana: 0x74,
    Types.Blueprint: [0xDE, 0xE0, 0xE1, 0xDD, 0xDF],
    Types.RarewareCoin: 0x28F,
    Types.NintendoCoin: 0x48,
    Types.Key: 0x13C,
    Types.Crown: 0x18D,
    Types.Medal: 0x90,
    Types.Shop: [0x5B, 0x1F2, 0x59, 0x1F3, 0x1F5, 0x1F6],
    Types.TrainingBarrel: 0x1F6,
    Types.Climbing: 0x1F6,
    Types.Shockwave: 0x1F6,
    Types.NoItem: 0,  # No Item
    Types.Kong: [0x257, 0x258, 0x259, 0x25A, 0x25B],
    Types.Bean: 0x198,
    Types.Pearl: 0x1B4,
    Types.Fairy: 0x25C,
    Types.RainbowCoin: 0xB7,
    Types.FakeItem: [0x25D, 0x264, 0x265],
    Types.JunkItem: [0x56, 0x8F, 0x8E, 0x25E, 0x98],  # Orange, Ammo, Crystal, Watermelon, Film
    Types.Cranky: 0x25F,
    Types.Funky: 0x260,
    Types.Candy: 0x261,
    Types.Snide: 0x262,
    Types.Hint: [638, 649, 650, 651, 652],
    Types.ArchipelagoItem: 0x291,
}

model_two_scales = {
    # Anything not here is 0.25
    Types.Blueprint: 2,
    Types.NintendoCoin: 0.4,
    Types.RarewareCoin: 0.4,
    Types.Key: 0.17,
    Types.Crown: 0.25,
    Types.Medal: 0.22,
}

actor_indexes = {
    Types.Banana: 45,
    Types.Blueprint: [78, 75, 77, 79, 76],
    Types.Key: 72,
    Types.Crown: 86,
    Types.NintendoCoin: CustomActors.NintendoCoin,
    Types.RarewareCoin: CustomActors.RarewareCoin,
    Types.Shop: [
        CustomActors.PotionDK,
        CustomActors.PotionDiddy,
        CustomActors.PotionLanky,
        CustomActors.PotionTiny,
        CustomActors.PotionChunky,
        CustomActors.PotionAny,
    ],
    Types.TrainingBarrel: CustomActors.PotionAny,
    Types.Shockwave: CustomActors.PotionAny,
    Types.NoItem: CustomActors.Null,
    Types.Medal: CustomActors.Medal,
    Types.Kong: [
        CustomActors.KongDK,
        CustomActors.KongDiddy,
        CustomActors.KongLanky,
        CustomActors.KongTiny,
        CustomActors.KongChunky,
    ],
    Types.Bean: CustomActors.Bean,
    Types.Pearl: CustomActors.Pearl,
    Types.Fairy: CustomActors.Fairy,
    Types.RainbowCoin: 0x8C,
    Types.FakeItem: CustomActors.IceTrapBubble,
    Types.JunkItem: [0x34, 0x33, 0x79, 0x2F, 0],  # Orange, Ammo, Crystal, Watermelon, Film
    Types.Cranky: CustomActors.CrankyItem,
    Types.Funky: CustomActors.FunkyItem,
    Types.Candy: CustomActors.CandyItem,
    Types.Snide: CustomActors.SnideItem,
    Types.Hint: [
        CustomActors.HintItemDK,
        CustomActors.HintItemDiddy,
        CustomActors.HintItemLanky,
        CustomActors.HintItemTiny,
        CustomActors.HintItemChunky,
    ],
    Types.ArchipelagoItem: CustomActors.ArchipelagoItem,
}
model_indexes = {
    Types.Banana: 0x69,
    Types.Key: 0xF5,
    Types.Crown: 0xF4,
    Types.Fairy: 0x3D,
    Types.Shop: [0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB],
    Types.Shockwave: 0xFB,
    Types.TrainingBarrel: 0xFB,
    Types.Climbing: 0xFB,
    Types.Kong: [4, 1, 6, 9, 0xC],
    Types.FakeItem: [-4, -3, -2],  # -4 for bubble trap, -3 for reverse trap, -2 for slow trap
    Types.Bean: 0x104,
    Types.Pearl: 0x106,
    Types.Medal: 0x108,
    Types.NintendoCoin: 0x10A,
    Types.RarewareCoin: 0x10C,
    Types.JunkItem: 0x10E,
    Types.Cranky: 0x11,
    Types.Funky: 0x12,
    Types.Candy: 0x13,
    Types.Snide: 0x1F,
    Types.Hint: [0x11B, 0x11D, 0x11F, 0x121, 0x123],
    Types.ArchipelagoItem: 0x125,
}

TRAINING_LOCATIONS = (
    Locations.IslesSwimTrainingBarrel,
    Locations.IslesVinesTrainingBarrel,
    Locations.IslesOrangesTrainingBarrel,
    Locations.IslesBarrelsTrainingBarrel,
)

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


textboxes = [
    TextboxChange(Locations.AztecTinyBeetleRace, 14, 0, "GOLDEN BANANA", Types.Banana, "\x04|\x04", True),
    TextboxChange(Locations.CavesLankyBeetleRace, 14, 0, "GOLDEN BANANA", Types.Banana, "\x04|\x04", True),
    TextboxChange(Locations.JapesDiddyMinecarts, 16, 2, "GOLDEN BANANA", Types.Banana),
    TextboxChange(Locations.JapesDiddyMinecarts, 16, 3, "BANANA", Types.Banana),
    TextboxChange(Locations.JapesDiddyMinecarts, 16, 4, "BANANA", Types.Banana),
    TextboxChange(Locations.ForestChunkyMinecarts, 16, 5, "GOLDEN BANANA", Types.Banana),
    TextboxChange(Locations.ForestChunkyMinecarts, 16, 7, "BANANA", Types.Banana),
    TextboxChange(Locations.CastleDonkeyMinecarts, 16, 8, "BE A WINNER", Types.Banana, "WIN A |"),
    TextboxChange(Locations.CastleDonkeyMinecarts, 16, 9, "BANANA", Types.Banana),
    TextboxChange(Locations.IslesDonkeyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, "SOMETHING"),
    TextboxChange(Locations.IslesDiddyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, "SOMETHING"),
    TextboxChange(Locations.IslesLankyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, "SOMETHING"),
    TextboxChange(Locations.IslesTinyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, "SOMETHING"),
    TextboxChange(Locations.IslesChunkyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, "SOMETHING"),
    TextboxChange(Locations.FactoryTinyCarRace, 17, 4, "GOLDEN BANANA", Types.Banana),
    TextboxChange(
        Locations.GalleonTinyPearls,
        23,
        0,
        "PLEASE TRY AND GET THEM BACK",
        Types.Banana,
        "IF YOU HELP ME FIND THEM, I WILL REWARD YOU WITH A |",
    ),
    TextboxChange(Locations.GalleonTinyPearls, 23, 1, "GOLDEN BANANA", Types.Banana),
    TextboxChange(
        Locations.GalleonTinyPearls,
        23,
        2,
        "ALTOGETHER.",
        Types.Banana,
        "ALTOGETHER. IF YOU FIND THEM ALL, YOU WILL RECEIVE A |",
    ),
    TextboxChange(Locations.AztecDiddyVultureRace, 15, 1, "PRIZE", Types.Banana),
    TextboxChange(Locations.AztecDonkeyFreeLlama, 10, 1, "ALL THIS SAND", Types.Banana, "THIS |"),
    TextboxChange(Locations.AztecDonkeyFreeLlama, 10, 2, "BANANA", Types.Banana),
    TextboxChange(Locations.RarewareCoin, 8, 2, "RAREWARE COIN", Types.RarewareCoin),  # Rareware Coin
    TextboxChange(Locations.RarewareCoin, 8, 34, "RAREWARE COIN", Types.RarewareCoin),  # Rareware Coin
    TextboxChange(Locations.ForestLankyRabbitRace, 20, 1, "TROPHY", Types.Banana, "| TROPHY"),
    TextboxChange(Locations.ForestLankyRabbitRace, 20, 2, "TROPHY", Types.Banana, "| TROPHY"),
    TextboxChange(Locations.ForestLankyRabbitRace, 20, 3, "TROPHY", Types.Banana, "| TROPHY"),
    TextboxChange(Locations.ForestChunkyApple, 22, 0, "BANANA", Types.Banana),
    TextboxChange(Locations.ForestChunkyApple, 22, 1, "BANANA", Types.Banana),
    TextboxChange(Locations.ForestChunkyApple, 22, 4, "BANANA", Types.Banana),
    TextboxChange(Locations.GalleonDonkeySealRace, 28, 2, "CHEST O' GOLD", Types.Banana),
    TextboxChange(Locations.RarewareBanana, 30, 0, "REWARD ANYONE", Types.Banana, "REWARD ANYONE WITH A |"),
    TextboxChange(Locations.CavesLankyCastle, 33, 0, "HOW ABOUT IT", Types.Banana, "HOW ABOUT A |"),
    TextboxChange(Locations.CastleTinyCarRace, 34, 4, "BANANA", Types.Banana),
    TextboxChange(
        Locations.ForestDiddyOwlRace,
        21,
        0,
        "WHEN YOU CAN FLY",
        Types.Banana,
        "WHEN YOU CAN FLY TO HAVE A CHANCE TO RECEIVE A |",
    ),
    TextboxChange(Locations.ForestTinySpiderBoss, 19, 32, "\x04GOLDEN BANANA\x04", Types.Banana),
    TextboxChange(Locations.CavesChunky5DoorIgloo, 19, 34, "\x04GOLDEN BANANA\x04", Types.Banana),
]


text_rewards = {
    Types.Banana: ("\x04GOLDEN BANANA\x04", "\x04BANANA OF PURE GOLD\x04"),
    Types.Blueprint: ("\x04BLUEPRINT\x04", "\x04MAP O' DEATH MACHINE\x04"),
    Types.Key: ("\x04BOSS KEY\x04", "\x04KEY TO DAVY JONES LOCKER\x04"),
    Types.Crown: ("\x04BATTLE CROWN\x04", "\x04CROWN TO PLACE ATOP YER HEAD\x04"),
    Types.Fairy: ("\x04BANANA FAIRY\x04", "\x04MAGICAL FLYING PIXIE\x04"),
    Types.Medal: ("\x04BANANA MEDAL\x04", "\x04MEDALLION\x04"),
    Types.Shop: ("\x04POTION\x04", "\x04BOTTLE OF GROG\x04"),
    Types.Shockwave: ("\x04POTION\x04", "\x04BOTTLE OF GROG\x04"),
    Types.TrainingBarrel: ("\x04POTION\x04", "\x04BOTTLE OF GROG\x04"),
    Types.Climbing: ("\x04POTION\x04", "\x04BOTTLE OF GROG\x04"),
    Types.Kong: ("\x04KONG\x04", "\x04WEIRD MONKEY\x04"),
    Types.Bean: ("\x04BEAN\x04", "\x04QUESTIONABLE VEGETABLE\x04"),
    Types.Pearl: ("\x04PEARL\x04", "\x04BLACK PEARL\x04"),
    Types.RainbowCoin: ("\x04RAINBOW COIN\x04", "\x04COLORFUL COIN HIDDEN FOR 17 YEARS\x04"),
    Types.FakeItem: ("\x04GLODEN BANANE\x04", "\x04BANANA OF FOOLS GOLD\x04"),
    Types.JunkItem: ("\x04JUNK ITEM\x04", "\x04HEAP OF JUNK\x04"),
    Types.NoItem: ("\x04NOTHING\x04", "\x04DIDDLY SQUAT\x04"),
    Types.RarewareCoin: ("\x04RAREWARE COIN\x04", "\x04DOUBLOON OF THE RAREST KIND\x04"),
    Types.NintendoCoin: ("\x04NINTENDO COIN\x04", "\x04ANCIENT DOUBLOON\x04"),
    Types.Snide: ("\x04SHOPKEEPER\x04", "\x04NERDY SOUL\x04"),
    Types.Cranky: ("\x04SHOPKEEPER\x04", "\x04BARTERING SOUL\x04"),
    Types.Candy: ("\x04SHOPKEEPER\x04", "\x04BARTERING SOUL\x04"),
    Types.Funky: ("\x04SHOPKEEPER\x04", "\x04BARTERING SOUL\x04"),
    Types.Hint: ("\x04HINT\x04", "\x04LAYTON RIDDLE\x04"),
    Types.ArchipelagoItem: ("\x04ARCHIPELAGO ITEM\x04", "\x04ANOTHER SCALLYWAG'S BOOTY\x04"),
}

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


def appendTextboxChange(spoiler, file_index: int, textbox_index: int, search: str, target: str):
    """Alter a specific textbox."""
    data = {"textbox_index": textbox_index, "mode": "replace", "search": search, "target": target}
    if file_index in spoiler.text_changes:
        spoiler.text_changes[file_index].append(data)
    else:
        spoiler.text_changes[file_index] = [data]


NUMBERS_AS_WORDS = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE"]


def alterTextboxRequirements(spoiler):
    """Alters various textboxes based on the requirement count changing."""
    pearl_req = spoiler.settings.mermaid_gb_pearls
    appendTextboxChange(spoiler, 23, 2, "FIVE MISSING PEARLS", f"{NUMBERS_AS_WORDS[pearl_req]} MISSING PEARL{'S' if pearl_req != 1 else ''}")
    all_text = ""
    if pearl_req == 5:
        all_text = "ALL "
    plea_including_pearl_count = f"PLEASE TRY AND GET {all_text}{NUMBERS_AS_WORDS[pearl_req]} OF THEM BACK"
    for x in textboxes:
        if x.location == Locations.GalleonTinyPearls and x.textbox_index == 0:
            x.text_replace = plea_including_pearl_count
            x.replacement_text = f"IF YOU HELP ME FIND {all_text}{NUMBERS_AS_WORDS[pearl_req]} OF THEM, I WILL REWARD YOU WITH A |"
    appendTextboxChange(spoiler, 23, 0, "PLEASE TRY AND GET THEM BACK", plea_including_pearl_count)
    fairy_req = spoiler.settings.rareware_gb_fairies
    if fairy_req != 20:
        appendTextboxChange(spoiler, 30, 0, "FIND THEM ALL", f"FIND {fairy_req} OF THEM")
        appendTextboxChange(spoiler, 40, 0, "RESCUED ALL THE BANANA FAIRIES", "RESCUED THE BANANA FAIRIES")
    appendTextboxChange(spoiler, 40, 4, "MUST GET FAIRIES", f"MUST GET {fairy_req} FAIRIES")


def pushItemMicrohints(spoiler):
    """Push hint for the micro-hints system."""
    helm_prog_items = getHelmProgItems(spoiler)
    hinted_items = [
        # Key = Item, Value = (Textbox index in text file 19, (all_accepted_settings))
        (helm_prog_items[0], 26, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (helm_prog_items[1], 25, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Bongos, 27, [MicrohintsEnabled.all]),
        (Items.Triangle, 28, [MicrohintsEnabled.all]),
        (Items.Saxophone, 29, [MicrohintsEnabled.all]),
        (Items.Trombone, 30, [MicrohintsEnabled.all]),
        (Items.Guitar, 31, [MicrohintsEnabled.all]),
        (Items.ProgressiveSlam, 33, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Cranky, 35, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Funky, 36, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Candy, 37, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Snide, 38, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
    ]
    for item_hint, item_data in enumerate(hinted_items):
        if spoiler.settings.microhints_enabled in list(item_data[2]):
            if ItemList[item_data[0]].name in spoiler.microhints:
                data = {
                    "textbox_index": item_data[1],
                    "mode": "replace_whole",
                    "target": spoiler.microhints[ItemList[item_data[0]].name],
                }
                if 19 in spoiler.text_changes:
                    spoiler.text_changes[19].append(data)
                else:
                    spoiler.text_changes[19] = [data]


def getTextRewardIndex(item) -> int:
    """Get reward index for text item."""
    if item.new_item == Types.RarewareCoin:
        return 5
    elif item.new_item == Types.NintendoCoin:
        return 6
    elif item.new_item in (Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing):
        return 8
    elif item.new_item in (Types.Snide, Types.Cranky, Types.Candy, Types.Funky):
        return 15
    elif item.new_item is None:
        return 14
    else:
        item_text_indexes = (
            Types.Banana,  # 0
            Types.Blueprint,  # 1
            Types.Key,  # 2
            Types.Crown,  # 3
            Types.Fairy,  # 4
            Types.RarewareCoin,  # 5
            Types.NintendoCoin,  # 6
            Types.Medal,  # 7
            Types.Shop,  # 8
            Types.Kong,  # 9
            Types.Bean,  # 10
            Types.Pearl,  # 11
            Types.RainbowCoin,  # 12
            Types.FakeItem,  # 13
            Types.NoItem,  # 14
            Types.Cranky,  # 15
            Types.JunkItem,  # 16
            Types.ArchipelagoItem,  # 17
        )
        if item.new_item in item_text_indexes:
            return item_text_indexes.index(item.new_item)
        return 14


def writeNullShopSlot(ROM_COPY: LocalROM, location: int):
    """Write an empty shop slot."""
    ROM_COPY.seek(location)
    ROM_COPY.writeMultipleBytes(MoveTypes.Nothing, 2)
    ROM_COPY.writeMultipleBytes(0, 2)
    ROM_COPY.writeMultipleBytes(0, 1)
    ROM_COPY.writeMultipleBytes(0, 1)


def writeShopData(ROM_COPY: LocalROM, location: int, item_type: MoveTypes, flag: int, kong: int, price: int):
    """Write shop data to slot."""
    ROM_COPY.seek(location)
    ROM_COPY.writeMultipleBytes(item_type, 2)
    ROM_COPY.writeMultipleBytes(flag, 2)
    ROM_COPY.writeMultipleBytes(kong, 1)
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
    if item.new_item is None:
        return actor_indexes[Types.NoItem]
    elif item.new_item == Types.Blueprint:
        return actor_indexes[Types.Blueprint][item.new_kong]
    elif item.new_item == Types.JunkItem:
        return actor_indexes[Types.JunkItem][subitems.index(item.new_subitem)]
    elif item.new_item == Types.FakeItem:
        trap_types = {
            Items.IceTrapBubble: CustomActors.IceTrapBubble,
            Items.IceTrapReverse: CustomActors.IceTrapReverse,
            Items.IceTrapSlow: CustomActors.IceTrapSlow,
        }
        return trap_types.get(item.new_subitem, CustomActors.IceTrapBubble)
    elif item.new_item in (Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing):
        if (item.new_flag & 0x8000) == 0:
            slot = 5
        else:
            slot = (item.new_flag >> 12) & 7
            if item.shared or slot > 5:
                slot = 5
        return actor_indexes[Types.Shop][slot]
    elif item.new_item == Types.Kong:
        slot = 0
        if item.new_flag in kong_flags:
            slot = kong_flags.index(item.new_flag)
        return actor_indexes[Types.Kong][slot]
    elif item.new_item == Types.Hint:
        return actor_indexes[Types.Hint][getHintKongFromFlag(item.new_flag)]
    return actor_indexes[item.new_item]


def place_randomized_items(spoiler, original_flut: list, ROM_COPY: LocalROM):
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
        item_data = spoiler.item_assignment
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
        map_items = {}
        bonus_table_offset = 0
        flut_items = original_flut.copy()
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
                    item_kong = (item_flag >> 12) & 7
                    item_subtype = (item_flag >> 8) & 0xF
                    if item_subtype == 7:
                        item_subindex = 0
                    else:
                        item_subindex = (item_flag & 0xFF) - 1
                    writeShopData(ROM_COPY, write_space, item_subtype, item_subindex, item_kong, 0)
                else:
                    # Is Flagged Item
                    writeShopData(ROM_COPY, write_space, MoveTypes.Flag, item_flag, 0, 0)
        # Go through bijection
        for item in item_data:
            if item.can_have_item:
                # Write array data for AP
                if item.new_item == Types.Medal:
                    if item.new_flag < (0x225 + 40):
                        setItemInWorld(ROM_COPY, sav + 4, 0x225, item.new_flag)
                    else:
                        # Isles Medals
                        setItemInWorld(ROM_COPY, sav + 9, 0x3C6, item.new_flag)
                elif item.new_item == Types.Crown:
                    setItemInWorld(ROM_COPY, sav + 1, 0x261, item.new_flag)
                elif item.new_item == Types.Pearl:
                    setItemInWorld(ROM_COPY, sav + 3, 0xBA, item.new_flag)
                elif item.new_item == Types.Fairy:
                    setItemInWorld(ROM_COPY, sav + 0xA, 0x24D, item.new_flag)
                # Write placement
                if item.is_shop:
                    # Write in placement index
                    movespaceOffset = spoiler.settings.move_location_data
                    if item.location in TRAINING_LOCATIONS:
                        if not FAST_START:
                            # Add to bonus table
                            old_tflag = 0x182 + TRAINING_LOCATIONS.index(item.location)
                            ROM_COPY.seek(0x1FF1200 + (4 * bonus_table_offset))
                            ROM_COPY.writeMultipleBytes(old_tflag, 2)
                            ROM_COPY.writeMultipleBytes(getActorIndex(item), 2)
                            bonus_table_offset += 1
                            # Append to FLUT
                            data = [old_tflag]
                            if item.new_item is None:
                                data.append(0)
                            else:
                                data.append(item.new_flag)
                            flut_items.append(data)
                    for placement in item.placement_index:
                        write_space = movespaceOffset + (6 * placement)
                        if item.new_item is None:
                            # Is Nothing
                            # First check if there is an item here
                            ROM_COPY.seek(write_space)
                            check = int.from_bytes(ROM_COPY.readBytes(2), "big")
                            if check == MoveTypes.Nothing or placement >= 120:  # No Item
                                writeNullShopSlot(ROM_COPY, write_space)
                        elif item.new_flag & 0x8000:
                            # Is Move
                            item_kong = (item.new_flag >> 12) & 7
                            item_subtype = (item.new_flag >> 8) & 0xF
                            if item_subtype == 7:
                                item_subindex = 0
                            else:
                                item_subindex = (item.new_flag & 0xFF) - 1
                            writeShopData(ROM_COPY, write_space, item_subtype, item_subindex, item_kong, item.price)
                        else:
                            # Is Flagged Item
                            subtype = MoveTypes.Flag
                            if item.new_item == Types.Banana:
                                subtype = MoveTypes.GB
                            elif item.new_item == Types.FakeItem:
                                trap_types = {
                                    Items.IceTrapBubble: MoveTypes.IceTrapBubble,
                                    Items.IceTrapReverse: MoveTypes.IceTrapReverse,
                                    Items.IceTrapSlow: MoveTypes.IceTrapSlow,
                                }
                                subtype = trap_types.get(item.new_subitem, MoveTypes.IceTrapBubble)
                            price_var = 0
                            if isinstance(item.price, list):
                                price_var = 0
                            else:
                                price_var = item.price
                            writeShopData(ROM_COPY, write_space, subtype, item.new_flag, 0, price_var)
                elif not item.reward_spot:
                    for map_id in item.placement_data:
                        if map_id not in map_items:
                            map_items[map_id] = []
                        if item.new_item is None:
                            map_items[map_id].append(
                                {
                                    "id": item.placement_data[map_id],
                                    "obj": Types.NoItem,
                                    "kong": 0,
                                    "flag": 0,
                                    "upscale": 1,
                                    "shared": False,
                                    "subitem": 0,
                                }
                            )
                        else:
                            numerator = model_two_scales.get(item.new_item, 0.25)
                            denominator = model_two_scales.get(item.old_item, 0.25)
                            upscale = numerator / denominator
                            map_items[map_id].append(
                                {
                                    "id": item.placement_data[map_id],
                                    "obj": item.new_item,
                                    "kong": item.new_kong,
                                    "flag": item.new_flag,
                                    "upscale": upscale,
                                    "shared": item.shared,
                                    "subitem": item.new_subitem,
                                }
                            )
                    if item.location == Locations.NintendoCoin:
                        spoiler.arcade_item_reward = item.new_subitem
                        arcade_rewards = (
                            Types.NoItem,  # Or Nintendo Coin
                            Types.Bean,
                            Types.Blueprint,
                            Types.Crown,
                            Types.Fairy,
                            Types.Banana,
                            Types.Key,
                            Types.Medal,
                            Types.Pearl,
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.RainbowCoin,
                            Types.RarewareCoin,  # Flag check handled separately
                            Types.JunkItem,
                        )
                        arcade_reward_index = 0
                        if item.new_item == Types.Kong:
                            if item.new_flag in kong_flags:
                                arcade_reward_index = kong_flags.index(item.new_flag) + 15
                        elif item.new_item in (Types.Shop, Types.TrainingBarrel, Types.Shockwave, Types.Climbing):
                            if (item.new_flag & 0x8000) == 0:
                                slot = 5
                            else:
                                slot = (item.new_flag >> 12) & 7
                                if item.shared or slot > 5:
                                    slot = 5
                            arcade_reward_index = 9 + slot
                        elif item.new_item in arcade_rewards:
                            arcade_reward_index = arcade_rewards.index(item.new_item)
                        ROM_COPY.seek(sav + 0x110)
                        ROM_COPY.write(arcade_reward_index)
                    elif item.location == Locations.RarewareCoin:
                        spoiler.jetpac_item_reward = item.new_subitem
                        jetpac_rewards = (
                            Types.NoItem,  # Or RW Coin
                            Types.Bean,
                            Types.Blueprint,
                            Types.Crown,
                            Types.Fairy,
                            Types.Banana,
                            Types.Key,
                            Types.Medal,
                            Types.Pearl,
                            Types.Shop,  # Shockwave/Training/Climbing handled separately
                            Types.Kong,
                            Types.RainbowCoin,
                            Types.NintendoCoin,  # Flag check handled separately
                            Types.JunkItem,
                        )
                        jetpac_reward_index = 0
                        if item.new_item in (Types.Shop, Types.TrainingBarrel, Types.Shockwave, Types.Climbing):
                            jetpac_reward_index = 9
                        elif item.new_item in jetpac_rewards:
                            jetpac_reward_index = jetpac_rewards.index(item.new_item)
                        ROM_COPY.seek(sav + 0x111)
                        ROM_COPY.write(jetpac_reward_index)
                    elif item.location in (Locations.ForestDonkeyBaboonBlast, Locations.CavesDonkeyBaboonBlast):
                        # Autocomplete bonus barrel fix
                        actor_index = getActorIndex(item)
                        ROM_COPY.seek(0x1FF1200 + (4 * bonus_table_offset))
                        ROM_COPY.writeMultipleBytes(item.old_flag, 2)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        bonus_table_offset += 1
                    elif item.location in (Locations.AztecTinyBeetleRace, Locations.CavesLankyBeetleRace):
                        text_index = getTextRewardIndex(item)
                        if item.location == Locations.AztecTinyBeetleRace:
                            ROM_COPY.seek(sav + 0x50)
                        else:
                            ROM_COPY.seek(sav + 0x51)
                        ROM_COPY.write(text_index)
                elif item.old_item == Types.Kong:
                    for i in range(4):
                        if item.new_item is None or item.new_item == Types.NoItem:
                            # Write Empty Cage
                            ROM_COPY.seek(sav + 0x152 + (2 * i))
                            ROM_COPY.writeMultipleBytes(0xFF, 1)
                else:
                    if item.old_item != Types.Medal:
                        actor_index = getActorIndex(item)
                    if item.old_item == Types.Blueprint:
                        # Write to BP Table
                        # Just needs to store an array of actors spawned
                        offset = (item.old_flag - 469) * 2
                        ROM_COPY.seek(0x1FF0E00 + offset)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                    elif item.old_item == Types.Crown:
                        # Write to Crown Table
                        crown_flags = [0x261, 0x262, 0x263, 0x264, 0x265, 0x268, 0x269, 0x266, 0x26A, 0x267]
                        ROM_COPY.seek(0x1FF10C0 + (crown_flags.index(item.old_flag) * 2))
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                    elif item.old_item == Types.Key:
                        key_flags = [26, 74, 138, 168, 236, 292, 317, 380]
                        ROM_COPY.seek(0x1FF1000 + (key_flags.index(item.old_flag) * 2))
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                    elif item.old_item == Types.RainbowCoin:
                        index = item.location - Locations.RainbowCoin_Location00
                        if index < 16:
                            ROM_COPY.seek(0x1FF10E0 + (index * 2))
                            ROM_COPY.writeMultipleBytes(actor_index, 2)
                        else:
                            print("Dirt Patch Item Placement Error")
                    elif item.location >= Locations.MelonCrate_Location00 and item.location <= Locations.MelonCrate_Location12:
                        index = item.location - Locations.MelonCrate_Location00
                        if index < 13:
                            ROM_COPY.seek(0x1FF0E80 + (index * 2))
                            ROM_COPY.writeMultipleBytes(actor_index, 2)
                        else:
                            print("Melon Crate Item Placement Error")
                    elif item.location >= Locations.JapesMainEnemy_Start and item.location <= Locations.IslesMainEnemy_LowerFactoryPath1:
                        index = item.location - Locations.JapesMainEnemy_Start
                        ROM_COPY.seek(0x1FF9000 + (index * 4))
                        ROM_COPY.writeMultipleBytes(enemy_location_list[item.location].map, 1)
                        ROM_COPY.writeMultipleBytes(enemy_location_list[item.location].id, 1)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                    elif item.old_item in (Types.Medal, Types.Hint):
                        # Write to Medal Table
                        # Just need offset of subtype:
                        # 0 = Banana
                        # 1 = BP
                        # 2 = Key
                        # 3 = Crown
                        # 4 = Special Coin
                        # 5 = Medal
                        # 6 = Cranky Potion
                        # 7 = Funky Potion
                        # 8 = Candy Potion
                        # 9 = Training Barrel
                        # 10 = Shockwave
                        # 11 = Kong
                        # 12 = Bean
                        # 13 = Pearl
                        # 14 = Fairy
                        # 15 = Rainbow Coin
                        # 16 = Ice Trap (Bubble)
                        # 17 = Junk Melon
                        # 18 = Cranky Item
                        # 19 = Funky Item
                        # 20 = Candy Item
                        # 21 = Snide Item
                        # 22 = Nothing
                        # 23 = Ice Trap (Reverse)
                        # 24 = Ice Trap (Slow)
                        slots = [
                            Types.Banana,  # GB
                            Types.Blueprint,  # BP
                            Types.Key,  # Key
                            Types.Crown,  # Crown
                            Types.NintendoCoin,  # Special Coin
                            Types.Medal,  # Medal
                            Types.Shop,  # Cranky Item
                            Types.Shop,  # Funky Item
                            Types.Shop,  # Candy Item
                            Types.TrainingBarrel,  # Training Move
                            Types.Shockwave,  # Fairy Item
                            Types.Kong,  # Kong
                            Types.Bean,  # Bean
                            Types.Pearl,  # Pearl
                            Types.Fairy,  # Fairy
                            Types.RainbowCoin,  # Rainbow Coin
                            Types.FakeItem,  # Fake Item (Bubble)
                            Types.JunkItem,  # Junk Item
                            Types.Cranky,  # Cranky Item
                            Types.Funky,  # Funky Item
                            Types.Candy,  # Candy Item
                            Types.Snide,  # Snide Item
                            None,  # No Item
                            Types.FakeItem,  # Fake Item (Reverse)
                            Types.FakeItem,  # Fake Item (Slow)
                            Types.Hint,  # Hint Item
                            Types.ArchipelagoItem,  # Archipelago Item
                        ]
                        offset = None
                        base_addr = None
                        if item.old_item == Types.Medal:
                            offset = item.old_flag - 549
                            if item.old_flag >= 0x3C6 and item.old_flag < 0x3CB:  # Isles Medals
                                offset = 40 + (item.old_flag - 0x3C6)
                            base_addr = 0x1FF1080
                        elif item.old_item == Types.Hint:
                            offset = item.old_flag - 0x384
                            base_addr = 0x1FF0EC0
                        ROM_COPY.seek(base_addr + offset)
                        if item.new_item == Types.Shop:
                            medal_index = 6
                            if item.new_flag in (0x3BC, 0x3BD, 0x3BE):
                                medal_index = 6
                            elif item.new_flag in (0x292, 0x293):
                                medal_index = 7
                            elif item.new_flag in (0x294, 0x295, 0x296):
                                medal_index = 8
                            else:
                                subtype = (item.new_flag >> 8) & 0xF
                                if subtype == 4:
                                    medal_index = 8
                                elif (subtype == 2) or (subtype == 3):
                                    medal_index = 7
                            ROM_COPY.write(medal_index)
                        elif item.new_item == Types.RarewareCoin:
                            ROM_COPY.write(slots.index(Types.NintendoCoin))
                        elif item.new_item == Types.Climbing:
                            ROM_COPY.write(slots.index(Types.TrainingBarrel))
                        elif item.new_item == Types.FakeItem:
                            trap_types = {
                                Items.IceTrapBubble: 16,
                                Items.IceTrapReverse: 23,
                                Items.IceTrapSlow: 24,
                            }
                            val = trap_types.get(item.new_subitem, 16)
                            ROM_COPY.write(val)
                        else:
                            ROM_COPY.write(slots.index(item.new_item))
                    elif item.location == Locations.JapesChunkyBoulder:
                        # Write to Boulder Spawn Location
                        spoiler.japes_rock_actor = actor_index
                    elif item.location == Locations.AztecLankyVulture:
                        # Write to Vulture Spawn Location
                        spoiler.aztec_vulture_actor = actor_index
                    elif item.old_item == Types.Banana:
                        # Bonus GB Table
                        ROM_COPY.seek(0x1FF1200 + (4 * bonus_table_offset))
                        ROM_COPY.writeMultipleBytes(item.old_flag, 2)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        bonus_table_offset += 1
                    elif item.old_item == Types.Fairy:
                        # Fairy Item
                        if item.new_item in model_indexes:
                            model = model_indexes[item.new_item]
                            if item.new_item == Types.Shop:
                                if (item.new_flag & 0x8000) == 0:
                                    slot = 5
                                else:
                                    slot = (item.new_flag >> 12) & 7
                                    if item.shared or slot > 5:
                                        slot = 5
                                model = model_indexes[Types.Shop][slot]
                            elif item.new_item == Types.Kong:
                                slot = 0
                                if item.new_flag in kong_flags:
                                    slot = kong_flags.index(item.new_flag)
                                model = model_indexes[Types.Kong][slot]
                            elif item.new_item == Types.FakeItem:
                                trap_types = {
                                    Items.IceTrapBubble: -4,
                                    Items.IceTrapReverse: -3,
                                    Items.IceTrapSlow: -2,
                                }
                                model = trap_types.get(item.new_subitem, -4) + 0x10000
                            elif item.new_item == Types.Hint:
                                model = model_indexes[Types.Hint][getHintKongFromFlag(item.new_flag)]
                            ROM_COPY.seek(0x1FF1040 + (2 * (item.old_flag - 589)))
                            ROM_COPY.writeMultipleBytes(model, 2)
            if item.new_item == Types.Hint:
                offset = item.new_flag - 0x384
                tied_region = GetRegionIdOfLocation(spoiler, item.location)
                spoiler.tied_hint_regions[offset] = spoiler.RegionList[tied_region].hint_name
            if not item.is_shop and item.can_have_item and item.old_item != Types.Kong:
                # Write flag lookup table
                data = [item.old_flag]
                if item.new_item is None:
                    data.append(0)
                else:
                    data.append(item.new_flag)
                flut_items.append(data)
            ref_index = 0
            if item.new_subitem == Items.ProgressiveAmmoBelt:
                ref_index = item.new_flag - 0x292
            elif item.new_subitem == Items.ProgressiveInstrumentUpgrade:
                ref_index = item.new_flag - 0x294
            elif item.new_subitem == Items.ProgressiveSlam:
                ref_index = item.new_flag - 0x3BC
            setItemReferenceName(spoiler, item.new_subitem, ref_index, spoiler.LocationList[item.location].name)
            # Handle pre-given shops, only ran into if shop owners are in the pool
            if item.old_item in shop_owner_types:
                if pregiven_shop_owners is None:
                    pregiven_shop_owners = []
                if item.new_item in shop_owner_types:
                    pregiven_shop_owners.append(item.new_item)
                elif item.new_item != Items.NoItem and item.new_item is not None:
                    raise Exception(f"Invalid item {item.new_subitem.name} placed in shopkeeper slot. This shouldn't happen.")
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
        # Text stuff
        if spoiler.settings.item_reward_previews:
            for textbox in textboxes:
                new_item = textbox.default_type
                flag = 379  # Rareware Coin flag for RW Coin textbox
                for item in item_data:
                    if textbox.location == item.location:
                        new_item = item.new_item
                        flag = item.new_flag
                replacement = textbox.replacement_text
                if not textbox.force_pipe:
                    reward_text = "|"
                    reference = None
                    if new_item in text_rewards.keys():
                        reference = text_rewards[new_item]
                    if reference is not None:
                        # Found reference
                        reward_text = reference[0]
                        if textbox.location == Locations.GalleonDonkeySealRace:
                            # Use pirate text
                            reward_text = reference[1]
                    replacement = replacement.replace("|", reward_text)
                data = {
                    "textbox_index": textbox.textbox_index,
                    "mode": "replace",
                    "search": textbox.text_replace,
                    "target": replacement,
                }
                if textbox.file_index in spoiler.text_changes:
                    spoiler.text_changes[textbox.file_index].append(data)
                else:
                    spoiler.text_changes[textbox.file_index] = [data]
            minor_item = "\x05FOR A FOOLISH GAME\x05"
            major_item = "\x04FOR SOMETHING YOU MIGHT NEED ON YOUR QUEST\x04"
            if 8 not in spoiler.text_changes:
                spoiler.text_changes[8] = []
            major_items = spoiler.majorItems
            new_item = Items.RarewareCoin
            for item in item_data:
                if item.location == Locations.RarewareCoin:
                    new_item = item.new_subitem
            placed_text = major_item if new_item in major_items else minor_item
            spoiler.text_changes[8].append({"textbox_index": 0, "mode": "replace", "search": "FOR MY AMAZING SURPRISE", "target": placed_text})

        # Terminate FLUT
        flut_items.append([0xFFFF, 0xFFFF])
        flags_to_push = []
        if not FAST_START:
            flags_to_push = [0x182, 0x183, 0x184, 0x185]
        for flut in flut_items:
            input_flag = flut[0]
            if input_flag in flags_to_push:
                flags_to_push = [x for x in flags_to_push if x != input_flag]
        for flag in flags_to_push:
            flut_items.append([flag, 0])
        ROM_COPY.seek(0x1FF2000)
        for flut in sorted(flut_items, key=lambda x: x[0]):
            for flag in flut:
                ROM_COPY.writeMultipleBytes(flag, 2)
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
                    if item_slot["id"] == item_id:
                        ROM_COPY.seek(start + 0x28)
                        old_item = int.from_bytes(ROM_COPY.readBytes(2), "big")
                        if old_item in model_two_items:
                            ROM_COPY.seek(start + 0x28)
                            item_obj_index = 0
                            if item_slot["obj"] == Types.Blueprint:
                                item_obj_index = model_two_indexes[Types.Blueprint][item_slot["kong"]]
                            elif item_slot["obj"] == Types.JunkItem:
                                item_obj_index = model_two_indexes[Types.JunkItem][subitems.index(item_slot["subitem"])]
                            elif item_slot["obj"] == Types.FakeItem:
                                trap_types = {
                                    Items.IceTrapBubble: 0x25D,
                                    Items.IceTrapReverse: 0x264,
                                    Items.IceTrapSlow: 0x265,
                                }
                                item_obj_index = trap_types.get(item_slot["subitem"], 0x25D)
                            elif item_slot["obj"] == Types.Shop:
                                if (item_slot["flag"] & 0x8000) == 0:
                                    slot = 5
                                else:
                                    slot = (item_slot["flag"] >> 12) & 7
                                    if item_slot["shared"] or slot > 5:
                                        slot = 5
                                item_obj_index = model_two_indexes[Types.Shop][slot]
                            elif item_slot["obj"] == Types.Kong:
                                slot = 0
                                if item_slot["flag"] in kong_flags:
                                    slot = kong_flags.index(item_slot["flag"])
                                item_obj_index = model_two_indexes[Types.Kong][slot]
                            elif item_slot["obj"] == Types.Hint:
                                item_obj_index = model_two_indexes[Types.Hint][getHintKongFromFlag(item_slot["flag"])]
                            else:
                                item_obj_index = model_two_indexes[item_slot["obj"]]
                            ROM_COPY.writeMultipleBytes(item_obj_index, 2)
                            # Scaling fix
                            ROM_COPY.seek(start + 0xC)
                            old_scale = intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                            new_scale = old_scale * item_slot["upscale"]
                            ROM_COPY.seek(start + 0xC)
                            ROM_COPY.writeMultipleBytes(int(float_to_hex(new_scale), 16), 4)

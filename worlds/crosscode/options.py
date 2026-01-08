"""
This module provides the options and option dataclass for the Options dataclass.
"""

from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Toggle, Range

# class LogicMode(Choice):
#     """
#     Logic mode; in other words, how is the player allowed to access items.
#     [Linear] Progression follows the game's linear path, though sequence breaks are allowed and inevitably will still
#              occur. Makes for a longer, more BK-heavy playthrough with fewer options at each point.
#     [Open] (Default) Progression is based only on whether it is possible to reach area given the current list of
#            received items.
#     """
#     display_name = "Logic Mode"
#     option_linear = 0
#     option_open = 1

#     default = 1

class VTShadeLock(Choice):
    """
    If set to a non-None value, creates an in-game barrier at the entrance of Vermillion Tower to prevent extremely
    quick playthroughs.
    [Bosses] Vermillion Tower only opens when the bosses at the end of the first four dungeons have been beaten.
    [Shades] Vermillion Tower only opens when the four shades acquired at the end of the first four dungeons have been
             acquired.
    [Bosses and Shades] Vermillion Tower opens when both of the other conditions have been satisfied.
    """
    display_name = "Vermillion Tower Shade Lock"

    option_none = 0
    option_bosses_and_shades = 1
    option_shades = 2
    option_bosses = 3
    default = 1

class VWMeteorPassage(DefaultOnToggle):
    """
    If enabled, places a gate between Sapphire Ridge and Vermillion Wasteland unlockable with the meteor shade,
    """
    display_name = "Vermillion Wasteland Meteor Passage"

class VTSkip(DefaultOnToggle):
    """
    If enabled, Vermillion Tower will not need to be completed; instead, the player will skip through it to the final
    boss.
    """
    display_name = "Skip Vermillion Tower"

class QuestRando(Toggle):
    """
    If enabled, all quest rewards will be added to the location list.
    """
    display_name = "Quest Randomization"

class HiddenQuestRewardMode(Choice):
    """
    Some quests hide their rewards until they are completed.
    [Vanilla] Behavior is unchanged from the base game.
    [Show All] Show all rewards regardless of whether they're hidden in the base game.
    [Hide All] Hide all rewards regardless of whether they're hidden in the base game.
    """
    display_name = "Show Hidden Quest Rewards"

    option_vanilla = 0
    option_show_all = 1
    option_hide_all = 2

    default = 0

class HiddenQuestObfuscationLevel(Choice):
    """
    For quests with hidden rewards, this option controls the level to which rewards are obscured.
    [Hide Item] Only hides the item name. The icon and receiving player are still accurate.
    [Hide Text] Obscures item name and receiving player. The icon will still be accurate.
    [Hide All] The item name and receiving player will all be hidden and the icon will be replaced with a generic
               Archipelago logo.
    """
    display_name = "Hidden Quest Obfuscation Level"

    option_hide_item = 0
    option_hide_text = 1
    option_hide_all = 2

    default = 0

class QuestDialogHints(DefaultOnToggle):
    """
    If enabled, upon viewing the quest dialog for a quest with rewards that are not hidden, hints are sent to the
    Archipelago server for all non-filler quest rewards.
    """
    display_name = "Quest Dialog Hints"

class ShopRando(Toggle):
    """
    If enabled, all shops will be added to the location list.
    """
    display_name = "Shop Randomization"

class ShopSendMode(Choice):
    """
    Controls what exactly counts as a check when shop randomization is enabled.
    [Per Item Type] A check is added for each type of item (for example, Sandwich). Therefore, purchasing a sandwich
    from any shop in the game clears the same check.
    [Per Slot] A check is added for each item slot in each shop. Therefore, purchasing a Sandwich in Rookie Harbor
    clears a separate check than purchasing a Sandwich in Bergen Village.
    """

    display_name = "Shop Send Mode"

    option_per_item_type = 1
    option_per_slot = 3

    default = option_per_item_type

class ShopReceiveMode(Choice):
    """
    Controls how shops are unlocked when shop randomization is enabled.
    [None] All shop slots are able to be purchased as soon as the player can access the shop.
    [Per Item Type] A check is added for each type of item (for example, Sandwich) which unlocks the ability to purchase
    that item from any shop.
    [Per Shop] A check is added for each shop (for example, Rookie Harbor Items) which unlocks the ability to purchase
    items from that shop.
    [Per Slot] A check is added for each item slot in each shop which unlocks the ability to purchase that item from
    that shop (this may lead to tedious playthroughs).
    """

    display_name = "Shop Receive Mode"

    option_none = 0
    option_per_item_type = 1
    option_per_shop = 2
    option_per_slot = 3

    default = option_per_item_type

class ShopDialogHints(DefaultOnToggle):
    """
    If enabled, upon opening the dialog for a shop, corresponding hints are sent to the Archipelago server for all
    non-filler shop items.
    """
    display_name = "Shop Dialog Hints"

class StartWithGreenLeafShade(DefaultOnToggle):
    """
    If enabled, the player will start with the green leaf shade, unlocking Autumn's Fall. This makes the early game far
    more open.
    """
    display_name = "Start with Green Leaf Shade"

class StartWithChestDetector(DefaultOnToggle):
    """
    If enabled, the player will start with the chest detector item, which will notify them of the chests in the room.
    """
    display_name = "Start with Chest Detector"

class StartWithDiscs(Choice):
    """
    If set to a value other than "none", the player will start with the corresponding disc items.
    Disc of Insight unlocks the records menu.
    Disc of Flora unlocks the botany menu, allowing the player to start collecting plant samples from the beginning.
    """

    option_none = 0
    option_insight = 1
    option_flora = 2
    option_both = 3

    default = 1

    display_name = "Start with Discs"

class StartWithPet(DefaultOnToggle):
    """
    If enabled, the player will start with a random pet. This is just for fun.
    """
    display_name = "Start with Pet"

class Keyrings(Toggle):
    """
    If enabled, all keys for each dungeon will be replaced with a singular item that unlocks every door in that dungeon.
    """
    display_name = "Keyrings"

class ProgressiveAreaUnlocks(Choice):
    """
    If enabled, the items that unlock overworld areas and dungeons (including shades and some passes) will be made
    progressive.
    [None] no areas are unlocked progressively.
    [Dungeons] dungeons are unlocked progressively; overworld areas are not.
    [Overworld] overworld areas are unlocked progressively; dungeons are not.
    [Split] both dungeons and overworld areas are unlocked progressively in separate progressive chains.
    [Combined] both dungeons and overworld areas are unlocked progressively from the same progressive chain.
    """
    display_name = "Progressive Area Unlocks"

    # treat this option as a bitmask
    # first bit: include dungeons
    # second bit: include overworld
    # third bit: combine pools
    DUNGEONS = 1 << 0
    OVERWORLD = 1 << 1
    COMBINE_POOLS = 1 << 2

    option_none = 0
    option_dungeons = DUNGEONS
    option_overworld = OVERWORLD
    option_split = DUNGEONS | OVERWORLD
    option_combined = COMBINE_POOLS | DUNGEONS | OVERWORLD

    default = 0

class ProgressiveEquipment(Toggle):
    """
    If enabled, equipment will be progressive, sorted into different categories according to playstyle depending on
    which of the other location-adding options are enabled.
    """
    display_name = "Progressive Equipment"

class Reachability(Choice):
    """
    This is an internal class. Can define where an item can be placed.
    """
    option_own_world = 0
    option_different_world = 1
    option_any_world = 2

    default = 2

    items: dict[str, set[str]]
    """
    A dict associating areas with the set of items that this option specifies as part of that area.
    """

    def register_locality(self, local_items: set[str], non_local_items: set[str]):
        """
        Adds this option's `items` to the two arguments, `local_items` and `non_local_items` based on this option's
        value.
        """
        if self.value == Reachability.option_own_world:
            for _, lst in self.items.items():
                local_items |= lst
        elif self.value == Reachability.option_different_world:
            for _, lst in self.items.items():
                non_local_items |= lst

class DungeonReachability(Reachability):
    """
    Extends the Reachability class, adding options for items that are local to dungeons.
    """
    option_own_dungeons = 10
    option_original_dungeons = 11

    def register_pre_fill_lists(
        self,
        specific_dungeons: dict[str, set[str]],
        all_dungeons: set[str]
    ):
        """
        Adds this option's `items` to the `specific_dungeons` or `all_dungeons` argument depending on the value of this
        option.
        """
        if self.value == DungeonReachability.option_own_dungeons:
            for _, lst in self.items.items():
                all_dungeons |= lst
        if self.value == DungeonReachability.option_original_dungeons:
            for key, lst in self.items.items():
                specific_dungeons[key] |= lst

class ShadeShuffle(Reachability):
    """
    Where shades will appear.
    """
    display_name = "Shade Shuffle"

    items = {
        "any": {
            "Green Leaf Shade", "Yellow Sand Shade", "Blue Ice Shade",
            "Red Flame Shade", "Purple Bolt Shade", "Azure Drop Shade",
            "Green Seed Shade", "Star Shade", "Meteor Shade",
            "Progressive Area Unlock", "Progressive Overworld Area Unlock",
        }
    }

class ElementShuffle(DungeonReachability):
    """
    Where elements will appear.
    """
    display_name = "Element Shuffle"

    items = {
        "cold-dng": { "Heat" },
        "heat-dng": { "Cold" },
        "wave-dng": { "Shock" },
        "shock-dng": { "Wave" },
    }

class SmallKeyShuffle(DungeonReachability):
    """
    Where small keys will appear.
    """
    display_name = "Small Key Shuffle"

    items = {
        "cold-dng": { "Mine Key" },
        "heat-dng": { "Faj'ro Key" },
        "wave-dng": { "So'najiz Key" },
        "shock-dng": { "Zir'vitar Key" },
        "tree-dng": { "Krys'kajo Key" },
    }

class MasterKeyShuffle(DungeonReachability):
    """
    Where master keys will appear.
    """
    display_name = "Master Key Shuffle"

    items = {
        "cold-dng": { "Mine Master Key" },
        "heat-dng": { "Faj'ro Master Key" },
        "tree-dng": { "Kajo Master Key" },
    }

class ChestKeyShuffle(DungeonReachability):
    """
    Where the Thief's Key, White Key, and Radiant Key (the keys that open bronze, silver, and gold chests, respectively)
    may appear.
    """

    display_name = "Chest Key Shuffle"

    items = {
        "cold-dng": { "Thief's Key" },
        "heat-dng": { "White Key" },
        "wave-dng": { "Radiant Key" },
    }

class ChestLockRandomization(Toggle):
    """
    If enabled, the lock on all chests (Bronze, Silver, Gold, or None) will be randomized.
    """
    display_name = "Chest Lock Randomization"

class NoChestLockWeight(Range):
    """
    Controls the likelihood of giving a chest no lock (if chest lock randomization is enabled).
    """
    display_name = "Unlocked Chest Weight"

    range_start = 0
    range_end = 100
    default = 60

class BronzeChestLockWeight(Range):
    """
    Controls the likelihood of giving a chest bronze lock, requiring Thief's Key to open (if chest lock randomization is enabled).
    """
    display_name = "Bronze Chest Lock Weight"

    range_start = 0
    range_end = 100
    default = 15

class SilverChestLockWeight(Range):
    """
    Controls the likelihood of giving a chest silver lock, requiring White Key to open (if chest lock randomization is enabled).
    """
    display_name = "Silver Chest Lock Weight"

    range_start = 0
    range_end = 100
    default = 15

class GoldChestLockWeight(Range):
    """
    Controls the likelihood of giving a chest gild lock, requiring Radiant Key to open (if chest lock randomization is enabled).
    """
    display_name = "Gold Chest Lock Weight"

    range_start = 0
    range_end = 100
    default = 10

class ExcludeAlwaysQuests(DefaultOnToggle):
    """
    Certain quests are always in the location pool because they hold progression items when playing vanilla CrossCode.
    If this option is selected (and quest rando is disabled), this option will ensure that none of those locations are
    populated with progression or useful items. It will also prohibit items from being placed on NPC interactions that
    give progression items but require working through part of a questline to get to.
    """
    display_name = "Exclude Always Quests"

class CommonPoolWeight(Range):
    """
    Controls the likelihood of choosing a common filler item when filling the world.
    """
    display_name = "Common Pool Weight"

    range_start = 0
    range_end = 100
    default = 38

class RarePoolWeight(Range):
    """
    Controls the likelihood of choosing a rare filler item when filling the world.
    """
    display_name = "Rare Pool Weight"

    range_start = 0
    range_end = 100
    default = 32

class EpicPoolWeight(Range):
    """
    Controls the likelihood of choosing a epic filler item when filling the world.
    """
    display_name = "Epic Pool Weight"

    range_start = 0
    range_end = 100
    default = 24

class LegendaryPoolWeight(Range):
    """
    Controls the likelihood of choosing a legendary filler item when filling the world.
    """
    display_name = "Legendary Pool Weight"

    range_start = 0
    range_end = 100
    default = 6

class ConsumableWeight(Range):
    """
    Controls the likelihood of choosing a consumable item (as opposed to a drop).
    """
    display_name = "Consumable Weight"

    range_start = 0
    range_end = 100
    default = 50

class DropWeight(Range):
    """
    Controls the likelihood of choosing a drop item (as opposed to a consumable).
    """
    display_name = "Drop Weight"

    range_start = 0
    range_end = 100
    default = 50

@dataclass
class CrossCodeOptions(PerGameCommonOptions):
    """
    Options dataclass for CrossCode
    """
    # logic_mode: LogicMode
    vt_shade_lock: VTShadeLock
    vw_meteor_passage: VWMeteorPassage
    vt_skip: VTSkip

    quest_rando: QuestRando
    hidden_quest_reward_mode: HiddenQuestRewardMode
    hidden_quest_obfuscation_level: HiddenQuestObfuscationLevel
    quest_dialog_hints: QuestDialogHints

    shop_rando: ShopRando
    shop_dialog_hints: ShopDialogHints
    shop_send_mode: ShopSendMode
    shop_receive_mode: ShopReceiveMode

    start_with_green_leaf_shade: StartWithGreenLeafShade
    start_with_chest_detector: StartWithChestDetector
    start_with_discs: StartWithDiscs
    start_with_pet: StartWithPet

    progressive_area_unlocks: ProgressiveAreaUnlocks
    progressive_equipment: ProgressiveEquipment
    keyrings: Keyrings

    shade_shuffle: ShadeShuffle
    element_shuffle: ElementShuffle
    small_key_shuffle: SmallKeyShuffle
    master_key_shuffle: MasterKeyShuffle
    chest_key_shuffle: ChestKeyShuffle

    chest_lock_randomization: ChestLockRandomization
    no_chest_lock_weight: NoChestLockWeight
    bronze_chest_lock_weight: BronzeChestLockWeight
    silver_chest_lock_weight: SilverChestLockWeight
    gold_chest_lock_weight: GoldChestLockWeight

    exclude_always_quests: ExcludeAlwaysQuests

    common_pool_weight: CommonPoolWeight
    rare_pool_weight: RarePoolWeight
    epic_pool_weight: EpicPoolWeight
    legendary_pool_weight: LegendaryPoolWeight
    consumable_weight: ConsumableWeight
    drop_weight: DropWeight

addon_options = ["quest_rando"]

option_groups: list[OptionGroup] = [
    OptionGroup(
        name="Quests",
        options=[
            QuestRando,
            HiddenQuestRewardMode,
            HiddenQuestObfuscationLevel,
            QuestDialogHints,
        ]
    ),
    OptionGroup(
        name="Shops",
        options=[
            ShopRando,
            ShopDialogHints,
            ShopSendMode,
            ShopReceiveMode
        ]
    ),
    OptionGroup(
        name="Starting Inventory",
        options=[
            StartWithGreenLeafShade,
            StartWithChestDetector,
            StartWithDiscs,
            StartWithPet,
        ]
    ),
    OptionGroup(
        name="Item Locations",
        options=[
            ShadeShuffle,
            ElementShuffle,
            SmallKeyShuffle,
            MasterKeyShuffle,
            ChestKeyShuffle,
        ]
    ),
    OptionGroup(
        name="Chest Locks",
        options=[
            ChestLockRandomization,
            NoChestLockWeight,
            BronzeChestLockWeight,
            SilverChestLockWeight,
            GoldChestLockWeight,
        ]
    ),
    OptionGroup(
        name="Locations",
        options=[
            ExcludeAlwaysQuests
        ]
    ),
    OptionGroup(
        name="Pools",
        options=[
            CommonPoolWeight,
            RarePoolWeight,
            EpicPoolWeight,
            LegendaryPoolWeight,
            ConsumableWeight,
            DropWeight
        ]
    ),
]

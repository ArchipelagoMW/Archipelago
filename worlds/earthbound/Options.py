from dataclasses import dataclass
from Options import (Toggle, DefaultOnToggle, DeathLink, Choice, Range, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, FreeText, Visibility, PlandoBosses)
from .modules.boss_shuffle import boss_plando_keys 


class GiygasRequired(DefaultOnToggle):
    """If enabled, your goal will be to defeat Giygas at the Cave of the Past.
       If disabled, your goal will either complete automatically upon completing
       enough Sanctuaries, or completing Magicant if it is required."""
    display_name = "Giygas Required"


class SanctuariesRequired(Range):
    """How many of the eight "Your Sanctuary" locations are required to be cleared."""
    display_name = "Required Sanctuaries"
    range_start = 1
    range_end = 8
    default = 4


class SanctuaryAltGoal(Toggle):
    """If enabled, you will be able to win by completing 2 more Sanctuaries than are required.
       Does nothing if 7 or more Sanctuaries are required, or if Magicant and Giygas are not required."""
    display_name = "Sanctuary Alternate Goal"


class MagicantMode(Choice):
    """PSI Location: You will be able to find a Magicant teleport item. Ness's Nightmare contains a PSI location, and no stat boost.
       Required: You will unlock the Magicant Teleport upon reaching your Sanctuary goal. If Giygas is required, beating Ness's Nightmare will unlock the Cave of the Past and grant a party-wide stat boost. Otherwise, Ness's Nightmare will finish your game.
       Alternate Goal: You will unlock the Magicant Teleport upon reaching one more Sanctuary than required. Beating Ness's Nightmare will finish your game. Does nothing if Giygas is not required, or if 8 Sanctuaries are required. Magicant locations are removed from the multiworld, but contain random junk for yourself.
       Optional Boost: You will be able to find a Magicant teleport item. Beating Ness's Nightmare will grant a party-wide stat boost. Magicant locations are removed from the multiworld, but contain random junk for yourself.
       Removed: Magicant will be completely inacessible."""
    display_name = "Magicant Mode"
    option_psi_location = 0
    option_required = 1
    option_alternate_goal = 2
    option_optional_boost = 3
    option_removed = 4
    default = 0


class MonkeyCavesMode(Choice):
    """Chests: Items required to finish the Monkey Caves will be forcibly placed on the chests that can be found in-between rooms of the monkey caves. The "reward" locations, usually found at the end of a branch, are still random. If you waste chest items, they will need to be replaced via the methods in hunt mode.
       Hunt: Items required to finish the Monkey Caves will needsell you every minor item needed to be found outside. They can be obtained from the Dusty Dunes drugstore, the Fourside department store, and the pizza shop in either Twoson or Threed.
       Shop: The monkey outside the Monkey Caves will sell every item needed to complete the caves and is not affected by shop randomization.
       Solved: The Monkey Caves monkeys will already be moved out of the way and not require any items."""
    display_name = "Monkey Caves Mode"
    option_chests = 0
    option_hunt = 1
    option_shop = 2
    option_solved = 3
    default = 1
    

class ShortenPrayers(DefaultOnToggle):
    """If enabled, the Prayer cutscenes while fighting Giygas will be skipped, excluding the final one."""
    display_name = "Skip Prayer Sequences"


class RandomStartLocation(Toggle):
    """If disabled, you will always start at Ness's house with no teleports unlocked.
       If enabled, you will start at a random teleport destination with one teleport unlocked.
       Additionally, you will need to fight Captain Strong to access the north part of Onett if this is enabled."""
    display_name = "Random Starting Location"


class LocalTeleports(Toggle):
    """Forces all teleports and Poo PSI to be placed locally in your world."""
    display_name = "Local Teleports"


class CharacterShuffle(Choice):
    """Shuffled: Characters will be shuffled amongst Character Locations. Extra locations will have Flying Man, a Teddy Bear, or a Super Plush Bear.
       Anywhere: Characters can be found anywhere in the multiworld, and character locations will have regular checks.
       See the Game Page for more information on Character Locations."""
    display_name = "Character Shuffle"
    option_shuffled = 0
    option_anywhere = 1
    default = 0


class PSIShuffle(Choice):
    """None: Characters will learn their normal PSI skills.
       Basic: Offensive and Assist PSI will be shuffled. Recovery PSI is not modified. Ness's Favorite Thing will be named Wave in other slots.
       Extended: Basic shuffle, but includes Jeff gadgets and some combat items.
       See the Game Page for more information."""
    display_name = "PSI Shuffle"
    option_none = 0
    option_basic = 1
    option_extended = 2


class BossShuffle(PlandoBosses):
    """Shuffles boss encounters amongst each other."""
    display_name = "Boss Shuffle"

    option_false = 0
    option_true = 1
    default = 0
    bosses = boss_plando_keys
    locations = boss_plando_keys
    duplicate_bosses = False

    @classmethod
    def can_place_boss(cls, boss: str, location: str) -> bool:
        return True


class DecoupleDiamondDog(Toggle):
    """Shuffles Diamond Dog as a boss separate from Carbon Dog. Carbon Dog will transform into a random boss.
       Does nothing if Boss Shuffle is disabled."""
    display_name = "Decouple Diamond Dog"


class ShuffleGiygas(Toggle):
    """Adds the standalone Giygas fight to the shuffled boss pool.
       This only applies to the second phase Giygas. The prayer fight is not affected.
       Does nothing if Boss Shuffle is disabled."""
    display_name = "Add Giygas to Boss Pool"


class BanFlashFavorite(Toggle):
    """If enabled, allows PSI Flash to be shuffled onto the Favorite Thing PSI slot. Can be quite annoying early-game. 
       Does nothing if PSI Shuffle is set to None."""
    display_name = "Flash as Favorite"


class PreFixItems(Toggle):
    """If enabled, broken items in the multiworld pool will be replaced with their fixed versions.
       This does not affect any items that are not placed by the multiworld."""
    display_name = "Prefixed Items"


class AutoscaleParty(Toggle):
    """If enabled, joining party members will be scaled to roughly the level of the sphere they were obtained in."""
    display_name = "Autoscale Party Members"


class ProgressiveWeapons(Toggle):
    """If enabled, Bats, Fry Pans, and Guns will be progressive. Does not apply to items dropped by enemies or found in shops."""
    display_name = "Progressive Weapons"


class ProgressiveArmor(Toggle):
    """If enabled, Bracelets and items for the Other slot besides Ribbons will be progressive. Does not apply to items dropped by enemies or found in shops."""
    display_name = "Progressive Armor"


class PresentSprites(DefaultOnToggle):
    """If enabled, Presents, Trash cans, and chests will have their appearance modified to be indicative of the item they contain."""
    display_name = "Match Present Sprites"


class NoAPPresents(Toggle):
    """If enabled, present that contain items for other players will appear as EarthBound presents (trashcan, present, and chest) instead of Archipelago boxes.
       Does nothing if Presents Match Contents is disabled."""


class ShuffleDrops(Toggle):
    """If enabled, enemies will drop random filler items. This does not put checks on enemy drops.
       Drop rates are unchanged."""
    display_name = "Shuffle Drops"


class RandomFranklinBadge(Toggle):
    """If enabled, the Franklin Badge will reflect a randomly selected attack type. The type can be determined from the item's name, as well as the help
       text for it. The badge's function outside of battle will not change, and neither will its name outside of the game itself."""
    display_name = "Franklin Badge Protection"


class CommonWeight(Range):
    """Weight for placing a common filler item."""
    display_name = "Common Filler Weight"
    range_start = 1
    range_end = 100
    default = 80


class UncommonWeight(Range):
    """Weight for placing an uncommon filler item."""
    display_name = "Uncommon Filler Weight"
    range_start = 1
    range_end = 100
    default = 30


class RareWeight(Range):
    """Weight for placing a rare filler item."""
    display_name = "Rare Filler Weight"
    range_start = 0
    range_end = 100
    default = 5


class MoneyWeight(Range):
    """Weight for placing money in the item pool."""
    display_name = "Money Weight"
    range_start = 0
    range_end = 100
    default = 0


class ExperienceModifier(Range):
    """Percentage of EXP enemies give you. 100 is vanilla, after scaling, and 300 is x3."""
    display_name = "Experience Percentage"
    range_start = 100
    range_end = 300
    default = 150


class StartingMoney(Range):
    """How much money you start with."""
    display_name = "Starting Money"
    range_start = 0
    range_end = 99999
    default = 20


class EasyDeaths(DefaultOnToggle):
    """Fully revives and heals all party members after death. If off, only Ness will be healed with 0 PP."""
    display_name = "Easy Deaths"


class RandomFlavors(DefaultOnToggle):
    """Randomizes the non-plain window color options."""
    display_name = "Random Flavors"


class DeathLinkMode(Choice):
    """Controls how receiving a Deathlink functions in battle.
       Instant: The player will be instantly defeated.
       Mortal: All characters will receieve mortal damage. The player will not be able to heal until the battle is finished.
       Mortal Mercy: All characters will receieve mortal damage, but the player will be able to heal it before they die.
       Regardless of this setting, receiving a deathlink outside of battle will always instantly defeat the player."""
    display_name = "Death Link Mode"
    option_instant = 0
    option_mortal = 1
    option_mortal_mercy = 2
    default = 1


class RandomBattleBG(Toggle):
    """Generates random battle backgrounds."""
    display_name = "Randomize Battle Backgrounds"


class RandomSwirlColors(Toggle):
    """Generates random colors for pre-battle swirls."""
    display_name = "Randomize Swirl Colors"


class RemoteItems(Toggle):
    """If enabled, you will receive your own items from the server upon collecting them, rather than locally.
       This allows co-op within the same game, and protects against loss of save data.
       However, you will not be able to play offline if this is enabled."""
    display_name = "Remote Items"


class PlandoLumineHallText(FreeText):
    """Set text to be displayed at Lumine Hall. If nothing is entered, random community-submitted text will be selected instead."""
    display_name = "Lumine Hall Text Plando"
    visibility = Visibility.none


class Armorizer(Choice):
    """All equippable armor will have randomly generated attributes. This includes who can equip it, elemental resistance (and how strong that resistance is),
       defense, and the secondary stat it increases (Either Luck or Speed, depending on armor slot.) Choosing "Help!" from the Goods menu will give you exact details
       on that piece of equipment.
       Keep Type: Equipment will keep its original equipment slot. If Progressive Armor is enabled, you will get armor with progressively higher defense. 
       Chaos: Equipment will have a randomly selected slot. It will try to respect the defense progressively, but the type may not match the type received."""
    display_name = "Armorizer"
    option_off = 0
    option_keep_type = 1
    option_chaos = 2
    default = 0


class Weaponizer(Choice):
    """All weapons will have randomly generated attributes. This includes offense, guts boost, and miss rate.
       Keep Type: Equipment will keep the character that was originally able to use it. If Progressive Weapons is enabled, you will get weapons with progressively higher offense.
       Chaos: Equipment will be able to be equipped by a randomly selected character. It will try to respect the offense progresively, but the type may not match the type recieved.
       The Tee Ball Bat will always be a weapon for Ness."""
    display_name = "Weaponizer"
    option_off = 0
    option_keep_type = 1
    option_chaos = 2
    default = 0


class ElementChance(Range):
    """Percent chance for any given Body/Other equipment to have elemental protection.
       Affects Armorizer only."""
    display_name = "Elemental Resistance Chance"
    range_start = 1
    range_end = 50
    default = 15


class NoFreeSancs(Toggle):
    """If enabled, the entrance to Lilliput Steps and Fire Spring will be locked and require extra key items to access.
       These items are the Tiny Key and Tenda Lavapants, respectively."""
    display_name = "No Free Sanctuaries"


class RandomizeFanfares(Choice):
    """Randomizes fanfares."""
    display_name = "Randomize Fanfares"
    option_off = 0
    option_on = 1
    option_on_no_sound_stone_fanfares = 2
    default = 0


class RandomizeBattleMusic(Toggle):
    """Randomizes in-battle songs."""
    display_name = "Randomize Battle Music"


class RandomizeOverworldMusic(Choice):
    """Randomizes music on the overworld. Some sound effects might sound weird.
       Normal: Does not randomize music.
       Match Type: Music will be randomized with similar song categories (Town, dungeon, etc.)
       Full: Overworld music will be randomized disregarding categories."""
    display_name = "Overworld Music Randomizer"
    option_normal = 0
    option_match_type = 1
    option_full = 2
    default = 0


class RandomizePSIPalettes(Choice):
    """Randomizes the colors of PSI spells.
       Normal: Doesn't randomize PSI colors.
       Shuffled: PSI spell palettes are swapped around with each other.
       Randomized: PSI spells use completely random colors."""
    display_name = "Random PSI Palettes"
    option_normal = 0
    option_shuffled = 1
    option_randomized = 2
    default = 0


class ShopRandomizer(Choice):
    """Randomizes items in shops.
       Local Filler: Shops contain only random items for yourself and are not checks.
       Shopsanity. Every shop slot in the game contains a Multiworld location. ONLY ENABLE SHOPSANITY IF YOU KNOW WHAT YOU ARE DOING."""
    display_name = "Shop Randomizer"
    option_off = 0
    option_local_filler = 1
    option_shopsanity = 2
    default = 0


class ScoutShopChecks(Choice):
    """Scouts Shop checks when you open a shop. Only affects shops in Shopsanity mode."""
    display_name = "Scout Shop Checks"
    option_off = 0
    option_progression_only = 1
    option_all = 2
    default = 1


class StartingCharacter(Choice):
    """Sets which character you start as. Each character will always start with the ability to teleport,
       and the ATM card. Ness will not be required to fight Sanctuary bosses."""
    display_name = "Starting Character"
    option_Ness = 0
    option_Paula = 1
    option_Jeff = 2
    option_Poo = 3
    default = 0


class EquipamizerStatCap(DefaultOnToggle):
    """If enabled, the highest value that Equipamizer can roll for a piece of equipment's
       main stat will be capped. 80 for armor, 125 for weapons.
       If disabled, the main stat can potentially roll up to 128."""
    display_name = "Equipamizer Stat Cap"


class MoneyDropMultiplier(Range):
    """Multiplies money dropped by enemies by the chosen value."""
    display_name = "Money Drop Multiplier"
    range_start = 1
    range_end = 100
    default = 1


class EnemyShuffle(Toggle):
    """Shuffles Non-boss enemies amongst each other."""
    display_name = "Enemy Shuffle"


class SkipEpilogue(Toggle):
    """If enabled, the choice to play the epilogue after beating Giygas will be removed, and you will
       go directly to the credits. This option is mainly for no-release seeds where checks could be
       potentially spoiled in the open-access epilogue."""
    display_name = "Skip Epilogue"
    visibility = Visibility.template


class EnergyLink(Toggle):
    """If enabled, the money in the ATM will be linked across the Archipelago Server.
       This requires a server connection to be used, but won't break offline play."""
    display_name = "Energy Link"


class DungeonShuffle(Toggle):
    """Shuffles Dungeon entrances amongst each other."""
    display_name = "Dungeon Shuffle"


class PhotoCount(Range):
    """How many Photograph traps are placed in the item pool."""
    display_name = "Photos in pool"
    range_start = 0
    range_end = 32
    default = 20


class EasyCombat(Toggle):
    """Automatically halves all scaled enemy levels."""
    display_name = "Easy Combat"


class EnemizerStats(Toggle):
    """Randomizes base stats and level of non-boss enemies."""
    display_name = "Randomize Enemy Stats"


class EnemizerAttacks(Toggle):
    """Randomizes attacks of non-boss enemies."""
    display_name = "Randomize Enemy Attacks"


class EnemizerAttributes(Toggle):
    """Randomizes most attributes of non-boss enemies."""
    display_name = "Randomize Enemy Attributes"


class RandomMapColors(Choice):
    """Randomizes map colors.
       Normal: Uses normal colors
       Nice: Uses generally good looking palettes for maps with little artifacting.
       Ugly: Allows map palettes with artifacting or colors that may not look good.
       Nonsense: Allows really bad palettes or heavy artifacting."""
    display_name = "Shuffle Map Palettes"
    option_normal = 0
    option_nice = 1
    option_ugly = 2
    option_nonsense = 3
    default = 0

class SafeFinalBoss(DefaultOnToggle):
    """Prevents specific difficult bosses from being randomized onto Heavily Armed Pokey's boss slot.
       Only affects Boss Shuffle, and does not affect Phase 2 Giygas if Boss Shuffle Add Giygas is enabled."""
    display_name = "Safe Final Boss"


@dataclass
class EBOptions(PerGameCommonOptions):
    giygas_required: GiygasRequired
    sanctuaries_required: SanctuariesRequired
    skip_prayer_sequences: ShortenPrayers
    random_start_location: RandomStartLocation
    alternate_sanctuary_goal: SanctuaryAltGoal
    magicant_mode: MagicantMode
    monkey_caves_mode: MonkeyCavesMode
    local_teleports: LocalTeleports
    character_shuffle: CharacterShuffle
    starting_character: StartingCharacter
    psi_shuffle: PSIShuffle
    allow_flash_as_favorite_thing: BanFlashFavorite
    enemy_shuffle: EnemyShuffle
    boss_shuffle: BossShuffle
    decouple_diamond_dog: DecoupleDiamondDog
    boss_shuffle_add_giygas: ShuffleGiygas
    safe_final_boss: SafeFinalBoss
    randomize_enemy_attributes: EnemizerAttributes
    randomize_enemy_stats: EnemizerStats
    randomize_enemy_attacks: EnemizerAttacks
    experience_modifier: ExperienceModifier
    money_drop_multiplier: MoneyDropMultiplier
    starting_money: StartingMoney
    easy_deaths: EasyDeaths
    easy_combat: EasyCombat
    progressive_weapons: ProgressiveWeapons
    progressive_armor: ProgressiveArmor
    armorizer: Armorizer
    weaponizer: Weaponizer
    armorizer_resistance_chance: ElementChance
    equipamizer_cap_stats: EquipamizerStatCap
    auto_scale_party_members: AutoscaleParty
    remote_items: RemoteItems
    random_flavors: RandomFlavors
    random_battle_backgrounds: RandomBattleBG
    random_swirl_colors: RandomSwirlColors
    presents_match_contents: PresentSprites
    nonlocal_items_use_local_presents: NoAPPresents
    prefixed_items: PreFixItems
    total_photos: PhotoCount
    randomize_franklinbadge_protection: RandomFranklinBadge
    shuffle_enemy_drops: ShuffleDrops
    common_filler_weight: CommonWeight
    uncommon_filler_weight: UncommonWeight
    rare_filler_weight: RareWeight
    money_weight: MoneyWeight
    plando_lumine_hall_text: PlandoLumineHallText
    no_free_sanctuaries: NoFreeSancs
    randomize_overworld_music: RandomizeOverworldMusic
    randomize_battle_music: RandomizeBattleMusic
    randomize_fanfares: RandomizeFanfares
    randomize_psi_palettes: RandomizePSIPalettes
    map_palette_shuffle: RandomMapColors
    shop_randomizer: ShopRandomizer
    scout_shop_checks: ScoutShopChecks
    dungeon_shuffle: DungeonShuffle
    skip_epilogue: SkipEpilogue
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    death_link_mode: DeathLinkMode
    energy_link: EnergyLink


eb_option_groups = [
    OptionGroup("Goal Settings", [
        GiygasRequired,
        SanctuariesRequired,
        SanctuaryAltGoal
    ]),
    
    OptionGroup("Item Settings", [
        LocalTeleports,
        CharacterShuffle,
        ProgressiveWeapons,
        ProgressiveArmor,
        RandomFranklinBadge,
        CommonWeight,
        UncommonWeight,
        RareWeight,
        MoneyWeight,
        PreFixItems,
        PhotoCount
    ]),

    OptionGroup("Equipamizer", [
        Armorizer,
        Weaponizer,
        ElementChance,
        EquipamizerStatCap
    ]),

    OptionGroup("World Modes", [
        RandomStartLocation,
        MagicantMode,
        MonkeyCavesMode,
        NoFreeSancs,
        StartingCharacter
    ]),

    OptionGroup("PSI Randomization", [
        PSIShuffle,
        BanFlashFavorite
    ]),

    OptionGroup("Enemy Randomization", [
        EnemyShuffle,
        BossShuffle,
        SafeFinalBoss,
        DecoupleDiamondDog,
        ShuffleGiygas,
        ExperienceModifier,
        ShuffleDrops,
        MoneyDropMultiplier
    ]),

    OptionGroup("Enemizer", [
        EnemizerAttributes,
        EnemizerAttacks,
        EnemizerStats
    ]),

    OptionGroup("Shop Randomization", [
        ShopRandomizer,
        ScoutShopChecks
    ]),

    OptionGroup("Entrance Randomization", [
        DungeonShuffle
    ]),

    OptionGroup("Convenience Settings", [
        ShortenPrayers,
        EasyDeaths,
        StartingMoney,
        RemoteItems,
        AutoscaleParty,
        SkipEpilogue,
        EasyCombat
    ]),

    OptionGroup("Aesthetic Settings", [
        RandomFlavors,
        RandomSwirlColors,
        RandomBattleBG,
        RandomMapColors,
        PresentSprites,
        NoAPPresents,
        RandomizePSIPalettes,
        PlandoLumineHallText
    ]),

    OptionGroup("Music Randomizer", [
        RandomizeOverworldMusic,
        RandomizeBattleMusic,
        RandomizeFanfares
    ]),

    OptionGroup("Multiplayer Features", [
        DeathLink,
        DeathLinkMode,
        EnergyLink
    ])
]

import typing

from BaseClasses import MultiWorld
from Options import Choice, Range, Option, Toggle, DefaultOnToggle, DeathLink, OptionDict, OptionList


class Logic(Choice):
    """Determine the logic used to reach locations."""
    display_name = "Glitch Logic"
    option_no_glitches = 0
    option_minor_glitches = 1
    option_overworld_glitches = 2
    option_hybrid_major_glitches = 3
    option_no_logic = 4
    alias_owg = 2
    alias_hmg = 3


class DarkRoomLogic(Choice):
    """Requirement to traverse unlit dark rooms."""
    display_name = "Dark Room Logic"
    option_lamp = 0
    option_torches = 1
    option_none = 2


class GlitchBoots(DefaultOnToggle):
    """Start with Pegasus Boots if any glitches that use them are available."""
    display_name = "Glitched Starting Boots"


class OpenPyramid(Choice):
    """Determines whether the hole at the top of pyramid is open.
    Goal will open the pyramid if the goal requires you to kill Ganon, without needing to kill Agahnim 2.
    Auto is the same as goal except if Ganon's dropdown is in another location, the hole will be closed."""
    display_name = "Open Pyramid Hole"
    option_closed = 0
    option_open = 1
    option_goal = 2
    option_auto = 3
    default = option_goal

    alias_true = option_open
    alias_false = option_closed
    alias_yes = option_open
    alias_no = option_closed

    def to_bool(self, world: MultiWorld, player: int) -> bool:
        if self.value == self.option_goal:
            return world.goal[player] in {'crystals', 'ganontriforcehunt', 'localganontriforcehunt', 'ganonpedestal'}
        elif self.value == self.option_auto:
            return world.goal[player] in {'crystals', 'ganontriforcehunt', 'localganontriforcehunt', 'ganonpedestal'} \
            and (world.shuffle[player] in {'vanilla', 'dungeonssimple', 'dungeonsfull', 'dungeonscrossed'} or not
                 world.shuffle_ganon)
        elif self.value == self.option_open:
            return True
        else:
            return False


class DungeonItem(Choice):
    value: int
    option_original_dungeon = 0
    option_own_dungeons = 1
    option_own_world = 2
    option_any_world = 3
    option_different_world = 4
    option_start_with = 6
    alias_true = 3
    alias_false = 0

    @property
    def in_dungeon(self):
        return self.value in {0, 1}

    @property
    def hints_useful(self):
        """Indicates if hints for this Item are useful in any way."""
        return self.value in {1, 2, 3, 4}


class bigkey_shuffle(DungeonItem):
    """How Big Keys will be placed."""
    item_name_group = "Big Keys"
    display_name = "Big Key Shuffle"


class smallkey_shuffle(DungeonItem):
    """How Small Keys will be placed."""
    option_universal = 5
    item_name_group = "Small Keys"
    display_name = "Small Key Shuffle"


class compass_shuffle(DungeonItem):
    """How Compasses will be placed."""
    item_name_group = "Compasses"
    display_name = "Compass Shuffle"


class map_shuffle(DungeonItem):
    """How maps will be placed."""
    item_name_group = "Maps"
    display_name = "Map Shuffle"


class Crystals(Range):
    range_start = 0
    range_end = 7
    default = 7


class CrystalsTower(Crystals):
    """Number of Crystals needed to enter Ganon's Tower."""
    display_name = "Crystals for Ganon's Tower"


class CrystalsGanon(Crystals):
    """Number of Crystals needed to damage Ganon."""
    display_name = "Crystals for Ganon"


class TriforcePieces(Range):
    default = 30
    range_start = 1
    range_end = 90


class TriforceMode(Choice):
    """Determines how extra available triforce pieces are calculated. Up to 90 can be available.
    Extra makes available pieces = extra + required.
    Percentage makes available pieces = percentage * required.
    Available makes available pieces = available value."""
    display_name = "Triforce Pieces Mode"
    option_extra = 0
    option_percentage = 1
    option_available = 2
    default = option_available


class TriforceExtra(TriforcePieces):
    """How many extra Triforce pieces are available."""
    display_name = "Extra Triforce Pieces"
    default = 10


class TriforcePercentage(Range):
    """Percentage of required Triforce pieces that will be available."""
    range_start = 100
    range_end = 200
    default = 150


class TriforceAvailable(TriforcePieces):
    """Total number of available Triforce pieces."""
    display_name = "Triforce Pieces Available"
    default = 30


class TriforceRequired(TriforcePieces):
    """Number of Triforce pieces required to complete the goal."""
    display_name = "Triforce Pieces Required"
    default = 20


class ShopItemSlots(Range):
    """Number of shop slots that can contain items from the multiworld."""
    display_name = "Shop Item Slots"
    range_start = 0
    range_end = 30


class ShopPriceModifier(Range):
    """Percentage modifier for shuffled item prices in shops"""
    display_name = "Shop Item Price"
    range_start = 0
    default = 100
    range_end = 400


class PrizeShuffle(Choice):
    """Affects how prize packs that enemies drop get shuffled around."""
    display_name = "Prize Pack Shuffle"
    option_none = 0
    option_general = 1
    option_bonk = 2
    option_both = 3
    alias_g = 1
    alias_b = 2
    alias_bg = 3
    default = option_general


class WorldState(Choice):
    """Starting world state for the game.
    Standard starts with the rain sequence and uncle will have a guaranteed weapon including bombs.
    Open starts at Link's House in Light World with the player free to go anywhere.
    Inverted begins at Link's House in the Dark World, requiring Moon Pearl for Light World access as well as other
    changes."""
    display_name = "World State"
    option_standard = 1
    option_open = 0
    option_inverted = 2


class Medallions(Choice):
    option_ether = 0
    option_bombos = 1
    option_quake = 2
    default = "random"


class MireMedallion(Medallions):
    """Required medallion to open Misery Mire entrance."""
    display_name = "Misery Mire Medallion"


class TurtleMedallion(Medallions):
    """Required medallion to open Turtle Rock entrance."""
    display_name = "Turtle Rock Medallion"


class Bosses(Choice):
    option_vanilla = 0
    option_simple = 1
    option_full = 2
    option_chaos = 3
    option_singularity = 4


class Enemies(Choice):
    option_vanilla = 0
    option_shuffled = 1
    option_chaos = 2


class Counters(Choice):
    """Determines if an item counter shows up in dungeons.
    Default will be True if compasses are in their own dungeons, otherwise on pickup."""
    display_name = "Dungeon Item Counter"
    option_off = 0
    option_compass = 1
    option_default = 2
    option_on = 3
    alias_pickup = option_compass
    alias_true = 3
    alias_false = 0
    default = option_compass


class Progressive(Choice):
    display_name = "Progressive Items"
    option_off = 0
    option_grouped_random = 1
    option_on = 2
    alias_false = 0
    alias_true = 2
    default = 2

    def want_progressives(self, random):
        return random.choice([True, False]) if self.value == self.option_grouped_random else bool(self.value)


class Swordless(Toggle):
    """No swords. Curtains in Skull Woods and Agahnim\'s
    Tower are removed, Agahnim\'s Tower barrier can be
    destroyed with hammer. Misery Mire and Turtle Rock
    can be opened without a sword. Hammer damages Ganon.
    Ether and Bombos Tablet can be activated with Hammer
    (and Book)."""
    display_name = "Swordless"


class Difficulty(Choice):
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    default = option_normal


class ItemPool(Difficulty):
    """Determines the frequency of useful items in the pool.
    Easy doubles the number of upgrades and progressive weapons and armor.
    Hard has maximum of: 14 hearts, blue mail, tempered sword, red shield, and
    silvers are removed if glitch logic is enabled.
    Expert has maximum of: 8 hearts, green mail, master sword, fighter shield,
    and silvers are removed if glitch logic is enabled."""
    display_name = "Item Pool"


class ItemFunc(Difficulty):
    """Modifies the functionality of certain items within the item pool.
    Easy allows hammer to damage ganon and collect tablets, and medallions can be used anywhere without a sword.
    Hard makes potions less effective, faeries can't be caught,cape uses double magic,
    byrna does not grant invulnerability, boomerangs do not stun, and silvers are disabled outside Ganon.
    Expert is like hard except potions are even weaker, and hookshot does not stun."""
    display_name = "Item Functionality"


# Might be a decent idea to split "Bow" into its own option with choices of
# Defer to Progressive Option (default), Progressive, Non-Progressive, Bow + Silvers, Retro
class RetroBow(Toggle):
    """Zelda-1 like mode. You have to purchase a quiver to shoot arrows using rupees."""
    display_name = "Retro Bow"


class RetroCaves(Toggle):
    """Zelda-1 like mode. There are randomly placed take-any caves that contain one Sword and
    choices of Heart Container/Blue Potion."""
    display_name = "Retro Caves"


class RestrictBossItem(Toggle):
    """Don't place dungeon-native items on the dungeon's boss."""
    display_name = "Prevent Dungeon Item on Boss"


class Hints(Choice):
    """On/Full: Put item and entrance placement hints on telepathic tiles and some NPCs, Full removes joke hints."""
    display_name = "Hints"
    option_off = 0
    option_on = 2
    option_full = 3
    default = 2
    alias_false = 0
    alias_true = 2


class Scams(Choice):
    """If on, these Merchants will no longer tell you what they're selling."""
    display_name = "Scams"
    option_off = 0
    option_king_zora = 1
    option_bottle_merchant = 2
    option_all = 3
    alias_false = 0

    @property
    def gives_king_zora_hint(self):
        return self.value in {0, 2}

    @property
    def gives_bottle_merchant_hint(self):
        return self.value in {0, 1}


class EnemyShuffle(Toggle):
    """Randomize every enemy spawn.
    If mode is Standard, Hyrule Castle is left out (may result in visually wrong enemy sprites in that area.)"""
    display_name = "Enemy Shuffle"


class EnemyDamage(Choice):
    """Randomizes the amount of damage enemies deal.
    Shuffled causes enemies to deal from 0-4 hearts and armor upgrades always help.
    Chaos causes enemies to deal from 0-8 hearts and armor reshuffles the damage."""
    display_name = "Enemy Damage"
    option_default = 0
    option_shuffled = 1
    option_chaos = 2
    alias_none = 0


class EnemyHealth(Choice):
    """Modifies amount of health that enemies have.
    Easy reduces their health, hard increases it, and expert greatly increases it."""
    display_name = "Enemy Health"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3

    alias_default = option_normal
    default = option_normal


class KillableThieves(Toggle):
    """Makes Thieves killable."""
    display_name = "Killable Thieves"


class BushShuffle(Toggle):
    """Randomize chance that a bush contains an enemy as well as which enemy may spawn."""
    display_name = "Bush Shuffle"


class TileShuffle(Toggle):
    """Randomize flying tiles floor patterns."""
    display_name = "Tile Shuffle"


class PotShuffle(Toggle):
    """Shuffle contents of pots within "supertiles" (item will still be nearby original placement)."""
    display_name = "Pot Shuffle"


class Palette(Choice):
    option_default = 0
    option_good = 1
    option_blackout = 2
    option_puke = 3
    option_classic = 4
    option_grayscale = 5
    option_negative = 6
    option_dizzy = 7
    option_sick = 8


class OWPalette(Palette):
    display_name = "Overworld Palette"


class UWPalette(Palette):
    display_name = "Underworld Palette"


class HUDPalette(Palette):
    display_name = "Menu Palette"


class SwordPalette(Palette):
    display_name = "Sword Palette"


class ShieldPalette(Palette):
    display_name = "Shield Palette"


class LinkPalette(Palette):
    display_name = "Link Palette"


class HeartBeep(Choice):
    display_name = "Heart Beep Rate"
    option_normal = 0
    option_double = 1
    option_half = 2
    option_quarter = 3
    option_off = 4
    alias_false = 4


class HeartColor(Choice):
    display_name = "Heart Color"
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3


class QuickSwap(DefaultOnToggle):
    display_name = "L/R Quickswapping"


class MenuSpeed(Choice):
    display_name = "Menu Speed"
    option_normal = 0
    option_instant = 1,
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5


# TODO this is a bad way to do this. maybe turn enabled into a toggle then the rest of these into an Optionlist?
class RandomSprite(OptionDict):
    """Allows different random sprite events to be simultaneously enabled."""
    display_name = "Random Sprite On Event"
    valid_keys = {"enabled", "on_hit", "on_enter", "on_exit", "on_slash",
                  "on_item", "on_bonk", "on_everything", "use_weighted_sprite_pool"}
    default = {
        "enabled": "off",
        "on_hit": "on",
        "on_enter": "off",
        "on_exit": "off",
        "on_slash": "off",
        "on_item": "off",
        "on_bonk": "off",
        "on_everything": "off",
        "use_weighted_sprite_bool": "off"
    }


class SpritePool(OptionList):
    """Limits the pool of available sprites for random events to specified pool."""
    valid_keys = {"Abigail", "Adol", "Adventure 2600", "Aggretsuko", "Alice", "Angry Video Game Nerd", "Arcane",
                  "ArcticArtemisFox", "Aria", "Ark (Cape)", "Ark (No Cape)", "Arrghus", "Astor", "Astronaut", "Asuna",
                  "B.S. Boy", "B.S. Girl", "Baba", "Baby Fro", "Baby Metroid", "Badeline", "Bananas in Pyjamas",
                  "Bandit", "Batman", "Beau", "Bee", "Bel", "Bewp", "Big Key", "Birb", "Birb of Paradise", "Birdfruit",
                  "Birdo", "Black Mage", "Blacksmith Link", "Blazer", "Blossom", "Bob", "Bob Ross", "Boco the Chocobo",
                  "Boo", "Boo 2", "Bottle o' Goo", "BotW Link", "BotW Zelda", "Bowser", "Bowsette", "Bowsette Red",
                  "Branch", "Brian", "Broccoli", "Bronzor", "Bubbles", "Bullet Bill", "Buttercup", "Cactuar", "Cadence",
                  "Captain Novolin", "Captain Toadette", "CarlSagan42", "Casual Zelda", "Cat Boo", "Catgirl (Hidari)",
                  "CD-i Link", "Celes", "Centaur Enos", "Charizard", "Cheep Cheep", "Chef Pepper", "Chibity", "Chrizzz",
                  "Chrono", "Cinna", "Cirno", "Clifford", "Clippy", "Cloud", "Clyde", "Conker", "Conker Neo", "Cornelius",
                  "Corona", "Crewmate", "Cucco", "Cursor", "D.Owls", "Dark Boy", "Dark Girl", "Dark Link",
                  "Dark Link (Tunic)", "Dark Link (Zelda 2)", "Dark Panda", "Dark Swatchy", "Dark Zelda", "Dark Zora",
                  "Deadpool (Mythic)", "Deadpool (SirCzah)", "Deadrock", "Decidueye", "Dekar", "Demon Link", "Dennsen86",
                  "Diddy Kong", "Dig Dug", "Dipper", "DQ Slime", "Dragonair", "Dragonite", "Drake The Dragon", "Eevee",
                  "Eggplant", "Eirika", "Ema Skye", "EmoSaru", "Espeon", "Ezlo", "Fierce Diety Link", "Figaro Merchant",
                  "Finn Merten", "Finny Bear", "Flavor Guy", "Floodgate Fish", "Four Swords Link", "Fox Link",
                  "Freya Crescent", "Frisk", "Frog Link", "Fujin", "Future Trunks", "Gamer", "Ganondorf", "Garfield",
                  "Garnet", "Garo Master", "GBC Link", "Geno", "GliitchWiitch", "Glove Color Link", "Gobli", "Goomba",
                  "Goose", "Graalian Noob", "GrandPOOBear", "Gretis", "Growlithe", "Gruncle Stan", "Guiz", "Hanna",
                  "Hardhate Beetle", "Hat Color Link", "Hat Kid", "Head Link", "Headless Link", "Heem", "Hello Kitty",
                  "Hero of Awakening", "Hero of Hyrule", "Hint Tile", "Hoarder (Bush)", "Hoarder (Pot)",
                  "Hoarder (Rock)", "Hollow Knight", "Hollow Knight (Malmo/Winter", "Homer Simpson", "Hornet",
                  "Horseman", "Hotdog", "Hyrule Knight", "Hyrule Soldier", "iBazly", "Ignignokt", "Informant Woman",
                  "Inkling", "Invisible Link", "Jack Frost", "Jason Frudnick", "Jasp", "Jogurt", "Juste Belmont",
                  "Juzcook", "Kaguya", "Kain", "Katsura", "Kecleon", "Kefka", "Kenny McCormick", "Ketchup", "Kholdstare",
                  "King Gothalion", "King Graham", "Kinu", "Kira", "Kirby", "Kirby (Dreamland 3)", "Koragi", "Kore8",
                  "Korok", "Kriv", "Lakitu", "Lapras", "League Mascot", "Lest", "Lestat", "Lily", "Linja",
                  "Link (Zelda 1)", "Link Redrawn", "Little Hylian", "Locke", "Lucario", "Luffy", "Luigi", "Luna Maindo",
                  "Lynel (BotW)", "Mad_Tears", "Madeline", "Magus", "Maiden", "Majora's Mask", "Mallow (Cat)",
                  "Manga Link", "Maple Queen", "Marin", "Mario (Classic)", "Mario and Cappy", "Marisa Kirisame",
                  "Marvin the Cat", "Matthias", "Meatwad", "Medallions", "Medli", "Mega Man (Classic)", "Megaman X",
                  "Megaman X2", "MewLp", "Mike Jones", "Mimic", "Mini Ganon", "Minish Cap Link", "Minish Link", "Mipha",
                  "missingno", "Moblin", "Modern Link", "Mog", "Momiji Inubashiri", "Moosh", "Mouse", "Ms. Paint Dog",
                  "Nature Link", "Navi", "Navirou", "Ned Flanders", "Negative Link", "Neosad", "Neptune", "NES Link",
                  "Ness", "Nia", "Niddraig", "Niko", "Ninten", "Octorok", "Old Man", "Olde Man", "Ori", "Outline Link",
                  "Paper Mario", "Parallel Worlds Link", "Paula", "Penguin Link", "Pete", "Phoenix Wright", "Pikachu",
                  "Pink Ribbon Link", "Piranha Plant", "Plague Knight", "Plouni", "PoC Link", "Pokey", "Pony", "Popoi",
                  "Poppy", "Porg Knight", "Power Ranger", "Power Up with Pride Mushroom", "Powerpuff Girl", "Pride Link",
                  "Primm", "Princess Bubblegum", "Princess Peach", "Prof.Renderer Grizzleton", "Psyduck", "Purple Chest",
                  "Pyro", "QuadBanger", "Rainbow Link", "Rat", "Red Mage", "Reimu Hakurei (HoxNorf)", "Remeer",
                  "Remus R Black", "Reverse Mail Order", "Rick", "Robo-Link 9000", "Rocko", "Rottytops", "Rover",
                  "Roy Koopa", "Rumia", "Rydia", "Ryu", "Sailor Jupiter", "Sailor Mars", "Sailor Mercury", "Sailor Moon",
                  "Sailor Venus", "Saitama", "Samurott", "Samus", "Samus (Classic)", "Samus (Super Metroid)",
                  "Santa Hat Link", "Santa Link", "Scholar", "Selan", "SevenS1ns", "Shadow", "Shadow Sakura", "Shantae",
                  "Shinmyoumaru Sukuna", "Shuppet", "Shy Gal", "Shy Guy", "SighnWaive", "Skunk", "Slowpoke",
                  "SNES Controller", "Sobble", "Soda Can", "Sokka", "Solaire of Astora", "Sonic the Hedgehog", "Sora",
                  "Sora (KH1)", "Spiked Roller", "SpongeBob SquarePants", "Spyro the Dragon", "Squall", "Squirrel",
                  "Squirtle", "Stalfos", "Stan", "Static Link", "Steamed Ham", "Stick Man", "Super Bomb", "Super Bunny",
                  "Super Meat Boy", "Susie", "Swatchy", "Swiper", "Tanooki Mario", "TASBot", "Tea Time", "Terra (Esper)",
                  "Terry", "Tetra Sheet", "TGH", "The Professor", "The Pug", "Thief", "ThinkDorm", "Thomcrow", "Tile",
                  "Tingle", "TMNT", "Toad", "Toadette", "TotemLinks", "TP Zelda", "Trogdor the Burninator",
                  "Tunic Color Link", "TwoFaced", "Ty the Tasmanian Tiger", "Ultros", "Umbreon", "Valeera",
                  "VanillaLink", "Vaporeon", "Vegeta", "Vera", "Vitreous", "Vivi", "Vivian", "Wario", "White Mage",
                  "Will", "Wizzrobe", "Wolf Link (Festive)", "Wolf Link (TP)", "Yoshi", "Yunica Tovah", "Zandra",
                  "Zaruvyen", "Zebra Unicorn", "Zeckemyro", "Zelda", "Zero Suit Samus", "Zora"}


# # TODO obviously waiting on the freetext options
# class Sprite(TextChoice):
#     valid_keys = SpritePool.valid_keys
#     option_link = 0
#     option_random_on_hit = 1
#     option_random_on_enter = 2
#     option_random_on_exit = 3
#     option_random_on_slash = 4
#     option_random_on_item = 5
#     option_random_on_bonk = 6
#     option_random_on_all = 7
#
#     def verify(self, world, player_name, plando_options) -> None:
#         if isinstance(self.value, int):
#             return
#         if self.value in self.valid_keys:
#             return
#         raise ValueError(f"{self.value} for {player_name} is not a valid Sprite option.")
#

class Music(DefaultOnToggle):
    display_name = "Play music"


class ReduceFlashing(DefaultOnToggle):
    display_name = "Reduce Screen Flashes"


class TriforceHud(Choice):
    display_name = "Display Method for Triforce Hunt"
    option_normal = 0
    option_hide_goal = 1
    option_hide_required = 2
    option_hide_both = 3


class BeemizerRange(Range):
    value: int
    range_start = 0
    range_end = 100


class BeemizerTotalChance(BeemizerRange):
    """Percentage chance for each junk-fill item (rupees, bombs, arrows) to be
    replaced with either a bee swarm trap or a single bottle-filling bee."""
    default = 0
    display_name = "Beemizer Total Chance"


class BeemizerTrapChance(BeemizerRange):
    """Percentage chance for each replaced junk-fill item to be a bee swarm
    trap; all other replaced items are single bottle-filling bees."""
    default = 60
    display_name = "Beemizer Trap Chance"


class AllowCollect(Toggle):
    """Allows for !collect / co-op to auto-open chests containing items for other players.
    Off by default, because it currently crashes on real hardware."""
    display_name = "Allow Collection of checks for other players"


alttp_options: typing.Dict[str, type(Option)] = {
    "glitches_required": Logic,
    "dark_room_logic": DarkRoomLogic,
    "glitch_boots": GlitchBoots,
    "world_state": WorldState,
    "crystals_needed_for_gt": CrystalsTower,
    "crystals_needed_for_ganon": CrystalsGanon,
    "open_pyramid": OpenPyramid,
    "triforce_pieces_mode": TriforceMode,
    "triforce_pieces_extra": TriforceExtra,
    "triforce_pieces_percentage": TriforcePercentage,
    "triforce_pieces_available": TriforceAvailable,
    "triforce_pieces_required": TriforceRequired,
    "bigkey_shuffle": bigkey_shuffle,
    "smallkey_shuffle": smallkey_shuffle,
    "compass_shuffle": compass_shuffle,
    "map_shuffle": map_shuffle,
    "dungeon_counters": Counters,
    "progressive": Progressive,
    "swordless": Swordless,
    "item_pool": ItemPool,
    "item_functionality": ItemFunc,
    "retro_bow": RetroBow,
    "retro_caves": RetroCaves,
    "hints": Hints,
    "scams": Scams,
    "restrict_dungeon_item_on_boss": RestrictBossItem,
    "pot_shuffle": PotShuffle,
    "misery_mire_medallion": MireMedallion,
    "turtle_rock_medallion": TurtleMedallion,
    "enemy_shuffle": EnemyShuffle,
    "enemy_damage": EnemyDamage,
    "enemy_health": EnemyHealth,
    "killable_thieves": KillableThieves,
    "bush_shuffle": BushShuffle,
    "shop_item_slots": ShopItemSlots,
    "shop_price_modifier": ShopPriceModifier,
    "shuffle_prizes": PrizeShuffle,
    "tile_shuffle": TileShuffle,
    "ow_palettes": OWPalette,
    "uw_palettes": UWPalette,
    "hud_palettes": HUDPalette,
    "sword_palettes": SwordPalette,
    "shield_palettes": ShieldPalette,
    "link_palettes": LinkPalette,
    "heartbeep": HeartBeep,
    "heartcolor": HeartColor,
    "quickswap": QuickSwap,
    "menuspeed": MenuSpeed,
    "music": Music,
    "reduceflashing": ReduceFlashing,
    "triforcehud": TriforceHud,
    "beemizer_total_chance": BeemizerTotalChance,
    "beemizer_trap_chance": BeemizerTrapChance,
    "death_link": DeathLink,
    "allow_collect": AllowCollect
}

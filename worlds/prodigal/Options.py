from dataclasses import dataclass
from Options import Toggle, Range, Choice, PerGameCommonOptions
from typing import Dict, List

class SpecificKeys(Toggle):
    """Normal keys are specific to a dungeon. The key count for each dungeon may be found in extra pages in the pause menu. Turn off to make normal keys act like in vanilla. If off, you may need to buy keys from Zaegul."""
    display_name = "Specific Keys"

class ColorsRequired(Range):
    """Number of colors out of 5 needed to enter the Lighthouse."""
    display_name = "Colors Required"
    range_start = 0
    range_end = 5
    default = 5

class BlessingsRequired(Range):
    """Number of blessings out of 5 needed to access Enlightenment or to get the Hero's Rest ending."""
    display_name = "Blessings Required"
    range_start = 0
    range_end = 5
    default = 5

class CrestFragmentsRequired(Range):
    """Number of crest fragments out of 5 needed to get past the door in Castle Vann."""
    display_name = "Crest Fragments Required"
    range_start = 0
    range_end = 5
    default = 5

class CoinsOfCrowlRequired(Range):
    """Number of Coins of Crowl out of 13 needed to get past the underwater door."""
    display_name = "Coins of Crowl Required"
    range_start = 0
    range_end = 13
    default = 13

class Goal(Choice):
    """The goal of the game.
        var: Defeat Var.
        rest: Revive Torran.
        shadow: Defeat Shadow Oran.
        torran: Defeat Torran.
        any: Defeat any of the three."""
    display_name = "Goal"
    option_var = 0
    option_rest = 1
    option_shadow = 2
    option_torran = 3
    option_any = 4
    default = 0

class ColorLocations(Choice):
    """Choose where your colors can be found.
        dungeon_prizes: Colors can be found on dungeon prizes (Vulture, Tidal Frog, Water Blessing, Rat Potion, Wren, Yhote, Spirit of Vann, Ram Wraith, Loomagnos, Earth Blessing, Color Correction, Light Spirit, Stindle, Frozen Heart, Killer, Siska, Mechanized Slot Machine, Inkwell).
        local: Colors can be found anywhere in your own world.
        any: Colors can be found in any world."""
    display_name = "Color Locations"
    option_dungeon_prizes = 0
    option_local = 1
    option_any = 2
    default = 2

class BlessingLocations(Choice):
    """Choose where your blessings can be found.
        dungeon_prizes: Blessings can be found on dungeon prizes (Vulture, Tidal Frog, Water Blessing, Rat Potion, Wren, Yhote, Spirit of Vann, Ram Wraith, Loomagnos, Earth Blessing, Color Correction, Light Spirit, Stindle, Frozen Heart, Killer, Siska, Mechanized Slot Machine, Inkwell).
        local: Blessings can be found anywhere in your own world.
        any: Blessings can be found in any world."""
    display_name = "Blessing Locations"
    option_dungeon_prizes = 0
    option_local = 1
    option_any = 2
    default = 2

class LighthouseKey(Choice):
    """Choose where your lighthouse key can be found. (Only applies if Specific Keys is on)
        blessings: The lighthouse key is obtained when you return the blessings and get the Hero's Soul.
        coins: The lighthouse key is found underwater behind the door requiring coins of Crowl.
        materials: The lighthouse key is given to you by Bolivar when you give him the four materials.
        local: The lighthouse key may be found anywhere in your own world.
        any: The lighthouse key may be found in any world."""
    display_name = "Lighthouse Key"
    option_blessings = 0
    option_coins = 1
    option_materials = 2
    option_local = 3
    option_any = 4
    default = 4

class TradingQuest(Choice):
    """How to handle the trading quest.
        vanilla: The Lost Shipment and Ulni checks are randomized. The entire trading quest must be completed as in vanilla to get Ulni's check.
        skip: The Lost Shipment location and Anchor Greaves are randomized. The Lost Shipment itself is not randomized, and Ulni is not a check.
        shuffle: All items in the trading quest are randomized, and each of the corresponding NPCs is a check."""
    display_name = "Trading Quest"
    option_vanilla = 0
    option_skip = 1
    option_shuffle = 2
    default = 0

class ShuffleGrelinDrops(Toggle):
    """Grelin randomly drop four Archipelago items, and the Holy Relic, Wedding Ring, Silver Mirror, and Painting are added to the pool."""
    display_name = "Shuffle Grelin Drops"

class ShuffleHiddenItems(Toggle):
    """Include hidden overworld items in the pool."""
    display_name = "Shuffle Hidden Items"

class ShuffleBjergCastle(Toggle):
    """Include Bjerg Castle (Mariana's marriage dungeon) in the pool. A sailor near the arena will take you there."""
    display_name = "Shuffle Bjerg Castle"

class ShuffleDaemonsDive(Toggle):
    """Include Daemon's Dive in the pool."""
    display_name = "Shuffle Daemon's Dive"

class ShuffleEnlightenment(Toggle):
    """Include Enlightenment in the pool."""
    display_name = "Shuffle Enlightenment"

class ShuffleSecretShop(Toggle):
    """Include Zaegul's Secret Shop in the pool."""
    display_name = "Shuffle Secret Shop"

class SkipsInLogic(Toggle):
    """The seed may require skips such as side hits, two-tile flare jumps outside of Enlightenment, deleting objects with the Empowered Hand, and interacting with objects from a tile away."""
    display_name = "Skips In Logic"

class StartWithSpicedHam(Toggle):
    """Start with a buff that lets you run."""
    display_name = "Start With Spiced Ham"

class StartWithWingedBoots(Toggle):
    """Start with Winged Boots."""
    display_name = "Start With Winged Boots"

class SkipOneSmallFavor(Toggle):
    """Tara gives you an item directly instead of requiring you to go on a fetch quest."""
    display_name = "Skip One Small Favor"

class FakeDreadHand(Toggle):
    """Allow using teleport statues without having the dread hand."""
    display_name = "Fake Dread Hand"

class FastFishing(Toggle):
    """Only 100 points are required in the fishing minigame to get the item from Keaton and to get free fish."""
    display_name = "Fast Fishing"

class AltarToVar(Toggle):
    """Defile the altar to Var. Receive double damage."""
    display_name = "Altar to Var"

class AltarToZolei(Toggle):
    """Defile the altar to Zolei. Item drops are reduced in frequency, and you must fight Zolei alongside Var."""
    display_name = "Altar to Zolei"

class AltarToRaem(Toggle):
    """Defile the altar to Raem. Raem will attack you with beams of light, and you cannot gain extra HP through prayer."""
    display_name = "Altar to Raem"

class AltarToHate(Toggle):
    """Defile the altar to Hate. Heart ores do not increase your maximum HP."""
    display_name = "Altar to Hate"

class CurseOfFrailty(Toggle):
    """Accept the curse of frailty. You die in one hit."""
    display_name = "Curse of Frailty"

class CurseOfFamine(Toggle):
    """Accept the curse of famine. You cannot buy buffs."""
    display_name = "Curse of Famine"

class CurseOfRust(Toggle):
    """Accept the curse of rust. The pick cannot be upgraded, and boots and rings do not work, except for the Winged Boots and Wedding Rings."""
    display_name = "Curse of Rust"

class CurseOfWind(Toggle):
    """Accept the curse of wind. Doubles the speed of projectiles."""
    display_name = "Curse of Wind"

class CurseOfBlooms(Toggle):
    """Accept the curse of blooms. Enemies drop bombs when they die."""
    display_name = "Curse of Blooms"

class CurseOfCrowns(Toggle):
    """Accept the curse of crowns. You cannot marry anyone."""
    display_name = "Curse of Crowns"

class CurseOfHorns(Toggle):
    """Accept the curse of horns. All junk items, such as gold, are replaced by traps. Note that if no trap options are selected then all traps will be enabled."""
    display_name = "Curse of Horns"

class CurseOfFlames(Toggle):
    """Accept the curse of flames. Flames appear behind you as you move through dungeons."""
    display_name = "Curse of Flames"

class TrapChance(Range):
    """Percentage chance of an added filler item being a trap. Items in the base pool are not affected. Has no effect if Curse of Horns is active."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 50

class EnableAllTraps(Toggle):
    """Enabling this overrides the individual trap settings and enables all types of traps."""
    display_name = "Enable All Traps"

class SlownessTraps(Toggle):
    """Enable slowness traps, which prevent you from running for 20 seconds."""
    display_name = "Slowness Traps"

class RustTraps(Toggle):
    """Enable rust traps, which disable boots and rings for 20 seconds."""
    display_name = "Rust Traps"

class ConfusionTraps(Toggle):
    """Enable confusion traps, which reverse your movement for 20 seconds."""
    display_name = "Confusion Traps"

class DisarmingTraps(Toggle):
    """Enable disarming traps, which prevent use of the pick for 20 seconds."""
    display_name = "Disarming Traps"

class LightTraps(Toggle):
    """Enable light traps, which attack you with beams of light for 20 seconds."""
    display_name = "Light Traps"

class GlitchTraps(Toggle):
    """Enable glitch traps, which cause graphical glitches for 20 seconds."""
    display_name = "Glitch Traps"

class ZombieTraps(Toggle):
    """Enable zombie traps, which spawn zombies around you."""
    display_name = "Zombie Traps"

class ShadowTraps(Toggle):
    """Enable shadow traps, which warp you as though you used the Dread Hand."""
    display_name = "Shadow Traps"

@dataclass
class ProdigalOptions(PerGameCommonOptions):
    specific_keys: SpecificKeys
    colors_required: ColorsRequired
    blessings_required: BlessingsRequired
    crest_fragments_required: CrestFragmentsRequired
    coins_of_crowl_required: CoinsOfCrowlRequired
    goal: Goal
    color_locations: ColorLocations
    blessing_locations: BlessingLocations
    lighthouse_key: LighthouseKey
    trading_quest: TradingQuest
    shuffle_grelin_drops: ShuffleGrelinDrops
    shuffle_hidden_items: ShuffleHiddenItems
    shuffle_bjerg_castle: ShuffleBjergCastle
    shuffle_daemons_dive: ShuffleDaemonsDive
    shuffle_enlightenment: ShuffleEnlightenment
    shuffle_secret_shop: ShuffleSecretShop
    skips_in_logic: SkipsInLogic
    start_with_spiced_ham: StartWithSpicedHam
    start_with_winged_boots: StartWithWingedBoots
    skip_one_small_favor: SkipOneSmallFavor
    fake_dread_hand: FakeDreadHand
    fast_fishing: FastFishing
    altar_to_var: AltarToVar
    altar_to_zolei: AltarToZolei
    altar_to_raem: AltarToRaem
    altar_to_hate: AltarToHate
    curse_of_frailty: CurseOfFrailty
    curse_of_famine: CurseOfFamine
    curse_of_rust: CurseOfRust
    curse_of_wind: CurseOfWind
    curse_of_blooms: CurseOfBlooms
    curse_of_crowns: CurseOfCrowns
    curse_of_horns: CurseOfHorns
    curse_of_flames: CurseOfFlames
    trap_chance: TrapChance
    enable_all_traps: EnableAllTraps
    slowness_traps: SlownessTraps
    rust_traps: RustTraps
    confusion_traps: ConfusionTraps
    disarming_traps: DisarmingTraps
    light_traps: LightTraps
    glitch_traps: GlitchTraps
    zombie_traps: ZombieTraps
    shadow_traps: ShadowTraps

slot_data_options: List[str] = [
    "specific_keys",
    "colors_required",
    "blessings_required",
    "crest_fragments_required",
    "coins_of_crowl_required",
    "goal",
    "trading_quest",
    "shuffle_grelin_drops",
    "shuffle_hidden_items",
    "shuffle_bjerg_castle",
    "shuffle_daemons_dive",
    "shuffle_enlightenment",
    "shuffle_secret_shop",
    "skips_in_logic",
    "start_with_spiced_ham",
    "start_with_winged_boots",
    "skip_one_small_favor",
    "fake_dread_hand",
    "fast_fishing",
    "altar_to_var",
    "altar_to_zolei",
    "altar_to_raem",
    "altar_to_hate",
    "curse_of_frailty",
    "curse_of_famine",
    "curse_of_rust",
    "curse_of_wind",
    "curse_of_blooms",
    "curse_of_crowns",
    "curse_of_horns",
    "curse_of_flames",
]
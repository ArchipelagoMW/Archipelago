from dataclasses import dataclass
from BaseClasses import PlandoOptions
from Options import Toggle, DefaultOnToggle, Range, Choice, PerGameCommonOptions, DeathLink, ItemSet
from .enums import ItemName, Spelunky2Goal, Spelunky2ShortcutMode
from .Items import (item_options, locked_items, powerup_options, equip_options, quest_items, character_options,
                    hard_locations)


def format_options(options, row_length=10):
    """Formats a list of options into a multi-line string, with each line
    containing 'row_length' options separated by '|'.
    """
    lines = []
    # Convert the options to a list to ensure order
    options_list = list(options)
    for i in range(0, len(options_list), row_length):
        row = " | ".join(options_list[i:i + row_length])
        lines.append(f"- {row}")
    return "\n".join(lines)


def list_to_string(options, row_length=3):
    lines = []
    options_list = list(options)
    for i in range(0, len(options_list), row_length):
        row = " | ".join(options_list[i:i + row_length])
        lines.append(f"{row}")
    return "\n".join(lines)


item_options_text = format_options(sorted(item_options))
locked_items_text = format_options(sorted(locked_items))
character_options_text = format_options(sorted(character_options))
hard_locations_text = list_to_string(sorted(hard_locations))


class Goal(Choice):
    """When is your world considered finished.
    Easy: Requires completing the "normal" ending by reaching 6-4 and defeating Tiamat
    Hard: Requires completing the "hard" ending by reaching 7-4 and defeating Hundun
    CO: Requires reaching a specified level in Cosmic Ocean"""
    display_name = "Goal"
    option_easy = Spelunky2Goal.EASY
    option_hard = Spelunky2Goal.HARD
    option_co = Spelunky2Goal.CO
    default = Spelunky2Goal.EASY


class GoalLevel(Range):
    """Which level in Cosmic Ocean are you required to clear to consider your game as beaten.
    This option can be ignored if your goal is not set to \"CO\""""
    display_name = "Cosmic Ocean Goal Level"
    range_start = 10
    range_end = 99
    default = 30


class GoalIronmanMode(Toggle):
    """Cannot enter goal level unless you started your run from the world start (Not using a shortcut)"""
    display_name = "Ironman Goal mode"

class DeathLinkBypassesAnkh(Toggle):
    """Sets whether deaths sent through Death Link will trigger the Ankh, or ignore it."""
    display_name = "Death Link Ankh Handling"


class DeathLinkAmnesty(Range):
    """A \"grace\" count of how many deaths you are allowed before you send a Deathlink out to the multiworld."""
    display_name = "Death Link Amnesty"
    range_start = 0
    range_end = 10
    default = 2


class DeathLinkGrace(Range):
    """How many deaths you receive before you fall victim to a Deathlink from the multiworld."""
    display_name = "Death Link Grace"
    range_start = 0
    range_end = 10
    default = 2


class IncludeHardLocations(Toggle):
    __doc__ = f"""Include the following more problematic journal entries as locations in the AP world:
{hard_locations_text}"""
    display_name = "Include harder journal entries"


class JournalEntryRequired(DefaultOnToggle):
    """Should the Journal Entry of an item be required for its Item/Waddler upgrade to take effect?"""
    display_name = "Journal Entry Required"


class IncreaseStartingWallet(Toggle):
    """Should treasure (gold/emerald/sapphire/ruby/diamond) you receive from other players
    increase the amount of gold you begin with after death."""
    display_name = "Increase Starting Wallet"


class StartingCharacters(ItemSet):
    __doc__ = f"""Characters that are immediately selectable. Adding more or less to this will adjust how many character locations you need to visit.
Normally unlocked characters (Ana/Margaret/Colin/Roffy) will show up in shopkeeper locked cages if a hired hand would be there -OR- in Vlad's Castle
If you do not specify ANY then Ana will be the only unlocked character
Options: 
{character_options_text}"""  # noqa: E128
    display_name = "Starting Characters"
    valid_keys = character_options
    default = {ItemName.ANA_SPELUNKY.value, ItemName.MARGARET_TUNNEL.value, ItemName.COLIN_NORTHWARD.value,
               ItemName.ROFFY_D_SLOTH.value}


class ProgressiveWorlds(DefaultOnToggle):
    """Progressive worlds are unlocked in order:
    Volcana, Jungle, Olmec's Lair, Tide Pool, Temple, Ice Caves, Neo Babylon, Sunken City, Cosmic Ocean.
    Set this to 'false' to unlock worlds individually."""
    display_name = "Progressive Worlds"


class ShortcutsMode(Choice):
    """Should shortcuts unlock as you gain worlds, or instead receive them from the multiworld
    (You still the associated world for the shortcut to be open when you receive it from the multiworld)"""
    display_name = "Shortcut Mode"
    option_off = Spelunky2ShortcutMode.OFF
    option_progressive = Spelunky2ShortcutMode.PROGRESSIVE
    option_individual = Spelunky2ShortcutMode.INDIVIDUAL
    default = Spelunky2ShortcutMode.OFF


class StartingHealth(Range):
    """How much Health should you initially start with."""
    display_name = "Starting Health"
    range_start = 1
    range_end = 10
    default = 4


class HealthUpgrades(Range):
    """Increases how much health you will begin with after death."""
    display_name = "Progressive Health"
    range_start = 0
    range_end = 30
    default = 10


class StartingBombs(Range):
    """How many Bombs should you initially start with."""
    display_name = "Starting Bombs"
    range_start = 0
    range_end = 10
    default = 4


class BombUpgrades(Range):
    """Increases how many bombs you will begin with after death."""
    display_name = "Starting Bombs Upgrades"
    range_start = 0
    range_end = 30
    default = 5


class StartingRopes(Range):
    """How many Ropes should you initially start with."""
    display_name = "Starting Ropes"
    range_start = 0
    range_end = 10
    default = 4


class RopeUpgrades(Range):
    """Increases how many ropes you will begin with after death."""
    display_name = "Starting Rope Upgrades"
    range_start = 0
    range_end = 20
    default = 0


class RestrictedItems(ItemSet):
    __doc__ = f"""Items that must be unlocked in the multi-world before they appear in the game.
(Quest items like Hou Yi's Bow will be ignored if it's not suitable for your goal)
Options ("ALL" can be used for everything): 
{locked_items_text}"""  # noqa: E128
    display_name = "Restricted Items"
    valid_keys = locked_items + ["ALL"]
    default = quest_items

    def verify(self, world: type["World"], player_name: str, plando_options: PlandoOptions):
        lowered = [item.lower() for item in self.value]
        if "all" in lowered:
            return
        super().verify(world, player_name, plando_options)


class ItemUpgrades(ItemSet):
    __doc__ = f"""Add the following useful items in the multi-world item pool which are kept on death,
AFTER obtaining it's journal entry if 'Journal Entry Required' is true.
Options: 
{item_options_text}"""  # noqa: E128
    display_name = "Item Upgrades"
    valid_keys = sorted(set(item_options) | {ItemName.ALIEN_COMPASS.value})
    default = powerup_options - {ItemName.TRUE_CROWN.value, ItemName.EGGPLANT_CROWN.value, ItemName.PITCHERS_MITT.value}


class WaddlerUpgrades(ItemSet):
    __doc__ = f"""Add the following useful items in the multi-world item pool which are added to Waddler's storage between runs, 
AFTER obtaining it's journal entry if 'Journal Entry Required' is true.
Options (any selected here override options in item_upgrades):
{locked_items_text}"""  # noqa: E128
    display_name = "Waddler Items"
    valid_keys = locked_items
    default = equip_options - {ItemName.TRUE_CROWN.value, ItemName.EGGPLANT_CROWN.value,
                               ItemName.PASTE.value, ItemName.SHIELD.value}


class AnkhSkipLogic(Toggle):
    """Sets if progression logic should assume you can perform Ankh skipping in Tidepool"""


class UdjatSkipLogic(Toggle):
    """Sets if progression logic should assume you can perform Udjat skipping to get into Black Market/Vlad's Castle"""


class QilinSkipLogic(Toggle):
    """Sets if progression logic should assume you can perform Qilin skip"""


class KinguExcaliburSkipLogic(Toggle):
    """Sets if progression should assume you can kill Kingu without needing Excalibur to break the shell"""


class AlienCompassSkipLogic(Toggle):
    """Sets if progression should assume you know how to find the Mothership without Alien Compass"""


class RopePileWeight(Range):
    """Sets the likelihood of a filler item being a Rope Pile relative to others."""
    display_name = "Rope Pile Weight"
    range_start = 0
    range_end = 100
    default = 13


class BombBagWeight(Range):
    """Sets the likelihood of a filler item being a Bomb Bag relative to others."""
    display_name = "Bomb Bag Weight"
    range_start = 0
    range_end = 100
    default = 13


class BombBoxWeight(Range):
    """Sets the likelihood of a filler item being a Bomb Box relative to others."""
    display_name = "Bomb Box Weight"
    range_start = 0
    range_end = 100
    default = 5


class CookedTurkeyWeight(Range):
    """Sets the likelihood of a filler item being a Cooked Turkey relative to others."""
    display_name = "Cooked Turkey Weight"
    range_start = 0
    range_end = 100
    default = 18


class RoyalJellyWeight(Range):
    """Sets the likelihood of a filler item being a Royal Jelly relative to others."""
    display_name = "Royal Jelly Weight"
    range_start = 0
    range_end = 100
    default = 5


class GoldBarWeight(Range):
    """Sets the likelihood of a filler item being a Gold Bar relative to others."""
    display_name = "Gold Bar Weight"
    range_start = 0
    range_end = 100
    default = 20


class EmeraldGemWeight(Range):
    """Sets the likelihood of a filler item being an Emerald relative to others."""
    display_name = "Emerald Gem Weight"
    range_start = 0
    range_end = 100
    default = 10


class SapphireGemWeight(Range):
    """Sets the likelihood of a filler item being a Sapphire relative to others."""
    display_name = "Sapphire Gem Weight"
    range_start = 0
    range_end = 100
    default = 8


class RubyGemWeight(Range):
    """Sets the likelihood of a filler item being a Ruby relative to others."""
    display_name = "Ruby Gem Weight"
    range_start = 0
    range_end = 100
    default = 6


class DiamondGemWeight(Range):
    """Sets the likelihood of a filler item being a Diamond relative to others."""
    display_name = "Diamond Gem Weight"
    range_start = 0
    range_end = 100
    default = 2


class EnableTraps(Toggle):
    """Whether traps should be included in the item pool."""
    display_name = "Enable Traps"


class TrapWeight(Range):
    """Determines the percentage of filler items that will be replaced by traps."""
    display_name = "Trap Percentage"
    range_start = 5
    range_end = 30
    default = 15


class PoisonTrapChance(Range):
    """Sets the likelihood of a trap being a Poison Trap relative to other traps.
    Poison Traps will instantly poison the player."""
    display_name = "Poison Trap Weight"
    range_start = 0
    range_end = 100
    default = 15


class CurseTrapChance(Range):
    """Sets the likelihood of a trap being a Curse Trap relative to other traps.
    Curse Traps will instantly curse the player."""
    display_name = "Curse Trap Weight"
    range_start = 0
    range_end = 100
    default = 5


class GhostTrapChance(Range):
    """Sets the likelihood of a trap being a Ghost Trap relative to other traps.
    Ghost Traps will immediately spawn the ghost (or Jelly if in Cosmic Ocean)."""
    display_name = "Ghost Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


class StunTrapChance(Range):
    """Sets the likelihood of a trap being a Stun Trap relative to other traps.
    Stun Traps wll stun the player for 1 second."""
    display_name = "Stun Trap Weight"
    range_start = 0
    range_end = 100
    default = 25


class LooseBombsTrapChance(Range):
    """Sets the likelihood of a trap being a Loose Bombs Trap relative to other traps.
    Loose Bombs Traps will spawn 1 lit bomb at the player's feet every second for 5 seconds."""
    display_name = "Loose Bombs Trap Weight"
    range_start = 0
    range_end = 100
    default = 15


class BlindnessTrapChance(Range):
    """Sets the likelihood of a trap being a Blindness Trap relative to other traps.
    Blindness traps will trigger a darkness effect similar to the \"I can't see a thing!\" level
    feeling for the current level."""
    display_name = "Blindness Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


class PunishBallTrapChance(Range):
    """Sets the likelihood of a trap being a Punish Ball Trap relative to other traps.
    Punish Ball Traps will attach a ball and chain to the player for 3 levels."""
    display_name = "Punish Ball Trap Weight"
    range_start = 0
    range_end = 100
    default = 10


@dataclass
class Spelunky2Options(PerGameCommonOptions):
    goal: Goal
    goal_level: GoalLevel
    goal_ironman: GoalIronmanMode
    death_link: DeathLink
    bypass_ankh: DeathLinkBypassesAnkh
    death_link_amnesty_count: DeathLinkAmnesty
    death_link_grace_count: DeathLinkGrace
    include_hard_locations: IncludeHardLocations
    journal_entry_required: JournalEntryRequired
    starting_wallet: IncreaseStartingWallet
    starting_characters: StartingCharacters
    progressive_worlds: ProgressiveWorlds
    shortcut_mode: ShortcutsMode
    starting_health: StartingHealth
    health_upgrades: HealthUpgrades
    starting_bombs: StartingBombs
    bomb_upgrades: BombUpgrades
    starting_ropes: StartingRopes
    rope_upgrades: RopeUpgrades
    restricted_items: RestrictedItems
    item_upgrades: ItemUpgrades
    waddler_upgrades: WaddlerUpgrades
    can_ankh_skip: AnkhSkipLogic
    can_udjat_skip: UdjatSkipLogic
    can_qilin_skip: QilinSkipLogic
    can_kingu_skip: KinguExcaliburSkipLogic
    can_mothership_skip: AlienCompassSkipLogic
    rope_pile_weight: RopePileWeight
    bomb_bag_weight: BombBagWeight
    bomb_box_weight: BombBoxWeight
    cooked_turkey_weight: CookedTurkeyWeight
    royal_jelly_weight: RoyalJellyWeight
    gold_bar_weight: GoldBarWeight
    emerald_gem_weight: EmeraldGemWeight
    sapphire_gem_weight: SapphireGemWeight
    ruby_gem_weight: RubyGemWeight
    diamond_gem_weight: DiamondGemWeight
    enable_traps: EnableTraps
    trap_weight: TrapWeight
    poison_weight: PoisonTrapChance
    curse_weight: CurseTrapChance
    ghost_weight: GhostTrapChance
    stun_weight: StunTrapChance
    bomb_weight: LooseBombsTrapChance
    blind_weight: BlindnessTrapChance
    punish_weight: PunishBallTrapChance

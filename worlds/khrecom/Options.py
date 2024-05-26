from dataclasses import dataclass

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet, PerGameCommonOptions

class EarlyCure(DefaultOnToggle):
    """
    Toggle whether one of the starting checks should include Cure
    """
    display_name = "Early Cure"

class AttackPower(Range):
    """
    Modifier for Sora's strike power.  Default is 10
    """
    display_name = "Attack Power"
    range_start = 1
    range_end = 100
    default = 10

class DaysLocations(DefaultOnToggle):
    """
    Toggle whether locations not available to the player until they watch 358/2 Days are included in the locations list.
    """
    display_name = "Days Locations"

class StartingWorlds(Toggle):
    """
    Toggle whether 3 world cards are guaranteed as part of your starting checks.
    """
    display_name = "Starting Worlds"

class ChecksBehindLeon(Toggle):
    """
    Toggle whether to include checks behind the Leon sleight tutorial.  If left off, the player can safely skip that room.
    """
    display_name = "Checks Behind Leon"

class ChecksBehindMinigames(Toggle):
    """
    Toggle whether to include checks behind 100 Acre Woods Minigames.
    """
    display_name = "Checks Behind Minigames"

class ChecksBehindSleightsLevels(Toggle):
    """
    Toggle whether to include checks behind Sleights received from Leveling Up.
    """
    display_name = "Checks Behind Level Up Sleights"

class EXPMultiplier(Range):
    """
    Multiplier to apply to XP received.
    """
    display_name = "EXP Multiplier"
    range_start = 1
    range_end = 10
    default = 1

class Value0On(Range):
    """
    Determines which consecutive card set 0 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "0 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value1On(Range):
    """
    Determines which consecutive card set 1 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "1 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1
    
class Value2On(Range):
    """
    Determines which consecutive card set 2 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "2 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value3On(Range):
    """
    Determines which consecutive card set 3 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "3 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value4On(Range):
    """
    Determines which consecutive card set 4 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "4 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value5On(Range):
    """
    Determines which consecutive card set 5 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "5 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value6On(Range):
    """
    Determines which consecutive card set 6 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "6 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value7On(Range):
    """
    Determines which consecutive card set 7 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "7 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value8On(Range):
    """
    Determines which consecutive card set 8 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "8 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value9On(Range):
    """
    Determines which consecutive card set 9 value cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "9 Value Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 1

class Value0POn(Range):
    """
    Determines which consecutive card set 0 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "0 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class Value1POn(Range):
    """
    Determines which consecutive card set 1 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "1 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0
    
class Value2POn(Range):
    """
    Determines which consecutive card set 2 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "2 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class Value3POn(Range):
    """
    Determines which consecutive card set 3 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "3 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class Value4POn(Range):
    """
    Determines which consecutive card set 4 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "4 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class Value5POn(Range):
    """
    Determines which consecutive card set 5 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "5 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class Value6POn(Range):
    """
    Determines which consecutive card set 6 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "6 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class Value7POn(Range):
    """
    Determines which consecutive card set 7 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "7 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class Value8POn(Range):
    """
    Determines which consecutive card set 8 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "8 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class Value9POn(Range):
    """
    Determines which consecutive card set 9 value premium cards are found on.  Set to 0 if you would like it be impossible to receive this value.
    """
    display_name = "9 Value Premium Cards on Card Set Number"
    range_start = 0
    range_end = 20
    default = 0

class EnemyCardAmount(Range):
    """
    Determines the number of enemy cards shuffled into the pool.  There are 57 unique enemy cards in the game.
    If this value is less than 57, the enemy cards chosen to be shuffled in will be random."""
    display_name = "Enemy Cards Shuffled In"
    range_start = 0
    range_end = 57
    default = 57

class SleightAmount(Range):
    """
    Determines the number of sleights shuffled into the pool.  There are 83 unique sleights in the game.
    If this value is less than 83, the sleights chosen to be shuffled in will be random."""
    display_name = "Sleights Shuffled In"
    range_start = 0
    range_end = 83
    default = 83

class ExcludeCards(OptionSet):
    """
    Determines which attack, magic, item, or summon cards are to be exluded from the pool, if any.
    """
    display_name = "Excluded Cards"
    valid_keys = ["Three Wishes", "Crabclaw", "Pumpkinhead", "Fairy Harp", "Wishing Star", "Spellbinder", "Metal Chocobo", "Olympia", "Lionheart", "Lady Luck",
        "Divine Rose", "Oathkeeper", "Oblivion", "Ultima Weapon", "Diamond Dust", "One Winged Angel", "Soul Eater", "Star Seeker", "Total Eclipse", "Midnight Roar",
        "Maverick Flare", "Two Become One", "Bond of Flame", "Fire", "Blizzard", "Thunder", "Cure", "Gravity", "Stop", "Aero", "Simba", "Genie", "Bambi", "Dumbo",
        "Tinker Bell", "Mushu", "Cloud", "Potion", "Hi-Potion", "Mega-Potion", "Ether", "Mega-Ether", "Elixir", "Megalixir"]
    default = ["Ultima Weapon", "Diamond Dust", "One Winged Angel", "Soul Eater", "Star Seeker", "Total Eclipse", "Midnight Roar", "Maverick Flare", "Two Become One", "Bond of Flame"]

class ExcludeEnemyCards(OptionSet):
    """
    Determines which enemy cards should be excluded from the pool, if any.
    """
    display_name = "Excluded Enemy Cards"
    valid_keys = ["Shadow", "Soldier", "Large Body", "Red Nocturne", "Blue Rhapsody", "Yellow Opera", "Green Requiem", "Powerwild", "Bouncywild", "Air Soldier", "Bandit",
        "Fat Bandit", "Barrel Spider", "Search Ghost", "Sea Neon", "Screwdiver", "Aquatank", "Wight Knight", "Gargoyle", "Pirate", "Air Pirate", "Darkball", "Defender",
        "Wyvern", "Wizard", "Neoshadow", "White Mushroom", "Black Fungus", "Creeper Plant", "Tornado Step", "Crescendo", "Guard Armor", "Parasite Cage", "Trickmaster",
        "Darkside", "Card Soldier", "Hades", "Jafar", "Oogie Boogie", "Ursula", "Hook", "Dragon Maleficent", "Riku", "Axel", "Larxene", "Vexen", "Marluxia", "Lexaeus",
        "Ansem", "Zexion", "Xemnas", "Xigbar", "Xaldin", "Saix", "Demyx", "Luxord", "Roxas"]
    default = ["Lexaeus", "Ansem", "Zexion", "Xemnas", "Xigbar", "Xaldin", "Saix", "Demyx", "Luxord", "Roxas"]

class ExcludeSleights(OptionSet):
    """
    Detmerines which sleights should be excluded from the pool, if any.
    """
    display_name = "Exclude Sleights"
    valid_keys = ["Sliding Dash", "Blitz", "Stun Impact", "Zantetsuken", "Strike Raid", "Sonic Blade", "Ars Arcanum", "Ragnarok", "Trinity Limit", "Fira", "Blizzara",
        "Thundara", "Cura", "Gravira", "Stopra", "Aerora", "Firaga", "Blizzaga", "Thundaga", "Curaga", "Graviga", "Stopga", "Aeroga", "Fire Raid", "Blizzard Raid",
        "Thunder Raid", "Reflect Raid", "Judgement", "Firaga Burst", "Raging Storm", "Mega Flare", "Freeze", "Homing Blizzara", "Aqua Splash", "Magnet Spiral",
        "Lethal Frame", "Shock Impact", "Tornado", "Quake", "Warpinator", "Warp", "Bind", "Confuse", "Terror", "Synchro", "Gifted Miracle", "Teleport", "Holy",
        "Proud Roar LV2", "Proud Roar LV3", "Splash LV2", "Splash LV3", "Paradise LV2", "Paradise LV3", "Idyll Romp", "Flare Breath LV2", "Flare Breath LV3",
        "Showtime LV2", "Showtime LV3", "Twinkle LV2", "Twinkle LV3", "Cross-slash", "Omnislash", "Cross-slash+", "Magic LV2", "Magic LV3", "Stardust Blitz",
        "Goofy Tornado LV2", "Goofy Tornado LV3", "Goofy Smash", "Wild Crush", "Sandstorm LV2", "Sandstorm LV3", "Surprise! LV2", "Surprise! LV3", "Spiral Wave LV2",
        "Spiral Wave LV3", "Hummingbird LV2", "Hummingbird LV3", "Furious Volley LV2", "Furious Volley LV3", "Lucky Bounty LV2", "Lucky Bounty LV3"]
    default = []

@dataclass
class KHRECOMOptions(PerGameCommonOptions):
    early_cure: EarlyCure
    days_locations: DaysLocations
    checks_behind_leon: ChecksBehindLeon
    exp_multiplier: EXPMultiplier
    minigames: ChecksBehindMinigames
    levels: ChecksBehindSleightsLevels
    attack_power: AttackPower
    starting_worlds: StartingWorlds
    enemy_card_amount: EnemyCardAmount
    sleight_amount: SleightAmount
    value_0_on: Value0On
    value_1_on: Value1On
    value_2_on: Value2On
    value_3_on: Value3On
    value_4_on: Value4On
    value_5_on: Value5On
    value_6_on: Value6On
    value_7_on: Value7On
    value_8_on: Value8On
    value_9_on: Value9On
    value_0_p_on: Value0POn
    value_1_p_on: Value1POn
    value_2_p_on: Value2POn
    value_3_p_on: Value3POn
    value_4_p_on: Value4POn
    value_5_p_on: Value5POn
    value_6_p_on: Value6POn
    value_7_p_on: Value7POn
    value_8_p_on: Value8POn
    value_9_p_on: Value9POn
    exclude_cards: ExcludeCards
    exclude_enemy_cards: ExcludeEnemyCards
    exclude_sleights: ExcludeSleights
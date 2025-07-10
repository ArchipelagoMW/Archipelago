from BaseClasses import LocationProgressType
from .Items import OOTItem

#   Abbreviations
#       DMC     Death Mountain Crater
#       DMT     Death Mountain Trail
#       GC      Goron City
#       GF      Gerudo's Fortress
#       GS      Gold Skulltula
#       GV      Gerudo Valley
#       HC      Hyrule Castle
#       HF      Hyrule Field
#       KF      Kokiri Forest
#       LH      Lake Hylia
#       LLR     Lon Lon Ranch
#       LW      Lost Woods
#       OGC     Outside Ganon's Castle
#       SFM     Sacred Forest Meadow
#       TH      Thieves' Hideout
#       ZD      Zora's Domain
#       ZF      Zora's Fountain
#       ZR      Zora's River

class Hint(object):
    name = ""
    text = ""
    type = []

    def __init__(self, name, text, type, rand, choice=None):
        self.name = name
        self.type = [type] if not isinstance(type, list) else type

        if isinstance(text, str):
            self.text = text
        else:
            if choice == None:
                self.text = rand.choice(text)
            else:
                self.text = text[choice]


def getHint(item, rand, clearer_hint=False):
    if item in hintTable:
        textOptions, clearText, hintType = hintTable[item]
        if clearer_hint:
            if clearText == None:
                return Hint(item, textOptions, hintType, rand, 0)
            return Hint(item, clearText, hintType, rand)
        else:
            return Hint(item, textOptions, hintType, rand)
    elif isinstance(item, str):
        return Hint(item, item, 'generic', rand)
    else: # is an Item
        return Hint(item.name, item.hint_text, 'item', rand)


def getHintGroup(group, world):
    ret = []
    for name in hintTable:

        hint = getHint(name, world.random, world.clearer_hints)

        if hint.name in world.always_hints and group == 'always':
            hint.type = 'always'

        # Hint inclusion override from distribution
        if group in world.added_hint_types or group in world.item_added_hint_types:
            if hint.name in world.added_hint_types[group]:
                hint.type = group
            if nameIsLocation(name, hint.type, world):
                location = world.get_location(name)
                for i in world.item_added_hint_types[group]:
                    if i == location.item.name:
                        hint.type = group
                for i in world.item_hint_type_overrides[group]:
                    if i == location.item.name:
                        hint.type = []
        type_override = False
        if group in world.hint_type_overrides:
            if name in world.hint_type_overrides[group]:
                type_override = True
        if group in world.item_hint_type_overrides:
            if nameIsLocation(name, hint.type, world):
                location = world.get_location(name)
                if location.item.name in world.item_hint_type_overrides[group]:
                    type_override = True

        if group in hint.type and (name not in hintExclusions(world)) and not type_override:
            ret.append(hint)
    return ret


def getRequiredHints(world):
    ret = []
    for name in hintTable:
        hint = getHint(name, world.random)
        if 'always' in hint.type or hint.name in conditional_always and conditional_always[hint.name](world):
            ret.append(hint)
    return ret


# Helpers for conditional always hints
def stones_required_by_settings(world):
    stones = 0
    if world.bridge == 'stones':
        stones = max(stones, world.bridge_stones)
    if world.shuffle_ganon_bosskey == 'on_lacs' and world.lacs_condition == 'stones':
        stones = max(stones, world.lacs_stones)
    if world.bridge == 'dungeons':
        stones = max(stones, world.bridge_rewards - 6)
    if world.shuffle_ganon_bosskey == 'on_lacs' and world.lacs_condition == 'dungeons':
        stones = max(stones, world.lacs_rewards - 6)

    return stones


def medallions_required_by_settings(world):
    medallions = 0
    if world.bridge == 'medallions':
        medallions = max(medallions, world.bridge_medallions)
    if world.shuffle_ganon_bosskey == 'on_lacs' and world.lacs_condition == 'medallions':
        medallions = max(medallions, world.lacs_medallions)
    if world.bridge == 'dungeons':
        medallions = max(medallions, max(world.bridge_rewards - 3, 0))
    if world.shuffle_ganon_bosskey == 'on_lacs' and world.lacs_condition == 'dungeons':
        medallions = max(medallions, max(world.lacs_rewards - 3, 0))

    return medallions


def tokens_required_by_settings(world):
    tokens = 0
    if world.bridge == 'tokens':
        tokens = max(tokens, world.bridge_tokens)
    if world.shuffle_ganon_bosskey == 'on_lacs' and world.lacs_condition == 'tokens':
        tokens = max(tokens, world.lacs_tokens)

    return tokens


# Hints required under certain settings
conditional_always = {
    'Market 10 Big Poes':           lambda world: world.big_poe_count > 3,
    'Deku Theater Mask of Truth':   lambda world: not world.complete_mask_quest,
    'Song from Ocarina of Time':    lambda world: stones_required_by_settings(world) < 2,
    'HF Ocarina of Time Item':      lambda world: stones_required_by_settings(world) < 2,
    'Sheik in Kakariko':            lambda world: medallions_required_by_settings(world) < 5,
    'DMT Biggoron':                 lambda world: world.adult_trade_start != {'Claim Check'},
    'Kak 30 Gold Skulltula Reward': lambda world: tokens_required_by_settings(world) < 30 and '30_skulltulas' not in world.misc_hints,
    'Kak 40 Gold Skulltula Reward': lambda world: tokens_required_by_settings(world) < 40 and '40_skulltulas' not in world.misc_hints,
    'Kak 50 Gold Skulltula Reward': lambda world: tokens_required_by_settings(world) < 50 and '50_skulltulas' not in world.misc_hints,
}

# Entrance hints required under certain settings
conditional_entrance_always = {
    'Ganons Castle Grounds -> Ganons Castle Lobby': lambda world: (world.bridge != 'open'
        and (world.bridge != 'stones' or world.bridge_stones > 1)
        and (world.bridge != 'medallions' or world.bridge_medallions > 1)
        and (world.bridge != 'dungeons' or world.bridge_rewards > 2)
        and (world.bridge != 'tokens' or world.bridge_tokens > 20)
        and (world.bridge != 'hearts' or world.bridge_hearts > world.starting_hearts + 1)),
}


# table of hints, format is (name, hint text, clear hint text, type of hint) there are special characters that are read for certain in game commands:
# ^ is a box break
# & is a new line
# @ will print the player name
# # sets color to white (currently only used for dungeon reward hints).
hintTable = {
    'Kokiri Emerald':                                           (["a tree's farewell", "the Spiritual Stone of the Forest"], "the Kokiri Emerald", 'item'),
    'Goron Ruby':                                               (["the Gorons' hidden treasure", "the Spiritual Stone of Fire"], "the Goron Ruby", 'item'),
    'Zora Sapphire':                                            (["an engagement ring", "the Spiritual Stone of Water"], "the Zora Sapphire", 'item'),
    'Light Medallion':                                          (["Rauru's sagely power", "a yellow disc"], "the Light Medallion", 'item'),
    'Forest Medallion':                                         (["Saria's sagely power", "a green disc"], "the Forest Medallion", 'item'),
    'Fire Medallion':                                           (["Darunia's sagely power", "a red disc"], "the Fire Medallion", 'item'),
    'Water Medallion':                                          (["Ruto's sagely power", "a blue disc"], "the Water Medallion", 'item'),
    'Shadow Medallion':                                         (["Impa's sagely power", "a purple disc"], "the Shadow Medallion", 'item'),
    'Spirit Medallion':                                         (["Nabooru's sagely power", "an orange disc"], "the Spirit Medallion", 'item'),
    'Triforce Piece':                                           (["a triumph fork", "cheese", "a gold fragment"], "a Piece of the Triforce", 'item'),
    'Magic Meter':                                              (["mystic training", "pixie dust", "a green rectangle"], "a Magic Meter", 'item'),
    'Double Defense':                                           (["a white outline", "damage decrease", "strengthened love"], "Double Defense", 'item'),
    'Slingshot':                                                (["a seed shooter", "a rubberband", "a child's catapult"], "a Slingshot", 'item'),
    'Boomerang':                                                (["a banana", "a stun stick"], "the Boomerang", 'item'),
    'Bow':                                                      (["an archery enabler", "a danger dart launcher"], "a Bow", 'item'),
    'Bomb Bag':                                                 (["an explosive container", "a blast bag"], "a Bomb Bag", 'item'),
    'Progressive Hookshot':                                     (["Dampé's keepsake", "the Grapple Beam", "the BOING! chain"], "a Hookshot", 'item'),
    'Progressive Strength Upgrade':                             (["power gloves", "metal mittens", "the heavy lifty"], "a Strength Upgrade", 'item'),
    'Progressive Scale':                                        (["a deeper dive", "a piece of Zora"], "a Zora Scale", 'item'),
    'Megaton Hammer':                                           (["the dragon smasher", "the metal mallet", "the heavy hitter"], "the Megaton Hammer", 'item'),
    'Iron Boots':                                               (["sink shoes", "clank cleats"], "the Iron Boots", 'item'),
    'Hover Boots':                                              (["butter boots", "sacred slippers", "spacewalkers"], "the Hover Boots", 'item'),
    'Kokiri Sword':                                             (["a butter knife", "a starter slasher", "a switchblade"], "the Kokiri Sword", 'item'),
    'Giants Knife':                                             (["a fragile blade", "a breakable cleaver"], "the Giant's Knife", 'item'),
    'Biggoron Sword':                                           (["the biggest blade", "a colossal cleaver"], "the Biggoron Sword", 'item'),
    'Master Sword':                                             (["evil's bane"], "the Master Sword", 'item'),
    'Deku Shield':                                              (["a wooden ward", "a burnable barrier"], "a Deku Shield", 'item'),
    'Hylian Shield':                                            (["a steel safeguard", "Like Like's metal meal"], "a Hylian Shield", 'item'),
    'Mirror Shield':                                            (["the reflective rampart", "Medusa's weakness", "a silvered surface"], "the Mirror Shield", 'item'),
    'Farores Wind':                                             (["teleportation", "a relocation rune", "a green ball", "a green gust"], "Farore's Wind", 'item'),
    'Nayrus Love':                                              (["a safe space", "an impregnable aura", "a blue barrier", "a blue crystal"], "Nayru's Love", 'item'),
    'Dins Fire':                                                (["an inferno", "a heat wave", "a red ball"], "Din's Fire", 'item'),
    'Fire Arrows':                                              (["the furnace firearm", "the burning bolts", "a magma missile"], "the Fire Arrows", 'item'),
    'Ice Arrows':                                               (["the refrigerator rocket", "the frostbite bolts", "an iceberg maker"], "the Ice Arrows", 'item'),
    'Light Arrows':                                             (["the shining shot", "the luminous launcher", "Ganondorf's bane", "the lighting bolts"], "the Light Arrows", 'item'),
    'Lens of Truth':                                            (["a lie detector", "a ghost tracker", "true sight", "a detective's tool"], "the Lens of Truth", 'item'),
    'Ocarina':                                                  (["a flute", "a music maker"], "an Ocarina", 'item'),
    'Goron Tunic':                                              (["ruby robes", "fireproof fabric", "cooking clothes"], "a Goron Tunic", 'item'),
    'Zora Tunic':                                               (["a sapphire suit", "scuba gear", "a swimsuit"], "a Zora Tunic", 'item'),
    'Epona':                                                    (["a horse", "a four legged friend"], "Epona", 'item'),
    'Zeldas Lullaby':                                           (["a song of royal slumber", "a triforce tune"], "Zelda's Lullaby", 'item'),
    'Eponas Song':                                              (["an equestrian etude", "Malon's melody", "a ranch song"], "Epona's Song", 'item'),
    'Sarias Song':                                              (["a song of dancing Gorons", "Saria's phone number"], "Saria's Song", 'item'),
    'Suns Song':                                                (["Sunny Day", "the ReDead's bane", "the Gibdo's bane"], "the Sun's Song", 'item'),
    'Song of Time':                                             (["a song 7 years long", "the tune of ages"], "the Song of Time", 'item'),
    'Song of Storms':                                           (["Rain Dance", "a thunderstorm tune", "windmill acceleration"], "the Song of Storms", 'item'),
    'Minuet of Forest':                                         (["the song of tall trees", "an arboreal anthem", "a green spark trail"], "the Minuet of Forest", 'item'),
    'Bolero of Fire':                                           (["a song of lethal lava", "a red spark trail", "a volcanic verse"], "the Bolero of Fire", 'item'),
    'Serenade of Water':                                        (["a song of a damp ditch", "a blue spark trail", "the lake's lyric"], "the Serenade of Water", 'item'),
    'Requiem of Spirit':                                        (["a song of sandy statues", "an orange spark trail", "the desert ditty"], "the Requiem of Spirit", 'item'),
    'Nocturne of Shadow':                                       (["a song of spooky spirits", "a graveyard boogie", "a haunted hymn", "a purple spark trail"], "the Nocturne of Shadow", 'item'),
    'Prelude of Light':                                         (["a luminous prologue melody", "a yellow spark trail", "the temple traveler"], "the Prelude of Light", 'item'),
    'Bottle':                                                   (["a glass container", "an empty jar", "encased air"], "a Bottle", 'item'),
    'Rutos Letter':                                             (["a call for help", "the note that Mweeps", "an SOS call", "a fishy stationery"], "Ruto's Letter", 'item'),
    'Bottle with Milk':                                         (["cow juice", "a white liquid", "a baby's breakfast"], "a Milk Bottle", 'item'),
    'Bottle with Red Potion':                                   (["a vitality vial", "a red liquid"], "a Red Potion Bottle", 'item'),
    'Bottle with Green Potion':                                 (["a magic mixture", "a green liquid"], "a Green Potion Bottle", 'item'),
    'Bottle with Blue Potion':                                  (["an ailment antidote", "a blue liquid"], "a Blue Potion Bottle", 'item'),
    'Bottle with Fairy':                                        (["an imprisoned fairy", "an extra life", "Navi's cousin"], "a Fairy Bottle", 'item'),
    'Bottle with Fish':                                         (["an aquarium", "a deity's snack"], "a Fish Bottle", 'item'),
    'Bottle with Blue Fire':                                    (["a conflagration canteen", "an icemelt jar"], "a Blue Fire Bottle", 'item'),
    'Bottle with Bugs':                                         (["an insectarium", "Skulltula finders"], "a Bug Bottle", 'item'),
    'Bottle with Poe':                                          (["a spooky ghost", "a face in the jar"], "a Poe Bottle", 'item'),
    'Bottle with Big Poe':                                      (["the spookiest ghost", "a sidequest spirit"], "a Big Poe Bottle", 'item'),
    'Stone of Agony':                                           (["the shake stone", "the Rumble Pak (TM)"], "the Stone of Agony", 'item'),
    'Gerudo Membership Card':                                   (["a girl club membership", "a desert tribe's pass"], "the Gerudo Card", 'item'),
    'Progressive Wallet':                                       (["a mo' money holder", "a gem purse", "a portable bank"], "a Wallet", 'item'),
    'Deku Stick Capacity':                                      (["a lumber rack", "more flammable twigs"], "Deku Stick Capacity", 'item'),
    'Deku Nut Capacity':                                        (["more nuts", "flashbang storage"], "Deku Nut Capacity", 'item'),
    'Heart Container':                                          (["a lot of love", "a Valentine's gift", "a boss's organ"], "a Heart Container", 'item'),
    'Piece of Heart':                                           (["a little love", "a broken heart"], "a Piece of Heart", 'item'),
    'Piece of Heart (Treasure Chest Game)':                     ("a victory valentine", "a Piece of Heart", 'item'),
    'Recovery Heart':                                           (["a free heal", "a hearty meal", "a Band-Aid"], "a Recovery Heart", 'item'),
    'Rupee (Treasure Chest Game)':                              ("the dollar of defeat", 'a Green Rupee', 'item'),
    'Deku Stick (1)':                                           ("a breakable branch", 'a Deku Stick', 'item'),
    'Rupee (1)':                                                (["a unique coin", "a penny", "a green gem"], "a Green Rupee", 'item'),
    'Rupees (5)':                                               (["a common coin", "a blue gem"], "a Blue Rupee", 'item'),
    'Rupees (20)':                                              (["couch cash", "a red gem"], "a Red Rupee", 'item'),
    'Rupees (50)':                                              (["big bucks", "a purple gem", "wealth"], "a Purple Rupee", 'item'),
    'Rupees (200)':                                             (["a juicy jackpot", "a yellow gem", "a giant gem", "great wealth"], "a Huge Rupee", 'item'),
    'Weird Egg':                                                (["a chicken dilemma"], "the Weird Egg", 'item'),
    'Zeldas Letter':                                            (["an autograph", "royal stationery", "royal snail mail"], "Zelda's Letter", 'item'),
    'Pocket Egg':                                               (["a Cucco container", "a Cucco, eventually", "a fowl youth"], "the Pocket Egg", 'item'),
    'Pocket Cucco':                                             (["a little clucker"], "the Pocket Cucco", 'item'),
    'Cojiro':                                                   (["a cerulean capon"], "Cojiro", 'item'),
    'Odd Mushroom':                                             (["a powder ingredient"], "an Odd Mushroom", 'item'),
    'Odd Potion':                                               (["Granny's goodies"], "an Odd Potion", 'item'),
    'Poachers Saw':                                             (["a tree killer"], "the Poacher's Saw", 'item'),
    'Broken Sword':                                             (["a shattered slicer"], "the Broken Sword", 'item'),
    'Prescription':                                             (["a pill pamphlet", "a doctor's note"], "the Prescription", 'item'),
    'Eyeball Frog':                                             (["a perceiving polliwog"], "the Eyeball Frog", 'item'),
    'Eyedrops':                                                 (["a vision vial"], "the Eyedrops", 'item'),
    'Claim Check':                                              (["a three day wait"], "the Claim Check", 'item'),
    'Map':                                                      (["a dungeon atlas", "blueprints"], "a Map", 'item'),
    'Map (Deku Tree)':                                          (["an atlas of an ancient tree", "blueprints of an ancient tree"], "a Map of the Deku Tree", 'item'),
    'Map (Dodongos Cavern)':                                    (["an atlas of an immense cavern", "blueprints of an immense cavern"], "a Map of Dodongo's Cavern", 'item'),
    'Map (Jabu Jabus Belly)':                                   (["an atlas of the belly of a deity", "blueprints of the belly of a deity"], "a Map of Jabu Jabu's Belly", 'item'),
    'Map (Forest Temple)':                                      (["an atlas of a deep forest", "blueprints of a deep forest"], "a Map of the Forest Temple", 'item'),
    'Map (Fire Temple)':                                        (["an atlas of a high mountain", "blueprints of a high mountain"], "a Map of the Fire Temple", 'item'),
    'Map (Water Temple)':                                       (["an atlas of a vast lake", "blueprints of a vast lake"], "a Map of the Water Temple", 'item'),
    'Map (Shadow Temple)':                                      (["an atlas of the house of the dead", "blueprints of the house of the dead"], "a Map of the Shadow Temple", 'item'),
    'Map (Spirit Temple)':                                      (["an atlas of the goddess of the sand", "blueprints of the goddess of the sand"], "a Map of the Spirit Temple", 'item'),
    'Map (Bottom of the Well)':                                 (["an atlas of a shadow's prison", "blueprints of a shadow's prison"], "a Map of the Bottom of the Well", 'item'),
    'Map (Ice Cavern)':                                         (["an atlas of a frozen maze", "blueprints of a frozen maze"], "a Map of the Ice Cavern", 'item'),
    'Compass':                                                  (["a treasure tracker", "a magnetic needle"], "a Compass", 'item'),
    'Compass (Deku Tree)':                                      (["a treasure tracker for an ancient tree", "a magnetic needle for an ancient tree"], "a Deku Tree Compass", 'item'),
    'Compass (Dodongos Cavern)':                                (["a treasure tracker for an immense cavern", "a magnetic needle for an immense cavern"], "a Dodongo's Cavern Compass", 'item'),
    'Compass (Jabu Jabus Belly)':                               (["a treasure tracker for the belly of a deity", "a magnetic needle for the belly of a deity"], "a Jabu Jabu's Belly Compass", 'item'),
    'Compass (Forest Temple)':                                  (["a treasure tracker for a deep forest", "a magnetic needle for a deep forest"], "a Forest Temple Compass", 'item'),
    'Compass (Fire Temple)':                                    (["a treasure tracker for a high mountain", "a magnetic needle for a high mountain"], "a Fire Temple Compass", 'item'),
    'Compass (Water Temple)':                                   (["a treasure tracker for a vast lake", "a magnetic needle for a vast lake"], "a Water Temple Compass", 'item'),
    'Compass (Shadow Temple)':                                  (["a treasure tracker for the house of the dead", "a magnetic needle for the house of the dead"], "a Shadow Temple Compass", 'item'),
    'Compass (Spirit Temple)':                                  (["a treasure tracker for a goddess of the sand", "a magnetic needle for a goddess of the sand"], "a Spirit Temple Compass", 'item'),
    'Compass (Bottom of the Well)':                             (["a treasure tracker for a shadow's prison", "a magnetic needle for a shadow's prison"], "a Bottom of the Well Compass", 'item'),
    'Compass (Ice Cavern)':                                     (["a treasure tracker for a frozen maze", "a magnetic needle for a frozen maze"], "an Ice Cavern Compass", 'item'),
    'BossKey':                                                  (["a master of unlocking", "a dungeon's master pass"], "a Boss Key", 'item'),
    'GanonBossKey':                                             (["a master of unlocking", "a dungeon's master pass"], "a Boss Key", 'item'),
    'SmallKey':                                                 (["a tool for unlocking", "a dungeon pass", "a lock remover", "a lockpick"], "a Small Key", 'item'),
    'HideoutSmallKey':                                          (["a get out of jail free card"], "a Jail Key", 'item'),
    'Boss Key (Forest Temple)':                                 (["a master of unlocking for a deep forest", "a master pass for a deep forest"], "the Forest Temple Boss Key", 'item'),
    'Boss Key (Fire Temple)':                                   (["a master of unlocking for a high mountain", "a master pass for a high mountain"], "the Fire Temple Boss Key", 'item'),
    'Boss Key (Water Temple)':                                  (["a master of unlocking for under a vast lake", "a master pass for under a vast lake"], "the Water Temple Boss Key", 'item'),
    'Boss Key (Shadow Temple)':                                 (["a master of unlocking for the house of the dead", "a master pass for the house of the dead"], "the Shadow Temple Boss Key", 'item'),
    'Boss Key (Spirit Temple)':                                 (["a master of unlocking for a goddess of the sand", "a master pass for a goddess of the sand"], "the Spirit Temple Boss Key", 'item'),
    'Boss Key (Ganons Castle)':                                 (["an master of unlocking", "a floating dungeon's master pass"], "Ganon's Castle Boss Key", 'item'),
    'Small Key (Forest Temple)':                                (["a tool for unlocking a deep forest", "a dungeon pass for a deep forest", "a lock remover for a deep forest", "a lockpick for a deep forest"], "a Forest Temple Small Key", 'item'),
    'Small Key (Fire Temple)':                                  (["a tool for unlocking a high mountain", "a dungeon pass for a high mountain", "a lock remover for a high mountain", "a lockpick for a high mountain"], "a Fire Temple Small Key", 'item'),
    'Small Key (Water Temple)':                                 (["a tool for unlocking a vast lake", "a dungeon pass for under a vast lake", "a lock remover for under a vast lake", "a lockpick for under a vast lake"], "a Water Temple Small Key", 'item'),
    'Small Key (Shadow Temple)':                                (["a tool for unlocking the house of the dead", "a dungeon pass for the house of the dead", "a lock remover for the house of the dead", "a lockpick for the house of the dead"], "a Shadow Temple Small Key", 'item'),
    'Small Key (Spirit Temple)':                                (["a tool for unlocking a goddess of the sand", "a dungeon pass for a goddess of the sand", "a lock remover for a goddess of the sand", "a lockpick for a goddess of the sand"], "a Spirit Temple Small Key", 'item'),
    'Small Key (Bottom of the Well)':                           (["a tool for unlocking a shadow's prison", "a dungeon pass for a shadow's prison", "a lock remover for a shadow's prison", "a lockpick for a shadow's prison"], "a Bottom of the Well Small Key", 'item'),
    'Small Key (Gerudo Training Ground)':                       (["a tool for unlocking the test of thieves", "a dungeon pass for the test of thieves", "a lock remover for the test of thieves", "a lockpick for the test of thieves"], "a Gerudo Training Ground Small Key", 'item'),
    'Small Key (Ganons Castle)':                                (["a tool for unlocking a conquered citadel", "a dungeon pass for a conquered citadel", "a lock remover for a conquered citadel", "a lockpick for a conquered citadel"], "a Ganon's Castle Small Key", 'item'),
    'Small Key (Thieves Hideout)':                              (["a get out of jail free card"], "a Jail Key", 'item'),
    'Small Key Ring (Forest Temple)':                           (["a toolbox for unlocking a deep forest", "a dungeon season pass for a deep forest", "a jingling ring for a deep forest", "a skeleton key for a deep forest"], "a Forest Temple Small Key Ring", 'item'),
    'Small Key Ring (Fire Temple)':                             (["a toolbox for unlocking a high mountain", "a dungeon season pass for a high mountain", "a jingling ring for a high mountain", "a skeleton key for a high mountain"], "a Fire Temple Small Key Ring", 'item'),
    'Small Key Ring (Water Temple)':                            (["a toolbox for unlocking a vast lake", "a dungeon season pass for under a vast lake", "a jingling ring for under a vast lake", "a skeleton key for under a vast lake"], "a Water Temple Small Key Ring", 'item'),
    'Small Key Ring (Shadow Temple)':                           (["a toolbox for unlocking the house of the dead", "a dungeon season pass for the house of the dead", "a jingling ring for the house of the dead", "a skeleton key for the house of the dead"], "a Shadow Temple Small Key Ring", 'item'),
    'Small Key Ring (Spirit Temple)':                           (["a toolbox for unlocking a goddess of the sand", "a dungeon season pass for a goddess of the sand", "a jingling ring for a goddess of the sand", "a skeleton key for a goddess of the sand"], "a Spirit Temple Small Key Ring", 'item'),
    'Small Key Ring (Bottom of the Well)':                      (["a toolbox for unlocking a shadow's prison", "a dungeon season pass for a shadow's prison", "a jingling ring for a shadow's prison", "a skeleton key for a shadow's prison"], "a Bottom of the Well Small Key Ring", 'item'),
    'Small Key Ring (Gerudo Training Ground)':                  (["a toolbox for unlocking the test of thieves", "a dungeon season pass for the test of thieves", "a jingling ring for the test of thieves", "a skeleton key for the test of thieves"], "a Gerudo Training Ground Small Key Ring", 'item'),
    'Small Key Ring (Ganons Castle)':                           (["a toolbox for unlocking a conquered citadel", "a dungeon season pass for a conquered citadel", "a jingling ring for a conquered citadel", "a skeleton key for a conquered citadel"], "a Ganon's Castle Small Key Ring", 'item'),
    'Small Key Ring (Thieves Hideout)':                         (["a deck of get out of jail free cards"], "a Jail Key Ring", 'item'),
    'KeyError':                                                 (["something mysterious", "an unknown treasure"], "An Error (Please Report This)", 'item'),
    'Arrows (5)':                                               (["a few danger darts", "a few sharp shafts"], "Arrows (5 pieces)", 'item'),
    'Arrows (10)':                                              (["some danger darts", "some sharp shafts"], "Arrows (10 pieces)", 'item'),
    'Arrows (30)':                                              (["plenty of danger darts", "plenty of sharp shafts"], "Arrows (30 pieces)", 'item'),
    'Bombs (5)':                                                (["a few explosives", "a few blast balls"], "Bombs (5 pieces)", 'item'),
    'Bombs (10)':                                               (["some explosives", "some blast balls"], "Bombs (10 pieces)", 'item'),
    'Bombs (20)':                                               (["lots-o-explosives", "plenty of blast balls"], "Bombs (20 pieces)", 'item'),
    'Ice Trap':                                                 (["a gift from Ganon", "a chilling discovery", "frosty fun"], "an Ice Trap", 'item'),
    'Magic Bean':                                               (["a wizardly legume"], "a Magic Bean", 'item'),
    'Buy Magic Bean':                                           (["a wizardly legume"], "a Magic Bean", 'item'),
    'Magic Bean Pack':                                          (["wizardly legumes"], "Magic Beans", 'item'),
    'Bombchus':                                                 (["mice bombs", "proximity mice", "wall crawlers", "trail blazers"], "Bombchus", 'item'),
    'Bombchus (5)':                                             (["a few mice bombs", "a few proximity mice", "a few wall crawlers", "a few trail blazers"], "Bombchus (5 pieces)", 'item'),
    'Bombchus (10)':                                            (["some mice bombs", "some proximity mice", "some wall crawlers", "some trail blazers"], "Bombchus (10 pieces)", 'item'),
    'Bombchus (20)':                                            (["plenty of mice bombs", "plenty of proximity mice", "plenty of wall crawlers", "plenty of trail blazers"], "Bombchus (20 pieces)", 'item'),
    'Deku Nuts (5)':                                            (["some nuts", "some flashbangs", "some scrub spit"], "Deku Nuts (5 pieces)", 'item'),
    'Deku Nuts (10)':                                           (["lots-o-nuts", "plenty of flashbangs", "plenty of scrub spit"], "Deku Nuts (10 pieces)", 'item'),
    'Deku Seeds (30)':                                          (["catapult ammo", "lots-o-seeds"], "Deku Seeds (30 pieces)", 'item'),
    'Gold Skulltula Token':                                     (["proof of destruction", "an arachnid chip", "spider remains", "one percent of a curse"], "a Gold Skulltula Token", 'item'),

    'ZR Frogs Ocarina Game':                                       (["an #amphibian feast# yields", "the #croaking choir's magnum opus# awards", "the #froggy finale# yields"], "the final reward from the #Frogs of Zora's River# is", 'always'),
    'KF Links House Cow':                                          ("the #bovine bounty of a horseback hustle# gifts", "#Malon's obstacle course# leads to", 'always'),

    'Song from Ocarina of Time':                                   ("the #Ocarina of Time# teaches", None, ['song', 'sometimes']),
    'Song from Royal Familys Tomb':                                (["#ReDead in the royal tomb# guard", "the #Composer Brothers wrote#"], None, ['song', 'sometimes']),
    'Sheik in Forest':                                             ("#in a meadow# Sheik teaches", None, ['song', 'sometimes']),
    'Sheik at Temple':                                             ("Sheik waits at a #monument to time# to teach", None, ['song', 'sometimes']),
    'Sheik in Crater':                                             ("the #crater's melody# is", None, ['song', 'sometimes']),
    'Sheik in Ice Cavern':                                         ("the #frozen cavern# echoes with", None, ['song', 'sometimes']),
    'Sheik in Kakariko':                                           ("a #ravaged village# mourns with", None, ['song', 'sometimes']),
    'Sheik at Colossus':                                           ("a hero ventures #beyond the wasteland# to learn", None, ['song', 'sometimes']),

    'Market 10 Big Poes':                                          ("#ghost hunters# will be rewarded with", "catching #Big Poes# leads to", ['overworld', 'sometimes']),
    'Deku Theater Skull Mask':                                     ("the #Skull Mask# yields", None, ['overworld', 'sometimes']),
    'Deku Theater Mask of Truth':                                  ("showing a #truthful eye to the crowd# rewards", "the #Mask of Truth# yields", ['overworld', 'sometimes']),
    'HF Ocarina of Time Item':                                     ("the #treasure thrown by Princess Zelda# is", None, ['overworld', 'sometimes']),
    'DMT Biggoron':                                                ("#Biggoron# crafts", None, ['overworld', 'sometimes']),
    'Kak 50 Gold Skulltula Reward':                                (["#50 bug badges# rewards", "#50 spider souls# yields", "#50 auriferous arachnids# lead to"], "slaying #50 Gold Skulltulas# reveals", ['overworld', 'sometimes']),
    'Kak 40 Gold Skulltula Reward':                                (["#40 bug badges# rewards", "#40 spider souls# yields", "#40 auriferous arachnids# lead to"], "slaying #40 Gold Skulltulas# reveals", ['overworld', 'sometimes']),
    'Kak 30 Gold Skulltula Reward':                                (["#30 bug badges# rewards", "#30 spider souls# yields", "#30 auriferous arachnids# lead to"], "slaying #30 Gold Skulltulas# reveals", ['overworld', 'sometimes']),
    'Kak 20 Gold Skulltula Reward':                                (["#20 bug badges# rewards", "#20 spider souls# yields", "#20 auriferous arachnids# lead to"], "slaying #20 Gold Skulltulas# reveals", ['overworld', 'sometimes']),
    'Kak Anju as Child':                                           (["#wrangling roosters# rewards", "#chucking chickens# gifts"], "#collecting cuccos# rewards", ['overworld', 'sometimes']),
    'GC Darunias Joy':                                             ("a #groovin' goron# gifts", "#Darunia's dance# leads to", ['overworld', 'sometimes']),
    'LW Skull Kid':                                                ("the #Skull Kid# grants", None, ['overworld', 'sometimes']),
    'LH Sun':                                                      ("staring into #the sun# grants", "shooting #the sun# grants", ['overworld', 'sometimes']),
    'Market Treasure Chest Game Reward':                           (["#gambling# grants", "there is a #1/32 chance# to win"], "the #treasure chest game# grants", ['overworld', 'sometimes']),
    'GF HBA 1500 Points':                                          ("mastery of #horseback archery# grants", "scoring 1500 in #horseback archery# grants", ['overworld', 'sometimes']),
    'Graveyard Heart Piece Grave Chest':                           ("playing #Sun's Song# in a grave spawns", None, ['overworld', 'sometimes']),
    'GC Maze Left Chest':                                          ("in #Goron City# the hammer unlocks", None, ['overworld', 'sometimes']),
    'GV Chest':                                                    ("in #Gerudo Valley# the hammer unlocks", None, ['overworld', 'sometimes']),
    'GV Cow':                                                      ("a #cow in Gerudo Valley# gifts", None, ['overworld', 'sometimes']),
    'HC GS Storms Grotto':                                         ("a #spider behind a muddy wall# in a grotto holds", None, ['overworld', 'sometimes']),
    'HF GS Cow Grotto':                                            ("a #spider behind webs# in a grotto holds", None, ['overworld', 'sometimes']),
    'HF Cow Grotto Cow':                                           ("the #cobwebbed cow# gifts", "a #cow behind webs# in a grotto gifts", ['overworld', 'sometimes']),
    'ZF GS Hidden Cave':                                           ("a spider high #above the icy waters# holds", None, ['overworld', 'sometimes']),
    'Wasteland Chest':                                             (["#deep in the wasteland# is", "beneath #the sands#, flames reveal"], None, ['overworld', 'sometimes']),
    'Wasteland GS':                                                ("a #spider in the wasteland# holds", None, ['overworld', 'sometimes']),
    'Graveyard Royal Familys Tomb Chest':                          (["#flames in the royal tomb# reveal", "the #Composer Brothers hid#"], None, ['overworld', 'sometimes']),
    'ZF Bottom Freestanding PoH':                                  ("#under the icy waters# lies", None, ['overworld', 'sometimes']),
    'GC Pot Freestanding PoH':                                     ("spinning #Goron pottery# contains", None, ['overworld', 'sometimes']),
    'ZD King Zora Thawed':                                         ("a #defrosted dignitary# gifts", "unfreezing #King Zora# grants", ['overworld', 'sometimes']),
    'DMC Deku Scrub':                                              ("a single #scrub in the crater# sells", None, ['overworld', 'sometimes']),
    'DMC GS Crate':                                                ("a spider under a #crate in the crater# holds", None, ['overworld', 'sometimes']),
    'LW Target in Woods':                                          ("shooting a #target in the woods# grants", None, ['overworld', 'sometimes']),
    'ZR Frogs in the Rain':                                        ("#frogs in a storm# gift", None, ['overworld', 'sometimes']),
    'LH Lab Dive':                                                 ("a #diving experiment# is rewarded with", None, ['overworld', 'sometimes']),
    'HC Great Fairy Reward':                                       ("the #fairy of fire# holds", "a #fairy outside Hyrule Castle# holds", ['overworld', 'sometimes']),
    'OGC Great Fairy Reward':                                      ("the #fairy of strength# holds", "a #fairy outside Ganon's Castle# holds", ['overworld', 'sometimes']),

    'Deku Tree MQ After Spinning Log Chest':                       ("a #temporal stone within a tree# contains", "a #temporal stone within the Deku Tree# contains", ['dungeon', 'sometimes']),
    'Deku Tree MQ GS Basement Graves Room':                        ("a #spider on a ceiling in a tree# holds", "a #spider on a ceiling in the Deku Tree# holds", ['dungeon', 'sometimes']),
    'Dodongos Cavern MQ GS Song of Time Block Room':               ("a spider under #temporal stones in a cavern# holds", "a spider under #temporal stones in Dodongo's Cavern# holds", ['dungeon', 'sometimes']),
    'Jabu Jabus Belly Boomerang Chest':                            ("a school of #stingers swallowed by a deity# guard", "a school of #stingers swallowed by Jabu Jabu# guard", ['dungeon', 'sometimes']),
    'Jabu Jabus Belly MQ GS Invisible Enemies Room':               ("a spider surrounded by #shadows in the belly of a deity# holds", "a spider surrounded by #shadows in Jabu Jabu's Belly# holds", ['dungeon', 'sometimes']),
    'Jabu Jabus Belly MQ Cow':                                     ("a #cow swallowed by a deity# gifts", "a #cow swallowed by Jabu Jabu# gifts", ['dungeon', 'sometimes']),
    'Fire Temple Scarecrow Chest':                                 ("a #scarecrow atop the volcano# hides", "#Pierre atop the Fire Temple# hides", ['dungeon', 'sometimes']),
    'Fire Temple Megaton Hammer Chest':                            ("the #Flare Dancer atop the volcano# guards a chest containing", "the #Flare Dancer atop the Fire Temple# guards a chest containing", ['dungeon', 'sometimes']),
    'Fire Temple MQ Chest On Fire':                                ("the #Flare Dancer atop the volcano# guards a chest containing", "the #Flare Dancer atop the Fire Temple# guards a chest containing", ['dungeon', 'sometimes']),
    'Fire Temple MQ GS Skull On Fire':                             ("a #spider under a block in the volcano# holds", "a #spider under a block in the Fire Temple# holds", ['dungeon', 'sometimes']),
    'Water Temple River Chest':                                    ("beyond the #river under the lake# waits", "beyond the #river in the Water Temple# waits", ['dungeon', 'sometimes']),
    'Water Temple Central Pillar Chest':                           ("beneath a #tall tower under a vast lake# lies", "a chest in the #central pillar of Water Temple# contains", ['dungeon', 'sometimes']),
    'Water Temple Boss Key Chest':                                 ("dodging #rolling boulders under the lake# leads to", "dodging #rolling boulders in the Water Temple# leads to", ['dungeon', 'sometimes']),
    'Water Temple GS Behind Gate':                                 ("a spider behind a #gate under the lake# holds", "a spider behind a #gate in the Water Temple# holds", ['dungeon', 'sometimes']),
    'Water Temple MQ Central Pillar Chest':                        ("beneath a #tall tower under a vast lake# lies", "a chest in the #central pillar of Water Temple# contains", ['dungeon', 'sometimes']),
    'Water Temple MQ Freestanding Key':                            ("hidden in a #box under the lake# lies", "hidden in a #box in the Water Temple# lies", ['dungeon', 'sometimes']),
    'Water Temple MQ GS Freestanding Key Area':                    ("the #locked spider under the lake# holds", "the #locked spider in the Water Temple# holds", ['dungeon', 'sometimes']),
    'Water Temple MQ GS Triple Wall Torch':                        ("a spider behind a #gate under the lake# holds", "a spider behind a #gate in the Water Temple# holds", ['dungeon', 'sometimes']),
    'Gerudo Training Ground Underwater Silver Rupee Chest':        (["those who seek #sunken silver rupees# will find", "the #thieves' underwater training# rewards"], None, ['dungeon', 'sometimes']),
    'Gerudo Training Ground MQ Underwater Silver Rupee Chest':     (["those who seek #sunken silver rupees# will find", "the #thieves' underwater training# rewards"], None, ['dungeon', 'sometimes']),
    'Gerudo Training Ground Maze Path Final Chest':                ("the final prize of #the thieves' training# is", None, ['dungeon', 'sometimes']),
    'Gerudo Training Ground MQ Ice Arrows Chest':                  ("the final prize of #the thieves' training# is", None, ['dungeon', 'sometimes']),
    'Spirit Temple Silver Gauntlets Chest':                        ("the treasure #sought by Nabooru# is", "upon the #Colossus's right hand# is", ['dungeon', 'sometimes']),
    'Spirit Temple Mirror Shield Chest':                           ("upon the #Colossus's left hand# is", None, ['dungeon', 'sometimes']),
    'Spirit Temple MQ Child Hammer Switch Chest':                  ("a #temporal paradox in the Colossus# yields", "a #temporal paradox in the Spirit Temple# yields", ['dungeon', 'sometimes']),
    'Spirit Temple MQ Symphony Room Chest':                        ("a #symphony in the Colossus# yields", "a #symphony in the Spirit Temple# yields", ['dungeon', 'sometimes']),
    'Spirit Temple MQ GS Symphony Room':                           ("a #spider's symphony in the Colossus# yields", "a #spider's symphony in the Spirit Temple# yields", ['dungeon', 'sometimes']),
    'Shadow Temple Freestanding Key':                              ("a #burning skull in the house of the dead# holds", "a #giant pot in the Shadow Temple# holds", ['dungeon', 'sometimes']),
    'Shadow Temple MQ Bomb Flower Chest':                          ("shadows in an #invisible maze# guard", None, ['dungeon', 'sometimes']),
    'Shadow Temple MQ Stalfos Room Chest':                         ("near an #empty pedestal within the house of the dead# lies", "#stalfos in the Shadow Temple# guard", ['dungeon', 'sometimes']),
    'Ice Cavern Iron Boots Chest':                                 ("a #monster in a frozen cavern# guards", "the #final treasure of Ice Cavern# is", ['dungeon', 'sometimes']),
    'Ice Cavern MQ Iron Boots Chest':                              ("a #monster in a frozen cavern# guards", "the #final treasure of Ice Cavern# is", ['dungeon', 'sometimes']),
    'Ganons Castle Shadow Trial Golden Gauntlets Chest':           ("#deep in the test of darkness# lies", "a #like-like in Ganon's Shadow Trial# guards", ['dungeon', 'sometimes']),
    'Ganons Castle MQ Shadow Trial Eye Switch Chest':              ("#deep in the test of darkness# lies", "shooting an #eye switch in Ganon's Shadow Trial# reveals", ['dungeon', 'sometimes']),

    'Deku Theater Rewards':                                        ("the #Skull Mask and Mask of Truth# reward...^", None, 'dual'),
    'HF Ocarina of Time Retrieval':                                ("during her escape, #Princess Zelda# entrusted you with both...^", "the #Ocarina of Time# rewards both...^", 'dual'),
    'HF Valley Grotto':                                            ("in a grotto with a #spider and a cow# you will find...^", None, 'dual'),
    'Market Bombchu Bowling Rewards':                              ("at the #Bombchu Bowling Alley#, you will be rewarded with...^", None, 'dual'),
    'ZR Frogs Rewards':                                            ("the #Frogs of Zora River# will reward you with...^", None, 'dual'),
    'LH Lake Lab Pool':                                            ("inside the #lakeside lab# a person and a spider hold...^", None, 'dual'),
    'LH Adult Bean Destination Checks':                            ("#riding the bean in Lake Hylia# leads to...^", None, 'dual'),
    'GV Pieces of Heart Ledges':                                   ("within the #valley#, the crate and waterfall conceal...^", None, 'dual'),
    'GF Horseback Archery Rewards':                                ("the #Gerudo Horseback Archery# rewards...^", None, 'dual'),
    'Colossus Nighttime GS':                                       ("#at the Desert Colossus#, skulltulas at night hold...^", None, 'dual'),
    'Graveyard Dampe Race Rewards':                                ("racing #Dampé's ghost# rewards...^", None, 'dual'),
    'Graveyard Royal Family Tomb Contents':                        ("inside the #Royal Family Tomb#, you will find...^", None, 'dual'),
    'DMC Child Upper Checks':                                      ("in the #crater, a spider in a crate and a single scrub# guard...^", None, 'dual'),
    'Haunted Wasteland Checks':                                    ("deep in the #wasteland a spider and a chest# hold...^", None, 'dual'),

    'Deku Tree MQ Basement GS':                                    ("in the back of the #basement of the Great Deku Tree# two spiders hold...^", None, 'dual'),
    'Dodongos Cavern Upper Business Scrubs':                       ("deep in #Dodongo's Cavern a pair of scrubs# sell...^", None, 'dual'),
    'Dodongos Cavern MQ Larvae Room':                              ("amid #larvae in Dodongo's Cavern# a chest and a spider hold...^", None, 'dual'),
    'Fire Temple Lower Loop':                                      ("under the #entrance of the Fire Temple# a blocked path leads to...^", None, 'dual'),
    'Fire Temple MQ Lower Loop':                                   ("under the #entrance of the Fire Temple# a blocked path leads to...^", None, 'dual'),
    'Water Temple River Loop Chests':                              ("#chests past a shadowy fight# in the Water Temple hold...^", "#chests past Dark Link# in the Water Temple hold...^", 'dual'),
    'Water Temple River Checks':                                   ("in the #river in the Water Temple# lies...^", None, 'dual'),
    'Water Temple North Basement Checks':                          ("the #northern basement of the Water Temple# contains...^", None, 'dual'),
    'Water Temple MQ North Basement Checks':                       ("the #northern basement of the Water Temple# contains...^", None, 'dual'),
    'Water Temple MQ Lower Checks':                                ("#a chest and a crate in locked basements# in the Water Temple hold...^", None, 'dual'),
    'Spirit Temple Colossus Hands':                                ("upon the #Colossus's right and left hands# lie...^", None, 'dual'),
    'Spirit Temple Child Lower':                                   ("between the #crawl spaces in the Spirit Temple# chests contain...^", None, 'dual'),
    'Spirit Temple Child Top':                                     ("on the path to the #right hand of the Spirit Temple# a chest and a spider hold...^", None, 'dual'),
    'Spirit Temple Adult Lower':                                   ("past a #silver block in the Spirit Temple# boulders and a melody conceal...^", None, 'dual'),
    'Spirit Temple MQ Child Top':                                  ("on the path to the #right hand of the Spirit Temple# a chest and a spider hold respectively...^", None, 'dual'),
    'Spirit Temple MQ Symphony Room':                              ("#the symphony room# in the Spirit Temple protects...^", None, 'dual'),
    'Spirit Temple MQ Throne Room GS':                             ("in the #nine thrones room# of the Spirit Temple spiders hold...^", None, 'dual'),
    'Shadow Temple Invisible Blades Chests':                       ("an #invisible spinning blade# in the Shadow Temple guards...^", None, 'dual'),
    'Shadow Temple Single Pot Room':                               ("a room containing #a single skull-shaped pot# holds...^", "a room containing a #large pot in the Shadow Temple# holds...^", 'dual'),
    'Shadow Temple Spike Walls Room':                              ("#wooden walls# in the Shadow Temple hide...^", None, 'dual'),
    'Shadow Temple MQ Upper Checks':                               ("#before the Truth Spinner gap# in the Shadow Temple locked chests contain...^", None, 'dual'),
    'Shadow Temple MQ Invisible Blades Chests':                    ("an #invisible spinning blade# in the Shadow Temple guards...^", None, 'dual'),
    'Shadow Temple MQ Spike Walls Room':                           ("#wooden walls# in the Shadow Temple hide...^", None, 'dual'),
    'Bottom of the Well Inner Rooms GS':                           ("in the #central rooms of the well# spiders hold...^", None, 'dual'),
    'Bottom of the Well Dead Hand Room':                           ("#Dead Hand in the well# guards...^", None, 'dual'),
    'Bottom of the Well MQ Dead Hand Room':                        ("#Dead Hand in the well# guards...^", None, 'dual'),
    'Bottom of the Well MQ Basement':                              ("in the #depths of the well# a spider and a chest hold...^", None, 'dual'),
    'Ice Cavern Final Room':                                       ("the #final treasures of Ice Cavern# are...^", None, 'dual'),
    'Ice Cavern MQ Final Room':                                    ("the #final treasures of Ice Cavern# are...^", None, 'dual'),
    'Ganons Castle Spirit Trial Chests':                           ("#within the Spirit Trial#, chests contain...^", None, 'dual'),

    'KF Kokiri Sword Chest':                                       ("the #hidden treasure of the Kokiri# is", None, 'exclude'),
    'KF Midos Top Left Chest':                                     ("the #leader of the Kokiri# hides", "#inside Mido's house# is", 'exclude'),
    'KF Midos Top Right Chest':                                    ("the #leader of the Kokiri# hides", "#inside Mido's house# is", 'exclude'),
    'KF Midos Bottom Left Chest':                                  ("the #leader of the Kokiri# hides", "#inside Mido's house# is", 'exclude'),
    'KF Midos Bottom Right Chest':                                 ("the #leader of the Kokiri# hides", "#inside Mido's house# is", 'exclude'),
    'Graveyard Shield Grave Chest':                                ("the #treasure of a fallen soldier# is", None, 'exclude'),
    'DMT Chest':                                                   ("hidden behind a wall on a #mountain trail# is", None, 'exclude'),
    'GC Maze Right Chest':                                         ("in #Goron City# explosives unlock", None, 'exclude'),
    'GC Maze Center Chest':                                        ("in #Goron City# explosives unlock", None, 'exclude'),
    'ZD Chest':                                                    ("fire #beyond a waterfall# reveals", None, 'exclude'),
    'Graveyard Dampe Race Hookshot Chest':                         ("a chest hidden by a #speedy spectre# holds", "#dead Dampé's first prize# is", 'exclude'),
    'GF Chest':                                                    ("on a #rooftop in the desert# lies", None, 'exclude'),
    'Kak Redead Grotto Chest':                                     ("#zombies beneath the earth# guard", None, 'exclude'),
    'SFM Wolfos Grotto Chest':                                     ("#wolves beneath the earth# guard", None, 'exclude'),
    'HF Near Market Grotto Chest':                                 ("a #hole in a field near a drawbridge# holds", None, 'exclude'),
    'HF Southeast Grotto Chest':                                   ("a #hole amongst trees in a field# holds", None, 'exclude'),
    'HF Open Grotto Chest':                                        ("an #open hole in a field# holds", None, 'exclude'),
    'Kak Open Grotto Chest':                                       ("an #open hole in a town# holds", None, 'exclude'),
    'ZR Open Grotto Chest':                                        ("a #hole along a river# holds", None, 'exclude'),
    'KF Storms Grotto Chest':                                      ("a #hole in a forest village# holds", None, 'exclude'),
    'LW Near Shortcuts Grotto Chest':                              ("a #hole in a wooded maze# holds", None, 'exclude'),
    'DMT Storms Grotto Chest':                                     ("#hole flooded with rain on a mountain# holds", None, 'exclude'),
    'DMC Upper Grotto Chest':                                      ("a #hole in a volcano# holds", None, 'exclude'),

    'ToT Light Arrows Cutscene':                                   ("the #final gift of a princess# is", None, 'exclude'),
    'LW Gift from Saria':                                          (["a #potato hoarder# holds", "a rooty tooty #flutey cutey# gifts"], "#Saria's Gift# is", 'exclude'),
    'ZF Great Fairy Reward':                                       ("the #fairy of winds# holds", None, 'exclude'),
    'Colossus Great Fairy Reward':                                 ("the #fairy of love# holds", None, 'exclude'),
    'DMT Great Fairy Reward':                                      ("a #magical fairy# gifts", None, 'exclude'),
    'DMC Great Fairy Reward':                                      ("a #magical fairy# gifts", None, 'exclude'),

    'Song from Impa':                                              ("#deep in a castle#, Impa teaches", None, 'exclude'),
    'Song from Malon':                                             ("#a farm girl# sings", None, 'exclude'),
    'Song from Saria':                                             ("#deep in the forest#, Saria teaches", None, 'exclude'),
    'Song from Windmill':                                          ("a man #in a windmill# is obsessed with", None, 'exclude'),

    'HC Malon Egg':                                                ("a #girl looking for her father# gives", None, 'exclude'),
    'HC Zeldas Letter':                                            ("a #princess in a castle# gifts", None, 'exclude'),
    'ZD Diving Minigame':                                          ("an #unsustainable business model# gifts", "those who #dive for Zora rupees# will find", 'exclude'),
    'LH Child Fishing':                                            ("#fishing in youth# bestows", None, 'exclude'),
    'LH Adult Fishing':                                            ("#fishing in maturity# bestows", None, 'exclude'),
    'GC Rolling Goron as Adult':                                   ("#comforting yourself# provides", "#reassuring a young Goron# is rewarded with", 'exclude'),
    'Market Bombchu Bowling First Prize':                          ("the #first explosive prize# is", None, 'exclude'),
    'Market Bombchu Bowling Second Prize':                         ("the #second explosive prize# is", None, 'exclude'),
    'Market Lost Dog':                                             ("#puppy lovers# will find", "#rescuing Richard the Dog# is rewarded with", 'exclude'),
    'LW Ocarina Memory Game':                                      (["the prize for a #game of Simon Says# is", "a #child sing-a-long# holds"], "#playing an Ocarina in Lost Woods# is rewarded with", 'exclude'),
    'Kak 10 Gold Skulltula Reward':                                (["#10 bug badges# rewards", "#10 spider souls# yields", "#10 auriferous arachnids# lead to"], "slaying #10 Gold Skulltulas# reveals", 'exclude'),
    'Kak Man on Roof':                                             ("a #rooftop wanderer# holds", None, 'exclude'),
    'ZR Magic Bean Salesman':                                      ("a seller of #colorful crops# has", "a #bean seller# offers", 'exclude'),
    'GF HBA 1000 Points':                                          ("scoring 1000 in #horseback archery# grants", None, 'exclude'),
    'Market Shooting Gallery Reward':                              ("#shooting in youth# grants", None, 'exclude'),
    'Kak Shooting Gallery Reward':                                 ("#shooting in maturity# grants", None, 'exclude'),
    'Kak Anju as Adult':                                           ("a #chicken caretaker# offers adults", None, 'exclude'),
    'LLR Talons Chickens':                                         ("#finding Super Cuccos# is rewarded with", None, 'exclude'),
    'GC Rolling Goron as Child':                                   ("the prize offered by a #large rolling Goron# is", None, 'exclude'),
    'LH Underwater Item':                                          ("the #sunken treasure in a lake# is", None, 'exclude'),
    'Hideout Gerudo Membership Card':                              ("#rescuing captured carpenters# is rewarded with", None, 'exclude'),
    'Wasteland Bombchu Salesman':                                  ("a #carpet guru# sells", None, 'exclude'),
    'GC Medigoron':                                                ("#Medigoron# sells", None, 'exclude'),

    'Kak Impas House Freestanding PoH':                            ("#imprisoned in a house# lies", None, 'exclude'),
    'HF Tektite Grotto Freestanding PoH':                          ("#deep underwater in a hole# is", None, 'exclude'),
    'Kak Windmill Freestanding PoH':                               ("on a #windmill ledge# lies", None, 'exclude'),
    'Graveyard Dampe Race Freestanding PoH':                       ("#racing a ghost# leads to", "#dead Dampé's second# prize is", 'exclude'),
    'LLR Freestanding PoH':                                        ("in a #ranch silo# lies", None, 'exclude'),
    'Graveyard Freestanding PoH':                                  ("a #crate in a graveyard# hides", None, 'exclude'),
    'Graveyard Dampe Gravedigging Tour':                           ("a #gravekeeper digs up#", None, 'exclude'),
    'ZR Near Open Grotto Freestanding PoH':                        ("on top of a #pillar in a river# lies", None, 'exclude'),
    'ZR Near Domain Freestanding PoH':                             ("on a #river ledge by a waterfall# lies", None, 'exclude'),
    'LH Freestanding PoH':                                         ("high on a #lab rooftop# one can find", None, 'exclude'),
    'ZF Iceberg Freestanding PoH':                                 ("#floating on ice# is", None, 'exclude'),
    'GV Waterfall Freestanding PoH':                               ("behind a #desert waterfall# is", None, 'exclude'),
    'GV Crate Freestanding PoH':                                   ("a #crate in a valley# hides", None, 'exclude'),
    'Colossus Freestanding PoH':                                   ("on top of an #arch of stone# lies", None, 'exclude'),
    'DMT Freestanding PoH':                                        ("above a #mountain cavern entrance# is", None, 'exclude'),
    'DMC Wall Freestanding PoH':                                   ("nestled in a #volcanic wall# is", None, 'exclude'),
    'DMC Volcano Freestanding PoH':                                ("obscured by #volcanic ash# is", None, 'exclude'),
    'Hideout 1 Torch Jail Gerudo Key':                             ("#defeating Gerudo guards# reveals", None, 'exclude'),
    'Hideout 2 Torches Jail Gerudo Key':                           ("#defeating Gerudo guards# reveals", None, 'exclude'),
    'Hideout 3 Torches Jail Gerudo Key':                           ("#defeating Gerudo guards# reveals", None, 'exclude'),
    'Hideout 4 Torches Jail Gerudo Key':                           ("#defeating Gerudo guards# reveals", None, 'exclude'),

    'ZR Frogs Zeldas Lullaby':                                     ("after hearing #Zelda's Lullaby, frogs gift#", None, 'exclude'),
    'ZR Frogs Eponas Song':                                        ("after hearing #Epona's Song, frogs gift#", None, 'exclude'),
    'ZR Frogs Sarias Song':                                        ("after hearing #Saria's Song, frogs gift#", None, 'exclude'),
    'ZR Frogs Suns Song':                                          ("after hearing the #Sun's Song, frogs gift#", None, 'exclude'),
    'ZR Frogs Song of Time':                                       ("after hearing the #Song of Time, frogs gift#", None, 'exclude'),

    'Deku Tree Map Chest':                                         ("in the #center of the Deku Tree# lies", None, 'exclude'),
    'Deku Tree Slingshot Chest':                                   ("the #treasure guarded by a scrub# in the Deku Tree is", None, 'exclude'),
    'Deku Tree Slingshot Room Side Chest':                         ("the #treasure guarded by a scrub# in the Deku Tree is", None, 'exclude'),
    'Deku Tree Compass Chest':                                     ("#pillars of wood# in the Deku Tree lead to", None, 'exclude'),
    'Deku Tree Compass Room Side Chest':                           ("#pillars of wood# in the Deku Tree lead to", None, 'exclude'),
    'Deku Tree Basement Chest':                                    ("#webs in the Deku Tree# hide", None, 'exclude'),

    'Deku Tree MQ Map Chest':                                      ("in the #center of the Deku Tree# lies", None, 'exclude'),
    'Deku Tree MQ Compass Chest':                                  ("a #treasure guarded by a large spider# in the Deku Tree is", None, 'exclude'),
    'Deku Tree MQ Slingshot Chest':                                ("#pillars of wood# in the Deku Tree lead to", None, 'exclude'),
    'Deku Tree MQ Slingshot Room Back Chest':                      ("#pillars of wood# in the Deku Tree lead to", None, 'exclude'),
    'Deku Tree MQ Basement Chest':                                 ("#webs in the Deku Tree# hide", None, 'exclude'),
    'Deku Tree MQ Before Spinning Log Chest':                      ("#magical fire in the Deku Tree# leads to", None, 'exclude'),

    'Dodongos Cavern Boss Room Chest':                             ("#above King Dodongo# lies", None, 'exclude'),

    'Dodongos Cavern Map Chest':                                   ("a #muddy wall in Dodongo's Cavern# hides", None, 'exclude'),
    'Dodongos Cavern Compass Chest':                               ("a #statue in Dodongo's Cavern# guards", None, 'exclude'),
    'Dodongos Cavern Bomb Flower Platform Chest':                  ("above a #maze of stone# in Dodongo's Cavern lies", None, 'exclude'),
    'Dodongos Cavern Bomb Bag Chest':                              ("the #second lizard cavern battle# yields", None, 'exclude'),
    'Dodongos Cavern End of Bridge Chest':                         ("a #chest at the end of a bridge# yields", None, 'exclude'),

    'Dodongos Cavern MQ Map Chest':                                ("a #muddy wall in Dodongo's Cavern# hides", None, 'exclude'),
    'Dodongos Cavern MQ Bomb Bag Chest':                           ("an #elevated alcove# in Dodongo's Cavern holds", None, 'exclude'),
    'Dodongos Cavern MQ Compass Chest':                            ("#fire-breathing lizards# in Dodongo's Cavern guard", None, 'exclude'),
    'Dodongos Cavern MQ Larvae Room Chest':                        ("#baby spiders# in Dodongo's Cavern guard", None, 'exclude'),
    'Dodongos Cavern MQ Torch Puzzle Room Chest':                  ("above a #maze of stone# in Dodongo's Cavern lies", None, 'exclude'),
    'Dodongos Cavern MQ Under Grave Chest':                        ("#beneath a headstone# in Dodongo's Cavern lies", None, 'exclude'),

    'Jabu Jabus Belly Map Chest':                                  ("#tentacle trouble# in a deity's belly guards", "a #slimy thing# guards", 'exclude'),
    'Jabu Jabus Belly Compass Chest':                              ("#bubble trouble# in a deity's belly guards", "#bubbles# guard", 'exclude'),

    'Jabu Jabus Belly MQ First Room Side Chest':                   ("shooting a #mouth cow# reveals", None, 'exclude'),
    'Jabu Jabus Belly MQ Map Chest':                               (["#pop rocks# hide", "an #explosive palate# holds"], "a #boulder before cows# hides", 'exclude'),
    'Jabu Jabus Belly MQ Second Room Lower Chest':                 ("near a #spiked elevator# lies", None, 'exclude'),
    'Jabu Jabus Belly MQ Compass Chest':                           ("a #drowning cow# unveils", None, 'exclude'),
    'Jabu Jabus Belly MQ Second Room Upper Chest':                 ("#moving anatomy# creates a path to", None, 'exclude'),
    'Jabu Jabus Belly MQ Basement Near Switches Chest':            ("a #pair of digested cows# hold", None, 'exclude'),
    'Jabu Jabus Belly MQ Basement Near Vines Chest':               ("a #pair of digested cows# hold", None, 'exclude'),
    'Jabu Jabus Belly MQ Near Boss Chest':                         ("the #final cows' reward# in a deity's belly is", None, 'exclude'),
    'Jabu Jabus Belly MQ Falling Like Like Room Chest':            ("#cows protected by falling monsters# in a deity's belly guard", None, 'exclude'),
    'Jabu Jabus Belly MQ Boomerang Room Small Chest':              ("a school of #stingers swallowed by a deity# guard", "a school of #stingers swallowed by Jabu Jabu# guard", 'exclude'),
    'Jabu Jabus Belly MQ Boomerang Chest':                         ("a school of #stingers swallowed by a deity# guard", "a school of #stingers swallowed by Jabu Jabu# guard", 'exclude'),

    'Forest Temple First Room Chest':                              ("a #tree in the Forest Temple# supports", None, 'exclude'),
    'Forest Temple First Stalfos Chest':                           ("#defeating enemies beneath a falling ceiling# in Forest Temple yields", None, 'exclude'),
    'Forest Temple Well Chest':                                    ("a #sunken chest deep in the woods# contains", None, 'exclude'),
    'Forest Temple Map Chest':                                     ("a #fiery skull# in Forest Temple guards", None, 'exclude'),
    'Forest Temple Raised Island Courtyard Chest':                 ("a #chest on a small island# in the Forest Temple holds", None, 'exclude'),
    'Forest Temple Falling Ceiling Room Chest':                    ("beneath a #checkerboard falling ceiling# lies", None, 'exclude'),
    'Forest Temple Eye Switch Chest':                              ("a #sharp eye# will spot", "#blocks of stone# in the Forest Temple surround", 'exclude'),
    'Forest Temple Floormaster Chest':                             ("deep in the forest #shadows guard a chest# containing", None, 'exclude'),
    'Forest Temple Bow Chest':                                     ("an #army of the dead# guards", "#Stalfos deep in the Forest Temple# guard", 'exclude'),
    'Forest Temple Red Poe Chest':                                 ("#Joelle# guards", "a #red ghost# guards", 'exclude'),
    'Forest Temple Blue Poe Chest':                                ("#Beth# guards", "a #blue ghost# guards", 'exclude'),
    'Forest Temple Basement Chest':                                ("#revolving walls# in the Forest Temple conceal", None, 'exclude'),
    'Forest Temple Boss Key Chest':                                ("a #turned trunk# contains", "a #sideways chest in the Forest Temple# hides", 'exclude'),

    'Forest Temple MQ Boss Key Chest':                             ("a #turned trunk# contains", "a #sideways chest in the Forest Temple# hides", 'exclude'),
    'Forest Temple MQ First Room Chest':                           ("a #tree in the Forest Temple# supports", None, 'exclude'),
    'Forest Temple MQ Wolfos Chest':                               ("#defeating enemies beneath a falling ceiling# in Forest Temple yields", None, 'exclude'),
    'Forest Temple MQ Bow Chest':                                  ("an #army of the dead# guards", "#Stalfos deep in the Forest Temple# guard", 'exclude'),
    'Forest Temple MQ Raised Island Courtyard Lower Chest':        ("a #chest on a small island# in the Forest Temple holds", None, 'exclude'),
    'Forest Temple MQ Raised Island Courtyard Upper Chest':        ("#high in a courtyard# within the Forest Temple is", None, 'exclude'),
    'Forest Temple MQ Well Chest':                                 ("a #sunken chest deep in the woods# contains", None, 'exclude'),
    'Forest Temple MQ Map Chest':                                  ("#Joelle# guards", "a #red ghost# guards", 'exclude'),
    'Forest Temple MQ Compass Chest':                              ("#Beth# guards", "a #blue ghost# guards", 'exclude'),
    'Forest Temple MQ Falling Ceiling Room Chest':                 ("beneath a #checkerboard falling ceiling# lies", None, 'exclude'),
    'Forest Temple MQ Basement Chest':                             ("#revolving walls# in the Forest Temple conceal", None, 'exclude'),
    'Forest Temple MQ Redead Chest':                               ("deep in the forest #undead guard a chest# containing", None, 'exclude'),

    'Fire Temple Near Boss Chest':                                 ("#near a dragon# is", None, 'exclude'),
    'Fire Temple Flare Dancer Chest':                              ("the #Flare Dancer behind a totem# guards", None, 'exclude'),
    'Fire Temple Boss Key Chest':                                  ("a #prison beyond a totem# holds", None, 'exclude'),
    'Fire Temple Big Lava Room Blocked Door Chest':                ("#explosives over a lava pit# unveil", None, 'exclude'),
    'Fire Temple Big Lava Room Lower Open Door Chest':             ("a #Goron trapped near lava# holds", None, 'exclude'),
    'Fire Temple Boulder Maze Lower Chest':                        ("a #Goron at the end of a maze# holds", None, 'exclude'),
    'Fire Temple Boulder Maze Upper Chest':                        ("a #Goron above a maze# holds", None, 'exclude'),
    'Fire Temple Boulder Maze Side Room Chest':                    ("a #Goron hidden near a maze# holds", None, 'exclude'),
    'Fire Temple Boulder Maze Shortcut Chest':                     ("a #blocked path# in Fire Temple holds", None, 'exclude'),
    'Fire Temple Map Chest':                                       ("a #caged chest# in the Fire Temple hoards", None, 'exclude'),
    'Fire Temple Compass Chest':                                   ("a #chest in a fiery maze# contains", None, 'exclude'),
    'Fire Temple Highest Goron Chest':                             ("a #Goron atop the Fire Temple# holds", None, 'exclude'),

    'Fire Temple MQ Near Boss Chest':                              ("#near a dragon# is", None, 'exclude'),
    'Fire Temple MQ Megaton Hammer Chest':                         ("the #Flare Dancer in the depths of a volcano# guards", "the #Flare Dancer in the depths of the Fire Temple# guards", 'exclude'),
    'Fire Temple MQ Compass Chest':                                ("a #blocked path# in Fire Temple holds", None, 'exclude'),
    'Fire Temple MQ Lizalfos Maze Lower Chest':                    ("#crates in a maze# contain", None, 'exclude'),
    'Fire Temple MQ Lizalfos Maze Upper Chest':                    ("#crates in a maze# contain", None, 'exclude'),
    'Fire Temple MQ Map Room Side Chest':                          ("a #falling slug# in the Fire Temple guards", None, 'exclude'),
    'Fire Temple MQ Map Chest':                                    ("using a #hammer in the depths of the Fire Temple# reveals", None, 'exclude'),
    'Fire Temple MQ Boss Key Chest':                               ("#illuminating a lava pit# reveals the path to", None, 'exclude'),
    'Fire Temple MQ Big Lava Room Blocked Door Chest':             ("#explosives over a lava pit# unveil", None, 'exclude'),
    'Fire Temple MQ Lizalfos Maze Side Room Chest':                ("a #Goron hidden near a maze# holds", None, 'exclude'),
    'Fire Temple MQ Freestanding Key':                             ("hidden #beneath a block of stone# lies", None, 'exclude'),

    'Water Temple Map Chest':                                      ("#rolling spikes# in the Water Temple surround", None, 'exclude'),
    'Water Temple Compass Chest':                                  ("#roaming stingers in the Water Temple# guard", None, 'exclude'),
    'Water Temple Torches Chest':                                  ("#fire in the Water Temple# reveals", None, 'exclude'),
    'Water Temple Dragon Chest':                                   ("a #serpent's prize# in the Water Temple is", None, 'exclude'),
    'Water Temple Central Bow Target Chest':                       ("#blinding an eye# in the Water Temple leads to", None, 'exclude'),
    'Water Temple Cracked Wall Chest':                             ("#through a crack# in the Water Temple is", None, 'exclude'),
    'Water Temple Longshot Chest':                                 (["#facing yourself# reveals", "a #dark reflection# of yourself guards"], "#Dark Link# guards", 'exclude'),

    'Water Temple MQ Boss Key Chest':                              ("fire in the Water Temple unlocks a #vast gate# revealing a chest with", None, 'exclude'),
    'Water Temple MQ Longshot Chest':                              ("#through a crack# in the Water Temple is", None, 'exclude'),
    'Water Temple MQ Compass Chest':                               ("#fire in the Water Temple# reveals", None, 'exclude'),
    'Water Temple MQ Map Chest':                                   ("#sparring soldiers# in the Water Temple guard", None, 'exclude'),

    'Spirit Temple Child Bridge Chest':                            ("a child conquers a #skull in green fire# in the Spirit Temple to reach", None, 'exclude'),
    'Spirit Temple Child Early Torches Chest':                     ("a child can find a #caged chest# in the Spirit Temple with", None, 'exclude'),
    'Spirit Temple Compass Chest':                                 ("#across a pit of sand# in the Spirit Temple lies", None, 'exclude'),
    'Spirit Temple Early Adult Right Chest':                       ("#dodging boulders to collect silver rupees# in the Spirit Temple yields", None, 'exclude'),
    'Spirit Temple First Mirror Left Chest':                       ("a #shadow circling reflected light# in the Spirit Temple guards", None, 'exclude'),
    'Spirit Temple First Mirror Right Chest':                      ("a #shadow circling reflected light# in the Spirit Temple guards", None, 'exclude'),
    'Spirit Temple Map Chest':                                     ("#before a giant statue# in the Spirit Temple lies", None, 'exclude'),
    'Spirit Temple Child Climb North Chest':                       ("#lizards in the Spirit Temple# guard", None, 'exclude'),
    'Spirit Temple Child Climb East Chest':                        ("#lizards in the Spirit Temple# guard", None, 'exclude'),
    'Spirit Temple Sun Block Room Chest':                          ("#torchlight among Beamos# in the Spirit Temple reveals", None, 'exclude'),
    'Spirit Temple Statue Room Hand Chest':                        ("a #statue in the Spirit Temple# holds", None, 'exclude'),
    'Spirit Temple Statue Room Northeast Chest':                   ("on a #ledge by a statue# in the Spirit Temple rests", None, 'exclude'),
    'Spirit Temple Near Four Armos Chest':                         ("those who #show the light among statues# in the Spirit Temple find", None, 'exclude'),
    'Spirit Temple Hallway Right Invisible Chest':                 ("the #Eye of Truth in the Spirit Temple# reveals", None, 'exclude'),
    'Spirit Temple Hallway Left Invisible Chest':                  ("the #Eye of Truth in the Spirit Temple# reveals", None, 'exclude'),
    'Spirit Temple Boss Key Chest':                                ("a #chest engulfed in flame# in the Spirit Temple holds", None, 'exclude'),
    'Spirit Temple Topmost Chest':                                 ("those who #show the light above the Colossus# find", None, 'exclude'),

    'Spirit Temple MQ Entrance Front Left Chest':                  ("#lying unguarded# in the Spirit Temple is", None, 'exclude'),
    'Spirit Temple MQ Entrance Back Right Chest':                  ("a #switch in a pillar# within the Spirit Temple drops", None, 'exclude'),
    'Spirit Temple MQ Entrance Front Right Chest':                 ("#collecting rupees through a water jet# reveals", None, 'exclude'),
    'Spirit Temple MQ Entrance Back Left Chest':                   ("an #eye blinded by stone# within the Spirit Temple conceals", None, 'exclude'),
    'Spirit Temple MQ Map Chest':                                  ("surrounded by #fire and wrappings# lies", None, 'exclude'),
    'Spirit Temple MQ Map Room Enemy Chest':                       ("a child defeats a #gauntlet of monsters# within the Spirit Temple to find", None, 'exclude'),
    'Spirit Temple MQ Child Climb North Chest':                    ("#explosive sunlight# within the Spirit Temple uncovers", None, 'exclude'),
    'Spirit Temple MQ Child Climb South Chest':                    ("#trapped by falling enemies# within the Spirit Temple is", None, 'exclude'),
    'Spirit Temple MQ Compass Chest':                              ("#blinding the colossus# unveils", None, 'exclude'),
    'Spirit Temple MQ Statue Room Lullaby Chest':                  ("a #royal melody awakens the colossus# to reveal", None, 'exclude'),
    'Spirit Temple MQ Statue Room Invisible Chest':                ("the #Eye of Truth# finds the colossus's hidden", None, 'exclude'),
    'Spirit Temple MQ Silver Block Hallway Chest':                 ("#the old hide what the young find# to reveal", None, 'exclude'),
    'Spirit Temple MQ Sun Block Room Chest':                       ("#sunlight in a maze of fire# hides", None, 'exclude'),
    'Spirit Temple MQ Leever Room Chest':                          ("#across a pit of sand# in the Spirit Temple lies", None, 'exclude'),
    'Spirit Temple MQ Beamos Room Chest':                          ("where #temporal stone blocks the path# within the Spirit Temple lies", None, 'exclude'),
    'Spirit Temple MQ Chest Switch Chest':                         ("a #chest of double purpose# holds", None, 'exclude'),
    'Spirit Temple MQ Boss Key Chest':                             ("a #temporal stone blocks the light# leading to", None, 'exclude'),
    'Spirit Temple MQ Mirror Puzzle Invisible Chest':              ("those who #show the light above the Colossus# find", None, 'exclude'),

    'Shadow Temple Map Chest':                                     ("the #Eye of Truth# pierces a hall of faces to reveal", None, 'exclude'),
    'Shadow Temple Hover Boots Chest':                             ("a #nether dweller in the Shadow Temple# holds", "#Dead Hand in the Shadow Temple# holds", 'exclude'),
    'Shadow Temple Compass Chest':                                 ("#mummies revealed by the Eye of Truth# guard", None, 'exclude'),
    'Shadow Temple Early Silver Rupee Chest':                      ("#spinning scythes# protect", None, 'exclude'),
    'Shadow Temple Invisible Blades Visible Chest':                ("#invisible blades# guard", None, 'exclude'),
    'Shadow Temple Invisible Blades Invisible Chest':              ("#invisible blades# guard", None, 'exclude'),
    'Shadow Temple Falling Spikes Lower Chest':                    ("#falling spikes# block the path to", None, 'exclude'),
    'Shadow Temple Falling Spikes Upper Chest':                    ("#falling spikes# block the path to", None, 'exclude'),
    'Shadow Temple Falling Spikes Switch Chest':                   ("#falling spikes# block the path to", None, 'exclude'),
    'Shadow Temple Invisible Spikes Chest':                        ("the #dead roam among invisible spikes# guarding", None, 'exclude'),
    'Shadow Temple Wind Hint Chest':                               ("an #invisible chest guarded by the dead# holds", None, 'exclude'),
    'Shadow Temple After Wind Enemy Chest':                        ("#mummies guarding a ferry# hide", None, 'exclude'),
    'Shadow Temple After Wind Hidden Chest':                       ("#mummies guarding a ferry# hide", None, 'exclude'),
    'Shadow Temple Spike Walls Left Chest':                        ("#walls consumed by a ball of fire# reveal", None, 'exclude'),
    'Shadow Temple Invisible Floormaster Chest':                   ("shadows in an #invisible maze# guard", None, 'exclude'),
    'Shadow Temple Boss Key Chest':                                ("#walls consumed by a ball of fire# reveal", None, 'exclude'),

    'Shadow Temple MQ Compass Chest':                              ("the #Eye of Truth# pierces a hall of faces to reveal", None, 'exclude'),
    'Shadow Temple MQ Hover Boots Chest':                          ("#Dead Hand in the Shadow Temple# holds", None, 'exclude'),
    'Shadow Temple MQ Early Gibdos Chest':                         ("#mummies revealed by the Eye of Truth# guard", None, 'exclude'),
    'Shadow Temple MQ Map Chest':                                  ("#spinning scythes# protect", None, 'exclude'),
    'Shadow Temple MQ Beamos Silver Rupees Chest':                 ("#collecting rupees in a vast cavern# with the Shadow Temple unveils", None, 'exclude'),
    'Shadow Temple MQ Falling Spikes Switch Chest':                ("#falling spikes# block the path to", None, 'exclude'),
    'Shadow Temple MQ Falling Spikes Lower Chest':                 ("#falling spikes# block the path to", None, 'exclude'),
    'Shadow Temple MQ Falling Spikes Upper Chest':                 ("#falling spikes# block the path to", None, 'exclude'),
    'Shadow Temple MQ Invisible Spikes Chest':                     ("the #dead roam among invisible spikes# guarding", None, 'exclude'),
    'Shadow Temple MQ Boss Key Chest':                             ("#walls consumed by a ball of fire# reveal", None, 'exclude'),
    'Shadow Temple MQ Spike Walls Left Chest':                     ("#walls consumed by a ball of fire# reveal", None, 'exclude'),
    'Shadow Temple MQ Invisible Blades Invisible Chest':           ("#invisible blades# guard", None, 'exclude'),
    'Shadow Temple MQ Invisible Blades Visible Chest':             ("#invisible blades# guard", None, 'exclude'),
    'Shadow Temple MQ Wind Hint Chest':                            ("an #invisible chest guarded by the dead# holds", None, 'exclude'),
    'Shadow Temple MQ After Wind Hidden Chest':                    ("#mummies guarding a ferry# hide", None, 'exclude'),
    'Shadow Temple MQ After Wind Enemy Chest':                     ("#mummies guarding a ferry# hide", None, 'exclude'),
    'Shadow Temple MQ Near Ship Invisible Chest':                  ("#caged near a ship# lies", None, 'exclude'),
    'Shadow Temple MQ Freestanding Key':                           ("#behind three burning skulls# lies", None, 'exclude'),

    'Bottom of the Well Front Left Fake Wall Chest':               ("the #Eye of Truth in the well# reveals", None, 'exclude'),
    'Bottom of the Well Front Center Bombable Chest':              ("#gruesome debris# in the well hides", None, 'exclude'),
    'Bottom of the Well Right Bottom Fake Wall Chest':             ("the #Eye of Truth in the well# reveals", None, 'exclude'),
    'Bottom of the Well Compass Chest':                            ("a #hidden entrance to a cage# in the well leads to", None, 'exclude'),
    'Bottom of the Well Center Skulltula Chest':                   ("a #spider guarding a cage# in the well protects", None, 'exclude'),
    'Bottom of the Well Back Left Bombable Chest':                 ("#gruesome debris# in the well hides", None, 'exclude'),
    'Bottom of the Well Invisible Chest':                          ("#Dead Hand's invisible secret# is", None, 'exclude'),
    'Bottom of the Well Underwater Front Chest':                   ("a #royal melody in the well# uncovers", None, 'exclude'),
    'Bottom of the Well Underwater Left Chest':                    ("a #royal melody in the well# uncovers", None, 'exclude'),
    'Bottom of the Well Map Chest':                                ("in the #depths of the well# lies", None, 'exclude'),
    'Bottom of the Well Fire Keese Chest':                         ("#perilous pits# in the well guard the path to", None, 'exclude'),
    'Bottom of the Well Like Like Chest':                          ("#locked in a cage# in the well lies", None, 'exclude'),
    'Bottom of the Well Freestanding Key':                         ("#inside a coffin# hides", None, 'exclude'),
    'Bottom of the Well Lens of Truth Chest':                      (["the well's #grasping ghoul# hides", "a #nether dweller in the well# holds"], "#Dead Hand in the well# holds", 'exclude'),

    'Bottom of the Well MQ Compass Chest':                         (["the well's #grasping ghoul# hides", "a #nether dweller in the well# holds"], "#Dead Hand in the well# holds", 'exclude'),
    'Bottom of the Well MQ Map Chest':                             ("a #royal melody in the well# uncovers", None, 'exclude'),
    'Bottom of the Well MQ Lens of Truth Chest':                   ("an #army of the dead# in the well guards", None, 'exclude'),
    'Bottom of the Well MQ Dead Hand Freestanding Key':            ("#Dead Hand's explosive secret# is", None, 'exclude'),
    'Bottom of the Well MQ East Inner Room Freestanding Key':      ("an #invisible path in the well# leads to", None, 'exclude'),

    'Ice Cavern Map Chest':                                        ("#winds of ice# surround", "a chest #atop a pillar of ice# contains", 'exclude'),
    'Ice Cavern Compass Chest':                                    ("a #wall of ice# protects", None, 'exclude'),
    'Ice Cavern Freestanding PoH':                                 ("a #wall of ice# protects", None, 'exclude'),

    'Ice Cavern MQ Compass Chest':                                 ("#winds of ice# surround", None, 'exclude'),
    'Ice Cavern MQ Map Chest':                                     ("a #wall of ice# protects", None, 'exclude'),
    'Ice Cavern MQ Freestanding PoH':                              ("#winds of ice# surround", None, 'exclude'),

    'Gerudo Training Ground Lobby Left Chest':                     ("a #blinded eye in the Gerudo Training Ground# drops", None, 'exclude'),
    'Gerudo Training Ground Lobby Right Chest':                    ("a #blinded eye in the Gerudo Training Ground# drops", None, 'exclude'),
    'Gerudo Training Ground Stalfos Chest':                        ("#soldiers walking on shifting sands# in the Gerudo Training Ground guard", None, 'exclude'),
    'Gerudo Training Ground Beamos Chest':                         ("#reptilian warriors# in the Gerudo Training Ground protect", None, 'exclude'),
    'Gerudo Training Ground Hidden Ceiling Chest':                 ("the #Eye of Truth# in the Gerudo Training Ground reveals", None, 'exclude'),
    'Gerudo Training Ground Maze Path First Chest':                ("the first prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Ground Maze Path Second Chest':               ("the second prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Ground Maze Path Third Chest':                ("the third prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Ground Maze Right Central Chest':             ("the #Song of Time# in the Gerudo Training Ground leads to", None, 'exclude'),
    'Gerudo Training Ground Maze Right Side Chest':                ("the #Song of Time# in the Gerudo Training Ground leads to", None, 'exclude'),
    'Gerudo Training Ground Hammer Room Clear Chest':              ("#fiery foes# in the Gerudo Training Ground guard", None, 'exclude'),
    'Gerudo Training Ground Hammer Room Switch Chest':             ("#engulfed in flame# where thieves train lies", None, 'exclude'),
    'Gerudo Training Ground Eye Statue Chest':                     ("thieves #blind four faces# to find", None, 'exclude'),
    'Gerudo Training Ground Near Scarecrow Chest':                 ("thieves #blind four faces# to find", None, 'exclude'),
    'Gerudo Training Ground Before Heavy Block Chest':             ("#before a block of silver# thieves can find", None, 'exclude'),
    'Gerudo Training Ground Heavy Block First Chest':              ("a #feat of strength# rewards thieves with", None, 'exclude'),
    'Gerudo Training Ground Heavy Block Second Chest':             ("a #feat of strength# rewards thieves with", None, 'exclude'),
    'Gerudo Training Ground Heavy Block Third Chest':              ("a #feat of strength# rewards thieves with", None, 'exclude'),
    'Gerudo Training Ground Heavy Block Fourth Chest':             ("a #feat of strength# rewards thieves with", None, 'exclude'),
    'Gerudo Training Ground Freestanding Key':                     ("the #Song of Time# in the Gerudo Training Ground leads to", None, 'exclude'),

    'Gerudo Training Ground MQ Lobby Right Chest':                 ("#thieves prepare for training# with", None, 'exclude'),
    'Gerudo Training Ground MQ Lobby Left Chest':                  ("#thieves prepare for training# with", None, 'exclude'),
    'Gerudo Training Ground MQ First Iron Knuckle Chest':          ("#soldiers walking on shifting sands# in the Gerudo Training Ground guard", None, 'exclude'),
    'Gerudo Training Ground MQ Before Heavy Block Chest':          ("#before a block of silver# thieves can find", None, 'exclude'),
    'Gerudo Training Ground MQ Eye Statue Chest':                  ("thieves #blind four faces# to find", None, 'exclude'),
    'Gerudo Training Ground MQ Flame Circle Chest':                ("#engulfed in flame# where thieves train lies", None, 'exclude'),
    'Gerudo Training Ground MQ Second Iron Knuckle Chest':         ("#fiery foes# in the Gerudo Training Ground guard", None, 'exclude'),
    'Gerudo Training Ground MQ Dinolfos Chest':                    ("#reptilian warriors# in the Gerudo Training Ground protect", None, 'exclude'),
    'Gerudo Training Ground MQ Maze Right Central Chest':          ("a #path of fire# leads thieves to", None, 'exclude'),
    'Gerudo Training Ground MQ Maze Path First Chest':             ("the first prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Ground MQ Maze Right Side Chest':             ("a #path of fire# leads thieves to", None, 'exclude'),
    'Gerudo Training Ground MQ Maze Path Third Chest':             ("the third prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Ground MQ Maze Path Second Chest':            ("the second prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Ground MQ Hidden Ceiling Chest':              ("the #Eye of Truth# in the Gerudo Training Ground reveals", None, 'exclude'),
    'Gerudo Training Ground MQ Heavy Block Chest':                 ("a #feat of strength# rewards thieves with", None, 'exclude'),

    'Ganons Tower Boss Key Chest':                                 ("the #Evil King# hoards", None, 'exclude'),

    'Ganons Castle Forest Trial Chest':                            ("the #test of the wilds# holds", None, 'exclude'),
    'Ganons Castle Water Trial Left Chest':                        ("the #test of the seas# holds", None, 'exclude'),
    'Ganons Castle Water Trial Right Chest':                       ("the #test of the seas# holds", None, 'exclude'),
    'Ganons Castle Shadow Trial Front Chest':                      ("#music in the test of darkness# unveils", None, 'exclude'),
    'Ganons Castle Spirit Trial Crystal Switch Chest':             ("the #test of the sands# holds", None, 'exclude'),
    'Ganons Castle Spirit Trial Invisible Chest':                  ("the #test of the sands# holds", None, 'exclude'),
    'Ganons Castle Light Trial First Left Chest':                  ("the #test of radiance# holds", None, 'exclude'),
    'Ganons Castle Light Trial Second Left Chest':                 ("the #test of radiance# holds", None, 'exclude'),
    'Ganons Castle Light Trial Third Left Chest':                  ("the #test of radiance# holds", None, 'exclude'),
    'Ganons Castle Light Trial First Right Chest':                 ("the #test of radiance# holds", None, 'exclude'),
    'Ganons Castle Light Trial Second Right Chest':                ("the #test of radiance# holds", None, 'exclude'),
    'Ganons Castle Light Trial Third Right Chest':                 ("the #test of radiance# holds", None, 'exclude'),
    'Ganons Castle Light Trial Invisible Enemies Chest':           ("the #test of radiance# holds", None, 'exclude'),
    'Ganons Castle Light Trial Lullaby Chest':                     ("#music in the test of radiance# reveals", None, 'exclude'),

    'Ganons Castle MQ Water Trial Chest':                          ("the #test of the seas# holds", None, 'exclude'),
    'Ganons Castle MQ Forest Trial Eye Switch Chest':              ("the #test of the wilds# holds", None, 'exclude'),
    'Ganons Castle MQ Forest Trial Frozen Eye Switch Chest':       ("the #test of the wilds# holds", None, 'exclude'),
    'Ganons Castle MQ Light Trial Lullaby Chest':                  ("#music in the test of radiance# reveals", None, 'exclude'),
    'Ganons Castle MQ Shadow Trial Bomb Flower Chest':             ("the #test of darkness# holds", None, 'exclude'),
    'Ganons Castle MQ Spirit Trial Golden Gauntlets Chest':        ("#reflected light in the test of the sands# reveals", None, 'exclude'),
    'Ganons Castle MQ Spirit Trial Sun Back Right Chest':          ("#reflected light in the test of the sands# reveals", None, 'exclude'),
    'Ganons Castle MQ Spirit Trial Sun Back Left Chest':           ("#reflected light in the test of the sands# reveals", None, 'exclude'),
    'Ganons Castle MQ Spirit Trial Sun Front Left Chest':          ("#reflected light in the test of the sands# reveals", None, 'exclude'),
    'Ganons Castle MQ Spirit Trial First Chest':                   ("#reflected light in the test of the sands# reveals", None, 'exclude'),
    'Ganons Castle MQ Spirit Trial Invisible Chest':               ("#reflected light in the test of the sands# reveals", None, 'exclude'),
    'Ganons Castle MQ Forest Trial Freestanding Key':              ("the #test of the wilds# holds", None, 'exclude'),

    'Deku Tree Queen Gohma Heart':                                 ("the #Parasitic Armored Arachnid# holds", "#Queen Gohma# holds", 'exclude'),
    'Dodongos Cavern King Dodongo Heart':                          ("the #Infernal Dinosaur# holds", "#King Dodongo# holds", 'exclude'),
    'Jabu Jabus Belly Barinade Heart':                             ("the #Bio-Electric Anemone# holds", "#Barinade# holds", 'exclude'),
    'Forest Temple Phantom Ganon Heart':                           ("the #Evil Spirit from Beyond# holds", "#Phantom Ganon# holds", 'exclude'),
    'Fire Temple Volvagia Heart':                                  ("the #Subterranean Lava Dragon# holds", "#Volvagia# holds", 'exclude'),
    'Water Temple Morpha Heart':                                   ("the #Giant Aquatic Amoeba# holds", "#Morpha# holds", 'exclude'),
    'Spirit Temple Twinrova Heart':                                ("the #Sorceress Sisters# hold", "#Twinrova# holds", 'exclude'),
    'Shadow Temple Bongo Bongo Heart':                             ("the #Phantom Shadow Beast# holds", "#Bongo Bongo# holds", 'exclude'),

    'Queen Gohma':                                                 ("the #Parasitic Armored Arachnid# holds", "#Queen Gohma# holds", 'exclude'),
    'King Dodongo':                                                ("the #Infernal Dinosaur# holds", "#King Dodongo# holds", 'exclude'),
    'Barinade':                                                    ("the #Bio-Electric Anemone# holds", "#Barinade# holds", 'exclude'),
    'Phantom Ganon':                                               ("the #Evil Spirit from Beyond# holds", "#Phantom Ganon# holds", 'exclude'),
    'Volvagia':                                                    ("the #Subterranean Lava Dragon# holds", "#Volvagia# holds", 'exclude'),
    'Morpha':                                                      ("the #Giant Aquatic Amoeba# holds", "#Morpha# holds", 'exclude'),
    'Bongo Bongo':                                                 ("the #Sorceress Sisters# hold", "#Twinrova# holds", 'exclude'),
    'Twinrova':                                                    ("the #Phantom Shadow Beast# holds", "#Bongo Bongo# holds", 'exclude'),
    'Links Pocket':                                                ("#@'s pocket# holds", "@ already has", 'exclude'),

    'Deku Tree GS Basement Back Room':                             ("a #spider deep within the Deku Tree# hides", None, 'exclude'),
    'Deku Tree GS Basement Gate':                                  ("a #web protects a spider# within the Deku Tree holding", None, 'exclude'),
    'Deku Tree GS Basement Vines':                                 ("a #web protects a spider# within the Deku Tree holding", None, 'exclude'),
    'Deku Tree GS Compass Room':                                   ("a #spider atop the Deku Tree# holds", None, 'exclude'),

    'Deku Tree MQ GS Lobby':                                       ("a #spider in a crate# within the Deku Tree hides", None, 'exclude'),
    'Deku Tree MQ GS Compass Room':                                ("a #wall of rock protects a spider# within the Deku Tree holding", None, 'exclude'),
    'Deku Tree MQ GS Basement Back Room':                          ("a #spider deep within the Deku Tree# hides", None, 'exclude'),

    'Dodongos Cavern GS Vines Above Stairs':                       ("a #spider entangled in vines# in Dodongo's Cavern guards", None, 'exclude'),
    'Dodongos Cavern GS Scarecrow':                                ("a #spider among explosive slugs# hides", None, 'exclude'),
    'Dodongos Cavern GS Alcove Above Stairs':                      ("a #spider just out of reach# in Dodongo's Cavern holds", None, 'exclude'),
    'Dodongos Cavern GS Back Room':                                ("a #spider behind a statue# in Dodongo's Cavern holds", None, 'exclude'),
    'Dodongos Cavern GS Side Room Near Lower Lizalfos':            ("a #spider among bats# in Dodongo's Cavern holds", None, 'exclude'),

    'Dodongos Cavern MQ GS Scrub Room':                            ("a #spider high on a wall# in Dodongo's Cavern holds", None, 'exclude'),
    'Dodongos Cavern MQ GS Lizalfos Room':                         ("a #spider on top of a pillar of rock# in Dodongo's Cavern holds", None, 'exclude'),
    'Dodongos Cavern MQ GS Larvae Room':                           ("a #spider in a crate# in Dodongo's Cavern holds", None, 'exclude'),
    'Dodongos Cavern MQ GS Back Area':                             ("a #spider among graves# in Dodongo's Cavern holds", None, 'exclude'),

    'Jabu Jabus Belly GS Lobby Basement Lower':                    ("a #spider resting near a princess# in Jabu Jabu's Belly holds", None, 'exclude'),
    'Jabu Jabus Belly GS Lobby Basement Upper':                    ("a #spider resting near a princess# in Jabu Jabu's Belly holds", None, 'exclude'),
    'Jabu Jabus Belly GS Near Boss':                               ("#jellyfish surround a spider# holding", None, 'exclude'),
    'Jabu Jabus Belly GS Water Switch Room':                       ("a #spider guarded by a school of stingers# in Jabu Jabu's Belly holds", None, 'exclude'),

    'Jabu Jabus Belly MQ GS Tailpasaran Room':                     ("a #spider surrounded by electricity# in Jabu Jabu's Belly holds", None, 'exclude'),
    'Jabu Jabus Belly MQ GS Boomerang Chest Room':                 ("a #spider guarded by a school of stingers# in Jabu Jabu's Belly holds", None, 'exclude'),
    'Jabu Jabus Belly MQ GS Near Boss':                            ("a #spider in a web within Jabu Jabu's Belly# holds", None, 'exclude'),

    'Forest Temple GS Raised Island Courtyard':                    ("a #spider on a small island# in the Forest Temple holds", None, 'exclude'),
    'Forest Temple GS First Room':                                 ("a #spider high on a wall of vines# in the Forest Temple holds", None, 'exclude'),
    'Forest Temple GS Level Island Courtyard':                     ("#stone columns# lead to a spider in the Forest Temple hiding", None, 'exclude'),
    'Forest Temple GS Lobby':                                      ("a #spider among ghosts# in the Forest Temple guards", None, 'exclude'),
    'Forest Temple GS Basement':                                   ("a #spider within revolving walls# in the Forest Temple holds", None, 'exclude'),

    'Forest Temple MQ GS First Hallway':                           ("an #ivy-hidden spider# in the Forest Temple hoards", None, 'exclude'),
    'Forest Temple MQ GS Block Push Room':                         ("a #spider in a hidden nook# within the Forest Temple holds", None, 'exclude'),
    'Forest Temple MQ GS Raised Island Courtyard':                 ("a #spider on an arch# in the Forest Temple holds", None, 'exclude'),
    'Forest Temple MQ GS Level Island Courtyard':                  ("a #spider on a ledge# in the Forest Temple holds", None, 'exclude'),
    'Forest Temple MQ GS Well':                                    ("#draining a well# in Forest Temple uncovers a spider with", None, 'exclude'),

    'Fire Temple GS Song of Time Room':                            ("#eight tiles of malice# guard a spider holding", None, 'exclude'),
    'Fire Temple GS Boss Key Loop':                                ("#five tiles of malice# guard a spider holding", None, 'exclude'),
    'Fire Temple GS Boulder Maze':                                 ("#explosives in a maze# unveil a spider hiding", None, 'exclude'),
    'Fire Temple GS Scarecrow Top':                                ("a #spider-friendly scarecrow# atop a volcano hides", "a #spider-friendly scarecrow# atop the Fire Temple hides", 'exclude'),
    'Fire Temple GS Scarecrow Climb':                              ("a #spider-friendly scarecrow# atop a volcano hides", "a #spider-friendly scarecrow# atop the Fire Temple hides", 'exclude'),

    'Fire Temple MQ GS Above Flame Maze':                          ("a #spider above a fiery maze# holds", None, 'exclude'),
    'Fire Temple MQ GS Flame Maze Center':                         ("a #spider within a fiery maze# holds", None, 'exclude'),
    'Fire Temple MQ GS Big Lava Room Open Door':                   ("a #Goron trapped near lava# befriended a spider with", None, 'exclude'),
    'Fire Temple MQ GS Flame Maze Side Room':                      ("a #spider beside a fiery maze# holds", None, 'exclude'),

    'Water Temple GS Falling Platform Room':                       ("a #spider over a waterfall# in the Water Temple holds", None, 'exclude'),
    'Water Temple GS Central Pillar':                              ("a #spider in the center of the Water Temple# holds", None, 'exclude'),
    'Water Temple GS Near Boss Key Chest':                         ("a spider protected by #rolling boulders under the lake# hides", "a spider protected by #rolling boulders in the Water Temple# hides", 'exclude'),
    'Water Temple GS River':                                       ("a #spider over a river# in the Water Temple holds", None, 'exclude'),

    'Water Temple MQ GS Before Upper Water Switch':                ("#beyond a pit of lizards# is a spider holding", None, 'exclude'),
    'Water Temple MQ GS Lizalfos Hallway':                         ("#lizards guard a spider# in the Water Temple with", None, 'exclude'),
    'Water Temple MQ GS River':                                    ("a #spider over a river# in the Water Temple holds", None, 'exclude'),

    'Spirit Temple GS Hall After Sun Block Room':                  ("a spider in the #hall of a knight# guards", None, 'exclude'),
    'Spirit Temple GS Boulder Room':                               ("a #spider behind a temporal stone# in the Spirit Temple yields", None, 'exclude'),
    'Spirit Temple GS Lobby':                                      ("a #spider beside a statue# holds", None, 'exclude'),
    'Spirit Temple GS Sun on Floor Room':                          ("a #spider at the top of a deep shaft# in the Spirit Temple holds", None, 'exclude'),
    'Spirit Temple GS Metal Fence':                                ("a child defeats a #spider among bats# in the Spirit Temple to gain", None, 'exclude'),

    'Spirit Temple MQ GS Leever Room':                             ("#above a pit of sand# in the Spirit Temple hides", None, 'exclude'),
    'Spirit Temple MQ GS Nine Thrones Room West':                  ("a spider in the #hall of a knight# guards", None, 'exclude'),
    'Spirit Temple MQ GS Nine Thrones Room North':                 ("a spider in the #hall of a knight# guards", None, 'exclude'),
    'Spirit Temple MQ GS Sun Block Room':                          ("#upon a web of glass# in the Spirit Temple sits a spider holding", None, 'exclude'),

    'Shadow Temple GS Single Giant Pot':                           ("#beyond a burning skull# lies a spider with", None, 'exclude'),
    'Shadow Temple GS Falling Spikes Room':                        ("a #spider beyond falling spikes# holds", None, 'exclude'),
    'Shadow Temple GS Triple Giant Pot':                           ("#beyond three burning skulls# lies a spider with", None, 'exclude'),
    'Shadow Temple GS Invisible Blades Room':                      ("a spider guarded by #invisible blades# holds", None, 'exclude'),
    'Shadow Temple GS Near Ship':                                  ("a spider near a #docked ship# hoards", None, 'exclude'),

    'Shadow Temple MQ GS Falling Spikes Room':                     ("a #spider beyond falling spikes# holds", None, 'exclude'),
    'Shadow Temple MQ GS Wind Hint Room':                          ("a #spider amidst roaring winds# in the Shadow Temple holds", None, 'exclude'),
    'Shadow Temple MQ GS After Wind':                              ("a #spider beneath gruesome debris# in the Shadow Temple hides", None, 'exclude'),
    'Shadow Temple MQ GS After Ship':                              ("a #fallen statue# reveals a spider with", None, 'exclude'),
    'Shadow Temple MQ GS Near Boss':                               ("a #suspended spider# guards", None, 'exclude'),

    'Bottom of the Well GS Like Like Cage':                        ("a #spider locked in a cage# in the well holds", None, 'exclude'),
    'Bottom of the Well GS East Inner Room':                       ("an #invisible path in the well# leads to", None, 'exclude'),
    'Bottom of the Well GS West Inner Room':                       ("a #spider locked in a crypt# within the well guards", None, 'exclude'),

    'Bottom of the Well MQ GS Basement':                           ("a #gauntlet of invisible spiders# protects", None, 'exclude'),
    'Bottom of the Well MQ GS Coffin Room':                        ("a #spider crawling near the dead# in the well holds", None, 'exclude'),
    'Bottom of the Well MQ GS West Inner Room':                    ("a #spider locked in a crypt# within the well guards", None, 'exclude'),

    'Ice Cavern GS Push Block Room':                               ("a #spider above icy pits# holds", None, 'exclude'),
    'Ice Cavern GS Spinning Scythe Room':                          ("#spinning ice# guards a spider holding", None, 'exclude'),
    'Ice Cavern GS Heart Piece Room':                              ("a #spider behind a wall of ice# hides", None, 'exclude'),

    'Ice Cavern MQ GS Scarecrow':                                  ("a #spider above icy pits# holds", None, 'exclude'),
    'Ice Cavern MQ GS Ice Block':                                  ("a #web of ice# surrounds a spider with", None, 'exclude'),
    'Ice Cavern MQ GS Red Ice':                                    ("a #spider in fiery ice# hoards", None, 'exclude'),

    'HF GS Near Kak Grotto':                                       ("a #spider-guarded spider in a hole# hoards", None, 'exclude'),

    'LLR GS Back Wall':                                            ("night reveals a #spider in a ranch# holding", None, 'exclude'),
    'LLR GS Rain Shed':                                            ("night reveals a #spider in a ranch# holding", None, 'exclude'),
    'LLR GS House Window':                                         ("night reveals a #spider in a ranch# holding", None, 'exclude'),
    'LLR GS Tree':                                                 ("a spider hiding in a #ranch tree# holds", None, 'exclude'),

    'KF GS Bean Patch':                                            ("a #spider buried in a forest# holds", None, 'exclude'),
    'KF GS Know It All House':                                     ("night in the past reveals a #spider in a forest# holding", None, 'exclude'),
    'KF GS House of Twins':                                        ("night in the future reveals a #spider in a forest# holding", None, 'exclude'),

    'LW GS Bean Patch Near Bridge':                                ("a #spider buried deep in a forest maze# holds", None, 'exclude'),
    'LW GS Bean Patch Near Theater':                               ("a #spider buried deep in a forest maze# holds", None, 'exclude'),
    'LW GS Above Theater':                                         ("night reveals a #spider deep in a forest maze# holding", None, 'exclude'),
    'SFM GS':                                                      ("night reveals a #spider in a forest meadow# holding", None, 'exclude'),

    'OGC GS':                                                      ("a #spider outside a tyrant's tower# holds", None, 'exclude'),
    'HC GS Tree':                                                  ("a spider hiding in a #tree outside of a castle# holds", None, 'exclude'),
    'Market GS Guard House':                                       ("a #spider in a guarded crate# holds", None, 'exclude'),

    'DMC GS Bean Patch':                                           ("a #spider buried in a volcano# holds", None, 'exclude'),

    'DMT GS Bean Patch':                                           ("a #spider buried outside a cavern# holds", None, 'exclude'),
    'DMT GS Near Kak':                                             ("a #spider hidden in a mountain nook# holds", None, 'exclude'),
    'DMT GS Above Dodongos Cavern':                                ("the hammer reveals a #spider on a mountain# holding", None, 'exclude'),
    'DMT GS Falling Rocks Path':                                   ("the hammer reveals a #spider on a mountain# holding", None, 'exclude'),

    'GC GS Center Platform':                                       ("a #suspended spider# in Goron City holds", None, 'exclude'),
    'GC GS Boulder Maze':                                          ("a spider in a #Goron City crate# holds", None, 'exclude'),

    'Kak GS House Under Construction':                             ("night in the past reveals a #spider in a town# holding", None, 'exclude'),
    'Kak GS Skulltula House':                                      ("night in the past reveals a #spider in a town# holding", None, 'exclude'),
    'Kak GS Near Gate Guard':                                      ("night in the past reveals a #spider in a town# holding", None, 'exclude'),
    'Kak GS Tree':                                                 ("night in the past reveals a #spider in a town# holding", None, 'exclude'),
    'Kak GS Watchtower':                                           ("night in the past reveals a #spider in a town# holding", None, 'exclude'),
    'Kak GS Above Impas House':                                    ("night in the future reveals a #spider in a town# holding", None, 'exclude'),

    'Graveyard GS Wall':                                           ("night reveals a #spider in a graveyard# holding", None, 'exclude'),
    'Graveyard GS Bean Patch':                                     ("a #spider buried in a graveyard# holds", None, 'exclude'),

    'ZR GS Ladder':                                                ("night in the past reveals a #spider in a river# holding", None, 'exclude'),
    'ZR GS Tree':                                                  ("a spider hiding in a #tree by a river# holds", None, 'exclude'),
    'ZR GS Above Bridge':                                          ("night in the future reveals a #spider in a river# holding", None, 'exclude'),
    'ZR GS Near Raised Grottos':                                   ("night in the future reveals a #spider in a river# holding", None, 'exclude'),

    'ZD GS Frozen Waterfall':                                      ("night reveals a #spider by a frozen waterfall# holding", None, 'exclude'),
    'ZF GS Above the Log':                                         ("night reveals a #spider near a deity# holding", None, 'exclude'),
    'ZF GS Tree':                                                  ("a spider hiding in a #tree near a deity# holds", None, 'exclude'),

    'LH GS Bean Patch':                                            ("a #spider buried by a lake# holds", None, 'exclude'),
    'LH GS Small Island':                                          ("night reveals a #spider by a lake# holding", None, 'exclude'),
    'LH GS Lab Wall':                                              ("night reveals a #spider by a lake# holding", None, 'exclude'),
    'LH GS Lab Crate':                                             ("a spider deed underwater in a #lab crate# holds", None, 'exclude'),
    'LH GS Tree':                                                  ("night reveals a #spider by a lake high in a tree# holding", None, 'exclude'),

    'GV GS Bean Patch':                                            ("a #spider buried in a valley# holds", None, 'exclude'),
    'GV GS Small Bridge':                                          ("night in the past reveals a #spider in a valley# holding", None, 'exclude'),
    'GV GS Pillar':                                                ("night in the future reveals a #spider in a valley# holding", None, 'exclude'),
    'GV GS Behind Tent':                                           ("night in the future reveals a #spider in a valley# holding", None, 'exclude'),

    'GF GS Archery Range':                                         ("night reveals a #spider in a fortress# holding", None, 'exclude'),
    'GF GS Top Floor':                                             ("night reveals a #spider in a fortress# holding", None, 'exclude'),

    'Colossus GS Bean Patch':                                      ("a #spider buried in the desert# holds", None, 'exclude'),
    'Colossus GS Hill':                                            ("night reveals a #spider deep in the desert# holding", None, 'exclude'),
    'Colossus GS Tree':                                            ("night reveals a #spider deep in the desert# holding", None, 'exclude'),

    'KF Shop Item 1':                                              ("a #child shopkeeper# sells", None, 'exclude'),
    'KF Shop Item 2':                                              ("a #child shopkeeper# sells", None, 'exclude'),
    'KF Shop Item 3':                                              ("a #child shopkeeper# sells", None, 'exclude'),
    'KF Shop Item 4':                                              ("a #child shopkeeper# sells", None, 'exclude'),
    'KF Shop Item 5':                                              ("a #child shopkeeper# sells", None, 'exclude'),
    'KF Shop Item 6':                                              ("a #child shopkeeper# sells", None, 'exclude'),
    'KF Shop Item 7':                                              ("a #child shopkeeper# sells", None, 'exclude'),
    'KF Shop Item 8':                                              ("a #child shopkeeper# sells", None, 'exclude'),

    'Kak Potion Shop Item 1':                                      ("a #potion seller# offers", "the #Kakariko Potion Shop# offers", 'exclude'),
    'Kak Potion Shop Item 2':                                      ("a #potion seller# offers", "the #Kakariko Potion Shop# offers", 'exclude'),
    'Kak Potion Shop Item 3':                                      ("a #potion seller# offers", "the #Kakariko Potion Shop# offers", 'exclude'),
    'Kak Potion Shop Item 4':                                      ("a #potion seller# offers", "the #Kakariko Potion Shop# offers", 'exclude'),
    'Kak Potion Shop Item 5':                                      ("a #potion seller# offers", "the #Kakariko Potion Shop# offers", 'exclude'),
    'Kak Potion Shop Item 6':                                      ("a #potion seller# offers", "the #Kakariko Potion Shop# offers", 'exclude'),
    'Kak Potion Shop Item 7':                                      ("a #potion seller# offers", "the #Kakariko Potion Shop# offers", 'exclude'),
    'Kak Potion Shop Item 8':                                      ("a #potion seller# offers", "the #Kakariko Potion Shop# offers", 'exclude'),

    'Market Bombchu Shop Item 1':                                  ("a #Bombchu merchant# sells", None, 'exclude'),
    'Market Bombchu Shop Item 2':                                  ("a #Bombchu merchant# sells", None, 'exclude'),
    'Market Bombchu Shop Item 3':                                  ("a #Bombchu merchant# sells", None, 'exclude'),
    'Market Bombchu Shop Item 4':                                  ("a #Bombchu merchant# sells", None, 'exclude'),
    'Market Bombchu Shop Item 5':                                  ("a #Bombchu merchant# sells", None, 'exclude'),
    'Market Bombchu Shop Item 6':                                  ("a #Bombchu merchant# sells", None, 'exclude'),
    'Market Bombchu Shop Item 7':                                  ("a #Bombchu merchant# sells", None, 'exclude'),
    'Market Bombchu Shop Item 8':                                  ("a #Bombchu merchant# sells", None, 'exclude'),

    'Market Potion Shop Item 1':                                   ("a #potion seller# offers", "the #Market Potion Shop# offers", 'exclude'),
    'Market Potion Shop Item 2':                                   ("a #potion seller# offers", "the #Market Potion Shop# offers", 'exclude'),
    'Market Potion Shop Item 3':                                   ("a #potion seller# offers", "the #Market Potion Shop# offers", 'exclude'),
    'Market Potion Shop Item 4':                                   ("a #potion seller# offers", "the #Market Potion Shop# offers", 'exclude'),
    'Market Potion Shop Item 5':                                   ("a #potion seller# offers", "the #Market Potion Shop# offers", 'exclude'),
    'Market Potion Shop Item 6':                                   ("a #potion seller# offers", "the #Market Potion Shop# offers", 'exclude'),
    'Market Potion Shop Item 7':                                   ("a #potion seller# offers", "the #Market Potion Shop# offers", 'exclude'),
    'Market Potion Shop Item 8':                                   ("a #potion seller# offers", "the #Market Potion Shop# offers", 'exclude'),

    'Market Bazaar Item 1':                                        ("the #Market Bazaar# offers", None, 'exclude'),
    'Market Bazaar Item 2':                                        ("the #Market Bazaar# offers", None, 'exclude'),
    'Market Bazaar Item 3':                                        ("the #Market Bazaar# offers", None, 'exclude'),
    'Market Bazaar Item 4':                                        ("the #Market Bazaar# offers", None, 'exclude'),
    'Market Bazaar Item 5':                                        ("the #Market Bazaar# offers", None, 'exclude'),
    'Market Bazaar Item 6':                                        ("the #Market Bazaar# offers", None, 'exclude'),
    'Market Bazaar Item 7':                                        ("the #Market Bazaar# offers", None, 'exclude'),
    'Market Bazaar Item 8':                                        ("the #Market Bazaar# offers", None, 'exclude'),

    'Kak Bazaar Item 1':                                           ("the #Kakariko Bazaar# offers", None, 'exclude'),
    'Kak Bazaar Item 2':                                           ("the #Kakariko Bazaar# offers", None, 'exclude'),
    'Kak Bazaar Item 3':                                           ("the #Kakariko Bazaar# offers", None, 'exclude'),
    'Kak Bazaar Item 4':                                           ("the #Kakariko Bazaar# offers", None, 'exclude'),
    'Kak Bazaar Item 5':                                           ("the #Kakariko Bazaar# offers", None, 'exclude'),
    'Kak Bazaar Item 6':                                           ("the #Kakariko Bazaar# offers", None, 'exclude'),
    'Kak Bazaar Item 7':                                           ("the #Kakariko Bazaar# offers", None, 'exclude'),
    'Kak Bazaar Item 8':                                           ("the #Kakariko Bazaar# offers", None, 'exclude'),

    'ZD Shop Item 1':                                              ("a #Zora shopkeeper# sells", None, 'exclude'),
    'ZD Shop Item 2':                                              ("a #Zora shopkeeper# sells", None, 'exclude'),
    'ZD Shop Item 3':                                              ("a #Zora shopkeeper# sells", None, 'exclude'),
    'ZD Shop Item 4':                                              ("a #Zora shopkeeper# sells", None, 'exclude'),
    'ZD Shop Item 5':                                              ("a #Zora shopkeeper# sells", None, 'exclude'),
    'ZD Shop Item 6':                                              ("a #Zora shopkeeper# sells", None, 'exclude'),
    'ZD Shop Item 7':                                              ("a #Zora shopkeeper# sells", None, 'exclude'),
    'ZD Shop Item 8':                                              ("a #Zora shopkeeper# sells", None, 'exclude'),

    'GC Shop Item 1':                                              ("a #Goron shopkeeper# sells", None, 'exclude'),
    'GC Shop Item 2':                                              ("a #Goron shopkeeper# sells", None, 'exclude'),
    'GC Shop Item 3':                                              ("a #Goron shopkeeper# sells", None, 'exclude'),
    'GC Shop Item 4':                                              ("a #Goron shopkeeper# sells", None, 'exclude'),
    'GC Shop Item 5':                                              ("a #Goron shopkeeper# sells", None, 'exclude'),
    'GC Shop Item 6':                                              ("a #Goron shopkeeper# sells", None, 'exclude'),
    'GC Shop Item 7':                                              ("a #Goron shopkeeper# sells", None, 'exclude'),
    'GC Shop Item 8':                                              ("a #Goron shopkeeper# sells", None, 'exclude'),

    'Deku Tree MQ Deku Scrub':                                     ("a #scrub in the Deku Tree# sells", None, 'exclude'),

    'HF Deku Scrub Grotto':                                        ("a lonely #scrub in a hole# sells", None, 'exclude'),
    'LLR Deku Scrub Grotto Left':                                  ("a #trio of scrubs# sells", None, 'exclude'),
    'LLR Deku Scrub Grotto Right':                                 ("a #trio of scrubs# sells", None, 'exclude'),
    'LLR Deku Scrub Grotto Center':                                ("a #trio of scrubs# sells", None, 'exclude'),

    'LW Deku Scrub Near Deku Theater Right':                       ("a pair of #scrubs in the woods# sells", None, 'exclude'),
    'LW Deku Scrub Near Deku Theater Left':                        ("a pair of #scrubs in the woods# sells", None, 'exclude'),
    'LW Deku Scrub Near Bridge':                                   ("a #scrub by a bridge# sells", None, 'exclude'),
    'LW Deku Scrub Grotto Rear':                                   ("a #scrub underground duo# sells", None, 'exclude'),
    'LW Deku Scrub Grotto Front':                                  ("a #scrub underground duo# sells", None, 'exclude'),

    'SFM Deku Scrub Grotto Rear':                                  ("a #scrub underground duo# sells", None, 'exclude'),
    'SFM Deku Scrub Grotto Front':                                 ("a #scrub underground duo# sells", None, 'exclude'),

    'GC Deku Scrub Grotto Left':                                   ("a #trio of scrubs# sells", None, 'exclude'),
    'GC Deku Scrub Grotto Right':                                  ("a #trio of scrubs# sells", None, 'exclude'),
    'GC Deku Scrub Grotto Center':                                 ("a #trio of scrubs# sells", None, 'exclude'),

    'Dodongos Cavern Deku Scrub Near Bomb Bag Left':               ("a pair of #scrubs in Dodongo's Cavern# sells", None, 'exclude'),
    'Dodongos Cavern Deku Scrub Side Room Near Dodongos':          ("a #scrub guarded by Lizalfos# sells", None, 'exclude'),
    'Dodongos Cavern Deku Scrub Near Bomb Bag Right':              ("a pair of #scrubs in Dodongo's Cavern# sells", None, 'exclude'),
    'Dodongos Cavern Deku Scrub Lobby':                            ("a #scrub in Dodongo's Cavern# sells", None, 'exclude'),

    'Dodongos Cavern MQ Deku Scrub Lobby Rear':                    ("a pair of #scrubs in Dodongo's Cavern# sells", None, 'exclude'),
    'Dodongos Cavern MQ Deku Scrub Lobby Front':                   ("a pair of #scrubs in Dodongo's Cavern# sells", None, 'exclude'),
    'Dodongos Cavern MQ Deku Scrub Staircase':                     ("a #scrub in Dodongo's Cavern# sells", None, 'exclude'),
    'Dodongos Cavern MQ Deku Scrub Side Room Near Lower Lizalfos': ("a #scrub guarded by Lizalfos# sells", None, 'exclude'),

    'DMC Deku Scrub Grotto Left':                                  ("a #trio of scrubs# sells", None, 'exclude'),
    'DMC Deku Scrub Grotto Right':                                 ("a #trio of scrubs# sells", None, 'exclude'),
    'DMC Deku Scrub Grotto Center':                                ("a #trio of scrubs# sells", None, 'exclude'),

    'ZR Deku Scrub Grotto Rear':                                   ("a #scrub underground duo# sells", None, 'exclude'),
    'ZR Deku Scrub Grotto Front':                                  ("a #scrub underground duo# sells", None, 'exclude'),

    'Jabu Jabus Belly Deku Scrub':                                 ("a #scrub in a deity# sells", None, 'exclude'),

    'LH Deku Scrub Grotto Left':                                   ("a #trio of scrubs# sells", None, 'exclude'),
    'LH Deku Scrub Grotto Right':                                  ("a #trio of scrubs# sells", None, 'exclude'),
    'LH Deku Scrub Grotto Center':                                 ("a #trio of scrubs# sells", None, 'exclude'),

    'GV Deku Scrub Grotto Rear':                                   ("a #scrub underground duo# sells", None, 'exclude'),
    'GV Deku Scrub Grotto Front':                                  ("a #scrub underground duo# sells", None, 'exclude'),

    'Colossus Deku Scrub Grotto Front':                            ("a #scrub underground duo# sells", None, 'exclude'),
    'Colossus Deku Scrub Grotto Rear':                             ("a #scrub underground duo# sells", None, 'exclude'),

    'Ganons Castle Deku Scrub Center-Left':                        ("#scrubs in Ganon's Castle# sell", None, 'exclude'),
    'Ganons Castle Deku Scrub Center-Right':                       ("#scrubs in Ganon's Castle# sell", None, 'exclude'),
    'Ganons Castle Deku Scrub Right':                              ("#scrubs in Ganon's Castle# sell", None, 'exclude'),
    'Ganons Castle Deku Scrub Left':                               ("#scrubs in Ganon's Castle# sell", None, 'exclude'),

    'Ganons Castle MQ Deku Scrub Right':                           ("#scrubs in Ganon's Castle# sell", None, 'exclude'),
    'Ganons Castle MQ Deku Scrub Center-Left':                     ("#scrubs in Ganon's Castle# sell", None, 'exclude'),
    'Ganons Castle MQ Deku Scrub Center':                          ("#scrubs in Ganon's Castle# sell", None, 'exclude'),
    'Ganons Castle MQ Deku Scrub Center-Right':                    ("#scrubs in Ganon's Castle# sell", None, 'exclude'),
    'Ganons Castle MQ Deku Scrub Left':                            ("#scrubs in Ganon's Castle# sell", None, 'exclude'),

    'LLR Stables Left Cow':                                        ("a #cow in a stable# gifts", None, 'exclude'),
    'LLR Stables Right Cow':                                       ("a #cow in a stable# gifts", None, 'exclude'),
    'LLR Tower Right Cow':                                         ("a #cow in a ranch silo# gifts", None, 'exclude'),
    'LLR Tower Left Cow':                                          ("a #cow in a ranch silo# gifts", None, 'exclude'),
    'Kak Impas House Cow':                                         ("a #cow imprisoned in a house# protects", None, 'exclude'),
    'DMT Cow Grotto Cow':                                          ("a #cow in a luxurious hole# offers", None, 'exclude'),

    'Desert Colossus -> Colossus Grotto':                       ("lifting a #rock in the desert# reveals", None, 'entrance'),
    'GV Grotto Ledge -> GV Octorok Grotto':                     ("a rock on #a ledge in the valley# hides", None, 'entrance'),
    'GC Grotto Platform -> GC Grotto':                          ("a #pool of lava# in Goron City blocks the way to", None, 'entrance'),
    'GF Entrances Behind Crates -> GF Storms Grotto':           ("a #storm within Gerudo's Fortress# reveals", None, 'entrance'),
    'Zoras Domain -> ZD Storms Grotto':                         ("a #storm within Zora's Domain# reveals", None, 'entrance'),
    'Hyrule Castle Grounds -> HC Storms Grotto':                ("a #storm near the castle# reveals", None, 'entrance'),
    'GV Fortress Side -> GV Storms Grotto':                     ("a #storm in the valley# reveals", None, 'entrance'),
    'Desert Colossus -> Colossus Great Fairy Fountain':         ("a #fractured desert wall# hides", None, 'entrance'),
    'Ganons Castle Grounds -> OGC Great Fairy Fountain':        ("a #heavy pillar# outside the castle obstructs", None, 'entrance'),
    'Zoras Fountain -> ZF Great Fairy Fountain':                ("a #fountain wall# hides", None, 'entrance'),
    'GV Fortress Side -> GV Carpenter Tent':                    ("a #tent in the valley# covers", None, 'entrance'),
    'Graveyard Warp Pad Region -> Shadow Temple Entryway':      ("at the #back of the Graveyard#, there is", None, 'entrance'),
    'Lake Hylia -> Water Temple Lobby':                         ("deep #under a vast lake#, one can find", None, 'entrance'),
    'Gerudo Fortress -> Gerudo Training Ground Lobby':          ("paying a #fee to the Gerudos# grants access to", None, 'entrance'),
    'Zoras Fountain -> Jabu Jabus Belly Beginning':             ("inside #Jabu Jabu#, one can find", None, 'entrance'),
    'Kakariko Village -> Bottom of the Well':                   ("a #village well# leads to", None, 'entrance'),

    'Ganons Castle Grounds -> Ganons Castle Lobby':             ("the #rainbow bridge# leads to", None, 'entrance'),

    'KF Links House':                                           ("Link's House", None, 'region'),
    'Temple of Time':                                           ("the #Temple of Time#", None, 'region'),
    'KF Midos House':                                           ("Mido's house", None, 'region'),
    'KF Sarias House':                                          ("Saria's House", None, 'region'),
    'KF House of Twins':                                        ("the #House of Twins#", None, 'region'),
    'KF Know It All House':                                     ("Know-It-All Brothers' House", None, 'region'),
    'KF Kokiri Shop':                                           ("the #Kokiri Shop#", None, 'region'),
    'LH Lab':                                                   ("the #Lakeside Laboratory#", None, 'region'),
    'LH Fishing Hole':                                          ("the #Fishing Pond#", None, 'region'),
    'GV Carpenter Tent':                                        ("the #Carpenters' tent#", None, 'region'),
    'Market Guard House':                                       ("the #Guard House#", None, 'region'),
    'Market Mask Shop':                                         ("the #Happy Mask Shop#", None, 'region'),
    'Market Bombchu Bowling':                                   ("the #Bombchu Bowling Alley#", None, 'region'),
    'Market Potion Shop':                                       ("the #Market Potion Shop#", None, 'region'),
    'Market Treasure Chest Game':                               ("the #Treasure Box Shop#", None, 'region'),
    'Market Bombchu Shop':                                      ("the #Bombchu Shop#", None, 'region'),
    'Market Man in Green House':                                ("Man in Green's House", None, 'region'),
    'Kak Windmill':                                             ("the #Windmill#", None, 'region'),
    'Kak Carpenter Boss House':                                 ("the #Carpenters' Boss House#", None, 'region'),
    'Kak House of Skulltula':                                   ("the #House of Skulltula#", None, 'region'),
    'Kak Impas House':                                          ("Impa's House", None, 'region'),
    'Kak Impas House Back':                                     ("Impa's cow cage", None, 'region'),
    'Kak Odd Medicine Building':                                ("Granny's Potion Shop", None, 'region'),
    'Graveyard Dampes House':                                   ("Dampé's Hut", None, 'region'),
    'GC Shop':                                                  ("the #Goron Shop#", None, 'region'),
    'ZD Shop':                                                  ("the #Zora Shop#", None, 'region'),
    'LLR Talons House':                                         ("Talon's House", None, 'region'),
    'LLR Stables':                                              ("a #stable#", None, 'region'),
    'LLR Tower':                                                ("the #Lon Lon Tower#", None, 'region'),
    'Market Bazaar':                                            ("the #Market Bazaar#", None, 'region'),
    'Market Shooting Gallery':                                  ("a #Slingshot Shooting Gallery#", None, 'region'),
    'Kak Bazaar':                                               ("the #Kakariko Bazaar#", None, 'region'),
    'Kak Potion Shop Front':                                    ("the #Kakariko Potion Shop#", None, 'region'),
    'Kak Potion Shop Back':                                     ("the #Kakariko Potion Shop#", None, 'region'),
    'Kak Shooting Gallery':                                     ("a #Bow Shooting Gallery#", None, 'region'),
    'Colossus Great Fairy Fountain':                            ("a #Great Fairy Fountain#", None, 'region'),
    'HC Great Fairy Fountain':                                  ("a #Great Fairy Fountain#", None, 'region'),
    'OGC Great Fairy Fountain':                                 ("a #Great Fairy Fountain#", None, 'region'),
    'DMC Great Fairy Fountain':                                 ("a #Great Fairy Fountain#", None, 'region'),
    'DMT Great Fairy Fountain':                                 ("a #Great Fairy Fountain#", None, 'region'),
    'ZF Great Fairy Fountain':                                  ("a #Great Fairy Fountain#", None, 'region'),
    'Graveyard Shield Grave':                                   ("a #grave with a free chest#", None, 'region'),
    'Graveyard Heart Piece Grave':                              ("a chest spawned by #Sun's Song#", None, 'region'),
    'Graveyard Royal Familys Tomb':                             ("the #Royal Family's Tomb#", None, 'region'),
    'Graveyard Dampes Grave':                                   ("Dampé's Grave", None, 'region'),
    'DMT Cow Grotto':                                           ("a solitary #Cow#", None, 'region'),
    'HC Storms Grotto':                                         ("a sandy grotto with #fragile walls#", None, 'region'),
    'HF Tektite Grotto':                                        ("a pool guarded by a #Tektite#", None, 'region'),
    'HF Near Kak Grotto':                                       ("a #Big Skulltula# guarding a Gold one", None, 'region'),
    'HF Cow Grotto':                                            ("a grotto full of #spider webs#", None, 'region'),
    'Kak Redead Grotto':                                        ("#ReDeads# guarding a chest", None, 'region'),
    'SFM Wolfos Grotto':                                        ("#Wolfos# guarding a chest", None, 'region'),
    'GV Octorok Grotto':                                        ("an #Octorok# guarding a rich pool", None, 'region'),
    'Deku Theater':                                             ("the #Lost Woods Stage#", None, 'region'),
    'ZR Open Grotto':                                           ("a #generic grotto#", None, 'region'),
    'DMC Upper Grotto':                                         ("a #generic grotto#", None, 'region'),
    'DMT Storms Grotto':                                        ("a #generic grotto#", None, 'region'),
    'Kak Open Grotto':                                          ("a #generic grotto#", None, 'region'),
    'HF Near Market Grotto':                                    ("a #generic grotto#", None, 'region'),
    'HF Open Grotto':                                           ("a #generic grotto#", None, 'region'),
    'HF Southeast Grotto':                                      ("a #generic grotto#", None, 'region'),
    'KF Storms Grotto':                                         ("a #generic grotto#", None, 'region'),
    'LW Near Shortcuts Grotto':                                 ("a #generic grotto#", None, 'region'),
    'HF Inside Fence Grotto':                                   ("a #single Upgrade Deku Scrub#", None, 'region'),
    'LW Scrubs Grotto':                                         ("#2 Deku Scrubs# including an Upgrade one", None, 'region'),
    'Colossus Grotto':                                          ("2 Deku Scrubs", None, 'region'),
    'ZR Storms Grotto':                                         ("2 Deku Scrubs", None, 'region'),
    'SFM Storms Grotto':                                        ("2 Deku Scrubs", None, 'region'),
    'GV Storms Grotto':                                         ("2 Deku Scrubs", None, 'region'),
    'LH Grotto':                                                ("3 Deku Scrubs", None, 'region'),
    'DMC Hammer Grotto':                                        ("3 Deku Scrubs", None, 'region'),
    'GC Grotto':                                                ("3 Deku Scrubs", None, 'region'),
    'LLR Grotto':                                               ("3 Deku Scrubs", None, 'region'),
    'ZR Fairy Grotto':                                          ("a small #Fairy Fountain#", None, 'region'),
    'HF Fairy Grotto':                                          ("a small #Fairy Fountain#", None, 'region'),
    'SFM Fairy Grotto':                                         ("a small #Fairy Fountain#", None, 'region'),
    'ZD Storms Grotto':                                         ("a small #Fairy Fountain#", None, 'region'),
    'GF Storms Grotto':                                         ("a small #Fairy Fountain#", None, 'region'),

    # Junk hints must satisfy all of the following conditions:
    # - They aren't inappropriate.
    # - They aren't absurdly long copy pastas.
    # - They aren't quotes or references that are simply not funny when out-of-context.
    # To elaborate on this last point: junk hints need to be able to be understood 
    # by everyone, and not just those who get the obscure references.
    # Zelda references are considered fair game.

    # First generation junk hints
    '1002':                                                     ("${12 68 79}They say that monarchy is a terrible system of governance.", None, 'junk'), # sfx: Zelda gasp
    '1003':                                                     ("${12 68 79}They say that Zelda is a poor leader.", None, 'junk'), # sfx: Zelda gasp
    '1004':                                                     ("These hints can be quite useful. This is an exception.", None, 'junk'),
    '1006':                                                     ("They say that all the Zora drowned in Wind Waker.", None, 'junk'),
    '1008':                                                     ("Remember when Ganon was a blue pig?^I remember.", None, 'junk'), # ref: A Link to the Past
    '1009':                                                     ("One who does not have Triforce can't go in.", None, 'junk'),
    '1010':                                                     ("Save your future, end the Happy Mask Salesman.", None, 'junk'),
    '1012':                                                     ("I'm stoned. Get it?", None, 'junk'),
    '1013':                                                     ("Hoot! Hoot! Would you like me to repeat that?", None, 'junk'), # ref: Kaepora Gaebora (the owl)
    '1014':                                                     ("Gorons are stupid. They eat rocks. Except, apparently, the big rock blocking Dodongo's Cavern.", None, 'junk'),
    '1015':                                                     ("They say that Lon Lon Ranch prospered under Ingo.", None, 'junk'),
    '1017':                                                     ("Without the Lens of Truth, the Treasure Chest Mini-Game is a 1 out of 32 chance.^Good luck!", None, 'junk'),
    '1018':                                                     ("Use bombs wisely.", None, 'junk'),
    '1022':                                                     ("You're comparing yourself to me?^Ha! You're not even good enough to be my fake.", None, 'junk'), # ref: SA2
    '1024':                                                     ("What happened to Sheik?", None, 'junk'),
    '1026':                                                     ("I've heard Sploosh Kaboom is a tricky game.", None, 'junk'), # ref: Wind Waker
    '1028':                                                     ("I bet you'd like to have more bombs.", None, 'junk'),
    '1029':                                                     ("When all else fails, use Fire.", None, 'junk'),
    # '1030':                                                     ("Here's a hint, @. Don't be bad.", None, 'junk'),
    '1031':                                                     ("Game Over. Return of Ganon.", None, 'junk'), # ref: Zelda II
    '1032':                                                     ("May the way of the Hero lead to the Triforce.", None, 'junk'),
    '1033':                                                     ("Can't find an item? Scan an Amiibo.", None, 'junk'),
    '1034':                                                     ("They say this game has just a few glitches.", None, 'junk'),
    '1035':                                                     ("BRRING BRRING This is Ulrira. Wrong number?", None, 'junk'), # ref: Link's Awakening
    '1036':                                                     ("Tingle Tingle Kooloo Limpah", None, 'junk'), # ref: Majora's Mask
    '1038':                                                     ("They say that Ganondorf will appear in the next Mario Tennis.", None, 'junk'),
    '1039':                                                     ("Medigoron sells the earliest Breath of the Wild demo.", None, 'junk'),
    '1041':                                                     ("You were almost a @ sandwich.", None, 'junk'),
    '1042':                                                     ("I'm a helpful hint Gossip Stone!^See, I'm helping.", None, 'junk'),
    '1043':                                                     ("Dear @, please come to the castle. I've baked a cake for you.&Yours truly, princess Zelda.", None, 'junk'), # ref: Super Mario 64
    '1044':                                                     ("They say all toasters toast toast.", None, 'junk'), # ref: Hotel Mario
    '1045':                                                     ("They say that Okami is the best Zelda game.", None, 'junk'), # ref: people often say that Okami feels and plays like a Zelda game
    '1046':                                                     ("They say that quest guidance can be found at a talking rock.", None, 'junk'),
    # '1047':                                                     ("They say that the final item you're looking for can be found somewhere in Hyrule.", None, 'junk'),
    '1048':                                                     ("${12 68 7a}Mweep${07 04 51}", None, 'junk'), # Mweep
    '1049':                                                     ("They say that Barinade fears Deku Nuts.", None, 'junk'),
    '1050':                                                     ("They say that Flare Dancers do not fear Goron-crafted blades.", None, 'junk'), 
    '1051':                                                     ("They say that Morpha is easily trapped in a corner.", None, 'junk'),
    '1052':                                                     ("They say that Bongo Bongo really hates the cold.", None, 'junk'),
    '1053':                                                     ("They say that crouch stabs mimic the effects of your last attack.", None, 'junk'),
    '1054':                                                     ("They say that bombing the hole Volvagia last flew into can be rewarding.", None, 'junk'),
    '1055':                                                     ("They say that invisible ghosts can be exposed with Deku Nuts.", None, 'junk'),
    '1056':                                                     ("They say that the real Phantom Ganon is bright and loud.", None, 'junk'),
    '1057':                                                     ("They say that the fastest way forward is walking backwards.", None, 'junk'),
    '1058':                                                     ("They say that leaping above the Market entrance enriches most children.", None, 'junk'),
    '1059':                                                     ("They say that looking into darkness may find darkness looking back into you.", None, 'junk'), # ref: Nietzsche
    '1060':                                                     ("You found a spiritual Stone! By which I mean, I worship Nayru.", None, 'junk'),
    '1061':                                                     ("A broken stick is just as good as a Master Sword. Who knew?", None, 'junk'),
    '1062':                                                     ("Open your eyes.^Open your eyes.^Wake up, @.", None, 'junk'), # ref: Breath of the Wild
    '1063':                                                     ("They say that arbitrary code execution leads to the credits sequence.", None, 'junk'),
    '1064':                                                     ("They say that Twinrova always casts the same spell the first three times.", None, 'junk'),
    # '1065':                                                     ("They say that the Development branch may be unstable.", None, 'junk'),
    '1066':                                                     ("You're playing a Randomizer. I'm randomized!^${12 48 31}Here's a random number:  #4#.&Enjoy your Randomizer!", None, 'junk'), # ref: xkcd comic / sfx: get small item from chest
    '1067':                                                     ("They say Ganondorf's bolts can be reflected with glass or steel.", None, 'junk'),
    '1068':                                                     ("They say Ganon's tail is vulnerable to nuts, arrows, swords, explosives, hammers...^...sticks, seeds, boomerangs...^...rods, shovels, iron balls, angry bees...", None, 'junk'), # ref: various Zelda games
    '1069':                                                     ("They say that you're wasting time reading this hint, but I disagree. Talk to me again!", None, 'junk'),
    '1070':                                                     ("They say Ganondorf knows where to find the instrument of his doom.", None, 'junk'),
    '1071':                                                     ("I heard @ is pretty good at Zelda.", None, 'junk'),

    # Second generation junk hints
    '1072':                                                     ("Fingers-Mazda, the first thief in the world, stole fire from the gods.^But he was unable to fence it.&It was too hot.&He got really burned on that deal.", None, 'junk'), # ref: Discworld
    '1073':                                                     ("Boing-oing!^There are times in life when one should seek the help of others...^Thus, when standing alone fails to help, stand together.", None, 'junk'), # ref: Gossip Stone in Phantom Hourglass
    '1074':                                                     ("They say that if you don't use your slingshot at all when you play the slingshot minigame, the owner gets upset with you.", None, 'junk'),
    '1075':                                                     ("Hey! Wait! Don't go out! It's unsafe!^Wild Pokémon live in tall grass!^You need your own Pokémon for your protection.", None, 'junk'), # ref: Pokémon
    '1076':                                                     ("They say it's 106 miles to Hyrule Castle, we have half a bar of magic, it's dark, and we're wearing sunglasses.", None, 'junk'), # ref: Blues Brothers
    '1078':                                                     ("It would be a shame if something... unfortunate... were to happen to you.^Have you considered saving lately?", None, 'junk'), # ref: meme
    '1079':                                                     ("They say that something wonderful happens when playing the Song of Storms after planting a magic bean.", None, 'junk'),
    '1080':                                                     ("Long time watcher, first time player. Greetings from Termina. Incentive goes to Randobot's choice.", None, 'junk'), # ref: GDQ meme
    '1081':                                                     ("No matter what happens...Do not give up, do not complain, and do NOT stay up all night playing!", None, 'junk'), # ref: Wind Waker
    '1082':                                                     ("That's a nice wall you got there. Would be a shame if I just... clipped right through that.", None, 'junk'),
    '1083':                                                     ("Ganondorf used to be an adventurer like me, but then he took a light arrow to the knee.", None, 'junk'), # ref: Skyrim
    '1084':                                                     ("They say that the easiest way to kill Peahats is using Din's Fire while they're grounded.", None, 'junk'),
    '1085':                                                     ("They say that the castle guards' routes have major security vulnerabilities.", None, 'junk'),
    '1086':                                                     ("They say that Epona is an exceptional horse. Able to clear canyons in a single bound.", None, 'junk'),
    '1087':                                                     ("They say only one heart piece in all of Hyrule will declare the holder a winner.", None, 'junk'),
    # '1088':                                                     ("Are you stuck? Try asking for help in our Discord server or check out our Wiki!", None, 'junk'),
    '1089':                                                     ("You would be surprised at all the things you can Hookshot in the Spirit Temple!", None, 'junk'),
    '1090':                                                     ("I once glued a set of false teeth to the Boomerang.^${12 39 c7}That came back to bite me.", None, 'junk'), # sfx: Ganondorf laugh
    '1091':                                                     ("They say that most of the water in Hyrule flows through King Zora's buttocks.", None, 'junk'),
    '1092':                                                     ("Space, space, wanna go to space, yes, please space. Space space. Go to space.", None, 'junk'), # ref: Portal 2
    '1093':                                                     ("They say that you must read the names of \"Special Deal\" items in shops carefully.", None, 'junk'),
    '1094':                                                     ("Did you know that the Boomerang instantly stuns Phantom Ganon's second form?", None, 'junk'),
    '1095':                                                     ("I came here to chew bubblegum and play rando. And I'm all out of bubblegum.", None, 'junk'), # ref: They Live
    '1096':                                                     ("Did you know that Stalchildren leave you alone when wearing the Bunny Hood?", None, 'junk'),
    '1097':                                                     ("This Gossip Stone Is Dedicated to Those Who Perished Before Ganon Was Defeated.", None, 'junk'),
    '1098':                                                     ("Did you know that Blue Fire destroys mud walls and detonates Bomb Flowers?", None, 'junk'),
    '1099':                                                     ("Are you sure you want to play this? Wanna go get some tacos or something?", None, 'junk'),
    '1100':                                                     ("What did Zelda suggest that Link do when diplomacy didn't work?^${12 39 C7}Triforce.", None, 'junk'), # sfx: Ganondorf laugh
    '1101':                                                     ("They say that bombing the hole Volvagia last flew into can be rewarding.", None, 'junk'),
    '1102':                                                     ("Hi @, we've been trying to reach you about your horse's extended warranty.", None, 'junk'),
    '1103':                                                     ("Ganondorf brushes his rotten teeth with salted slug flavoured tooth paste!", None, 'junk'), # ref: Banjo Kazooie
    '1104':                                                     ("I'm Commander Shepard, and this is my favorite Gossip Stone in Hyrule!", None, 'junk'), # ref: Mass Effect
    '1105':                                                     ("They say that tossing a bomb will cause a Blue Bubble to go after it.", None, 'junk'),
    '1106':                                                     ("They say that the Lizalfos in Dodongo's Cavern like to play in lava.", None, 'junk'),
    '1107':                                                     ("Why won't anyone acknowledge the housing crisis in Kakariko Village?", None, 'junk'),
    '1108':                                                     ("Don't believe in yourself. Believe in the me that believes in you!", None, 'junk'), # ref: Anime
    '1109':                                                     ("This is a haiku&Five syllables then seven&Five more to finish", None, 'junk'),
    '1110':                                                     ("They say that beating Bongo Bongo quickly requires an even tempo.", None, 'junk'),
    '1111':                                                     ("Did you know that you can tune a piano but you can't tune a fish?", None, 'junk'), # Studio Album by REO Speedwagon
    '1112':                                                     ("You thought it would be a useful hint, but it was me, Junk Hint!", None, 'junk'), # ref: Jojo's Bizarre Adventure
    '1113':                                                     ("They say you can cut corners to get to your destination faster.", None, 'junk'),
    '1114':                                                     ("Three things are certain: death, taxes, and forgetting a check.", None, 'junk'), # ref: Benjamin Franklin, allegedly
    '1115':                                                     ("Have you thought about going where the items are?^Just saying.", None, 'junk'),
    '1116':                                                     ("They say that the true reward is the friends we made along the way.", None, 'junk'), # ref: common meme with unknown origins
    '1117':                                                     ("Gossip Stone Shuffle must be on. I'm normally in Zora's Domain!", None, 'junk'),
    '1118':                                                     ("When ASM is used to code a randomizer they should call it ASMR.", None, 'junk'),
    '1119':                                                     ("It's so lonely being stuck here with nobody else to talk to...", None, 'junk'),
    '1120':                                                     ("Why are they called Wallmasters if they come from the ceiling?", None, 'junk'),
    '1121':                                                     ("They say that Zelda's Lullaby can be used to repair broken signs.", None, 'junk'),
    '1122':                                                     ("Fell for it, didn't you, fool? Junk hint cross split attack!", None, 'junk'), # ref: Jojo's Bizarre Adventure
    '1123':                                                     ("Please don't abandon this seed. Our world deserves saving!", None, 'junk'),
    '1124':                                                     ("I wanna be a rocketship, @! Please help me live my dreams!", None, 'junk'),
    '1125':                                                     ("They say that King Zora needs to build a taller fence.", None, 'junk'),
    '1126':                                                     ("They say Goron fabrics protect against more than fire.", None, 'junk'),
    '1127':                                                     ("Did you know that ReDead mourn their defeated friends?", None, 'junk'),
    '1128':                                                     ("Did you know that ReDead eat their defeated friends?", None, 'junk'),
    '1129':                                                     ("What is a Hylian? A miserable little pile of secrets!", None, 'junk'), # ref: Castlevania
    '1130':                                                     ("The hint stone you have dialed&has been disconnected.", None, 'junk'), # ref: telephone error message
    '1131':                                                     ("We don't make mistakes, we have happy accidents.", None, 'junk'), # ref: Bob Ross
    '1132':                                                     ("I've heard Ganon dislikes lemon-flavored popsicles.", None, 'junk'),
    '1133':                                                     ("If Gorons eat rocks, does that mean I'm in danger?", None, 'junk'),
    '1134':                                                     ("They say Ingo is not very good at planning ahead.", None, 'junk'),
    '1136':                                                     ("They say that Anju needs to stop losing her chickens.", None, 'junk'),
    '1137':                                                     ("Can you move me? I don't get great service here.", None, 'junk'),
    '1138':                                                     ("Have you embraced the power of the Deku Nut yet?", None, 'junk'),
    '1139':                                                     ("They say that Mido is easily confused by sick flips.", None, 'junk'), # ref: Mido Skip
    '1140':                                                     ("They say that the path to Termina is a one-way trip.", None, 'junk'), # ref: Majora's Mask
    '1141':                                                     ("They say that @ deserves a hug. Everyone does!", None, 'junk'),
    '1142':                                                     ("I hear Termina is a great spot for a vacation!", None, 'junk'), # ref: Majora's Mask
    '1144':                                                     ("You've met with a terrible fate, haven't you?", None, 'junk'), # ref: Majora's Mask
    '1145':                                                     ("Try using various items and weapons on me :)", None, 'junk'),
    '1146':                                                     ("On second thought, let's not go to Hyrule Castle. 'Tis a silly place.", None, 'junk'), # ref: Monty Python
    '1147':                                                     ("If you see something suspicious, bomb it!", None, 'junk'),
    '1148':                                                     ("Don't forget to write down your hints :)", None, 'junk'),
    '1149':                                                     ("Would you kindly...&close this textbox?", None, 'junk'), # ref: Bioshock
    '1150':                                                     ("They say that King Dodongo dislikes smoke.", None, 'junk'), # ref: Zelda 1
    '1151':                                                     ("Never give up. Trust your instincts!", None, 'junk'), # ref: Star Fox 64
    '1152':                                                     ("I love to gossip! Wanna be friends?", None, 'junk'),
    '1153':                                                     ("This isn't where I parked my horse!", None, 'junk'), # ref: EuroTrip
    '1156':                                                     ("Anything not saved will be lost.", None, 'junk'), # ref: Nintendo (various games and platforms)
    '1157':                                                     ("I was voted least helpful hint stone five years in a row!", None, 'junk'),
    '1158':                                                     ("They say that the Groose is loose.", None, 'junk'), # ref: Skyward Sword
    '1159':                                                     ("Twenty-three is number one!^And thirty-one is number two!", None, 'junk'), # ref: Deku Scrubs in Deku Tree
    '1160':                                                     ("Ya ha ha! You found me!", None, 'junk'), # ref: Breath of the Wild
    '1161':                                                     ("Do you like Like Likes?", None, 'junk'),
    '1162':                                                     ("Next you'll say:^\"Why am I still reading these?\"", None, 'junk'), # ref: Jojo's Bizarre Adventure
    '1165':                                                     ("You're a cool cat, @.", None, 'junk'),
    '1167':                                                     ("This hint is in another castle.", None, 'junk'), # ref: Mario
    '1169':                                                     ("Hydrate!", None, 'junk'),
    '1170':                                                     ("They say that there is an alcove with a Recovery Heart behind the lava wall in Dodongo's Cavern.", None, 'junk'),
    '1171':                                                     ("Having regrets? Reset without saving!", None, 'junk'),
    '1172':                                                     ("Did you know that Gorons understood SRM long before speedrunners did?", None, 'junk'), # ref: Goron City murals
    # '1173':                                                     ("Did you know that the Discord server has a public Plandomizer library?", None, 'junk'),
    '1174':                                                     ("${12 28 DF}Moo!", None, 'junk'), # sfx: cow
    '1175':                                                     ("${12 28 D8}Woof!", None, 'junk'), # sfx: dog
    '1176':                                                     ("${12 68 08}Aah! You startled me!", None, 'junk'), # sfx: adult Link scream (when falling)
    '1178':                                                     ("Use Multiworld to cross the gaps between worlds and engage in jolly co-operation!", None, 'junk'), # ref: Dark Souls
    '1179':                                                     ("${12 68 51}What in tarnation!", None, 'junk'), # sfx: Talon surprised at being woken
    '1180':                                                     ("Press \u00A5\u00A5\u00A6\u00A6\u00A7\u00A8\u00A7\u00A8\u00A0\u009F to warp to&the credits.", None, 'junk'), # ref: Konami Code
    '1181':                                                     ("Oh!^Oh-oh!^C'mon!^Come on! Come on! Come on!^HOT!!^What a hot beat!^WHOOOOAH!^YEEEEAH!^YAHOOO!!", None, 'junk'), # ref: Darunia dancing
    '1182':                                                     ("${12 68 5F}Hey! Listen!", None, 'junk'), # sfx: Navi: "Hey!"
    '1183':                                                     ("I am the King of Gossip Stones, but fear not - I have the common touch! That means I can make conversation with everyone^from foreign dignitaries to the lowliest bumpkin - such as yourself!", None, 'junk'), # ref: Dragon Quest XI
    '1184':                                                     ("I am @, hero of the Gossip Stones! Hear my name and tremble!", None, 'junk'), # ref: Link the Goron
    '1185':                                                     ("Having trouble defeating Dark Link?^Look away from him while holding Z-Target and then when Dark Link walks up behind you, strafe sideways and slash your sword.", None, 'junk'),
    '1186':                                                     ("They say that if Link could say a few words, he'd be a better public speaker.", None, 'junk'),
    '1187':                                                     ("Did you know that you only need to play the Song of Time to open the Door of Time? The Spiritual Stones are not needed.", None, 'junk'),
    '1188':                                                     ("Where did Anju meet her lover?^${12 39 C7}At a Kafei.", None, 'junk'), # ref: Majora's Mask / sfx: Ganondorf laugh
    '1189':                                                     ("Did you know that you can access the Fire Temple boss door without dropping the pillar by using the Hover boots?", None, 'junk'),
    '1190':                                                     ("Key-locked in Fire Temple? Maybe Volvagia has your Small Key.", None, 'junk'),
    # '1191':                                                     ("Expired Spoiler Log? Don't worry! The OoTR Discord staff can help you out.", None, 'junk'),
    '1192':                                                     ("Try holding a D-pad button on the item screen.", None, 'junk'),
    '1193':                                                     ("Did you know that in the Forest Temple you can reach the alcove in the block push room with Hover Boots?", None, 'junk'),
    '1194':                                                     ("Dodongo's Cavern is much easier and faster to clear as Adult.", None, 'junk'),
    '1195':                                                     ("Did you know that the solution to the Truth Spinner in Shadow Temple is never one of the two positions closest to the initial position?", None, 'junk'),
    '1196':                                                     ("Did you know that the Kokiri Sword is as effective as Deku Sticks against Dead Hand?", None, 'junk'),
    '1197':                                                     ("Did you know that Ruto is strong enough to defeat enemies and activate ceiling switches inside Jabu Jabu's Belly?", None, 'junk'),
    '1198':                                                     ("Did you know that Barinade, Volvagia and Twinrova hard require the Boomerang, Megaton Hammer and Mirror Shield, respectively?", None, 'junk'),
    '1199':                                                     ("Did you know that Dark Link's max health is equal to @'s max health?", None, 'junk'),
    '1200':                                                     ("Did you know that you can reach the invisible Hookshot target before the fans room in Shadow Temple with just the Hookshot if you backflip onto the chest?", None, 'junk'),
    '1201':                                                     ("${12 68 54}Objection!", None, 'junk'), # ref: Ace Attorney / sfx: Ingo's BWAAAAAH
    '1202':                                                     ("They say that in the castle courtyard you can see a portrait of a young Talon.", None, 'junk'), # ref: Talon = Mario joke
    '1203':                                                     ("They say that Phantom Ganon is a big Louisa May Alcott fan.", None, 'junk'), # ref: The Poe Sisters are named after characters from one of her novels
    '1204':                                                     ("Have you found all 41 Gossip Stones?^Only 40 of us give hints.", None, 'junk'), # The 41th stone is the Lake Hylia water level stone
    '1205':                                                     ("It's time for you to look inward and begin asking yourself the big questions:^How did Medigoron get inside that hole, and how does he get out for the credits?", None, 'junk'), # ref: Avatar The Last Airbender
    '1206':                                                     ("They say that Jabu Jabu is no longer a pescetarian in Master Quest.", None, 'junk'),
    '1207':                                                     ("Why are the floating skulls called \"Bubbles\" and the floating bubbles \"Shaboms\"?", None, 'junk'),
    '1208':                                                     ("Why aren't ReDead called ReAlive?", None, 'junk'),
    '1209':                                                     ("${12 48 27}Songs are hard, aren't they?", None, 'junk'), # sfx: failing a song
    '1210':                                                     ("Did you know that you can Boomerang items that are freestanding Heart Pieces in the unrandomized game?", None, 'junk'),
    '1211':                                                     ("Did you know that ReDead won't attack if you walk very slowly?", None, 'junk'),
    '1212':                                                     ("Did you know that ReDead and Gibdo have their own version of Sun's Song that freezes you?", None, 'junk'),
    '1213':                                                     ("${12 28 B1}\u009F \u00A7\u00A8\u00A6 \u00A7\u00A8\u00A6 \u009F\u00A6 \u009F\u00A6 \u00A8\u00A7\u009F", None, 'junk'), # ref: Frogs 2 / sfx: Frogs
    '1214':                                                     ("${12 28 A2}Help! I'm melting away!", None, 'junk'), # sfx: red ice melting
    '1215':                                                     ("${12 38 80}Eek!^I'm a little shy...", None, 'junk'), # sfx: Scrub hurt/stunned by Link
    '1216':                                                     ("Master, there is a 0 percent chance that this hint is useful in any way.", None, 'junk'), # ref: Skyward Sword
    '1217':                                                     ("${12 48 0B}Here, have a heart <3", None, 'junk'), # sfx: get Recovery Heart
    '1218':                                                     ("${12 48 03}Here, have a Rupee.", None, 'junk'), # sfx: get Rupee
    '1219':                                                     ("${12 68 31}Don't forget to stand up and stretch regularly.", None, 'junk'), # sfx: child Link stretching and yawning
    '1220':                                                     ("Remember that time you did that really embarrassing thing?^${12 68 3A}Yikes.", None, 'junk'), # sfx: child Link fall damage
    '1221':                                                     ("@ tries to read the Gossip Stone...^${12 48 06}but he's standing on the wrong side of it!", None, 'junk'), # ref: Dragon Quest XI / sfx: error (e.g. trying to equip an item as the wrong age)
    '1222':                                                     ("Plandomizer is a pathway to many abilities some consider to be... unnatural.", None, 'junk'), # ref: Star Wars
    '1223':                                                     ("Did you know that you can have complete control over the item placement, item pool, and more, using Plandomizer?", None, 'junk'),
    '1224':                                                     ("They say that the earth is round.^Just like pizza.", None, 'junk'),
    '1225':                                                     ("${12 68 62}Keeeyaaaah!^What is this?! A Hylian?!", None, 'junk'), # ref: Ruto meeting Big Octo / sfx: Ruto screaming
    '1226':                                                     ("For you, the day you read this hint was the most important day of your life.^But for me, it was Tuesday.", None, 'junk'), # ref: Street Fighter (the movie)
    '1227':                                                     ("Did you know that Barinade is allergic to bananas?", None, 'junk'),
    '1228':                                                     ("Have you seen my dodongo? Very large, eats everything, responds to \"King\".^Call Darunia in Goron City if found. Huge rupee reward!", None, 'junk'),
    '1229':                                                     ("Having trouble breathing underwater?^Have you tried wearing more BLUE?", None, 'junk'),
    # '1230':                                                     ("Hi! I'm currently on an exchange program from Termina.^They say that East Clock Town is on the way of the hero.", None, 'junk'), # ref: Majora's Mask
    '1231':                                                     ("Why are you asking me? I don't have any answers! I'm just as confused as you are!", None, 'junk'),
    '1232':                                                     ("What do you call a group of Gorons?^${12 39 C7}A rock band.", None, 'junk'), # sfx: Ganondorf laugh
    '1233':                                                     ("When the moon hits Termina like a big pizza pie that's game over.", None, 'junk'), # ref: That's Amore by Dean Martin + Majora's Mask
    '1234':                                                     ("Ganondorf doesn't specialize in hiding items, nor in keeping secrets for that matter.", None, 'junk'),
    '1235':                                                     ("While you're wasting time reading this hint, the others are playing the seed.", None, 'junk'),
    '1236':                                                     ("Have you ever tried hammering the ground or wall in a room with Torch Slugs, Flare Dancers, Tektites, Walltulas, Scrubs or Deku Babas?", None, 'junk'),
    '1237':                                                     ("Did you know that there's a 1/201 chance per Rupee that the Zora from the diving minigame tosses a 500 Rupee?^Keep winning and the odds go up!", None, 'junk'),
    '1238':                                                     ("J = 0;&while J < 10;&   Press \u009F;&   J++;^   Press \u009F;&   J++;^   Press \u009F;&   J++;^   Press \u009F;&   J++;^   Press \u009F;&   J++;^   Press \u009F;&   J++;^   Press \u009F;&   J++;^   Press \u009F;&   J++;^   Press \u009F;&   J++;^   Press \u009F;^break;", None, 'junk'), # \u009F = A button

    'Deku Tree':                                                ("an ancient tree", "the Deku Tree", 'dungeonName'),
    'Dodongos Cavern':                                          ("an immense cavern", "Dodongo's Cavern", 'dungeonName'),
    'Jabu Jabus Belly':                                         ("the belly of a deity", "Jabu Jabu's Belly", 'dungeonName'),
    'Forest Temple':                                            ("a deep forest", "the Forest Temple", 'dungeonName'),
    'Fire Temple':                                              ("a high mountain", "the Fire Temple", 'dungeonName'),
    'Water Temple':                                             ("a vast lake", "the Water Temple", 'dungeonName'),
    'Shadow Temple':                                            ("the house of the dead", "the Shadow Temple", 'dungeonName'),
    'Spirit Temple':                                            ("the goddess of the sand", "the Spirit Temple", 'dungeonName'),
    'Ice Cavern':                                               ("a frozen maze", "the Ice Cavern", 'dungeonName'),
    'Bottom of the Well':                                       ("a shadow's prison", "the Bottom of the Well", 'dungeonName'),
    'Gerudo Training Ground':                                   ("the test of thieves", "the Gerudo Training Ground", 'dungeonName'),
    'Ganons Castle':                                            ("a conquered citadel", "inside Ganon's Castle", 'dungeonName'),

    'bridge_vanilla':                                           ("the #Shadow and Spirit Medallions# as well as the #Light Arrows#", None, 'bridge'),
    'bridge_stones':                                            ("Spiritual Stones", None, 'bridge'),
    'bridge_medallions':                                        ("Medallions", None, 'bridge'),
    'bridge_dungeons':                                          ("Spiritual Stones and Medallions", None, 'bridge'),
    'bridge_tokens':                                            ("Gold Skulltula Tokens", None, 'bridge'),
    'bridge_hearts':                                            ("hearts", None, 'bridge'),

    'ganonBK_dungeon':                                          ("hidden somewhere #inside its castle#", None, 'ganonBossKey'),
    'ganonBK_regional':                                         ("hidden somewhere #inside or nearby its castle#", None, 'ganonBossKey'),
    'ganonBK_vanilla':                                          ("kept in a big chest #inside its tower#", None, 'ganonBossKey'),
    'ganonBK_overworld':                                        ("hidden #outside of dungeons# in Hyrule", None, 'ganonBossKey'),
    'ganonBK_any_dungeon':                                      ("hidden #inside a dungeon# in Hyrule", None, 'ganonBossKey'),
    'ganonBK_keysanity':                                        ("hidden #anywhere in Hyrule#", None, 'ganonBossKey'),
    'ganonBK_triforce':                                         ("given to the Hero once the #Triforce# is completed", None, 'ganonBossKey'),
    'ganonBK_medallions':                                       ("Medallions", None, 'ganonBossKey'),
    'ganonBK_stones':                                           ("Spiritual Stones", None, 'ganonBossKey'),
    'ganonBK_dungeons':                                         ("Spiritual Stones and Medallions", None, 'ganonBossKey'),
    'ganonBK_tokens':                                           ("Gold Skulltula Tokens", None, 'ganonBossKey'),
    'ganonBK_hearts':                                           ("hearts", None, 'ganonBossKey'),

    'lacs_vanilla':                                             ("the #Shadow and Spirit Medallions#", None, 'lacs'),
    'lacs_medallions':                                          ("Medallions", None, 'lacs'),
    'lacs_stones':                                              ("Spiritual Stones", None, 'lacs'),
    'lacs_dungeons':                                            ("Spiritual Stones and Medallions", None, 'lacs'),
    'lacs_tokens':                                              ("Gold Skulltula Tokens", None, 'lacs'),
    'lacs_hearts':                                              ("hearts", None, 'lacs'),

    'Spiritual Stone Text Start':                               ("3 Spiritual Stones found in Hyrule...", None, 'altar'),
    'Child Altar Text End':                                     ("\x13\x07Ye who may become a Hero...&Stand with the Ocarina and&play the Song of Time.", None, 'altar'),
    'Adult Altar Text Start':                                   ("When evil rules all, an awakening&voice from the Sacred Realm will&call those destined to be Sages,&who dwell in the \x05\x41five temples\x05\x40.", None, 'altar'),
    'Adult Altar Text End':                                     ("Together with the Hero of Time,&the awakened ones will bind the&evil and return the light of peace&to the world...", None, 'altar'),

    'Validation Line':                                          ("Hmph... Since you made it this far,&I'll let you know what glorious&prize of Ganon's you likely&missed out on in my tower.^Behold...^", None, 'validation line'),
    '2001':                                                     ("Oh! It's @.&I was expecting someone called&Sheik. Do you know what&happened to them?", None, 'ganonLine'),
    '2002':                                                     ("I knew I shouldn't have put the key&on the other side of my door.", None, 'ganonLine'),
    '2003':                                                     ("Looks like it's time for a&round of tennis.", None, 'ganonLine'),
    '2004':                                                     ("You'll never deflect my bolts of&energy with your sword,&then shoot me with those Light&Arrows you happen to have.", None, 'ganonLine'),
    '2005':                                                     ("Why did I leave my trident&back in the desert?", None, 'ganonLine'),
    '2006':                                                     ("Zelda is probably going to do&something stupid, like send you&back to your own timeline.^So this is quite meaningless.&Do you really want&to save this moron?", None, 'ganonLine'),
    '2007':                                                     ("What about Zelda makes you think&she'd be a better ruler than I?^I saved Lon Lon Ranch,&fed the hungry,&and my castle floats.", None, 'ganonLine'),
    '2008':                                                     ("I've learned this spell,&it's really neat,&I'll keep it later&for your treat!", None, 'ganonLine'),
    '2009':                                                     ("Many tricks are up my sleeve,&to save yourself&you'd better leave!", None, 'ganonLine'),
    '2010':                                                     ("After what you did to&Koholint Island, how can&you call me the bad guy?", None, 'ganonLine'),
    '2011':                                                     ("Today, let's begin down&'The Hero is Defeated' timeline.", None, 'ganonLine'),
}

# Table containing the groups of locations for the multi hints (dual, etc.)
# The is used in order to add the locations to the checked list
multiTable = {
    'Deku Theater Rewards':                                     ['Deku Theater Skull Mask', 'Deku Theater Mask of Truth'],
    'HF Ocarina of Time Retrieval':                             ['HF Ocarina of Time Item', 'Song from Ocarina of Time'],
    'HF Valley Grotto':                                         ['HF Cow Grotto Cow', 'HF GS Cow Grotto'],
    'Market Bombchu Bowling Rewards':                           ['Market Bombchu Bowling First Prize', 'Market Bombchu Bowling Second Prize'],
    'ZR Frogs Rewards':                                         ['ZR Frogs in the Rain', 'ZR Frogs Ocarina Game'],
    'LH Lake Lab Pool':                                         ['LH Lab Dive', 'LH GS Lab Crate'],
    'LH Adult Bean Destination Checks':                         ['LH Freestanding PoH', 'LH Adult Fishing'],
    'GV Pieces of Heart Ledges':                                ['GV Crate Freestanding PoH', 'GV Waterfall Freestanding PoH'],
    'GF Horseback Archery Rewards':                             ['GF HBA 1000 Points', 'GF HBA 1500 Points'],
    'Colossus Nighttime GS':                                    ['Colossus GS Tree', 'Colossus GS Hill'],
    'Graveyard Dampe Race Rewards':                             ['Graveyard Dampe Race Hookshot Chest', 'Graveyard Dampe Race Freestanding PoH'],
    'Graveyard Royal Family Tomb Contents':                     ['Graveyard Royal Familys Tomb Chest', 'Song from Royal Familys Tomb'],
    'DMC Child Upper Checks':                                   ['DMC GS Crate', 'DMC Deku Scrub'],
    'Haunted Wasteland Checks':                                 ['Wasteland Chest', 'Wasteland GS'],

    'Deku Tree MQ Basement GS':                                 ['Deku Tree MQ GS Basement Graves Room','Deku Tree MQ GS Basement Back Room'],
    'Dodongos Cavern Upper Business Scrubs':                    ['Dodongos Cavern Deku Scrub Near Bomb Bag Left', 'Dodongos Cavern Deku Scrub Near Bomb Bag Right'],
    'Dodongos Cavern MQ Larvae Room':                           ['Dodongos Cavern MQ Larvae Room Chest', 'Dodongos Cavern MQ GS Larvae Room'],
    'Fire Temple Lower Loop':                                   ['Fire Temple Flare Dancer Chest', 'Fire Temple Boss Key Chest'],
    'Fire Temple MQ Lower Loop':                                ['Fire Temple MQ Megaton Hammer Chest', 'Fire Temple MQ Map Chest'],
    'Water Temple River Loop Chests':                           ['Water Temple Longshot Chest', 'Water Temple River Chest'],
    'Water Temple River Checks':                                ['Water Temple GS River', 'Water Temple River Chest'],
    'Water Temple North Basement Checks':                       ['Water Temple GS Near Boss Key Chest', 'Water Temple Boss Key Chest'],
    'Water Temple MQ North Basement Checks':                    ['Water Temple MQ Freestanding Key', 'Water Temple MQ GS Freestanding Key Area'],
    'Water Temple MQ Lower Checks':                             ['Water Temple MQ Boss Key Chest', 'Water Temple MQ Freestanding Key'],
    'Spirit Temple Colossus Hands':                             ['Spirit Temple Silver Gauntlets Chest', 'Spirit Temple Mirror Shield Chest'],
    'Spirit Temple Child Lower':                                ['Spirit Temple Child Bridge Chest', 'Spirit Temple Child Early Torches Chest'],
    'Spirit Temple Child Top':                                  ['Spirit Temple Sun Block Room Chest', 'Spirit Temple GS Hall After Sun Block Room'],
    'Spirit Temple Adult Lower':                                ['Spirit Temple Early Adult Right Chest', 'Spirit Temple Compass Chest'],
    'Spirit Temple MQ Child Top':                               ['Spirit Temple MQ Sun Block Room Chest', 'Spirit Temple MQ GS Sun Block Room'],
    'Spirit Temple MQ Symphony Room':                           ['Spirit Temple MQ Symphony Room Chest', 'Spirit Temple MQ GS Symphony Room'],
    'Spirit Temple MQ Throne Room GS':                          ['Spirit Temple MQ GS Nine Thrones Room West', 'Spirit Temple MQ GS Nine Thrones Room North'],
    'Shadow Temple Invisible Blades Chests':                    ['Shadow Temple Invisible Blades Visible Chest', 'Shadow Temple Invisible Blades Invisible Chest'],
    'Shadow Temple Single Pot Room':                            ['Shadow Temple Freestanding Key', 'Shadow Temple GS Single Giant Pot'],
    'Shadow Temple Spike Walls Room':                           ['Shadow Temple Spike Walls Left Chest', 'Shadow Temple Boss Key Chest'],
    'Shadow Temple MQ Upper Checks':                            ['Shadow Temple MQ Compass Chest', 'Shadow Temple MQ Hover Boots Chest'],
    'Shadow Temple MQ Invisible Blades Chests':                 ['Shadow Temple MQ Invisible Blades Visible Chest', 'Shadow Temple MQ Invisible Blades Invisible Chest'],
    'Shadow Temple MQ Spike Walls Room':                        ['Shadow Temple MQ Spike Walls Left Chest', 'Shadow Temple MQ Boss Key Chest'],
    'Bottom of the Well Inner Rooms GS':                        ['Bottom of the Well GS West Inner Room', 'Bottom of the Well GS East Inner Room'],
    'Bottom of the Well Dead Hand Room':                        ['Bottom of the Well Lens of Truth Chest', 'Bottom of the Well Invisible Chest'],
    'Bottom of the Well MQ Dead Hand Room':                     ['Bottom of the Well MQ Compass Chest', 'Bottom of the Well MQ Dead Hand Freestanding Key'],
    'Bottom of the Well MQ Basement':                           ['Bottom of the Well MQ GS Basement', 'Bottom of the Well MQ Lens of Truth Chest'],
    'Ice Cavern Final Room':                                    ['Ice Cavern Iron Boots Chest', 'Sheik in Ice Cavern'],
    'Ice Cavern MQ Final Room':                                 ['Ice Cavern MQ Iron Boots Chest', 'Sheik in Ice Cavern'],
    'Ganons Castle Spirit Trial Chests':                        ['Ganons Castle Spirit Trial Crystal Switch Chest', 'Ganons Castle Spirit Trial Invisible Chest'],
}

misc_item_hint_table = {
    'dampe_diary': {
        'id': 0x5003,
        'hint_location': 'Dampe Diary Hint',
        'default_item': 'Progressive Hookshot',
        'default_item_text': "Whoever reads this, please enter {area}. I will let you have my stretching, shrinking keepsake.^I'm waiting for you.&--Dampé",
        'custom_item_text': "Whoever reads this, please enter {area}. I will let you have {item}.^I'm waiting for you.&--Dampé",
        'default_item_fallback': "Whoever reads this, I'm sorry, but I seem to have #misplaced# my stretching, shrinking keepsake.&--Dampé",
        'custom_item_fallback': "Whoever reads this, I'm sorry, but I seem to have #misplaced# {item}.&--Dampé",
        'replace': {
            "enter #your pocket#. I will let you have": "check #your pocket#. You will find",
        },
        'use_alt_hint': False,
        'local_only': True,
    },
    'ganondorf': {
        'id': 0x70CC,
        'hint_location': 'Ganondorf Hint',
        'default_item': 'Light Arrows',
        'default_item_text': "Ha ha ha... You'll never beat me by reflecting my lightning bolts and unleashing the arrows from {area}!",
        'custom_item_text': "Ha ha ha... You'll never find {item} from {area}!",
        'replace': {
            "from #inside Ganon's Castle#": "from #inside my castle#",
            "from #outside Ganon's Castle#": "from #outside my castle#",
            "from #Ganondorf's Chamber#": "from #those pots over there#",
        },
        'use_alt_hint': True,
        'local_only': False,
    },
}

misc_location_hint_table = {
    '10_skulltulas': {
        'id': 0x9004,
        'hint_location': '10 Skulltulas Reward Hint',
        'item_location': 'Kak 10 Gold Skulltula Reward',
        'location_text': "Yeaaarrgh! I'm cursed!! Please save me by destroying \x05\x4110 Spiders of the Curse\x05\x40 and I will give you \x05\x42{item}\x05\x40.",
        'location_fallback': "Yeaaarrgh! I'm cursed!!",
    },
    '20_skulltulas': {
        'id': 0x9005,
        'hint_location': '20 Skulltulas Reward Hint',
        'item_location': 'Kak 20 Gold Skulltula Reward',
        'location_text': "Yeaaarrgh! I'm cursed!! Please save me by destroying \x05\x4120 Spiders of the Curse\x05\x40 and I will give you \x05\x42{item}\x05\x40.",
        'location_fallback': "Yeaaarrgh! I'm cursed!!",
    },
    '30_skulltulas': {
        'id': 0x9006,
        'hint_location': '30 Skulltulas Reward Hint',
        'item_location': 'Kak 30 Gold Skulltula Reward',
        'location_text': "Yeaaarrgh! I'm cursed!! Please save me by destroying \x05\x4130 Spiders of the Curse\x05\x40 and I will give you \x05\x42{item}\x05\x40.",
        'location_fallback': "Yeaaarrgh! I'm cursed!!",
    },
    '40_skulltulas': {
        'id': 0x9007,
        'hint_location': '40 Skulltulas Reward Hint',
        'item_location': 'Kak 40 Gold Skulltula Reward',
        'location_text': "Yeaaarrgh! I'm cursed!! Please save me by destroying \x05\x4140 Spiders of the Curse\x05\x40 and I will give you \x05\x42{item}\x05\x40.",
        'location_fallback': "Yeaaarrgh! I'm cursed!!",
    },
    '50_skulltulas': {
        'id': 0x9008,
        'hint_location': '50 Skulltulas Reward Hint',
        'item_location': 'Kak 50 Gold Skulltula Reward',
        'location_text': "Yeaaarrgh! I'm cursed!! Please save me by destroying \x05\x4150 Spiders of the Curse\x05\x40 and I will give you \x05\x42{item}\x05\x40.",
        'location_fallback': "Yeaaarrgh! I'm cursed!!",
    },
}

# Separate table for goal names to avoid duplicates in the hint table.
# Link's Pocket will always be an empty goal, but it's included here to
# prevent key errors during the dungeon reward lookup.
goalTable = {
    'Queen Gohma':                                              ("path to the #Spider#", "path to #Queen Gohma#", "Green"),
    'King Dodongo':                                             ("path to the #Dinosaur#", "path to #King Dodongo#", "Red"),
    'Barinade':                                                 ("path to the #Tentacle#", "path to #Barinade#", "Blue"),
    'Phantom Ganon':                                            ("path to the #Puppet#", "path to #Phantom Ganon#", "Green"),
    'Volvagia':                                                 ("path to the #Dragon#", "path to #Volvagia#", "Red"),
    'Morpha':                                                   ("path to the #Amoeba#", "path to #Morpha#", "Blue"),
    'Bongo Bongo':                                              ("path to the #Hands#", "path to #Bongo Bongo#", "Pink"),
    'Twinrova':                                                 ("path to the #Witches#", "path to #Twinrova#", "Yellow"),
    'Links Pocket':                                             ("path to #Links Pocket#", "path to #Links Pocket#", "Light Blue"),
}


# This specifies which hints will never appear due to either having known or known useless contents or due to the locations not existing.
def hintExclusions(world, clear_cache=False):
    if not clear_cache and world.hint_exclusions is not None:
        return world.hint_exclusions

    world.hint_exclusions = []

    for location in world.get_locations():
        if (location.locked and ((isinstance(location.item, OOTItem) and location.item.type != 'Song') or world.shuffle_song_items != 'song')) or location.progress_type == LocationProgressType.EXCLUDED:
            world.hint_exclusions.append(location.name)

    world_location_names = [
        location.name for location in world.get_locations()]

    location_hints = []
    for name in hintTable:
        hint = getHint(name, world.random, world.clearer_hints)
        if any(item in hint.type for item in 
                ['always',
                 'dual_always',
                 'sometimes',
                 'overworld',
                 'dungeon',
                 'song',
                 'dual',
                 'exclude']):
            location_hints.append(hint)

    for hint in location_hints:
        if hint.name not in world_location_names and hint.name not in world.hint_exclusions:
            world.hint_exclusions.append(hint.name)

    return world.hint_exclusions

def nameIsLocation(name, hint_type, world):
    if isinstance(hint_type, (list, tuple)):
        for htype in hint_type:
            if htype in ['sometimes', 'song', 'overworld', 'dungeon', 'always', 'exclude'] and name not in hintExclusions(world):
                return True
    elif hint_type in ['sometimes', 'song', 'overworld', 'dungeon', 'always', 'exclude'] and name not in hintExclusions(world):
        return True
    return False

hintExclusions.exclusions = None

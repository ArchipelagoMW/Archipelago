import random

#   Abbreviations
#       DMC     Death Mountain Crater
#       DMT     Death Mountain Trail
#       GC      Goron City
#       GF      Gerudo Fortress
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
#       ZD      Zora's Domain
#       ZF      Zora's Fountain
#       ZR      Zora's River

class Hint(object):
    name = ""
    text = ""
    type = []

    def __init__(self, name, text, type, choice=None):
        self.name = name
        self.type = [type] if not isinstance(type, list) else type

        if isinstance(text, str):
            self.text = text
        else:
            if choice == None:
                self.text = random.choice(text)
            else:
                self.text = text[choice]


def getHint(name, clearer_hint=False):
    textOptions, clearText, type = hintTable[name]
    if clearer_hint:
        if clearText == None:
            return Hint(name, textOptions, type, 0)
        return Hint(name, clearText, type)
    else:
        return Hint(name, textOptions, type)


def getHintGroup(group, world):
    ret = []
    for name in hintTable:

        hint = getHint(name, world.clearer_hints)

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
        hint = getHint(name)
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
    'DMT Biggoron':                 lambda world: world.logic_earliest_adult_trade != 'claim_check' or world.logic_latest_adult_trade != 'claim_check',
    'Kak 30 Gold Skulltula Reward': lambda world: tokens_required_by_settings(world) < 30,
    'Kak 40 Gold Skulltula Reward': lambda world: tokens_required_by_settings(world) < 40,
    'Kak 50 Gold Skulltula Reward': lambda world: tokens_required_by_settings(world) < 50,
}


# table of hints, format is (name, hint text, clear hint text, type of hint) there are special characters that are read for certain in game commands:
# ^ is a box break
# & is a new line
# @ will print the player name
# # sets color to white (currently only used for dungeon reward hints).
hintTable = {
    'Triforce Piece':                                           (["a triumph fork", "cheese", "a gold fragment"], "a Piece of the Triforce", "item"),
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
    'Compass':                                                  (["a treasure tracker", "a magnetic needle"], "a Compass", 'item'),
    'BossKey':                                                  (["a master of unlocking", "a dungeon's master pass"], "a Boss Key", 'item'),
    'GanonBossKey':                                             (["a master of unlocking", "a dungeon's master pass"], "a Boss Key", 'item'),
    'SmallKey':                                                 (["a tool for unlocking", "a dungeon pass", "a lock remover", "a lockpick"], "a Small Key", 'item'),
    'FortressSmallKey':                                         (["a get out of jail free card"], "a Jail Key", 'item'),
    'KeyError':                                                 (["something mysterious", "an unknown treasure"], "An Error (Please Report This)", 'item'),
    'Arrows (5)':                                               (["a few danger darts", "a few sharp shafts"], "Arrows (5 pieces)", 'item'),
    'Arrows (10)':                                              (["some danger darts", "some sharp shafts"], "Arrows (10 pieces)", 'item'),
    'Arrows (30)':                                              (["plenty of danger darts", "plenty of sharp shafts"], "Arrows (30 pieces)", 'item'),
    'Bombs (5)':                                                (["a few explosives", "a few blast balls"], "Bombs (5 pieces)", 'item'),
    'Bombs (10)':                                               (["some explosives", "some blast balls"], "Bombs (10 pieces)", 'item'),
    'Bombs (20)':                                               (["lots-o-explosives", "plenty of blast balls"], "Bombs (20 pieces)", 'item'),
    'Ice Trap':                                                 (["a gift from Ganon", "a chilling discovery", "frosty fun"], "an Ice Trap", 'item'),
    'Magic Bean':                                               (["a wizardly legume"], "a Magic Bean", 'item'),
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
    'Song from Composers Grave':                                   (["#ReDead in the Composers' Grave# guard", "the #Composer Brothers wrote#"], None, ['song', 'sometimes']),
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
    'Graveyard Composers Grave Chest':                             (["#flames in the Composers' Grave# reveal", "the #Composer Brothers hid#"], None, ['overworld', 'sometimes']),
    'ZF Bottom Freestanding PoH':                                  ("#under the icy waters# lies", None, ['overworld', 'sometimes']),
    'GC Pot Freestanding PoH':                                     ("spinning #Goron pottery# contains", None, ['overworld', 'sometimes']),
    'ZD King Zora Thawed':                                         ("a #defrosted dignitary# gifts", "unfreezing #King Zora# grants", ['overworld', 'sometimes']),
    'DMC Deku Scrub':                                              ("a single #scrub in the crater# sells", None, ['overworld', 'sometimes']),
    'DMC GS Crate':                                                ("a spider under a #crate in the crater# holds", None, ['overworld', 'sometimes']),

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
    'Water Temple Boss Key Chest':                                 ("dodging #rolling boulders under the lake# leads to", "dodging #rolling boulders in the Water Temple# leads to", ['dungeon', 'sometimes']),
    'Water Temple GS Behind Gate':                                 ("a spider behind a #gate under the lake# holds", "a spider behind a #gate in the Water Temple# holds", ['dungeon', 'sometimes']),
    'Water Temple MQ Freestanding Key':                            ("hidden in a #box under the lake# lies", "hidden in a #box in the Water Temple# lies", ['dungeon', 'sometimes']),
    'Water Temple MQ GS Freestanding Key Area':                    ("the #locked spider under the lake# holds", "the #locked spider in the Water Temple# holds", ['dungeon', 'sometimes']),
    'Water Temple MQ GS Triple Wall Torch':                        ("a spider behind a #gate under the lake# holds", "a spider behind a #gate in the Water Temple# holds", ['dungeon', 'sometimes']),
    'Gerudo Training Grounds Underwater Silver Rupee Chest':       (["those who seek #sunken silver rupees# will find", "the #thieves' underwater training# rewards"], None, ['dungeon', 'sometimes']),
    'Gerudo Training Grounds MQ Underwater Silver Rupee Chest':    (["those who seek #sunken silver rupees# will find", "the #thieves' underwater training# rewards"], None, ['dungeon', 'sometimes']),
    'Gerudo Training Grounds Maze Path Final Chest':               ("the final prize of #the thieves' training# is", None, ['dungeon', 'sometimes']),
    'Gerudo Training Grounds MQ Ice Arrows Chest':                 ("the final prize of #the thieves' training# is", None, ['dungeon', 'sometimes']),
    'Bottom of the Well Lens of Truth Chest':                      (["the well's #grasping ghoul# hides", "a #nether dweller in the well# holds"], "#Dead Hand in the well# holds", ['dungeon', 'sometimes']),
    'Bottom of the Well MQ Compass Chest':                         (["the well's #grasping ghoul# hides", "a #nether dweller in the well# holds"], "#Dead Hand in the well# holds", ['dungeon', 'sometimes']),
    'Spirit Temple Silver Gauntlets Chest':                        ("the treasure #sought by Nabooru# is", "upon the #Colossus's right hand# is", ['dungeon', 'sometimes']),
    'Spirit Temple Mirror Shield Chest':                           ("upon the #Colossus's left hand# is", None, ['dungeon', 'sometimes']),
    'Spirit Temple MQ Child Hammer Switch Chest':                  ("a #temporal paradox in the Colossus# yields", "a #temporal paradox in the Spirit Temple# yields", ['dungeon', 'sometimes']),
    'Spirit Temple MQ Symphony Room Chest':                        ("a #symphony in the Colossus# yields", "a #symphony in the Spirit Temple# yields", ['dungeon', 'sometimes']),
    'Spirit Temple MQ GS Symphony Room':                           ("a #spider's symphony in the Colossus# yields", "a #spider's symphony in the Spirit Temple# yields", ['dungeon', 'sometimes']),
    'Shadow Temple Invisible Floormaster Chest':                   ("shadows in an #invisible maze# guard", None, ['dungeon', 'sometimes']),
    'Shadow Temple MQ Bomb Flower Chest':                          ("shadows in an #invisible maze# guard", None, ['dungeon', 'sometimes']),

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
    'Graveyard Hookshot Chest':                                    ("a chest hidden by a #speedy spectre# holds", "#dead Dampé's first prize# is", 'exclude'),
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
    'HC Great Fairy Reward':                                       ("the #fairy of fire# holds", None, 'exclude'),
    'Colossus Great Fairy Reward':                                 ("the #fairy of love# holds", None, 'exclude'),
    'DMT Great Fairy Reward':                                      ("a #magical fairy# gifts", None, 'exclude'),
    'DMC Great Fairy Reward':                                      ("a #magical fairy# gifts", None, 'exclude'),
    'OGC Great Fairy Reward':                                      ("the #fairy of strength# holds", None, 'exclude'),

    'Song from Impa':                                              ("#deep in a castle#, Impa teaches", None, 'exclude'),
    'Song from Malon':                                             ("#a farm girl# sings", None, 'exclude'),
    'Song from Saria':                                             ("#deep in the forest#, Saria teaches", None, 'exclude'),
    'Song from Windmill':                                          ("a man #in a windmill# is obsessed with", None, 'exclude'),

    'HC Malon Egg':                                                ("a #girl looking for her father# gives", None, 'exclude'),
    'HC Zeldas Letter':                                            ("a #princess in a castle# gifts", None, 'exclude'),
    'ZD Diving Minigame':                                          ("an #unsustainable business model# gifts", "those who #dive for Zora rupees# will find", 'exclude'),
    'LH Child Fishing':                                            ("#fishing in youth# bestows", None, 'exclude'),
    'LH Adult Fishing':                                            ("#fishing in maturity# bestows", None, 'exclude'),
    'LH Lab Dive':                                                 ("a #diving experiment# is rewarded with", None, 'exclude'),
    'GC Rolling Goron as Adult':                                   ("#comforting yourself# provides", "#reassuring a young Goron# is rewarded with", 'exclude'),
    'Market Bombchu Bowling First Prize':                          ("the #first explosive prize# is", None, 'exclude'),
    'Market Bombchu Bowling Second Prize':                         ("the #second explosive prize# is", None, 'exclude'),
    'Market Lost Dog':                                             ("#puppy lovers# will find", "#rescuing Richard the Dog# is rewarded with", 'exclude'),
    'LW Ocarina Memory Game':                                      (["the prize for a #game of Simon Says# is", "a #child sing-a-long# holds"], "#playing an Ocarina in Lost Woods# is rewarded with", 'exclude'),
    'Kak 10 Gold Skulltula Reward':                                (["#10 bug badges# rewards", "#10 spider souls# yields", "#10 auriferous arachnids# lead to"], "slaying #10 Gold Skulltulas# reveals", 'exclude'),
    'Kak Man on Roof':                                             ("a #rooftop wanderer# holds", None, 'exclude'),
    'ZR Magic Bean Salesman':                                      ("a seller of #colorful crops# has", "a #bean seller# offers", 'exclude'),
    'ZR Frogs in the Rain':                                        ("#frogs in a storm# gift", None, 'exclude'),
    'GF HBA 1000 Points':                                          ("scoring 1000 in #horseback archery# grants", None, 'exclude'),
    'Market Shooting Gallery Reward':                              ("#shooting in youth# grants", None, 'exclude'),
    'Kak Shooting Gallery Reward':                                 ("#shooting in maturity# grants", None, 'exclude'),
    'LW Target in Woods':                                          ("shooting a #target in the woods# grants", None, 'exclude'),
    'Kak Anju as Adult':                                           ("a #chicken caretaker# offers adults", None, 'exclude'),
    'LLR Talons Chickens':                                         ("#finding Super Cuccos# is rewarded with", None, 'exclude'),
    'GC Rolling Goron as Child':                                   ("the prize offered by a #large rolling Goron# is", None, 'exclude'),
    'LH Underwater Item':                                          ("the #sunken treasure in a lake# is", None, 'exclude'),
    'GF Gerudo Membership Card':                                   ("#rescuing captured carpenters# is rewarded with", None, 'exclude'),
    'Wasteland Bombchu Salesman':                                  ("a #carpet guru# sells", None, 'exclude'),

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
    'GF North F1 Carpenter':                                       ("#defeating Gerudo guards# reveals", None, 'exclude'),
    'GF North F2 Carpenter':                                       ("#defeating Gerudo guards# reveals", None, 'exclude'),
    'GF South F1 Carpenter':                                       ("#defeating Gerudo guards# reveals", None, 'exclude'),
    'GF South F2 Carpenter':                                       ("#defeating Gerudo guards# reveals", None, 'exclude'),

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
    'Forest Temple Boss Key Chest':                                ("a #turned trunk# contains", None, 'exclude'),
    'Forest Temple Floormaster Chest':                             ("deep in the forest #shadows guard a chest# containing", None, 'exclude'),
    'Forest Temple Bow Chest':                                     ("an #army of the dead# guards", "#Stalfos deep in the Forest Temple# guard", 'exclude'),
    'Forest Temple Red Poe Chest':                                 ("#Joelle# guards", "a #red ghost# guards", 'exclude'),
    'Forest Temple Blue Poe Chest':                                ("#Beth# guards", "a #blue ghost# guards", 'exclude'),
    'Forest Temple Basement Chest':                                ("#revolving walls# in the Forest Temple conceal", None, 'exclude'),

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
    'Forest Temple MQ Boss Key Chest':                             ("a #turned trunk# contains", None, 'exclude'),

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
    'Water Temple Central Pillar Chest':                           ("in the #depths of the Water Temple# lies", None, 'exclude'),
    'Water Temple Cracked Wall Chest':                             ("#through a crack# in the Water Temple is", None, 'exclude'),
    'Water Temple Longshot Chest':                                 (["#facing yourself# reveals", "a #dark reflection# of yourself guards"], "#Dark Link# guards", 'exclude'),

    'Water Temple MQ Central Pillar Chest':                        ("in the #depths of the Water Temple# lies", None, 'exclude'),
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
    'Shadow Temple Boss Key Chest':                                ("#walls consumed by a ball of fire# reveal", None, 'exclude'),
    'Shadow Temple Freestanding Key':                              ("#inside a burning skull# lies", None, 'exclude'),

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
    'Shadow Temple MQ Stalfos Room Chest':                         ("near an #empty pedestal# within the Shadow Temple lies", None, 'exclude'),
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

    'Bottom of the Well MQ Map Chest':                             ("a #royal melody in the well# uncovers", None, 'exclude'),
    'Bottom of the Well MQ Lens of Truth Chest':                   ("an #army of the dead# in the well guards", None, 'exclude'),
    'Bottom of the Well MQ Dead Hand Freestanding Key':            ("#Dead Hand's explosive secret# is", None, 'exclude'),
    'Bottom of the Well MQ East Inner Room Freestanding Key':      ("an #invisible path in the well# leads to", None, 'exclude'),

    'Ice Cavern Map Chest':                                        ("#winds of ice# surround", None, 'exclude'),
    'Ice Cavern Compass Chest':                                    ("a #wall of ice# protects", None, 'exclude'),
    'Ice Cavern Iron Boots Chest':                                 ("a #monster in a frozen cavern# guards", None, 'exclude'),
    'Ice Cavern Freestanding PoH':                                 ("a #wall of ice# protects", None, 'exclude'),

    'Ice Cavern MQ Iron Boots Chest':                              ("a #monster in a frozen cavern# guards", None, 'exclude'),
    'Ice Cavern MQ Compass Chest':                                 ("#winds of ice# surround", None, 'exclude'),
    'Ice Cavern MQ Map Chest':                                     ("a #wall of ice# protects", None, 'exclude'),
    'Ice Cavern MQ Freestanding PoH':                              ("#winds of ice# surround", None, 'exclude'),

    'Gerudo Training Grounds Lobby Left Chest':                    ("a #blinded eye in the Gerudo Training Grounds# drops", None, 'exclude'),
    'Gerudo Training Grounds Lobby Right Chest':                   ("a #blinded eye in the Gerudo Training Grounds# drops", None, 'exclude'),
    'Gerudo Training Grounds Stalfos Chest':                       ("#soldiers walking on shifting sands# in the Gerudo Training Grounds guard", None, 'exclude'),
    'Gerudo Training Grounds Beamos Chest':                        ("#reptilian warriors# in the Gerudo Training Grounds protect", None, 'exclude'),
    'Gerudo Training Grounds Hidden Ceiling Chest':                ("the #Eye of Truth# in the Gerudo Training Grounds reveals", None, 'exclude'),
    'Gerudo Training Grounds Maze Path First Chest':               ("the first prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Grounds Maze Path Second Chest':              ("the second prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Grounds Maze Path Third Chest':               ("the third prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Grounds Maze Right Central Chest':            ("the #Song of Time# in the Gerudo Training Grounds leads to", None, 'exclude'),
    'Gerudo Training Grounds Maze Right Side Chest':               ("the #Song of Time# in the Gerudo Training Grounds leads to", None, 'exclude'),
    'Gerudo Training Grounds Hammer Room Clear Chest':             ("#fiery foes# in the Gerudo Training Grounds guard", None, 'exclude'),
    'Gerudo Training Grounds Hammer Room Switch Chest':            ("#engulfed in flame# where thieves train lies", None, 'exclude'),
    'Gerudo Training Grounds Eye Statue Chest':                    ("thieves #blind four faces# to find", None, 'exclude'),
    'Gerudo Training Grounds Near Scarecrow Chest':                ("thieves #blind four faces# to find", None, 'exclude'),
    'Gerudo Training Grounds Before Heavy Block Chest':            ("#before a block of silver# thieves can find", None, 'exclude'),
    'Gerudo Training Grounds Heavy Block First Chest':             ("a #feat of strength# rewards thieves with", None, 'exclude'),
    'Gerudo Training Grounds Heavy Block Second Chest':            ("a #feat of strength# rewards thieves with", None, 'exclude'),
    'Gerudo Training Grounds Heavy Block Third Chest':             ("a #feat of strength# rewards thieves with", None, 'exclude'),
    'Gerudo Training Grounds Heavy Block Fourth Chest':            ("a #feat of strength# rewards thieves with", None, 'exclude'),
    'Gerudo Training Grounds Freestanding Key':                    ("the #Song of Time# in the Gerudo Training Grounds leads to", None, 'exclude'),

    'Gerudo Training Grounds MQ Lobby Right Chest':                ("#thieves prepare for training# with", None, 'exclude'),
    'Gerudo Training Grounds MQ Lobby Left Chest':                 ("#thieves prepare for training# with", None, 'exclude'),
    'Gerudo Training Grounds MQ First Iron Knuckle Chest':         ("#soldiers walking on shifting sands# in the Gerudo Training Grounds guard", None, 'exclude'),
    'Gerudo Training Grounds MQ Before Heavy Block Chest':         ("#before a block of silver# thieves can find", None, 'exclude'),
    'Gerudo Training Grounds MQ Eye Statue Chest':                 ("thieves #blind four faces# to find", None, 'exclude'),
    'Gerudo Training Grounds MQ Flame Circle Chest':               ("#engulfed in flame# where thieves train lies", None, 'exclude'),
    'Gerudo Training Grounds MQ Second Iron Knuckle Chest':        ("#fiery foes# in the Gerudo Training Grounds guard", None, 'exclude'),
    'Gerudo Training Grounds MQ Dinolfos Chest':                   ("#reptilian warriors# in the Gerudo Training Grounds protect", None, 'exclude'),
    'Gerudo Training Grounds MQ Maze Right Central Chest':         ("a #path of fire# leads thieves to", None, 'exclude'),
    'Gerudo Training Grounds MQ Maze Path First Chest':            ("the first prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Grounds MQ Maze Right Side Chest':            ("a #path of fire# leads thieves to", None, 'exclude'),
    'Gerudo Training Grounds MQ Maze Path Third Chest':            ("the third prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Grounds MQ Maze Path Second Chest':           ("the second prize of #the thieves' training# is", None, 'exclude'),
    'Gerudo Training Grounds MQ Hidden Ceiling Chest':             ("the #Eye of Truth# in the Gerudo Training Grounds reveals", None, 'exclude'),
    'Gerudo Training Grounds MQ Heavy Block Chest':                ("a #feat of strength# rewards thieves with", None, 'exclude'),

    'Ganons Tower Boss Key Chest':                                 ("the #Evil King# hoards", None, 'exclude'),

    'Ganons Castle Forest Trial Chest':                            ("the #test of the wilds# holds", None, 'exclude'),
    'Ganons Castle Water Trial Left Chest':                        ("the #test of the seas# holds", None, 'exclude'),
    'Ganons Castle Water Trial Right Chest':                       ("the #test of the seas# holds", None, 'exclude'),
    'Ganons Castle Shadow Trial Front Chest':                      ("#music in the test of darkness# unveils", None, 'exclude'),
    'Ganons Castle Shadow Trial Golden Gauntlets Chest':           ("#light in the test of darkness# unveils", None, 'exclude'),
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
    'Ganons Castle MQ Shadow Trial Eye Switch Chest':              ("the #test of darkness# holds", None, 'exclude'),
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

    'Fire Temple MQ GS Above Fire Wall Maze':                      ("a #spider above a fiery maze# holds", None, 'exclude'),
    'Fire Temple MQ GS Fire Wall Maze Center':                     ("a #spider within a fiery maze# holds", None, 'exclude'),
    'Fire Temple MQ GS Big Lava Room Open Door':                   ("a #Goron trapped near lava# befriended a spider with", None, 'exclude'),
    'Fire Temple MQ GS Fire Wall Maze Side Room':                  ("a #spider beside a fiery maze# holds", None, 'exclude'),

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
    'Shadow Temple GS Like Like Room':                             ("a spider guarded by #invisible blades# holds", None, 'exclude'),
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
    'Kak GS Guards House':                                         ("night in the past reveals a #spider in a town# holding", None, 'exclude'),
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
    'Gerudo Fortress -> GF Storms Grotto':                      ("a #storm within Gerudo's Fortress# reveals", None, 'entrance'),
    'Zoras Domain -> ZD Storms Grotto':                         ("a #storm within Zora's Domain# reveals", None, 'entrance'),
    'Hyrule Castle Grounds -> HC Storms Grotto':                ("a #storm near the castle# reveals", None, 'entrance'),
    'GV Fortress Side -> GV Storms Grotto':                     ("a #storm in the valley# reveals", None, 'entrance'),
    'Desert Colossus -> Colossus Great Fairy Fountain':         ("a #fractured desert wall# hides", None, 'entrance'),
    'Ganons Castle Grounds -> OGC Great Fairy Fountain':        ("a #heavy pillar# outside the castle obstructs", None, 'entrance'),
    'Zoras Fountain -> ZF Great Fairy Fountain':                ("a #fountain wall# hides", None, 'entrance'),
    'GV Fortress Side -> GV Carpenter Tent':                    ("a #tent in the valley# covers", None, 'entrance'),
    'Graveyard Warp Pad Region -> Shadow Temple Entryway':      ("at the #back of the Graveyard#, there is", None, 'entrance'),
    'Lake Hylia -> Water Temple Lobby':                         ("deep #under a vast lake#, one can find", None, 'entrance'),
    'Gerudo Fortress -> Gerudo Training Grounds Lobby':         ("paying a #fee to the Gerudos# grants access to", None, 'entrance'),
    'Zoras Fountain -> Jabu Jabus Belly Beginning':             ("inside #Jabu Jabu#, one can find", None, 'entrance'),
    'Kakariko Village -> Bottom of the Well':                   ("a #village well# leads to", None, 'entrance'),

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
    'Graveyard Composers Grave':                                ("the #Composers' Grave#", None, 'region'),
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

    '1001':                                                     ("Ganondorf 2022!", None, 'junk'),
    '1002':                                                     ("They say that monarchy is a terrible system of governance.", None, 'junk'),
    '1003':                                                     ("They say that Zelda is a poor leader.", None, 'junk'),
    '1004':                                                     ("These hints can be quite useful. This is an exception.", None, 'junk'),
    '1006':                                                     ("They say that all the Zora drowned in Wind Waker.", None, 'junk'),
    '1008':                                                     ("'Member when Ganon was a blue pig?^I 'member.", None, 'junk'),
    '1009':                                                     ("One who does not have Triforce can't go in.", None, 'junk'),
    '1010':                                                     ("Save your future, end the Happy Mask Salesman.", None, 'junk'),
    '1012':                                                     ("I'm stoned. Get it?", None, 'junk'),
    '1013':                                                     ("Hoot! Hoot! Would you like me to repeat that?", None, 'junk'),
    '1014':                                                     ("Gorons are stupid. They eat rocks.", None, 'junk'),
    '1015':                                                     ("They say that Lon Lon Ranch prospered under Ingo.", None, 'junk'),
    '1016':                                                     ("The single rupee is a unique item.", None, 'junk'),
    '1017':                                                     ("Without the Lens of Truth, the Treasure Chest Mini-Game is a 1 out of 32 chance.^Good luck!", None, 'junk'),
    '1018':                                                     ("Use bombs wisely.", None, 'junk'),
    '1021':                                                     ("I found you, faker!", None, 'junk'),
    '1022':                                                     ("You're comparing yourself to me?^Ha! You're not even good enough to be my fake.", None, 'junk'),
    '1023':                                                     ("I'll make you eat those words.", None, 'junk'),
    '1024':                                                     ("What happened to Sheik?", None, 'junk'),
    '1025':                                                     ("L2P @.", None, 'junk'),
    '1026':                                                     ("I've heard Sploosh Kaboom is a tricky game.", None, 'junk'),
    '1027':                                                     ("I'm Lonk from Pennsylvania.", None, 'junk'),
    '1028':                                                     ("I bet you'd like to have more bombs.", None, 'junk'),
    '1029':                                                     ("When all else fails, use Fire.", None, 'junk'),
    '1030':                                                     ("Here's a hint, @. Don't be bad.", None, 'junk'),
    '1031':                                                     ("Game Over. Return of Ganon.", None, 'junk'),
    '1032':                                                     ("May the way of the Hero lead to the Triforce.", None, 'junk'),
    '1033':                                                     ("Can't find an item? Scan an Amiibo.", None, 'junk'),
    '1034':                                                     ("They say this game has just a few glitches.", None, 'junk'),
    '1035':                                                     ("BRRING BRRING This is Ulrira. Wrong number?", None, 'junk'),
    '1036':                                                     ("Tingle Tingle Kooloo Limpah", None, 'junk'),
    '1037':                                                     ("L is real 2041", None, 'junk'),
    '1038':                                                     ("They say that Ganondorf will appear in the next Mario Tennis.", None, 'junk'),
    '1039':                                                     ("Medigoron sells the earliest Breath of the Wild demo.", None, 'junk'),
    '1040':                                                     ("There's a reason why I am special inquisitor!", None, 'junk'),
    '1041':                                                     ("You were almost a @ sandwich.", None, 'junk'),
    '1042':                                                     ("I'm a helpful hint Gossip Stone!^See, I'm helping.", None, 'junk'),
    '1043':                                                     ("Dear @, please come to the castle. I've baked a cake for you.&Yours truly, princess Zelda.", None, 'junk'),
    '1044':                                                     ("They say all toasters toast toast.", None, 'junk'),
    '1045':                                                     ("They say that Okami is the best Zelda game.", None, 'junk'),
    '1046':                                                     ("They say that quest guidance can be found at a talking rock.", None, 'junk'),
    '1047':                                                     ("They say that the final item you're looking for can be found somewhere in Hyrule.", None, 'junk'),
    '1048':                                                     ("Mweep.^Mweep.^Mweep.^Mweep.^Mweep.^Mweep.^Mweep.^Mweep.^Mweep.^Mweep.^Mweep.^Mweep.", None, 'junk'),
    '1049':                                                     ("They say that Barinade fears Deku Nuts.", None, 'junk'),
    '1050':                                                     ("They say that Flare Dancers do not fear Goron-crafted blades.", None, 'junk'),
    '1051':                                                     ("They say that Morpha is easily trapped in a corner.", None, 'junk'),
    '1052':                                                     ("They say that Bongo Bongo really hates the cold.", None, 'junk'),
    '1053':                                                     ("They say that crouch stabs mimic the effects of your last attack.", None, 'junk'),
    '1054':                                                     ("They say that bombing the hole Volvagia last flew into can be rewarding.", None, 'junk'),
    '1055':                                                     ("They say that invisible ghosts can be exposed with Deku Nuts.", None, 'junk'),
    '1056':                                                     ("They say that the real Phantom Ganon is bright and loud.", None, 'junk'),
    '1057':                                                     ("They say that walking backwards is very fast.", None, 'junk'),
    '1058':                                                     ("They say that leaping above the Market entrance enriches most children.", None, 'junk'),
    '1059':                                                     ("They say that looking into darkness may find darkness looking back into you.", None, 'junk'),
    '1060':                                                     ("You found a spiritual Stone! By which I mean, I worship Nayru.", None, 'junk'),
    '1061':                                                     ("They say that the stick is mightier than the sword.", None, 'junk'),
    '1062':                                                     ("Open your eyes.^Open your eyes.^Wake up, @.", None, 'junk'),
    '1063':                                                     ("They say that arbitrary code execution leads to the credits sequence.", None, 'junk'),
    '1064':                                                     ("They say that Twinrova always casts the same spell the first three times.", None, 'junk'),
    '1065':                                                     ("They say that the Development branch may be unstable.", None, 'junk'),
    '1066':                                                     ("You're playing a Randomizer. I'm randomized!^Here's a random number:  #4#.&Enjoy your Randomizer!", None, 'junk'),
    '1067':                                                     ("They say Ganondorf's bolts can be reflected with glass or steel.", None, 'junk'),
    '1068':                                                     ("They say Ganon's tail is vulnerable to nuts, arrows, swords, explosives, hammers...^...sticks, seeds, boomerangs...^...rods, shovels, iron balls, angry bees...", None, 'junk'),
    '1069':                                                     ("They say that you're wasting time reading this hint, but I disagree. Talk to me again!", None, 'junk'),
    '1070':                                                     ("They say Ganondorf knows where to find the instrument of his doom.", None, 'junk'),
    '1071':                                                     ("I heard @ is pretty good at Zelda.", None, 'junk'),

    'Deku Tree':                                                ("an ancient tree", "Deku Tree", 'dungeonName'),
    'Dodongos Cavern':                                          ("an immense cavern", "Dodongo's Cavern", 'dungeonName'),
    'Jabu Jabus Belly':                                         ("the belly of a deity", "Jabu Jabu's Belly", 'dungeonName'),
    'Forest Temple':                                            ("a deep forest", "Forest Temple", 'dungeonName'),
    'Fire Temple':                                              ("a high mountain", "Fire Temple", 'dungeonName'),
    'Water Temple':                                             ("a vast lake", "Water Temple", 'dungeonName'),
    'Shadow Temple':                                            ("the house of the dead", "Shadow Temple", 'dungeonName'),
    'Spirit Temple':                                            ("the goddess of the sand", "Spirit Temple", 'dungeonName'),
    'Ice Cavern':                                               ("a frozen maze", "Ice Cavern", 'dungeonName'),
    'Bottom of the Well':                                       ("a shadow\'s prison", "Bottom of the Well", 'dungeonName'),
    'Gerudo Training Grounds':                                  ("the test of thieves", "Gerudo Training Grounds", 'dungeonName'),
    'Ganons Castle':                                            ("a conquered citadel", "Inside Ganon's Castle", 'dungeonName'),
    
    'Queen Gohma':                                              ("One inside an #ancient tree#...", "One in the #Deku Tree#...", 'boss'),
    'King Dodongo':                                             ("One within an #immense cavern#...", "One in #Dodongo's Cavern#...", 'boss'),
    'Barinade':                                                 ("One in the #belly of a deity#...", "One in #Jabu Jabu's Belly#...", 'boss'),
    'Phantom Ganon':                                            ("One in a #deep forest#...", "One in the #Forest Temple#...", 'boss'),
    'Volvagia':                                                 ("One on a #high mountain#...", "One in the #Fire Temple#...", 'boss'),
    'Morpha':                                                   ("One under a #vast lake#...", "One in the #Water Temple#...", 'boss'),
    'Bongo Bongo':                                              ("One within the #house of the dead#...", "One in the #Shadow Temple#...", 'boss'),
    'Twinrova':                                                 ("One inside a #goddess of the sand#...", "One in the #Spirit Temple#...", 'boss'),
    'Links Pocket':                                             ("One in #@'s pocket#...", "One #@ already has#...", 'boss'),

    'bridge_vanilla':                                           ("the #Shadow and Spirit Medallions# as well as the #Light Arrows#", None, 'bridge'),
    'bridge_stones':                                            ("Spiritual Stones", None, 'bridge'),
    'bridge_medallions':                                        ("Medallions", None, 'bridge'),
    'bridge_dungeons':                                          ("Spiritual Stones and Medallions", None, 'bridge'),
    'bridge_tokens':                                            ("Gold Skulltula Tokens", None, 'bridge'),

    'ganonBK_dungeon':                                          ("hidden somewhere #inside its castle#", None, 'ganonBossKey'),
    'ganonBK_vanilla':                                          ("kept in a big chest #inside its tower#", None, 'ganonBossKey'),
    'ganonBK_overworld':                                        ("hidden #outside of dungeons# in Hyrule", None, 'ganonBossKey'),
    'ganonBK_any_dungeon':                                      ("hidden #inside a dungeon# in Hyrule", None, 'ganonBossKey'),
    'ganonBK_keysanity':                                        ("hidden somewhere #in Hyrule#", None, 'ganonBossKey'),
    'ganonBK_triforce':                                         ("given to the Hero once the #Triforce# is completed", None, 'ganonBossKey'),

    'lacs_vanilla':                                             ("the #Shadow and Spirit Medallions#", None, 'lacs'),
    'lacs_medallions':                                          ("Medallions", None, 'lacs'),
    'lacs_stones':                                              ("Spiritual Stones", None, 'lacs'),
    'lacs_dungeons':                                            ("Spiritual Stones and Medallions", None, 'lacs'),
    'lacs_tokens':                                              ("Gold Skulltula Tokens", None, 'lacs'),

    'Spiritual Stone Text Start':                               ("3 Spiritual Stones found in Hyrule...", None, 'altar'),
    'Child Altar Text End':                                     ("\x13\x07Ye who may become a Hero...&Stand with the Ocarina and&play the Song of Time.", None, 'altar'),
    'Adult Altar Text Start':                                   ("When evil rules all, an awakening&voice from the Sacred Realm will&call those destined to be Sages,&who dwell in the \x05\x41five temples\x05\x40.", None, 'altar'),
    'Adult Altar Text End':                                     ("Together with the Hero of Time,&the awakened ones will bind the&evil and return the light of peace&to the world...", None, 'altar'),

    'Validation Line':                                          ("Hmph... Since you made it this far,&I'll let you know what glorious&prize of Ganon's you likely&missed out on in my tower.^Behold...^", None, 'validation line'),
    'Light Arrow Location':                                     ("Ha ha ha... You'll never beat me by&reflecting my lightning bolts&and unleashing the arrows from&", None, 'Light Arrow Location'),
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


# This specifies which hints will never appear due to either having known or known useless contents or due to the locations not existing.
def hintExclusions(world, clear_cache=False):
    if not clear_cache and hintExclusions.exclusions is not None:
        return hintExclusions.exclusions

    hintExclusions.exclusions = []
    hintExclusions.exclusions.extend(world.disabled_locations)

    for location in world.get_locations():
        if location.locked:
            hintExclusions.exclusions.append(location.name)

    world_location_names = [
        location.name for location in world.get_locations()]

    location_hints = []
    for name in hintTable:
        hint = getHint(name, world.clearer_hints)
        if any(item in hint.type for item in 
                ['always',
                 'sometimes',
                 'overworld',
                 'dungeon',
                 'song']):
            location_hints.append(hint)

    for hint in location_hints:
        if hint.name not in world_location_names and hint.name not in hintExclusions.exclusions:
            hintExclusions.exclusions.append(hint.name)

    return hintExclusions.exclusions

def nameIsLocation(name, hint_type, world):
    if isinstance(hint_type, (list, tuple)):
        for htype in hint_type:
            if htype in ['sometimes', 'song', 'overworld', 'dungeon', 'always'] and name not in hintExclusions(world):
                return True
    elif hint_type in ['sometimes', 'song', 'overworld', 'dungeon', 'always'] and name not in hintExclusions(world):
        return True
    return False

hintExclusions.exclusions = None

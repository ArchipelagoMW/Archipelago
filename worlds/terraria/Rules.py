class RuleConfig:
    def __init__(self, fishing, alt_prog, calamity):
        self.fishing = fishing
        self.alt_prog = alt_prog
        self.calamity = calamity

# 1
def npc_count_at_least(s, p, c, threshold, count_traveling_merchant = False, count_pets = True, count_old_man = False, count_santa = True):
    count = 0
    for npc in [
        lambda: merchant(),
        lambda: nurse(),
        lambda: demolitionist(),
        lambda: angler(),
        lambda: zoologist(),
        lambda: count_pets and cat(),
        lambda: count_pets and dog(),
        lambda: count_pets and bunny(),
        lambda: golfer(),
        lambda: arms_dealer(),
        lambda: stylist(),
        lambda: dryad(s, p, c),
        lambda: guide(s, p, c),
        lambda: tavernkeep(s, p),
        lambda: goblin_tinkerer(s, p),
        lambda: witch_doctor(s, p),
        lambda: (count_old_man and old_man(s, p, c)) or clothier(s, p),
        lambda: mechanic(s, p),
        lambda: wizard(s, p, c),
        lambda: tax_collector(s, p),
        lambda: truffle(s, p, c),
        lambda: pirate(s, p),
        lambda: steampunker(s, p, c),
        lambda: cyborg(s, p, c),
        lambda: count_santa and santa(s, p, c),
        lambda: count_traveling_merchant and threshold > 2 and traveling_merchant(s, p, c),
        lambda: threshold > 4 and dye_trader(s, p, c),
        lambda: threshold > 8 and painter(s, p, c),
        lambda: threshold > 14 and party_girl(s, p, c),
        lambda: threshold > 24 and princess(s, p, c),
    ]:
        if npc():
            count += 1
            if count >= threshold:
                return True
    return False

# 3
def pick_power(s, p, c, max):
    if max > 1000 and c.calamity and draedons_forge(s, p, c, 1000) and fragments(s, p, c) and luminite(s, p, c, 1000) and uelibloom(s, p, c, 1000) and shadowspec():
        return 1000
    if max > 250 and c.calamity and ancient_manipulator(s, p) and uelibloom(s, p, c, 250):
        return 250
    if max > 225 and ancient_manipulator(s, p) and fragments(s, p, c) and luminite(s, p, c, 225):
        return 225
    if max > 220 and c.calamity and ancient_manipulator(s, p) and astral():
        return 220
    if max > 210 and (golem() or (c.calamity and mythril(s, p, c, 210) and scoria(s, p, c, 210))):
        return 210
    if max > 200 and ((mythril(s, p, c, 200) and hallowed() and the_twins() and the_destroyer() and skeletron_prime()) or (c.alt_prog and ((wizard(s, p, c) and ectoplasm()) or autohammer()))):
        return 200
    if max > 180 and mythril(s, p, c, 180) and adamantite(s, p, c, 180):
        return 180
    if max > 150 and mythril(s, p, c, 180):
        return 150
    if max > 110 and cobalt():
        return 110
    if max > 100 and hellstone():
        return 100
    if max > 75 and c.calamity and aerialite():
        return 75
    return 65

def merchant(): return True
def nurse(): return True
def traveling_merchant(s, p, c): return npc_count_at_least(s, p, c, 2)
def demolitionist(): return True
def dye_trader(s, p, c): return npc_count_at_least(s, p, c, 4, True, count_old_man = True)
def angler(): return True
def zoologist(): return True
def cat(): return True
def dog(): return True # You can get a dog before any items
def bunny(): return False # I don't want to do the logic for this. It would be really slow anyway
def painter(s, p, c): return npc_count_at_least(s, p, c, 8, True, count_old_man = True)
def golfer(): return True
def arms_dealer(): return True
def stylist(): return True
def dryad(s, p, c): return (c.alt_prog and s.has("Post-King Slime"), p) or (not c.alt_prog and s.has_any({"Post-Eye of Cthulhu", "Post-Eater of World or Brain of Cthulhu", "Post-Skeletron"}, p))
def guide(s, p, c): return not c.alt_prog or s.has("Post-Eye of Cthulhu", p)
def tavernkeep(s, p): return s.has("Post-Eater of Worlds or Brain of Cthulhu", p)
def goblin_tinkerer(s, p): return s.has("Post-Goblin Army", p)
def hive(s, p, c): return not c.alt_prog or s.has("Post-King Slime", p)
def queen_bee(s, p, c): return hive(s, p, c)
def witch_doctor(s, p): return s.has("Post-Queen Bee", p)
def cyst(s, p, c): return not c.alt_prog or s.has("Post-Eater of Worlds or Brain of Cthulhu", p)
def old_man(s, p, c): return not c.alt_prog or s.has("Post-Goblin Army", p)
def skeletron(s, p, c): return old_man(s, p, c) or clothier(s, p)
def clothier(s, p): return s.has("Post-Skeletron", p)
def dungeon(s, p): return s.has("Post-Skeletron", p)
def mechanic(s, p): return dungeon(s, p)
def party_girl(s, p, c): return npc_count_at_least(s, p, c, 14, True, count_old_man = True)
def wall_of_flesh(s, p, c): return guide(s, p, c)
def hardmode_hammer(s, p, c, pick_pow):
    return wall_of_flesh() \
        or (s.has("Hardmode", p) and (not c.alt_prog or s.has("Post-Golem", p))) \
        or (truffle(s, p, c) and mech_boss_count(s, p) >= 1) \
        or (mythril(s, p, c, pick_pow) and chlorophyte()) \
        or (c.calamity and \
            ((mythril(s, p, c, pick_pow) and cryonic(s, p, c, pick_pow)) \
            or (ancient_manipulator(s, p) and astral()) \
            or (mythril(s, p, c, pick_pow) and twins()) \
            or (mythril(s, p, c, pick_pow) and scoria(s, p, c, pick_pow))))
def wizard(s, p, c): return s.has("Hardmode", p) and (not c.alt_prog or s.has("Post-Deerclops", p))
def tax_collector(s, p, c): return s.has("Hardmode", p) and dryad(s, p, c)
def truffle(s, p, c): return s.has("Hardmode", p) and (not c.alt_prog or not c.calamity or s.has("Crabulon", p))
def pirate(s, p): return s.has("Post-Pirate Invasion", p)
def mech_boss_count(s, p): return sum([s.has("Post-The Twins", p), s.has("Post-The Destroyer", p), s.has("Post-Skeletron Prime", p)])
def steampunker(s, p): return mech_boss_count(s, p) >= 1
def mythril(s, p, c, pick_pow): return (c.calamity and mech_boss_count(s, p) >= 1) or (not c.calamity and s.has("Hardmode", p) and hardmode_hammer(s, p, c, pick_pow)) and pick_power(s, p, c, pick_pow) >= 110
def adamantite(s, p, c, pick_pow): return (c.calamity and mech_boss_count(s, p) >= 2) or (not c.calamity and s.has("Hardmode", p)) and pick_power(s, p, c, pick_pow) >= 150
def cryonic(s, p, c, pick_pow): return s.has("Post-Cryogen", p) and adamantite() and pick_power(s, p, c, pick_pow) >= 180
def cyborg(s, p): return s.has_all({"Hardmode", "Post-Plantera"}, p)
def perennial(s, p, c, pick_pow): return s.has("Post-Plantera", p) and adamantite() and pick_power(s, p, c, pick_pow) >= 200
def scoria(s, p, c, pick_pow): return adamantite(s, p, c, pick_pow) and (s.has("Post-Golem") or pick_power(s, p, c, pick_pow) >= 210)
# 2
def frost_moon(s, p, c): return mythril(s, p, c) and ((c.alt_prog and wizard(s, p, c) and the_twins()) or (not c.alt_prog and ectoplasm() and skeletron_prime()))
def santa(s, p, c): return frost_moon(s, p, c) and s.has("Post-Frost Legion", p)
def ravager(s, p, c, pick_pow): return mythril() and pick_power(s, p, c, pick_pow) >= 210
def life_alloy(s, p, c, pick_pow): return (mythril(s, p, c, pick_pow) and cryonic(s, p, c, pick_pow) and perennial(s, p, c, pick_pow) and scoria(s, p, c, pick_pow)) or (ravager() and s.has("Post-Providence, the Profaned Goddess", p))
def lunatic_cultist(s, p): return s.has_all({"Post-Skeletron", "Hardmode", "Post-Golem"}, p)
def ancient_manipulator(s, p): return lunatic_cultist(s, p)
def lunar_events(s, p): return lunatic_cultist(s, p)
def astrum_deus(s, p, c): return s.has("Hardmode", p) and (not c.alt_prog or s.has("Post-Astrum Aureus", p))
def fragments(s, p, c): return lunar_events(s, p) or (c.calamity and astrum_deus(s, p, c))
def moon_lord(s, p): return lunar_events(s, p)
def luminite(s, p, c, pick_pow): return moon_lord(s, p) or (c.calamity and s.has("Post-Moon Lord", p) and pick_power(s, p, c, pick_pow) >= 225)
def phantoplasm(s, p): return dungeon(s, p) and s.has("Post-Moon Lord", p)
def unholy_essence(s, p): return s.has("Post-Moon Lord", p)
def profaned_guardians(s, p, c, pick_pow): return ancient_manipulator(s, p) and unholy_essence(s, p) and luminite(s, p, c, pick_pow)
def effulgent_feather(s, p, c): return s.has("Post-Moon Lord", p) or (ancient_manipulator(s, p) and life_alloy() and fragments(s, p, c))
def providence(s, p, c, pick_pow): return profaned_guardians(s, p, c, pick_pow)
def uelibloom(s, p, c, pick_pow): return adamantite() and s.has("Post-Providence", p) and pick_power(s, p, c, pick_pow) >= 225
def storm_weaver(s, p, c, pick_pow): return providence(s, p, c, pick_pow) and (not c.alt_prog or s.has("Post-Martian Madness", p))
def signus(s, p, c, pick_pow): return providence(s, p, c, pick_pow) and (not c.alt_prog or s.has("Post-Old One's Army Tier 3", p))
def ceaseless_void(s, p, c, pick_pow): return providence(s, p, c, pick_pow) and (not c.alt_prog or s.has("Post-Acid Rain Tier 2", p))
def polterghast(s, p, c, pick_pow): return dungeon() and s.has_all("Post-Moon Lord", p)
def devourer_of_gods(s, p, c, pick_pow): return ancient_manipulator(s, p) and ((luminite(s, p, c, pick_pow) and fragments(s, p, c) and s.has("Hardmode", p) and phantoplasm(s, p) and (not c.alt_prog or (uelibloom(s, p, c, pick_pow) and adamantite()))) or (storm_weaver(s, p, c, pick_pow) and signus() and ceaseless_void()))
def cosmilite(s, p, c, pick_pow): return devourer_of_gods(s, p, c, pick_pow)
def cosmic_anvil(s, p, c, pick_pow): return ancient_manipulator(s, p) and mythril(s, p, c, pick_pow) and cosmilite(s, p, c, pick_pow) and luminite(s, p, c, pick_pow) and fragments(s, p, c)
# 6
def yharon(s, p, c): return ancient_manipulator(s, p) and effulgent_feather() and life_alloy() and (not c.alt_prog or (polterghast() and reaper_shark() and s.has("Post-Polterghast")))
# 5
def auric(s, p, c, pick_pow): return cosmic_anvil(s, p, c, pick_pow) and s.has("Post-Yharon", p) and yharon() and pick_power(s, p, c, pick_pow) >= 250
# 4
def draedons_forge(s, p, c, pick_pow): return cosmic_anvil(s, p, c, pick_pow) and adamantite() and goblin_tinkerer(s, p) and auric(s, p, c, pick_pow) and exo() and ascendant_spirit()

# Old stuff above

def npc_count(x, count_pets = True, count_santa = True):
    npcs = [
        "Guide", "Golfer", "Merchant", "Nurse", "Dye Trader", "Demolitionist", "Tavernkeep",
        "Stylist", "Painter", "Goblin Tinkerer", "Arms Dealer", "Angler", "Dryad", "Party Girl",
        "Witch Doctor", "Clothier", "Mechanic", "Zoologist", "Wizard", "Truffle", "Tax Collector",
        "Pirate", "Steampunker", "Cyborg", "Princess",
    ]
    # I don't want to do the logic for the bunny lol
    if count_pets: npcs += ["Cat", "Dog"]
    if count_santa: npcs.append("Santa Claus")

    return x.count(npcs)

def mech_boss_count(x):
    return x.count(["Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime"])

# `s` is state
# `p` is player
# `c` is config
class Ctx:
    def __init__(self, s, p, c):
        self.s = s
        self.p = p
        self.c = c

    def has(self, item):
        self.s.has(item, self.p)

    def count(self, items):
        count = 0
        for item in items:
            if self.has(item):
                count += 1
        return count

def get_rules(p, c):
    # TODO It's probably really slow to create this dictionary so many times!
    return {
        # Events
        "Guide": lambda s: not c.alt or s.has("Post-King Slime", p),
        "Golfer": lambda s: not c.alt or s.has("Post-King Slime", p),
        "Merchant": lambda s: not c.alt or s.has("Post-Eye of Cthulhu", p),
        "Nurse": lambda s: s.has("Merchant", p),
        "Dye Trader": lambda s: npc_count(Ctx(s, p, c), True) >= 4,
        "Dye Vat": lambda s: s.has("Dye Trader", p),
        "Demolitionist": lambda s: s.has("Merchant", p),
        "Tavernkeep": lambda s: s.has("Post-Evil Boss", p),
        "Stylist": lambda s: not c.alt or s.has("Post-Evil Boss", p),
        "Painter": lambda s: npc_count(Ctx(s, p, c), True) >= 8,
        "Goblin Tinkerer": lambda s: s.has("Post-Goblin Army", p),
        "Arms Dealer": lambda s: c.alt or s.has("Post-Goblin Army", p),
        "Old Man": lambda s: (not c.alt or s.has("Post-Old One's Army Tier 1", p)),
        "Angler": lambda s: (not c.alt or s.has("Post-Old One's Army Tier 1", p)),
        "Hive": lambda s: not c.alt or s.has("Post-King Slime", p),
        "Bee Wax": lambda s: s.can_reach("Queen Bee", "Location", p),
        "Dryad": lambda s: s.has("Post-Queen Bee", p) or (not c.alt and s.has_any({
            "Post-Eye of Cthulhu", "Post-Evil Boss", "Post-Skeletron",
        }, p)),
        "Party Girl": lambda s: npc_count(Ctx(s, p, c), True) >= 14, # Alt: Spawns as often as other NPCs
        "Witch Doctor": lambda s: s.has("Post-Queen Bee", p),
        "Clothier": lambda s: s.has("Post-Skeletron", p),
        "Mechanic": lambda s: s.has("Post-Skeletron", p),
        "Dungeon": lambda s: s.has("Post-Skeletron", p),
        "Zoologist": lambda s: not c.alt or s.has("Post-Deerclops", p),
        "Cat": lambda s: s.has("Zoologist", p),
        "Dog": lambda s: s.has("Zoologist", p), # You can get a dog before any other items
        "Wizard": lambda s: s.has("Hardmode", p), #
        "Truffle": lambda s: s.has("Hardmode", p), #
        "Tax Collector": lambda s: s.has_all({"Dryad", "Hardmode"}, p),
        "Pirate": lambda s: s.has("Post-Pirate Invasion", p),
        "Steampunker": lambda s: mech_boss_count(Ctx(s, p, c)) >= 1, #
        "Cyborg": lambda s: s.has("Post-Plantera", p), #
        "Princess": lambda s: s.has_all({
            "Guide", "Golfer", "Merchant", "Nurse", "Dye Trader", "Demolitionist", "Tavernkeep",
            "Stylist", "Painter", "Goblin Tinkerer", "Arms Dealer", "Old Man", "Angler", "Dryad",
            "Party Girl", "Witch Doctor", "Clothier", "Mechanic", "Zoologist", "Wizard", "Truffle",
            "Tax Collector", "Pirate", "Steampunker", "Cyborg",
        }, p),
        "Christmas": lambda s: s.can_reach("Frost Moon", "Location", p),
        "Santa Claus": lambda s: s.has("Post-Frost Legion") and s.has("Christmas", p),

        # Calamity Events
        "Calamity Evil Boss Summon": lambda s: not c.alt or s.has("Post-Evil Boss", p),

        # Solidifier: King Slime
        # Dye Vat: Misc
        # Tinkerer's Workshop: Post-Goblin Army
        # Imbuing Station: Post-Queen Bee
        # Alchemy Table: Post-Skeletron
        # Crystal Ball: Hardmode, Post-Deerclops?
        # Blend-O-Matic: Post-1 Mech Boss
        # Steampunk Boiler: Post-1 Mech Boss, Post-Eye, Post-Evil, Post-Skeletron
        # Chlorophyte Extractinator: Post-3 Mech Bosses
        # Autohammer: Hardmode, Post-Plantera
        # Lihzahrd Furnace: Post-Plantera or good pick
        # Cauldron: Post-Queen Bee, Pumpkin Moon

        # Locations
        "Timber!!": None,
        "Benched": None,
        "Stop! Hammer Time!": None,
        "Ooo! Shiny!": None,
        "No Hobo": None,
        "Lucky Break": None,
        "Star Power": None,
        "You Can Do It!": None,
        "Throwing Lines": None,
        "Heavy Metal": None,
        "Hold on Tight!": None,
        "Matching Attire": None,
        "Fashion Statement": None,
        "Watch Your Step!": None,
        "Vehicular Manslaughter": None,
        "I Am Loot!": None,
        "Heart Breaker": None,
        "Dead Men Tell No Tales": None,
        "Jeepers Creepers": None,
        "There are Some Who Call Him...": None,
        "Deceiver of Fools": None,
        "Pretty in Pink": None,
        "Dye Hard": lambda s: s.has("Dye Trader", p),
        "Into Orbit": None,
        "Heliophobia": None,
        "A Rather Blustery Day": None,
        "Servant-in-Training": lambda s: s.has("Angler", p),
        "10 Fishing Quests": lambda s: s.has("Angler", p),
        "Trout Monkey": lambda s: s.has("Angler", p),
        "Glorious Golden Pole": lambda s: s.has("Angler", p),
        "Fast and Fishious": lambda s: s.has("Angler", p),
        "Supreme Helper Minion!": lambda s: s.has("Angler", p),
        "Torch God": None,
        "Like a Boss": None,
        "Sticky Situation": None,
        "King Slime": lambda s: not c.alt or s.has("Dye Vat", p),
        "The Cavalry": None,
        "Desert Scourge": lambda s: not c.alt or s.can_reach("King Slime", "Location", p),
        "Giant Clam": lambda s: s.has("Post-Desert Scourge", p),
        "Bloodbath": None,
        "Til Death...": None,
        "Quiet Neighborhood": None,
        "Feeling Petty": lambda s: s.has_any({"Cat", "Dog"}, p),
        "Eye of Cthulhu": None,
        "Acid Rain Tier 1": lambda s: s.has("Post-Eye of Cthulhu", p),
        "Crabulon": None,
        "Smashing, Poppet!": None,
        "Evil Boss": None,
        "Leading Landlord": lambda s: s.has_all({"Guide", "Clothier", "Zoologist"}, p)
            or s.has_all({"Merchant", "Golfer", "Nurse"}, p)
            or s.has_all({"Zoologist", "Witch Doctor"}, p)
            or s.has_all({"Golfer", "Angler"}, p)
            or (s.has_all({"Nurse", "Arms Dealer"}, p) and s.has_any({"Wizard", "Hardmode"}, p))
            or (
                s.has_all({"Tavernkeep", "Demolitionist"}, p)
                and s.has_any({"Goblin Tinkerer", "Hardmode"}, p)
            )
            or (s.has("Party Girl", p) and (
                s.has_all({"Hardmode", "Wizard"}, p)
                or s.has_all({"Hardmode", "Zoologist"}, p)
                or s.has_all({"Wizard", "Zoologist"}, p)
                or s.has_all({"Wizard", "Stylist"}, p)
                or s.has_all({"Zoologist", "Stylist"}, p)
            ))
            or (s.has_all({"Wizard", "Golfer"}, p) and s.has_any({"Hardmode", "Merchant"}), p)
            or s.has_all({"Demolitionist", "Tavernkeep"}, p)
            or s.has_all({"Goblin Tinkerer", "Mechanic"}, p)
            or s.has_all({"Clothier", "Truffle", "Tax Collector"}, p)
            or s.has_all({"Dye Trader", "Arms Dealer", "Painter"}, p)
            or s.has_all({"Arms Dealer", "Nurse"}, p)
            or s.has_all({"Steampunker", "Cyborg"}, p)
            or s.has_all({"Painter", "Dryad"}, p)
            or s.has_all({"Witch Doctor", "Dryad", "Guide"}, p)
            or s.has_all({"Stylist", "Dye Trader"}, p)
            or (s.has("Angler", p) and (
                s.has_all({"Demolitionist", "Party Girl"}, p)
                or s.has_all({"Demolitionist", "Tax Collector"}, p)
                or s.has_all({"Party Girl", "Tax Collector"}, p)
            ))
            or s.has_all({"Pirate", "Angler"}, p)
            or s.has_all({"Mechanic", "Goblin Tinkerer"}, p)
            or s.has_all({"Tax Collector", "Merchant"}, p)
            or (s.has("Cyborg", p) and (
                s.has_all({"Steampunker", "Pirate"}, p)
                or s.has_all({"Steampunker", "Stylist"}, p)
                or s.has_all({"Pirate", "Stylist"}, p)
            ))
            or s.has_all({"Truffle", "Guide"}, p)
            or s.has("Princess", p),
        "Completely Awesome": lambda s: s.has("Arms Dealer"),
        "Goblin Army": None,
        "Old One's Army Tier 1": lambda s: s.has("Tavernkeep", p),
        "Archaeologist": None,
        "Where's My Honey?": lambda s: s.has("Hive", p),
        "Queen Bee": lambda s: s.has("Hive", p),
        "Not the Bees!": lambda s: s.can_reach("Queen Bee", "Location", p) and s.has("Bee Wax", p),
        "The Frequent Flyer": None,
        "Calamity Evil Boss": lambda s: s.has("Calamity Evil Boss Summon", p),
        "Skeletron": lambda s: s.has("Old Man", p) or s.has_all({"Clothier", "Dungeon"}, p), # Alt: Clothier Voodoo Doll is much more common
        "Dungeon Heist": lambda s: s.has("Dungeon", p),
        "Jolly Jamboree": lambda s: s.has("Party Girl", p),
        "Deerclops": lambda s: None,
        "It's Getting Hot in Here": lambda s: None,
        "Rock Bottom": lambda s: None,
        "Miner for Fire": lambda s: None,
        "Hot Reels!": lambda s: None,
        "Boots of the Hero": lambda s: None,
        "The Slime God": lambda s: None,
        "Marathon Medalist": lambda s: None,
        "Wall of Flesh": lambda s: None,
        "Begone, Evil!": lambda s: None,
        "Extra Shiny!": lambda s: None,
        "Head in the Clouds": lambda s: None,
        "Gelatin World Tour": lambda s: None,
        "Don't Dread on Me": lambda s: None,
        "Pirate Invasion": lambda s: None,
        "Earth Elemental": lambda s: None,
        "Cloud Elemental": lambda s: None,
        "Queen Slime": lambda s: None,
        "Aquatic Scourge": lambda s: None,
        "Cragmaw Mire": lambda s: None,
        "Acid Rain Tier 2": lambda s: None,
        "The Twins": lambda s: None,
        "Prismancer": lambda s: None,
        "Get a Life": lambda s: None,
        "Topped Off": lambda s: None,
        "Old One's Army Tier 2": lambda s: None,
        "Brimstone Elemental": lambda s: None,
        "The Destroyer": lambda s: None,
        "Cryogen": lambda s: None,
        "Skeletron Prime": lambda s: None,
        "Buckets of Bolts": lambda s: None,
        "Drax Attax": lambda s: None,
        "Photosynthesis": lambda s: None,
        "Mecha Mayhem": lambda s: None,
        "Calamitas": lambda s: None,
        "Plantera": lambda s: None,
        "Temple Raider": lambda s: None,
        "Robbing the Grave": lambda s: None,
        "Big Booty": lambda s: None,
        "Rainbows and Unicorns": lambda s: None,
        "Funkytown": lambda s: None,
        "It Can Talk?!": lambda s: None,
        "Real Estate Agent": lambda s: None,
        "Armored Digger": lambda s: None,
        "Kill the Sun": lambda s: None,
        "Sword of the Hero": lambda s: None,
        "Great Sand Shark": lambda s: None,
        "Leviathan and Anahita": lambda s: None,
        "Astrum Aureus": lambda s: None,
        "Golem": lambda s: None,
        "Old One's Army Tier 3": lambda s: None,
        "Martian Madness": lambda s: None,
        "Plaguebringer": lambda s: None,
        "The Plaguebringer Goliath": lambda s: None,
        "Duke Fishron": lambda s: None,
        "Mourning Wood": lambda s: None,
        "Pumpking": lambda s: None,
        "Baleful Harvest": lambda s: None,
        "Everscream": lambda s: None,
        "Santa-NK1": lambda s: None,
        "Ice Queen": lambda s: None,
        "Ice Scream": lambda s: None,
        "Frost Legion": lambda s: None,
        "Ravager": lambda s: None,
        "Empress of Light": lambda s: None,
        "Lunatic Cultist": lambda s: None,
        "Lunar Events": lambda s: None,
        "Astrum Deus": lambda s: None,
        "Moon Lord": lambda s: None,
        "Slayer of Worlds": lambda s: None,
        "Sick Throw": lambda s: None,
        "You and What Army?": lambda s: None,
        "Zenith": lambda s: None,
        "Profaned Guardians": lambda s: None,
        "The Dragonfolly": lambda s: None,
        "Providence, the Profaned Goddess": lambda s: None,
        "Storm Weaver": lambda s: None,
        "Ceaseless Void": lambda s: None,
        "Signus, Envoy of the Devourer": lambda s: None,
        "Polterghast": lambda s: None,
        "Colossal Squid": lambda s: None,
        "Reaper Shark": lambda s: None,
        "Eidolon Wyrm": lambda s: None,
        "Mauler": lambda s: None,
        "Nuclear Terror": lambda s: None,
        "Acid Rain Tier 3": lambda s: None,
        "The Old Duke": lambda s: None,
        "The Devourer of Gods": lambda s: None,
        "Jungle Dragon, Yharon": lambda s: None,
        "Exo Mechs": lambda s: None,
        "Supreme Calamitas": lambda s: None,
        "Bulldozer": lambda s: None,
        "Adult Eidolon Wyrm": lambda s: None,
    }
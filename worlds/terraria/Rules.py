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

# s is state
# p is player
# c is config
def get_rules(p, c):
    return {
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
        "Dye Hard": lambda s: dye_trader(s, p, c),
        "Into Orbit": None,
        "Heliophobia": None,
        "A Rather Blustery Day": None,
        "Servant-in-Training": None,
        "10 Fishing Quests": None,
        "Trout Monkey": None,
        "Glorious Golden Pole": None,
        "Fast and Fishious": None,
        "Supreme Helper Minion!": None,
        "Torch God": None,
        "Like a Boss": None,
        "Sticky Situation": None,
        "King Slime": None,
        "The Cavalry": None,
        "Desert Scourge": None,
        "Giant Clam": lambda s: s.has("Post-Desert Scourge", p),
        "Bloodbath": None,
        "Til Death...": None,
        "Quiet Neighborhood": None,
        "Feeling Petty": None,
        "Eye of Cthulhu": None,
        "Acid Rain Tier 1": lambda s: s.has("Post-Eye of Cthulhu", p),
        "Crabulon": None,
        "Smashing, Poppet!": None,
        "Eater of Worlds or Brain of Cthulhu": None,
        "Leading Landlord": None,
        "Completely Awesome": None,
        "Goblin Army": None,
        "Old One's Army Tier 1": lambda s: tavernkeep(s, p),
        "Archaeologist": None,
        "Where's My Honey?": lambda s: hive(s, p, c),
        "Queen Bee": lambda s: queen_bee(s, p, c),
        "Not the Bees!": lambda s: queen_bee(s, p, c),
        "The Frequent Flyer": None,
        "The Hive Mind or The Perforators": lambda s: cyst(s, p, c),
        "Skeletron": lambda s: skeletron(s, p, c),
        "Dungeon Heist": lambda s: dungeon(s, p, c),
        "Jolly Jamboree": lambda s: party_girl(s, p, c),
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
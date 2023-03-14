from typing import Callable, Optional
from BaseClasses import CollectionState

class RuleConfig:
    def __init__(self, calamity: bool):
        self.clam = calamity

class Ctx:
    def __init__(self, state: CollectionState, player: int, config: RuleConfig):
        self.state = state
        self.player = player
        self.clam = config.clam

    def has(self, item: str) -> bool:
        self.state.has(item, self.player)

    def has_all(self, items: set[str]) -> bool:
        self.state.has_all(items, self.player)

    def count(self, items: list[str]) -> int:
        count = 0
        for item in items:
            if self.has(item):
                count += 1
        return count
    
    def can_reach(self, location: str) -> bool:
        self.state.can_reach(location, "Location", self.player)
        # self.s.multiworld.get_location(location, self.p).access_rule(self.s)

def npc_count(x: Ctx, count_pets = True, count_santa = True, count_old_man = True) -> int:
    npcs = [
        "Guide", "Merchant", "Nurse", "Demolitionist", "Dye Trader", "Angler", "Zoologist",
        "Painter", "Golfer", "Arms Dealer", "Tavernkeep", "Stylist", "Party Girl", "Dryad",
        "Goblin Tinkerer", "Witch Doctor", "Mechanic", "Wizard", "Truffle", "Tax Collector",
        "Pirate", "Steampunker", "Cyborg", "Princess",
    ]

    if count_pets: npcs += ["Cat", "Dog"] # I don't want to do the logic for the bunny lol
    if count_santa: npcs.append("Santa Claus")
    if not count_old_man: npcs.append("Clothier")

    count = x.count(npcs)
    if count_old_man:
        count += 1
    return count

def pick_power(x: Ctx) -> int:
    if x.clam and x.has("Crystyl Crusher"):
        return 1000
    if x.clam and x.has("Blossom Pickaxe"):
        return 250
    if x.has("Luminite Pickaxe"):
        return 225
    if x.clam and x.has("Genesis Pickaxe"):
        return 225
    if x.clam and x.has("Astral Pickaxe"):
        return 220
    if x.has("Picksaw"):
        return 210
    if x.clam and x.has("Seismic Hampick"):
        return 210
    if x.has_any({
        "Shroomite Digging Claw", "Pickaxe Axe", "Chlorophyte Pickaxe", "Spectre Pickaxe"
    }):
        return 200
    if x.clam and x.has("Beastial Pickaxe"):
        return 200
    if x.has("Adamantite Pickaxe"):
        return 180
    if x.clam and x.has("Shardlight Pickaxe"):
        return 180
    if x.has("Mythril Pickaxe"):
        return 150
    if x.has("Cobalt Pickaxe"):
        return 110
    if x.has("Molten Pickaxe"):
        return 100
    if x.clam and x.has("Gelpick"):
        return 100
    if x.clam and x.has("Skyfringe Pickaxe"):
        return 75
    if x.has("Evil Pickaxe"):
        return 65
    return 59

def hammer_power(x: Ctx) -> int:
    if x.clam and x.has("Grax"):
        return 110
    if x.has_any({"The Axe", "Luminite Hamaxe"}):
        return 100
    if x.clam and x.has_any({"Astral Hamaxe", "Hydraulic Volt Crasher"}):
        return 100
    if x.clam and x.has("Seismic Hampick"):
        return 95
    if x.has_any({"Spectre Hamaxe", "Chlorophyte Warhammer"}):
        return 90
    if x.clam and x.has("Abyssal Warhammer"):
        return 88
    if x.has_any({"Hammush", "Pwnhammer"}):
        return 85
    if x.has("Pwnhammer"):
        return 80
    if x.has("Molten Hamaxe"):
        return 70
    if x.clam and x.has_any({"Aerial Hamaxe", "Depth Crusher"}):
        return 70
    if x.has("Meteor Hamaxe"):
        return 60
    if x.clam and x.has("Reefclaw Hamaxe"):
        return 60
    return 55

def mech_boss_count(x: Ctx) -> int:
    return x.count(["Post-The Twins", "Post-The Destroyer", "Post-Skeletron Prime"])

# TODO Verify Hardmode "Post-" flags in code
# TODO Vanilla changes and recipes in Calamity wiki
# TODO Detail pass
# TODO Typing
# TODO Hook up to world

event_rules: dict[str, Optional[Callable[[Ctx], bool]]] = {
    # Events
    "Copper Shortsword": None,
    "Guide": None,
    "Merchant": None,
    "Bug Net": lambda x: x.has("Merchant"),
    "Nurse": None,
    "Demolitionist": None,
    "Dye Trader": lambda x: npc_count(x) >= 4,
    "Angler": None,
    "Zoologist": None,
    "Cat": lambda x: x.has("Zoologist"),
    "Dog": lambda x: x.has("Zoologist"), # You can get a dog before any other items
    "Painter": lambda x: npc_count(x) >= 8,
    "Golfer": None,
    "Arms Dealer": None,
    "Stylist": None,
    "Enchanted Sword": None,
    "Starfury": None,
    "Evil Sword": None,
    "Blade of Grass": None,
    "Solidifier": lambda x: x.can_reach("King Slime"),
    "Sandstorm": None,
    "Dryad": lambda x: x.has_any({"Post-Eye of Cthulhu", "Post-Evil Boss", "Post-Skeletron"}),
    "Purification Powder": lambda x: x.has("Dryad"), # Shimmered from Evil Powder in 1.4.4. Not bought from Dryad in get fixed boi.
    "Pumpkin Seeds": lambda x: x.has("Dryad"),
    "Pumpkin": lambda x: x.has("Pumpkin Seeds"),
    "Party Girl": lambda x: npc_count(x) >= 14,
    "Evil Boss Part": lambda x: x.can_reach("Evil Boss"),
    "Evil Pickaxe": lambda x: x.has("Evil Boss Part"),
    "Tavernkeep": lambda x: x.has("Post-Evil Boss"),
    "Meteorite": lambda x: x.has("Post-Evil Boss") and pick_power(x) >= 50,
    "Meteorite Bar": lambda x: x.has("Meteorite"),
    "Meteor Hamaxe": lambda x: x.has("Meteorite Bar"),
    "Goblin Tinkerer": lambda x: x.has("Post-Goblin Army"),
    "Tinkerer's Workshop": lambda x: x.has("Goblin Tinkerer"),
    "Rocket Boots": lambda x: x.has("Goblin Tinkerer"),
    "Spectre Boots": lambda x: x.has("Rocket Boots"),
    "Lightning Boots": lambda x: x.has("Spectre Boots"),
    "Frostspark Boots": lambda x: x.has("Lightning Boots"),
    "Terraspark Boots": lambda x: x.has("Frostspark Boots"),
    "Bee Wax": lambda x: x.can_reach("Queen Bee"),
    "Bee Keeper": lambda x: x.can_reach("Queen Bee"),
    "Witch Doctor": lambda x: x.has("Post-Queen Bee"),
    "Clothier": lambda x: x.has("Post-Skeletron"),
    "Dungeon": lambda x: x.has("Post-Skeletron"),
    "Bone": lambda x: x.has("Dungeon"),
    "Mechanic": lambda x: x.has("Dungeon"),
    "Wire": lambda x: x.has("Mechanic"),
    "Actuator": lambda x: x.has("Mechanic"),
    "Muramasa": lambda x: x.has("Dungeon"),
    "Hellforge": lambda x: pick_power(x) >= 60,
    "Hellstone": lambda x: x.has("Hardmode") or pick_power(x) >= 65,
    "Hellstone Bar": lambda x: x.has("Hellstone"),
    "Fiery Greatsword": lambda x: x.has("Hellstone Bar"),
    "Molten Pickaxe": lambda x: x.has("Hellstone Bar"),
    "Molten Hamaxe": lambda x: x.has("Hellstone Bar"),
    "Night's Edge": lambda x:
        x.has_all({"Evil Sword", "Muramasa", "Blade of Grass", "Fiery Greatsword"}),
    "Pwnhammer": lambda x: x.can_reach("Wall of Flesh"),
    "Wizard": lambda x: x.has("Hardmode"),
    "Truffle": lambda x: x.has("Hardmode"),
    "Tax Collector": lambda x: x.has_all({"Purification Powder", "Hardmode"}),
    "Altar": lambda x: x.has("Hardmode") and hammer_power(x) >= 80,
    "Cobalt Ore": lambda x: x.has("Altar") and pick_power(x) >= 100,
    "Cobalt Bar": lambda x: x.has("Cobalt Ore"),
    "Cobalt Pickaxe": lambda x: x.has("Cobalt Bar"),
    "Soul of Night": lambda x: x.has("Hardmode"),
    "Hallow": lambda x: x.has("Hardmode"),
    "Pixie Dust": lambda x: x.has("Hallow"),
    "Crystal Shard": lambda x: x.has("Hallow"),
    "Soul of Light": lambda x: x.has("Hallow"),
    "Blessed Apple": lambda x: x.has("Hallow"),
    "Rod of Discord": lambda x: x.has("Hallow"),
    "Forbidden Fragment": lambda x: x.has_all({"Sandstorm", "Hardmode"}),
    "Pirate": lambda x: x.has("Post-Pirate Invasion"),
    "Soul of Sight": lambda x: x.can_reach("The Twins"),
    "Steampunker": lambda x: mech_boss_count(x) >= 1,
    "Hammush": lambda x: x.has("Truffle") and mech_boss_count(x) >= 1,
    "Mythril Ore": lambda x: x.has("Altar") and pick_power(x) >= 110,
    "Mythril Bar": lambda x: x.has("Mythril Ore"),
    "Hardmode Anvil": lambda x: x.has("Mythril Bar"),
    "Mythril Pickaxe": lambda x: x.has_all({"Hardmode Anvil", "Mythril Bar"}),
    "Rainbow Rod": lambda x: x.has_all({
        "Hardmode Anvil", "Crystal Shard", "Unicorn Horn", "Pixie Dust", "Soul of Light",
        "Soul of Sight",
    }),
    "Life Fruit": lambda x: mech_boss_count(x) >= 1,
    "Soul of Might": lambda x: x.can_reach("The Destroyer"),
    "Adamantite Ore": lambda x: x.has("Altar") and pick_power(x) >= 150,
    "Hardmode Forge": lambda x: x.has_all({"Hardmode Anvil", "Adamantite Ore", "Hellforge"}),
    "Adamantite Bar": lambda x: x.has_all({"Hardmode Forge", "Adamantite Ore"}),
    "Adamantite Pickaxe": lambda x: x.has_all({"Hardmode Anvil", "Adamantite Bar"}),
    "Soul of Fright": lambda x: x.can_reach("Skeletron Prime"),
    "Hallowed Bar": lambda x: x.can_reach_any(["The Twins", "The Destroyer", "Skeletron Prime"]),
    "Pickaxe Axe": lambda x: x.has_all({
        "Hardmode Anvil", "Hallowed Bar", "Soul of Fright", "Soul of Might", "Soul of Sight",
    }),
    "True Night's Edge": lambda x: x.has_all({
        "Hardmode Anvil", "Night's Edge", "Soul of Fright", "Soul of Might", "Soul of Sight",
    }),
    "Chlorophyte Ore": lambda x: x.has("Hardmode") and pick_power(x) >= 200,
    "Chlorophyte Bar": lambda x: x.has_all({"Hardmode Forge", "Chlorophyte Ore"}),
    "True Excalibur": lambda x: x.has_all({"Hardmode Anvil", "Excalibur", "Chlorophyte Bar"}),
    "Chlorophyte Pickaxe": lambda x: x.has_all({"Hardmode Anvil", "Chlorophyte Bar"}),
    "Chlorophyte Warhammer": lambda x: x.has_all({"Hardmode Anvil", "Chlorophyte Bar"}),
    "Ashes of Calamity": lambda x: x.can_reach("Calamitas Clone"),
    "The Axe": lambda x: x.can_reach("Plantera"),
    "Cyborg": lambda x: x.has("Post-Plantera"),
    "Princess": lambda x: x.npc_count(x, False, False, False) >= 24,
    "Autohammer": lambda x: x.has_all({"Truffle", "Post-Plantera"}),
    "Shroomite Bar": lambda x: x.has_all({"Autohammer", "Chlorophyte Bar"}),
    "Shroomite Digging Claw": lambda x: x.has_all({"Hardmode Anvil", "Shroomite Bar"}),
    "Ectoplasm": lambda x: x.has_all({"Post-Plantera", "Dungeon"}),
    "Spectre Bar": lambda x: x.has_all({"Hardmode Forge", "Chlorophyte Bar", "Ectoplasm"}),
    "Spectre Pickaxe": lambda x: x.has_all({"Hardmode Anvil", "Spectre Bar"}),
    "Spectre Hamaxe": lambda x: x.has_all({"Hardmode Anvil", "Spectre Bar"}),
    "Rainbow Gun": lambda x: x.can_reach("Big Booty"),
    "Lihzahrd Temple": lambda x: x.can_reach("Plantera") or (x.has_all("Post-Plantera", "Actuator"))
        or pick_power(x) >= 210, # Review this
    "Solar Eclipse": lambda x: x.has("Lihzahrd Temple"),
    "Broken Hero Sword": lambda x: x.has_all({"Solar Eclipse", "Post-Plantera"}),
    "Terra Blade": lambda x:
        x.has_all({"Hardmode Anvil", "True Night's Edge", "True Excalibur", "Broken Hero Sword"}),
    "Picksaw": lambda x: x.can_reach("Golem"),
    "Lihzahrd Brick": lambda x: pick_power(x) >= 210,
    "Influx Waver": lambda x: x.can_reach("Martian Madness"),
    "Pumpkin Moon": lambda x: x.has_all({"Hardmode Anvil", "Pumpkin", "Ectoplasm", "Hallowed Bar"}),
    "The Horseman's Blade": lambda x: x.can_reach("Pumpking"),
    "Frost Moon": lambda x: x.has_all({"Hardmode Anvil", "Ectoplasm", "Soul of Fright"}),
    "Christmas": lambda x: x.has("Frost Moon"),
    "Santa Claus": lambda x: x.has_all({"Post-Frost Legion", "Christmas"}),
    "Ancient Manipulator": lambda x: x.can_reach("Lunatic Cultist"),
    "Fragment": lambda x: x.has("Lunar Events"),
    "Luminite": lambda x: x.can_reach("Moon Lord"),
    "Luminite Bar": lambda x: x.has_all({"Ancient Manipulator", "Luminite"}),
    "Luminite Pickaxe": lambda x: x.has_all({"Ancient Manipulator", "Fragment", "Luminite Bar"}),
    "Luminite Hamaxe": lambda x: x.has_all({"Ancient Manipulator", "Fragment", "Luminite Bar"}),
    "Terrarian": lambda x: x.can_reach("Moon Lord"),
    "Meowmere": lambda x: x.can_reach("Moon Lord"),
    "Star Wrath": lambda x: x.can_reach("Moon Lord"),
}

calamity_event_rules: dict[str, Optional[Callable[[Ctx], bool]]] = {
    # Calamity Events
    "Feller of Evergreens": None,
    "Mysterious Circuitry": None,
    "Dubious Plating": None,
    "Charging Station": None,
    "Codebreaker Base": lambda x:
        x.has_all({"Charging Station", "Mysterious Circuitry", "Dubious Plating"}),
    "Pearl Shard": lambda x: x.can_reach("Desert Scourge"),
    "Sea Remains": lambda x: x.has("Pearl Shard"),
    "Reefclaw Hamaxe": lambda x: x.has("Sea Remains"),
    "Amidias": lambda x: x.has("Post-Desert Scourge") and x.can_reach("Giant Clam"),
    "Aerialite Ore": lambda x: x.can_reach("Calamity Evil Boss") and pick_power(x) >= 65,
    "Aerialite Bar": lambda x: x.has("Aerialite Ore"),
    "Skyfringe Pickaxe": lambda x: x.has("Aerialite Bar"),
    "Aerial Hamaxe": lambda x: x.has("Aerialite Bar"),
    "Decryption Computer": lambda x: x.has_all({"Mysterious Circuitry", "Dubious Plating", "Wire"}),
    "Brimstone Slag": lambda x: pick_power(x) >= 100,
    "Purified Gel": lambda x: x.can_reach("The Slime God"),
    "Static Refiner": lambda x: x.has_all({"Purified Gel", "Solidifier"}),
    "Gelpick": lambda x: x.has_all({"Static Refiner", "Purified Gel"}),
    "Axe of Purity": lambda x:
        x.has_all({"Feller of Evergreens", "Purification Powder", "Pixie Dust", "Crystal Shard"}),
    "Astral Infection": lambda x: x.has("Hardmode"),
    "Stardust": lambda x:
        x.has("Astral Infection") or x.can_reach_any(["Astrum Aureus", "Astrum Deus"]),
    "Titan Heart": lambda x: x.has("Astral Infection"),
    "Essence of Sunlight": lambda x: x.has("Hardmode") or x.can_reach("Golem"),
    "Essence of Eleum": lambda x: x.has_any({"Hardmode", "Post-Cryogen"}) or x.can_reach("Cryogen"),
    "Essence of Havoc": lambda x:
        x.has("Hardmode") or x.can_reach_any({"Calamitas Clone", "Brimstone Elemental"}),
    "Infernal Suevite": lambda x: pick_power(x) >= 150 or x.has("Post-Brimstone Elemental"),
    "Unholy Core": lambda x: x.has_all({"Infernal Suevite", "Hellstone"}),
    "Long Ranged Sensor Array": lambda x: x.has_all({
        "Hardmode Anvil", "Mysterious Circuitry", "Dubious Plating", "Mythril Bar", "Wire",
        "Decryption Computer", "Codebreaker Base",
    }),
    "Hydraulic Volt Crasher": lambda x: x.has_all({
        "Hardmode Anvil", "Mysterious Circuitry", "Dubious Plating", "Mythril Bar", "Soul of Sight",
    }),
    "Cryonic Ore": lambda x:
        x.has("Post-Cryogen") and (pick_power(x) >= 180 or mech_boss_count(x) >= 2),
    "Cryonic Bar": lambda x: x.has_all({"Hardmode Forge", "Cryonic Ore"})
        or x.has_any({"Fleshy Geode", "Necromantic Geode"}),
    "Shardlight Pickaxe": lambda x: x.has_all({"Hardmode Anvil", "Cryonic Bar"}),
    "Abyssal Warhammer": lambda x: x.has_all({"Hardmode Anvil", "Cryonic Bar"}),
    "Inferna Cutter": lambda x:
        x.has_all({"Hardmode Anvil", "Axe of Purity", "Soul of Fright", "Essence of Havoc"}),
    "Perennial Ore": lambda x: x.has("Post-Plantera"),
    "Perennial Bar": lambda x: x.has_all({"Hardmode Forge", "Perennial Ore"})
        or x.has_any({"Fleshy Geode", "Necromantic Geode"}),
    "Beastial Pickaxe": lambda x: x.has_all({"Hardmode Anvil", "Perennial Bar"}),
    "Core of Sunlight": lambda x: x.has_all({"Hardmode Anvil", "Essence of Sunlight", "Ectoplasm"})
        or x.has_any({"Fleshy Geode", "Necromantic Geode"}),
    "Core of Eleum": lambda x: x.has_all({"Hardmode Anvil", "Essence of Eleum", "Ectoplasm"})
        or x.has_any({"Fleshy Geode", "Necromantic Geode"}),
    "Core of Havoc": lambda x: x.has_all({"Hardmode Anvil", "Essence of Havoc", "Ectoplasm"})
        or x.has_any({"Fleshy Geode", "Necromantic Geode"}),
    "Core of Calamity": lambda x: x.has_all({
        "Hardmode Anvil", "Core of Sunlight", "Core of Eleum", "Core of Havoc", "Ashes of Calamity"
    }),
    "Scoria Ore": lambda x: x.has("Post-Golem") or pick_power(x) >= 210,
    "Scoria Bar": lambda x: x.has_all({"Hardmode Forge", "Scoria Ore"})
        or x.has_any({"Fleshy Geode", "Necromantic Geode"}),
    "Seismic Hampick": lambda x: x.has_all({"Hardmode Anvil", "Scoria Bar"}),
    "Life Alloy": lambda x: x.has_all({
        "Hardmode Anvil", "Cryonic Bar", "Perennial Bar", "Scoria Bar",
    }) or x.has("Necromantic Geode"),
    "Advanced Display": lambda x: x.has_all({
        "Hardmode Anvil", "Mysterious Circuitry", "Dubious Plating", "Life Alloy",
        "Long Ranged Sensor Array",
    }),
    "Plague Cell Canister": lambda x: x.has("Post-Golem"),
    "Fleshy Geode": lambda x: x.can_reach("Ravager"),
    "Galactica Singularity": lambda x: x.has_all({"Ancient Manipulator", "Fragment"}),
    "Meld Blob": lambda x: x.has("Lunar Events") or x.can_reach("Astrum Deus"),
    "Meld Construct": lambda x: x.has_all({"Ancient Manipulator", "Meld Blob", "Stardust"}),
    "Astral Ore": lambda x: x.has_all({"Hardmode", "Post-Astrum Deus"}),
    "Astral Bar": lambda x: x.has_all({"Ancient Manipulator", "Stardust", "Astral Ore"}),
    "Astral Pickaxe": lambda x: x.has_all({"Ancient Manipulator", "Astral Bar"}),
    "Astral Hamaxe": lambda x: x.has_all({"Ancient Manipulator", "Astral Bar"}),
    "Genesis Pickaxe": lambda x:
        x.has_all({"Ancient Manipulator", "Meld Construct", "Luminite Bar"}),
    "Exodium Cluster": lambda x: x.has("Post-Moon Lord") and pick_power(x) >= 225,
    "Normality Relocator": lambda x:
        x.has_all({"Ancient Manipulator", "Rod of Discord", "Exodium Cluster", "Fragment"}),
    "Unholy Essence": lambda x:
        x.has("Post-Moon Lord") or x.can_reach("Providence, the Profaned Goddess"),
    "Phantoplasm": lambda x: x.has("Post-Moon Lord") and (x.has("Hardmode") or x.has("Dungeon")), # TODO Review this
    "Effulgent Feather": lambda x: x.has("Post-Moon Lord") or x.can_reach("The Dragonfolly"),
    "Rune of Kos": lambda x: x.can_reach("Providence, the Profaned Goddess")
        or x.has_all({"Unholy Essence", "Fragment", "Luminite Bar"}),
    "Uelibloom Ore": lambda x: x.has("Post-Providence, the Profaned Goddess"),
    "Uelibloom Bar": lambda x: x.has_all({"Hardmode Forge", "Uelibloom Ore"}),
    "Blossom Pickaxe": lambda x: x.has_all({"Ancient Manipulator", "Uelibloom Bar"}),
    "Grax": lambda x:
        x.has_all({"Ancient Manipulator", "Inferna Cutter", "Luminite Hamaxe", "Uelibloom Bar"}),
    "Voltage Regulation System": lambda x: x.has_all({
        "Ancient Manipulator", "Mysterious Circuitry", "Dubious Plating", "Uelibloom Bar",
        "Luminite Bar", "Advanced Display",
    }),
    "Necromantic Geode": lambda x:
        x.can_reach("Ravager") and x.has("Post-Providence, the Profaned Goddess"),
    "Cosmilite Bar": lambda x: x.can_reach("The Devourer of Gods"),
    "Cosmic Anvil": lambda x: x.has_all({
        "Ancient Manipulator", "Hardmode Anvil", "Cosmilite Bar", "Luminite Bar",
        "Galactica Singularity", "Exodium Cluster",
    }),
    "Nightmare Fuel": lambda x: x.has_all({"Pumpkin Moon", "Post-Devourer of Gods"}),
    "Endothermic Energy": lambda x: x.has_all({"Frost Moon", "Post-Devourer of Gods"}),
    "Darksun Fragment": lambda x: x.has_all({"Solar Eclipse", "The Devourer of Gods"}),
    "Ascendant Spirit Essence": lambda x: x.has_all({
        "Ancient Manipulator", "Phantoplasm", "Nightmare Fuel", "Endothermic Energy",
        "Darksun Fragment",
    }),
    "Yharon Soul Fragment": lambda x: x.can_reach("Yharon, Dragon of Rebirth"),
    "Auric Ore": lambda x: x.has("Post-Yharon, Dragon of Rebirth") and pick_power(x) >= 250,
    "Auric Bar": lambda x: x.has_all({"Cosmic Anvil", "Auric Ore", "Yharon Soul Fragment"}),
    "Auric Quantum Cooling Cell": lambda x: x.has_all({
        "Cosmic Anvil", "Auric Bar", "Mysterious Circuitry", "Dubious Plating",
        "Endothermic Energy", "Core of Eleum", "Voltage Regulation System",
    }),
    "Exo Prism": lambda x: x.can_reach("Exo Mechs"),
    "Draedon's Forge": lambda x: x.has_all({
        "Cosmic Anvil", "Hardmode Forge", "Tinkerer's Workshop", "Ancient Manipulator", "Auric Bar",
        "Exo Prism", "Ascendant Spirit Essence",
    }),
    "Ashes of Annihilation": lambda x: x.can_reach("Supreme Witch, Calamitas"),
    "Shadowspec Bar": lambda x:
        x.has_all({"Draedon's Forge", "Auric Bar", "Exo Prism", "Ashes of Annihilation"}),
    "Crystyl Crusher": lambda x:
        x.has_all({"Draedon's Forge", "Luminite Pickaxe", "Blossom Pickaxe", "Shadowspec Bar"}),
}

location_rules: dict[str, Optional[Callable[[Ctx], bool]]] = {
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
    "Dye Hard": lambda x: x.has("Dye Trader"),
    "Into Orbit": None,
    "Heliophobia": None,
    "A Rather Blustery Day": None,
    "Servant-in-Training": lambda x: x.has("Angler"),
    "10 Fishing Quests": lambda x: x.has("Angler"),
    "Trout Monkey": lambda x: x.has("Angler"),
    "Glorious Golden Pole": lambda x: x.has("Angler"),
    "Fast and Fishious": lambda x: x.has("Angler"),
    "Supreme Helper Minion!": lambda x: x.has("Angler"),
    "Torch God": None,
    "Like a Boss": None,
    "Sticky Situation": None,
    "King Slime": None,
    "The Cavalry": None,
    "Desert Scourge": None,
    "Giant Clam": lambda x: x.has("Post-Desert Scourge"),
    "Bloodbath": None,
    "Til Death...": None,
    "Quiet Neighborhood": None,
    "Feeling Petty": lambda x: x.has_any({"Cat", "Dog"}),
    "Eye of Cthulhu": None,
    "Acid Rain Tier 1": lambda x: x.has("Post-Eye of Cthulhu"),
    "Crabulon": None,
    "Smashing, Poppet!": None,
    "Evil Boss": None,
    "Leading Landlord": None,
    "Completely Awesome": lambda x: x.has("Arms Dealer"),
    "Goblin Army": None,
    "Old One's Army Tier 1": lambda x: x.has("Tavernkeep"),
    "Archaeologist": None,
    "Where's My Honey?": None,
    "Queen Bee": None,
    "Not the Bees!": lambda x: x.can_reach("Queen Bee") and x.has("Bee Wax"),
    "The Frequent Flyer": None,
    "Calamity Evil Boss": None,
    "Skeletron": None,
    "Dungeon Heist": lambda x: x.has("Dungeon"),
    "Jolly Jamboree": lambda x: x.has("Party Girl"),
    "Deerclops": None,
    "It's Getting Hot in Here": None,
    "Rock Bottom": None,
    "Miner for Fire": lambda x: x.has("Molten Pickaxe"),
    "Hot Reels!": lambda x: x.has("Lavaproof Bug Net"), # TODO Needs calamity considerations
    "Boots of the Hero": lambda x: x.has("Terraspark Boots"),
    "The Slime God": None,
    "Marathon Medalist": None,
    "Wall of Flesh": None,
    "Begone, Evil!": lambda x: x.has("Altar"),
    "Extra Shiny!": lambda x:
        x.has_any("Cobalt Ore", "Mythril Ore", "Adamantite Ore", "Chlorophyte Ore"),
    "Head in the Clouds": None, # TODO
    "Gelatin World Tour": lambda x:
        x.has_all({"Dungeon", "Hardmode", "Hallow"}) and x.can_reach("King Slime"),
    "Don't Dread on Me": lambda x: x.has("Hardmode"),
    "Pirate Invasion": lambda x: x.has("Hardmode"),
    "Earth Elemental": lambda x: x.has("Hardmode"),
    "Cloud Elemental": lambda x: x.has("Hardmode"),
    "Queen Slime": lambda x: x.has("Hallow"),
    "Aquatic Scourge": None,
    "Cragmaw Mire": lambda x: x.can_reach("Acid Rain Tier 2"),
    "Acid Rain Tier 2": lambda x: x.can_reach("Acid Rain Tier 1") and x.has("Post-Aquatic Scourge"),
    "The Twins": lambda x: x.has_all({"Hardmode Anvil", "Soul of Light"}),
    "Prismancer": lambda x: x.has("Rainbow Rod"),
    "Get a Life": lambda x: x.has("Life Fruit"),
    "Topped Off": lambda x: x.has("Life Fruit"),
    "Old One's Army Tier 2": lambda x: x.can_reach("Old One's Army Tier 1")
        and (mech_boss_count(x) >= 1 or x.can_reach("Old One's Army Tier 3")),
    "Brimstone Elemental":
        lambda x: x.has_all({"Soul of Night", "Essence of Havoc", "Unholy Core"}),
    "The Destroyer": lambda x: x.has_all({"Hardmode Anvil", "Soul of Night"}),
    "Cryogen": lambda x: x.has_all({"Soul of Night", "Soul of Light", "Essence of Eleum"}),
    "Skeletron Prime": lambda x: x.has_all({"Hardmode Anvil", "Bone", "Soul of Light", "Soul of Night"}),
    "Buckets of Bolts": lambda x: mech_boss_count(x) >= 3, # TODO Check
    "Drax Attax": lambda x: x.has("Pickaxe Axe"),
    "Photosynthesis": lambda x: x.has("Chlorophyte Ore"),
    "Mecha Mayhem": lambda x: x.can_reach_all({"The Twins", "The Detstroyer", "Skeletron Prime"}), # TODO Check
    "Calamitas Clone": lambda x: x.has_all({"Hardmode Anvil", "Hellstone Bar", "Essence of Havoc"}),
    "Plantera": lambda x: mech_boss_count(x) >= 3,
    "Seedler": lambda x: x.can_reach("Plantera"),
    "Temple Raider": lambda x: x.can_reach("Plantera"),
    "Robbing the Grave": lambda x: x.has_all({"Dungeon", "Post-Plantera"}),
    "Big Booty": lambda x: x.has_all({"Dungeon", "Hardmode", "Post-Plantera"}),
    "Rainbows and Unicorns": lambda x: x.has_all({"Rainbow Gun", "Blessed Apple"}),
    "Funkytown": None,
    "It Can Talk?!": lambda x: x.has("Truffle"),
    "Real Estate Agent": lambda x: x.has("Princess"),
    "Armored Digger": lambda x: x.has("Post-Plantera"), # TODO Check
    "Kill the Sun": lambda x: x.has("Solar Eclipse"),
    "Sword of the Hero": lambda x: x.has("Terra Blade"),
    "Great Sand Shark": lambda x:
        x.has_all({"Hardmode Anvil", "Forbidden Fragment", "Core of Sunlight"}),
    "Leviathan and Anahita": None,
    "Astrum Aureus": lambda x: x.has_all({"Hardmode Anvil", "Stardust"}),
    "Golem": lambda x: x.has_all({"Post-Plantera", "Lihzahrd Temple"}),
    "Old One's Army Tier 3": lambda x: x.can_reach("Old One's Army Tier 1") and x.has("Post-Golem"),
    "Martian Madness": lambda x: x.has("Post-Golem"),
    "Plaguebringer": lambda x: x.has("Post-Golem"),
    "The Plaguebringer Goliath": lambda x: x.has_all({"Hardmode Anvil", "Plague Cell Canister"}),
    "Duke Fishron": lambda x: x.has_all({"Bug Net", "Hardmode"}),
    "Mourning Wood": lambda x: x.has("Pumpkin Moon"),
    "Pumpking": lambda x: x.has("Pumpkin Moon"),
    "Baleful Harvest": lambda x: x.has("Pumpkin Moon"),
    "Everscream": lambda x: x.has("Frost Moon"),
    "Santa-NK1": lambda x: x.has("Frost Moon"),
    "Ice Queen": lambda x: x.has("Frost Moon"),
    "Ice Scream": lambda x: x.has("Frost Moon"),
    "Frost Legion": lambda x: x.has_all({"Hardmode", "Frost Moon"}),
    "Ravager": lambda x: x.has_all({"Hardmode Anvil", "Lihzahrd Temple", "Lihzahrd Brick"}),
    "Empress of Light": lambda x: x.has_all({"Hallow", "Post-Plantera"}),
    "Lunatic Cultist": lambda x: x.has_all({"Dungeon", "Post-Golem"}),
    "Lunar Events": lambda x: x.can_reach("Lunatic Cultist"),
    "Astrum Deus": lambda x: x.has("Titan Heart"),
    "Moon Lord": lambda x: x.can_reach("Lunar Events"),
    "Slayer of Worlds": lambda x: x.can_reach_all({
        "Evil Boss", "The Destroyer", "Duke Fishron", "Eye of Cthulhu", "Golem", "King Slime",
        "Lunatic Cultist", "Moon Lord", "Plantera", "Queen Bee", "Skeletron", "Skeletron Prime",
        "The Twins", "Wall of Flesh",
    }),
    "Sick Throw": lambda x: x.has("Terrarian"),
    "You and What Army?": None, # TODO
    "Zenith": lambda x: x.has_all({
        "Hardmode Anvil", "Terra Blade", "Meowmere", "Star Wrath", "Influx Waver",
        "The Horseman's Blade", "Seedler", "Starfury", "Bee Keeper", "Enchanted Sword",
        "Copper Shortsword",
    }),
    "Profaned Guardians": lambda x: x.has_all({"Ancient Manipulator", "Unholy Essence", "Luminite Bar"}),
    "The Dragonfolly": lambda x: x.has_all({"Ancient Manipulator", "Life Alloy", "Fragment"}),
    "Providence, the Profaned Goddess": lambda x: x.can_reach("Profaned Guardians"),
    "Storm Weaver": lambda x: x.has("Rune of Kos"),
    "Ceaseless Void": lambda x: x.has("Rune of Kos"),
    "Signus, Envoy of the Devourer": lambda x: x.has("Rune of Kos"),
    "Polterghast": lambda x: x.has("Dungeon")
        and (x.has_all({"Ancient Manipulator", "Phantoplasm"}) or x.has("Post-Moon Lord")),
    "Colossal Squid": None,
    "Reaper Shark": None,
    "Eidolon Wyrm": None,
    "Mauler": lambda x: x.can_reach("Acid Rain Tier 3"),
    "Nuclear Terror": lambda x: x.can_reach("Acid Rain Tier 3"),
    "Acid Rain Tier 3": lambda x: x.can_reach("Acid Rain Tier 1") and x.has("Post-Polterghast"), # TODO Check
    "The Old Duke": lambda x: x.can_reach("Acid Rain Tier 3")
        or x.has_all({"Bug Net", "Post-Moon Lord"}) or x.has_all({"Amidias", "Post-The Old Duke"}),
    "The Devourer of Gods": lambda x: x.has("Ancient Manipulator") and (x.has_all({
        "Armored Shell", "Twisting Nether", "Dark Plasma"
    }) or x.has_all({"Luminite Bar", "Galactica Singularity", "Phantoplasm"})),
    "Yharon, Dragon of Rebirth": lambda x:
        x.has_all({"Ancient Manipulator", "Effulgent Feather", "Life Alloy"}),
    "Exo Mechs": lambda x:
        x.has_all({"Codebreaker Base", "Decryption Computer", "Auric Quantum Cooling Cell"}),
    "Supreme Witch, Calamitas": lambda x: x.has_all({
        "Cosmic Anvil", "Brimstone Slag", "Auric Bar", "Core of Calamity", "Ashes of Calamity",
    }),
    "Bulldozer": None,
    "Adult Eidolon Wyrm": lambda x: x.has_any({"Rod of Discord", "Normality Relocator"}),
}

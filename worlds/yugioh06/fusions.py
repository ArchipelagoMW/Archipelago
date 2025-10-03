from typing import List, NamedTuple, Dict


class FusionData(NamedTuple):
    name: str
    materials: List[str]
    replaceable: bool
    additional_spells: List[str] = []
    contact_fusion: bool = False
    generic: str | None = None


fusions: Dict[str, FusionData] = {
    "Alkana Knight Joker": FusionData(
        "Alkana Knight Joker",
        ["Queen's Knight", "Jack's Knight", "King's Knight"],
        False,
    ),
    "Alligator's Sword Dragon": FusionData(
        "Alligator's Sword Dragon",
        ["Baby Dragon", "Alligator's Sword"],
        True,
        ["Dragon's Mirror"]
    ),
    "Amphibious Bugroth": FusionData(
        "Amphibious Bugroth",
        ["Gound Attacker", "Guradian of the Sea"],
        True
    ),
    "B. Skull Dragon": FusionData(
        "B. Skull Dragon",
        ["Summoned Skull", "Red-Eyes B. Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Barox": FusionData(
        "Barox",
        ["Frenzied Panda", "Ryu-Kishin"],
        True
    ),
    "Bickuribox": FusionData(
        "Bickuribox",
        ["Crass Clown", "Dream Clown"],
        True
    ),
    "Blue-Eyes Ultimate Dragon": FusionData(
        "Blue-Eyes Ultimate Dragon",
        ["Blue-Eyes White Dragon", "Blue-Eyes White Dragon", "Blue-Eyes White Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Blue-Eyes Ultimate Dragon Alt 1": FusionData(
        "Blue-Eyes Ultimate Dragon Alt 1",
        ["Blue-Eyes White Dragon", "Blue-Eyes White Dragon", "Blue-Eyes White Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Bracchio-raidus": FusionData(
        "Bracchio-raidus",
        ["Two-Headed King Rex", "Crawling Dragon #2"],
        True
    ),
    "Charubin the Fire Knight": FusionData(
        "Charubin the Fire Knight",
        ["Monster Egg", "Hinotama Soul"],
        True
    ),
    "Chimera the Flying Mythical Beast": FusionData(
        "Chimera the Flying Mythical Beast",
        ["Gazelle the King of Mythical Beasts", "Berfomet"],
        True
    ),
    "Crimson Sunbird": FusionData(
        "Crimson Sunbird",
        ["Faith Bird", "Skull Red Bird"],
        True
    ),
    "Cyber Blader": FusionData(
        "Cyber Blader",
        ["Etoile Cyber", "Blade Skater"],
        False
    ),
    "Cyber End Dragon": FusionData(
        "Cyber End Dragon",
        ["Cyber Dragon", "Cyber Dragon", "Cyber Dragon"],
        False,
        ["Power Bond"]
    ),
    "Cyber Twin Dragon": FusionData(
        "Cyber Twin Dragon",
        ["Cyber Dragon", "Cyber Dragon"],
        False,
        ["Power Bond"]
    ),
    "D.3.S. Frog": FusionData(
        "D.3.S. Frog",
        ["Des Frog", "Des Frog", "Des Frog"],
        False
    ),
    "Dark Balter the Terrible": FusionData(
        "Dark Balter the Terrible",
        ["Possessed Dark Soul", "Frontier Wiseman"],
        False
    ),
    "Dark Blade the Dragon Knight": FusionData(
        "Dark Blade the Dragon Knight",
        ["Dark Blade", "Pitch-Dark Dragon"],
        True
    ),
    "Dark Flare Knight": FusionData(
        "Dark Flare Knight",
        ["Dark Magician", "Flame Swordsman"],
        True
    ),
    "Dark Paladin": FusionData(
        "Dark Paladin",
        ["Dark Magician", "Buster Blader"],
        True
    ),
    "Dark Paladin Alt 1": FusionData(
        "Dark Paladin Alt 1",
        ["Dark Magician", "Buster Blader"],
        True
    ),
    "Dark Paladin Alt 2": FusionData(
        "Dark Paladin Alt 2",
        ["Dark Magician", "Buster Blader"],
        True
    ),
    "Darkfire Dragon": FusionData(
        "Darkfire Dragon",
        ["Firegrass", "Petit Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Deepsea Shark": FusionData(
        "Deepsea Shark",
        ["Bottom Dweller", "Tongyo"],
        True
    ),
    "Dragoness the Wicked Knight": FusionData(
        "Dragoness the Wicked Knight",
        ["Armaill", "One-Eyed Shield Dragon"],
        True
    ),
    "Elemental Hero Erikshieler": FusionData(
        "Elemental Hero Erikshieler",
        ["Elemental Hero Avian", "Elemental Hero Burstinatrix",
         "Elemental Hero Bubbleman", "Elemental Hero Clayman"],
        True,
        ["Miracle Fusion"]
    ),
    "Elemental Hero Flame Wingman": FusionData(
        "Elemental Hero Flame Wingman",
        ["Elemental Hero Avian", "Elemental Hero Burstinatrix"],
        True,
        ["Miracle Fusion"]
    ),
    "Elemental Hero Madballman": FusionData(
        "Elemental Hero Madballman",
        ["Elemental Hero Bubbleman", "Elemental Hero Clayman"],
        True,
        ["Miracle Fusion"]
    ),
    "Elemental Hero Rampart Blaster": FusionData(
        "Elemental Hero Rampart Blaster",
        ["Elemental Hero Burstinatrix", "Elemental Hero Clayman"],
        True,
        ["Miracle Fusion"]
    ),
    "Elemental Hero Shining Flare Wingman": FusionData(
        "Elemental Hero Shining Flare Wingman",
        ["Elemental Hero Flame Wingman", "Elemental Hero Sparkman"],
        True,
        ["Miracle Fusion"]
    ),
    "Elemental Hero Steam Healer": FusionData(
        "Elemental Hero Steam Healer",
        ["Elemental Hero Burstinatrix", "Elemental Hero Bubbleman"],
        True,
        ["Miracle Fusion"]
    ),
    "Elemental Hero Tempest": FusionData(
        "Elemental Hero Tempest",
        ["Elemental Hero Avian", "Elemental Hero Sparkman", "Elemental Hero Bubbleman"],
        True,
        ["Miracle Fusion"]
    ),
    "Elemental Hero Thunder Giant": FusionData(
        "Elemental Hero Thunder Giant",
        ["Elemental Hero Sparkman", "Elemental Hero Clayman"],
        True,
        ["Miracle Fusion"]
    ),
    "Elemental Hero Wildedge": FusionData(
        "Elemental Hero Wildedge",
        ["Elemental Hero Wildheart", "Elemental Hero Bladedge"],
        True,
        ["Miracle Fusion"]
    ),
    "F.G.D.": FusionData(
        "F.G.D.",
        [],
        False, ["Dragon's Mirror"],
        generic="Dragon",
    ),
    "Fiend Skull Dragon": FusionData(
        "Fiend Skull Dragon",
        ["Cave Dragon", "Lesser Fiend"],
        False,
        ["Dragon's Mirror"]
    ),
    "Flame Ghost": FusionData(
        "Flame Ghost",
        ["Skull Servant", "Dissolverock"],
        True
    ),
    "Flame Swordsman": FusionData(
        "Flame Swordsman",
        ["Flame Manipulator", "Masaki the Legendary Swordsman"],
        True
    ),
    "Flame Swordsman Alt 1": FusionData(
        "Flame Swordsman Alt 1",
        ["Flame Manipulator", "Masaki the Legendary Swordsman"],
        True
    ),
    "Flower Wolf": FusionData(
        "Flower Wolf",
        ["Silver Fang", "Darkworld Thorns"],
        True
    ),
    "Fusionist": FusionData(
        "Fusionist",
        ["Petit Angel", "Mystical Sheep #2"],
        True
    ),
    "Gaia the Dragon Champion": FusionData(
        "Gaia the Dragon Champion",
        ["Gaia The Fierce Knight", "Curse of Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Gatling Dragon": FusionData(
        "Gatling Dragon",
        ["Barrel Dragon", "Blowback Dragon"],
        True,
        ["Power Bond"]
    ),
    "Giltia the D. Knight": FusionData(
        "Giltia the D. Knight",
        ["Guardian of the Labyrinth", "Protector of the Throne"],
        True
    ),
    "Great Mammoth of Goldfine": FusionData(
        "Great Mammoth of Goldfine",
        ["The Snake Hair", "Dragon Zombie"],
        True
    ),
    "Humanoid Worm Drake": FusionData(
        "Humanoid Worm Drake",
        ["Worm Drake", "Humanoid Slime"],
        True
    ),
    "Kaiser Dragon": FusionData(
        "Kaiser Dragon",
        ["Winged Dragon, Guardian of the Fortress #1", "Fairy Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Kaminari Attack": FusionData(
        "Kaminari Attack",
        ["Ocubeam", "Mega Thunderball"],
        True
    ),
    "Kamionwizard": FusionData(
        "Kamionwizard",
        ["Mystical Elf", "Curtain of the Dark Ones"],
        True
    ),
    "Karbonala Warrior": FusionData(
        "Karbonala Warrior",
        ["M-Warrior #1", "M-Warrior #2"],
        True
    ),
    "King Dragun": FusionData(
        "King Dragun",
        ["Lord of D.", "Divine Dragon Ragnarok"],
        True,
        ["Dragon's Mirror"]
    ),
    "Labyrinth Tank": FusionData(
        "Labyrinth Tank",
        ["Giga-Tech Wolf", "Cannon Soldier"],
        True,
        ["Power Bond"]
    ),
    "Man-eating Black Shark": FusionData(
        "Man-eating Black Shark",
        ["Sea Kamen", "Gruesome Goo", "Amazon of the Seas"],
        True
    ),
    "Marine Beast": FusionData(
        "Marine Beast",
        ["Water Magician", "Behegon"],
        True
    ),
    "Master of Dragon Soldier": FusionData(
        "Master of Dragon Soldier",
        ["Black Luster Soldier", "Blue-Eyes Ultimate Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Master of Oz": FusionData(
        "Master of Oz",
        ["Big Koala", "Des Kangaroo"],
        True
    ),
    "Mavelus": FusionData(
        "Mavelus",
        ["Tyhone", "Wings of Wicked Flame"],
        True
    ),
    "Metal Dragon": FusionData(
        "Metal Dragon",
        ["Steel Ogre Grotto #1", "Lesser Dragon"],
        True,
        ["Power Bond"]
    ),
    "Meteor B. Dragon": FusionData(
        "Meteor B. Dragon",
        ["Red-Eyes B. Dragon", "Meteor Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Mokey Mokey King": FusionData(
        "Mokey Mokey King",
        ["Mokey Mokey", "Mokey Mokey", "Mokey Mokey"],
        True
    ),
    "Musician King": FusionData(
        "Musician King",
        ["Witch of the Black Forest", "Lady of Faith"],
        True
    ),
    "Mystical Sand": FusionData(
        "Mystical Sand",
        ["Giant Soldier of Stone", "Ancient Elf"],
        True
    ),
    "Ojama King": FusionData(
        "Ojama King",
        ["Ojama Green", "Ojama Yellow", "Ojama Black"],
        True
    ),
    "Pragtical": FusionData(
        "Pragtical",
        ["Trakadon", "Flame Viper"],
        True
    ),
    "Punished Eagle": FusionData(
        "Punished Eagle",
        ["Blue-Winged Crown", "Niwatori"],
        True
    ),
    "Rabid Horseman": FusionData(
        "Rabid Horseman",
        ["Battle Ox", "Mystic Horseman"],
        True
    ),
    "Rare Fish": FusionData(
        "Rare Fish",
        ["Fusionist", "Enchanting Mermaid"],
        True
    ),
    "Reaper on the Nightmare": FusionData(
        "Reaper on the Nightmare",
        ["Spirit Reaper", "Nightmare Horse"],
        True
    ),
    "Rose Spectre of Dunn": FusionData(
        "Rose Spectre of Dunn",
        ["Feral Imp", "Snakeyashi"],
        True
    ),
    "Ryu Senshi": FusionData(
        "Ryu Senshi",
        ["Warrior Dai Grepher", "Spirit Ryu"],
        False
    ),
    "Sanwitch": FusionData(
        "Sanwitch",
        ["Sangan", "Witch of the Black Forest"],
        True
    ),
    "Skelgon": FusionData(
        "Skelgon",
        ["The Snake Hair", "Blackland Fire Dragon"],
        True
    ),
    "Skullbird": FusionData(
        "Skullbird",
        ["Takuhee", "Temple of Skulls"],
        True
    ),
    "Soul Hunter": FusionData(
        "Soul Hunter",
        ["Lord of the Lamp", "Invader from Another Dimension"],
        True
    ),
    "St. Joan": FusionData(
        "St. Joan",
        ["The Forgiving Maiden", "Marie the Fallen One"],
        True
    ),
    "Steam Gyroid": FusionData(
        "Steam Gyroid",
        ["Gyroid", "Steamroid"],
        True,
        ["Power Bond"]
    ),
    "Super Robolady": FusionData(
        "Super Robolady",
        ["Robolady", "Roboyarou"],
        True,
        ["Power Bond"]
    ),
    "Super Roboyarou": FusionData(
        "Super Roboyarou",
        ["Robolady", "Roboyarou"],
        True,
        ["Power Bond"]
    ),
    "The Last Warrior from Another Planet": FusionData(
        "The Last Warrior from Another Planet",
        ["Zombyra the Dark", "Maryokutai"],
        True
    ),
    "Thousand Dragon": FusionData(
        "Thousand Dragon",
        ["Time Wizard", "Baby Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Thousand Dragon Alt 1": FusionData(
        "Thousand Dragon Alt 1",
        ["Time Wizard", "Baby Dragon"],
        True,
        ["Dragon's Mirror"]
    ),
    "Thousand-Eyes Restrict": FusionData(
        "Thousand-Eyes Restrict",
        ["Relinquished", "Thousand-Eyes Idol"],
        True
    ),
    "Twin-Headed Thunder Dragon": FusionData(
        "Twin-Headed Thunder Dragon",
        ["Thunder Dragon", "Thunder Dragon"],
        True
    ),
    "UFOroid Fighter": FusionData(
        "UFOroid Fighter",
        ["UFOroid"],
        False,
        ["Power Bond"], generic="Warrior",

    ),
    "Vermillion Sparrow": FusionData(
        "Vermillion Sparrow",
        ["Rhaimundos of the Red Sword", "Fireyarou"],
        True
    ),
    "VW-Tiger Catapult": FusionData(
        "VW-Tiger Catapult",
        ["V-Tiger Jet", "W-Wing Catapult"],
        True, contact_fusion=True
    ),
    "VWXYZ-Dragon Catapult Cannon": FusionData(
        "VWXYZ-Dragon Catapult Cannon",
        ["VW-Tiger Catapult", "XYZ-Dragon Cannon"],
        True, contact_fusion=True
    ),
    "Warrior of Tradition": FusionData(
        "Warrior of Tradition",
        ["Sonic Maid", "Beautiful Headhuntress"],
        True
    ),
    "XY-Dragon Cannon": FusionData(
        "XY-Dragon Cannon",
        ["X-Head Cannon", "Y-Dragon Head"],
        True, contact_fusion=True
    ),
    "XYZ-Dragon Cannon": FusionData(
        "XYZ-Dragon Cannon",
        ["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank"],
        True, contact_fusion=True
    ),
    "XYZ-Dragon Cannon Alt 1": FusionData(
        "XYZ-Dragon Cannon Alt 1",
        ["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank"],
        True, contact_fusion=True
    ),
    "XYZ-Dragon Cannon Alt 2": FusionData(
        "XYZ-Dragon Cannon Alt 2",
        ["X-Head Cannon", "Y-Dragon Head", "Z-Metal Tank"],
        True, contact_fusion=True
    ),
    "XZ-Tank Cannon": FusionData(
        "XZ-Tank Cannon",
        ["X-Head Cannon", "Z-Metal Tank"],
        True, contact_fusion=True
    ),
    "YZ-Tank Dragon": FusionData(
        "YZ-Tank Dragon",
        ["Y-Dragon Head", "Z-Metal Tank"],
        True, contact_fusion=True
    ),
    "Zombie Warrior": FusionData(
        "Zombie Warrior",
        ["Skull Servant", "Battle Warrior"],
        True
    ),
}

fusion_subs = ["The Dark - Hex-Sealed Fusion",
               "The Earth - Hex-Sealed Fusion",
               "The Light - Hex-Sealed Fusion",
               "Goddess with the Third Eye",
               "King of the Swamp",
               "Versago the Destroyer"]
fusion_subs_nisp = [
               # Only in All-packs
               "Beastking of the Swamps",
               "Mystical Sheep #1"]


def has_all_materials(state, monster, player):
    data = fusions.get(monster)
    if not state.has(monster, player):
        return False
    if data is None:
        return True
    else:
        materials = data.replaceable and state.has_any(fusion_subs, player)
        for material in data.materials:
            materials += has_all_materials(state, material, player)
        return materials >= len(data.materials)


def count_has_materials(state, monsters, player):
    amount = 0
    for monster in monsters:
        amount += has_all_materials(state, monster, player)
    return amount

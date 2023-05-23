booster_contents = {
    "LEGEND OF B.E.W.D.": {
        "Exodia",
        "Dark Magician"
        "Polymerization"
    },
    "METAL RAIDERS": {
        "Petit Moth",
        "Cocoon of Evolution",
        "Time Wizard",
        "Gate Guardian",
        "Kazejin",
        "Suijin",
        "Sanga of the Thunder",
        "Sangan",
        "Castle of Dark Illusions"
    },
    "PHARAOH'S SERVANT": {},
    "PHARAONIC GUARDIAN": {
        "Don Zaloog",
        "Reasoning"
    },
    "SPELL RULER": {
        "Ritual"
    },
    "LABYRINTH OF NIGHTMARE": {
        "Destiny Board",
        "Spirit Message 'I'",
        "Spirit Message 'N'",
        "Spirit Message 'A'",
        "Spirit Message 'L'",
        "Fusion Gate",
        "Jowgen the Spiritualist"
    },
    "LEGACY OF DARKNESS": {
        "Last Turn",
        "Yata-Garasu"
    },
    "MAGICIAN'S FORCE": {
        "Huge Revolution",
        "Oppressed People",
        "United Resistance",
        "People Running About",
        "X-Head Cannon",
        "Y-Dragon Head",
        "Z-Metal Tank",
        "XY-Dragon Cannon",
        "XZ-Tank Cannon",
        "YZ-Tank Dragon",
        "XYZ-Dragon Cannon",
        "V-Tiger Jet",
        "W-Wing Catapult",
        "VW-Tiger Catapult",
        "VWXYZ-Dragon Catapult Cannon",
        "Dark Scorpion - Cliff the Trap Remover",
        "Wave-Motion Cannon",
        "Ritual",
        "Magical Merchant",
        "Poison of the Old Man"
    },
    "DARK CRISIS": {
        "Final Countdown",
        "Ojama Green",
        "Dark Scorpion Combination",
        "Dark Scorpion - Chick the Yellow",
        "Dark Scorpion - Meanae the Thorn",
        "Dark Scorpion - Gorg the Strong",
        "Ritual"
    },
    "INVASION OF CHAOS": {
        "Ojama Delta Hurricane",
        "Ojama Yellow",
        "Ojama Black",
        "Heart of the Underdog",
        "Chaos Emperor Dragon - Envoy of the End"
    },
    "ANCIENT SANCTUARY": {
        "Monster Gate",
        "Wall of Revealing Light",
        "Mystik Wok"
    },
    "SOUL OF THE DUELIST": {},
    "RISE OF DESTINY": {},
    "FLAMING ETERNITY": {},
    "THE LOST MILLENIUM": {
        "Ritual"
    },
    "CYBERNETIC REVOLUTION": {
        "Power Bond"
    },
    "ELEMENTAL ENERGY": {},
    "SHADOW OF INFINITY": {
        "Hamon, Lord of Striking Thunder",
        "Raviel, Lord of Phantasms",
        "Uria, Lord of Searing Flames",
        "Ritual"
    },
    "GAME GIFT COLLECTION": {
        "Valkyrion the Magna Warrior",
        "Alpha the Magnet Warrior",
        "Beta the Magnet Warrior",
        "Gamma the Magnet Warrior"
    },
    "Special Gift Collection": {
        "Gate Guardian"
    },
    "Fairy Collection": {},
    "Dragon Collection": {
        "Victory D",
        "Chaos Emperor Dragon - Envoy of the End"
    },
    "Warrior Collection A": {
        "Gate Guardian"
    },
    "Warrior Collection B": {
        "Don Zaloog",
        "Dark Scorpion - Chick the Yellow",
        "Dark Scorpion - Meanae the Thorn",
        "Dark Scorpion - Gorg the Strong",
        "Dark Scorpion - Cliff the Trap Remover"
    },
    "Fiend Collection A": {
        "Sangan",
        "Castle of Dark Illusions",
        "Barox"
    },
    "Fiend Collection B": {
        "Raviel, Lord of Phantasms",
        "Yata-Garasu"
    },
    "Machine Collection A": {
        "Cyber-Stein"
    },
    "Machine Collection B": {
        "X-Head Cannon",
        "Y-Dragon Head",
        "Z-Metal Tank",
        "XY-Dragon Cannon",
        "XZ-Tank Cannon",
        "YZ-Tank Dragon",
        "XYZ-Dragon Cannon",
        "V-Tiger Jet",
        "W-Wing Catapult",
        "VW-Tiger Catapult",
        "VWXYZ-Dragon Catapult Cannon"
    },
    "Spellcaster Collection A": {
        "Exodia",
        "Dark Sage",
        "Dark Magician",
        "Time Wizard",
        "Kazejin"
    },
    "Spellcaster Collection B": {
        "Jowgen the Spiritualist"
    },
    "Zombie Collection": {},
    "Special Monsters A": {
        "X-Head Cannon",
        "Y-Dragon Head",
        "Z-Metal Tank",
        "V-Tiger Jet",
        "W-Wing Catapult",
        "Yata-Garasu"
    },
    "Special Monsters B": {
        "Polymerization"
    },
    "Reverse Collection": {
        "Magical Merchant",
        "Castle of Dark Illusions"
    },
    "LP Recovery Collection": {
        "Mystik Wok",
        "Poison of the Old Man"
    },
    "Special Summon Collection A": {
        "Perfectly Ultimate Great Moth",
        "Dark Sage",
        "Polymerization",
        "Ritual",
        "Cyber-Stein"
    },
    "Special Summon Collection B": {
        "Monster Gate",
        "Chaos Emperor Dragon - Envoy of the End"
    },
    "Special Summon Collection C": {
        "Hamon, Lord of Striking Thunder",
        "Raviel, Lord of Phantasms",
        "Uria, Lord of Searing Flames"
    },
    "Equipment Collection": {},
    "Continuous Spell/Trap A": {
        "Destiny Board",
        "Spirit Message 'I'",
        "Spirit Message 'N'",
        "Spirit Message 'A'",
        "Spirit Message 'L'",
    },
    "Continuous Spell/Trap B": {
        "Hamon, Lord of Striking Thunder",
        "Uria, Lord of Searing Flames",
        "Wave-Motion Cannon",
        "Heart of the Underdog",
        "Wall of Revealing Light"
    },
    "Quick/Counter Collection": {
        "Mystik Wok",
        "Poison of the Old Man"
    },
    "Direct Damage Collection": {
        "Hamon, Lord of Striking Thunder",
        "Chaos Emperor Dragon - Envoy of the End"
    },
    "Direct Attack Collection": {
        "Victory D",
        "Dark Scorpion Combination"
    },
    "Monster Destroy Collection": {
        "Hamon, Lord of Striking Thunder"
    },
}


def get_booster_locations(booster: str) -> dict[str, str]:
    location = {}
    i = 1
    for content in booster_contents.get(booster):
        location[booster + " " +str(i)] = content
        i = i + 1
    return location

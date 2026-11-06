from typing import List, Dict, NamedTuple


class RitualData(NamedTuple):
    name: str
    ritual_spells: List[str]
    nisp_spell: str = None


rituals: Dict[str, RitualData] = {
    "Black Luster Soldier": RitualData("Black Luster Soldier", ["Earth Chant"], "Black Luster Ritual"),
    "Chakra": RitualData("Chakra", ["Contract with the Abyss"], "Resurrection of Chakra"),
    "Crab Turtle": RitualData("Crab Turtle", ["Turtle Oath"]),
    "Dark Master - Zorc": RitualData("Dark Master - Zorc", ["Contract with the Dark Master",
                                                            "Contract with the Abyss"]),
    "Demise, King of Armageddon": RitualData("Demise, King of Armageddon",
                                             ["End of the World", "Contract with the Abyss"]),
    "Dokurorider": RitualData("Dokurorider", ["Contract with the Abyss"], "Revival of Dokurorider"),
    "Elemental Mistress Doriado": RitualData("Elemental Mistress Doriado", ["Doriado's Blessing"]),
    "Fiend's Mirror": RitualData("Fiend's Mirror", ["Contract with the Abyss"], "Beastly Mirror Ritual"),
    "Fortess Whale": RitualData("Fortess Whale", [], "Fortess Whale's Oath"),
    "Garma Sword": RitualData("Garma Sword", ["Garma Sword Oath", "Contract with the Abyss"]),
    "Hungry Burger": RitualData("Hungry Burger", ["Hamburger Recipe", "Contract with the Abyss"]),
    "Javelin Beetle": RitualData("Javelin Beetle", ["Earth Chant"], "Javelin Beetle Pact"),
    "Legendary Flame Lord": RitualData("Legendary Flame Lord", ["Incandescent Ordeal"]),
    "Magician of Black Chaos": RitualData("Magician of Black Chaos", ["Dark Magic Ritual", "Contract with the Abyss"]),
    "Paladin of White Dragon": RitualData("Paladin of White Dragon", ["White Dragon Ritual"]),
    "Performance of Sword": RitualData("Performance of Sword", ["Commencement Dance", "Earth Chant"]),
    "Relinquished": RitualData("Relinquished", ["Black Illusion Ritual", "Contract with the Abyss"]),
    "Reshef the Dark Being": RitualData("Reshef the Dark Being", ["Final Ritual of the Ancients"]),
    "Ruin, Queen of Oblivion": RitualData("Ruin, Queen of Oblivion", ["End of the World"]),
    "Shinato, King of a Higher Plane": RitualData("Shinato, King of a Higher Plane", ["Shinato's Ark"]),
    "Skull Guardian": RitualData("Skull Guardian", [], "Novox's Prayer"),
    "Super War-Lion": RitualData("Super War-Lion", ["War-Lion Ritual", "Earth Chant"]),
    "The Masked Beast": RitualData("The Masked Beast", ["Curse of the Masked Beast", "Contract with the Abyss"]),
    "Zera The Mant": RitualData("Zera The Mant", ["Contract with the Abyss"], "Zera Ritual")
}

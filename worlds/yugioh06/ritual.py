from typing import List, Dict, NamedTuple


class RitualData(NamedTuple):
    name: str
    ritual_spells: List[str]
    nisp_spell: str = None


rituals: Dict[str, RitualData] = {
    "Black Luster Soldier": RitualData("Black Luster Soldier", ["Earth Chant"], "Black Luster Ritual"),
    "Chakra": RitualData("Chakra", ["Contract with the Abyss"], "Resurrection of Chakra"),
    "Crab Turtle": RitualData("Crab Turtle", ["Turtle Oath"]),
    "Dark Master - Zorc": RitualData("Dark Master - Zorc", ["Contract with the Dark Master", "Contract with the Abyss"]),
    "Demise, King of Armageddon": RitualData("Demise, King of Armageddon",
                                             ["End of the World", "Contract with the Abyss"])
    # todo
}

nisp_ritual_spells = {

}
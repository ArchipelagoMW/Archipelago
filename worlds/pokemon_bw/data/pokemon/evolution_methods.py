from .. import EvolutionMethodData, ExtendedRule
from . import species


def has_species(name: str) -> ExtendedRule:
    return lambda state, world: state.has(name, world.player)


always_possible: ExtendedRule = lambda state, world: True
can_reach_magnetic_area: ExtendedRule = lambda state, world: state.can_reach_region("Chargestone Cave", world.player)
can_reach_moss_rock: ExtendedRule = lambda state, world: state.can_reach_region("Pinwheel Forest West", world.player)
can_reach_ice_rock: ExtendedRule = lambda state, world: state.can_reach_region("Twist Mountain", world.player)
can_reach_nacrene_city: ExtendedRule = lambda state, world: state.can_reach_region("Nacrene City", world.player)
can_reach_mistralton_city: ExtendedRule = lambda state, world: state.can_reach_region("Mistralton City", world.player)

can_buy_item_castelia: ExtendedRule = lambda state, world: state.can_reach_region("Castelia City", world.player)
can_get_item_chargestone: ExtendedRule = lambda state, world: state.can_reach_region("Chargestone Cave", world.player)
can_buy_item_twist: ExtendedRule = lambda state, world: state.can_reach_region("Twist Mountain", world.player)
can_buy_item_mall: ExtendedRule = lambda state, world: state.can_reach_region("Route 9", world.player)
can_get_item_r10: ExtendedRule = lambda state, world: state.can_reach_region("Route 10", world.player)
can_buy_item_undella: ExtendedRule = lambda state, world: state.can_reach_region("Undella Town", world.player)
can_get_item_chasm: ExtendedRule = lambda state, world: state.can_reach_region("Giant Chasm Entrance Cave", world.player)
can_buy_item: dict[int, ExtendedRule] = {
    80: can_buy_item_twist,  # Sun Stone
    81: can_buy_item_twist,  # Moon Stone
    82: can_buy_item_castelia,  # Fire Stone
    83: can_get_item_chargestone,  # Thunderstone
    84: can_buy_item_castelia,  # Water Stone
    85: can_buy_item_castelia,  # Leaf Stone
    107: can_get_item_r10,  # Shiny Stone
    108: can_get_item_r10,  # Dusk Stone
    109: can_get_item_r10,  # Dawn Stone
    110: can_buy_item_mall,  # Oval Stone
    221: can_buy_item_mall,  # King's Rock
    226: can_buy_item_undella,  # Deep Sea Tooth
    227: can_buy_item_undella,  # Deep Sea Scale
    233: can_get_item_chargestone,  # Metal Coat
    235: can_buy_item_mall,  # Dragon Scale
    252: can_buy_item_undella,  # Up-Grade
    321: can_buy_item_mall,  # Protector
    322: can_buy_item_undella,  # Electirizer
    323: can_buy_item_undella,  # Magmarizer
    324: can_buy_item_undella,  # Dubious Disc
    325: can_buy_item_mall,  # Reaper Cloth
    326: can_get_item_chasm,  # Razor Claw
    327: can_get_item_chasm,  # Razor Fang
    537: can_buy_item_undella,  # Prism Scale
}

in_vanilla_east: ExtendedRule = lambda state, world: (
    state.can_reach_region("Route 15", world.player)
    and "Wild" not in world.options.adjust_levels
)
can_challenge_alder: ExtendedRule = lambda state, world: state.can_reach_region("N's Castle", world.player)
between_ghetsis_and_alder: ExtendedRule = lambda state, world: (
    in_vanilla_east(state, world)
    or can_challenge_alder(state, world)
)
is_in_appropriate_region: dict[int, ExtendedRule] = {  # Artificial logic so that you're not expected to evolve Larvesta in Striaton City
    0: always_possible,
    1: always_possible,
    2: always_possible,
    3: lambda state, world: state.can_reach_region("Pinwheel Forest Outside", world.player),
    4: lambda state, world: state.can_reach_region("Castelia City", world.player),
    5: lambda state, world: state.can_reach_region("Desert Resort", world.player),
    6: lambda state, world: state.can_reach_region("Undella Town", world.player) or  # Includes in_vanilla_east
                            state.can_reach_region("Mistralton Cave Inner", world.player) or
                            state.can_reach_region("Chargestone Cave", world.player),
    7: lambda state, world: state.can_reach_region("Route 13", world.player) or  # Includes in_vanilla_east
                            state.can_reach_region("Twist Mountain", world.player),
    8: lambda state, world: in_vanilla_east(state, world) or state.can_reach_region("Opelucid City", world.player),
    9: lambda state, world: in_vanilla_east(state, world) or state.can_reach_region("Victory Road", world.player),
    10: lambda state, world: in_vanilla_east(state, world) or state.can_reach_region("Pokémon League", world.player),
    11: between_ghetsis_and_alder,
    12: between_ghetsis_and_alder,
    13: between_ghetsis_and_alder,
    14: between_ghetsis_and_alder,
    15: can_challenge_alder,
    16: can_challenge_alder,
    17: can_challenge_alder,
    18: can_challenge_alder,
    19: can_challenge_alder,
}

methods: dict[str, EvolutionMethodData] = {
    "Level up": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),
    "Stone": EvolutionMethodData(0, lambda value: can_buy_item[value]),
    "Stone male": EvolutionMethodData(0, lambda value: can_buy_item[value]),  # Repeatable encounters, including static, are ensured
    "Stone female": EvolutionMethodData(0, lambda value: can_buy_item[value]),  # Repeatable encounters, including static, are ensured
    "Friendship": EvolutionMethodData(0, lambda value: can_reach_nacrene_city),  # Artificial logic because there's the friendship checker
    "Friendship (Day)": EvolutionMethodData(0, None),  # Removed
    "Friendship (Night)": EvolutionMethodData(0, None),  # Removed
    "Trade": EvolutionMethodData(0, None),  # Removed
    "Trade with item": EvolutionMethodData(0, None),  # Removed
    "Trade Karrablast Shelmet": EvolutionMethodData(0, None),  # Removed
    "Magnetic area": EvolutionMethodData(0, lambda value: can_reach_magnetic_area),
    "Level up with move": EvolutionMethodData(0, lambda value: can_reach_mistralton_city),  # When randomized evolutions, then move id must be taken from level up moveset
    "Level up moss rock": EvolutionMethodData(0, lambda value: can_reach_moss_rock),
    "Level up ice rock": EvolutionMethodData(0, lambda value: can_reach_ice_rock),
    "Level up item day": EvolutionMethodData(0, lambda value: can_buy_item[value]),  # Always paired with night
    "Level up item night": EvolutionMethodData(0, lambda value: can_buy_item[value]),  # Always paired with day
    "Level up higher defense": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),  # Repeatable encounters, including static, are ensured
    "Level up higher attack": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),  # Repeatable encounters, including static, are ensured
    "Level up equal physical": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),  # Repeatable encounters, including static, are ensured
    "Level up Silcoon": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),  # Repeatable encounters, including static, are ensured
    "Level up Cascoon": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),  # Repeatable encounters, including static, are ensured
    "Level up Ninjask": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),
    "Level up Shedinja": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),
    "Level up high beauty": EvolutionMethodData(0, None),  # Removed
    "Level up (female)": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),  # Repeatable encounters, including static, are ensured
    "Level up (male)": EvolutionMethodData(0, lambda value: is_in_appropriate_region[value//5]),  # Repeatable encounters, including static, are ensured
    "Level up with party member": EvolutionMethodData(0, lambda value: has_species(species.by_id[value, 0])),
}

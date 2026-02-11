from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, add_item_rule
from BaseClasses import ItemClassification

from .Locations import KHDDDLocation, location_data_table
from .Items import get_items_by_category

if TYPE_CHECKING:
    from . import KHDDDWorld

SORA_WORLDS = ["Traverse Town [Sora]", "La Cite des Cloches [Sora]", "The Grid [Sora]", "Prankster's Paradise [Sora]", "Country of the Musketeers [Sora]", "Symphony of Sorcery [Sora]"]
RIKU_WORLDS = ["Traverse Town [Riku]", "La Cite des Cloches [Riku]", "The Grid [Riku]", "Prankster's Paradise [Riku]", "Country of the Musketeers [Riku]", "Symphony of Sorcery [Riku]"]

def has_x_sora_worlds(state: CollectionState, player: int, num_of_worlds: int) -> bool:
    worlds_acquired = 0.0
    for i in range(len(SORA_WORLDS)):
        if state.has(SORA_WORLDS[i], player):
            worlds_acquired += 1.0
    return worlds_acquired >= num_of_worlds

def has_x_riku_worlds(state: CollectionState, player: int, num_of_worlds: int) -> bool:
    worlds_acquired = 0.0
    for i in range(len(RIKU_WORLDS)):
        if state.has(RIKU_WORLDS[i], player):
            worlds_acquired += 1.0
    return worlds_acquired >= num_of_worlds

def tt2_access_sora(state:CollectionState, player:int) -> bool:
    return state.count("Traverse Town [Sora]", player) > 1

def tt2_access_riku(state:CollectionState, player:int) -> bool:
    return state.count("Traverse Town [Riku]", player) > 1

def can_access_sora_portals(state:CollectionState, player:int) -> bool:
    soraPortals = ["Traverse Town Secret Portal [Sora]", "La Cite des Cloches Secret Portal [Sora]", "The Grid Secret Portal [Sora]",
                          "Country of the Musketeers Secret Portal [Sora]", "Prankster's Paradise Secret Portal [Sora]", "Symphony of Sorcery Secret Portal [Sora]"]
    soraPortalCount = 6
    currPortalCount = 0
    for x in soraPortals:
        if state.can_reach_location(x, player):
            currPortalCount += 1
    if currPortalCount >= soraPortalCount:
        return True
    return False


def can_access_riku_portals(state:CollectionState, player:int) -> bool:
    rikuPortals = ["Traverse Town Secret Portal [Riku]", "La Cite des Cloches Secret Portal [Riku]",
                   "The Grid Secret Portal [Riku]", "Country of the Musketeers Secret Portal [Riku]", "Prankster's Paradise Secret Portal [Riku]"]
    rikuPortalCount = 5
    currPortalCount = 0
    for x in rikuPortals:
        if state.can_reach_location(x, player):
            currPortalCount += 1
    if currPortalCount >= rikuPortalCount:
        return True
    return False

def has_required_recipes(state:CollectionState, player:int, num_of_recipes: int) -> bool:
    RECIPES = []
    for name, data in get_items_by_category("Recipe").items():
        RECIPES.append(name)

    recipes_acquired = 0
    for recipe in RECIPES:
        if state.has(recipe, player):
            recipes_acquired += 1

    return recipes_acquired >= num_of_recipes

def has_macguffins(state:CollectionState, player:int, num_of_recipes) -> bool:
    return state.has_all({"Meow Wow Recipe", "Komory Bat Recipe", "Recusant Sigil"}, player) and has_required_recipes(state, player, num_of_recipes)

def can_infinite_jump(state: CollectionState, player: int) -> bool:
    return state.has_all({"Wall Kick", "Super Jump"}, player) or state.has("Flowmotion", player)

def can_glide(state: CollectionState, player: int) -> bool:
    return state.has_any({"Glide", "Superglide"}, player) or state.has("Flowmotion", player)

def can_pole_jump(state: CollectionState, player: int) -> bool:
    return state.has_all({"Pole Swing", "Super Jump", "Air Slide"}, player) or state.has("Flowmotion", player)

#Region-specific helpers
def post_office_access(state: CollectionState, player: int) -> bool:
    return state.has_any({"Wall Kick", "Glide", "Rail Slide"}, player) or state.has("Flowmotion", player)

def set_rules(khdddworld):
    multiworld = khdddworld.multiworld
    player = khdddworld.player
    options = khdddworld.options

    #Ensure the player is not expected to level grind much for checks

    #Sora Level Rules

    if options.character == 0 or options.character == 1:
        add_rule(khdddworld.get_location("Sora Level 02"), lambda state: has_x_sora_worlds(state, player, 1))
        add_rule(khdddworld.get_location("Sora Level 03"), lambda state: has_x_sora_worlds(state, player, 1))
        add_rule(khdddworld.get_location("Sora Level 04"), lambda state: has_x_sora_worlds(state, player, 1))
        add_rule(khdddworld.get_location("Sora Level 05"), lambda state: has_x_sora_worlds(state, player, 1))
        add_rule(khdddworld.get_location("Sora Level 06"), lambda state: has_x_sora_worlds(state, player, 2))
        add_rule(khdddworld.get_location("Sora Level 07"), lambda state: has_x_sora_worlds(state, player, 2))
        add_rule(khdddworld.get_location("Sora Level 08"), lambda state: has_x_sora_worlds(state, player, 2))
        add_rule(khdddworld.get_location("Sora Level 09"), lambda state: has_x_sora_worlds(state, player, 2))
        add_rule(khdddworld.get_location("Sora Level 10"), lambda state: has_x_sora_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Sora Level 11"), lambda state: has_x_sora_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Sora Level 12"), lambda state: has_x_sora_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Sora Level 13"), lambda state: has_x_sora_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Sora Level 14"), lambda state: has_x_sora_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Sora Level 15"), lambda state: has_x_sora_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Sora Level 16"), lambda state: has_x_sora_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Sora Level 17"), lambda state: has_x_sora_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Sora Level 18"), lambda state: has_x_sora_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Sora Level 19"), lambda state: has_x_sora_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Sora Level 20"), lambda state: has_x_sora_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Sora Level 21"), lambda state: has_x_sora_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Sora Level 22"), lambda state: has_x_sora_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Sora Level 23"), lambda state: has_x_sora_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Sora Level 24"), lambda state: has_x_sora_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Sora Level 25"), lambda state: has_x_sora_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Sora Level 26"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 27"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 28"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 29"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 30"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 31"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 32"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 33"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 34"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 35"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 36"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 37"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 38"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 39"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 40"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 41"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 42"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 43"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 44"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 45"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 46"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 47"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 48"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 49"), lambda state: has_x_sora_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Sora Level 50"), lambda state: has_x_sora_worlds(state, player, 6))

    # Riku Level Rules
    if options.character == 0 or options.character == 2:
        add_rule(khdddworld.get_location("Riku Level 02"), lambda state: has_x_riku_worlds(state, player, 1))
        add_rule(khdddworld.get_location("Riku Level 03"), lambda state: has_x_riku_worlds(state, player, 1))
        add_rule(khdddworld.get_location("Riku Level 04"), lambda state: has_x_riku_worlds(state, player, 1))
        add_rule(khdddworld.get_location("Riku Level 05"), lambda state: has_x_riku_worlds(state, player, 1))
        add_rule(khdddworld.get_location("Riku Level 06"), lambda state: has_x_riku_worlds(state, player, 2))
        add_rule(khdddworld.get_location("Riku Level 07"), lambda state: has_x_riku_worlds(state, player, 2))
        add_rule(khdddworld.get_location("Riku Level 08"), lambda state: has_x_riku_worlds(state, player, 2))
        add_rule(khdddworld.get_location("Riku Level 09"), lambda state: has_x_riku_worlds(state, player, 2))
        add_rule(khdddworld.get_location("Riku Level 10"), lambda state: has_x_riku_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Riku Level 11"), lambda state: has_x_riku_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Riku Level 12"), lambda state: has_x_riku_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Riku Level 13"), lambda state: has_x_riku_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Riku Level 14"), lambda state: has_x_riku_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Riku Level 15"), lambda state: has_x_riku_worlds(state, player, 3))
        add_rule(khdddworld.get_location("Riku Level 16"), lambda state: has_x_riku_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Riku Level 17"), lambda state: has_x_riku_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Riku Level 18"), lambda state: has_x_riku_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Riku Level 19"), lambda state: has_x_riku_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Riku Level 20"), lambda state: has_x_riku_worlds(state, player, 4))
        add_rule(khdddworld.get_location("Riku Level 21"), lambda state: has_x_riku_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Riku Level 22"), lambda state: has_x_riku_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Riku Level 23"), lambda state: has_x_riku_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Riku Level 24"), lambda state: has_x_riku_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Riku Level 25"), lambda state: has_x_riku_worlds(state, player, 5))
        add_rule(khdddworld.get_location("Riku Level 26"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 27"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 28"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 29"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 30"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 31"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 32"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 33"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 34"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 35"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 36"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 37"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 38"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 39"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 40"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 41"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 42"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 43"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 44"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 45"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 46"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 47"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 48"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 49"), lambda state: has_x_riku_worlds(state, player, 6))
        add_rule(khdddworld.get_location("Riku Level 50"), lambda state: has_x_riku_worlds(state, player, 6))

    ###############################
    #########SORA RULES############
    ###############################

    if options.character == 0 or options.character == 1:
        ###################################
        ############Superbosses############
        ###################################
        if options.superbosses or options.goal == 1:
            add_rule(khdddworld.get_location("Traverse Town Secret Portal [Sora]"),
                     lambda state: has_x_sora_worlds(state, player, 6) and(state.has("High Jump", player) or can_infinite_jump(state, player)))
            add_rule(khdddworld.get_location("La Cite des Cloches Secret Portal [Sora]"),
                     lambda state: has_x_sora_worlds(state, player, 6))
            add_rule(khdddworld.get_location("The Grid Secret Portal [Sora]"),
                     lambda state: has_x_sora_worlds(state, player, 6))
            add_rule(khdddworld.get_location("Prankster's Paradise Secret Portal [Sora]"),
                     lambda state: has_x_sora_worlds(state, player, 6))
            add_rule(khdddworld.get_location("Country of the Musketeers Secret Portal [Sora]"),
                     lambda state: has_x_sora_worlds(state, player, 6))
            add_rule(khdddworld.get_location("Symphony of Sorcery Secret Portal [Sora]"),
                     lambda state: has_x_sora_worlds(state, player, 6) and(state.has("High Jump", player) or can_infinite_jump(state, player)))
            add_rule(khdddworld.get_location("Traverse Town 2 Ultima Weapon Reward [Sora]"),
                     lambda state: can_access_sora_portals(state, player) and (
                         has_required_recipes(state, player, options.recipe_reqs)))
            add_rule(khdddworld.get_location("Unbound Keyblade Reward [Sora]"),
                     lambda state: can_access_sora_portals(state, player))
            if options.goal == 1: #All Superbosses defeated needs a rule here too
                add_rule(khdddworld.get_location("All Superbosses Defeated [Sora] [Riku]"),
                         lambda state: can_access_sora_portals(state, player) and tt2_access_sora(state, player) and has_required_recipes(state, player, options.recipe_reqs))


        ###################################
        ###########Traverse Town###########
        ###################################

        #####Third District Balcony#####
        add_rule(khdddworld.get_location("Traverse Town Third District Vibrant Fantasy [Sora]"),
                 lambda state: state.has_any({"Glide", "Superglide", "High Jump"}, player) or can_infinite_jump(state, player))

        #####Second District Rooftops#####
        add_rule(khdddworld.get_location("Traverse Town Second District Confetti Candy [Sora]"),
                 lambda state: state.has("High Jump", player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Second District Balloon [Sora]"),
                 lambda state: state.has("High Jump", player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Second District Hi-Potion [Sora]"),
                 lambda state: state.has("High Jump", player) or can_infinite_jump(state, player))

        #Everything in and beyond Sora's Post Office room should require this movement for the player's own sanity

        #####Post Office#####
        add_rule(khdddworld.get_location("Traverse Town Post Office Rampant Fantasy [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Post Office Vibrant Fantasy [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Post Office Troubling Fantasy [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Post Office Spark [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Post Office Paint Gun: Red [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Post Office Potion [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Post Office Ice Dream Cone [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))

        #####Fountain Plaza#####
        add_rule(khdddworld.get_location("Traverse Town Fountain Plaza Balloon [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fountain Plaza Intrepid Figment [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fountain Plaza Ice Dream Cone [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fountain Plaza Rampant Fantasy [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) and (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fountain Plaza Strike Raid [Sora]"),
                 lambda state: state.has_any({"Glide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))

        #####Fourth District#####
        add_rule(khdddworld.get_location("Traverse Town Fourth District Shield Cookie [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fourth District Water Barrel [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fourth District Hi-Potion [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fourth District Ice Dream Cone [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fourth District Potion [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fourth District Block-It Chocolate [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fourth District 2nd Potion [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fourth District Balloon (Command) [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))

        #####Fifth District#####
        add_rule(khdddworld.get_location("Traverse Town Fifth District Shield Cookie [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fifth District Potion [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Fifth District Block-It Chocolate [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))

        #####Garden#####
        add_rule(khdddworld.get_location("Traverse Town Garden Royal Cake [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Garden Confetti Candy [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Garden Rampant Figment [Sora]"), #On the upper ledge
                 lambda state: state.has_any({"Rail Slide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Traverse Town Garden Drop-Me-Not [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or (can_infinite_jump(state, player)))


        #####Story#####
        add_rule(khdddworld.get_location("Traverse Town Hockomonkey Bonus Slot 1 [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Hockomonkey Bonus Slot 2 [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Skull Noise Reward [Sora]"),
                 lambda state: state.has_any({"Glide", "Rail Slide", "Superglide", "Flowmotion"}, player) or can_infinite_jump(state, player))

        ###################################
        ########La Cite des Cloches########
        ###################################
        add_rule(khdddworld.get_location("La Cite des Cloches Bell Tower Dulcet Figment [Sora]"),
                 lambda state: state.has_any({"Flowmotion", "High Jump"}, player) or (can_pole_jump(state, player)) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("La Cite des Cloches Bell Tower Drop-Me-Not [Sora]"),
                 lambda state: state.has_any({"Flowmotion", "High Jump"}, player) or (can_pole_jump(state, player)) or (can_infinite_jump(state, player)))

        ###################################
        ##############The Grid#############
        ###################################
        for name, data in location_data_table.items(): #Sora can only reach the first location without tools
            if data.region == "The Grid [Sora]" and name != "The Grid City Potion [Sora]":

                if name == "The Grid Secret Portal [Sora]":
                    if not options.superbosses and options.goal == 0:
                        continue

                add_rule(khdddworld.get_location(name),
                         lambda state: (state.has_any({"Air Slide", "Glide", "Superglide", "Rail Slide", "Flowmotion"}, player)
                         or can_infinite_jump(state, player)))

        add_rule(khdddworld.get_location("The Grid Throughput Dulcet Figment [Sora]"),
                lambda state: (state.has_any({"High Jump", "Rail Slide", "Flowmotion"}, player)
                or (can_infinite_jump(state, player)) or (can_pole_jump(state, player))))
        add_rule(khdddworld.get_location("The Grid City Troubling Fancy [Sora]"),
                    lambda state: (state.has("Flowmotion", player)
                    or (can_infinite_jump(state, player)) or (state.has_any({"Glide", "Superglide"}, player))))

        ###################################
        ########Prankster's Paradise#######
        ###################################
        add_rule(khdddworld.get_location("Prankster's Paradise Windup Way Aerial Slam [Sora]"),
                 lambda state: can_infinite_jump(state, player) or (state.has("High Jump", player) and can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Prankster's Paradise Windup Way Royal Cake [Sora]"),
                 lambda state: can_infinite_jump(state, player) or (state.has("High Jump", player) and can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Prankster's Paradise Circus Rampant Fancy [Sora]"),
                 lambda state: can_infinite_jump(state, player) or (state.has("High Jump", player) and can_pole_jump(state, player)))

        ###################################
        #####Country of the Musketeers#####
        ###################################
        add_rule(khdddworld.get_location("Country of the Musketeers Mont Saint-Michel Sparkga [Sora]"),
                 lambda state: (can_infinite_jump(state, player) or (state.has_any({"High Jump", "Flowmotion"}, player))))

        ###################################
        ########Symphony of Sorcery########
        ###################################
        add_rule(khdddworld.get_location("Symphony of Sorcery Cloudwalk Candy Goggles [Sora]"),
                 lambda state: (state.has_any({"Wall Kick", "Superglide", "Glide", "Flowmotion"}, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Glen Royal Cake [Sora]"),
                 lambda state: (state.has_any({"Wall Kick", "Superglide", "Glide", "Flowmotion"}, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Glen Intrepid Fantasy [Sora]"),
                 lambda state: (state.has_any({"Wall Kick", "Superglide", "Glide", "Flowmotion"}, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Fields Electricorn Recipe [Sora]"),
                 lambda state: (state.has_any({"Superglide", "Glide", "Flowmotion"}, player) or (can_infinite_jump(state, player))))

        ###################################
        #####The World That Never Was######
        ###################################
        add_rule(khdddworld.get_location("The World That Never Was Xemnas Bonus Slot 1 [Sora]"),
                 lambda state: (can_infinite_jump(state, player) or (state.has("High Jump", player)
                        and (state.has_any({"Air Slide", "Glide"}, player))) or (state.has("Flowmotion", player))))

        add_rule(khdddworld.get_location("The World That Never Was Glossary: Recusant's Sigil Reward [Sora]"),
                 lambda state: (can_infinite_jump(state, player) or (state.has("High Jump", player)
                        and (state.has_any({"Air Slide", "Glide"}, player))) or (state.has("Flowmotion", player))))

        add_rule(khdddworld.get_location("The World That Never Was Glossary: Hearts Tied to Sora Reward [Sora]"),
                 lambda state: (can_infinite_jump(state, player) or (state.has("High Jump", player)
                        and (state.has_any({"Air Slide", "Glide"}, player))) or (state.has("Flowmotion", player))))

        add_rule(khdddworld.get_location("The World That Never Was Contorted City Ice Dream Cone 3 [Sora]"),
                 lambda state: (can_infinite_jump(state, player) or (state.has("Flowmotion", player))
                        or (state.has("High Jump", player) and (state.has_any({"Air Slide", "Glide"}, player)))))

        #####Add Macguffin Rules#####
        add_rule(khdddworld.get_location("The World That Never Was Xemnas Bonus Slot 1 [Sora]"),
                 lambda state: has_macguffins(state, player, options.recipe_reqs))
        add_rule(khdddworld.get_location("The World That Never Was Glossary: Recusant's Sigil Reward [Sora]"),
                 lambda state: has_macguffins(state, player, options.recipe_reqs))
        add_rule(khdddworld.get_location("The World That Never Was Glossary: Hearts Tied to Sora Reward [Sora]"),
                 lambda state: has_macguffins(state, player, options.recipe_reqs))

    ###############################
    #########RIKU RULES############
    ###############################

    if options.character == 0 or options.character == 2:
        ###################################
        ############Superbosses############
        ###################################
        if options.superbosses or options.goal == 1:
            add_rule(khdddworld.get_location("Traverse Town Secret Portal [Riku]"), lambda state: has_x_riku_worlds(state, player, 6)
                                                                                            and (state.has_any({"Rail Slide", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player)))
            add_rule(khdddworld.get_location("La Cite des Cloches Secret Portal [Riku]"), lambda state: has_x_riku_worlds(state, player, 6) and state.has("Air Slide", player))
            add_rule(khdddworld.get_location("The Grid Secret Portal [Riku]"), lambda state: has_x_riku_worlds(state, player, 6))
            add_rule(khdddworld.get_location("Prankster's Paradise Secret Portal [Riku]"), lambda state: has_x_riku_worlds(state, player, 6))
            add_rule(khdddworld.get_location("Country of the Musketeers Secret Portal [Riku]"), lambda state: has_x_riku_worlds(state, player, 6))
            add_rule(khdddworld.get_location("Traverse Town 2 Ultima Weapon Reward [Riku]"), lambda state: can_access_riku_portals(state, player) and (has_required_recipes(state, player, options.recipe_reqs)))
            add_rule(khdddworld.get_location("Unbound Keyblade Reward [Riku]"), lambda state: can_access_riku_portals(state, player))
            if options.goal == 1:
                add_rule(khdddworld.get_location("All Superbosses Defeated [Sora] [Riku]"),
                         lambda state: can_access_riku_portals(state, player) and tt2_access_riku(state, player) and has_required_recipes(state, player, options.recipe_reqs))

        ###################################
        ###########Traverse Town###########
        ###################################
        add_rule(khdddworld.get_location("Traverse Town Second District Block-It Chocolate [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Second District Balloon [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Traverse Town Second District Yoggy Ram Recipe [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player))

        add_rule(khdddworld.get_location("Traverse Town Third District Ice Dream Cone [Riku]"),
                 lambda state: state.has_any({"Double Flight", "Flowmotion"}, player) or (
                     can_infinite_jump(state, player)) or state.has_all({"High Jump", "Wall Kick"}, player))

        add_rule(khdddworld.get_location("Traverse Town Back Streets Troubling Fantasy [Riku]"),
                 lambda state: state.has_all({"Double Flight", "Air Slide"}, player) or (
                     can_infinite_jump(state, player)) or (state.has("Flowmotion", player)))

        add_rule(khdddworld.get_location("Traverse Town Back Streets Intrepid Figment [Riku]"),
                 lambda state: state.has_all({"Double Flight", "Air Slide"}, player) or (
                     can_infinite_jump(state, player)) or state.has("Flowmotion", player))

        add_rule(khdddworld.get_location("Traverse Town Garden Royal Cake [Riku]"),
                 lambda state: state.has_any({"Rail Slide, Flowmotion"}, player) or can_infinite_jump(state, player))

        ###################################
        ########La Cite des Cloches########
        ###################################
        add_rule(khdddworld.get_location("La Cite des Cloches Bell Tower Royal Cake [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "High Jump", "Double Flight"}, player) or (
                     can_pole_jump(state, player)) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("La Cite des Cloches Bell Tower Dulcet Figment [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "High Jump", "Double Flight"}, player) or (
                     can_pole_jump(state, player)) or (can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("La Cite des Cloches Wargoyle Bonus Slot 1 [Riku]"), #Require Air Slide for these checks for convenience
                 lambda state: state.has("Air Slide", player))
        add_rule(khdddworld.get_location("La Cite des Cloches Wargoyle Bonus Slot 2 [Riku]"),
                 lambda state: state.has("Air Slide", player))
        add_rule(khdddworld.get_location("La Cite des Cloches Chronicle: Kingdom Hearts Reward [Riku]"),
                 lambda state: state.has("Air Slide", player))
        add_rule(khdddworld.get_location("La Cite des Cloches Guardian Bell Reward [Riku]"),
                 lambda state: state.has("Air Slide", player))

        ###################################
        ##############The Grid#############
        ###################################
        add_rule(khdddworld.get_location("The Grid City Fleeting Figment [Riku]"),
                 lambda state: (state.has_any({"Air Slide", "Flowmotion", "Rail Slide"}, player)
                        or (can_infinite_jump(state, player))))
        add_rule(khdddworld.get_location("The Grid City Drop-Me-Not [Riku]"),
                 lambda state: (state.has_any({"Air Slide", "Flowmotion", "Rail Slide"}, player)
                        or (can_infinite_jump(state, player))))
        add_rule(khdddworld.get_location("The Grid City Thundara [Riku]"),
                 lambda state: (state.has("Flowmotion", player)
                         or (can_infinite_jump(state, player))))
        add_rule(khdddworld.get_location("The Grid Throughput Noble Fantasy [Riku]"),
                 lambda state: (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player)
                         or (can_infinite_jump(state, player)) or (can_pole_jump(state, player))))

        ###################################
        ########Prankster's Paradise#######
        ###################################
        #Both of these are technically possible without flowmotion
        add_rule(khdddworld.get_location("Prankster's Paradise Monstro: Gullet Charming Fantasy [Riku]"),
                 lambda state: state.has("Flowmotion", player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("Prankster's Paradise Monstro: Gullet Sir Kyroo Recipe [Riku]"),
                 lambda state: (state.has_any({"Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))

        ###################################
        #####Country of the Musketeers#####
        ###################################

        #####Grand Lobby#####
        add_rule(khdddworld.get_location("Country of the Musketeers Grand Lobby Shadowbreaker [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight"}, player) or can_infinite_jump(state, player)))

        #####Green Room#####
        add_rule(khdddworld.get_location("Country of the Musketeers Green Room Candy Goggles [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Green Room Prickly Fantasy [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Green Room Fleeting Fantasy [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Green Room Shield Cookie 3 [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Green Room Hi-Potion [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Green Room Stop [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Green Room Drop-Me-Not [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Green Room Confetti Candy 3 [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))

        #####Machine Room#####
        add_rule(khdddworld.get_location("Country of the Musketeers Machine Room Blizzaga [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Machine Room Ducky Goose Recipe [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Machine Room Ice Dream Cone 2 [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Machine Room Drop-Me-Not [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Machine Room Hi-Potion [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Machine Room Mega-Potion [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))

        #####Backstage#####
        add_rule(khdddworld.get_location("Country of the Musketeers Backstage Royal Cake [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Backstage Fleeting Fantasy [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Backstage Dream Candy [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Backstage Staggerceps Recipe [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Backstage Drop-Me-Not [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Backstage Mega-Potion [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))

        #####Story#####
        add_rule(khdddworld.get_location("Country of the Musketeers Flashback: Bon Journey Reward [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Stage Gadget Reward [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Holey Moley Bonus Slot 1 [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Shadow Strike Reward [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers Shadow Slide Reward [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))
        add_rule(khdddworld.get_location("Country of the Musketeers All For One Reward [Riku]"),
                 lambda state: state.has_any({"Pole Spin", "Flowmotion"}, player)
                        and (state.has_any({"High Jump", "Double Flight", "Rail Slide", "Flowmotion"}, player) or can_infinite_jump(state, player)))

        ###################################
        ########Symphony of Sorcery########
        ###################################

        #####Moonlight Wood#####
        add_rule(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Zero Graviza [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))
        add_rule(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Paint Gun: Green [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))
        add_rule(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Intrepid Fancy [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))

        if options.lord_kyroo:
            add_rule(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Lord Kyroo Fight [Riku]"),
                     lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))

        #####Golden Wood#####
        add_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Elixir [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))
        add_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Intrepid Fantasy [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))
        add_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Mega-Potion [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Paint Gun: Red [Riku]"),
                 lambda state: state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))
        add_rule(khdddworld.get_location("Symphony of Sorcery Golden Wood Ryu Dragon Recipe [Riku]"),
                 lambda state: state.has_any({"Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))

        #####Snowgleam Wood#####
        add_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Ice Barrage [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Candy Goggles [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Block-It Chocolate [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Ice Dream Cone 3 [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Dulcet Fancy [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Snowgleam Wood Confetti Candy 3 [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))

        #####Story#####
        add_rule(khdddworld.get_location("Symphony of Sorcery Chernobog Bonus Slot 1 [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Chernobog Bonus Slot 2 [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))
        add_rule(khdddworld.get_location("Symphony of Sorcery Counterpoint Reward [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player)
                               and (state.has_any({"High Jump", "Double Flight", "Flowmotion"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player)))

        ###################################
        #####The World That Never Was######
        ###################################
        add_rule(khdddworld.get_location("The World That Never Was Delusive Beginning Third Elixir [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide", "High Jump"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))
        add_rule(khdddworld.get_location("The World That Never Was Delusive Beginning Keeba Tiger Recipe [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide", "High Jump"}, player) or can_infinite_jump(state, player) or can_pole_jump(state, player))

        add_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Candy Goggles [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Second Elixir [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Shield Cookie 3 [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Skelterwild Recipe [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player) or can_infinite_jump(state, player))
        add_rule(khdddworld.get_location("The World That Never Was Verge of Chaos Wondrous Fantasy [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player) or can_infinite_jump(state, player))

        add_rule(khdddworld.get_location("The World That Never Was Ansem II Bonus Slot 1 [Riku]"),
                 lambda state: state.has_any({"Flowmotion", "Rail Slide"}, player) and state.has("Air Slide", player))

        if options.goal == 0: #YX/AVN can only be played with Final Boss goal
            if options.character == 0:
                add_rule(khdddworld.get_location("The World That Never Was Young Xehanort Defeated [Riku]"),
                    lambda state: (state.can_reach(khdddworld.get_location("The World That Never Was Xemnas Bonus Slot 1 [Sora]"), player)))
            elif options.character == 2:
                 add_rule(khdddworld.get_location("The World That Never Was Young Xehanort Defeated [Riku]"),
             lambda state: (state.has_all({"Meow Wow Recipe", "Komory Bat Recipe", "Recusant Sigil"}, player) and(has_required_recipes(state, player, options.recipe_reqs))))

            if options.armored_ventus_nightmare:
                add_rule(khdddworld.get_location("Armored Ventus Nightmare Defeated [Riku]"),
                    lambda state: (state.can_reach(khdddworld.get_location("The World That Never Was Young Xehanort Defeated [Riku]"), player)))

            if not options.fast_go_mode: #Additionally require Rail Slide
                add_rule(khdddworld.get_location("The World That Never Was Young Xehanort Defeated [Riku]"),
                         lambda state: state.has_any({"Rail Slide", "Flowmotion"}, player))
                if options.armored_ventus_nightmare:
                    add_rule(khdddworld.get_location("Armored Ventus Nightmare Defeated [Riku]"),
                         lambda state: state.has_any({"Rail Slide", "Flowmotion"}, player))


    #Lord Kyroo Completion Access
    if options.lord_kyroo:
        if options.character == 0 or options.character == 1:
            add_rule(khdddworld.get_location("Lord Kyroo Defeated [Sora] [Riku]"),
                     lambda state: state.can_reach(khdddworld.get_location("Prankster's Paradise Promontory Lord Kyroo Fight [Sora]"), player))
        elif options.character == 0 or options.character == 2:
            add_rule(khdddworld.get_location("Lord Kyroo Defeated [Sora] [Riku]"),
                     lambda state: state.can_reach(khdddworld.get_location("La Cite des Cloches Nave Lord Kyroo Fight [Riku]"), player))
            add_rule(khdddworld.get_location("Lord Kyroo Defeated [Sora] [Riku]"),
                     lambda state: state.can_reach(khdddworld.get_location("Symphony of Sorcery Moonlight Wood Lord Kyroo Fight [Riku]"), player))

    #Region rules
    if options.character == 0:
        add_rule(khdddworld.get_entrance("Levels"),
                 lambda state: has_x_sora_worlds(state, player, 1) or (has_x_riku_worlds(state, player, 1)))
    elif options.character == 1:
        add_rule(khdddworld.get_entrance("Levels"),
                 lambda state: has_x_sora_worlds(state, player, 1))
    elif options.character == 2:
        add_rule(khdddworld.get_entrance("Levels"),
                 lambda state: has_x_riku_worlds(state, player, 1))

    add_rule(khdddworld.get_entrance("Traverse Town [Sora]"),
             lambda state: state.has("Traverse Town [Sora]", player))
    add_rule(khdddworld.get_entrance("The Grid [Sora]"),
             lambda state: state.has("The Grid [Sora]", player))
    add_rule(khdddworld.get_entrance("La Cite des Cloches [Sora]"),
             lambda state: state.has("La Cite des Cloches [Sora]", player))
    add_rule(khdddworld.get_entrance("Prankster's Paradise [Sora]"),
             lambda state: state.has("Prankster's Paradise [Sora]", player))
    add_rule(khdddworld.get_entrance("Country of the Musketeers [Sora]"),
             lambda state: state.has("Country of the Musketeers [Sora]", player))
    add_rule(khdddworld.get_entrance("The World That Never Was [Sora]"),
             lambda state: state.has("The World That Never Was [Sora]", player) and has_x_sora_worlds(state, player, 3))
    add_rule(khdddworld.get_entrance("Symphony of Sorcery [Sora]"),
             lambda state: state.has("Symphony of Sorcery [Sora]", player))
    add_rule(khdddworld.get_entrance("Traverse Town 2 [Sora]"),
             lambda state: state.has_any({"Wall Kick", "Glide", "Superglide", "Rail Slide", "Flowmotion"}, player) and (state.count("Traverse Town [Sora]", player) > 1))

    add_rule(khdddworld.get_entrance("Traverse Town [Riku]"),
             lambda state: state.has("Traverse Town [Riku]", player))
    add_rule(khdddworld.get_entrance("The Grid [Riku]"),
             lambda state: state.has("The Grid [Riku]", player))
    add_rule(khdddworld.get_entrance("La Cite des Cloches [Riku]"),
             lambda state: state.has("La Cite des Cloches [Riku]", player))
    add_rule(khdddworld.get_entrance("Prankster's Paradise [Riku]"),
             lambda state: state.has("Prankster's Paradise [Riku]", player))
    add_rule(khdddworld.get_entrance("Country of the Musketeers [Riku]"),
             lambda state: state.has("Country of the Musketeers [Riku]", player))
    add_rule(khdddworld.get_entrance("The World That Never Was [Riku]"),
             lambda state: state.has("The World That Never Was [Riku]", player) and has_x_riku_worlds(state, player, 3))
    add_rule(khdddworld.get_entrance("Symphony of Sorcery [Riku]"),
             lambda state: state.has("Symphony of Sorcery [Riku]", player))
    add_rule(khdddworld.get_entrance("Traverse Town 2 [Riku]"),
             lambda state: state.count("Traverse Town [Riku]", player) > 1)



    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
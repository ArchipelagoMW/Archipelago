from ..generic.Rules import add_item_rule, add_rule, location_item_name
from .items import item_groups


def set_rules(world, player):

    item_rules = {
        "Pallet Town - Player's PC": (lambda i: i.player == player and "Badge" not in i.name and "Trap" not in i.name
                                      and i.name != "Pokedex" and "Coins" not in i.name)
    }

    if world.prizesanity[player]:
        def prize_rule(i):
            return i.player != player or i.name in item_groups["Unique"]
        item_rules["Celadon Prize Corner - Item Prize 1"] = prize_rule
        item_rules["Celadon Prize Corner - Item Prize 2"] = prize_rule
        item_rules["Celadon Prize Corner - Item Prize 3"] = prize_rule

    if world.accessibility[player] != "locations":
        world.get_location("Cerulean City - Bicycle Shop", player).always_allow = (lambda state, item:
                                                                                   item.name == "Bike Voucher"
                                                                                   and item.player == player)
        world.get_location("Fuchsia City - Safari Zone Warden", player).always_allow = (lambda state, item:
                                                                                        item.name == "Gold Teeth" and
                                                                                        item.player == player)

    access_rules = {
        "Pallet Town - Rival's Sister": lambda state: state.has("Oak's Parcel", player),
        "Pallet Town - Oak's Post-Route-22-Rival Gift": lambda state: state.has("Oak's Parcel", player),
        "Viridian City - Sleepy Guy": lambda state: state.pokemon_rb_can_cut(player) or state.pokemon_rb_can_surf(player),
        "Route 2 - Oak's Aide": lambda state: state.pokemon_rb_oaks_aide(state.multiworld.oaks_aide_rt_2[player].value + 5, player),
        "Pewter City - Museum": lambda state: state.pokemon_rb_can_cut(player),
        "Cerulean City - Bicycle Shop": lambda state: state.has("Bike Voucher", player)
            or location_item_name(state, "Cerulean City - Bicycle Shop", player) == ("Bike Voucher", player),
        "Lavender Town - Mr. Fuji": lambda state: state.has("Fuji Saved", player),
        "Vermilion Gym - Lt. Surge 1": lambda state: state.pokemon_rb_can_cut(player or state.pokemon_rb_can_surf(player)),
        "Vermilion Gym - Lt. Surge 2": lambda state: state.pokemon_rb_can_cut(player or state.pokemon_rb_can_surf(player)),
        "Route 11 - Oak's Aide": lambda state: state.pokemon_rb_oaks_aide(state.multiworld.oaks_aide_rt_11[player].value + 5, player),
        "Celadon City - Stranded Man": lambda state: state.pokemon_rb_can_surf(player),
        "Silph Co 11F - Silph Co President (Card Key)": lambda state: state.has("Card Key", player),
        "Fuchsia City - Safari Zone Warden": lambda state: state.has("Gold Teeth", player)
            or location_item_name(state, "Fuchsia City - Safari Zone Warden", player) == ("Gold Teeth", player),
        "Route 12 - Island Item": lambda state: state.pokemon_rb_can_surf(player),
        "Route 12 - Item Behind Cuttable Tree": lambda state: state.pokemon_rb_can_cut(player),
        "Route 15 - Oak's Aide": lambda state: state.pokemon_rb_oaks_aide(state.multiworld.oaks_aide_rt_15[player].value + 5, player),
        "Route 15 - Item": lambda state: state.pokemon_rb_can_cut(player),
        "Route 25 - Item": lambda state: state.pokemon_rb_can_cut(player),
        "Fuchsia City - Warden's House Item": lambda state: state.pokemon_rb_can_strength(player),
        "Rocket Hideout B4F - Southwest Item (Lift Key)": lambda state: state.has("Lift Key", player),
        "Rocket Hideout B4F - Giovanni Item (Lift Key)": lambda state: state.has("Lift Key", player),
        "Silph Co 3F - Item (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 4F - Left Item (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 4F - Middle Item (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 4F - Right Item (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 5F - Northwest Item (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 6F - West Item (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 6F - Southwest Item (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 7F - East Item (Card Key)": lambda state: state.has("Card Key", player),
        "Safari Zone Center - Island Item": lambda state: state.pokemon_rb_can_surf(player),
        "Celadon Prize Corner - Item Prize 1": lambda state: state.has("Coin Case", player),
        "Celadon Prize Corner - Item Prize 2": lambda state: state.has("Coin Case", player),
        "Celadon Prize Corner - Item Prize 3": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - West Gambler's Gift (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Center Gambler's Gift (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - East Gambler's Gift (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Northwest By Counter (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Southwest Corner (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Near Rumor Man (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Near Speculating Woman (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Near West Gifting Gambler (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Near Wonderful Time Woman (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Near Failing Gym Information Guy (Coin Case)": lambda state: state.has( "Coin Case", player),
        "Celadon Game Corner - Hidden Item Near East Gifting Gambler (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Near Hooked Guy (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item at End of Horizontal Machine Row (Coin Case)": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item in Front of Horizontal Machine Row (Coin Case)": lambda state: state.has("Coin Case", player),

        "Silph Co 11F - Silph Co Liberated": lambda state: state.has("Card Key", player),

        "Pallet Town - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Pallet Town - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Route 22 - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Route 22 - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Route 24 - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Route 24 - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Route 24 - Super Rod Pokemon - 3": lambda state: state.has("Super Rod", player),
        "Route 6 - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Route 6 - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Route 10 - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Route 10 - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Safari Zone Center - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Safari Zone Center - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Safari Zone Center - Super Rod Pokemon - 3": lambda state: state.has("Super Rod", player),
        "Safari Zone Center - Super Rod Pokemon - 4": lambda state: state.has("Super Rod", player),
        "Route 12 - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Route 12 - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Route 12 - Super Rod Pokemon - 3": lambda state: state.has("Super Rod", player),
        "Route 12 - Super Rod Pokemon - 4": lambda state: state.has("Super Rod", player),
        "Route 19 - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Route 19 - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Route 19 - Super Rod Pokemon - 3": lambda state: state.has("Super Rod", player),
        "Route 19 - Super Rod Pokemon - 4": lambda state: state.has("Super Rod", player),
        "Route 23 - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Route 23 - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Route 23 - Super Rod Pokemon - 3": lambda state: state.has("Super Rod", player),
        "Route 23 - Super Rod Pokemon - 4": lambda state: state.has("Super Rod", player),
        "Fuchsia City - Super Rod Pokemon - 1": lambda state: state.has("Super Rod", player),
        "Fuchsia City - Super Rod Pokemon - 2": lambda state: state.has("Super Rod", player),
        "Fuchsia City - Super Rod Pokemon - 3": lambda state: state.has("Super Rod", player),
        "Fuchsia City - Super Rod Pokemon - 4": lambda state: state.has("Super Rod", player),
        "Anywhere - Good Rod Pokemon - 1": lambda state: state.has("Good Rod", player),
        "Anywhere - Good Rod Pokemon - 2": lambda state: state.has("Good Rod", player),
        "Anywhere - Old Rod Pokemon": lambda state: state.has("Old Rod", player),
        "Celadon Prize Corner - Pokemon Prize - 1": lambda state: state.has("Coin Case", player),
        "Celadon Prize Corner - Pokemon Prize - 2": lambda state: state.has("Coin Case", player),
        "Celadon Prize Corner - Pokemon Prize - 3": lambda state: state.has("Coin Case", player),
        "Celadon Prize Corner - Pokemon Prize - 4": lambda state: state.has("Coin Case", player),
        "Celadon Prize Corner - Pokemon Prize - 5": lambda state: state.has("Coin Case", player),
        "Celadon Prize Corner - Pokemon Prize - 6": lambda state: state.has("Coin Case", player),
        "Cinnabar Island - Old Amber Pokemon": lambda state: state.has("Old Amber", player),
        "Cinnabar Island - Helix Fossil Pokemon": lambda state: state.has("Helix Fossil", player),
        "Cinnabar Island - Dome Fossil Pokemon": lambda state: state.has("Dome Fossil", player),
        "Route 12 - Sleeping Pokemon": lambda state: state.has("Poke Flute", player),
        "Route 16 - Sleeping Pokemon": lambda state: state.has("Poke Flute", player),
        "Seafoam Islands B4F - Legendary Pokemon": lambda state: state.pokemon_rb_can_strength(player),
        "Vermilion City - Legendary Pokemon": lambda state: state.pokemon_rb_can_surf(player) and state.has("S.S. Ticket", player),

        "Route 2 - Marcel Trade": lambda state: state.can_reach("Route 24 - Wild Pokemon - 6", "Location", player),
        "Underground Tunnel West-East - Spot Trade": lambda state: state.can_reach("Route 24 - Wild Pokemon - 6", "Location", player),
        "Route 11 - Terry Trade": lambda state: state.can_reach("Safari Zone Center - Wild Pokemon - 5", "Location", player),
        "Route 18 - Marc Trade": lambda state: state.can_reach("Route 23 - Super Rod Pokemon - 1", "Location", player),
        "Cinnabar Island - Sailor Trade": lambda state: state.can_reach("Pokemon Mansion 1F - Wild Pokemon - 3", "Location", player),
        "Cinnabar Island - Crinkles Trade": lambda state: state.can_reach("Route 12 - Wild Pokemon - 4", "Location", player),
        "Cinnabar Island - Doris Trade": lambda state: state.can_reach("Cerulean Cave 1F - Wild Pokemon - 9", "Location", player),
        "Vermilion City - Dux Trade": lambda state: state.can_reach("Route 3 - Wild Pokemon - 2", "Location", player),
        "Cerulean City - Lola Trade": lambda state: state.can_reach("Route 10 - Super Rod Pokemon - 1", "Location", player),

        # Pokédex check
        "Pallet Town - Oak's Parcel Reward": lambda state: state.has("Oak's Parcel", player),

        # trainers
        "Route 4 - Cooltrainer F": lambda state: state.pokemon_rb_can_surf(player),
        "Route 15 - Jr. Trainer F 1": lambda state: state.pokemon_rb_can_cut(player),
        "Silph Co 11F - Rocket 2 (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 9F - Rocket 2 (Card Key)": lambda state: state.has("Card Key", player),
        "Silph Co 3F - Scientist (Card Key)": lambda state: state.has("Card Key", player),
        "Route 10 North - Pokemaniac": lambda state: state.pokemon_rb_can_surf(player),
        "Rocket Hideout B1F - Rocket 5 (Lift Key)": lambda state: state.has("Lift Key", player),
        "Rocket Hideout B4F - Rocket 2 (Lift Key)": lambda state: state.has("Lift Key", player),
        "Rocket Hideout B4F - Rocket 3 (Lift Key)": lambda state: state.has("Lift Key", player),

        # hidden items
        "Viridian Forest - Hidden Item Northwest by Trainer": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Viridian Forest - Hidden Item Entrance Tree": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Mt Moon B2F - Hidden Item Dead End Before Fossils": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Route 25 - Hidden Item Fence Outside Bill's House": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Route 9 - Hidden Item Bush By Grass": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "S.S. Anne 1F - Hidden Item Kitchen Trash": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "S.S. Anne B1F - Hidden Item Under Pillow": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 10 - Hidden Item Behind Rock Tunnel Entrance Cuttable Tree": lambda
            state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 10 - Hidden Item Bush": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Rocket Hideout B1F - Hidden Item Pot Plant": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Rocket Hideout B3F - Hidden Item Near East Item": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Rocket Hideout B4F - Hidden Item Behind Giovanni (Lift Key)": lambda state:
            state.pokemon_rb_can_get_hidden_items(player) and state.has("Lift Key", player),
        "Pokemon Tower 5F - Hidden Item Near West Staircase": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Route 13 - Hidden Item Dead End Bush": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 13 - Hidden Item Dead End By Water Corner": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Pokemon Mansion B1F - Hidden Item Secret Key Room Corner": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Safari Zone West - Hidden Item Secret House Statue": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Silph Co 5F - Hidden Item Pot Plant": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Silph Co 9F - Hidden Item Nurse Bed (Card Key)": lambda state: state.pokemon_rb_can_get_hidden_items(
            player) and state.has("Card Key", player),
        "Copycat's House - Hidden Item Desk": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Cerulean Cave 1F - Hidden Item Center Rocks": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Cerulean Cave B1F - Hidden Item Northeast Rocks": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Power Plant - Hidden Item Central Dead End": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Power Plant - Hidden Item Before Zapdos": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Seafoam Islands B2F - Hidden Item Rock": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Seafoam Islands B4F - Hidden Item Corner Island": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Pokemon Mansion 1F - Hidden Item Block Near Entrance Carpet": lambda
            state: state.pokemon_rb_can_get_hidden_items(player),
        "Pokemon Mansion 3F - Hidden Item Behind Burglar": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 23 - Hidden Item Rocks Before Victory Road": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Route 23 - Hidden Item East Bush After Water": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Route 23 - Hidden Item On Island": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Victory Road 2F - Hidden Item Rock Before Moltres": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Victory Road 2F - Hidden Item Rock In Final Room": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Viridian City - Hidden Item Cuttable Tree": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 11 - Hidden Item Isolated Bush Near Gate": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 12 - Hidden Item Bush Near Gate": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 17 - Hidden Item In Grass": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 17 - Hidden Item Near Northernmost Sign": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 17 - Hidden Item East Center": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 17 - Hidden Item West Center": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Route 17 - Hidden Item Before Final Bridge": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Underground Tunnel North-South - Hidden Item Near Northern Stairs": lambda
            state: state.pokemon_rb_can_get_hidden_items(player),
        "Underground Tunnel North-South - Hidden Item Near Southern Stairs": lambda
            state: state.pokemon_rb_can_get_hidden_items(player),
        "Underground Tunnel West-East - Hidden Item West": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Underground Tunnel West-East - Hidden Item East": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Celadon City - Hidden Item Dead End Near Cuttable Tree": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Route 25 - Hidden Item Northeast Of Grass": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Mt Moon B2F - Hidden Item Lone Rock": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Seafoam Islands B3F - Hidden Item Rock": lambda state: state.pokemon_rb_can_get_hidden_items(player),
        "Vermilion City - Hidden Item In Water Near Fan Club": lambda state: state.pokemon_rb_can_get_hidden_items(
            player) and state.pokemon_rb_can_surf(player),
        "Cerulean City - Hidden Item Gym Badge Guy's Backyard": lambda state: state.pokemon_rb_can_get_hidden_items(
            player),
        "Route 4 - Hidden Item Plateau East Of Mt Moon": lambda state: state.pokemon_rb_can_get_hidden_items(player),
    }
    for loc in world.get_locations(player):
        if loc.name in access_rules:
            add_rule(loc, access_rules[loc.name])
        if loc.name in item_rules:
            add_item_rule(loc, item_rules[loc.name])
        if loc.name.startswith("Pokedex"):
            mon = loc.name.split(" - ")[1]
            add_rule(loc, lambda state, i=mon: (state.has("Pokedex", player) or not
                     state.multiworld.require_pokedex[player]) and (state.has(i, player)
                                                                    or state.has(f"Static {i}", player)))


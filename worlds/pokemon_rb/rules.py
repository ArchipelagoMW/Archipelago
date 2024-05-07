from worlds.generic.Rules import add_item_rule, add_rule, location_item_name
from .items import item_groups
from . import logic


def set_rules(multiworld, player):

    item_rules = {
        # Some items do special things when they are passed into the GiveItem function in the game, but
        # withdrawing from the PC or buying from a shop will not call the function and will add the items
        # directly to the inventory, so we need to avoid placing these special items (including "AP Item") to
        # such places
        "Player's House 2F - Player's PC": (lambda i: i.player == player and "Badge" not in i.name and "Trap" not in
                                            i.name and i.name != "Pokedex" and "Coins" not in i.name and "Progressive"
                                            not in i.name)
    }

    if multiworld.prizesanity[player]:
        def prize_rule(i):
            return i.player != player or i.name in item_groups["Unique"]
        item_rules["Celadon Prize Corner - Item Prize 1"] = prize_rule
        item_rules["Celadon Prize Corner - Item Prize 2"] = prize_rule
        item_rules["Celadon Prize Corner - Item Prize 3"] = prize_rule

    if multiworld.accessibility[player] != "locations":
        multiworld.get_location("Cerulean Bicycle Shop", player).always_allow = (lambda state, item:
                                                                                   item.name == "Bike Voucher"
                                                                                   and item.player == player)
        multiworld.get_location("Fuchsia Warden's House - Safari Zone Warden", player).always_allow = (lambda state, item:
                                                                                        item.name == "Gold Teeth" and
                                                                                        item.player == player)

    access_rules = {
        "Rival's House - Rival's Sister": lambda state: state.has("Oak's Parcel", player),
        "Oak's Lab - Oak's Post-Route-22-Rival Gift": lambda state: state.has("Oak's Parcel", player),
        "Viridian City - Sleepy Guy": lambda state: logic.can_cut(state, player) or logic.can_surf(state, player),
        "Route 2 Gate - Oak's Aide": lambda state: logic.oaks_aide(state, state.multiworld.oaks_aide_rt_2[player].value + 5, player),
        "Cerulean Bicycle Shop": lambda state: state.has("Bike Voucher", player)
            or location_item_name(state, "Cerulean Bicycle Shop", player) == ("Bike Voucher", player),
        "Lavender Mr. Fuji's House - Mr. Fuji": lambda state: state.has("Fuji Saved", player),
        "Route 11 Gate 2F - Oak's Aide": lambda state: logic.oaks_aide(state, state.multiworld.oaks_aide_rt_11[player].value + 5, player),
        "Celadon City - Stranded Man": lambda state: logic.can_surf(state, player),
        "Fuchsia Warden's House - Safari Zone Warden": lambda state: state.has("Gold Teeth", player)
            or location_item_name(state, "Fuchsia Warden's House - Safari Zone Warden", player) == ("Gold Teeth", player),
        "Route 12 - Island Item": lambda state: logic.can_surf(state, player),
        "Route 15 Gate 2F - Oak's Aide": lambda state: logic.oaks_aide(state, state.multiworld.oaks_aide_rt_15[player].value + 5, player),
        "Route 25 - Item": lambda state: logic.can_cut(state, player),
        "Fuchsia Warden's House - Behind Boulder Item": lambda state: logic.can_strength(state, player),
        "Safari Zone Center - Island Item": lambda state: logic.can_surf(state, player),
        "Saffron Copycat's House 2F - Copycat": lambda state: state.has("Buy Poke Doll", player),

        "Celadon Game Corner - West Gambler's Gift": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Center Gambler's Gift": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - East Gambler's Gift": lambda state: state.has("Coin Case", player),
        "Celadon Game Corner - Hidden Item Northwest By Counter": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item Southwest Corner": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item Near Rumor Man": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item Near Speculating Woman": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item Near West Gifting Gambler": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item Near Wonderful Time Woman": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item Near Failing Gym Information Guy": lambda state: state.has( "Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item Near East Gifting Gambler": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item Near Hooked Guy": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item at End of Horizontal Machine Row": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),
        "Celadon Game Corner - Hidden Item in Front of Horizontal Machine Row": lambda state: state.has("Coin Case", player) and logic.can_get_hidden_items(state, player),

        "Celadon Prize Corner - Item Prize 1": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        "Celadon Prize Corner - Item Prize 2": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        "Celadon Prize Corner - Item Prize 3": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        
        "Celadon Prize Corner - Pokemon Prize - 1": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        "Celadon Prize Corner - Pokemon Prize - 2": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        "Celadon Prize Corner - Pokemon Prize - 3": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        "Celadon Prize Corner - Pokemon Prize - 4": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        "Celadon Prize Corner - Pokemon Prize - 5": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        "Celadon Prize Corner - Pokemon Prize - 6": lambda state: state.has("Coin Case", player) and state.has("Game Corner", player),
        "Cinnabar Lab Fossil Room - Old Amber Pokemon": lambda state: state.has("Old Amber", player) and state.has("Cinnabar Island", player),
        "Cinnabar Lab Fossil Room - Helix Fossil Pokemon": lambda state: state.has("Helix Fossil", player) and state.has("Cinnabar Island", player),
        "Cinnabar Lab Fossil Room - Dome Fossil Pokemon": lambda state: state.has("Dome Fossil", player) and state.has("Cinnabar Island", player),
        "Route 12 - Sleeping Pokemon": lambda state: state.has("Poke Flute", player),
        "Route 16 - Sleeping Pokemon": lambda state: state.has("Poke Flute", player),
        "Seafoam Islands B4F - Legendary Pokemon": lambda state: logic.can_strength(state, player) and state.has("Seafoam Boss Boulders", player),
        "Vermilion Dock - Legendary Pokemon": lambda state: logic.can_surf(state, player),
        "Cerulean Cave B1F - Legendary Pokemon": lambda state: logic.can_surf(state, player),

        **{f"Pokemon Tower {floor}F - Wild Pokemon - {slot}": lambda state: state.has("Silph Scope", player) for floor in range(3, 8) for slot in range(1, 11)},
        "Pokemon Tower 6F - Restless Soul": lambda state: state.has("Silph Scope", player),  # just for level scaling

        "Silph Co 1F - Receptionist": lambda state: state.has("Silph Co Liberated", player),
        "Silph Co 5F - Hostage": lambda state: logic.card_key(state, 5, player),
        "Silph Co 7F - Hostage": lambda state: logic.card_key(state, 7, player),

        "Route 2 Trade House - Marcel Trade": lambda state: state.can_reach("Route 24 - Wild Pokemon - 6", "Location", player),
        "Underground Path Route 5 - Spot Trade": lambda state: state.can_reach("Route 24 - Wild Pokemon - 6", "Location", player),
        "Route 11 Gate 2F - Terry Trade": lambda state: state.can_reach("Safari Zone Center - Wild Pokemon - 5", "Location", player),
        "Route 18 Gate 2F - Marc Trade": lambda state: state.can_reach("Route 23/Cerulean Cave Fishing - Super Rod Pokemon - 1", "Location", player),
        "Cinnabar Lab Fossil Room - Sailor Trade": lambda state: state.can_reach("Pokemon Mansion 1F - Wild Pokemon - 3", "Location", player),
        "Cinnabar Lab Trade Room - Crinkles Trade": lambda state: state.can_reach("Route 12 - Wild Pokemon - 4", "Location", player),
        "Cinnabar Lab Trade Room - Doris Trade": lambda state: state.can_reach("Cerulean Cave 1F - Wild Pokemon - 9", "Location", player),
        "Vermilion Trade House - Dux Trade": lambda state: state.can_reach("Route 3 - Wild Pokemon - 2", "Location", player),
        "Cerulean Trade House - Lola Trade": lambda state: state.can_reach("Route 10/Celadon Fishing - Super Rod Pokemon - 1", "Location", player),

        "Route 22 - Trainer Parties": lambda state: state.has("Oak's Parcel", player),

        # # Rock Tunnel
        "Rock Tunnel 1F - PokeManiac": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel 1F - Hiker 1": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel 1F - Hiker 2": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel 1F - Hiker 3": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel 1F - Jr. Trainer F 1": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel 1F - Jr. Trainer F 2": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel 1F - Jr. Trainer F 3": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - PokeManiac 1": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - PokeManiac 2": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - PokeManiac 3": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - Jr. Trainer F 1": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - Jr. Trainer F 2": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - Hiker 1": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - Hiker 2": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - Hiker 3": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - North Item": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - Northwest Item": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - Southwest Item": lambda state: logic.rock_tunnel(state, player),
        "Rock Tunnel B1F - West Item": lambda state: logic.rock_tunnel(state, player),

        # Pokédex check
        "Oak's Lab - Oak's Parcel Reward": lambda state: state.has("Oak's Parcel", player),

        # Hidden items
        "Viridian Forest - Hidden Item Northwest by Trainer": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Viridian Forest - Hidden Item Entrance Tree": lambda state: logic.can_get_hidden_items(state, player),
        "Mt Moon B2F - Hidden Item Dead End Before Fossils": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Route 25 - Hidden Item Fence Outside Bill's House": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Route 9 - Hidden Item Bush By Grass": lambda state: logic.can_get_hidden_items(state, player),
        "S.S. Anne Kitchen - Hidden Item Kitchen Trash": lambda state: logic.can_get_hidden_items(state, player),
        "S.S. Anne B1F Rooms - Hidden Item Under Pillow": lambda state: logic.can_get_hidden_items(state, player),
        "Route 10 - Hidden Item Behind Rock Tunnel Entrance Cuttable Tree": lambda
            state: logic.can_get_hidden_items(state, player) and logic.can_cut(state, player),
        "Route 10 - Hidden Item Bush": lambda state: logic.can_get_hidden_items(state, player),
        "Rocket Hideout B1F - Hidden Item Pot Plant": lambda state: logic.can_get_hidden_items(state, player),
        "Rocket Hideout B3F - Hidden Item Near East Item": lambda state: logic.can_get_hidden_items(state, player),
        "Rocket Hideout B4F - Hidden Item Behind Giovanni": lambda state:
            logic.can_get_hidden_items(state, player),
        "Pokemon Tower 5F - Hidden Item Near West Staircase": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Route 13 - Hidden Item Dead End Bush": lambda state: logic.can_get_hidden_items(state, player),
        "Route 13 - Hidden Item Dead End By Water Corner": lambda state: logic.can_get_hidden_items(state, player),
        "Pokemon Mansion B1F - Hidden Item Secret Key Room Corner": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Safari Zone West - Hidden Item Secret House Statue": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Silph Co 5F - Hidden Item Pot Plant": lambda state: logic.can_get_hidden_items(state, player),
        "Silph Co 9F - Hidden Item Nurse Bed": lambda state: logic.can_get_hidden_items(state, player),
        "Saffron Copycat's House 2F - Hidden Item Desk": lambda state: logic.can_get_hidden_items(state, player),
        "Cerulean Cave 1F - Hidden Item Center Rocks": lambda state: logic.can_get_hidden_items(state, player),
        "Cerulean Cave B1F - Hidden Item Northeast Rocks": lambda state: logic.can_get_hidden_items(state, player),
        "Power Plant - Hidden Item Central Dead End": lambda state: logic.can_get_hidden_items(state, player),
        "Power Plant - Hidden Item Before Zapdos": lambda state: logic.can_get_hidden_items(state, player),
        "Seafoam Islands B2F - Hidden Item Rock": lambda state: logic.can_get_hidden_items(state, player),
        "Seafoam Islands B3F - Hidden Item Rock": lambda state: logic.can_get_hidden_items(state, player),
        # if you can reach any exit boulders, that means you can drop into the water tunnel and auto-surf
        "Seafoam Islands B4F - Hidden Item Corner Island": lambda state: logic.can_get_hidden_items(state, player),
        "Pokemon Mansion 1F - Hidden Item Block Near Entrance Carpet": lambda
            state: logic.can_get_hidden_items(state, player),
        "Pokemon Mansion 3F - Hidden Item Behind Burglar": lambda state: logic.can_get_hidden_items(state, player),
        "Route 23 - Hidden Item Rocks Before Victory Road": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Route 23 - Hidden Item East Bush After Water": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Route 23 - Hidden Item On Island": lambda state: logic.can_get_hidden_items(state, 
            player) and logic.can_surf(state, player),
        "Victory Road 2F - Hidden Item Rock Before Moltres": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Victory Road 2F - Hidden Item Rock In Final Room": lambda state: logic.can_get_hidden_items(state, player),
        "Viridian City - Hidden Item Cuttable Tree": lambda state: logic.can_get_hidden_items(state, player),
        "Route 11 - Hidden Item Isolated Bush Near Gate": lambda state: logic.can_get_hidden_items(state, player),
        "Route 12 - Hidden Item Bush Near Gate": lambda state: logic.can_get_hidden_items(state, player),
        "Route 17 - Hidden Item In Grass": lambda state: logic.can_get_hidden_items(state, player),
        "Route 17 - Hidden Item Near Northernmost Sign": lambda state: logic.can_get_hidden_items(state, player),
        "Route 17 - Hidden Item East Center": lambda state: logic.can_get_hidden_items(state, player),
        "Route 17 - Hidden Item West Center": lambda state: logic.can_get_hidden_items(state, player),
        "Route 17 - Hidden Item Before Final Bridge": lambda state: logic.can_get_hidden_items(state, player),
        "Underground Path North South - Hidden Item Near Northern Stairs": lambda
            state: logic.can_get_hidden_items(state, player),
        "Underground Path North South - Hidden Item Near Southern Stairs": lambda
            state: logic.can_get_hidden_items(state, player),
        "Underground Path West East - Hidden Item West": lambda state: logic.can_get_hidden_items(state, player),
        "Underground Path West East - Hidden Item East": lambda state: logic.can_get_hidden_items(state, player),
        "Celadon City - Hidden Item Dead End Near Cuttable Tree": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Route 25 - Hidden Item Northeast Of Grass": lambda state: logic.can_get_hidden_items(state, player),
        "Mt Moon B2F - Hidden Item Lone Rock": lambda state: logic.can_get_hidden_items(state, player),
        "Vermilion City - Hidden Item In Water Near Fan Club": lambda state: logic.can_get_hidden_items(state, 
            player) and logic.can_surf(state, player),
        "Cerulean City - Hidden Item Gym Badge Guy's Backyard": lambda state: logic.can_get_hidden_items(state, 
            player),
        "Route 4 - Hidden Item Plateau East Of Mt Moon": lambda state: logic.can_get_hidden_items(state, player),

        # Evolutions
        "Evolution - Ivysaur": lambda state: state.has("Bulbasaur", player) and logic.evolve_level(state, 16, player),
        "Evolution - Venusaur": lambda state: state.has("Ivysaur", player) and logic.evolve_level(state, 32, player),
        "Evolution - Charmeleon": lambda state: state.has("Charmander", player) and logic.evolve_level(state, 16, player),
        "Evolution - Charizard": lambda state: state.has("Charmeleon", player) and logic.evolve_level(state, 36, player),
        "Evolution - Wartortle": lambda state: state.has("Squirtle", player) and logic.evolve_level(state, 16, player),
        "Evolution - Blastoise": lambda state: state.has("Wartortle", player) and logic.evolve_level(state, 36, player),
        "Evolution - Metapod": lambda state: state.has("Caterpie", player) and logic.evolve_level(state, 7, player),
        "Evolution - Butterfree": lambda state: state.has("Metapod", player) and logic.evolve_level(state, 10, player),
        "Evolution - Kakuna": lambda state: state.has("Weedle", player) and logic.evolve_level(state, 7, player),
        "Evolution - Beedrill": lambda state: state.has("Kakuna", player) and logic.evolve_level(state, 10, player),
        "Evolution - Pidgeotto": lambda state: state.has("Pidgey", player) and logic.evolve_level(state, 18, player),
        "Evolution - Pidgeot": lambda state: state.has("Pidgeotto", player) and logic.evolve_level(state, 36, player),
        "Evolution - Raticate": lambda state: state.has("Rattata", player) and logic.evolve_level(state, 20, player),
        "Evolution - Fearow": lambda state: state.has("Spearow", player) and logic.evolve_level(state, 20, player),
        "Evolution - Arbok": lambda state: state.has("Ekans", player) and logic.evolve_level(state, 22, player),
        "Evolution - Raichu": lambda state: state.has("Pikachu", player) and state.has("Thunder Stone", player),
        "Evolution - Sandslash": lambda state: state.has("Sandshrew", player) and logic.evolve_level(state, 22, player),
        "Evolution - Nidorina": lambda state: state.has("Nidoran F", player) and logic.evolve_level(state, 16, player),
        "Evolution - Nidoqueen": lambda state: state.has("Nidorina", player) and state.has("Moon Stone", player),
        "Evolution - Nidorino": lambda state: state.has("Nidoran M", player) and logic.evolve_level(state, 16, player),
        "Evolution - Nidoking": lambda state: state.has("Nidorino", player) and state.has("Moon Stone", player),
        "Evolution - Clefable": lambda state: state.has("Clefairy", player) and state.has("Moon Stone", player),
        "Evolution - Ninetales": lambda state: state.has("Vulpix", player) and state.has("Fire Stone", player),
        "Evolution - Wigglytuff": lambda state: state.has("Jigglypuff", player) and state.has("Moon Stone", player),
        "Evolution - Golbat": lambda state: state.has("Zubat", player) and logic.evolve_level(state, 22, player),
        "Evolution - Gloom": lambda state: state.has("Oddish", player) and logic.evolve_level(state, 21, player),
        "Evolution - Vileplume": lambda state: state.has("Gloom", player) and state.has("Leaf Stone", player),
        "Evolution - Parasect": lambda state: state.has("Paras", player) and logic.evolve_level(state, 24, player),
        "Evolution - Venomoth": lambda state: state.has("Venonat", player) and logic.evolve_level(state, 31, player),
        "Evolution - Dugtrio": lambda state: state.has("Diglett", player) and logic.evolve_level(state, 26, player),
        "Evolution - Persian": lambda state: state.has("Meowth", player) and logic.evolve_level(state, 28, player),
        "Evolution - Golduck": lambda state: state.has("Psyduck", player) and logic.evolve_level(state, 33, player),
        "Evolution - Primeape": lambda state: state.has("Mankey", player) and logic.evolve_level(state, 28, player),
        "Evolution - Arcanine": lambda state: state.has("Growlithe", player) and state.has("Fire Stone", player),
        "Evolution - Poliwhirl": lambda state: state.has("Poliwag", player) and logic.evolve_level(state, 25, player),
        "Evolution - Poliwrath": lambda state: state.has("Poliwhirl", player) and state.has("Water Stone", player),
        "Evolution - Kadabra": lambda state: state.has("Abra", player) and logic.evolve_level(state, 16, player),
        "Evolution - Alakazam": lambda state: state.has("Kadabra", player) and logic.evolve_level(state, 35, player),
        "Evolution - Machoke": lambda state: state.has("Machop", player) and logic.evolve_level(state, 28, player),
        "Evolution - Machamp": lambda state: state.has("Machoke", player) and logic.evolve_level(state, 35, player),
        "Evolution - Weepinbell": lambda state: state.has("Bellsprout", player) and logic.evolve_level(state, 21, player),
        "Evolution - Victreebel": lambda state: state.has("Weepinbell", player) and state.has("Leaf Stone", player),
        "Evolution - Tentacruel": lambda state: state.has("Tentacool", player) and logic.evolve_level(state, 30, player),
        "Evolution - Graveler": lambda state: state.has("Geodude", player) and logic.evolve_level(state, 25, player),
        "Evolution - Golem": lambda state: state.has("Graveler", player) and logic.evolve_level(state, 35, player),
        "Evolution - Rapidash": lambda state: state.has("Ponyta", player) and logic.evolve_level(state, 40, player),
        "Evolution - Slowbro": lambda state: state.has("Slowpoke", player) and logic.evolve_level(state, 37, player),
        "Evolution - Magneton": lambda state: state.has("Magnemite", player) and logic.evolve_level(state, 30, player),
        "Evolution - Dodrio": lambda state: state.has("Doduo", player) and logic.evolve_level(state, 31, player),
        "Evolution - Dewgong": lambda state: state.has("Seel", player) and logic.evolve_level(state, 34, player),
        "Evolution - Muk": lambda state: state.has("Grimer", player) and logic.evolve_level(state, 38, player),
        "Evolution - Cloyster": lambda state: state.has("Shellder", player) and state.has("Water Stone", player),
        "Evolution - Haunter": lambda state: state.has("Gastly", player) and logic.evolve_level(state, 25, player),
        "Evolution - Gengar": lambda state: state.has("Haunter", player) and logic.evolve_level(state, 35, player),
        "Evolution - Hypno": lambda state: state.has("Drowzee", player) and logic.evolve_level(state, 26, player),
        "Evolution - Kingler": lambda state: state.has("Krabby", player) and logic.evolve_level(state, 28, player),
        "Evolution - Electrode": lambda state: state.has("Voltorb", player) and logic.evolve_level(state, 30, player),
        "Evolution - Exeggutor": lambda state: state.has("Exeggcute", player) and state.has("Leaf Stone", player),
        "Evolution - Marowak": lambda state: state.has("Cubone", player) and logic.evolve_level(state, 28, player),
        "Evolution - Weezing": lambda state: state.has("Koffing", player) and logic.evolve_level(state, 35, player),
        "Evolution - Rhydon": lambda state: state.has("Rhyhorn", player) and logic.evolve_level(state, 42, player),
        "Evolution - Seadra": lambda state: state.has("Horsea", player) and logic.evolve_level(state, 32, player),
        "Evolution - Seaking": lambda state: state.has("Goldeen", player) and logic.evolve_level(state, 33, player),
        "Evolution - Starmie": lambda state: state.has("Staryu", player) and state.has("Water Stone", player),
        "Evolution - Gyarados": lambda state: state.has("Magikarp", player) and logic.evolve_level(state, 33, player),
        "Evolution - Vaporeon": lambda state: state.has("Eevee", player) and state.has("Water Stone", player),
        "Evolution - Jolteon": lambda state: state.has("Eevee", player) and state.has("Thunder Stone", player),
        "Evolution - Flareon": lambda state: state.has("Eevee", player) and state.has("Fire Stone", player),
        "Evolution - Omastar": lambda state: state.has("Omanyte", player) and logic.evolve_level(state, 40, player),
        "Evolution - Kabutops": lambda state: state.has("Kabuto", player) and logic.evolve_level(state, 40, player),
        "Evolution - Dragonair": lambda state: state.has("Dratini", player) and logic.evolve_level(state, 30, player),
        "Evolution - Dragonite": lambda state: state.has("Dragonair", player) and logic.evolve_level(state, 55, player),
    }
    for loc in multiworld.get_locations(player):
        if loc.name in access_rules:
            add_rule(loc, access_rules[loc.name])
        if loc.name in item_rules:
            add_item_rule(loc, item_rules[loc.name])
        if loc.name.startswith("Pokedex"):
            mon = loc.name.split(" - ")[1]
            add_rule(loc, lambda state, i=mon: (state.has("Pokedex", player) or not
                     state.multiworld.require_pokedex[player]) and (state.has(i, player)
                                                                    or state.has(f"Static {i}", player)))

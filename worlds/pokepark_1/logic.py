from typing import NamedTuple

from worlds.pokepark_1 import FRIENDSHIP_ITEMS
from worlds.pokepark_1.items import UNLOCK_ITEMS, BERRIES, PRISM_ITEM, POWERS, REGION_UNLOCK


class Unlock(NamedTuple):
    name: str
    id: int


class Friendship(NamedTuple):
    name: str
    id: int


class Prisma(NamedTuple):
    name: str
    id: int


class Requirements(NamedTuple):
    unlocks: list[Unlock] = []
    friendships: list[Friendship] = []
    friendcount: int = 0
    prismas: list[Prisma] = []
    oneof_itemName: list[list[str]] = []

class Location(NamedTuple):
    name: str
    id: int
    requirements: Requirements = Requirements()


class PokeparkRegion(NamedTuple):
    name: str
    display: str
    requirements: Requirements = Requirements()
    friendship_locations: list[Location] = []
    unlock_location: list[Location] = []
    minigame_location: list[Location] = []
    ability_locations: list[Location] = []
    parent_region: str = "Menu"


REGIONS: list[PokeparkRegion] = [
    PokeparkRegion("Pokepark Entrance", "Pokepark Entrance", Requirements(), [
    ]),
    PokeparkRegion("Meadow Zone - Overworld", "Meadow Zone - Overworld", Requirements(),
                   [  # Location("Chikorita", FRIENDSHIP_ITEMS.get("Chikorita"), Requirements()),
                       Location("Bulbasaur", FRIENDSHIP_ITEMS.get("Bulbasaur"), Requirements(prismas=[
                           Prisma("Bulbasaur Prisma", PRISM_ITEM.get("Bulbasaur Prisma"))])),
                       Location("Munchlax", FRIENDSHIP_ITEMS.get("Munchlax"), Requirements(prismas=[
                           Prisma("Bulbasaur Prisma", PRISM_ITEM.get("Bulbasaur Prisma"))])),
                       Location("Tropius", FRIENDSHIP_ITEMS.get("Tropius"),
                                Requirements([Unlock("Tropius Unlock", UNLOCK_ITEMS.get("Tropius Unlock"))], prismas=
                                [Prisma("Bulbasaur Prisma", PRISM_ITEM.get("Bulbasaur Prisma"))])),
                       Location("Turtwig", FRIENDSHIP_ITEMS.get("Turtwig"), Requirements()),
                       Location("Bonsly", FRIENDSHIP_ITEMS.get("Bonsly"),
                                Requirements([Unlock("Bonsly Unlock", UNLOCK_ITEMS.get("Bonsly Unlock"))])),
                       Location("Pachirisu", FRIENDSHIP_ITEMS.get("Pachirisu"),
                                Requirements([Unlock("Pachirisu Unlock", UNLOCK_ITEMS.get("Pachirisu Unlock"))])),
                       Location("Sudowoodo", FRIENDSHIP_ITEMS.get("Sudowoodo"),
                                Requirements([Unlock("Sudowoodo Unlock", UNLOCK_ITEMS.get("Sudowoodo Unlock"))])),
                       Location("Buneary", FRIENDSHIP_ITEMS.get("Buneary"), Requirements()),
                       Location("Shinx", FRIENDSHIP_ITEMS.get("Shinx"),
                                Requirements([Unlock("Shinx Unlock", UNLOCK_ITEMS.get("Shinx Unlock"))])),
                       # Location("Mankey", FRIENDSHIP_ITEMS.get("Mankey"), Requirements()), #throwing out only through event unlockable constricting
                       Location("Spearow", FRIENDSHIP_ITEMS.get("Spearow"), Requirements()),
                       Location("Croagunk", FRIENDSHIP_ITEMS.get("Croagunk"), Requirements()),
                       Location("Lotad", FRIENDSHIP_ITEMS.get("Lotad"),
                                Requirements([Unlock("Lotad Unlock", UNLOCK_ITEMS.get("Lotad Unlock"))])),
                       Location("Treecko", FRIENDSHIP_ITEMS.get("Treecko"), Requirements()),
                       Location("Caterpie", FRIENDSHIP_ITEMS.get("Caterpie"),
                                Requirements([Unlock("Caterpie Unlock", UNLOCK_ITEMS.get("Caterpie Unlock"))])),
                       Location("Butterfree", FRIENDSHIP_ITEMS.get("Butterfree"),
                                Requirements([Unlock("Butterfree Unlock", UNLOCK_ITEMS.get("Butterfree Unlock"))])),
                       Location("Chimchar", FRIENDSHIP_ITEMS.get("Chimchar"),
                                Requirements([Unlock("Chimchar Unlock", UNLOCK_ITEMS.get("Chimchar Unlock"))])),
                       Location("Aipom", FRIENDSHIP_ITEMS.get("Aipom"), Requirements()),
                       Location("Ambipom", FRIENDSHIP_ITEMS.get("Ambipom"),
                                Requirements([Unlock("Ambipom Unlock", UNLOCK_ITEMS.get("Ambipom Unlock"))])),
                       Location("Weedle", FRIENDSHIP_ITEMS.get("Weedle"),
                                Requirements([Unlock("Weedle Unlock", UNLOCK_ITEMS.get("Weedle Unlock"))])),
                       Location("Shroomish", FRIENDSHIP_ITEMS.get("Shroomish"),
                                Requirements([Unlock("Shroomish Unlock", UNLOCK_ITEMS.get("Shroomish Unlock"))])),
                       Location("Magikarp", FRIENDSHIP_ITEMS.get("Magikarp"),
                                Requirements([Unlock("Magikarp Unlock", UNLOCK_ITEMS.get("Magikarp Unlock"))])),
                       Location("Oddish", FRIENDSHIP_ITEMS.get("Oddish"), Requirements()),
                       Location("Bidoof", FRIENDSHIP_ITEMS.get("Bidoof"), Requirements()),
                       Location("Bibarel", FRIENDSHIP_ITEMS.get("Bibarel"),
                                Requirements([Unlock("Bibarel Unlock", UNLOCK_ITEMS.get("Bibarel Unlock"))])),
                       Location("Leafeon", FRIENDSHIP_ITEMS.get("Leafeon"), Requirements(friendcount=21)),
                       # 21 Friend Requirement because Leafana itself is not counting
                       Location("Torterra", FRIENDSHIP_ITEMS.get("Torterra"),
                                Requirements([Unlock("Torterra Unlock", UNLOCK_ITEMS.get("Torterra Unlock"))])),
                       Location("Starly", FRIENDSHIP_ITEMS.get("Starly"),
                                Requirements(oneof_itemName=[["Starly Unlock"],["Starly Unlock 2"]])),
                       Location("Scyther", FRIENDSHIP_ITEMS.get("Scyther"),
                                Requirements(unlocks=[Unlock("Scyther Unlock",UNLOCK_ITEMS.get("Scyther Unlock"))]))
                   ],
                   [Location("Munchlax Friendship Event", UNLOCK_ITEMS.get("Tropius Unlock"), Requirements(prismas=[
                           Prisma("Bulbasaur Prisma", PRISM_ITEM.get("Bulbasaur Prisma"))])),
                    Location("Turtwig Friendship Event", UNLOCK_ITEMS.get("Pachirisu Unlock"), Requirements()),
                    Location("Bonsly Friendship Event", UNLOCK_ITEMS.get("Sudowoodo Unlock"),
                             Requirements([Unlock("Bonsly Unlock", UNLOCK_ITEMS.get("Bonsly Unlock"))])),
                    Location("Buneary Friendship Event", UNLOCK_ITEMS.get("Lotad Unlock"), Requirements()),
                    Location("Croagunk Friendship Event", UNLOCK_ITEMS.get("Scyther Unlock"), Requirements()),
                    Location("Caterpie Tree Dash", UNLOCK_ITEMS.get("Caterpie Unlock"), Requirements()),
                    Location("Caterpie Friendship Event", UNLOCK_ITEMS.get("Butterfree Unlock"),
                             Requirements([Unlock("Caterpie Unlock", UNLOCK_ITEMS.get("Caterpie Unlock"))])),
                    # Location("Mankey Friendship Event", UNLOCK_ITEMS.get("Chimchar Unlock"), Requirements()),
                    Location("Aipom Friendship Event", UNLOCK_ITEMS.get("Ambipom Unlock"), Requirements()),
                    Location("Weedle Tree Dash", UNLOCK_ITEMS.get("Weedle Unlock"), Requirements()),
                    Location("Shroomish Crate Dash", UNLOCK_ITEMS.get("Shroomish Unlock"), Requirements()),
                    Location("Magikarp shocked", UNLOCK_ITEMS.get("Magikarp Unlock"), Requirements()),
                    Location("Bidoof Housing 1", BERRIES.get("10 Berries")+1,
                             Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                    Location("Bidoof Housing 1 - Pokemon Unlock", UNLOCK_ITEMS.get("Bidoof1 Unlock"),
                             Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                    Location("Bidoof Housing 2", BERRIES.get("10 Berries") + 2,
                             Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                    Location("Bidoof Housing 2 - Pokemon Unlock", UNLOCK_ITEMS.get("Bidoof2 Unlock"),
                             Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                    Location("Bidoof Housing 3", BERRIES.get("10 Berries") + 3,
                             Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                    Location("Bidoof Housing 3 - Pokemon Unlock", UNLOCK_ITEMS.get("Bidoof3 Unlock"),
                             Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                    Location("Bidoof Housing 4", BERRIES.get("10 Berries") + 4,
                             Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                    Location("Bidoof Housing 4 - Pokemon Unlock", UNLOCK_ITEMS.get("Bibarel Unlock"),
                             Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                    # Location("Starly Unlock event - Dummy", UNLOCK_ITEMS.get("Starly Unlock"), Requirements([],[],0,[Prisma("Venusaur Prisma",PRISM_ITEM.get("Venusaur Prisma"))])), # not fun since autocomplete and kinda unstable
                    # Location("Starly Unlock event 2 - Dummy", UNLOCK_ITEMS.get("Starly Unlock 2"), Requirements([],[],0,[Prisma("Venusaur Prisma",PRISM_ITEM.get("Venusaur Prisma"))])),
                    # Location("Torterra Unlock event - Dummy", UNLOCK_ITEMS.get("Torterra Unlock"), Requirements([],[],0,[Prisma("Venusaur Prisma",PRISM_ITEM.get("Venusaur Prisma"))])),
                    ], parent_region= "Pokepark Entrance"),
    PokeparkRegion("Treehouse", "Treehouse",
                   ability_locations=[Location("Thunderbolt Upgrade 1", POWERS.get("Progressive Thunderbolt") + 1),
                                      Location("Thunderbolt Upgrade 2", POWERS.get("Progressive Thunderbolt") + 2),
                                      Location("Thunderbolt Upgrade 3", POWERS.get("Progressive Thunderbolt") + 3),
                                      Location("Dash Upgrade 1", POWERS.get("Progressive Dash") +1,Requirements(prismas=[Prisma("Pelipper Prisma",PRISM_ITEM.get("Pelipper Prisma"))])),
                                      Location("Dash Upgrade 2", POWERS.get("Progressive Dash")+2,Requirements(prismas=[Prisma("Pelipper Prisma",PRISM_ITEM.get("Pelipper Prisma"))])),
                                      Location("Dash Upgrade 3", POWERS.get("Progressive Dash")+3,Requirements(prismas=[Prisma("Pelipper Prisma",PRISM_ITEM.get("Pelipper Prisma"))])),
                                      Location("Health Upgrade 1", POWERS.get("Progressive Health") + 1, Requirements(
                                          unlocks=[Unlock("Beach Zone Unlock",REGION_UNLOCK.get("Beach Zone Unlock"))])),
                                      Location("Health Upgrade 2", POWERS.get("Progressive Health") + 2, Requirements(
                                          unlocks=[Unlock("Beach Zone Unlock",REGION_UNLOCK.get("Beach Zone Unlock"))])),
                                      Location("Health Upgrade 3", POWERS.get("Progressive Health") + 3, Requirements(
                                          unlocks=[Unlock("Beach Zone Unlock",REGION_UNLOCK.get("Beach Zone Unlock"))]))
],
                   parent_region="Meadow Zone - Overworld"),
    PokeparkRegion("Meadow Zone - Bulbasaur's Daring Dash Minigame", "Meadow Zone - Bulbasaur's Daring Dash Minigame",
                   minigame_location=
                   [Location("Prisma", PRISM_ITEM.get("Bulbasaur Prisma")),
                    Location("Pikachu", BERRIES.get("100 Berries") + 1),
                    Location("Turtwig", BERRIES.get("100 Berries") + 2,
                             Requirements(friendships=[Friendship("Turtwig", FRIENDSHIP_ITEMS.get("Turtwig"))])),
                    Location("Munchlax", BERRIES.get("100 Berries") + 3,
                             Requirements(friendships=[Friendship("Munchlax", FRIENDSHIP_ITEMS.get("Munchlax"))])),
                    Location("Chimchar", BERRIES.get("100 Berries") + 4,
                             Requirements(friendships=[Friendship("Chimchar", FRIENDSHIP_ITEMS.get("Chimchar"))])),
                    Location("Treecko", BERRIES.get("100 Berries") + 5,
                             Requirements(friendships=[Friendship("Treecko", FRIENDSHIP_ITEMS.get("Treecko"))])),
                    Location("Bibarel", BERRIES.get("100 Berries") + 6,
                             Requirements(friendships=[Friendship("Bibarel", FRIENDSHIP_ITEMS.get("Bibarel"))])),
                    Location("Bulbasaur", BERRIES.get("100 Berries") + 7,
                             Requirements(friendships=[Friendship("Bulbasaur", FRIENDSHIP_ITEMS.get("Bulbasaur"))])),
                    Location("Bidoof", BERRIES.get("100 Berries") + 8,
                             Requirements(friendships=[Friendship("Bidoof", FRIENDSHIP_ITEMS.get("Bidoof"))])),
                    Location("Oddish", BERRIES.get("100 Berries") + 9,
                             Requirements(friendships=[Friendship("Oddish", FRIENDSHIP_ITEMS.get("Oddish"))])),
                    Location("Shroomish", BERRIES.get("100 Berries") + 10,
                             Requirements(friendships=[Friendship("Shroomish", FRIENDSHIP_ITEMS.get("Shroomish"))])),
                    Location("Bonsly", BERRIES.get("100 Berries") + 11,
                             Requirements(friendships=[Friendship("Bonsly", FRIENDSHIP_ITEMS.get("Bonsly"))])),
                    Location("Lotad", BERRIES.get("100 Berries") + 12,
                             Requirements(friendships=[Friendship("Lotad", FRIENDSHIP_ITEMS.get("Lotad"))])),
                    Location("Weedle", BERRIES.get("100 Berries") + 13,
                             Requirements(friendships=[Friendship("Weedle", FRIENDSHIP_ITEMS.get("Weedle"))])),
                    Location("Caterpie", BERRIES.get("100 Berries") + 14,
                             Requirements(friendships=[Friendship("Caterpie", FRIENDSHIP_ITEMS.get("Caterpie"))])),
                    Location("Magikarp", BERRIES.get("100 Berries") + 15,
                             Requirements(friendships=[Friendship("Magikarp", FRIENDSHIP_ITEMS.get("Magikarp"))])),
                    # Location("Jolteon", BERRIES.get("100 Berries")+16, Requirements([], [Friendship("Jolteon", FRIENDSHIP_ITEMS.get("Jolteon"))])), # not implemented yet
                    # Location("Arcanine", BERRIES.get("100 Berries")+17, Requirements([], [Friendship("Arcanine", FRIENDSHIP_ITEMS.get("Arcanine"))])), #not implemented yet
                    Location("Leafeon", BERRIES.get("100 Berries") + 18,
                             Requirements(friendships=[Friendship("Leafeon", FRIENDSHIP_ITEMS.get("Leafeon"))])),
                    Location("Scyther", BERRIES.get("100 Berries")+19,Requirements([], [Friendship("Scyther", FRIENDSHIP_ITEMS.get("Scyther"))])),
                    # Location("Ponyta", BERRIES.get("100 Berries")+20, Requirements([], [Friendship("Ponyta", FRIENDSHIP_ITEMS.get("Ponyta"))])), #not implemented yet
                    Location("Shinx", BERRIES.get("100 Berries") + 21,
                             Requirements(friendships=[Friendship("Shinx", FRIENDSHIP_ITEMS.get("Shinx"))])),
                    # Location("Eevee", BERRIES.get("100 Berries")+22, Requirements([], [Friendship("Eevee", FRIENDSHIP_ITEMS.get("Eevee"))])), # not implemented yet
                    Location("Pachirisu", BERRIES.get("100 Berries") + 23,
                             Requirements(friendships=[Friendship("Pachirisu", FRIENDSHIP_ITEMS.get("Pachirisu"))])),
                    Location("Buneary", BERRIES.get("100 Berries") + 24,
                             Requirements(friendships=[Friendship("Buneary", FRIENDSHIP_ITEMS.get("Buneary"))])),
                    Location("Croagunk", BERRIES.get("100 Berries") + 25,
                             Requirements(friendships=[Friendship("Croagunk", FRIENDSHIP_ITEMS.get("Croagunk"))])),
                    ], parent_region="Meadow Zone - Overworld"),

    PokeparkRegion("Meadow Zone - Venusaur's Vine Swing", "Meadow Zone - Venusaur's Vine Swing",
                   Requirements(oneof_itemName=[["Croagunk","Spearow"],["Beach Zone Unlock"]]),
                   # needs croagunk and spearow friendship
                   minigame_location=[
                       Location("Prisma", PRISM_ITEM.get("Venusaur Prisma")),
                       Location("Pikachu", BERRIES.get("100 Berries") + 26),
                       Location("Munchlax", BERRIES.get("100 Berries") + 27,
                                Requirements(friendships=[Friendship("Munchlax", FRIENDSHIP_ITEMS.get("Munchlax"))])),
                       Location("Magikarp", BERRIES.get("100 Berries") + 28,
                                Requirements(friendships=[Friendship("Magikarp", FRIENDSHIP_ITEMS.get("Magikarp"))])),
                       # Location("Blaziken", BERRIES.get("100 Berries") + 29, Requirements([], [Friendship("Blaziken", FRIENDSHIP_ITEMS.get("Blaziken"))])),
                       # Location("Infernape", BERRIES.get("100 Berries") + 30, Requirements([], [Friendship("Infernape", FRIENDSHIP_ITEMS.get("Infernape"))])),
                       # Location("Lucario", BERRIES.get("100 Berries") + 31, Requirements([], [Friendship("Lucario", FRIENDSHIP_ITEMS.get("Lucario"))])),
                       # Location("Primeape", BERRIES.get("100 Berries") + 32, Requirements([], [Friendship("Primeape", FRIENDSHIP_ITEMS.get("Primeape"))])),
                       # Location("Tangrowth", BERRIES.get("100 Berries") + 33, Requirements([], [Friendship("Tangrowth", FRIENDSHIP_ITEMS.get("Tangrowth"))])),
                       Location("Ambipom", BERRIES.get("100 Berries") + 34,
                                Requirements(friendships=[Friendship("Ambipom", FRIENDSHIP_ITEMS.get("Ambipom"))])),
                       Location("Croagunk", BERRIES.get("100 Berries") + 35,
                                Requirements(friendships=[Friendship("Croagunk", FRIENDSHIP_ITEMS.get("Croagunk"))])),
                       Location("Mankey", BERRIES.get("100 Berries") + 36,
                                Requirements(friendships=[Friendship("Mankey", FRIENDSHIP_ITEMS.get("Mankey"))])),
                       Location("Aipom", BERRIES.get("100 Berries") + 37,
                                Requirements(friendships=[Friendship("Aipom", FRIENDSHIP_ITEMS.get("Aipom"))])),
                       Location("Chimchar", BERRIES.get("100 Berries") + 38,
                                Requirements(friendships=[Friendship("Chimchar", FRIENDSHIP_ITEMS.get("Chimchar"))])),
                       Location("Treecko", BERRIES.get("100 Berries") + 39,
                                Requirements(friendships=[Friendship("Treecko", FRIENDSHIP_ITEMS.get("Treecko"))])),
                       Location("Pachirisu", BERRIES.get("100 Berries") + 40,
                                Requirements(friendships=[Friendship("Pachirisu", FRIENDSHIP_ITEMS.get("Pachirisu"))])),

                   ], parent_region="Meadow Zone - Overworld"),

    PokeparkRegion("Beach Zone - Overworld", "Beach Zone - Overworld",
                   Requirements(unlocks=[Unlock("Beach Zone Unlock", REGION_UNLOCK.get("Beach Zone Unlock"))]),friendship_locations=[
            Location("Buizel", FRIENDSHIP_ITEMS.get("Buizel")),
            Location("Psyduck", FRIENDSHIP_ITEMS.get("Psyduck")),
            Location("Slowpoke", FRIENDSHIP_ITEMS.get("Slowpoke")),
            Location("Azurill",FRIENDSHIP_ITEMS.get("Azurill")),
            Location("Totodile",FRIENDSHIP_ITEMS.get("Totodile"),Requirements(unlocks=[Unlock("Totodile Unlock",UNLOCK_ITEMS.get("Totodile Unlock"))])),
            Location("Mudkip", FRIENDSHIP_ITEMS.get("Mudkip"),Requirements(unlocks=[Unlock("Mudkip Unlock",UNLOCK_ITEMS.get("Mudkip Unlock"))])),
            Location("Pidgeotto", FRIENDSHIP_ITEMS.get("Pidgeotto")),
            Location("Taillow", FRIENDSHIP_ITEMS.get("Taillow")),
            Location("Wingull", FRIENDSHIP_ITEMS.get("Wingull")),
            Location("Staravia", FRIENDSHIP_ITEMS.get("Staravia")),
            Location("Corsola", FRIENDSHIP_ITEMS.get("Corsola")),
            Location("Floatzel",FRIENDSHIP_ITEMS.get("Floatzel"),Requirements(unlocks=[Unlock("Floatzel Unlock",UNLOCK_ITEMS.get("Floatzel Unlock"))])),
            Location("Vaporeon",FRIENDSHIP_ITEMS.get("Vaporeon"),Requirements(friendcount=31)), # +1 for itself
            Location("Golduck", FRIENDSHIP_ITEMS.get("Golduck"), Requirements(unlocks=[Unlock("Golduck Unlock",UNLOCK_ITEMS.get("Golduck Unlock"))])),
            #Location("Pelipper", FRIENDSHIP_ITEMS.get("Pelipper"),Requirements(prismas=[Prisma("Pelipper Prisma",PRISM_ITEM.get("Pelipper Prisma"))])), #not working like Bulbasaur
            Location("Krabby", FRIENDSHIP_ITEMS.get("Krabby"),
                     Requirements(unlocks=[Unlock("Krabby Unlock",UNLOCK_ITEMS.get("Krabby Unlock"))])),
            Location("Wailord", FRIENDSHIP_ITEMS.get("Wailord")),
            Location("Corphish", FRIENDSHIP_ITEMS.get("Corphish"),Requirements(unlocks=[Unlock("Corphish Unlock",UNLOCK_ITEMS.get("Corphish Unlock"))])),
            #Location("Gyarados", FRIENDSHIP_ITEMS.get("Gyarados"),Requirements(prismas=[Prisma("Gyarados Prisma",PRISM_ITEM.get("Gyarados Prisma"))])), # not workin like Bulbasaur
            Location("Feraligatr", FRIENDSHIP_ITEMS.get("Feraligatr")),
            Location("Starly", FRIENDSHIP_ITEMS.get("Starly") +1000), #1000 offset to differentiate with Meadow Zone Starly

        ],unlock_location=[Location("Buizel Friendship Event",
                                    UNLOCK_ITEMS.get("Floatzel Unlock")),
Location("Psyduck Friendship Event", UNLOCK_ITEMS.get("Golduck Unlock")),
                           Location("Slowpoke Friendship Event", UNLOCK_ITEMS.get("Mudkip Unlock")),
                           Location("Azurill Friendship Event", UNLOCK_ITEMS.get("Totodile Unlock")),
                           Location("Bottle Recycling 1", BERRIES.get("10 Berries")+5),
                           Location("Bottle Recycling 2", BERRIES.get("10 Berries") + 6),
                           Location("Bottle Recycling 2 - Pokemon Unlock", UNLOCK_ITEMS.get("Krabby Unlock")),
                           Location("Bottle Recycling 3", BERRIES.get("10 Berries") + 7),
                           Location("Bottle Recycling 4", BERRIES.get("10 Berries") + 8),
                           Location("Bottle Recycling 4 - Pokemon Unlock", UNLOCK_ITEMS.get("Corphish Unlock")),
                           Location("Bottle Recycling 5", BERRIES.get("10 Berries") + 9),
                           Location("Bottle Recycling 6", BERRIES.get("10 Berries") + 10),

                           ],
                   parent_region="Treehouse"),
    PokeparkRegion("Beach Zone - Pelipper's Circle Circuit","Beach Zone - Pelipper's Circle Circuit",minigame_location=[
        Location("Prisma", PRISM_ITEM.get("Pelipper Prisma")),
        Location("Pikachu", BERRIES.get("100 Berries") + 41,Requirements(unlocks=[Unlock("Pikachu Balloon",UNLOCK_ITEMS.get("Pikachu Balloon"))])), #Ballon item is missing for now
        #Location("Staraptor", BERRIES.get("100 Berries") + 42,Requirements(friendships=[Friendship("Staraptor",FRIENDSHIP_ITEMS.get("Staraptor"))])), # Staraptor missing
        #Location("Togekiss", BERRIES.get("100 Berries") + 43,Requirements(friendships=[Friendship("Togekiss",FRIENDSHIP_ITEMS.get("Togekiss"))])), #togekiss is missing
        #Location("Honchkrow", BERRIES.get("100 Berries") + 44, Requirements(friendships=[Friendship("Honchkrow", FRIENDSHIP_ITEMS.get("Honchkrow"))])), #Honchkrow is missing
        #Location("Gliscor", BERRIES.get("100 Berries") + 45, Requirements(friendships=[Friendship("Gliscor", FRIENDSHIP_ITEMS.get("Gliscor"))])), #Gliscor is missing
        Location("Pelipper", BERRIES.get("100 Berries") + 46, Requirements(friendships=[Friendship("Pelipper", FRIENDSHIP_ITEMS.get("Pelipper"))])),
        Location("Staravia", BERRIES.get("100 Berries") + 47, Requirements(friendships=[Friendship("Staravia", FRIENDSHIP_ITEMS.get("Staravia"))])),
        Location("Pidgeotto", BERRIES.get("100 Berries") + 48, Requirements(friendships=[Friendship("Pidgeotto", FRIENDSHIP_ITEMS.get("Pidgeotto"))])),
        Location("Butterfree", BERRIES.get("100 Berries") + 49,Requirements(friendships=[Friendship("Butterfree", FRIENDSHIP_ITEMS.get("Butterfree"))])),
        Location("Tropius", BERRIES.get("100 Berries") + 50, Requirements(friendships=[Friendship("Tropius", FRIENDSHIP_ITEMS.get("Tropius"))])),
        #Location("Murkrow", BERRIES.get("100 Berries") + 51, Requirements(friendships=[Friendship("Murkrow", FRIENDSHIP_ITEMS.get("Murkrow"))])), # Murkow is missing
        Location("Taillow", BERRIES.get("100 Berries") + 52,
                 Requirements(friendships=[Friendship("Taillow", FRIENDSHIP_ITEMS.get("Taillow"))])),
        Location("Spearow", BERRIES.get("100 Berries") + 53,
                 Requirements(friendships=[Friendship("Spearow", FRIENDSHIP_ITEMS.get("Spearow"))])),
        Location("Starly", BERRIES.get("100 Berries") + 54,
                 Requirements(friendships=[Friendship("Starly", FRIENDSHIP_ITEMS.get("Starly"))])),
        Location("Wingull", BERRIES.get("100 Berries") + 55,
                 Requirements(friendships=[Friendship("Wingull", FRIENDSHIP_ITEMS.get("Wingull"))])),
    ],parent_region="Beach Zone - Overworld"),
    PokeparkRegion("Beach Zone - Gyarados' Aqua Dash", "Beach Zone - Gyarados' Aqua Dash",
                   minigame_location=[
                       Location("Prisma", PRISM_ITEM.get("Gyarados Prisma")),
                       Location("Pikachu",BERRIES.get("100 Berries")+56,Requirements(unlocks=[Unlock("Pikachu Surfboard",UNLOCK_ITEMS.get("Pikachu Surfboard"))])), # Pikachu is missing
                       Location("Psyduck",BERRIES.get("100 Berries")+57, Requirements(friendships=[Friendship("Psyduck",FRIENDSHIP_ITEMS.get("Psyduck"))])),
                       Location("Azurill", BERRIES.get("100 Berries") + 58,
                                Requirements(friendships=[Friendship("Azurill", FRIENDSHIP_ITEMS.get("Azurill"))])),
                       Location("Slowpoke", BERRIES.get("100 Berries") + 59,
                                Requirements(friendships=[Friendship("Slowpoke", FRIENDSHIP_ITEMS.get("Slowpoke"))])),
                       #Location("Empoleon", BERRIES.get("100 Berries") + 60, Requirements(friendships=[Friendship("Empoleon", FRIENDSHIP_ITEMS.get("Empoleon"))])), # Empoleon missing
                       Location("Floatzel", BERRIES.get("100 Berries") + 61,
                                Requirements(friendships=[Friendship("Floatzel", FRIENDSHIP_ITEMS.get("Floatzel"))])),
                       Location("Feraligatr", BERRIES.get("100 Berries") + 62,
                                Requirements(friendships=[Friendship("Feraligatr", FRIENDSHIP_ITEMS.get("Feraligatr"))])),
                       Location("Golduck", BERRIES.get("100 Berries") + 63,
                                Requirements(
                                    friendships=[Friendship("Golduck", FRIENDSHIP_ITEMS.get("Golduck"))])),
                       Location("Vaporeon", BERRIES.get("100 Berries") + 64,
                                Requirements(
                                    friendships=[Friendship("Vaporeon", FRIENDSHIP_ITEMS.get("Vaporeon"))])),
                       #Location("Prinplup", BERRIES.get("100 Berries") + 65,Requirements(friendships=[Friendship("Prinplup", FRIENDSHIP_ITEMS.get("Prinplup"))])),
                       Location("Bibarel", BERRIES.get("100 Berries") + 66,
                                Requirements(
                                    friendships=[Friendship("Bibarel", FRIENDSHIP_ITEMS.get("Bibarel"))])),
                       Location("Buizel", BERRIES.get("100 Berries") + 67,
                                Requirements(
                                    friendships=[Friendship("Buizel", FRIENDSHIP_ITEMS.get("Buizel"))])),
                       Location("Corsola", BERRIES.get("100 Berries") + 68,
                                Requirements(
                                    friendships=[Friendship("Corsola", FRIENDSHIP_ITEMS.get("Corsola"))])),
                       Location("Piplup", BERRIES.get("100 Berries") + 69,
                                Requirements(
                                    friendships=[Friendship("Piplup", FRIENDSHIP_ITEMS.get("Piplup"))])),
                       Location("Lotad", BERRIES.get("100 Berries") + 70,
                                Requirements(
                                    friendships=[Friendship("Lotad", FRIENDSHIP_ITEMS.get("Lotad"))])),
                   ], parent_region="Beach Zone - Overworld"),
    PokeparkRegion("Victory Region", "Victory Region",
                   Requirements(prismas=
                                [Prisma("Bulbasaur Prisma", PRISM_ITEM.get("Bulbasaur Prisma")),Prisma("Venusaur Prisma",PRISM_ITEM.get("Venusaur Prisma")), Prisma("Pelipper Prisma",PRISM_ITEM.get("Pelipper Prisma")), Prisma("Gyarados Prisma",PRISM_ITEM.get("Gyarados Prisma"))]),parent_region="Beach Zone - Overworld")
    # just some Victory Requirements for Demo so that meadow zone can be tested
]

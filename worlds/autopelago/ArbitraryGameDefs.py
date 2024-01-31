from enum import Enum, auto


# keep in sync with Region in the game code
class AutopelagoRegion(Enum):
    # Traveling = auto() # only used by the game
    BeforeBasketball = auto()
    Basketball = auto()
    BeforeMinotaur = auto()
    BeforePrawnStars = auto()
    Minotaur = auto()
    PrawnStars = auto()
    BeforeRestaurant = auto()
    BeforePirateBakeSale = auto()
    Restaurant = auto()
    PirateBakeSale = auto()
    AfterRestaurant = auto()
    AfterPirateBakeSale = auto()
    BowlingBallDoor = auto()
    BeforeGoldfish = auto()
    Goldfish = auto()
    # CompletedGoal = auto() # only used by the game

    def get_location_name(self, i: int):
        match self:
            case AutopelagoRegion.BeforeBasketball:
                return f"pre-basketball #{i}"
            case AutopelagoRegion.Basketball:
                return "basketball"
            case AutopelagoRegion.BeforeMinotaur:
                return f"pre-minotaur #{i}"
            case AutopelagoRegion.BeforePrawnStars:
                return f"pre-prawn stars #{i}"
            case AutopelagoRegion.Minotaur:
                return "minotaur"
            case AutopelagoRegion.PrawnStars:
                return "prawn stars"
            case AutopelagoRegion.BeforeRestaurant:
                return f"pre-restaurant #{i}"
            case AutopelagoRegion.BeforePirateBakeSale:
                return f"pre-pirate bake sale #{i}"
            case AutopelagoRegion.Restaurant:
                return "restaurant"
            case AutopelagoRegion.PirateBakeSale:
                return "pirate bake sale"
            case AutopelagoRegion.AfterRestaurant:
                return f"pre-bowling ball door (from restaurant) #{i}"
            case AutopelagoRegion.AfterPirateBakeSale:
                return f"pre-bowling ball door (from pirate bake sale) #{i}"
            case AutopelagoRegion.BowlingBallDoor:
                return "bowling ball door"
            case AutopelagoRegion.BeforeGoldfish:
                return f"pre-goldfish #{i}"
            case AutopelagoRegion.Goldfish:
                return "goldfish"


GAME_NAME = "Autopelago"

# keep in sync with BASE_ID in the game code
BASE_ID = 300000

# keep in sync with s_numLocationsIn in the game code
num_locations_in = {
    AutopelagoRegion.Basketball: 1,
    AutopelagoRegion.Minotaur: 1,
    AutopelagoRegion.PrawnStars: 1,
    AutopelagoRegion.Restaurant: 1,
    AutopelagoRegion.PirateBakeSale: 1,
    AutopelagoRegion.BowlingBallDoor: 1,
    AutopelagoRegion.Goldfish: 1,

    AutopelagoRegion.BeforeBasketball: 40,
    AutopelagoRegion.BeforeMinotaur: 10,
    AutopelagoRegion.BeforePrawnStars: 10,
    AutopelagoRegion.BeforeRestaurant: 10,
    AutopelagoRegion.BeforePirateBakeSale: 10,
    AutopelagoRegion.AfterRestaurant: 10,
    AutopelagoRegion.AfterPirateBakeSale: 10,
    AutopelagoRegion.BeforeGoldfish: 20,
}

key_item_count = 5 # not including the goal item
rat_item_count_for_balancing = 16
rat_item_count_skip_balancing = 10

total_item_count = sum(location_count for location_count in num_locations_in.values())

prog_item_count = key_item_count + rat_item_count_for_balancing + rat_item_count_skip_balancing + 1
del key_item_count
even_split_item_count = (total_item_count - prog_item_count) // 3

useful_item_count = even_split_item_count
filler_item_count = even_split_item_count
del even_split_item_count

trap_item_count = total_item_count - prog_item_count - useful_item_count - filler_item_count
del prog_item_count
